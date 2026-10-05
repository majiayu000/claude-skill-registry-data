---
name: knowledge-gaps
description: "This skill should be used when the user asks about 'knowledge gaps', 'tool coverage', 'undocumented dependencies', 'undocumented tools', 'concept gaps', 'installed plugins', 'plugin coverage', 'undocumented skills', 'globally installed plugins/skills', 'what is installed on this machine', 'stale/outdated/drifted notes', 'version drift', or 'which tools/packages need updating'. Audits project dependency and tool manifests — and installed Claude Code plugins + skills.sh bundles — against Basic Memory coverage, and detects concept-level hub gaps. Two flag modes: `--stale [brew|npm|cask|crate|vscode|plugin]` checks version drift instead of coverage; `--global` audits what is installed on this machine — Claude Code plugins + skills.sh bundles today — against coverage. Supported ecosystems and full flag mechanics are documented in the skill body."
user-invocable: true
argument-hint: "[--stale [brew|npm|cask|crate|vscode|plugin] [--limit N] [--since <date>] [--sample N] [--full]] [--global]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Skill
  - mcp__basic-memory__search_notes
  - mcp__basic-memory__read_note
  - mcp__basic-memory__list_directory
  - mcp__basic-memory__build_context
  - mcp__basic-memory__recent_activity
  - mcp__readwise__readwise_search_highlights
  - mcp__readwise__reader_search_documents
---

# Knowledge Gap Detection

Analyze the current project's dependencies against Basic Memory coverage to
identify packages that should be documented but aren't. Supports npm, Rust
crates, Go modules, PHP Composer, PyPI, and RubyGems.

When invoked with `--stale [<ecosystem>]`, the skill instead runs an
alternative version-drift workflow (Mode A below) that flags documented
brew/npm/cask/crate/vscode/plugin notes whose recorded version has fallen
behind upstream — not a coverage audit.

## Edge Cases

- **No manifest files found** — if none of the Step 0 globs match, report
  "No package manifest files detected" and skip Steps 1–5. Still proceed to
  Steps 6–9 to check for tool manifests.
- **No tool manifests found** — if Steps 6 finds nothing, report "No tool
  manifests detected" and skip Steps 7–9. Still run Step 10 for dead wiki-links.
- **Ecosystem directory missing in BM** — if `list_directory` returns nothing
  for `npm/`, `crates/`, etc., treat coverage as 0 documented for that
  ecosystem. Do not error.
- **Empty manifest** — if `package.json` has no `dependencies` or
  `devDependencies`, or `Cargo.toml` has no `[dependencies]` tables, report
  "No dependencies found in <manifest>" and skip that ecosystem.
- **Brewfile with only comments or taps** — if no `brew "..."`, `cask "..."`,
  or `vscode "..."` lines exist after filtering, report "No tools found in
  Brewfile".
- **Workflow file with no `uses:` lines** — if a `.github/workflows/*.yml`
  file exists but has no `uses:` lines matching the pattern, skip it silently.
- **RETRO-*.md not committed** — retro files are gitignored; `find` still
  detects them locally. This is expected behavior.
- **Readwise not available** — if `readwise_search_highlights` or
  `reader_search_documents` fails or returns no results, skip the reading-
  signal analysis in Step 14b and report only graph-based hub gaps in Step 15.
- **`bm` CLI not available** — if the `bm project info` command in Step 10
  fails, skip the quick-exit gate and proceed directly with the relation
  index queries.
- **`brew` CLI not available** — if `brew leaves` in Step 7b fails (non-zero
  exit, command not found, or empty output on a non-macOS host), skip the
  Brewfile-vs-installed reconciliation silently and report brew coverage in
  Brewfile-only mode. This is the expected fallback for auditing a remote
  machine's declared deps from a different host.
- **`--global` manifest absent** — if `~/.claude/plugins/installed_plugins.json`
  (plugins) or `~/.agents/.skill-lock.json` (skills) is missing/unreadable in
  Step 7c, skip that population silently and note it; the other still runs. These
  are user-global, so a CI host without `~/.claude` simply yields nothing.
- **`--global` + `--stale` together** — reject; they are separate modes
  (coverage vs drift). Run one at a time.
- **`--full` with a scope flag** — reject `--full` combined with any of
  `--limit`/`--since`/`--sample` ("`--full` can't be combined with
  `--limit`/`--since`/`--sample` — pick one"). `--full` is the opt-out from the
  scope preflight, not a narrowing flag, so pairing it with one is contradictory.
- **Scope preflight is top-level-only** — the `--stale` scope preflight
  (`AskUserQuestion`) fires only in the Mode A skill body, never inside a wave
  subagent. It must never migrate into `references/staleness-detection.md`
  (loaded verbatim into subagents), where `AskUserQuestion` auto-approves and
  returns empty. A sub-40 largest cohort, or any typed scope flag / `--full`,
  skips the prompt.
- **`recent_activity` unavailable or empty (Step 10 recency-scoped sweep)** —
  if the call errors, report "Recency sweep unavailable — could not confirm
  recent-note coverage" in the gap report rather than treating an empty or
  failed result as "zero recently active notes." If it returns zero results
  (no MCP error, empty list), that IS a valid clean state — distinguish the
  two explicitly in the report; do not conflate them.
- **`read_note` fails mid-sweep (Step 10 recency-scoped sweep, step 3)** —
  skip that note, name it in the report ("N of M recently-active notes could
  not be read — sweep is partial"), and continue with the remaining notes.
  Do not silently report the partial result as if it were the full recency
  sweep.

## Workflow

This skill has **two mutually exclusive modes**. Pick exactly one based on
the user's invocation, then run only that mode's steps. Never combine them.

### Mode A — Stale mode (alternative entry point)

**Triggered when:** the user invoked the skill with the `--stale` flag (e.g.,
`/knowledge-gaps --stale`, `/knowledge-gaps --stale npm`), or used trigger
phrases like "stale notes", "outdated formulae", "drifted notes", "which tools
need updating".

**Argument parsing:** `--stale` takes an optional ecosystem token —
`--stale [brew|npm|cask|crate|vscode|plugin]`:

- **bare `--stale`** → check all six supported cohorts.
- **`--stale <token>`** where the token ∈ `brew|npm|cask|crate|vscode|plugin`
  → check only that cohort.
- **any other token** (e.g. `action`, `gh`, `go`, `docker`, `skill`, `pypi`,
  `gem`, `composer`) → reject with: "`--stale` supports brew, npm, cask, crate,
  vscode, plugin. `action`/`gh`/`go`/`docker` have no single canonical
  comparable version; `skill` is unsupported (no comparable version);
  `pypi`/`gem`/`composer` are deferred." Do NOT silently fall back to all.

**Scope modifiers (additive):** after the ecosystem token, `--stale` also
accepts three optional scoping flags, in any order —
`--stale [<eco>] [--limit N] [--since <date>] [--sample N]`. These exist for
large cohorts (e.g. a 388-note `npm` directory) where the default full sweep
is impractical in one turn. Applied **per cohort** — a bare `--stale --limit
50` run against all six cohorts checks up to 50 notes in EACH of
brew/npm/cask/crate/vscode/plugin, not 50 total.

- **`--since <date>`** — the highest-leverage flag: it restricts the cohort to
  notes NOT touched since `<date>` (ISO `YYYY-MM-DD`), and does so BEFORE the
  upstream fetch (S3) and before S2's per-note read storm — it shrinks N, it
  doesn't just filter the rendered report. Resolved via one
  `recent_activity(timeframe="<date>")` call, not N `read_note` calls. See the
  staleness-detection reference's S1 for the exact mechanics.
- **`--limit N`** — caps the (optionally `--since`-narrowed) cohort to the
  first N notes in listing order. Deterministic: the same input always yields
  the same slice — which is exactly why it is **not** safe to tile a large
  cohort into waves on its own (a second `--limit N` call re-fetches the
  identical first N notes rather than advancing). Only safe to layer on top
  of an already date-disjoint `--since` slice; partitioning itself uses
  successive `--since` cutoffs, not `--limit` (see "Large-cohort strategy" in
  the reference file for the actual mechanism).
- **`--sample N`** — takes a random N-note sample instead of the first N — an
  unbiased bounded slice for a cohort too large to sweep in full, its N notes
  checked the same way as any other scope (it estimates no drift rate and
  extrapolates nothing). Not partition-safe (overlapping/uncovered draws across
  separate runs) — use it for a single bounded run, never to tile a full sweep.

`N` must be a positive integer and `<date>` a valid ISO date; reject a
malformed value by name rather than silently ignoring it. `--limit` and
`--sample` both set a cohort size, so they're mutually exclusive — if both
appear, reject with: "`--limit` and `--sample` can't both be set — pick one."

- **`--full`** — skips the interactive scope preflight below and sweeps the
  full cohort unscoped. It is the power-user opt-out from the preflight prompt,
  not a scope *narrower* — so it is mutually exclusive with the three scope
  flags. If `--full` appears alongside any of `--limit`/`--since`/`--sample`,
  reject with: "`--full` can't be combined with `--limit`/`--since`/`--sample`
  — pick one." (`--full` already implies the widest scope; a narrowing flag
  contradicts it.)

**Scope preflight (interactive, top-level only).** Before delegating to the
staleness-detection workflow, and **only in this top-level skill body** (a human
is present at every `/knowledge-gaps` invocation), run a one-question scope
preflight for large unscoped sweeps. This mitigates a filed, still-open upstream
limitation — Basic Memory has no bulk metadata/version projection, so the drift
sweep must `read_note` every entity in a cohort (`UPSTREAM-basic-memory.md`,
*No bulk metadata/version extraction*); the preflight lets a human shrink N
*before* that O(N) read storm rather than after. It is a UX layer over the open
gap, **not** a reopening of automated wave orchestration (spike `vp-claude-4g53`,
DEFER verdict) — it automates nothing, it only helps a human pick an existing
scope flag.

**Never place this preflight in `staleness-detection.md`.** That file is loaded
verbatim into wave subagents, and `AskUserQuestion` auto-approves / returns empty
answers inside a subagent — so an interactive gate there silently no-ops. The
gate is safe *by construction* only here, in Mode A's top-level body.

Run the preflight when **both** conditions hold:

1. **No scope modifier was typed** — none of `--limit`/`--since`/`--sample`, and
   `--full` was not passed (either flag skips the preflight: a typed scope flag
   already answers the question; `--full` is the explicit opt-out).
2. **The largest selected cohort exceeds 40 notes.** Learn each selected
   cohort's size from one cheap `list_directory(dir_name="<cohort-dir>",
   depth=1)` per selected cohort (the same listing S1 needs anyway) — a count
   only, no `read_note`. For bare `--stale` that is one listing per cohort; for
   `--stale <eco>` it is a single listing. Compare the *largest* count to 40.

The threshold 40 is an honest heuristic (≈5 concurrent reads/turn; a serialized
1s/call crate cohort; well below the 122-note brew incident this preflight was
built for) with no config surface by design — if it fires too eagerly or too
late in practice, it is a one-literal edit here.

When both conditions hold, ask **once** with a single `AskUserQuestion` — one
question object regardless of how many cohorts qualify (fold the per-cohort
counts into the question body), neutral framing. The menu is three options, or
four when the single-ecosystem sample option below applies.

**Scope question** (always asked):

1. **Full sweep (all N)** — check every documented note in the selected cohort(s).
2. **Untouched in the last 90 days (recommended)** — resolves to `--since <date>`
   where `<date>` is today minus 90 days in ISO `YYYY-MM-DD`. This is the
   **broader** narrowing: it keeps every note not refreshed in roughly the last
   three months. Recommended because it gives the widest coverage short of a full
   sweep, and because `--since`'s result set nests cleanly across repeat runs
   (per this skill's own S1 mechanics).
3. **Untouched in the last 180 days** — resolves to `--since <date>` where
   `<date>` is today minus 180 days, ISO. This is a **tighter subset** of option
   2, *not* a wider one: a note untouched for 180 days is necessarily also
   untouched for 90, so option 3 ⊆ option 2 ⊆ full. Pick it to check only the
   most-neglected notes (not refreshed in roughly six months) — a smaller cohort
   than option 2, not a larger one. When framing the options to the user (labels
   and question body), state this direction explicitly so a longer window is
   never mistaken for a bigger cohort.
4. **Random sample of 30, excluding the last 7 days (recency-floored, unbiased
   slice)** — *offered only for a single-ecosystem `--stale <eco>` run whose one
   cohort is very large* (**> 150 notes**); never for a bare `--stale` (see below
   for why). Resolves to `--since <today−7d> --sample 30` — compute the 7-day
   cutoff at runtime, the same way options 2/3 compute theirs — a random 30-note
   draw from the notes NOT touched in the last week, *checked in full*, the same
   per-note enumeration as any other scope. It computes **no** drift rate and
   extrapolates nothing; it is simply the only narrowing that stays representative
   when a cohort is both huge *and* actively touched, so neither `--since` *window*
   is tractable on its own: the 90-day narrowing still leaves more than one turn
   can process (dogfood: ~70 on a ~500-note npm cohort) while the 180-day option
   resolves to ≈0 (nothing sits untouched that long on a maintained graph), and
   `--limit`'s alphabetical slice (brew starts at `aarch64…`) would be a *biased*
   subset. The 7-day floor is a **narrow guard, not a staleness-narrowing
   strategy**: it excludes only notes an upgrade-haul (or any refresh) may have
   stamped with today's date moments earlier, so the draw stays representative of
   the wider cohort — unlike options 2/3, whose 90/180-day floors deliberately
   bias toward the *most*-neglected notes as their whole strategy. Its
   non-partition-safety (overlapping draws across runs) does not matter here — the
   preflight is a single-shot pick, not a tiled sweep. Below the 150 bar this
   option is **not** shown (a 90-day narrowing suffices — brew's 122-note cohort
   collapsed to 2), keeping the menu at three options for the common case. A
   different cutoff or sample size stays available as a typed
   `--since <date> --sample N` combo (already valid — only `--limit`+`--sample`
   are mutually exclusive, not `--since`+`--sample`; a typed combo bypasses this
   preflight).

Compute all cutoff dates at runtime — never hardcode them. **`--limit` is never a
preflight option** (it stays a typed flag): its alphabetical slice is the very
bias the sample option above is chosen to avoid, so it belongs layered on a typed
`--since`, not offered here.

The sample option is **single-ecosystem-only**. A bare `--stale --sample 30`
would draw 30 notes from *each* selected cohort and silently truncate the smaller
ones (a 45-note cask cohort → a random 30), so the > 150 gate is scoped to a
single `--stale <eco>` run by construction — never offered for a bare `--stale`.
The 150-note bar (like the 40-note trigger above) is a fixed heuristic with no
config surface — a one-literal edit if it fires too eagerly or too rarely.

**On no response (timeout):** default to option 2 (`--since <today−90d>`) —
**never** the full sweep, and **never** the sample even when it was on the menu.
The full sweep is the costliest option, so defaulting to it on silence would
reintroduce the exact blow-up this preflight exists to prevent. The sample,
though *cheaper* than the 90-day narrowing, is a random draw — a silent automatic
default must be deterministic and reproducible, which a stochastic sample is not
— so the deterministic 90-day `--since` is always the fallback, regardless of
whether the sample was offered. How long to wait before defaulting is the
executing session's own timeout config, not a number hardcoded here.

One caveat where the sample option *was* on the menu (a single >150 cohort whose
90-day narrowing is itself known to leave more than one turn can process): the
90-day timeout fallback keeps determinism but does **not** by itself make that
cohort one-turn-tractable. Flag the resulting default sweep as possibly partial
and prefer the Large-cohort wave-tiling strategy (see `staleness-detection.md`)
over silently attempting one oversized turn — a truncated single-turn sweep would
under-report drift with no signal that it stopped early.

Once the scope is resolved (a typed flag, an interactive pick, or the timeout
default), carry it forward as if it had been typed and proceed to **What to do**
below. A natural-language trigger with no flags is treated exactly like a bare
`--stale` — the same threshold check applies (the gate lives in these shared
Mode A instructions, not in slash-command parsing, so it fires identically on
both routes).

**What to do:** load and follow the staleness-detection reference file in
full — do NOT execute any of the Mode B steps below in the same session:

`${CLAUDE_PLUGIN_ROOT}/skills/knowledge-gaps/references/staleness-detection.md`

Pass the parsed ecosystem scope (one cohort, or all six) AND the resolved scope
value — any typed `--limit`/`--since`/`--sample`, or what the scope preflight
resolved to: a `--since <date>` (90d/180d pick or timeout default) or a
`--since <today−7d> --sample 30` (the large single-cohort recency-floored sample option) — to that workflow; it runs the
per-cohort drift check and renders one `### Version Drift — <eco>` section per
checked cohort. Also pass how the scope was chosen (typed flag / interactive pick
/ timeout default) so S8 can stamp its provenance footnote.

### Mode B — Standard mode (manifest-driven coverage)

**Triggered when:** the user invoked the skill *without* the `--stale` flag.

The remaining steps below (numbered 0 through 15) describe this mode only.
**Skip them entirely when `--stale` is present** — Mode A is a complete
alternative workflow.

The `--global` flag is a Mode B addition: when present, it activates **Step 7c**
(user-global installed-plugin / skill coverage) alongside the project-manifest
steps. `--global` and `--stale` are mutually exclusive — if both appear, reject
with "`--global` (coverage) and `--stale` (drift) are separate modes; run one."

#### 0. Detect project ecosystems

Before parsing dependencies, scan for manifest files using the `Read` tool
(not Bash). Check for the following in the current working directory:

| Manifest file | Ecosystem | BM directory |
|---------------|-----------|-------------|
| `package.json` | npm | `npm/` |
| `Cargo.toml` | Rust / crates | `crates/` |
| `go.mod` | Go modules | `go/` |
| `composer.json` | PHP / Composer | `composer/` |
| `requirements.txt` or `pyproject.toml` | Python / PyPI | `pypi/` |
| `Gemfile` or `Gemfile.lock` | Ruby / RubyGems | `gems/` |

A project may have multiple manifest files (e.g., a monorepo with both
`package.json` and `Cargo.toml`). Process each detected ecosystem separately
and combine results in the final report.

Check for root-level manifest files using `Read` — do not use `Glob` for
root manifests, as it recurses into `node_modules/` and similar directories:

```
Read("./package.json")
Read("./Cargo.toml")
Read("./go.mod")
Read("./composer.json")
Read("./pyproject.toml")
Read("./requirements.txt")
Read("./Gemfile")
```

If Read succeeds, the ecosystem is present and the content is already loaded
for Step 1 (no re-reading needed). If Read returns "file not found", skip
that ecosystem.

#### 1. Parse dependencies

For each detected ecosystem, read the manifest and extract dependencies:

**npm** (`package.json`):
Read `package.json` and extract all `dependencies` and `devDependencies` keys.
Exclude workspace packages (check `workspaces` field and skip matching entries).

**Rust** (`Cargo.toml`):
Read `Cargo.toml` and extract `[dependencies]`, `[dev-dependencies]`, and
`[build-dependencies]` table keys. Exclude workspace members.

**Go** (`go.mod`):
Read `go.mod` and extract all `require` directives. Ignore indirect
dependencies (`// indirect` comments) unless explicitly requested.

**PHP Composer** (`composer.json`):
Read `composer.json` and extract `require` and `require-dev` keys. Skip
`php` and `ext-*` entries (platform requirements, not packages).

**Python PyPI** (`pyproject.toml` or `requirements.txt`):
- `pyproject.toml`: extract `[project].dependencies` array and
  `[project.optional-dependencies]` entries
- `requirements.txt`: extract package names (strip version specifiers)

**Ruby** (`Gemfile`):
Read `Gemfile` and extract all `gem '<name>'` lines. Group by Bundler groups
(`group :development`, etc.).

#### 2. Check Basic Memory coverage

For each ecosystem, get all documented packages in one lightweight call:

```
list_directory(dir_name="<ecosystem-dir>", depth=1)
```

This returns all `<prefix>-*` note titles without loading content.
Cross-reference against the dependency list to classify each package:
- **Documented** — a `<prefix>-<package-name>` note exists
- **Undocumented** — no dedicated note

For undocumented packages that land in Tier 1 (after step 3), check if
they're mentioned in engineering notes:
```
search_notes(search_type="text", query="<package-name>", page_size=3)
```

Classify matches as:
- **Mentioned** — appears in a note but isn't the primary subject

Limit this fallback to Tier 1 candidates to avoid excessive API calls.

#### 3. Tier by import frequency

For undocumented packages, count imports using the Grep tool. Ripgrep
automatically respects `.gitignore`, skipping `node_modules`, `.git`, etc.

**npm:**
```
Grep(pattern="from ['\"]<package-name>['\"/]", glob="**/*.{js,ts,mjs,cjs}", output_mode="count")
Grep(pattern="require\\(['\"]<package-name>['\"/]", glob="**/*.{js,ts,mjs,cjs}", output_mode="count")
```

**Rust:**
```
Grep(pattern="use <crate_name>::", glob="**/*.rs", output_mode="count")
Grep(pattern="extern crate <crate_name>", glob="**/*.rs", output_mode="count")
```
(Replace hyphens with underscores for the crate name in `use` statements.)

**Go:**
```
Grep(pattern="\"<module/path>\"", glob="**/*.go", output_mode="count")
Grep(pattern="\"<module/path>/", glob="**/*.go", output_mode="count")
```

**PHP Composer:**
```
Grep(pattern="use <Vendor>\\\\<Package>", glob="**/*.php", output_mode="count")
```

**Python:**
```
Grep(pattern="import <package_name>", glob="**/*.py", output_mode="count")
Grep(pattern="from <package_name>", glob="**/*.py", output_mode="count")
```
(Replace hyphens with underscores for import names.)

**Ruby:**
```
Grep(pattern="require ['\"]<gem_name>['\"]", glob="**/*.rb", output_mode="count")
```

For scoped npm packages (e.g., `@fastify/postgres`), match the full name —
the `@` and `/` don't need escaping in the pattern.

Classify:
- **Tier 1** (3+ files import it): Must document — core dependency
- **Tier 2** (1-2 files): Should document — used but limited scope
- **Tier 3** (devDependencies/dev only, 0 runtime imports): Optional — tooling

#### 4. Generate gap report

Present a structured report with a section per ecosystem. See
`${CLAUDE_PLUGIN_ROOT}/skills/knowledge-gaps/references/report-templates.md`
("Package coverage report") for the full format: a
`## Knowledge Gap Report — <project>` header, one `### <eco> Coverage: X/Y (Z%)`
section per ecosystem (each with Tier 1 / Tier 2 / Tier 3 / Already Documented
subsections, packages ranked by import count), then an `### Overall Summary`.

#### 5. Offer enrichment

For the top 3-5 undocumented Tier 1 packages across all ecosystems, offer to
run `/intel` with the appropriate prefixed invocation:

- npm: `/intel fastify`
- crate: `/intel crate:serde`
- go: `/intel go:github.com/gin-gonic/gin`
- composer: `/intel composer:laravel/framework`
- pypi: `/intel pypi:requests`
- gem: `/intel gem:rails`

Present packages ranked by import count.

---

#### 6. Detect tool manifests

Glob for tool manifest files in the current working directory:

```
Read("./Brewfile")
Glob(pattern=".github/workflows/*.yml")
Glob(pattern=".github/workflows/*.yaml")
Read("./Dockerfile")
Glob(pattern="*.dockerfile")
Glob(pattern="Dockerfile.*")
Read("./.vscode/extensions.json")
```

Announce which manifests are found. If none are found AND `--global` was not
passed, skip Steps 7–9 and note "No tool manifests detected" in the report. If
`--global` was passed, still run **Step 7c** — it reads user-global manifests
independent of any project tool manifest.

#### 7. Parse tool manifests

For each detected manifest, read and extract tool identifiers:

**Brewfile:**
Read the file and extract entries by line pattern:
- `brew "<name>"` or `brew '<name>'` → `brew:<name>`
- `cask "<name>"` or `cask '<name>'` → `cask:<name>`
- `vscode "<publisher>.<ext>"` or `vscode '<publisher>.<ext>'` → `vscode:<publisher>.<ext>`

Skip comment lines (`#`) and other directive types (`tap`, `mas`, `whalebrew`).

Keep the parsed `brew:` set as the **Brewfile-declared** set. Step 7b reconciles
it against actual installed leaves before coverage is computed.

**`.github/workflows/*.yml` / `*.yaml`:**
Read each workflow file. Grep for `uses:` lines:
```
Grep(pattern="uses:\\s+[^./]", glob=".github/workflows/*.{yml,yaml}", output_mode="content")
```

From each match, extract the action reference:
- `uses: actions/checkout@v4` → `action:actions/checkout`
- `uses: docker://alpine:3.18` → skip (docker:// protocol, not an action)
- `uses: ./.github/actions/my-action` → skip (local action, `./` prefix)

Strip `@version` suffix. Deduplicate across all workflow files.

**`Dockerfile` / `*.dockerfile` / `Dockerfile.*`:**
Read each Dockerfile. Extract `FROM` lines:
```
Grep(pattern="^FROM\\s+", glob="{Dockerfile,*.dockerfile,Dockerfile.*}", output_mode="content")
```

From each match, extract the image identifier:
- `FROM node:22-alpine` → `docker:node` (strip `:tag`)
- `FROM node:22-alpine AS builder` → `docker:node` (strip `AS alias` and tag)
- `FROM gcr.io/distroless/node` → skip (non-Docker-Hub registry)
- `FROM ghcr.io/owner/image` → skip (non-Docker-Hub registry)
- `FROM quay.io/org/image` → skip (non-Docker-Hub registry)

Skip registries with a `.` or `/` prefix that indicates non-Docker-Hub. Strip
version tags (`:tag`) and AS aliases. Deduplicate across files.

**`.vscode/extensions.json`:**
Read the file and extract the `recommendations` array. Each entry is a
`vscode:<publisher>.<extension-id>` identifier. Example:
```json
{ "recommendations": ["esbenp.prettier-vscode", "dbaeumer.vscode-eslint"] }
```
→ `vscode:esbenp.prettier-vscode`, `vscode:dbaeumer.vscode-eslint`

#### 7b. Reconcile Brewfile against `brew leaves` (ground truth)

The Brewfile is **aspirational** (what the user *declared* they want installed)
— `brew leaves` is **actual** (formulae installed and not pulled in as a
dependency of something else). The two diverge in two directions worth
surfacing:

- **Installed but not Brewfile-declared** — silent leaves that snuck in via
  `brew install` outside the Brewfile. These are real usage signals worth
  documenting, even though no manifest declares them.
- **Brewfile-declared but not installed** — dead declarations the user
  intends but never realised, or formulae they have since uninstalled.

**When to run:** only if Step 7 parsed at least one `brew:<name>` entry from
a Brewfile (no Brewfile → nothing to reconcile, skip this step).

**Detection:** check whether the `brew` CLI is available and runnable:

```
Bash: command -v brew >/dev/null 2>&1 && brew leaves 2>/dev/null
```

If the command succeeds, treat its stdout (one formula name per line) as the
**installed-leaves set**. If it fails (non-zero exit, command not found, or
empty output on a non-macOS host), skip the reconciliation silently and
proceed to Step 8 with the Brewfile-declared set unchanged — this is the
expected fallback when auditing a remote machine's declared deps from a
different host.

**Why `brew leaves` and not `brew list` or the Homebrew MCP:**
- `brew list` includes transitive dependencies — the audit would flood with
  formulae the user never asked for (e.g., `openssl@3`, `libffi`).
- The Homebrew MCP's list endpoint returns plain text without
  `installed_on_request` metadata, so leaves cannot be distinguished from
  transitive deps.
- Per-formula Homebrew MCP info calls would need ~190 invocations at
  2-5s each — minutes of latency for one audit. `brew leaves` is the
  canonical leaf-finder and returns in ~200ms.

**Compute the diff** between `brewfile_declared` and `installed_leaves`:

- `installed_unlisted = installed_leaves − brewfile_declared`
- `declared_uninstalled = brewfile_declared − installed_leaves`
- `installed_and_declared = brewfile_declared ∩ installed_leaves`

**Update the brew set for Step 8:** the canonical installed-formulae set
used for BM coverage classification becomes
`installed_leaves ∪ brewfile_declared` (union — document anything the user
either declared or actually installed as a leaf). The two diff buckets are
carried forward for Step 9 to surface in the report.

If `brew leaves` was unavailable, the set used in Step 8 is just
`brewfile_declared`, and Step 9 reports brew coverage in Brewfile-only mode
without the diff buckets.

#### 7c. Detect host-installed sources (`--global`; plugins + skills today)

**When to run:** only when invoked with `--global`. `--global` audits what is
INSTALLED ON THIS MACHINE (vs. what the project *declares*) against coverage —
it reads USER-GLOBAL manifests in `$HOME` (`~/.claude/plugins/*`,
`~/.agents/.skill-lock.json`), not the project. That is why it is opt-in (the
result varies by machine and is not CI-reproducible) and why the Step 9 report
section is labelled "user-global". Today it covers Claude Code plugins +
skills.sh bundles; other host-installed sources (e.g. `brew leaves`, installed
VSCode/`gh` extensions — bd `vp-claude-1u1` et al.) are candidate sub-steps under
the same flag. This inverts the default's `gh:` handling: `gh:` has no *project*
manifest, but it does have an installed list (`gh extension list`) — detecting
that is a future `--global` sub-step, not a permanent exclusion.

The resolution (the `<name>@<marketplace>` → `owner/repo` join across
`installed_plugins.json` + `known_marketplaces.json` + each marketplace's
`marketplace.json`, the four `source` shapes, and skill grouping-by-source) is
deterministic, so it lives in a script — not in this prose:

```
Bash: node ${CLAUDE_PLUGIN_ROOT}/scripts/list-installed-plugins.mjs
```

It reads no stdin and emits one NDJSON record per installed plugin / skill-bundle:

```
{"identifier":"plugin:voxpelli/vp-claude#vp-knowledge","title":"plugin-voxpelli-vp-claude-vp-knowledge","installedAt":"…","members":[],"sourceResolved":true}
{"identifier":"skill:basicmachines-co/basic-memory-skills","title":"skill-basicmachines-co-basic-memory-skills","installedAt":"…","members":["memory-notes","memory-research"],"sourceResolved":true}
```

- `identifier` is the `/intel plugin:`/`skill:` address; `title` is the
  pre-normalized BM-note title Step 8 matches on; `members` is the grouped
  skill-dir roster (the report's "Skills installed" column); `installedAt` drives
  the Step 9 recency cap.
- `sourceResolved: false` means owner/repo could not be determined (no
  `marketplace.json` / unknown source shape) — always Undocumented, shown as
  "resolve manually".
- A **non-zero exit or empty output** → skip that population silently and note it
  (a fresh machine / CI host with no `~/.claude` is normal — mirrors the
  `command -v brew` fallback in Step 7b). Do NOT abort the audit.

Carry the parsed records forward to Step 8.

#### 8. Check Basic Memory coverage for tools

For each tool type with detected entries, get all documented tools in one call:

```
list_directory(dir_name="brew", depth=1)
list_directory(dir_name="casks", depth=1)
list_directory(dir_name="actions", depth=1)
list_directory(dir_name="docker", depth=1)
list_directory(dir_name="vscode", depth=1)
```

Only query directories for tool types that had manifest entries detected.
Cross-reference against the parsed identifiers to classify each tool:
- **Documented** — a `<prefix>-<name>` note exists
- **Undocumented** — no dedicated note

When Step 7c ran (`--global`), get the documented `claude_plugin` set — matched by
NOTE TYPE, not directory, since legacy notes may live outside `plugins/`:

```
list_directory(dir_name="plugins", depth=1)
search_notes(query="plugin skill", note_types=["claude_plugin"], page_size=100)
```

Match each Step 7c record's `title` against a `claude_plugin` note. For a miss,
fall back to `search_notes(query="<bare-name>", note_types=["claude_plugin"], page_size=5)`
where `<bare-name>` is the last `/`- or `#`-segment of the identifier — this catches
legacy-titled notes (e.g. a note titled "beads-marketplace" for an installed beads
plugin). Classify Documented / Undocumented as above; `sourceResolved:false` records
are always Undocumented.

#### 9. Add tools section to gap report

Append a tools section to the gap report after the package sections. See
`${CLAUDE_PLUGIN_ROOT}/skills/knowledge-gaps/references/report-templates.md`
("Tool coverage report") for the full format: one `### <type>: X/Y documented`
section per tool type (no import-count tiering — group by type, documented vs
undocumented), with a Brewfile ↔ installed reconciliation sub-section under
Homebrew Formulae only when Step 7b ran (`brew leaves` available; otherwise the
"Brewfile-only mode" note), then a `### Tool Summary`.

No import-count tiering for tools — all manifest entries are equally "used".
Group by type, show documented vs undocumented count per type.

For the top undocumented tools, offer `/intel` invocations:

- brew: `/intel brew:ripgrep`
- cask: `/intel cask:warp`
- action: `/intel action:actions/checkout`
- docker: `/intel docker:node`
- vscode: `/intel vscode:esbenp.prettier-vscode`

When Step 7c ran, append a **Plugin/Skill Coverage** section (template in
`report-templates.md`, labelled user-global). The coverage TABLE lists ALL
installed plugins/skills (the `X/Y documented` count needs the full denominator;
first **dedup the records by `title`** — the same plugin installed from two
marketplaces resolves to one title and would otherwise inflate `Y`),
but the actionable `/intel` OFFER below it is capped to the **top 5
undocumented by `installedAt`** (most recent first), with "…and N more — re-run to
see all" when truncated. When **0** `claude_plugin` notes match, lead the section
with "No plugin/skill notes yet — here are the 5 most-recently-installed to start"
rather than an all-red wall. Offer (use each record's `identifier` verbatim):

- plugin: `/intel plugin:<owner>/<repo>` (with `#<name>` when the record has it)
- skill: `/intel skill:<owner>/<repo>`

---

#### 10. Detect dead wiki-links

Check the graph for wiki-links referencing non-existent notes — organic
documentation debt surfaced by the graph itself.

**Quick-exit gate:** Check the unresolved count first:
```
Bash: bm project info main --json | jq '.statistics.total_unresolved_relations'
```
If the count is 0, skip this step. If the CLI is unavailable, proceed with
the search.

**Query the relation index** for each ecosystem detected in Steps 0–9.
Use `entity_types=["relation"]` to search the relation index directly —
this returns relation objects with `from_entity` and `to_entity` fields:

```
search_notes(query="npm-", entity_types=["relation"], output_format="json", page_size=50)
search_notes(query="crate-", entity_types=["relation"], output_format="json", page_size=50)
search_notes(query="go-", entity_types=["relation"], output_format="json", page_size=50)
search_notes(query="composer-", entity_types=["relation"], output_format="json", page_size=50)
search_notes(query="pypi-", entity_types=["relation"], output_format="json", page_size=50)
search_notes(query="gem-", entity_types=["relation"], output_format="json", page_size=50)
search_notes(query="brew-", entity_types=["relation"], output_format="json", page_size=50)
search_notes(query="action-", entity_types=["relation"], output_format="json", page_size=50)
search_notes(query="docker-", entity_types=["relation"], output_format="json", page_size=50)
search_notes(query="vscode-", entity_types=["relation"], output_format="json", page_size=50)
```

Only query prefixes for ecosystems detected in Steps 0–9.

**Identify unresolved relations:** For each result, check whether `to_entity`
is present in the JSON response. Relations missing `to_entity` are unresolved
— the wiki-link target has no corresponding note.

Extract the target name from the relation `title` (format:
`"source -> target"` — ASCII, not `→`) or `matched_chunk`. When the target
is unresolved the title is the **source name alone, with no arrow at all**,
which is exactly the case this technique exists to find. Cross-reference against the
`list_directory` results from Steps 2 and 8 to confirm.

**Deduplicate:** If a dead-linked package already appears in Tier 1/2/3
from manifest parsing, add "(also wiki-linked)" annotation rather than
listing it twice.

**Recency-scoped sweep (large-directory blind spot):** the relevance-ranked
query above is biased toward old, frequently-linked notes — in a large,
active ecosystem directory (e.g. `brew/`, ~190 notes) the top 50
relevance-ranked rows can be entirely old resolved links, never reaching
notes created that same session. Confirmed empirically: a `brew-` prefix
relation query returned only resolved old links, while 8 `brew-*` notes
created that day carried 11 dangling edges that were only found by reading
those notes directly — the relevance sweep reported a false-clean for the
largest, most-active directory in the graph. Run this sweep in addition to
the relevance-ranked query above, not instead of it:

1. Get recently-active ecosystem/tool notes in one call:
   ```
   recent_activity(timeframe="7d", type="entity", output_format="json")
   ```
2. Filter the result to titles matching a detected ecosystem/tool prefix
   (`npm-`, `crate-`, `go-`, `composer-`, `pypi-`, `gem-`, `brew-`,
   `action-`, `docker-`, `vscode-`) — the same prefixes queried above.
3. For each surviving note, `read_note` it and extract every `[[Target]]`
   wiki-link in its `## Relations` section.
4. For each target that itself matches an ecosystem/tool prefix, check it
   against the `list_directory` results already gathered in Steps 2 and 8 —
   a target absent from that title set is a dangling edge the relevance
   sweep may have missed.

This is O(recently-active notes), not O(corpus) — it stays cheap because it
is bounded by the 7-day window rather than directory size, and it is
recency-complete regardless of how large or old-link-dominated the
directory is. Merge findings from both sweeps into one table, deduplicating
by target.

Add dead-link findings to the gap report:

```
#### Referenced but not documented (dead wiki-links)
| Link | Referenced in | Detected via |
|------|--------------|--------------|
| [[npm-some-pkg]] | npm-fastify, engineering/patterns/http | relevance |
| [[brew-some-tool]] | brew-newly-added | recency |
```

Add dead-link counts to the Overall Summary:
```
- Dead wiki-links: Q (across R unique notes)
```

When offering enrichment (Steps 5, 9), include dead-link targets annotated
with "(wiki-linked in N notes)" to show organic graph momentum.

**Limitation:** `page_size=50` per prefix on the relevance-ranked query is a
sample, not exhaustive — the graph may have more unresolved relations than
one page returns, and in a large directory the sample skews toward old,
frequently-linked notes rather than recent ones (see the recency-scoped
sweep above, which exists specifically to cover that blind spot). Even with
both sweeps combined this remains a bounded gap-detection pass, not a full
audit — a note edited outside the 7-day window whose dangling edge also
falls outside the top-50 relevance-ranked sample is still missed by design
(the gardener handles comprehensive auditing). The highest-scored results
surface the most commonly referenced dead links; the recency sweep surfaces
the most recently introduced ones.

---

#### 11–13. Domain standard detection

Read the standard detection reference file for Steps 11–13:
`${CLAUDE_PLUGIN_ROOT}/skills/knowledge-gaps/references/standard-detection.md`

This covers detecting domain standards in Basic Memory, classifying them by
codebase reference count, and adding a standards section to the gap report.

---

#### 14–15. Concept-level gap detection

Read the concept detection reference file for Steps 14–15:
`${CLAUDE_PLUGIN_ROOT}/skills/knowledge-gaps/references/concept-detection.md`

This covers mining the relation graph for implicit hub gaps, checking
Readwise for reading signals, and adding a concept coverage section to
the gap report.
