# Discovery benchmark results

Measured 2026-11-01/02 on Windows 11, Python 3.13, with an authenticated GitHub token and default settings (4 evaluated candidates). Method and pair lists: [README.md](README.md). Raw scores: [results/](results/), where `baseline` is 0.1, `v3` is 0.2, `v5` is 0.3, `v6` is 0.4, and `v2`/`v4` are intermediate drafts of 0.2 and 0.3.

**Short version.** On ten pairs no version had seen (holdout3), Fossil 0.4 and 0.3 both found and confirmed the true upstream in 5 of 10, with documentation intact and with it stripped. 0.4 is a cleanup, not a gain: on the in-sample sets it confirms one more upstream than 0.3 (34 of 66 against 33), with fewer wasted evaluations. Holdout3 could barely exercise the change, because none of its five misses carries a GitHub-link credit for ranking to promote. The earlier out-of-sample step (holdout2, 0.2 → 0.3: 4 → 5 of 8 stripped) still stands as the only measured unseen gain. No run of any version confirmed a repository that did not genuinely share code with the target.

## Counts

"Confirmed" means the upstream was among the evaluated candidates and reached a verdict backed by source overlap. "Found" counts the upstream anywhere in the recorded leads. Renamed repositories count as the same upstream (`kyren/rlua` is `mlua-rs/rlua`, `mishoo/UglifyJS2` is `mishoo/UglifyJS`).

| Set | Condition | 0.1 found / confirmed | 0.2 | 0.3 | 0.4 |
|---|---|---|---|---|---|
| tuning (13) | intact | 10 / 6 | 12 / 8 | 12 / 8 | 12 / 8 |
| tuning (13) | stripped | 3 / 1 | 6 / 5 | 7 / 7 | 7 / 7 |
| holdout (6) | intact | not run | 4 / 3 | 4 / 4 | 5 / 5 |
| holdout (6) | stripped | not run | 2 / 2 | 5 / 5 | 4 / 4 |
| holdout2 (8) | intact | not run | 7 / 4 | 7 / 4 | 7 / 5 |
| holdout2 (8) | stripped | not run | 6 / 4 | 6 / 5 | 6 / 5 |
| **holdout3 (10)** | intact | not run | not run | 5 / 5 | 5 / 5 |
| **holdout3 (10)** | stripped | not run | not run | 5 / 5 | 5 / 5 |

Each holdout was committed before the code it measures was written, and run once after that version was frozen: holdout2 for 0.3 (frozen at 1435ee6, against 0.2 from a worktree of 10c3562), holdout3 for 0.4 (frozen at a74062e, against 0.3 from a worktree of a70bd26). The second run of each pair reused the first run's cached searches, so the comparison isolates code changes from changes in GitHub's index. Every set is in-sample for every later version.

## Per pair (upstream lead rank and verdict)

A second-hop lead is listed at the position it was evaluated in, which can be past #4 when failed acquisitions or hops reordered the queue.

Holdout3. 0.3 and 0.4 gave the same result on every pair except where shown:

| Pair | Intact | Stripped |
|---|---|---|
| pdfminer.six ← euske/pdfminer | not found | not found |
| dj-rest-auth ← Tivix/django-rest-auth | #1 code overlap | #1 code overlap |
| markdown-it ← jonschlinkert/remarkable | #1 code overlap | #1 code overlap |
| opentofu ← hashicorp/terraform | #2 (0.3), #1 (0.4) code overlap | #1 code overlap |
| yaml-rust2 ← chyh1990/yaml-rust | #1 corroborated | #1 code overlap |
| zlib-ng ← madler/zlib | not found | not found |
| htop ← hishamhm/htop | not found | not found |
| laminas-diactoros ← zendframework/zend-diactoros | not found | not found |
| kt-paperclip ← thoughtbot/paperclip | not found | not found |
| jellyfin ← MediaBrowser/Emby | #1 code overlap | #1 code overlap |

Holdout2, 0.3 and 0.4:

| Pair | Intact 0.3 | Intact 0.4 | Stripped 0.3 | Stripped 0.4 |
|---|---|---|---|---|
| eza ← ogham/exa | #2 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| terser ← mishoo/UglifyJS | #8 not evaluated | #4 code overlap (second hop) | #4 code overlap (second hop) | #4 code overlap (second hop) |
| golang-jwt ← dgrijalva/jwt-go | #16 not evaluated | #16 not evaluated | not found | not found |
| nextcord ← Rapptz/discord.py | #5 code overlap | #4 code overlap | #5 code overlap | #4 code overlap |
| pycryptodome ← pycrypto/pycrypto | not found | not found | not found | not found |
| angie ← nginx/nginx | #9 not evaluated | #7 not evaluated | #9 not evaluated | #7 not evaluated |
| neovim ← vim/vim | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| mysqlclient ← farcepest/MySQLdb1 | #1 corroborated | #1 corroborated | #1 code overlap | #1 code overlap |

Tuning pairs, 0.3 and 0.4:

| Pair | Intact 0.3 | Intact 0.4 | Stripped 0.3 | Stripped 0.4 |
|---|---|---|---|---|
| django-q2 ← Koed00/django-q | #1 corroborated | #1 corroborated | #1 code overlap | #1 code overlap |
| flask-caching ← thadeusb/flask-cache | #1 corroborated | #1 corroborated | not found | not found |
| flask-restx ← noirbizarre/flask-restplus | #1 corroborated | #1 corroborated | #1 code overlap | #1 code overlap |
| niquests ← psf/requests | #20 not evaluated | #20 not evaluated | not found | not found |
| urllib3-future ← urllib3/urllib3 | #21 not evaluated | #21 not evaluated | not found | not found |
| asyncclick ← pallets/click | #1 component | #4 component | #4 code overlap | #4 code overlap |
| hyfetch ← dylanaraps/neofetch (component) | #19 not evaluated | #19 not evaluated | not found | not found |
| pip ← psf/requests (component) | not found | not found | not found | not found |
| yt-dlp ← ytdl-org/youtube-dl | #2 corroborated | #2 corroborated | #2 code overlap (second hop) | #2 code overlap (second hop) |
| valkey ← redis/redis | #3 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| lodash ← jashkenas/underscore | #21 not evaluated | #21 not evaluated | not found | not found |
| gitea ← gogs/gogs | #3 code overlap | #2 code overlap | #1 code overlap | #1 code overlap |
| pypdf ← mfenniak/pyPdf | #4 code overlap | #4 code overlap | #4 code overlap | #4 code overlap |

First holdout, 0.3 and 0.4:

| Pair | Intact 0.3 | Intact 0.4 | Stripped 0.3 | Stripped 0.4 |
|---|---|---|---|---|
| searxng ← searx/searx | #1 corroborated | #1 corroborated | #4 code overlap | #4 code overlap |
| flask-security ← pallets-eco/flask-security-3.0 | not found | not found | not found | not found |
| pillow-simd ← python-pillow/Pillow | #4 code overlap (second hop) | #3 code overlap (second hop) | #3 code overlap | #3 code overlap |
| postman-request ← request/request | #1 component | #2 component | #2 code overlap | #2 code overlap |
| bbolt ← boltdb/bolt | not found | #4 code overlap (second hop) | #4 code overlap (second hop) | #4 code overlap (second hop) |
| mlua ← mlua-rs/rlua | #1 component overlap | #1 component overlap | #6 component overlap (second hop) | not found |

## What changed in 0.4

Both changes came from 0.3's diagnosed failures:

- **Snippet credits rank below code search.** A "based on X" comment in the target's own source credits a snippet, not the project, so it now ranks below code-search hits unless it pins the exact commit it took. A statement also counts as a credit only when the linked repository is its object ("a fork of X"), not when the phrase describes the linked project ("[reef-pi] - a controller based on a Raspberry Pi"). This freed the slots that bbolt's and terser's intact runs had spent on snippet and list credits; both now reach their upstream, as their stripped runs already did.
- **No statement-only second hops.** A confirmed copy's relationship statement in its own docs strengthens a hop backed by shared files but no longer creates one. Across every 0.3 run such hops produced twelve leads and led to the upstream once (mlua → rlua, through tiny-rlua's README); the rest were a changelog template, a tengine feature list, a bundled module's README, a "projects using bolt" entry and neovim links. That one find is the loss in the table above, and it is the price of the rule.

Hops backed by shared files are unchanged: across both versions they led to the upstream in four of seven distinct cases (Pillow, youtube-dl, boltdb/bolt, UglifyJS).

## Why the misses missed

**No GitHub-link credit** (holdout3: pdfminer.six, kt-paperclip). pdfminer.six's README says it is "a fork of PDFMiner" and links only euske.github.io; kt-paperclip links thoughtbot/paperclip 25 times, all inside issue, changelog and rdoc URLs. Each is a plain mention, which ranks below code-search hits, so thirty hits filled the 24-lead cap first: a repository mentioned 25 times counts no more than one mentioned once. Their stripped runs confirmed copies (PDF tools bundling pdfminer; a non-fork paperclip copy) that do not name the upstream in shared files.

**Copies of the upstream instead of the upstream** (htop, zlib-ng). htop's searches confirmed three unforked copies of htop 2.x at about 50% coverage each, and zlib-ng's a zlib-ng mirror and a bare-metal project bundling zlib; madler/zlib is in thousands of repositories. None of these copies is a GitHub fork or names the upstream in the files they share.

**PHP imports read as definitions** (laminas-diactoros). `use function array_key_exists;` is a PHP import, but the definition pattern takes it for a definition, so two of three queries were PHP builtins. This is a bug.

**Fork-only vocabulary** (niquests, urllib3-future, flask-caching, flask-security). Queries use names defined in the target's largest core files, which in a long-lived fork are mostly written after the split. The hits are committed virtualenvs carrying the *target*; the upstream is absent at any result count.

**Ubiquitous upstreams** (angie, zlib-ng). nginx and zlib code is everywhere; nginx/nginx ranks 7th behind tengine and an annotated nginx tree, both confirmed.

**Borrowed cores** (pycryptodome). Its largest C files are cipher code pycrypto took from older public-domain sources, so the queries lead elsewhere.

**Renamed copies with no credits** (golang-jwt). Repositories carrying jwt-go as an internal package were confirmed, but none names dgrijalva/jwt-go in shared files.

**Component pairs** (hyfetch, pip) query the target's own code, not the bundled component. **lodash** at its pinned commit is one file and yields a single query.

## Next round

Ranking is no longer where the misses are; better queries are. In rough order of expected value: replace the no-README fallback repository search, which currently searches for the subject's folder name ("subject" in every stripped bench run), with the package's declared name from its manifest (setup.py, pyproject, Cargo.toml, go.mod, gemspec, composer.json, package.json); let a repository the target's docs mention many times outrank single code-search hits; fix PHP `use function` imports; map `owner.github.io/repo` links to `owner/repo`; pick some queries from files more likely to predate a fork. Then the direction problem, where repository creation order is a weak but cheap hint. Each needs a fresh holdout; holdout3 is now in-sample.

## Other repositories that reached a confirming verdict

Every one was checked by hand (description and matched files). None was a spurious match.

- **Copies or bundles of the target.** Download-manager and Kodi add-ons carrying `yt_dlp/`, mlua forks, a TypeScript port of terser, apps vendoring flask-restx, asyncclick, dj-rest-auth or jwt-go as internal packages, pipenv vendoring pip, bbolt packaging, a Flask-Security-Too copy, a jellyfin hardware-decoding fork, an OpenTofu variant and an infrastructure tool built from its code, two sites bundling markdown-it 2.2.1 for benchmarks, a cgo binding bundling zlib-ng, saphyr.
- **Copies of, or links in, the upstream's lineage.** yt-dlc, a PyPDF2 mirror, exa forks, annotated Redis and nginx trees, tengine, a detached gogs fork, disnake and qq.py, MySQL-for-Python-3 and moist, vim.wasm, Pillow packaging, three htop 2.x builds, a paperclip copy, an old terraform copy, mini-v8 (one file borrowed from rlua).
- **Projects vendoring the same third-party code.** Blender add-ons bundling PIL, a test tool bundling `request`, GlowScript bundling uglify-es, PDF tools bundling pdfminer, a bare-metal project bundling zlib, two Rust crates carrying yaml-rust's emitter.

Fossil reports all of these as overlap with undetermined direction, which is correct. It cannot yet tell an ancestor from a descendant without Git history or an acknowledgement, and with acknowledgements stripped it more often finds descendants than ancestors.

## Limits of this measurement

Thirty-seven pairs across Python, Go, Rust, JavaScript, C, C#, PHP and Ruby, all public on GitHub. Each holdout has eight to ten pairs, so a one-pair difference is suggestive at best. Results depend on GitHub's live code index, which changes. Earlier sets have been used repeatedly and overstate what the next unseen pairs will show.
