"""How discovery spends its candidate budget: classification, ranking, failures and second-hop leads."""
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from fossil.acquire import AcquisitionError, acquire_local, extract_zip
from fossil.case import investigate
from fossil.inventory import context, inspect
from test_core import CODE

LAYERS = CODE.replace("decode_fossil_layers", "measure_strata_drift").replace("sediment_record", "core_sample_entry")
OTHER = '''def tabulate_orbital_period(bodies, gravity_constant):
    catalogue = {}
    for planet_name, semi_major_axis in bodies.items():
        radius_cubed = semi_major_axis ** 3
        orbital_seconds = (radius_cubed / gravity_constant) ** 0.5
        catalogue[planet_name] = round(orbital_seconds / 86400, 3)
    return catalogue
'''


class FakeGitHub:
    """Code search returns fixed hits; acquisition copies local folders standing in for repositories."""

    def __init__(self, repos: dict, hits: list, broken=()):
        self.repos, self.hits, self.broken, self.trail, self.acquired = repos, hits, set(broken), [], []

    def get(self, route):
        if route.startswith("/search/code"):
            return {"items": [{"repository": {"full_name": name}, "path": path} for name, path in self.hits]}
        return {"items": []}

    def acquire(self, value, destination):
        self.acquired.append(value)
        if value in self.broken:
            raise AcquisitionError("ZIP exceeds 10,000 entries")
        info = acquire_local(str(self.repos[value]), destination)
        info.update(input="https://github.com/" + value, repository=value, kind="github", metadata={})
        return info


class LeadTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def repo(self, name, files):
        p = self.root / "repos" / name.replace("/", "--")
        p.mkdir(parents=True)
        for rel, text in files.items():
            (p / rel).parent.mkdir(parents=True, exist_ok=True)
            (p / rel).write_text(text)
        return p

    def test_bundled_directories_and_go_and_js_test_files_are_classified(self):
        self.assertEqual(context("venv311/Lib/site-packages/click/core.py", ""), "vendored/external")
        self.assertEqual(context("pip/_vendor/requests/api.py", ""), "vendored/external")
        self.assertEqual(context("bucket_test.go", ""), "test/example")
        self.assertEqual(context("src/layers.spec.ts", ""), "test/example")
        self.assertEqual(context("src/latest.go", ""), "application")
        self.assertEqual(context("Pods/lua/lapi.c", ""), "vendored/external")
        self.assertEqual(context("public/plugins/codemirror-5.17.0/lib/codemirror.js", ""), "vendored/external")
        self.assertEqual(context("public/plugins/jquery.minicolors-2.2.3/jquery.minicolors.js", ""), "vendored/external")
        self.assertEqual(context("src/parser-v2/lexer.go", ""), "application")
        self.assertEqual(context("lib/release-1.2.js", ""), "application")
        self.assertEqual(context("tests/data/src/pep518-3.0/setup.py", ""), "test/example")

    def test_javascript_function_expressions_are_searchable_definitions(self):
        p = self.repo("js/target", {"lib/strata.js": "Widget.prototype.renderLayerStack = function (layers) {\n  return layers;\n};\n"
                                                      "var computeStrataDepth = function(x) { return x; };\n"
                                                      "const mergeSedimentRuns = (a, b) => a.concat(b);\n"})
        self.assertEqual(inspect(p)["search_terms"][0], ["renderLayerStack", "computeStrataDepth"])

    def test_go_test_and_benchmark_names_are_not_used_as_queries(self):
        p = self.repo("go/target", {"bucket_test.go": "func BenchmarkBucket_CreateBucketIfNotExists(b *testing.B) {}\n" * 50,
                                    "bucket.go": "func (b *Bucket) CreateBucketIfMissing(key []byte) {}\nfunc (b *Bucket) ForEachBucketKey() {}\n"})
        self.assertEqual(inspect(p)["search_terms"], [["CreateBucketIfMissing", "ForEachBucketKey"]])

    def test_code_hits_in_bundled_copies_or_data_files_rank_below_a_project_source_hit(self):
        from fossil.discovery import find_candidates
        p = self.repo("py/target", {"engine.py": CODE})
        inv = inspect(p)
        service = FakeGitHub({}, [("venv/copy", "v/Lib/site-packages/strata/engine.py"), ("bench/report", "raw-data/strata/GRAPH_REPORT.md"),
                                  ("app/bundle", "deps/strata/engine.py"), ("origin/strata", "strata/engine.py"), ("dylan/script", "fetchtool")])
        leads = list(find_candidates({"input": "target", "metadata": {}}, inv, service)[0])
        self.assertEqual(leads[:2], ["origin/strata", "dylan/script"])
        self.assertEqual(set(leads[2:]), {"venv/copy", "bench/report", "app/bundle"})

    def test_failed_acquisition_does_not_use_up_the_candidate_budget(self):
        target = self.repo("t/target", {"engine.py": CODE})
        upstream = self.repo("origin/strata", {"engine.py": CODE})
        service = FakeGitHub({"origin/strata": upstream}, [("junk/huge", "engine.py"), ("origin/strata", "engine.py")], broken={"junk/huge"})
        case = investigate(str(target), [], self.root / "case", discover=True, client=service, max_candidates=1)
        self.assertEqual([c["candidate"]["repository"] for c in case["comparisons"]], ["origin/strata"])
        self.assertTrue(next(l for l in case["leads"] if l["repository"] == "junk/huge")["status"].startswith("failed"))

    def test_failed_acquisitions_are_still_bounded(self):
        target = self.repo("t/target", {"engine.py": CODE})
        service = FakeGitHub({}, [(f"junk/huge{i}", "engine.py") for i in range(6)], broken={f"junk/huge{i}" for i in range(6)})
        investigate(str(target), [], self.root / "case", discover=True, client=service, max_candidates=2)
        self.assertEqual(len(service.acquired), 4)

    def test_old_names_that_redirect_to_the_target_or_an_evaluated_repository_are_not_evaluated(self):
        class Renaming(FakeGitHub):
            renames = {"old/target": "t/target", "old/strata": "origin/strata"}

            def canonical(self, value):
                return self.renames.get(value, value)

        target = self.repo("t/target", {"engine.py": CODE})
        upstream = self.repo("origin/strata", {"engine.py": CODE})
        service = Renaming({"old/strata": upstream, "origin/strata": upstream}, [("old/target", "engine.py"), ("old/strata", "engine.py"), ("origin/strata", "strata/engine.py")])
        case = investigate(str(target), [], self.root / "case", discover=True, client=service, exclude=["t/target"])
        self.assertEqual(service.acquired, ["old/strata"])
        status = {l["repository"]: l["status"] for l in case["leads"]}
        self.assertEqual(status["old/target"], "skipped: excluded (as t/target)")
        self.assertEqual(status["origin/strata"], "skipped: same repository as old/strata")

    def test_a_file_code_search_found_stays_inside_a_large_candidates_sample_and_replays(self):
        from fossil.case import replay

        class Linking(FakeGitHub):
            def get(self, route):
                data = super().get(route)
                for item in data["items"]:
                    item["html_url"] = f"https://github.com/{item['repository']['full_name']}/blob/abc123/{item['path']}"
                return data

        target = self.repo("t/target", {"engine.py": CODE})
        big = self.repo("big/app", {"app/orbit.py": OTHER * 3, "vendor/github.com/origin/strata/engine.py": CODE})
        service = Linking({"big/app": big}, [("big/app", "vendor/github.com/origin/strata/engine.py")])
        budget = len(inspect(big)["files"][0]["tokens"])  # the application file alone fills the sample
        with patch("fossil.inventory.MAX_TOTAL_TOKENS", budget):
            self.assertFalse(next(f for f in inspect(big)["files"] if f["path"].startswith("vendor"))["source"])
            case = investigate(str(target), [], self.root / "case", discover=True, client=service, max_candidates=1)
            self.assertEqual(case["comparisons"][0]["candidate"]["priority_paths"], ["vendor/github.com/origin/strata/engine.py"])
            self.assertEqual(case["comparisons"][0]["verdict"], "component_overlap")
            replay(self.root / "case")

    def test_a_go_vendor_path_in_a_shared_file_names_the_upstream(self):
        from fossil.discovery import second_hop
        copy = self.repo("fan/copy", {"vendor/github.com/origin/strata/engine.py": CODE, "vendor/github.com/origin/strata/layers.py": LAYERS})
        result = {"verdict": "component_overlap", "matches": [{"candidate_path": "vendor/github.com/origin/strata/engine.py"},
                                                              {"candidate_path": "vendor/github.com/origin/strata/layers.py"}]}
        hops = second_hop({"repository": "fan/copy"}, inspect(copy), result, set())
        self.assertEqual([name for name, _ in hops], ["origin/strata"])
        self.assertIn("the path vendor/github.com/origin/strata/", hops[0][1][0])
        cache = {"verdict": "code_overlap", "matches": [{"candidate_path": "pkg/mod/github.com/!burnt!sushi/toml@v1.2.0/lex.go"},
                                                        {"candidate_path": "pkg/mod/github.com/!burnt!sushi/toml@v1.2.0/parse.go"}]}
        self.assertEqual([name for name, _ in second_hop({"repository": "fan/copy"}, {"references": []}, cache, set())], ["BurntSushi/toml"])

    def test_confirmed_copy_that_names_an_upstream_in_shared_files_leads_to_it_next(self):
        target = self.repo("t/target", {"engine.py": CODE, "layers.py": LAYERS})
        copy = self.repo("fan/copy", {"engine.py": "# see https://github.com/origin/strata/issues/12\n" + CODE,
                                      "layers.py": "# see https://github.com/origin/strata/issues/40\n" + LAYERS,
                                      "README.md": "Thanks to https://github.com/unrelated/tool\n"})
        upstream = self.repo("origin/strata", {"engine.py": CODE, "layers.py": LAYERS})
        noise = self.repo("noise/a", {"orbit.py": OTHER})
        service = FakeGitHub({"fan/copy": copy, "origin/strata": upstream, "noise/a": noise, "noise/b": noise},
                             [("fan/copy", "engine.py"), ("noise/a", "orbit.py"), ("noise/b", "orbit.py")])
        case = investigate(str(target), [], self.root / "case", discover=True, client=service, max_candidates=2)
        evaluated = [c["candidate"]["repository"] for c in case["comparisons"]]
        self.assertEqual(evaluated, ["fan/copy", "origin/strata"])
        hop = case["comparisons"][1]
        self.assertEqual(hop["verdict"], "code_overlap")
        self.assertEqual(hop["direction"], "undetermined")
        self.assertTrue(hop["provenance"][0].startswith("Named by confirmed candidate fan/copy in 2 file(s)"))
        self.assertNotIn("unrelated/tool", [l["repository"] for l in case["leads"]])
        self.assertTrue(any(e["action"] == "second-hop lead" for e in case["discovery"]))

    def test_a_single_stray_link_in_a_copy_is_not_followed(self):
        target = self.repo("t/target", {"engine.py": CODE})
        copy = self.repo("fan/copy", {"engine.py": "# see https://github.com/someone/else/issues/1\n" + CODE})
        noise = self.repo("noise/a", {"orbit.py": OTHER})
        service = FakeGitHub({"fan/copy": copy, "noise/a": noise}, [("fan/copy", "engine.py"), ("noise/a", "orbit.py")])
        case = investigate(str(target), [], self.root / "case", discover=True, client=service, max_candidates=2)
        self.assertEqual([c["candidate"]["repository"] for c in case["comparisons"]], ["fan/copy", "noise/a"])

    def test_snippet_credits_and_tooling_links_in_a_copy_are_not_followed_but_a_stated_upstream_in_shared_code_is(self):
        from fossil.discovery import second_hop
        copy = self.repo("fan/copy", {"engine.py": "# Code based on https://github.com/python/cpython/blob/main/x.py\n"
                                                   "# see https://github.com/origin/strata/issues/3\n" + CODE,
                                      ".github/sbom.py": "A = 'https://github.com/google/brotli'\n# https://github.com/google/brotli\n",
                                      "README.md": "A fork of [strata](https://github.com/origin/strata).\n"})
        inv = inspect(copy)
        result = {"verdict": "code_overlap", "matches": [{"candidate_path": "engine.py"}, {"candidate_path": ".github/sbom.py"}]}
        hops = second_hop({"repository": "fan/copy"}, inv, result, set())
        self.assertEqual([name for name, _ in hops], ["origin/strata"])
        self.assertIn("1 file(s) it shares with the target and a relationship statement", hops[0][1][0])

    def test_a_copys_statement_alone_does_not_make_a_second_hop(self):
        from fossil.discovery import second_hop
        copy = self.repo("fan/copy", {"engine.py": CODE, "CHANGELOG/README.md": "This template is adapted from [pytest](https://github.com/pytest-dev/pytest).\n"})
        result = {"verdict": "code_overlap", "matches": [{"candidate_path": "engine.py"}]}
        self.assertEqual(second_hop({"repository": "fan/copy"}, inspect(copy), result, set()), [])

    def test_a_list_entry_describing_the_linked_project_is_not_a_credit(self):
        from fossil.discovery import credits
        self.assertFalse(credits({"repository": "reef-pi/reef-pi", "text": "",
                                  "statement": "* [reef-pi](https://github.com/reef-pi/reef-pi) - a reef controller based on a Raspberry Pi"}))
        self.assertTrue(credits({"repository": "origin/strata", "text": "", "statement": "A fork of [strata](https://github.com/origin/strata)"}))
        self.assertTrue(credits({"repository": "origin/strata", "text": "", "statement": "derived from https://github.com/origin/strata"}))
        self.assertFalse(credits({"repository": "origin/strata", "text": "", "statement": "This is not a fork of https://github.com/origin/strata"}))

    def test_unpinned_snippet_credits_in_target_source_rank_below_code_search_but_commit_pinned_ones_do_not(self):
        from fossil.discovery import find_candidates
        p = self.repo("py/target", {"engine.py": "# Based on: https://github.com/mmap/mmap-go\n"
                                                 "# derived from https://github.com/pinned/util/commit/" + "a" * 40 + "\n" + CODE})
        service = FakeGitHub({}, [("origin/strata", "strata/engine.py")])
        leads = list(find_candidates({"input": "target", "metadata": {}}, inspect(p), service)[0])
        self.assertEqual(leads[:3], ["pinned/util@" + "a" * 40, "origin/strata", "mmap/mmap-go"])

    def test_zip_entry_limit_ignores_directories_that_are_never_extracted(self):
        archive = self.root / "a.zip"
        with zipfile.ZipFile(archive, "w") as z:
            for i in range(3):
                z.writestr(f"src/m{i}.py", "x = 1\n")
            for i in range(10):
                z.writestr(f"node_modules/pkg/f{i}.js", "x\n")
        with patch("fossil.acquire.MAX_FILES", 5):
            extract_zip(archive, self.root / "out")
            with zipfile.ZipFile(archive, "a") as z:
                for i in range(3, 6):
                    z.writestr(f"src/m{i}.py", "x = 1\n")
            with self.assertRaises(AcquisitionError):
                extract_zip(archive, self.root / "out2")


if __name__ == "__main__":
    unittest.main()
