---
name: agentskillupdater
description: Run, verify, and troubleshoot the Antigravity Agent Skills Vault & Skill.Sea automation pipeline (update.py, skillssh.py, skillleaderboard.py, Skill.Sea catalog → R2 → Cloudflare Worker). Use whenever the user asks to run or update the skills vault or update.py, check or verify the pipeline, update the Skill.Sea website or live counts, add or sync library repos, investigate skill/repo counts, or fix or avoid the known pipeline pitfalls (staging junk, duplicate skill dirs, stale doc numbers, install-count parsing, git lock and Windows command-length errors).
---

# Agent Skills Updater

Operational runbook for the Antigravity Agent Skills Vault (this repo, public at `github.com/SeaXen/agentskills`) and its live web app **Skill.Sea** (`https://skill.drsea.top`). Everything below was learned by running this pipeline in production — follow it and you will not repeat the bugs listed in `references/pitfalls.md`.

## Ground truth — read, never guess

Counts drift and the docs disagree. **`Skill.Sea/data/stats.json` is the single source of truth** (`totalSkills`, `totalCategories`, `totalRepositories`, `activeHotSetCount`). As of 2026-11-06 it read 21,757 skills · 38 categories · 485 repositories · 131 hot-set — always re-read the file instead of quoting any doc. README/AGENTS.md prose numbers are auto-refreshed by the pipeline but can lag one run behind stats.json.

The hot-set (131) is a **union of two directories**: `skills/` (91 dirs) + the parent workspace `../.agent/skills/` (91 dirs, outside this repo) — roughly 51 names exist in both, so the union is not the sum (91 + 91 − 51 = 131). Adding a skill to one without the other produces confusing count diffs — edit or remove both copies.

## The one command

| Command | When to use | Typical time |
|---|---|---|
| `python update.py --offline` | routine updates (skip discovery) | ~3 min |
| `python update.py` | full run incl. discovery of new popular repos | ~6 min |
| `python update.py --reindex --no-push --offline` | safe local iteration, nothing committed | ~1–2 min |
| `python update.py --about` | quick counts, no writes | instant |
| `python skillssh/skillssh.py --check --min-installs 500k` | audit which popular skills.sh repos are missing | ~4 min (refreshes cache) |
| `node Skill.Sea/scripts/verify.js` | 64-check gate — run after every update | ~10 s |

Other flags: `--no-push` (commit-free), `--deploy` (also `npx wrangler deploy` — only when worker.js/static assets change, never for data), `--force`, `--find <kw>`, `--skills-sh`/`--skillleaderboard` delegation.

**Run long jobs in the user's own terminal.** The agent harness kills backgrounded processes on long runs — this killed two discovery runs mid-ingest. Runs of ~3 minutes or less survive backgrounding; anything longer (e.g. a fresh 1,500-repo discovery, 12–24 h) must run in the user's own PowerShell window.

## What a full run does (everything automatic)

- **[0/6] Discovery** — skills.sh audit (`--sync --min-installs 100k`) plus skillleaderboard (`--starred 150 --ingest`, `--trending 50 --ingest`). New repos are cloned into `library/<owner>-<repo>/` and registered in `library/upstreams.json`, so later runs track them. Ingestion resumes — already-ingested repos are skipped.
- **[1/6] Upstream sync** — parallel `git ls-remote` HEAD check of every repo; changed repos are shallow-cloned (blobless, 45 s timeout) into a temp dir; skills extracted to `library/<repo>/skills/<name>/`; dev-tooling junk stripped; `.upstream_commit` watermark written. If a clone times out but local skills exist, the watermark is still written (repo only retries on its next upstream commit).
- **[2/6] Active skills** - upstream updates copied into workspaces: this repo's `skills/`, any optional extra workspaces the user has configured (see pipeline.md), and the parent `.agent` workspace (only if it exists). Lockfile-sourced skills update only when their source repo was updated this run.
- **[3/6] Index** — incremental rebuild of `library/skills_index.json`: only updated/new repos are re-parsed; unchanged repos reuse their cached per-repo `skills_index.json`. This is why the count grows only when repos actually change.
- **[4/6] Lockfiles** — `skills-lock.json` reconciled against the actual skills dirs of each workspace.
- **[5/6] Categories / provenance / docs** — 38 categories rebuilt (`category/categories_index.json`), `SKILLS_PROVENANCE.md` regenerated, README/ARCHITECTURE/PRODUCT/AGENTS metrics synced.
- **[5.5/6] Catalog + doc auto-sync** — `node Skill.Sea/scripts/build-catalog.js` rewrites `Skill.Sea/data/*.json` (stats, catalog, categories, repositories); then `sync_frontend_doc_numbers()` refreshes ~28 hardcoded numbers across 9 doc/frontend files from the fresh stats.json.
- **[6/6] Git** — explicit-path staging (never `git add -A`), commit `chore(skills): automated update of skills & library (timestamp)`, push. The **pre-commit** hook rebuilds the catalog; the **pre-push** hook runs `sync-r2.js --allow-offline`, uploading to R2 bucket `skill-sea-vault`, which the Cloudflare Worker serves at `/data/*`. **Data-only changes need no redeploy.**

Full step internals: `references/pipeline.md`.

## Verify after every run (mandatory)

1. **Push confirmed**: `git rev-parse HEAD` == `git rev-parse origin/main`.
2. **Gate**: `node Skill.Sea/scripts/verify.js` → must print ALL 64 CHECKS PASSED.
3. **Live site matches local**: fetch `https://skill.drsea.top/data/stats.json` and compare to the local file (CDN cache for stats.json is 60 s, so brief staleness right after a sync is expected).
4. **Stale-number sweep**: grep the 9 doc/frontend files for `18,722|20,483|17,145|25,695|20\.30|\b339\b|\b370\b` — expect zero genuine hits (a per-category count such as `380` for backend-api-design is legitimately stale-proof).
5. **Clean tree**: `git status --porcelain --untracked-files=no` → empty.

Complete protocol with expected outputs: `references/verification.md`.

## Hard rules (violating these breaks the repo)

- **Never `git add -A`.** `library/` holds hundreds of untracked junk dirs (flat parent-prefixed duplicates left by re-clones, e.g. `skills/agp-agp-9-upgrade/` beside `skills/agp-9-upgrade/`). update.py stages explicit paths only, filtered against `library/skills_index.json` — keep it that way.
- **Never auto-delete non-skill files in `library/<repo>/`** (upstream READMEs, examples, scripts stay intact) unless the user explicitly instructs deletion. The only sanctioned cleanup is the dev-tooling junk *inside* skills (`tests/`, `.github/`, `package.json`, lockfiles, `.git*`) — the `SKILL_JUNK_LEVEL1`/`SKILL_JUNK_ANY_DEPTH` sets in update.py define exactly what counts as junk.
- **Never hand-edit `Skill.Sea/data/catalog.json`** — rebuild it (`node Skill.Sea/scripts/build-catalog.js`). Malformed upstream frontmatter is fixed at the source, not in the JSON.
- **Never quote numbers from README/AGENTS.md prose** — read `stats.json`.
- **Never put `overscroll-behavior-y: none` on `html`/`body`** in Skill.Sea (mobile touch-freeze) — only on `.drawer-body`, `.comparator-body`, `.stack-items-list`.
- **Never let React/Vue/Tailwind/Webpack/Vite into Skill.Sea** — zero runtime deps, pure HTML5 + CSS custom properties + vanilla ES6; `server.js` uses Node stdlib only.
- **Don't run full discovery casually** — it is a 12–24 h job if the ≥100K install tier has gaps. Check first with `skillssh --check`.

## Known pitfalls and their fixes

Compact list; full symptom/cause/fix detail in `references/pitfalls.md`.

1. `NameError: updated_ids` → the caller stores the return value as `updated_repos`; pass that.
2. Committing ~6,900 junk files → explicit-path staging with `index_prefixes` built from `skills_index.json`.
3. Windows `WinError 206` on `git add` with many long paths → `git add --pathspec-from-file=-` via stdin, 20K-char chunks, `:(literal)` pathspec prefixes.
4. Non-ASCII (Chinese) filenames silently skipped → `git status --porcelain -z` (NUL-separated, no C-quoting) + UTF-8 decode.
5. Flat parent-prefixed duplicate skill dirs → dedup by SKILL.md content hash; extraction refreshes in place when content matches, parent-prefix only when it genuinely differs.
6. Junk inside skills (`tests/`, `.github/`, `package.json`) → `clean_skill_internal_junk()` runs every run (in `clean_nested()` and right after extraction).
7. skillssh install counts all "1M" → the parser matched site chrome; anchored regex on `total installs` bridging HTML comments; delete the poisoned `.cache_skills_sh.json` to refresh.
8. Stale doc numbers → `sync_frontend_doc_numbers()` auto-syncs ~28 spots across 9 files on every run.
9. Stale `.git/index.lock` blocking git → auto-cleared when no git process is running.
10. Big repos stuck at watermark-only updates → clone timeout raised 15 s → 45 s.
11. Background runs dying → run in the user's own terminal.

## Portability (this repo is public)

No folder binding: `update.py` derives `agents_dir`/`repo_root` from `__file__`; `build-catalog.js` uses `path.resolve` and guards the parent hot-set dir with `existsSync`; `skillssh.py` detects the vault by structure (parent dir containing `library/`). Machine-specific paths (the Managment workspace, the parent `.agent/skills`) are gracefully skipped when absent, so any clone runs `python update.py` successfully. Deploying your own Skill.Sea needs your own Cloudflare account/R2 bucket; `--allow-offline` keeps git working without credentials.

## References

- `references/pipeline.md` — step-by-step internals, flags, data flow, hooks, GitHub Actions, timing expectations
- `references/verification.md` — full post-run verification protocol, commands, expected outputs
- `references/pitfalls.md` — every production bug found, with symptom / root cause / fix / how to detect
