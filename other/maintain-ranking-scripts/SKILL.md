---
name: maintain-ranking-scripts
description: Maintain and improve the scripts that auto-generate this repo's star-ranked "Awesome Claude Code" README. Use when editing helpers/fetch.py, helpers/render.py, or helpers/config.json — tuning scope/category rules, changing the repos.json schema or README layout — and when running the CLASSIFICATION AUDIT to curate helpers/filtered.json and fix scope_filter false positives. Does NOT run the daily refresh (CI cron does that) and does NOT hand-curate an include list (discovery is an exhaustive sweep).
---

# maintain-ranking-scripts

Maintain the scripts behind this repo's auto-generated, star-ranked README of the
Claude Code / skills / agents / MCP ecosystem.

## What this repo's pipeline does

1. **`helpers/fetch.py`** (network only) does an **exhaustive** star-bucketed sweep
   of every public repo at or above `min_stars` (the Search API caps each query at
   1,000 results, so the star range is split into adaptive buckets, then
   concatenated). Because the sweep is exhaustive, **discovery is complete by
   construction** — there are no scoped queries that could miss a popular repo. It
   writes two files and nothing else:
   - **`helpers/repos.json`** — the full universe (every repo ≥ `min_stars`),
     metadata only. The single source of truth for everything downstream.
   - **`helpers/out_of_scope.json`** — AUTO classification: universe entries that
     **fail** `scope_filter` (not AI/Claude). Regenerated every run; never
     hand-edited.
   It does **not** categorize, write briefs, rank-to-top-N, fetch READMEs, or apply
   any denylist.
2. **`helpers/render.py`** (no network) selects the published set —
   `repos.json` minus `out_of_scope.json` minus `helpers/filtered.json` minus
   `helpers/non_english.json` (which it derives itself, see below) minus
   archived, top `render.render_count` by stars — writes
   **`helpers/repos_to_render.json`**, then **categorizes**, builds the short
   **briefs** (from description / topics), and lays out **`README.md`**: a Table of
   Contents, the **Trending this week** cut, the Top-N leaderboard, the long tail
   split into per-category tables, and a footer of links. **The README body is tables
   only** — the prose (scope, column definitions, disclaimer, licensing) lives in
   hand-maintained docs, not in `render.py`; see "Where the static docs live" below.
3. **`helpers/trend.py`** (no network, git only) supplies the **momentum** columns
   (`Pos`, `+Stars`) and the Trending cut: it reads an *older committed version of
   `repos.json`* straight out of git history — the newest snapshot at least
   `render.trend.window_days` old. **One baseline feeds both columns**, so they always
   describe the same span. No extra API calls and no new state file; the daily commits
   **are** the star history. Best-effort: no git, a depth-1 clone, or history shorter
   than the window drops both columns and the Trending section, and the README still
   renders.
4. **CI** (`.github/workflows/`): `refresh-ranking.yml` runs the sweep+render daily
   and commits the artifacts; `render-on-edit.yml` re-renders (no network) when a
   human edits `filtered.json` (NOT `config.json` — scope/min_stars are sweep-time,
   so config edits wait for the next sweep). **Both check out with `fetch-depth: 0`**
   — the default depth-1 clone would silently render without the momentum columns.

The ≥`min_stars` universe partitions as `repos.json` ⊇ (`out_of_scope.json` ∪
`filtered.json` ∪ `non_english.json`). See `reference.md` for the full file contracts and schema.

## Where the static docs live

`render.py` holds **no prose** beyond the README's one-line header and the footer link
row. Everything explanatory is a hand-maintained file, edited directly (never
generated):

| file | holds |
|------|-------|
| `docs/METHODOLOGY.md` | how the list is built; what every column means; where `Pos`/`+Stars` come from |
| `CONTRIBUTING.md` | which files are generated, and which lever to pull to change the output |
| `docs/DISCLAIMER.md` | no-endorsement, third-party links, trademarks, removals, and the licensing note |
| `LICENSE` | the CC0-1.0 text itself — the only place it lives; don't restate it in a doc |

Keep the README body noise-free: a new explanation belongs in `METHODOLOGY.md`, not in
a note under a table. Don't restate config values (`min_stars`, `window_days`) in these
docs — reference the key so `config.json` stays the single source of truth.

The scripts are **stdlib-only** (no pip installs) and must stay that way.

## The three exclusion sets (orthogonal)

- **`out_of_scope.json` — AUTO, CI-owned.** "Not AI/Claude." Derived from
  `repos.json` + `scope_filter` every run. **Never hand-edit it** — if something is
  misclassified, fix the *rules* in `config.json` (single source of truth).
- **`non_english.json` — AUTO, render-owned.** "Description isn't English."
  Derived by `render.py` from `repos.json` every run: any otherwise-publishable
  repo whose GitHub description is ≥ `render.non_english_threshold` non-Latin
  letters, recorded with its measured share. **Never hand-edit it** — move the
  threshold in `config.json` instead. Sited at render because that is where a repo
  becomes *visible*; it needs no network, so it costs the offline half nothing.
- **`filtered.json` — MANUAL, human-owned.** Repos that *are* AI/Claude-adjacent
  (they pass scope) but are excluded as **redundant**. Each entry is
  `{ "repo_id": "owner/name", "reason": "..." }` (a bare string is also tolerated).
  This is the **only** editorial lever; there is **no allowlist**. Established
  categories:
  1. **Competing coding-agent CLIs / editors** — single-vendor / non-Claude
     (e.g. `google-gemini/gemini-cli`, `openai/codex`, `voideditor/void`).
  2. **API gateways / proxies / resellers** (e.g. `songquanpeng/one-api`,
     `BerriAI/litellm`, `QuantumNous/new-api`).
  3. **Generic AI apps / clients / platforms** — chat UIs, low/no-code builders,
     "AI second brain" apps (e.g. `danny-avila/LibreChat`, `khoj-ai/khoj`).
  4. **Leaked / rights-infringing content** — republished proprietary system
     prompts, credentials, closed-source material (e.g.
     `asgeirtj/system_prompts_leaks`). Excluded on legal/editorial grounds.
  5. **Non-English README** — the published list is English-language. The
     *description* half of this rule is automatic (`non_english.json` above); a
     repo with an English description but a primarily non-English **README**
     still belongs here, because reading a README needs the network and
     `render.py` never networks. **Bilingual is fine as long as the main one is
     English** — `farion1231/cc-switch` ships an English `README.md` with
     translations beside it and stays. Nothing enforces this half, so it decays
     silently — re-check it in every audit (step 5 below).

  (Generic **non-AI** repos that match only by keyword belong in neither file —
  they fail `scope_filter` and land in `out_of_scope.json` automatically.)

## Working on this

- **Adjust scope** (what counts as in-ecosystem) — `scope_filter` in `config.json`.
  This drives `out_of_scope.json`. Loosen a term to rescue a false positive; tighten
  to push a keyword-only match out. **`scope_filter` and `min_stars` are applied by
  `fetch.py` during the sweep, not by render** — editing them takes effect on the next
  daily sweep (or a manual `fetch.py` run / a `refresh-ranking` `workflow_dispatch`).
  A push to `config.json` does NOT trigger the on-edit re-render (that would publish a
  README that ignores the change); only `filtered.json` edits re-render instantly.
- **Improve categorization** — `category_rules` (`topic_map` / `keyword_rules`) in
  `config.json`; `render.py` assigns the category and groups by it. If you add a new
  category, also add its heading to `render.category_order` (must stay in sync, or it
  falls into "Other"). Rules are applied in this order, first hit wins:
  `match_owner` → keyword rules flagged `"beats_topics": true` → `topic_map` →
  the remaining keyword rules (in file order) → `default_category`. Reach for
  `beats_topics` when the signal describes what a repo *is* and its topics
  describe something else — a course tags the subject it teaches (`mcp`,
  `agents`), so "Learning & guides" must outrank `topic_map` to catch it.
  Verify any rule change by diffing the assignment for the whole published set
  (categorize every repo before and after), not by spot-checking one repo.
- **Change how many are published** — `render.render_count` in `config.json`.
- **Re-tune the English-language cutoff** — `render.non_english_threshold` in
  `config.json`; render applies it immediately, no sweep needed. Calibration: the
  five repos it removes score 0.56–0.78, while bilingual `farion1231/cc-switch`
  scores 0.001.
- **Change the momentum window / Trending size** — `render.trend.window_days` and
  `render.trend.trending_size` in `config.json`. `window_days` drives `Pos`, `+Stars`
  and the Trending cut alike (one baseline, one span).
- **Change the table layout / columns / Table of Contents** — `helpers/render.py`.
  All tables are assembled from the shared `COL_*` specs and `table()`, so add or
  reorder a column there once instead of per table.
- **Exclude an AI-adjacent-but-redundant repo** — add a `{ repo_id, reason }` entry
  to `helpers/filtered.json`.
- **Audit classification** — run the CLASSIFICATION AUDIT below.

## Critical constraints

- `helpers/fetch.py` — exhaustive sweep + auto scope classification; reads
  `helpers/config.json`, writes `helpers/repos.json` + `helpers/out_of_scope.json`.
  Networked. No categorize/brief/rank-to-N/README.
- `helpers/render.py` — reads `repos.json` + `out_of_scope.json` + `filtered.json`,
  selects the top-N, writes `non_english.json` + `repos_to_render.json` +
  `README.md`. **Never networks.**
- `helpers/trend.py` — the **only** git-reading module, as `ghclient.py` is the only
  networking one. Keep git out of `render.py`; keep `trend.py` best-effort (it returns
  `None` instead of raising, so a missing baseline degrades a column rather than
  failing a run). It reads nothing but committed `repos.json` blobs and writes nothing.
- Discovery stays **algorithmic** (an exhaustive sweep), never a hand-maintained
  allowlist. `filtered.json` is the only editorial lever.
- Keep scripts **stdlib-only** — no third-party packages.
- Preserve separation: `fetch.py` writes only `repos.json`/`out_of_scope.json`;
  `render.py` reads those + `filtered.json` and writes only
  `non_english.json`/`repos_to_render.json`/`README.md`. Both CI workflows `git add`
  an explicit file list — a new generated file must be added there too, or it is
  regenerated every run and never committed.
- Any `repos.json` schema change must update the `fetch.py` writer, the `render.py`
  reader, AND this doc + `reference.md` in lockstep.
- The pipeline stays **idempotent** and **deterministic**: same inputs → identical
  outputs (modulo `generated_at`).
- `render.py` must remain safe to re-run anytime (no network, atomic write).
- The big generated files (`repos.json`, `out_of_scope.json`) are committed and have
  a **single writer** (the daily job); don't add a second writer. Rate limits are
  real — `ghclient.py` paces calls; don't remove the throttling.

## CLASSIFICATION AUDIT

The sweep is exhaustive, so there is nothing to "discover" — every repo ≥ `min_stars`
is already in `repos.json`. Auditing means checking that each repo is in the *right*
bucket. **`grep` the large files; don't read them whole.** Note that
`out_of_scope.json` and `repos_to_render.json` hold only repo references (`repo_id` /
`full_name`); their stars/description/topics live in `repos.json` — join on the name
(`grep` the id in `repos.json`) when you need the metadata to judge a repo.

1. **Scope false positives** (ecosystem repos wrongly auto-excluded): scan
   `out_of_scope.json` for repo names that look genuinely Claude/agent/MCP-related,
   then check their description/topics in `repos.json`. Fix by loosening/adding a
   `scope_filter` term in `config.json` (never hand-edit `out_of_scope.json`).
2. **Scope false negatives** (off-topic repos that slipped into the published set):
   inspect `repos_to_render.json` (join `repos.json` for metadata); if a keyword-only
   match shouldn't be in scope, tighten `scope_filter`.
3. **Editorial redundancy** (AI-adjacent but not worth listing): add the repo to
   `helpers/filtered.json` with a `reason`.
4. **Renamed filtered repos** — the one check that needs the network, and the one that
   silently breaks the denylist. `render.py` prints a `note:` counting the
   `filtered.json` entries outside the universe. Most are **dormant**, not dead: an
   excluded repo that slipped under `min_stars` left `repos.json` but keeps its
   exclusion for when it climbs back — **don't delete those.** A *renamed* repo hides
   in the same bucket, and its old id now filters nothing, so it gets published against
   an explicit decision. Separate the two by asking GitHub, which follows renames:
   ```sh
   python3 -c "
   import json
   u={r['full_name'].lower() for r in json.load(open('helpers/repos.json'))['repos']}
   f=json.load(open('helpers/filtered.json'))['filtered']
   print('\n'.join(e['repo_id'] for e in f if e['repo_id'].lower() not in u))" |
   while read -r id; do
     printf '%s\t%s\n' "$id" "$(gh api "repos/$id" --jq '[.full_name,.stargazers_count]|@tsv' 2>/dev/null || echo 404)"
   done
   ```
   A returned `full_name` that differs from the requested id is a rename: repoint the
   entry (keep the `reason`, append `(renamed from <old>)`). A `404` is genuinely gone —
   drop it. Everything else is dormant — leave it alone.
   Expect dropping a `404` to shift `Pos` by one for every repo below it: the column
   re-ranks the baseline snapshot with *today's* exclusions, and the deleted repo is
   still in that older `repos.json`. It self-heals once the baseline rolls past the
   repo's disappearance — don't chase it.
5. **Non-English READMEs** in the published set (exclusion category 5 above) —
   descriptions are now gated automatically in `render.py`, so this audit covers
   the half that still can't be: a repo with an English description whose primary
   README is not English. It needs the network (`gh api`), which is why it is a
   skill-local script and not a pipeline stage:
   ```sh
   python3 .claude/skills/maintain-ranking-scripts/audit_language.py
   ```
   It prints a per-repo `desc`/`readme` ratio to stderr and the hits (either over
   `render.non_english_threshold`) as JSON on stdout. A `desc` hit means the gate
   regressed — fix `render.py`, don't hand-file it. A `readme`-only hit goes to
   `filtered.json` with the reason `non-English README`.
6. Never hand-edit `README.md`, `repos.json`, `out_of_scope.json`,
   `non_english.json`, or `repos_to_render.json`, and never add an allowlist.

## Notes

- The repo intentionally has **no Python deps**; don't add a `requirements.txt`.
- If you change the `repos.json` schema, bump `schema_version` and the docs.
- `render.py` has a min-repo floor on the **published set**; respect it. It also
  warns (non-fatal) when "Other" reaches `render.other_max` — refine
  `category_rules` / `category_order`.
