# Discovery benchmark results

Measured 2026-11-01/02 on Windows 11, Python 3.13, with an authenticated GitHub token and default settings (4 evaluated candidates). Method and pair lists: [README.md](README.md). Raw scores: [results/](results/), where `baseline` is 0.1, `v3` is 0.2, `v5` is 0.3, `v6` is 0.4, `v7` is 0.5, `v8` is 0.6, and `v2`/`v4` are intermediate drafts of 0.2 and 0.3.

**Short version.** On ten pairs no version had seen (holdout5), Fossil 0.6 and 0.5 gave identical results on every pair: the true upstream found and confirmed in 11 of 20 runs (6 intact, 5 stripped). In-sample, 0.6 confirmed two more upstreams than 0.5 (61 against 59 of 84 runs), both from the fixes aimed at them (hyfetch's neofetch past the diff budget, hammerspoon's mjolnir once `Pods/` counted as vendored), and lost none. That makes three unseen rounds in a row with no gain, so the in-sample gains of 0.4, 0.5 and 0.6 are fixes for known failures, not better discovery in general. The only measured unseen gain is still holdout2 (0.2 → 0.3: 4 → 5 of 8 stripped). No run of any version confirmed a repository that did not genuinely share code with the target, and 0.6 no longer evaluates the target under its own old name.

The largest single cause of misses is the evaluation limit, not search: in 20 of the 42 runs where 0.6 missed, the upstream was among the leads but ranked below the four that get evaluated.

## Counts

"Confirmed" means the upstream was among the evaluated candidates and reached a verdict backed by source overlap. "Found" counts the upstream anywhere in the recorded leads. Renamed repositories count as the same upstream (`kyren/rlua` is `mlua-rs/rlua`, `mishoo/UglifyJS2` is `mishoo/UglifyJS`).

| Set | Condition | 0.1 found / confirmed | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 |
|---|---|---|---|---|---|---|---|
| tuning (13) | intact | 10 / 6 | 12 / 8 | 12 / 8 | 12 / 8 | 12 / 10 | 12 / 11 |
| tuning (13) | stripped | 3 / 1 | 6 / 5 | 7 / 7 | 7 / 7 | 8 / 7 | 8 / 7 |
| holdout (6) | intact | not run | 4 / 3 | 4 / 4 | 5 / 5 | 6 / 5 | 6 / 5 |
| holdout (6) | stripped | not run | 2 / 2 | 5 / 5 | 4 / 4 | 6 / 4 | 6 / 4 |
| holdout2 (8) | intact | not run | 7 / 4 | 7 / 4 | 7 / 5 | 7 / 5 | 7 / 5 |
| holdout2 (8) | stripped | not run | 6 / 4 | 6 / 5 | 6 / 5 | 6 / 5 | 6 / 5 |
| holdout3 (10) | intact | not run | not run | 5 / 5 | 5 / 5 | 8 / 7 | 8 / 7 |
| holdout3 (10) | stripped | not run | not run | 5 / 5 | 5 / 5 | 8 / 5 | 8 / 5 |
| holdout4 (10) | intact | not run | not run | not run | 9 / 6 | 10 / 6 | 10 / 6 |
| holdout4 (10) | stripped | not run | not run | not run | 7 / 5 | 8 / 5 | 8 / 6 |
| **holdout5 (10)** | intact | not run | not run | not run | not run | 8 / 6 | 8 / 6 |
| **holdout5 (10)** | stripped | not run | not run | not run | not run | 6 / 5 | 6 / 5 |

Each holdout was committed before the code it measures was written, and run once after that version was frozen: holdout2 for 0.3 (frozen at 1435ee6, against 0.2 from a worktree of 10c3562), holdout3 for 0.4 (frozen at a74062e, against 0.3 from a worktree of a70bd26), holdout4 for 0.5 (frozen at c31dc87, against 0.4 from a worktree of 5142245), holdout5 for 0.6 (frozen at c8c4774, against 0.5 from a worktree of 835c4d7). The second run of each pair reused the first run's cached searches, so the comparison isolates code changes from changes in GitHub's index. Every set is in-sample for every later version.

## Per pair (upstream lead rank and verdict)

A second-hop lead is listed at the position it was evaluated in, which can be past #4 when failed acquisitions or hops reordered the queue. "Declared only" means the target's documents name the upstream but the sampled source showed no overlap.

Holdout5 (unseen by both versions):

| Pair | Intact 0.5 | Intact 0.6 | Stripped 0.5 | Stripped 0.6 |
|---|---|---|---|---|
| nu-ansi-term ← ogham/rust-ansi-term | #2 code overlap | #2 code overlap | #2 code overlap | #2 code overlap |
| mapstructure ← mitchellh/mapstructure | not found | not found | not found | not found |
| jshint ← jslint-org/jslint | not found | not found | not found | not found |
| phpspreadsheet ← PHPOffice/PHPExcel | #3 code overlap | #3 code overlap | #17 not evaluated | #17 not evaluated |
| c-toxcore ← irungentoo/toxcore | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| libresprite ← aseprite/aseprite | #10 not evaluated | #10 not evaluated | not found | not found |
| faust ← robinhood/faust | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| lite-xl ← rxi/lite | #1 corroborated | #1 corroborated | #2 code overlap | #2 code overlap |
| dnspy ← dnSpy/dnSpy | #14 not evaluated | #14 not evaluated | not found | not found |
| sorcery ← NoamB/sorcery | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |

Holdout4:

| Pair | Intact 0.5 | Intact 0.6 | Stripped 0.5 | Stripped 0.6 |
|---|---|---|---|---|
| fpdf2 ← reingart/pyfpdf | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| pynose ← nose-devs/nose | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| colors.js ← Marak/colors.js | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| gofrs-uuid ← satori/go.uuid | #9 not evaluated | #9 not evaluated | #9 not evaluated | #9 not evaluated |
| ratatui ← fdehau/tui-rs | #19 not evaluated | #19 not evaluated | not found | not found |
| nuklear ← vurtun/nuklear | #24 not evaluated | #24 not evaluated | #21 not evaluated | #21 not evaluated |
| delayed_job ← tobi/delayed_job | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| nextcloud ← owncloud/core | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| radarr ← Sonarr/Sonarr | #1 declared only | #1 declared only | not found | not found |
| hammerspoon ← mjolnirapp/mjolnir | #1 code overlap | #1 code overlap | #10 not evaluated | #4 code overlap |

Holdout3:

| Pair | Intact 0.5 | Intact 0.6 | Stripped 0.5 | Stripped 0.6 |
|---|---|---|---|---|
| pdfminer.six ← euske/pdfminer | #19 not evaluated | #19 not evaluated | #18 not evaluated | #18 not evaluated |
| dj-rest-auth ← Tivix/django-rest-auth | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| markdown-it ← jonschlinkert/remarkable | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| opentofu ← hashicorp/terraform | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| yaml-rust2 ← chyh1990/yaml-rust | #1 corroborated | #1 corroborated | #1 code overlap | #1 code overlap |
| zlib-ng ← madler/zlib | not found | not found | not found | not found |
| htop ← hishamhm/htop | not found | not found | not found | not found |
| laminas-diactoros ← zendframework/zend-diactoros | #3 code overlap | #3 code overlap | #6 not evaluated | #6 not evaluated |
| kt-paperclip ← thoughtbot/paperclip | #7 code overlap | #3 code overlap | #13 not evaluated | #13 not evaluated |
| jellyfin ← MediaBrowser/Emby | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |

Holdout2:

| Pair | Intact 0.5 | Intact 0.6 | Stripped 0.5 | Stripped 0.6 |
|---|---|---|---|---|
| eza ← ogham/exa | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| terser ← mishoo/UglifyJS | #4 code overlap (second hop) | #2 code overlap (second hop) | #4 code overlap (second hop) | #2 code overlap (second hop) |
| golang-jwt ← dgrijalva/jwt-go | #16 not evaluated | #16 not evaluated | not found | not found |
| nextcord ← Rapptz/discord.py | #4 code overlap | #5 code overlap | #4 code overlap | #5 code overlap |
| pycryptodome ← pycrypto/pycrypto | not found | not found | not found | not found |
| angie ← nginx/nginx | #7 not evaluated | #5 not evaluated | #7 not evaluated | #5 not evaluated |
| neovim ← vim/vim | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| mysqlclient ← farcepest/MySQLdb1 | #1 corroborated | #1 corroborated | #1 code overlap | #1 code overlap |

Tuning pairs:

| Pair | Intact 0.5 | Intact 0.6 | Stripped 0.5 | Stripped 0.6 |
|---|---|---|---|---|
| django-q2 ← Koed00/django-q | #1 corroborated | #1 corroborated | #1 code overlap | #1 code overlap |
| flask-caching ← thadeusb/flask-cache | #1 corroborated | #1 corroborated | #13 not evaluated | #14 not evaluated |
| flask-restx ← noirbizarre/flask-restplus | #1 corroborated | #1 corroborated | #1 code overlap | #1 code overlap |
| niquests ← psf/requests | #2 code overlap | #2 code overlap | not found | not found |
| urllib3-future ← urllib3/urllib3 | #2 code overlap | #2 code overlap | not found | not found |
| asyncclick ← pallets/click | #2 component | #2 component | #4 code overlap | #4 code overlap |
| hyfetch ← dylanaraps/neofetch (component) | #1 not established | #1 code overlap | not found | not found |
| pip ← psf/requests (component) | not found | not found | not found | not found |
| yt-dlp ← ytdl-org/youtube-dl | #2 corroborated (second hop) | #2 corroborated (second hop) | #2 code overlap (second hop) | #2 code overlap (second hop) |
| valkey ← redis/redis | #1 code overlap | #1 code overlap | #1 code overlap | #1 code overlap |
| lodash ← jashkenas/underscore | #11 not evaluated | #11 not evaluated | not found | not found |
| gitea ← gogs/gogs | #2 code overlap | #2 code overlap | #1 code overlap | #1 code overlap |
| pypdf ← mfenniak/pyPdf | #3 code overlap | #3 code overlap | #4 code overlap | #4 code overlap |

First holdout:

| Pair | Intact 0.5 | Intact 0.6 | Stripped 0.5 | Stripped 0.6 |
|---|---|---|---|---|
| searxng ← searx/searx | #1 corroborated | #1 corroborated | #4 code overlap | #4 code overlap |
| flask-security ← pallets-eco/flask-security-3.0 | #19 not evaluated | #20 not evaluated | #17 not evaluated | #18 not evaluated |
| pillow-simd ← python-pillow/Pillow | #1 code overlap | #1 code overlap | #3 code overlap (second hop) | #2 code overlap (second hop) |
| postman-request ← request/request | #2 component | #2 component | #2 code overlap | #2 code overlap |
| bbolt ← boltdb/bolt | #4 code overlap (second hop) | #4 code overlap (second hop) | #4 code overlap (second hop) | #4 code overlap (second hop) |
| mlua ← mlua-rs/rlua | #1 component overlap | #1 component overlap | #16 not evaluated | #14 not evaluated |

## What changed in 0.6

All five changes came from 0.5's diagnosed misses:

- **Leads are resolved before they are acquired.** Each lead is looked up through GitHub's rename and transfer redirects first; one that resolves to the target, to an excluded repository, or to a lead already evaluated is skipped without spending an evaluation. This removed the target-under-an-old-name bug (django-q2, Flask-Security-Too, ratatui) and moved thoughtbot/paperclip from #7 to #3 for kt-paperclip.
- **Searched files are sampled first.** When a candidate exceeds the 200,000-token snapshot budget, the files a code search pointed at are taken before the rest, and replay records them. gofrs/uuid's large candidates (doltgresql, encore, postgresql-parser) now establish the vendored uuid overlap they were searched for; satori/go.uuid still waits at #9, because their copies do not name it.
- **More bundled trees count as vendored:** `Pods/`, `Carthage/`, and directories named for a release (`codemirror-5.17.0/`, `lua-5.3.4/`) outside test trees. Hammerspoon's bundled Lua no longer reads as its own code, so stripped hammerspoon now reaches mjolnirapp/mjolnir (#10 → #4, code overlap).
- **Pairs past the diff budget are matched, not skipped.** When a modified-file diff would exceed 500,000 operations, the pair is matched from shared 25-token anchors in linear time. hyfetch's 52,000-token copy of neofetch now gives code overlap instead of "not established". This fallback produced most of 0.6's new extra confirmations (below); the slowest comparison across 221 re-checked pairs took 4.6 seconds. Cases record the fallback, so cases made by 0.5 and earlier still replay with the old method.
- **Go vendor and module-cache paths become second-hop leads.** A shared file at `vendor/github.com/owner/repo/...` or `pkg/mod/github.com/owner/repo@version/...` names its source. It led to no benchmark upstream (see mapstructure below).

**Replay of older cases.** Inventories that contain `Pods/` or release-named directories classify differently under 0.6, so cases holding such trees no longer replay: 24 of the 94 saved 0.5 bench cases (12 subjects, both conditions), all with the inventory mismatch the version note announces. The three bundled example cases still replay.

## Why the misses missed

**Found but not evaluated** (20 of 42 missed runs): LibreSprite's aseprite/aseprite (#10 intact), dnSpy (#14 intact), PHPExcel (#17 stripped), satori/go.uuid (#9), tui-rs (#19), Nuklear (#21 to #24), pdfminer (#18 to #19), zend-diactoros and paperclip stripped (#6, #13), jwt-go (#16), nginx (#5), Flask-Security (#17 to #20), rlua stripped (#14), underscore (#11) and flask-cache stripped (#14). Only four leads are evaluated by default (`--max-candidates` allows up to ten). What ranks above the upstream is usually real overlap with something else: copies of the target, forks of the upstream, or a library both bundle.

**A crowd of forks** (dnSpy). Four forks of dnSpy were confirmed ahead of the archived original; none links it from a shared file.

**A vendored path that named the upstream once** (mapstructure). eolinker/goku_lite was confirmed through `pkg/mod/github.com/mitchellh/mapstructure@v1.1.2/mapstructure.go`, a path that names the upstream outright, but a second hop needs two shared files (or one plus a statement) and this copy shared one. The repository search put mitchellh/mapstructure first in its own results, but it did not make the 24-lead list behind the code-search hits.

**Long divergence** (JSHint). JSHint split from JSLint in 2011 and was largely rewritten. Two confirmed candidates (seccubus, skulpt) carry old JSLint copies that still match jshint.js, so the lineage shows up, but neither links the upstream repository.

**Bundled libraries outside vendor folders** (LibreSprite). LibreSprite carries Allegro 4 under `src/allegro/`, so Allegro copies (ZeldaClassic, Adventure Game Studio, an Allegro 4.2.2 build) match it and rank ahead of aseprite. Hammerspoon's LuaFileSystem under `extensions/fs/` matched nelua-lang the same way.

**Copies instead of the upstream** (htop, zlib-ng, ratatui stripped, radarr stripped). Searches confirm unforked copies of the upstream, the target or a shared component, none of which names the upstream in the files they share.

**Old target, new candidate** (radarr intact). Radarr at its pinned 2017 commit declares itself a fork of Sonarr, but Sonarr is acquired at today's branch, and with both sides cut at the token budget no file pair is compared.

**Fork-only vocabulary** (niquests stripped, urllib3-future stripped, flask-caching stripped, flask-security). Queries use names defined in the target's largest core files, which in a long-lived fork are mostly written after the split.

**Ubiquitous upstreams** (angie, zlib-ng), **borrowed cores** (pycryptodome, whose C ciphers match libtomcrypt and Komodo's pycrypto copy, not pycrypto itself), **renamed copies with no credits** (golang-jwt), and **component pairs** (pip queries its own code, not the bundled requests) are unchanged from 0.5.

## Next round

Three unseen rounds have come out flat, so more query and ranking heuristics are unlikely to pay off; the recommendation is to stop tuning here. If the work continues, the measurements point to two changes that are not heuristics:

1. **Evaluate more candidates.** Twenty misses had the upstream in the leads. A run with `--max-candidates 8` (more time and API calls per investigation) measures what that buys, and needs a fresh holdout like any other change.
2. **Ask GitHub for the fork parent of confirmed candidates.** dnSpy's crowd of forks all point at one parent, and the repository API reports it for one call each.

Smaller, diagnosed but untested: let one shared file under a module-cache or vendor path make a second-hop lead (mapstructure); acquire a candidate near the target's own dates when the target is old (Radarr); count independent sources converging on one lead (pdfminer.six); then the direction problem.

holdout5 is in-sample from 0.7 on.

## Other repositories that reached a confirming verdict

Every one was checked by hand (description and matched files). None was a spurious match: each shares real code with the target. 0.5 also evaluated three targets under an old name; 0.6 skips those.

- **Copies or bundles of the target.** Download-manager and Kodi add-ons carrying `yt_dlp/`, mlua forks, a TypeScript port of terser, apps vendoring flask-restx, asyncclick, dj-rest-auth or jwt-go as internal packages, pipenv vendoring pip, bbolt packaging, a Flask-Security-Too copy, a jellyfin hardware-decoding fork, an OpenTofu variant and an infrastructure tool built from its code, two sites bundling markdown-it 2.2.1 for benchmarks, a cgo binding bundling zlib-ng, saphyr, a PHP project bundling laminas-diactoros, two delayed_job copies, two Bonarr forks of Radarr and Sportstarr, a game engine, a hobby OS and an OpenGL project carrying Nuklear's code and demo backends.
- **Copies of, or links in, the upstream's lineage.** yt-dlc, a PyPDF2 mirror, exa forks, annotated Redis and nginx trees, tengine, a detached gogs fork, disnake and qq.py, MySQL-for-Python-3 and moist, vim.wasm, Pillow packaging, three htop 2.x builds, a paperclip copy, an old terraform copy, mini-v8 (one file borrowed from rlua), nose-py3 and a project bundling nose, a tui-rs mirror, urllib3 (one shared noxfile block in niquests).
- **Projects vendoring the same third-party code.** Blender add-ons bundling PIL, a test tool bundling `request`, GlowScript bundling uglify-es, PDF tools bundling pdfminer, a Slack exporter bundling fpdf, a bare-metal project bundling zlib, two Rust crates carrying yaml-rust's emitter, codemirror5 bundled in gitea, bottom vendoring tui's canvas, three Lua-embedding projects matching hammerspoon's bundled Lua.
- **New in 0.6, mostly through the anchored fallback.** bazarr bundling flask-restx and click, web2py bundling fpdf, a Pythonista collection bundling PyPDF2, a browser bundling uglify-es, a site bundling flask-caching, a code-search dataset holding django-q's models, valkey-wasm, gopay carrying jwt-go, metagoofil carrying pdfminer, two projects carrying zlib-ng's deflate_quick.c, CarbonROM's htop and a C++ toolkit bundling htop, helix and evil-helix carrying a tui buffer, SignalR's TaskAsyncHelper in Radarr, hydra-2 and mjolnir-modules for hammerspoon, four Go projects vendoring mapstructure, four JavaScript projects carrying JSHint or JSLint, Allegro copies in three game projects for LibreSprite, libtomcrypt's DES in pycryptodome, lodash.js copied into four projects, MacVim's vim sources for neovim, and jquery.fileupload in two Nextcloud matches.

Fossil reports all of these as overlap with undetermined direction, which is correct. It cannot yet tell an ancestor from a descendant without Git history or an acknowledgement, and with acknowledgements stripped it more often finds descendants than ancestors.

## Limits of this measurement

Fifty-seven pairs across Python, Go, Rust, JavaScript, C, C++, C#, PHP, Ruby, Lua and Objective-C, all public on GitHub. Each holdout has six to ten pairs, so a one-pair difference is suggestive at best. Results depend on GitHub's live code index, which changes. Earlier sets have been used repeatedly and overstate what the next unseen pairs will show.
