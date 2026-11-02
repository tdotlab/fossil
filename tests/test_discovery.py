import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fossil.acquire import AcquisitionError
from fossil.inventory import inspect
from fossil.assessment import assess
from fossil.compare import compare
from test_core import CODE


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def test_target_only_discovery_searches_source_symbols_and_evaluates_results(self):
        from fossil.discovery import find_candidates
        p = self.root / "target"
        p.mkdir()
        (p / "engine.py").write_text(CODE)
        inv = inspect(p)
        class SearchService:
            def __init__(self): self.queries = []
            def get(self, route):
                self.queries.append(route)
                if route.startswith("/search/code"):
                    return {"items": [{"repository": {"full_name": "original/strata"}, "html_url": "https://github.com/original/strata/blob/main/engine.py"}]}
                return {"items": []}
        service = SearchService()
        leads, trail = find_candidates({"input": "target", "repository": "new/target", "metadata": {}, "inventory": inv}, inv, service)
        self.assertIn("original/strata", leads)
        self.assertTrue(any("decode_fossil_layers" in q for q in service.queries))
        self.assertTrue(any(e["action"] == "code search" for e in trail))

    def test_repository_found_by_several_code_searches_outranks_single_hits(self):
        from fossil.discovery import find_candidates
        p = self.root / "target"
        p.mkdir()
        (p / "engine.py").write_text(CODE + "\n\ndef reconcile_sediment_layers():\n    pass\n\n\ndef summarize_strata_report():\n    pass\n")
        (p / "other.py").write_text("def calibrate_epoch_offsets():\n    pass\n")
        inv = inspect(p)
        class SearchService:
            def get(self, route):
                if route.startswith("/search/code"):
                    # Alphabetically early noise ranks first in every result list; the true source is always second.
                    return {"items": [{"repository": {"full_name": "aaa/noise-" + str(len(route))}}, {"repository": {"full_name": "zzz/original"}}]}
                return {"items": []}
        leads, _ = find_candidates({"input": "target", "metadata": {}}, inv, SearchService())
        self.assertEqual(next(iter(leads)), "zzz/original")

    def test_credits_inside_vendored_code_rank_below_own_source_credits_and_code_search(self):
        from fossil.discovery import find_candidates
        p = self.root / "target"
        (p / "deps" / "lineedit").mkdir(parents=True)
        (p / "engine.py").write_text("# Adapted from https://github.com/author/snippet\n" + CODE)
        for i in range(4):
            (p / "deps" / "lineedit" / f"README{i}.md").write_text(f"Lineedit is a fork of https://github.com/third/party{i}\n")
        inv = inspect(p)
        class SearchService:
            def get(self, route):
                if route.startswith("/search/code"):
                    return {"items": [{"repository": {"full_name": "original/strata"}}]}
                return {"items": []}
        leads = list(find_candidates({"input": "target", "metadata": {}}, inv, SearchService())[0])
        self.assertEqual(leads[:2], ["original/strata", "author/snippet"])
        self.assertTrue(all(leads.index(f"third/party{i}") > 1 for i in range(4)))

    def test_repository_mentioned_on_many_lines_outranks_single_code_search_hits(self):
        from fossil.discovery import find_candidates
        p = self.root / "target"
        (p / "deps" / "lib").mkdir(parents=True)
        (p / "engine.py").write_text(CODE)
        (p / "NEWS").write_text("".join(f"* Fix crash (https://github.com/thoughtbot/paperclip/issues/{n}, https://github.com/thoughtbot/paperclip/pull/{n})\n" for n in range(12))
                                + "* Uses https://github.com/rails/rails\n* Tested with https://github.com/rails/rails\n")
        (p / "deps" / "lib" / "notes.txt").write_text("".join(f"https://github.com/bundled/dep/issues/{n}\n" for n in range(12)))
        (p / "Cargo.lock").write_text("".join(f'source = "registry+https://github.com/rust-lang/crates.io-index"\n# {n}\n' for n in range(12)))
        (p / ".hound.yml").write_text("".join(f"  StyleGuide: https://github.com/bbatsov/ruby-style-guide#rule-{n}\n" for n in range(12)))
        inv = inspect(p)
        class SearchService:
            def get(self, route):
                if route.startswith("/search/code"):
                    return {"items": [{"repository": {"full_name": f"hit/repo{i}"}} for i in range(5)]}
                return {"items": []}
        leads = find_candidates({"input": "target", "metadata": {}}, inv, SearchService())[0]
        order = list(leads)
        self.assertEqual(order[0], "thoughtbot/paperclip")
        self.assertTrue(any("12 lines" in r for r in leads["thoughtbot/paperclip"]))
        self.assertGreater(order.index("rails/rails"), order.index("hit/repo4"))
        for noise in ("bundled/dep", "rust-lang/crates.io-index", "bbatsov/ruby-style-guide"):
            self.assertGreater(order.index(noise), order.index("hit/repo4"), noise)

    def test_github_pages_links_become_leads_but_not_documentary_references(self):
        from fossil.discovery import find_candidates
        p = self.root / "target"
        p.mkdir()
        (p / "engine.py").write_text(CODE)
        (p / "README.md").write_text("# PDFMiner.six\n\nPDFMiner.six is a fork of PDFMiner (https://euske.github.io/pdfminer/index.html).\n"
                                     "Site: https://someone.github.io/ and https://someone.github.io/index.html\n")
        inv = inspect(p)
        self.assertEqual(inv["references"], [])
        self.assertEqual([r["repository"] for r in inv["page_references"]], ["euske/pdfminer"])
        class SearchService:
            def get(self, route):
                if route.startswith("/search/code"):
                    return {"items": [{"repository": {"full_name": f"hit/repo{i}"}} for i in range(5)]}
                return {"items": []}
        leads = find_candidates({"input": "target", "metadata": {}}, inv, SearchService())[0]
        self.assertEqual(next(iter(leads)), "euske/pdfminer")
        self.assertTrue(any("GitHub Pages" in r for r in leads["euske/pdfminer"]))

    def test_search_terms_pair_definitions_from_core_files_not_imports_or_build_scripts(self):
        p = self.root / "target"
        (p / "scripts").mkdir(parents=True)
        (p / "core.py").write_text("from contextlib import AbstractContextManager\n\n" + CODE + "\n\nclass StrataReconstructor:\n    pass\n")
        (p / "scripts" / "release.py").write_text("def publish_release_notes():\n    pass\n" * 40)
        terms = inspect(p)["search_terms"]
        self.assertEqual(terms[0], ["decode_fossil_layers", "StrataReconstructor"])
        self.assertNotIn("AbstractContextManager", sum(terms, []))
        self.assertNotIn("publish_release_notes", sum(terms, []))

    def test_c_and_shell_definitions_are_searchable_and_shebang_scripts_are_source(self):
        p = self.root / "target"
        p.mkdir()
        (p / "server.c").write_text("#include <stdio.h>\n\nstatic int createClusterNode(int port) {\n    return port;\n}\n\nvoid clusterAddNode(void *n)\n{\n}\n")
        (p / "fetchtool").write_text("#!/usr/bin/env bash\n\nget_window_manager_theme() {\n    echo theme\n}\n")
        inv = inspect(p)
        self.assertIn(["createClusterNode", "clusterAddNode"], inv["search_terms"])
        self.assertIn(["get_window_manager_theme"], inv["search_terms"])
        self.assertTrue(next(f for f in inv["files"] if f["path"] == "fetchtool")["source"])

    def test_php_function_imports_are_not_definitions(self):
        p = self.root / "target"
        p.mkdir()
        (p / "Factory.php").write_text("<?php\nnamespace Strata;\n\nuse function array_key_exists;\nuse function\tis_callable_layer;\n\n"
                                       "final class ServerRequestFactory\n{\n    public static function normalizeServerParams() {}\n}\n")
        terms = inspect(p)["search_terms"]
        self.assertEqual(terms, [["ServerRequestFactory", "normalizeServerParams"]])

    def test_package_name_ignores_subfolder_manifests_and_survives_blanked_json(self):
        p = self.root / "target"
        (p / "website").mkdir(parents=True)
        (p / "website" / "package.json").write_text('{"name": "docs-preview"}')
        self.assertEqual(inspect(p)["package_name"], "")
        (p / "package.json").write_text('{\n  "name": "markdown-it",\n  "version": "4.0.0",\n\n}\n')
        (p / "pyproject.toml").write_text('[project]\nname = "strata"\n')
        self.assertEqual(inspect(p)["package_name"], "strata")
        (p / "pyproject.toml").unlink()
        self.assertEqual(inspect(p)["package_name"], "markdown-it")

    def test_package_name_comes_from_the_root_manifest(self):
        cases = {
            "pyproject.toml": ('[project]\nname = "strata-tools"\n', "strata-tools"),
            "setup.py": ("from setuptools import setup\nsetup(\n    name='pdfminer.six',\n)\n", "pdfminer.six"),
            "Cargo.toml": ('[package]\nname = "yaml-rust2"\nversion = "0.1.0"\n', "yaml-rust2"),
            "package.json": ('{"name": "@colors/colors", "version": "1.5.0"}', "colors"),
            "composer.json": ('{"name": "laminas/laminas-diactoros"}', "laminas-diactoros"),
            "kt-paperclip.gemspec": ("Gem::Specification.new do |s|\n  s.name = \"kt-paperclip\"\nend\n", "kt-paperclip"),
            "go.mod": ("module github.com/gofrs/uuid/v5\n\ngo 1.19\n", "uuid"),
        }
        for manifest, (text, expected) in cases.items():
            p = self.root / manifest.replace(".", "_")
            (p / "vendor" / "dep").mkdir(parents=True)
            (p / manifest).write_text(text)
            (p / "vendor" / "dep" / "package.json").write_text('{"name": "bundled-dependency"}')
            self.assertEqual(inspect(p)["package_name"], expected, manifest)

    def test_without_a_readme_the_repository_search_uses_the_package_name_not_the_folder(self):
        from fossil.discovery import find_candidates
        p = self.root / "subject"
        p.mkdir()
        (p / "engine.py").write_text(CODE)
        (p / "setup.py").write_text("setup(name='strata-tools')\n")
        inv = inspect(p)
        class SearchService:
            def __init__(self): self.queries = []
            def get(self, route):
                self.queries.append(route)
                return {"items": []}
        service = SearchService()
        find_candidates({"input": str(p), "metadata": {}}, inv, service)
        repo_queries = [q for q in service.queries if q.startswith("/search/repositories")]
        self.assertTrue(any("strata-tools" in q for q in repo_queries))
        self.assertFalse(any("subject" in q for q in repo_queries))

    def test_vendored_code_that_sorts_first_cannot_starve_application_token_budget(self):
        p = self.root / "target"
        (p / "deps").mkdir(parents=True)
        (p / "deps" / "lua.c").write_text("int x = 1;\n" * 400)
        (p / "src.c").write_text(CODE)
        with patch("fossil.inventory.MAX_TOTAL_TOKENS", 500):
            inv = inspect(p)
        files = {f["path"]: f for f in inv["files"]}
        self.assertEqual(len(files["src.c"]["tokens"]), files["src.c"]["original_tokens"])
        self.assertLess(len(files["deps/lua.c"]["tokens"]), files["deps/lua.c"]["original_tokens"])
        self.assertTrue(any("deps/lua.c" in w for w in inv["warnings"]))

    def test_operator_exclusions_drop_leads_and_are_disclosed(self):
        from fossil.discovery import find_candidates
        p = self.root / "target"
        p.mkdir()
        (p / "engine.py").write_text(CODE)
        inv = inspect(p)
        class SearchService:
            def get(self, route):
                if route.startswith("/search/code"):
                    return {"items": [{"repository": {"full_name": "Known/Self"}}, {"repository": {"full_name": "original/strata"}}]}
                return {"items": []}
        leads, trail = find_candidates({"input": "target", "metadata": {}}, inv, SearchService(), exclude={"known/self"})
        self.assertNotIn("Known/Self", leads)
        self.assertIn("original/strata", leads)
        self.assertTrue(any(e["action"] == "operator exclusion" and "known/self" in e["detail"] for e in trail))

    def test_documented_influence_stays_a_claim_without_source_overlap(self):
        a, b = self.root / "a", self.root / "b"
        a.mkdir(); b.mkdir()
        (a / "README.md").write_text("Inspired by https://github.com/other/idea\n")
        ia, ib = inspect(a), inspect(b)
        result = assess(compare(ia, ib), {"inventory": ia, "git": {}, "metadata": {}}, {"repository": "other/idea", "git": {}})
        self.assertEqual(result["verdict"], "declared_relationship")
        self.assertIn("not independently proven", result["direction"])

    def test_dependency_link_and_unavailable_search_are_not_hidden_successes(self):
        from fossil.discovery import find_candidates
        p = self.root / "target"; p.mkdir()
        (p / "README.md").write_text("Uses https://github.com/psf/requests for HTTP requests\n")
        inv = inspect(p)
        class Blocked:
            def get(self, route): raise AcquisitionError("HTTP 403: rate limit")
        leads, trail = find_candidates({"input": "target", "inventory": inv, "metadata": {}}, inv, Blocked())
        self.assertIn("psf/requests", leads)
        self.assertTrue(any(e.get("status", "").startswith("failed") for e in trail))
        self.assertFalse(any("proven" in r for r in leads["psf/requests"]))

    def test_single_token_insertion_does_not_destroy_all_fingerprints(self):
        a, b = self.root / "a", self.root / "b"; a.mkdir(); b.mkdir()
        (a / "x.py").write_text(CODE)
        (b / "x.py").write_text("insertion\n" + CODE)
        self.assertEqual(compare(inspect(a), inspect(b))["verdict"], "code_overlap")

    def test_api_cache_offline_and_private_token_not_recorded(self):
        from fossil.github import GitHub
        client = GitHub(self.root / "cache")
        payload = {"full_name": "test/repo", "created_at": "2020-01-01T00:00:00Z"}
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self, *args): return json.dumps(payload).encode()
        with patch("fossil.github.urlopen", return_value=Response()) as transport:
            self.assertEqual(client.get("/repos/test/repo"), payload)
            self.assertEqual(transport.call_count, 1)
        offline = GitHub(self.root / "cache", offline=True)
        self.assertEqual(offline.get("/repos/test/repo"), payload)
        with self.assertRaises(AcquisitionError): offline.get("/repos/missing/repo")
        self.assertEqual(offline.trail[0]["status"], "cached")

    def test_ai_suggestions_must_be_github_repositories(self):
        from fossil.ai import parse_suggestions
        answer = '{"candidates": ["https://github.com/original/project", "http://localhost:8000/key", "../../secret", "other/repo"], "notes": "Unverified"}'
        self.assertEqual(parse_suggestions(answer), ["original/project", "other/repo"])


if __name__ == "__main__": unittest.main()
