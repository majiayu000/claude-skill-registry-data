---
name: harness-bootstrap
description: "Install or sync the generic harness runway in any repo — greenfield or with code present. Scaffolds CLAUDE.md, AGENTS.md (foreign-executor contract), CODING_STANDARDS.md (headings-only), skeleton docs (overview, techstack, decisions, specs/, work/), path-scoped rules, and the core plugin pin; bakes in doc-sync discipline. On greenfield it writes empty product skeletons; stack-matched skill/MCP/hook curation is gated tier-2, orchestrated by /super-bootstrap:setup; opt-in earn-gated scale module (parked + test-queue + outward containers, card fact fields). Monorepo tier fans path-scoped rules out per package; adopt mode retires superseded harness forks and backfills skeleton sections added since bootstrap on re-run. Solo dev workflow."
tags: [harness, scaffold, setup, meta, docs]
---

# Super Bootstrap — Development Pipeline for Any Repo

Set up (or sync) the development pipeline in a project. Installs harness — workflow rules, doc-sync gate, skeleton docs, the core plugin pin — in one scaffold session. The doc-sync gate at every later commit grows the skeleton docs over time, so there's no deferred deep-scan stage.

Designed for a solo developer working across multiple Claude Code sessions and cloud Claude Code.

## Phase 1: Quick Scan (lightweight, parallel reads)

Gather just enough to scaffold — skim manifests for stack/version, note structure shape, stop.

Check contributor count (`git shortlog -sn --all | head -5`). If >1 active contributor, surface as info — don't block:
> "FYI: detected multiple contributors. The pipeline's CLAUDE.md assumes solo dev (simple branching, no PRs for self-review). You can edit those sections after bootstrap if your team's workflow differs."

### Sampling Discipline (applies to all source-file reads)

Throughout this skill — Phase 1 detection, anywhere Claude reads source files — **paraphrase structure into committed docs; never paste raw file contents.** Skip files whose names suggest secrets (e.g. `.env*`, `*.key`, `*.pem`, `id_*`, `*credential*`, `*secret*`, `.npmrc`, `.netrc`, `*.p12` / `*.pfx`, `*.keystore`, `kubeconfig` — illustrative, judge by name).

When skipping, surface to user: `⊘ skipped <path> (likely secret)`.

Reason: reading alone isn't the breach — Claude's context isn't shared. The breach is **quoting raw content into auto-committed docs** (`techstack.md`, `overview.md`): a gitignored secret becomes permanent in git history. Defense lives in the write step. The illustrative list seeds pattern recognition for the skip step; new secret-bearing patterns are judged by name, not table lookup.

### Manifest Detection

Detect language/runtime by manifest files at repo root (e.g. `package.json`, `tsconfig.json`, `pyproject.toml` / `requirements.txt`, `Cargo.toml`, `go.mod`, `Gemfile`, `pom.xml` / `build.gradle`, `composer.json`, `pubspec.yaml`, `CMakeLists.txt` / `Makefile`, `*.csproj` / `*.sln` — illustrative, not exhaustive). Don't read fully — skim each for runtime/version, top-level deps, scripts/build commands. Cover unlisted stacks (Bun, Deno, Zig, Elixir, Gleam, etc.) by analogy from the manifest's contents.

**Code presence.** A manifest, or any source file (e.g. `.js` / `.ts` / `.py` / `.go` / `.rs` / `.sh` — scripts included; illustrative, judge by analogy), sets **code present**. Neither → **docs-only repo**: the code-touch pair — CLAUDE.md § Coding Principles and `CODING_STANDARDS.md` — is not applicable, the way monorepo-only sections are on a single-package repo (§ Pipeline-owned): the drift walk skips both and the receipt's `covered` omits them. A re-run that finds code raises both as `⊕ new` (§ 2b, § 2a). A pair an earlier bootstrap placed on a docs-only repo stays as the consumer left it — the walk carries no removal path.

### Quick Structure

- `ls` root directory
- Check for: `docs/`, `README.md`, `CLAUDE.md`, `.claude/`, monorepo indicators
- Note existing doc structure (don't read docs deeply yet)

### Monorepo detection

Check the repo root for a **workspace manifest** — the marker that one root hosts multiple packages (e.g. `pnpm-workspace.yaml`, `turbo.json`, `nx.json`, `lerna.json`, a `package.json` carrying a `"workspaces"` field, `Cargo.toml` with a `[workspace]` table — illustrative, judge by analogy). Present → set **monorepo tier**.

On monorepo tier, enumerate packages from the workspace globs (`apps/*`, `packages/*`, etc. — read the actual globs from the manifest, don't assume the layout). Each resolved directory with its own manifest is a package; record `{ name, path, role, build command }` per package for the Phase 2b `techstack.md` § Packages table rows (§ 2b) and the CLAUDE.md monorepo block.

Rule-signal detection (below) then fans out per package — one path-scoped rule carries the whole boundary, no nested CLAUDE.md needed.

No workspace manifest → single-package repo; skip, everything stays root-scoped.

### Existing CLAUDE.md

If it exists, read it. The pipeline may already be partially or fully present — note what's already there. **Also note legacy-skeleton blocks** (Coding Standards code-block walls, framework-specific patterns under pipeline-owned headings, large Project Structure trees) — these become migration candidates, routed by the Phase 2b migration table.

### Rule-signal detection

Phase 1 also flags which `.claude/rules/*.md` files Phase 2b should seed. Signals (illustrative — judge by analogy):

- **Frontend component dir** detected (e.g. `src/components/`, `src/pages/`, `app/`, `components/`) + framework manifest (React / Vue / Svelte / Angular / Solid) → seed `rules/<framework>.md` from `assets/rules-frontend-skeleton.md`.
- **Chrome MV3 manifest** (`manifest.json` with `"manifest_version": 3` + `service_worker` field) OR `src/background/` dir → seed `rules/mv3.md` from `assets/rules-mv3-skeleton.md`.
- **Migrations dir** (`migrations/`, `db/migrate/`, `prisma/migrations/`) → flag `rules/migrations.md` for body-fill via doc-sync (machinery-only seed at scaffold).
- **Tests dir** with non-trivial structure (`tests/`, `__tests__/`, `*.test.*` patterns) → flag `rules/tests.md` for body-fill via doc-sync.

On **monorepo tier** (§ Monorepo detection), each signal is evaluated **per package**, not root-only, and a fired signal's seeded glob is package-scoped (`apps/*/src/components/**`) so one rule file spans every package that shares the pattern.

**ECC-first seed source for language-scoped rules.** Before scaffolding from local `assets/rules-*-skeleton.md`, check ECC (`gh api repos/affaan-m/everything-claude-code/contents/rules`) for a matching language/framework rule. If ECC ships one, propose seeding from ECC (with attribution comment + license note) — defer to specialists. Local skeletons are the fallback. Cross-cutting / project-specific rules (e.g. MV3, custom service-worker patterns) stay on local skeletons. Skeleton seeding only — a rule file § 2b's legacy migration writes carries the consumer's own content and takes no ECC check.

Adjacent stacks (Bun + Next, Deno + Fresh, Tauri + React, etc.) infer by analogy. Unknown stacks → skip rule-seeding for that signal; user can add later.

**Output of Phase 1:** A mental model of "what kind of project is this" — stack name, structure shape, maturity level, **which rule files to seed in Phase 2b**, **which legacy CLAUDE.md sections need migration**. NOT a deep analysis.

### Greenfield (no seed docs)

The generic runway runs on greenfield. If Phase 1 detects a docs-only repo (§ Code presence — no manifests + no source files) whose `docs/overview.md` / `docs/techstack.md` are also missing, scaffold normally and write `overview.md` / `techstack.md` as empty skeletons in Phase 2b. The entry `/super-bootstrap:setup` seeds GAP cards against those empty skeletons and surfaces the gate.

When `docs/overview.md` + `docs/techstack.md` already carry substantive content, manifest facts and existing content feed the Phase 2b skeletons normally.

### Rot signals (harnessed-but-stale)

Catches "harness installed but carries renamed-away literals" — re-run is the right entry, flag before Phase 2b churns through migrations.

Trigger: any pipeline-owned file (§ Pipeline-owned, minus the files § 2b's rot scan skips — one scope, so `rot_hits[]` agrees with what 2b re-greps) contains a literal listed as `old` in `assets/rename-map.md`. Whole-token match; one hit is enough.

When the trigger fires, surface ONCE up front (single message, not a redirect — re-run is the correct entry point):

```
Renamed-away literals detected in pipeline-owned files.
Phase 2b will propose migrations alongside the normal drift check.
Affected files: {list of files where rot was observed}.

Continue? (y / dry-run report only)
```

If user answers `dry-run`, walk Phases 1–2b without writing — render the sync report (per-section listing + rename-map migration rows) inline without persisting `.claude/bootstrap-sync-report.md`, then exit. Otherwise proceed normally; Phase 2b's rot scan (see § 2b) handles the actual migrations.

**Output of Phase 1 (rot lane):** record `rot_hits[]` — the affected-files list the trigger message renders. § 2b re-derives the full scan itself for its row-writing pass; the two agree by sharing one scope, not by sharing one grep.

### Version-staleness signal (harnessed-but-stale)

Rot signals catch renamed literals; they miss template drift that shifted structure without renaming a token. The runway receipt closes that gap.

Read `.claude/super-bootstrap-runway.json` in the target repo (the runway coverage receipt — Phase 1 reads `version` and `covered`, the list of row identities the last sync read-and-compared; `declined` / `placed` semantics: § 2c Receipt write). Compare its `version` to the running plugin's own version — read `version` from the plugin's `.claude-plugin/plugin.json`, located at the plugin root two directory levels above this skill's base directory (`skills/harness-bootstrap/` → `skills/` → plugin root). That is the version currently installing/syncing.

- **Marker stale (older) or absent** → set `version_stale`, consumed by Phase 2b to enforce the full drift check (see § 2b). Surface ONCE up front:
  - Stale: `runway stamped v{old} < plugin v{new} — full drift re-check enforced.`
  - Absent: `runway carries no version stamp — full drift re-check enforced.`
- **Marker matches plugin version** → judge the receipt: enumerate the pipeline-owned sections applicable to this repo (§ Pipeline-owned, honoring the tier conditionals — monorepo, scale module, code presence) and set-difference against `covered`. A legacy version-only stamp carries no `covered` — its coverage is unknown, so every applicable section counts as uncovered.
  - Difference empty → normal path.
  - Difference non-empty → set `version_stale` with the gap list. Surface ONCE up front: `runway stamped v{cur} but coverage gaps: {list} — full drift re-check enforced.`

Detection only — Phase 1 reads the receipt and stops; it does not act on the flag or alter its own scan. Phase 2c overwrites the receipt later, after sync completes.

**Output of Phase 1 (version lane):** record `version_stale` (plus the old/new version strings, and the coverage-gap list when that was the trigger) for Phase 2b to consume.

### Fact-staleness signal (detected facts vs last run)

The version lane asks whether the receipt is old. This lane asks whether the facts it was written against still hold. The receipt records what the last sync *saw*: `covered` omits `CLAUDE.md § Coding Principles` and `CODING_STANDARDS.md` on a docs-only run (§ Code presence), so a `covered` list carrying neither says the last sync ran against a repo with no code.

Set `facts_stale` when **both** hold:

- the receipt exists, its `covered` is present and non-empty, and `covered` carries neither `CLAUDE.md § Coding Principles` nor `CODING_STANDARDS.md`
- this run's § Code presence reads **code present**

Every other state leaves it unset: no receipt (fresh install — the facts seed this run), a legacy version-only stamp with no `covered` (coverage unknown, nothing to compare against), a docs-only repo still docs-only, or a repo whose last run already saw code.

**Bound.** The receipt records no manifest identity, so this delta keys on the code-presence transition alone. A manifest that changed, moved, or was added beside an existing one on a repo the last run already read as code-present raises nothing here.

Detected here, materialized at § 2b: the flag rides the sync report, not context. When set, § 2b's enumeration appends one `facts:` row to `.claude/bootstrap-sync-report.md` — `facts: stale — last sync docs-only, code present now · manifest {file} · runtime {runtime + version} · framework {framework, or "none"}` — beside the rot rows, and Phase 3 prints its advisory from that row alone (§ Phase 3). The receipt shape and the § 2c set-difference are unchanged: the row is a print source, not a coverage claim.

**Output of Phase 1 (facts lane):** record `facts_stale`, and with it the facts this run detected — manifest file name, runtime, framework (§ Manifest Detection) — for § 2b to write as the `facts:` row.

---

The runway scaffolds with no product Q&A. Drift on existing files is resolved inline per-section at Phase 2b.

---

## Phase 2: Scaffold / Sync

Walk each pipeline artifact in order: folders → pipeline docs → sync report + commit. Same flow on fresh and re-run repos — fresh just sees "all new" at every step.

**Per-artifact rule** (applied uniformly in 2a / 2b):
- Missing → write from template / curate fresh
- Exists, matches template → skip (`✓ current`)
- Exists, drifted from template → show diff, get approval per change, then write
- Exists, pipeline-owned section absent → `⊕ new` — show the template section, get approval, insert
- Project-owned content → never touch, even on drift

**Registration rule** (2a / 2a-scale / 2b plantings, 2a-scale / 2b-adopt deletions): a durable artifact this run places for the first time or deletes earns its own sync-report row — status `⊕ new` for a planting, `⊘ removed` for a deletion:

```
registration: {artifact} → {surfaces, or none}
```

`{surfaces}` names the consumer-authored surfaces that enumerate the artifact's class — a table or list carrying one entry per member (a glob that already covers the artifact needs no edit and is not a surface; a curated shortlist of a few files is not an enumeration). Grep each of four places for the artifact's path and for its parent directory string (`docs/`, `.claude/skills/`), and name every place whose hit is such a list:

1. `.claude/rules/*.md` `paths:` frontmatter entries that name paths literally
2. root `README.md` — any table or list naming `docs/` paths
3. `docs/**/README.md` and `docs/overview.md` § Module Index
4. `.claude/rules/*.md` bodies — any table or list naming `docs/` paths (ownership / routing); `CLAUDE.md`'s pipeline-owned sections are the plugin's own registration and stay out of this search

The row resolves `updated` once every named surface is edited, before § 2c runs, in the same commit — or `none`, earned only when all four greps return nothing. An unresolved row halts § 2c like a drifted one. The 2a-hooks and 2a-autorun steps sit outside this rule, scripts included: the `.claude/settings.json` and `.gitignore` entries those steps already write are their registration.

**Pipeline-owned** (subject to drift check):
- CLAUDE.md sections: Development Workflow, Dispatch, Doc Sync, Coding Principles (code present only — Phase 1 § Code presence), Edit Discipline, Context Hygiene, Finding Triage, Rules, Git Notes, Planning, Monorepo (monorepo tier only — the conditional cross-package build block)
- `docs/techstack.md` skeleton sections: Runtime, Framework, Key Dependencies, Build & Distribution (**seed-once** — mechanics at § 2b; stale facts route to the Phase 3 advisory, § Fact-staleness signal), Edit Discipline (fixed prose — body drift-checked against the template), Packages (monorepo tier only — the § header + column shape; table rows are consumer-grown, project-owned)
- `docs/overview.md` skeleton sections: Problem, User, Current State; the `<!-- harness-meta -->` block — row identity `docs/overview.md harness-meta` (a marker block is not a heading — no `§`, the same spelling the fact-fields block takes) — compared **shape only**: marker comment present + `external-tools:` key present → `✓ current`, whatever the list holds (values are consumer-owned — § 2b asset table; the same rule the seed-once sections take at § 2b Per-doc handling)
- `docs/decisions.md` scope header (the blockquote + `## Closed Forks` heading)
- `CODING_STANDARDS.md` preamble + section headings (code present only; drift checked against `assets/coding-standards-skeleton.md`)
- `docs/work/README.md`, `docs/work/TEMPLATE.md` — the `**ID high-water mark:**` line (here, and in the scale module's `docs/outward/README.md` + `docs/parked.md`) compared **shape only**: line present in its skeleton position → `✓ matches`, whatever IDs it carries (values are consumer-owned, the way `harness-meta`'s are) — never a drift row, never an offer to reset the counter
- `AGENTS.md` (foreign-executor contract — always placed; whole shipped body drift-checked against `assets/agents-md-skeleton.md`)
- `.claude/rules/index.md` (rule-authoring guide)
- `.claude/rules/<seeded>.md` skeleton bodies (drift checked against `assets/rules-*-skeleton.md`)
- `.claude/settings.json` core plugin pin (`enabledPlugins`, `extraKnownMarketplaces`) — drift-checked for presence alone (§ 2a)
- `.claude/super-bootstrap-runway.json` (runway coverage receipt — not diffed section-by-section; read at Phase 1 § Version-staleness signal, written at § 2c Receipt write; durable, no cleaner)
- Scale module — checked only when installed (detected by `docs/parked.md` presence): `docs/parked.md` + `docs/test-queue.md` header/shape sections, `docs/outward/README.md` + `docs/outward/TEMPLATE.md` (whole files, the way `docs/work/README.md` / `docs/work/TEMPLATE.md` are — high-water line shape only, above), the `docs/work/README.md` fact-fields marker block (`<!-- scale-module: fact fields -->` … `<!-- /scale-module -->`)

**Project-owned** (never touched):
- CLAUDE.md: Tech Stack one-line (**seed-once**, same classification as the `docs/techstack.md` fact sections above — filled from Phase 1 detection facts when the runway first writes CLAUDE.md — the skeleton placeholder kept verbatim on a docs-only repo (§ 2b Placeholders) — consumer-edited from then on; no re-run rewrites it), Commands, any user-added custom sections
- `docs/techstack.md` grown sections: Architecture Rules, Coding Patterns
- `docs/overview.md` grown sections: Module Index, Data Flow, Key Boundaries
- `docs/decisions.md` § Closed Forks table rows (consumer-filled history)
- `CODING_STANDARDS.md` section content (consumer-authored by hand when a convention settles — the file sits outside the doc-sync surface)
- `AGENTS.md` grown content (additions appended below the shipped sections)
- `.claude/rules/<rule>.md` grown sections (additions the user/doc-sync added below the skeleton scaffold)
- `.claude/rules/<rule>.md` files the user authored without a matching skeleton (treat as fully project-owned)
- Scale-module container content — `docs/parked.md` `## Entries` + `## Sweep log` content, `docs/test-queue.md` `## Pending` / `## Failed (re-queued for fix)` rows, the `docs/outward/OUT-###.md` entry files (consumer-filled, like card content; only the skeleton headers/shape stay pipeline-owned)
- Other settings in `.claude/settings.json` outside the plugin-pin keys

### 2a: Folders & core plugin pin

Folders + the core plugin pin don't drift — only two states: missing or present.

**Migrate before creating — `docs/superpowers/` → `docs/work/`.** Repos bootstrapped
before the rename hold their temporal specs and plans under `docs/superpowers/`. Creating
`docs/work/` beside it would strand that work: every scan below — `/super-bootstrap:needs-me`,
`/super-bootstrap:autorun` — reads the new path only, so the old tree goes invisible
while still sitting in the repo. When `docs/superpowers/` exists, `git mv` it to
`docs/work/` first, then continue. If both exist, move the old tree's contents in
directory by directory and leave anything that would overwrite a file already at the
destination — report those paths rather than resolving them.

**Always created (fixed macro):**
```
docs/
  decisions.md   ← closed forks / rejected directions (history dimension — always scaffolded, starts empty)
  specs/         ← feature specs, one .md per feature, no index file (empty + .gitkeep; files land at the spec-seeding card's pickup — `/super-bootstrap:setup` seeds it on a code-present repo)
  work/
    README.md    ← work-unit workspace header: contract, categories, ID high-water line
    TEMPLATE.md  ← copy-to-create card template
.claude/
  rules/         ← path-scoped rules, full-body fires on file match
    index.md     ← rule-authoring guide (path-scoped — loads when editing rules)
```

For each: create if missing, skip if present. Add `.gitkeep` in empty folders. If `docs/` or `.claude/` already exists, nest alongside. Report status per directory.

**Code present only** (Phase 1 § Code presence — scaffold rule below):
```
CODING_STANDARDS.md ← repo binding conventions (headings-only scaffold; sections hand-recorded as conventions settle)
```

`docs/decisions.md` is **always** scaffolded — copy `assets/decisions-skeleton.md` to `docs/decisions.md` if missing (no substitutions). Starts empty (header + `## Closed Forks` table).

Copy `assets/work-readme-skeleton.md` to `docs/work/README.md` if missing (no substitutions). Copy `assets/work-template-skeleton.md` to `docs/work/TEMPLATE.md` if missing (no substitutions).

`AGENTS.md` is **always** scaffolded — copy `assets/agents-md-skeleton.md` to the repo root if missing (no substitutions). No code-presence gate: the build contract it carries binds a docs-only repo the same way.

`CODING_STANDARDS.md` is scaffolded **when code is present** (Phase 1 § Code presence) — copy `assets/coding-standards-skeleton.md` to the repo root if missing (no substitutions); a docs-only repo takes no file, and a later re-run that finds code raises it as `⊕ new`. Starts headings-only; its preamble states the fill contract and the three-way routing (binding + ambient here, binding + path-scoped → `.claude/rules/<scope>.md`, descriptive → `docs/techstack.md` § Coding Patterns).

`.claude/rules/` machinery is **always** scaffolded (zero-cost when empty). `index.md` is seeded from `assets/rules-index-skeleton.md`. Individual rule bodies fill in Phase 2b based on Phase 1 signal detection.

**Core plugin pin (pre-resolve).** A core dep, not an adaptive pick: the skeleton routes every door through `/super-bootstrap:*` and the committed `commit-channel.sh` deny text routes workers to `/super-bootstrap:commit`, so both dangle unless the project pin alone resolves `super-bootstrap` wherever user-scope settings don't apply (fresh clone, second machine). A cloud session is the exception the pin cannot cover — it loads no repo-declared plugin. The pin lives outside the official marketplace, so its `extraKnownMarketplaces` entry is required. Pin first — tier-2 curation layers adaptive picks on top later.

Ensure `.claude/settings.json` contains:

```json
{
  "enabledPlugins": {
    "super-bootstrap@super-bootstrap": true
  },
  "extraKnownMarketplaces": {
    "super-bootstrap": {
      "source": { "source": "github", "repo": "RockyHong/super-bootstrap" }
    }
  }
}
```

- File missing → create with this minimal shape.
- Key already present → skip (`✓ pinned`), whatever its value.
- Core-pin key absent → merge it in.
- Other `.claude/settings.json` content → never touched.

### 2a-hooks: Harness hooks (default-on)

Three hook assets ship as frozen files and install **unconditionally** — no
opt-in confirm (rationale + full procedure:
[`assets/hooks-ensure-infra.md`](assets/hooks-ensure-infra.md)).

| # | Asset | Fires on | Effect |
| - | - | - | - |
| 1 | `commit-channel` (PreToolUse) | `Bash(git *)` and `PowerShell(git *)` — one hook element per command tool, each a bare-command pre-filter; the script narrows to real `git commit` | Deny raw `git commit` from worker subagents — deny text routes the worker back to `/super-bootstrap:commit`; main session and separate-process workers pass |
| 2 | `consult-check-sessionstart` (SessionStart) | `startup\|resume\|clear\|compact` | Derives the compact `docs/**` catalog into the gitignored `.claude/.consult-catalog` cache, once per session boundary |
| 3 | `consult-check-check` (UserPromptSubmit) | every prompt | Injects the catalog + a forced relevance evaluation (judge which docs bear on the prompt, Read each that does; no stated verdict) — the read boundary's activation layer: the right project docs get read at the prompt moment (pure cache read; installs as a pair with #2) |

Execute the procedure in [`assets/hooks-ensure-infra.md`](assets/hooks-ensure-infra.md); stage the placed files with the Phase 2c commit.

**Report rows.** Each check writes one row to `.claude/bootstrap-sync-report.md` — `✓ current` included — its verdict → resolution as the procedure words it; an absent snippet or `.gitignore` line takes `⊕ new → seeded`, a replaced snippet `⚠ drifted → updated`:

- one row per script, identity its destination path — `.claude/hooks/commit-channel.sh`, `.claude/hooks/consult-check-sessionstart.sh`, `.claude/hooks/consult-check-check.sh`
- one combined row for the three settings snippets — `.claude/settings.json hook snippets`, verdict the most-changed across them (`⚠ drifted` over `⊕ new` over `✓ current`)
- one row for the `.gitignore` line — `.gitignore consult-catalog line`

§ 2c transcodes these rows into `covered` like whole-file rows; they sit outside the § 2c gate's required coverage set.

### 2a-autorun: Autorun infra (opt-in, earn-gated)

`/super-bootstrap:autorun` (unattended worktree runs) needs three committed infra pieces. Most active-dev repos use it; skill / plugin / docs-only repos usually don't. Earn-gated on code: a docs-only repo (Phase 1 § Code presence) skips silently, places nothing, and adds no sync-report row — the way § 2a-scale skips; autorun self-installs on first use, and a later re-run that finds code asks. Code present → ask once:

> Install `/super-bootstrap:autorun` worktree infra? — worktree settings template + `PreToolUse(Read)` guard + `.claude/worktrees/` gitignore. Most dev repos: yes. Skill / plugin / docs repos: skip (autorun self-installs on first use anyway).
> Install now? (y / skip)

Infra present and current (the asset's `infraPresent()` — all four pieces) → no ask; run the procedure below to write its rows, all `✓ current`. Any piece absent or stale → ask as above.

On `y`: execute the procedure in [`../autorun/assets/ensure-infra.md`](../autorun/assets/ensure-infra.md) — the same idempotent three-piece install autorun self-runs on first invocation; this `y` stands in for its install confirm. Stage the placed files with the Phase 2c commit. Report rows as § 2a-hooks writes them — every check, `✓ current` included, where the asset's "pass silently" means no prompt — outside the § 2c gate's required coverage set; row identities: `.claude/templates/worktree-settings.local.json` (the template), `.claude/settings.json worktree guard` (the Read guard, one combined row), `.gitignore worktrees + autorun-status lines` (both lines, one row). A repo that carries the retired `.drain-status` ignore line keeps it — harmless — and gains the `.autorun-status` line.

On `skip`: nothing placed; autorun's own § Pre-flight step 1 installs on first `/super-bootstrap:autorun`.

### 2a-scale: Scale module (opt-in, earn-gated)

The scale module adds work-substrate-adjacent runway — a parked-items artifact, a manual-verification queue, and an outward folder (one thread file per item the author or an outside party moves, the repo owning only the result tail) — for repos whose card set has outgrown simple scanning. Earn-gated: offer only when a signal shows the repo has grown into it, silent skip otherwise (no prompt spam on small repos).

Signals — any one arms the offer:
- Card files (`{BUG|DEBT|GAP}-###.md`) in `docs/work/` ≥ 10.
- Autorun worktree infra installed (`.claude/worktrees/` gitignore present).
- User asked for it.

None hold → skip the offer silently, place nothing. Already installed (`docs/parked.md` present) → no offer either; § 2b's drift check owns the members, a missing one resolving `Missing → write`.

**Split before placing — `docs/outward.md` → `docs/outward/`.** Repos that took the scale module before the folder shape hold every outward item as an `### OUT-###` chunk in one flat file. Placing `docs/outward/` beside it strands those entries: `/super-bootstrap:log`'s dedup and the mover gate read the folder, and the board only carries the flat file on a legacy branch that draws a `# note:` every render. When `docs/outward.md` exists — keyed on that file alone, whatever the signals or install state — run the split first, then continue with this step's placements:

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/harness-bootstrap/assets/scale/split-outward.py <repo root> ${CLAUDE_PLUGIN_ROOT}/skills/harness-bootstrap/assets/scale/outward-readme-skeleton.md
```

Deterministic, no per-item judgment (output shape: the script's docstring). It refuses (exit 2, nothing written) when any target file — `docs/outward/README.md` or an `OUT-###.md` it would create — already exists: the two shapes then coexist, so stop this sub-step — surface the flat file's entry list beside the folder's for the user to reconcile, write no split registration rows, and continue the sync; never treat exit 2 as a converted repo. A repo with no `docs/outward.md` is already on the folder shape and the placements below resolve `✓ current`. The split writes `docs/outward/README.md` from template, so its row takes `⊕ new`, resolution `seeded`, and neither the placement below nor § 2b's walk re-verdicts it this run. The split moves a durable artifact, so it earns two § Registration rule rows — `registration: docs/outward.md → {surfaces}` (`⊘ removed`) and `registration: docs/outward/ → {surfaces}` (`⊕ new`), folder-grain, not one per `OUT-###.md` — and every consumer surface naming the flat path re-points to `docs/outward/README.md`, `CLAUDE.md` § Planning's bracket line included (pipeline-owned; § 2b's drift check carries that one).

When armed, ask once:

> Install the scale module? — `docs/parked.md` (deferred items with named triggers) + `docs/test-queue.md` (manual-verification queue) + `docs/outward/` (outward threads — next move + waiting-on party, one file per item) + card fact-field guidance.
> Install now? (y / skip)

On `y`, place the five `assets/scale/` skeletons per Phase 2's per-artifact rule (all copy verbatim — no substitutions):
- `parked-skeleton.md` → `docs/parked.md`
- `test-queue-skeleton.md` → `docs/test-queue.md`
- `outward-readme-skeleton.md` → `docs/outward/README.md`
- `outward-template-skeleton.md` → `docs/outward/TEMPLATE.md`
- `card-fact-fields.md` → insert its marker-delimited block (`<!-- scale-module: fact fields -->` … `<!-- /scale-module -->`) into `docs/work/README.md` directly above the `## Thread contract` heading. Markers already present → the block is placed; § 2b's drift check judges its content against the asset (§ Pipeline-owned), so a re-run updates a stale block there, on approval.

Stage the placed files with the Phase 2c commit. A placed `.claude/rules/venue-map.md` from an earlier module version is retired: propose its deletion as a `⊘ removed` registration row and drop its CLAUDE.md § Rules bullet in the same run.

On `skip`: nothing placed; a re-run re-offers while a signal holds.

### 2b: Pipeline docs

Walk each pipeline doc and apply the per-artifact rule. Sources:

| Asset | Destination | Notes |
|---|---|---|
| `assets/claude-md-skeleton.md` | `CLAUDE.md` (project root) | Includes Rules summary section — fill bullets from seeded rule files |
| `assets/techstack-skeleton.md` | `docs/techstack.md` | Grown sections absorb migrated CLAUDE.md state-dimension content (Architecture Rules: still-binding decisions; Coding Patterns: examples) |
| `assets/overview-skeleton.md` | `docs/overview.md` | `<!-- harness-meta -->` block at top: seed `external-tools:` as a YAML list defaulting to `[github]`. Read by `/super-bootstrap:resolve-plugins` (tier-2 curation) as the external-tools source. |
| `assets/decisions-skeleton.md` | `docs/decisions.md` | Always |
| `assets/work-readme-skeleton.md` | `docs/work/README.md` | Always — categories, thread contract, ID high-water line |
| `assets/work-template-skeleton.md` | `docs/work/TEMPLATE.md` | Always — copy-to-create card template |
| `assets/coding-standards-skeleton.md` | `CODING_STANDARDS.md` (project root) | Code present only (Phase 1 § Code presence) |
| `assets/agents-md-skeleton.md` | `AGENTS.md` (project root) | Always — foreign-executor contract |
| `assets/rules-index-skeleton.md` | `.claude/rules/index.md` | Always — machinery |
| `assets/rules-frontend-skeleton.md` | `.claude/rules/<framework>.md` | Only if frontend signal fired in Phase 1 |
| `assets/rules-mv3-skeleton.md` | `.claude/rules/mv3.md` | Only if MV3 signal fired in Phase 1 |

**Per-doc handling:**

- **Missing** → fill placeholders, write.
- **Exists, drifted in pipeline-owned section** → diff that section vs template, present to user, get approval per section, write approved.
- **Exists, pipeline-owned section absent** → `⊕ new` row: render the template section at Block 2, get approval, insert at the skeleton-defined position relative to the surviving sections.
- **Exists, seed-once section** (`docs/techstack.md` § Runtime / Framework / Key Dependencies / Build & Distribution — § Pipeline-owned) → compare **shape only**: heading present and in its skeleton position → `✓ current`, whatever facts the body carries. Heading missing → `⊕ new` per the bullet above, inserted with this run's detected facts filled in where code is present (the template's placeholder body on a docs-only repo — § Placeholders' docs-only rule, shared with CLAUDE.md § Tech Stack / § Commands) — that insertion is the section's first fill. The body is never diffed against the template here: a filled body and a still-unfilled placeholder both read `✓ current`, and facts that went stale route to the Phase 3 stale-facts advisory (§ Phase 3), never to a write in this walk.
- **`.claude/settings.json` core plugin pin** → key present → `✓ pinned`; key absent → `⊕ new`, resolving `inserted` with no prompt (§ 2a).
- **Exists, current** → mark `✓ current`. **Still show the per-section comparison briefly** (one-line per pipeline-owned section: `[Runtime] ✓ matches`, `[Framework] ✓ matches`, etc.) — asserting "current" without showing the comparison is a gap.
- **Project-owned content** → never touched, even on drift.
- **Legacy / unrecognized format** — if existing doc structure doesn't align with template sections (different headings, merged sections, doc was written by an older version of this skill or by hand) → surface as **legacy format detected**, propose: `(a) rewrite to current skeleton format (preserves grown sections), (b) leave as-is and accept template drift, (c) show full template-vs-current diff`. **Do not silently skip drift detection** because section names don't match — that hides real drift.

**Legacy CLAUDE.md migration (re-run on already-installed repos):**

Older super-bootstrap skeletons baked content into CLAUDE.md that now belongs in `.claude/rules/` (path-scoped), `docs/techstack.md` grown sections (state reference), or `docs/decisions.md` (closed history). When Phase 1 flagged legacy blocks in pipeline-owned slots, propose per-section migration BEFORE running the normal drift check on those sections.

Migration patterns (illustrative — judge by content shape, not heading exact-match):

| Legacy CLAUDE.md content | Proposed destination | Reason |
|---|---|---|
| Enforcement rules with clear file-scope (component patterns, Tailwind tokens, async style, framework idioms) | `.claude/rules/<scope>.md` | Path-scoped — full body fires when matching file is read. **Cold-file alternative would silent-miss enforcement.** |
| Closed history — rejected alternatives, roads-not-taken, closed design rationale | `docs/decisions.md` § Closed Forks | History dimension — a state doc never holds it (same lane as § Rejected Alternatives retirement below). |
| Still-binding architecture decisions — module boundaries, data-flow direction, layering | `docs/techstack.md` § Architecture Rules (grown section) | State — a live constraint, written present-tense, stripped of when/why-decided. |
| Live reference — deep examples, pattern walkthroughs for browsing | `docs/techstack.md` § Coding Patterns (grown section) | On-demand reading, not enforcement. Safe to be cold. |
| Imperative coding convention with no clean file glob — binds every code touch (naming, error handling, testing posture) | `CODING_STANDARDS.md` § matching heading | Ambient standard — the CLAUDE.md § Coding Principles line is its guaranteed reader at every code touch. |
| MV3 / service-worker rules path-bound to `src/background/**` | `.claude/rules/mv3.md` | Path-scoped |
| `## Project Structure` directory tree | drop | `ls` / `tree` covers it; not load-bearing for any decision |
| Cross-cutting items inside a path-scoped list (storage-key constants, type-centralization across UI ↔ background, message-contract types) | keep in CLAUDE.md (no clean glob — every layer touches them) | Genuinely ambient |

A block named like reference but written as imperatives is enforcement — route it by the table's two imperative rows; an arguable glob defaults to the rule file (§ Principles, Default-to-rules).

Surface the migration plan as a single proposal. Format below pins shape — one row per legacy block, destination from the migration table above.

```
{path}: legacy content detected — propose migrations:

  [<legacy heading>: <area> (<role>, <scope>)]
    → <destination>
    Reason: <one line tying content shape to destination choice>

  ... (one row per legacy block)

Apply migrations? (y / n / select-per-section)
```

Concrete fill-in (one example, not a template — judge by analogy for the actual repo; here no Phase 1 signal seeded the component glob):

```
  [Coding Standards: Components/Tailwind (enforcement, frontend-scoped)]
    → .claude/rules/components.md
    Reason: imperatives — path-scoped fires on component reads, cold-file would silent-miss.
```

Per-migration handling:
- **User approves** → write content into destination with proper format conversion (rule files get `paths:` frontmatter; techstack grown sections get conventional headings; `docs/decisions.md` gets one `Domain | Rejected direction | Because | Ref` row per closed fork — same conversion as § Rejected Alternatives retirement below). Remove from CLAUDE.md. Add summary bullet to CLAUDE.md § Rules for any rule-file destination.
- **Rule-file destination** — content on a glob a Phase 1 signal seeded lands in that seeded `rules/<framework>.md` (content matching a skeleton heading fills that slot; the rest goes below the scaffold as grown content); a new `rules/<scope>.md` only for a scope no signal seeded. The destination takes its class's report row, no migration-specific verb: a signal-seeded file new this run → `⊕ new | seeded`; an existing rule file → none for the grown content; a migration-only file (no matching skeleton — the `components.md` case) is project-owned → no section row, not even `⊕ new`. A rule file this migration places for the first time earns its own `registration:` row (§ Registration rule — the § Rules bullet does not satisfy it).
- **User rejects** → leave content in CLAUDE.md, mark section project-owned for future runs (no further drift attempts on that section).
- **User selects per-section** → walk one at a time.

**Never destructive without confirmation.** Show source → dest mapping, get explicit approval, only then move content.

**The drift check is produce-then-judge — enumerate first, read the verdict off the rows.** The per-section enumeration is the *first* output, written to the sync-report artifact `.claude/bootstrap-sync-report.md` before any "current / drifted" conclusion exists. Per pipeline-owned file in scope, append one row per applicable § Pipeline-owned section: section name, line range in the existing file, verdict (`✓ matches` / `⚠ drifted` / `⊕ new` / `⊘ missing`), and — for drifted, `⊕ new`, and `⊘ missing` rows — the diff or template section, plus the resolution as it lands at Block 2 (`updated` / `inserted` / `declined ({reason})`); Phase 2c derives the coverage receipt from these rows. The verdict is a column filled while enumerating, never a headline asserted over the file: there is no "all current" to state until every row is written. For each artifact this run placed for the first time or deleted (§ Registration rule), append its `registration:` row before closing the enumeration. Overwrite any stale report from a prior run.

**Version-stale enforcement.** When Phase 1 set `version_stale`, this enumeration is mandatory in full this run — every pipeline-owned section gets an actual read-and-compare row; the "sections look similar → `✓ current`" skim is forbidden. No new mechanism — the 2c gate already refuses commit on any uncovered section (see § 2c). Print the Phase 1 surfaced line once at the top of Block 1 as the reminder.

Block 1 (shown to the user, rendered from the report — one row per pipeline-owned section in the file):

```
{file path} sync — per-section comparison:

  [{Section A}] ✓ matches template     (lines N–M)
  [{Section B}] ⚠ drifted               (see diff below)
  [{Section C}] ✓ matches template     (lines P–Q)
```

Block 2 (for `⚠ drifted` rows and for `⊕ new` rows whose section is absent from an *existing* file — one expansion per section; a section in a file this run wrote from template takes `⊕ new`, resolution `seeded`, no expansion):

```
{file path} sync — drift detected:

  [{Section Name}] section drifted from current template:
  ───────────────────────────────────────────────
  - {removed line}
  + {added line}
  ───────────────────────────────────────────────
  previously declined: {reason}

  Update? (y / n — {reason} / show full diff)
```

`⊕ new` expansion (section in the current skeleton, absent from the existing file):

```
{file path} sync — pipeline-owned section absent:

  [{Section Name}] in the current skeleton, missing here:
  ───────────────────────────────────────────────
  {template section body}
  ───────────────────────────────────────────────
  previously declined: {reason}

  Insert at the skeleton's position? (y / n — {reason})
```

The `previously declined:` line renders only when the prior receipt's `declined` carries the row's section — the whole line reads `previously declined: {reason}` from an object entry, `previously declined, no reason recorded` from a bare string; omit it otherwise. Display beside the diff: the row still takes its full read-and-compare and its own Block 2 answer. `n` takes its reason on the same line — `n — {reason}`, one line — and the report row records it as `declined ({reason})`; a bare `n` re-prompts for the reason before the row resolves.

The report is the forcing function: Phase 2c refuses to commit unless it exists and carries a row for every pipeline-owned section in scope (§ 2c gate). A collapsed "skeleton sections match" with no rows fails that gate mechanically — there is no assertion to trust, so there is nothing to collapse into one. Drift approval (Block 2) protects against (a) legit template updates the user wants to review and (b) bad-actor template injection on a future re-run — you see what's about to change before it's overwritten.

**Facts row (re-run, when Phase 1 set `facts_stale`).** Append the `facts:` row § Fact-staleness signal specifies to the report in this same enumeration — Phase 3's only source for the stale-facts advisory: no row, no advisory.

**Bootstrap-shaped commit — match every spelling.** A re-run is told from a fresh install by a bootstrap-shaped commit in history. The emitted strings are §2c's; repos bootstrapped before the rename carry `chore: scaffold superpowers pipeline` / `chore: sync superpowers pipeline`, and `chore: complete pipeline bootstrap` counts too.

**Rot scan (mandatory pre-step on re-run; none on a fresh install).** A fresh install — no bootstrap-shaped commit yet — runs no scan and writes no rot outcome line. On re-run, before Block 1 renders, read `assets/rename-map.md` and grep every pipeline-owned file in scope for each entry's `old` literal (whole-token match — avoid URL / identifier false hits), skipping any file whose leading frontmatter declares `dimension: history` — frozen provenance preserves old literals by construction, so a hit there is undeclinable-once and re-fires every sync (the same predicate the commit door's doc-sync gate carries). The skip is this lane only: those files' pipeline-owned sections stay in the per-section drift check. One rot row covers one `old` literal in one file, listing every line it hits that § Scan guidance judged migratable, and is appended to `bootstrap-sync-report.md` and surfaced to the user. **State the swept set beside the row count** — how many `old` literals were read out of the map and how many files were swept. A scan that swept **zero literals** is an instrument failure, recorded as **no rot scan**, never as a clean: zero rot rows is also what a healthy repo produces, so the report line cannot tell the two apart unless it carries the swept set. The row shape:

```
{file path} — stale literal `{old}` → propose `{new}`
  Lines: {line}, {line}, …
  Reason: {map entry reason}
  previously declined: {reason}
```

The scan's own outcome line, beside the rows — one of these two forms, re-run only:

```
rot scan: {N} literals read, {M} files swept, {K} rows
rot scan: no rot scan — {N} literals read, {M} files swept
```

**One row, one answer, one identity.** The row's identity is `{file} § rot:{old}` — the literal as a bare token, no backticks — and the row takes a single answer covering all its lines, so that identity can never carry two outcomes at once. Grouping is safe — § Scan guidance already resolves the referent per line before a row exists. A second `old` form in the same file is its own row with its own identity: that section's "surface each independently" is about forms, not lines.

The line list is display only — the identity omits it (§ 2c `covered`); the `previously declined:` line then renders on the same rule Block 2 states, read against this row's identity in place of a section. The line is advisory: the row still takes its own read and its own answer.

Acceptance takes legacy migration's three-way shape — `y / n — {reason} / per-row` — and Block 2's reason-capture rule, which legacy migration has none of — same mechanic, read against this row. A rot row resolves `migrated` or `declined ({reason})` — § 2c gates and records it like every other row. Keep the two reasons apart: the row's `Reason:` is the rename-map entry's reason for the *entry*; the `declined ({reason})` reason is this consumer's reason for leaving *this* literal alone in *this* file.

The rot scan runs even when every per-section diff is `✓ current` — a stale slash command literal inside a current-shaped doc is invisible to per-section diff (template hasn't drifted; only the literal inside it has).

**README ID re-plant (re-run, if `docs/work/README.md` predates the ID high-water line).** Detect: `docs/work/README.md` exists and lacks the `**ID high-water mark:**` line. When detected, surface:

```
docs/work/README.md predates the ID high-water line — missing high-water mark.
Re-plant rebuilds the counter from git history.

Re-plant? (y / n / dry-run)
```

On `y`: rebuild the high-water mark from `git log --grep` over consumed IDs — **never from current card files** (resolved-but-deleted IDs stay consumed; re-deriving from live files collides). Then write the high-water line per the rule documented in `docs/work/README.md` § ID high-water mark (the rule's SSoT — don't restate the algorithm). Stage `docs/work/README.md` with the 2c commit.

**Special case — `docs/techstack.md` § Rejected Alternatives retirement (re-run).** Older skeletons grew a § Rejected Alternatives section inside `techstack.md` — state/history dimension pollution, and tech-scoped. It is retired in favor of `docs/decisions.md` (cross-domain history dimension). On re-run, if `techstack.md` carries a § Rejected Alternatives section with content, propose migrating it:

```
docs/techstack.md § Rejected Alternatives detected — retired section (dimension pollution).
Propose: move its entries to docs/decisions.md § Closed Forks (domain: tech), remove the section.

Migrate? (y / n / show entries)
```

On `y`: append each entry as a `tech`-domain row in `docs/decisions.md` (preserve the claim verbatim, add a commit-pointer Ref where one is obvious), then delete the section from `techstack.md`. On `n`: leave it, mark project-owned (no further drift attempts).

**Legacy plan migration — `.claude/bootstrap.md` (re-run).** Pending pipeline work is carried by `docs/work/` cards. A legacy checkbox plan — `.claude/bootstrap.md`, or `docs/work/bootstrap.md` at its pre-relocation path — converts to cards when either exists (both present → the `.claude/` copy's boxes decide; report the other path):

- **Task 1 (Seed feature specs) / Task 2 (Seed cards)** still holding an unchecked box → seed the matching card from [`../setup/assets/seed-cards.md`](../setup/assets/seed-cards.md) (Task 1 → `spec-seeding`, Task 2 → `marker-sweep`) by the hand-copy of [`/super-bootstrap:setup`](../setup/SKILL.md) § Greenfield branch, skipping a card that guard checks 1–2 of § Code-present seed hit. A task with every box checked seeds nothing — the plan's checkboxes are its record.
- **Task 3 (Cleanup)** carries no card; any other task still holding an unchecked box is named to the user for `/super-bootstrap:log`, not converted.
- **Delete** every legacy plan copy present (git keeps the prior text) and stage the deletion with the new cards and the `docs/work/README.md` high-water bump.
- **Row** — identity `.claude/bootstrap.md` (whole-file), `⊘ removed`, resolution `updated`; it enters `covered` and takes no `registration:` row (the plan is no durable artifact). No plan present → no row.

**Placeholders:**
- `{Project Name}` — repo name
- `{date}` — today's date
- Manifest detection facts (Runtime / Framework / Key Dependencies / Build & Distribution) → fill into CLAUDE.md Tech Stack one-liner AND `techstack.md` skeleton sections; detected scripts / Makefile / Cargo commands → fill CLAUDE.md § Commands
- **Docs-only repo** (Phase 1 § Code presence) — no facts to fill: `techstack.md`'s seed-once sections, CLAUDE.md's § Tech Stack one-liner (`{detected one-line summary…}`), and its § Commands block body (`{detected from scripts/Makefile/Cargo…}`) all keep the skeleton placeholder body verbatim — one rule for both docs
- Problem / User / Current State (`overview.md` skeleton sections) → keep the skeleton placeholder body verbatim at install, on every repo — the docs-only rule above, unconditioned; filled at GAP-card pickup, not by the runway
- Bracketed conditional lines (`{- docs/parked.md — ...}`, `{- docs/test-queue.md — ...}`, `{- docs/outward/ — ...}`) — keep only if the corresponding adaptive doc is scaffolded for this repo (scale module per its 2a install gate); drop the whole line otherwise
- **Monorepo tier** (Phase 1 § Monorepo detection) — fill CLAUDE.md's conditional monorepo block (workspace tool + the workspace-aware filtered build command) and `techstack.md` § Packages table rows (package | path | role | build command) from the Phase 1 package enumeration. Single-package repo → drop the CLAUDE.md monorepo block and the § Packages section entirely
- **Code presence** (Phase 1 § Code presence) — code present → unbracket CLAUDE.md's conditional § Coding Principles block verbatim; docs-only repo → drop the block entirely (`CODING_STANDARDS.md` is not scaffolded either, § 2a)
- CLAUDE.md § **Rules** summary bullets — fill from seeded `.claude/rules/*.md` files (one bullet per rule with glob + 2-4 one-line key points). The `{example scaffolding — …}` label and the bracketed example bullets under it go together: replaced by the seeded rules' bullets, or dropped when no signal-seeded rule file landed (`index.md` is always-placed machinery and takes no bullet) — leaving the explanatory paragraph and the unbracketed read-the-rule-file sentence, which is shipped prose.
- Rule skeleton placeholders (`{component path glob}`, `{Framework}`, body bullets in `assets/rules-*-skeleton.md`) → fill from Phase 1 detection. Lines that don't apply get dropped during scaffold.

### 2b-adopt: Superseded-fork adoption (migration, silent-skip)

Migration machinery for repos that **forked the harness before this plugin existed** — they carry their own copies of skills/agents the plugin now ships as root artifacts (a local `commit` / `merge` / `log` / `needs-me` / `autorun` skill + agent that the installed plugin supersedes). On re-run, offer to delete the superseded forks so the single root copy takes over.

**Superseded-artifact map — derived at runtime, never hardcoded.** Enumerate the plugin's own shipped skills and agents from the install: the plugin's `skills/<name>/` directory names + `agents/<name>.md` basenames, read at the plugin root two directory levels above this skill's base dir (same anchor as the Phase 1 receipt read). That listing IS the map.

**Collision detection.** In the consumer repo, scan `.claude/skills/<name>/` directories and `.claude/agents/<name>.md` files. A consumer artifact whose **name** matches a shipped skill/agent name is a superseded-fork candidate — the installed root copy supersedes it. Name-non-colliding consumer skills/agents are **project delta** — never touched, never listed, never surfaced. None collide → silent skip: place nothing, surface nothing.

When candidates exist, surface the full list with a per-deletion confirm — each row maps the consumer path to the root artifact that supersedes it:

```
Superseded harness forks detected — the installed plugin now ships these:

  .claude/skills/commit/   → superseded by the plugin's `commit` skill (/super-bootstrap:commit)
  .claude/agents/triage.md → superseded by the plugin's `triage` agent
  ... (one row per collision: consumer path → superseding root artifact)

Delete the forked copies? (y = all / n = none / per-item)
```

`per-item` walks one candidate at a time (`y` / `n` each). **Never auto-delete** — every deletion is an explicit confirm.

Per-candidate handling:
- **Approve** → remove the consumer copy (`git rm -r` the skill dir / `git rm` the agent file; plain delete + stage where the path is untracked). Stage the deletion with the Phase 2c commit.
- **Reject** → leave it in place; a later re-run re-offers.

### 2c: Sync report + commit

**Gate — the sync report must exist and cover every pipeline-owned section, plus every artifact the § Registration rule covers, before commit.** Read `.claude/bootstrap-sync-report.md` and cross-check its per-section rows against § Pipeline-owned: every pipeline-owned section that applies to a file in scope must have a row, and every durable artifact the § Registration rule covers must have a `registration:` row. Missing file, or any uncovered section or artifact → halt, return to 2b, produce the missing rows. A `⚠ drifted`, `⊕ new`, `⊘ missing`, or `⊘ removed` row must also carry its resolution (`updated` / `inserted` / `seeded` / `declined ({reason})`), a rot row its own (`migrated` / `declined ({reason})`), a `registration:` row its own (`updated` / `none`), a § 2a-hooks / § 2a-autorun row also `kept (fork)` — a fork kept at the overwrite/keep prompt, which stays out of `declined` (`updated (stale)` / `updated (fork, overwritten)` count as `updated`) — an unresolved row, or a `declined` row carrying no reason, halts the same way. A rot outcome line present and reading `no rot scan` halts too — the scan swept no literals, so its zero rows are not a clean; return to 2b, re-run the rot scan with a working literal list. A fresh install carries no rot line, and the gate reads none. This is a Read + set-difference check, not a self-attestation — a skipped drift check leaves no rows to find, so it cannot pass the gate.

**Sync report** — rendered from the artifact (the file is canonical; this table is its commit-time view). Always shown once the gate above passes, before the commit. A re-run renders the table below — drift fixes and current items. A fresh install renders one coverage line in the table's place — `{N} sections placed, all ⊕ new` — while the report file keeps its per-row verdicts (`⊕ new | seeded`); the table stays the re-run surface.

```
| Artifact                            | Status       | Action              |
|-------------------------------------|--------------|---------------------|
| CLAUDE.md: Doc Sync                 | ✓ current    | —                   |
| docs/techstack.md: Runtime          | ⚠ drifted    | updated (approved)  |
| CLAUDE.md: Dispatch                 | ⚠ drifted    | declined (wires the repo's own guideline paths) |
| .claude/rules/mv3.md                | ⊕ new        | seeded (signal: MV3 manifest) |
| registration: docs/outward/ → README.md docs list (illustrative — name what the greps hit) | ⊕ new | updated |
| registration: .claude/skills/commit/ → none | ⊘ removed | none |
```

**Receipt for that report** — its four section and whole-file rows transcoded to row identities, its two `registration:` rows report-only, no rot row in this one to carry:

```json
{
  "version": "{current plugin version}",
  "covered": [
    "CLAUDE.md § Doc Sync",
    "docs/techstack.md § Runtime",
    "CLAUDE.md § Dispatch",
    ".claude/rules/mv3.md"
  ],
  "declined": [
    { "section": "CLAUDE.md § Dispatch", "reason": "wires the repo's own guideline paths" }
  ],
  "placed": { ".claude/hooks/commit-channel.sh": "<sha256 of the file as placed>" }
}
```

**Receipt write.** Once the sync completes, write `.claude/super-bootstrap-runway.json` = `{ "version": "{current plugin version}", "covered": [...], "declined": [...], "placed": { ... } }` — fresh install writes it new, re-run overwrites whole. Take `version` from the plugin version Phase 1 already read for its staleness compare — § Version-staleness signal names the file and how to locate it. This runs even when every row is `✓ current` — the receipt records "synced at this version, these sections compared," independent of whether content changed.

**`covered`** is an array of bare row-identity strings — one string per sync-report row across all three row classes: its per-section rows, its whole-file artifact rows (the § 2a-hooks / § 2a-autorun rows included, identity as those steps name it), and its rot rows. Each identity is *transcoded* from its report row rather than copied verbatim: the report renders a section row `{file}: {Section}` and the identity is `{file} § {Section}`; a whole-file artifact is its repo-relative path alone; a rot row is `{file} § rot:{old}` — keyed by the stale literal, never the line, since line numbers shift between runs. `registration:` rows stay report-only.

**`declined`** is the rows resolved `declined` — a drift kept or an insert declined at Block 2, a rot row left alone at the § 2b rot scan — each written `{ "section": "<row identity>", "reason": "<the row's declined reason>" }`, carrying the row's own `covered` identity string and the parenthetical of `declined ({reason})` as the reason — so `declined` stays a subset of `covered`, and marks divergence accepted, not pending.

**`placed`** is the ensure-infra procedures' own record — `{ "<destination path>": "<sha256 of the file as placed>" }` — which 2a-hooks / 2a-autorun write into the receipt file directly as each file resolves current — copied, or already sha-equal (mechanisms: [`assets/hooks-ensure-infra.md`](assets/hooks-ensure-infra.md) § Idempotency · [`../autorun/assets/ensure-infra.md`](../autorun/assets/ensure-infra.md) § Idempotency). Read the receipt back from disk here, after those steps ran, and carry its `placed` map forward whole — never from the Phase 1 snapshot, which predates this run's copies.

If every row is `✓ current` and nothing changed on disk, report and skip the commit.

Otherwise use `/super-bootstrap:commit` to stage:
- `CLAUDE.md` (new, modified, or post-migration)
- `CODING_STANDARDS.md` (new, or approved preamble / heading drift fix)
- `AGENTS.md` (new, or approved drift fix)
- `docs/techstack.md` (new, skeleton-section drift or insert, or post-migration absorbed content)
- `docs/overview.md` (new, skeleton-section drift or insert)
- `docs/decisions.md` (new, scope-header drift, post-retirement migration from techstack, or closed-history rows from legacy CLAUDE.md migration)
- `.claude/settings.json` (core pin seeded at 2a; harness hooks merged at 2a-hooks; autorun's `PreToolUse(Read)` guard merged at 2a-autorun)
- `.claude/hooks/commit-channel.sh`, `.claude/hooks/consult-check-{sessionstart,check}.sh` (frozen hook scripts seeded at 2a-hooks — always, default-on)
- `.gitignore` (when any 2a step appended a line — 2a-hooks' `.claude/.consult-catalog`, 2a-autorun's `.claude/worktrees/` + `.autorun-status`; skip if every line was already present)
- `.claude/templates/worktree-settings.local.json` (autorun worktree settings template — only if placed or refreshed on drift this run at 2a-autorun)
- `.claude/rules/index.md` (always — at minimum machinery seed)
- `.claude/rules/<seeded>.md` (any rule files newly seeded or migrated to)
- `docs/work/README.md` (if newly written, re-planted, or fact-fields block inserted this run at 2a-scale)
- `docs/work/TEMPLATE.md` (if newly written)
- Legacy plan migration (§ 2b) — the deleted `.claude/bootstrap.md` / `docs/work/bootstrap.md`, the `docs/work/GAP-###.md` cards it seeded, and the `docs/work/README.md` high-water bump
- `docs/specs/.gitkeep`
- `docs/parked.md`, `docs/test-queue.md`, `docs/outward/README.md`, `docs/outward/TEMPLATE.md` (scale-module targets — only if installed this run at 2a-scale)
- `docs/outward/OUT-###.md` entry files plus the removed `docs/outward.md` (only when 2a-scale ran the split)
- `.claude/super-bootstrap-runway.json` (runway coverage receipt — written/overwritten every sync)
- Superseded-fork deletions (adopt mode, § 2b-adopt) — staged removals of approved consumer `.claude/skills/<name>/` dirs / `.claude/agents/<name>.md` files that root artifacts now supersede
- Consumer surfaces edited to register a placed or deleted artifact (§ Registration rule — skip when every registration row resolved `none`)
- Any other adaptive files / folders created

Commit message: `chore: scaffold harness pipeline` on fresh repos, `chore: sync harness pipeline` when only drift fixes shipped, `refactor: migrate CLAUDE.md to rules layer + sync pipeline` when re-run performed legacy migration. These strings double as the bootstrap-shaped-commit match (§ 2b).

**Clean the run artifact.** `bootstrap-sync-report.md` is a transient diagnostic — never staged. After the commit lands (or after reporting no-changes) and the Phase 3 handoff block has rendered, delete it: its consumer is this phase, so this phase is its cleaner. A report orphaned by a session that broke between 2b and here is overwritten by the next run's § 2b enumeration.

---

## Phase 3: Handoff

After committing (or reporting no changes needed), present results based on repo state:

**First-run (just scaffolded)** — render the block verbatim, no additions, before § 2c deletes the sync report; each `{If …}` line resolves to its quoted text or drops; the command literals stay untranslated:

```
**Generic runway installed.** CLAUDE.md drives workflow. Skeleton `docs/techstack.md` and `docs/overview.md` carry detected facts (empty on greenfield) — grown sections fill via doc-sync as features land. The core plugin pin (super-bootstrap) sits in `.claude/settings.json` — local sessions only; a cloud session loads no repo-declared plugin, so install it from the cloud environment's Setup script: https://github.com/RockyHong/super-bootstrap#cloud-sessions. Stack-matched skill / MCP / hook picks come when `/super-bootstrap:setup` runs gated tier-2 curation. Everything this run installed is in the scaffold commit — `git show --stat HEAD`.

{If product skeletons are empty (greenfield): "`docs/overview.md` / `docs/techstack.md` are empty skeletons — `/super-bootstrap:setup` seeds GAP cards for them and surfaces the resolve gate."}

{If any rule files were seeded: "Path-scoped rules seeded in `.claude/rules/` ({list seeded rules}). They auto-load on file match — full ammo at the decision moment, summary mirrored in CLAUDE.md § Rules. Add more rule files when path-scoped patterns emerge."}
```

**Re-run / sync pass** — assembled per run from the fragments below, not rendered verbatim:

> **Pipeline synced.** {N items updated, M already current.}{If a commit landed: " Its full file list: `git show --stat HEAD`."}{If migration performed: " Migrated {sections moved} from CLAUDE.md to {destinations} — `CLAUDE.md` now {old line count} → {new line count} lines."}{If rule files added: " Rules: +K seeded, summary updated in CLAUDE.md § Rules."}

**Stale detected facts (re-run, when `.claude/bootstrap-sync-report.md` carries a `facts:` row — written at § 2b from § Fact-staleness signal):**

Read the row back and print this block once, directly under the sync line, its facts taken from the row:

> **Detected stack facts are stale.** This repo carried no code at the last runway sync and carries code now. The runway seeds stack facts once, at first fill, and never rewrites them — five sections still read their docs-only values:
>
> - `CLAUDE.md` § Tech Stack — the one-line summary. Hand-edited: it is § Project-owned, and doc-sync's write boundary excludes `CLAUDE.md`, so no other door refreshes it.
> - `docs/techstack.md` § Runtime · § Framework · § Key Dependencies · § Build & Distribution
>
> Detected this run: manifest `{manifest file}` · runtime `{runtime + version}` · framework `{framework, or "none"}`.
>
> Edit those five sections by hand from those facts and commit them. This run changed nothing in them.

The advisory step completes when that block has printed with all five section names and the row's facts substituted in. It has no approval prompt and no on-disk effect — the runway writes none of the five.

## Principles

- **Layer by decision-moment** — every rule has a moment-of-need: ambient (CLAUDE.md, every turn) for workflow + always-true safety; path-scoped (`.claude/rules/`, fires on file match) for full-body precision when relevant; on-demand (`docs/techstack.md`, `docs/specs/`) for reference Claude reads when intent surfaces. Skills are for thinking modes / structured processes — **not** a rule-storage layer.
- **Precision per always-on byte** — every CLAUDE.md line answers "what decision does this sharpen, at what moment?" Length is downstream of that: a line-count target is a smoke alarm on bloat, not a cap. Every always-on line competes with the task's own reads for attention, so the orchestrator brief stays lean enough that opening file reads + workflow + the task itself stay high-signal.
- **Default-to-rules when ambiguous** — enforcement-shaped content (imperatives: must / never / always) goes to `.claude/rules/<scope>.md` even when the heading sounds like reference. Silent-miss in a cold file costs more than slight over-attach.
- **Subagent dispatch protects orchestrator focus** — verbose work (10+ file reads, noisy test runs, parallel-safe chunks, fresh-eye review) belongs in a subagent's clean window. Orchestrator's attention budget is too valuable to spend on tool churn.
- **Mandatory checks ride a forcing function, not prose** — a step the model is merely told to "always run" collapses into a confident assertion on re-runs where the surface looks done. Encode it produce-then-judge: enumerate to a file first, then gate the downstream phase on that file's coverage (a Read + set-difference, not a self-attestation). This skill applies it at the drift check (2b → 2c); new mandatory steps take the same shape.
