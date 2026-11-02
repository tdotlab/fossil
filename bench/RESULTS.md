# Discovery benchmark results

Measured 2026-11-01/02 on Windows 11, Python 3.13, with an authenticated GitHub token and default settings (4 evaluated candidates). Method and pair lists: [README.md](README.md). Raw scores: [results/](results/), where `baseline` is 0.1, `v3` is 0.2, `v5` is 0.3, `v6` is 0.4, `v7` is 0.5, and `v2`/`v4` are intermediate drafts of 0.2 and 0.3.

**Short version.** On ten pairs no version had seen (holdout4), Fossil 0.5 and 0.4 both found and confirmed the true upstream in 11 of 20 runs (6 intact, 5 stripped). The 0.5 changes did what they were built for on the pairs that motivated them, raising the in-sample total from 44 to 48 of 74 with no losses, but none of holdout4's misses had the shape they fix. Two unseen rounds in a row have now come out flat, so the in-sample gains of 0.4 and 0.5 are best read as fixes for known failures, not as evidence of better discovery in general. The only measured unseen gain is still holdout2 (0.2 → 0.3: 4 → 5 of 8 stripped). No run of any version confirmed a repository that did not genuinely share code with the target, though 0.5 exposed a bug where the target is evaluated against itself under an old repository name (see below).

## Counts

"Confirmed" means the upstream was among the evaluated candidates and reached a verdict backed by source overlap. "Found" counts the upstream anywhere in the recorded leads. Renamed repositories count as the same upstream (`kyren/rlua` is `mlua-rs/rlua`, `mishoo/UglifyJS2` is `mishoo/UglifyJS`).

| Set | Condition | 0.1 found / confirmed | 0.2 | 0.3 | 0.4 | 0.5 |
|---|---|---|---|---|---|---|
| tuning (13) | intact | 10 / 6 | 12 / 8 | 12 / 8 | 12 / 8 | 12 / 10 |
| tuning (13) | stripped | 3 / 1 | 6 / 5 | 7 / 7 | 7 / 7 | 8 / 7 |
| holdout (6) | intact | not run | 4 / 3 | 4 / 4 | 5 / 5 | 6 / 5 |
| holdout (6) | stripped | not run | 2 / 2 | 5 / 5 | 4 / 4 | 6 / 4 |
| holdout2 (8) | intact | not run | 7 / 4 | 7 / 4 | 7 / 5 | 7 / 5 |
| holdout2 (8) | stripped | not run | 6 / 4 | 6 / 5 | 6 / 5 | 6 / 5 |
| holdout3 (10) | intact | not run | not run | 5 / 5 | 5 / 5 | 8 / 7 |
| holdout3 (10) | stripped | not run | not run | 5 / 5 | 5 / 5 | 8 / 5 |
| **holdout4 (10)** | intact | not run | not run | not run | 9 / 6 | 10 / 6 |
| **holdout4 (10)** | stripped | not run | not run | not run | 7 / 5 | 8 / 5 |

Each holdout was committed before the code it measures was written, and run once after that version was frozen: holdout2 for 0.3 (frozen at 1435ee6, against 0.2 from a worktree of 10c3562), holdout3 for 0.4 (frozen at a74062e, against 0.3 from a worktree of a70bd26), holdout4 for 0.5 (frozen at c31dc87, against 0.4 from a worktree of 5142245). The second run of each pair reused the first run's cached searches, so the comparison isolates code changes from changes in GitHub's index. Every set is in-sample for every later version.

## Per pair (upstream lead rank and verdict)

A second-hop lead is listed at the position it was evaluated in, which can be past #4 when failed acquisitions or hops reordered the queue. "Declared only" means the target's documents name the upstream but the sampled source showed no overlap.

Holdout4:

| Pair | Intact 0.4 | Intact 0.5 | Stripped 0.4 | Stripped 0.5 |
|---|---|---|---|---|
| fpdf2 ← reingart/pyfpdf | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| pynose ← nose-devs/nose | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| colors.js ← Marak/colors.js | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| gofrs-uuid ← satori/go.uuid | #9 not evaluated | #9 not evaluated | #9 not evaluated | #9 not evaluated |
| ratatui ← fdehau/tui-rs | not found | #19 not evaluated | not found | not found |
| nuklear ← vurtun/nuklear | #21 not evaluated | #24 not evaluated | not found | #21 not evaluated |
| delayed_job ← tobi/delayed_job | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| nextcloud ← owncloud/core | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| radarr ← Sonarr/Sonarr | #1 declared only | #1 declared only | not found | not found |
| hammerspoon ← mjolnirapp/mjolnir | #1 code overlap | #1 code overlap | #10 not evaluated | #10 not evaluated |

Holdout3:

| Pair | Intact 0.4 | Intact 0.5 | Stripped 0.4 | Stripped 0.5 |
|---|---|---|---|---|
| pdfminer.six ← euske/pdfminer | not found | #19 not evaluated | not found | #18 not evaluated |
| dj-rest-auth ← Tivix/django-rest-auth | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| markdown-it ← jonschlinkert/remarkable | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| opentofu ← hashicorp/terraform | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| yaml-rust2 ← chyh1990/yaml-rust | #1 corroborated | #1 corroborated | #1 code overlap | #1 code overlap |
| zlib-ng ← madler/zlib | not found | not found | not found | not found |
| htop ← hishamhm/htop | not found | not found | not found | not found |
| laminas-diactoros ← zendframework/zend-diactoros | not found | #3 code overlap | not found | #6 not evaluated |
| kt-paperclip ← thoughtbot/paperclip | not found | #7 code overlap | not found | #13 not evaluated |
| jellyfin ← MediaBrowser/Emby | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |

Holdout2. 0.4 and 0.5 gave the same result on every pair: eza ← ogham/exa #1 code overlap in both conditions; terser ← mishoo/UglifyJS #4 code overlap (second hop) in both; golang-jwt ← dgrijalva/jwt-go #16 not evaluated intact, not found stripped; nextcord ← Rapptz/discord.py #4 code overlap in both; pycryptodome ← pycrypto/pycrypto not found; angie ← nginx/nginx #7 not evaluated in both; neovim ← vim/vim #1 code overlap in both; mysqlclient ← farcepest/MySQLdb1 #1 corroborated intact, #1 code overlap stripped.

Tuning pairs:

| Pair | Intact 0.4 | Intact 0.5 | Stripped 0.4 | Stripped 0.5 |
|---|---|---|---|---|
| django-q2 ← Koed00/django-q | #1 corroborated | #1 corroborated | #1 code overlap | #1 code overlap |
| flask-caching ← thadeusb/flask-cache | #1 corroborated | #1 corroborated | not found | #13 not evaluated |
| flask-restx ← noirbizarre/flask-restplus | #1 corroborated | #1 corroborated | #1 code overlap | #1 code overlap |
| niquests ← psf/requests | #20 not evaluated | #2 code overlap | not found | not found |
| urllib3-future ← urllib3/urllib3 | #21 not evaluated | #2 code overlap | not found | not found |
| asyncclick ← pallets/click | #4 component | #2 component | #4 code overlap | #4 code overlap |
| hyfetch ← dylanaraps/neofetch (component) | #19 not evaluated | #1 not established | not found | not found |
| pip ← psf/requests (component) | not found | not found | not found | not found |
| yt-dlp ← ytdl-org/youtube-dl | #2 corroborated | #2 corroborated | #2 code overlap (second hop) | #2 code overlap (second hop) |
| valkey ← redis/redis | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| lodash ← jashkenas/underscore | #21 not evaluated | #11 not evaluated | not found | not found |
| gitea ← gogs/gogs | #2 code overlap | #2 code overlap | #1 code overlap | #1 code overlap |
| pypdf ← mfenniak/pyPdf | #4 code overlap | #3 code overlap | #4 code overlap | #4 code overlap |

First holdout:

| Pair | Intact 0.4 | Intact 0.5 | Stripped 0.4 | Stripped 0.5 |
|---|---|---|---|---|
| searxng ← searx/searx | #1 corroborated | #1 corroborated | #4 code overlap | #4 code overlap |
| flask-security ← pallets-eco/flask-security-3.0 | not found | #19 not evaluated | not found | #17 not evaluated |
| pillow-simd ← python-pillow/Pillow | #3 code overlap (second hop) | #1 code overlap | #3 code overlap | #3 code overlap |
| postman-request ← request/request | #2 component | #2 component | #2 code overlap | #2 code overlap |
| bbolt ← boltdb/bolt | #4 code overlap (second hop) | #4 code overlap (second hop) | #4 code overlap (second hop) | #4 code overlap (second hop) |
| mlua ← mlua-rs/rlua | #1 component overlap | #1 component overlap | not found | #16 not evaluated |

## What changed in 0.5

All four changes came from 0.4's diagnosed misses:

- **The package's own name replaces the folder name.** When a target has no README title, the repository search used to search for the folder it sat in ("subject" in every stripped bench run). It now uses the name declared in a root manifest (pyproject.toml, setup.cfg, setup.py, Cargo.toml, package.json, composer.json, a gemspec, go.mod). Only root manifests count, since a docs site's package.json names the site, not the project.
- **Often-linked repositories rank with code-search hits.** A repository the target links on three or more distinct lines of its own application files ranks 45 plus 2 per line (up to ten lines), so it overtakes a single code-search hit from about eight lines. Lockfiles and dotfile configs do not count: Cargo.lock, package-lock.json and .hound.yml put crates.io-index, sponsor and style-guide repositories in front of every lead in early drafts. This is what promoted psf/requests for niquests (#20 → #2), urllib3 for urllib3-future (#21 → #2) and thoughtbot/paperclip for kt-paperclip (not found → #7).
- **PHP `use function` imports are not definitions.** laminas-diactoros now queries its own functions instead of PHP builtins and reaches zend-diactoros at #3 intact.
- **`owner.github.io/repo` links become leads for `owner/repo`.** The mapping is a guess, so it stays out of documentary evidence and out of replay comparison. It made euske/pdfminer a lead for pdfminer.six (#19 intact, #18 stripped), but converging code searches on bundled pdfminer copies still outrank it.

## Why the misses missed

**The target matches itself under an old name** (bug, new in effect in 0.5). `--exclude` and the target's own repository are checked against the name a link spells, not the repository GitHub redirects it to. A README badge pointing at `GDay/django-q2`, `jwag956/flask-security` or `tui-rs-revival/ratatui` resolves to the target, and with the mention boost (62 to 70 linking lines) those self-links now rank high enough to be evaluated. It cost no upstream in these runs but spends an evaluation and reports the target overlapping with itself.

**Copies instead of the upstream** (htop, zlib-ng, ratatui stripped, radarr stripped, hammerspoon stripped). Searches confirm unforked copies of the upstream, the target or a shared component, none of which names the upstream in the files they share: three htop 2.x builds; a tui-rs mirror at 76% coverage; two Bonarr forks of Radarr itself and Sportstarr, which shares about 45% of Radarr's sampled code; and for hammerspoon, Lua interpreters, because its bundled Lua lives under `Pods/` (CocoaPods), which Fossil does not recognise as vendored, so code searches and the mention count both read it as the target's own code. Gitea's `public/plugins/codemirror-5.17.0/` has the same problem.

**Big candidates sampled past the evidence** (gofrs-uuid, radarr intact). gofrs/uuid's searches hit large projects that vendor the uuid package. cockroach was too big to acquire; doltgresql, kubernetes/autoscaler, encore and postgresql-parser were evaluated and none established overlap, because in each the 200,000-token snapshot budget ran out before the vendored uuid files the search had pointed at (0 tokens analyzed in every one). satori/go.uuid waited at #9. Radarr at its pinned 2017 commit declares itself a fork of Sonarr, but Sonarr was acquired at today's develop branch, and with both sides cut at the token budget not a single file pair was even considered.

**Diff budget on the one file that matters** (hyfetch). hyfetch carries neofetch as one 52,000-token script; the modified-file diff for that pair was estimated at 16.8 million units against a 500,000 budget and skipped, so the verdict is not established despite an obviously shared file.

**Vendored demo copies** (nuklear). Nuklear's backends are copied into game engines and hobby kernels; those copies win the code searches and the upstream lands at #21 to #24.

**Fork-only vocabulary** (niquests stripped, urllib3-future stripped, flask-caching, flask-security). Queries use names defined in the target's largest core files, which in a long-lived fork are mostly written after the split. The intact runs now reach the upstream through repeated links; stripped runs have nothing equivalent.

**Ubiquitous upstreams** (angie, zlib-ng). nginx and zlib code is everywhere; nginx/nginx ranks 7th behind tengine and an annotated nginx tree, both confirmed.

**Borrowed cores** (pycryptodome). Its largest C files are cipher code pycrypto took from older public-domain sources, so the queries lead elsewhere.

**Renamed copies with no credits** (golang-jwt). Repositories carrying jwt-go as an internal package were confirmed, but none names dgrijalva/jwt-go in shared files.

**Component pairs** (pip) query the target's own code, not the bundled component. **lodash** at its pinned commit is one file and yields a single query.

## Next round

Query and ranking fixes have run their course on the unseen sets; the holdout4 misses are about what Fossil compares, not what it searches for. In rough order of expected value:

1. Check `--exclude` and the target's own name against the repository a lead resolves to, after redirects. A bug fix, independent of tuning.
2. Recognise `Pods/` and versioned `public/plugins/<name>-<version>/` trees as vendored.
3. When a code search points at a file, make sure that file is inside the candidate's sampled budget.
4. When the diff budget skips a pair, fall back to the shingle blocks already computed for it instead of reporting nothing.
5. Acquire a candidate near the target's own dates when the target is old (Radarr 2017 against Sonarr 2026).
6. Let independent sources agreeing on one lead (a credit, a github.io link, a manifest-name repository search) count like converging code searches do (pdfminer.six).
7. Then the direction problem, where repository creation order is a weak but cheap hint.

Each needs a fresh holdout (holdout5); holdout4 is now in-sample. One bench artifact to keep in mind: stripping blanks every line containing a GitHub URL, which empties a go.mod whose module path is on github.com, so stripped Go targets have no package name. For gofrs/uuid the name would be "uuid", which would not have helped.

## Other repositories that reached a confirming verdict

Every one was checked by hand (description and matched files). None was a spurious match: each shares real code with the target. Three are the target itself under an old name, which is the bug above.

- **The target itself, through a redirect.** django-q2 (`GDay/django-q2`), Flask-Security-Too (`jwag956/flask-security`), ratatui (`tui-rs-revival/ratatui`).
- **Copies or bundles of the target.** Download-manager and Kodi add-ons carrying `yt_dlp/`, mlua forks, a TypeScript port of terser, apps vendoring flask-restx, asyncclick, dj-rest-auth or jwt-go as internal packages, pipenv vendoring pip, bbolt packaging, a Flask-Security-Too copy, a jellyfin hardware-decoding fork, an OpenTofu variant and an infrastructure tool built from its code, two sites bundling markdown-it 2.2.1 for benchmarks, a cgo binding bundling zlib-ng, saphyr, a PHP project bundling laminas-diactoros, two delayed_job copies, two Bonarr forks of Radarr and Sportstarr, a game engine, a hobby OS and an OpenGL project carrying Nuklear's code and demo backends.
- **Copies of, or links in, the upstream's lineage.** yt-dlc, a PyPDF2 mirror, exa forks, annotated Redis and nginx trees, tengine, a detached gogs fork, disnake and qq.py, MySQL-for-Python-3 and moist, vim.wasm, Pillow packaging, three htop 2.x builds, a paperclip copy, an old terraform copy, mini-v8 (one file borrowed from rlua), nose-py3 and a project bundling nose, a tui-rs mirror, urllib3 (one shared noxfile block in niquests).
- **Projects vendoring the same third-party code.** Blender add-ons bundling PIL, a test tool bundling `request`, GlowScript bundling uglify-es, PDF tools bundling pdfminer, a Slack exporter bundling fpdf, a bare-metal project bundling zlib, two Rust crates carrying yaml-rust's emitter, codemirror5 bundled in gitea, bottom vendoring tui's canvas, three Lua-embedding projects matching hammerspoon's bundled Lua.

Fossil reports all of these as overlap with undetermined direction, which is correct. It cannot yet tell an ancestor from a descendant without Git history or an acknowledgement, and with acknowledgements stripped it more often finds descendants than ancestors.

## Limits of this measurement

Forty-seven pairs across Python, Go, Rust, JavaScript, C, C#, PHP, Ruby and Objective-C, all public on GitHub. Each holdout has six to ten pairs, so a one-pair difference is suggestive at best. Results depend on GitHub's live code index, which changes. Earlier sets have been used repeatedly and overstate what the next unseen pairs will show.
