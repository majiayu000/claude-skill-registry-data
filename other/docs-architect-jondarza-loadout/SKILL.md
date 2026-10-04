---
name: docs-architect
description: Set up, migrate, and maintain a project's documentation for maximum AI context efficiency using Claude Code's native mechanisms. Builds a 2-layer system (`.claude/rules/*.md` for the AI + `docs/*.md` for humans) that cuts startup tokens 20-40% vs custom summary patterns. Triggers — "set up docs structure", "optimize docs for AI", "install .claude/rules", "migrate _lite to rules", "audit docs", "sync docs with code", "docs-architect", "estructura de documentacion".
---

# Docs Architect — AI-Optimized Documentation (v2)

Build and maintain documentation that rides on Claude Code's native loading mechanisms. Cuts AI token consumption by 20–40% versus the v1 custom-summary pattern while preserving all information and giving humans a clean reference.

## Core principle

Docs are a knowledge base. The AI receives only what is strictly necessary per task. v2 uses the official `.claude/rules/` mechanism with two loading modes:

- **Always-loaded rules** — frontmatter-less `.claude/rules/*.md` files load at session start alongside `CLAUDE.md`. Use for universally-needed content (business, stack, conventions, core architecture).
- **Path-scoped rules** — `.claude/rules/*.md` with `paths:` frontmatter auto-load **only** when Claude reads matching files. Zero startup token cost. Use for subsystem-specific rules (backend, frontend, api, database, testing).

Full human docs live in `docs/*.md` as the source of truth. `.claude/rules/*.md` are lean (≤40 lines, ≤12 bullets) distillations mirrored from the full docs.

## Architecture

```
./CLAUDE.md                            # <100 lines — hard NOs + pointer to rules
./.claude/rules/                       # AI-facing rules (flat, no subfolders)
  ├── business-context.md              # always-loaded
  ├── coding-rules.md                  # always-loaded
  ├── tech-stack.md                    # always-loaded
  ├── architecture.md                  # always-loaded
  ├── backend.md                       # path-scoped: backend/**
  ├── frontend.md                      # path-scoped: frontend/**
  ├── api.md                           # path-scoped: **/Controllers/**, **/routes/**
  ├── database.md                      # path-scoped: **/Entities/**, **/migrations/**
  └── testing.md                       # path-scoped: **/*.test.*, **/tests/**
./.claude/agents/doc-explorer.md       # research subagent (isolated context)
./.claude/commands/                    # /docs-audit, /docs-sync, /docs-migrate
./docs/                                # full human-readable reference
  ├── README.md                        # governance + index
  ├── architecture.md                  # full architecture doc
  ├── coding-rules.md                  # full conventions
  ├── tech-stack.md                    # full package catalog
  ├── api-contracts.md                 # full endpoint catalog
  ├── database-schema.md               # full table catalog
  ├── deployment.md                    # full dev/prod reference
  ├── roadmap.md                       # product phases, KPIs, decisions
  ├── backlog.md                       # story registry
  ├── bugs.md                          # bug registry
  ├── ideas.md                         # raw ideas inbox
  ├── stories/ bugs/ plans/            # individual item files
  └── research/                        # deep reference docs
```

---

## Modes

| Mode | Purpose | Primary reference to read |
|---|---|---|
| `/docs-architect` | Interactive — analyze, ask, build | Step 1, then files as needed per step |
| `/docs-architect init` | Full v2 setup on a new or clean project | [assets/CLAUDE.md.template](assets/CLAUDE.md.template) + [assets/docs-README.md.template](assets/docs-README.md.template) + [references/governance.md](references/governance.md) + [references/common-specs.md](references/common-specs.md) |
| `/docs-architect audit` | Audit structure + auto-fix offers | [references/audit-report.md](references/audit-report.md) |
| `/docs-architect sync` | Detect docs drift from code | none (uses git diff + `doc-explorer` subagent) |
| `/docs-architect migrate` | Convert v1 `_lite/` pattern to v2 `.claude/rules/` | [references/migration-v1-to-v2.md](references/migration-v1-to-v2.md) |
| `/docs-architect segment <file>` | Segment a large doc | [references/common-specs.md](references/common-specs.md) §Segmentation patterns |

For everything related to hooks, subagents, settings precedence, built-in commands, `claudeMdExcludes`, and `.claude/rules/` format details, read [references/claude-code-native.md](references/claude-code-native.md) on demand.

---

## Step 1: Analyze the project

Before creating or changing anything, understand the current state.

1. **Scan existing docs** — check if `docs/` exists, list files with line counts.
2. **Scan `.claude/rules/`** — check if the v2 layout is already in place.
3. **Check for legacy `_lite/`** — if `docs/_lite/*.summary.md` exists, this is a v1 project → recommend `/docs-architect migrate`.
4. **Read CLAUDE.md** — measure size (target <100 lines), look for stale `@docs/_lite/*` imports.
5. **Detect documentation language** — look for `Documentation language` in CLAUDE.md Conventions. If not declared, ask the user. All generated docs must use this language.
6. **Identify the stack** — backend, frontend, database, infra.
7. **Identify subtrees** — backend/, frontend/, src/api/, src/components/, etc. These drive which path-scoped rules to install.

```bash
for f in docs/*.md; do lines=$(wc -l < "$f" 2>/dev/null); echo "$lines $f"; done 2>/dev/null | sort -rn
wc -l CLAUDE.md 2>/dev/null
ls .claude/rules/ 2>/dev/null
ls docs/_lite/ 2>/dev/null
```

---

## Step 2: Create or optimize CLAUDE.md

**Hard limit: under 100 lines.** Copy from [assets/CLAUDE.md.template](assets/CLAUDE.md.template) and adapt. CLAUDE.md holds only:

- 1-2 line context
- Hard NOs (max 5 items — the single most destructive patterns for this project)
- Documentation language + code language declarations
- 1-2 universal conventions
- Process rules (branching, commits, CI)
- A pointer block explaining where context comes from (`.claude/rules/*.md` for AI, `docs/*.md` for humans)

Everything else belongs in `.claude/rules/`. No `@imports`. No tables of summaries. No tech stack details. No business context.

**Monorepo note**: if the project is a monorepo and ancestor `CLAUDE.md` files would load unnecessarily, add `claudeMdExcludes` to `.claude/settings.json`. See [references/claude-code-native.md](references/claude-code-native.md) §Monorepos.

---

## Step 3: Create docs/README.md

The **governance document** for the `docs/` folder. Copy from [assets/docs-README.md.template](assets/docs-README.md.template). Contains: folder structure tree, 2-layer usage guide (humans + AI), AI rules, update table, and index. Keep under 200 lines.

All governance rules come from [references/governance.md](references/governance.md):

- **Stories/bugs/plans tracking** — mandatory priority/severity, dual-update rule (registry + individual file)
- **File naming conventions** — `{NNNNN}-{slug}.{type}.md`
- **Documentation management** — no `.md` outside `docs/` (except CLAUDE.md, `.claude/rules/`, `.claude/agents/`, `.claude/commands/`), never mix languages
- **Dual-update rule** — when updating a `.claude/rules/*.md` that mirrors a `docs/*.md`, update the full doc in the same commit (and vice versa)
- **Ideas → Story pipeline** — raw ideas land in `ideas.md`, group via `/brainstorming`, promote to story + `backlog.md` entry
- **Research** — `research/` holds deep-reference docs consulted on-demand (no rule mirror)
- **Frontend workflow** (if applicable) — 3-step pipeline: product definition → design exploration → UX validation
- **Git and code safety** — all prohibitions (no autonomous migrations, no `git add .`, no `--force`, no `--no-verify`, no `--amend` without request)

---

## Step 4: Create full docs

Each full doc in `docs/*.md` is the source of truth. If a doc already exists, **read it first** and restructure — do NOT overwrite with a blank template.

### Full doc specs

Read the specific spec on-demand from `references/`:

**Individual specs (large docs)**: [architecture-spec.md](references/architecture-spec.md) (10 sections) · [coding-rules-spec.md](references/coding-rules-spec.md) (17) · [api-contracts-spec.md](references/api-contracts-spec.md) (10+5) · [database-schema-spec.md](references/database-schema-spec.md) (10+5)

**Common specs (one file)**: [common-specs.md](references/common-specs.md) — backlog, bugs, tech-stack, deployment, roadmap (never remove business content), dev-testing, plus segmentation patterns table.

**Research files** (`docs/research/<topic>.md`): free-form deep reference. One file per topic. No rule mirror. Consult before the work type it covers.

### Priority, severity, status

See [references/governance.md](references/governance.md) for priority/severity definitions (ASAP/Critical/High/Medium/Low) and status definitions per item type (Pending/Open/Draft → … → Completed/Resolved).

### Individual file templates

- [assets/story.md.template](assets/story.md.template) — created at `In progress`
- [assets/bug.md.template](assets/bug.md.template)
- [assets/plan.md.template](assets/plan.md.template)

---

## Step 5: Create `.claude/rules/` — the v2 core

`.claude/rules/*.md` replaces v1's `_lite/` entirely. Two loading modes.

### Decision table

| Rule applies… | Loading mode | Frontmatter |
|---|---|---|
| Every session, globally | always-loaded | none |
| Only when Claude touches a specific subtree | path-scoped | `paths:` with globs |
| On-demand reference only (humans or deep research) | not a rule | put in `docs/*.md` full file |

### Always-loaded rules (no frontmatter)

Install these four from `assets/rules/_always/*.md` (copied flat into `.claude/rules/`, no subfolder):

- [assets/rules/_always/business-context.md](assets/rules/_always/business-context.md) → `.claude/rules/business-context.md`
- [assets/rules/_always/coding-rules.md](assets/rules/_always/coding-rules.md) → `.claude/rules/coding-rules.md`
- [assets/rules/_always/tech-stack.md](assets/rules/_always/tech-stack.md) → `.claude/rules/tech-stack.md`
- [assets/rules/_always/architecture.md](assets/rules/_always/architecture.md) → `.claude/rules/architecture.md`

### Path-scoped rules (with `paths:` frontmatter)

Install the ones that match the project's subtrees. Ask the user which apply.

- [assets/rules/backend.md](assets/rules/backend.md) → `.claude/rules/backend.md`
- [assets/rules/frontend.md](assets/rules/frontend.md) → `.claude/rules/frontend.md`
- [assets/rules/api.md](assets/rules/api.md) → `.claude/rules/api.md`
- [assets/rules/database.md](assets/rules/database.md) → `.claude/rules/database.md`
- [assets/rules/testing.md](assets/rules/testing.md) → `.claude/rules/testing.md`

### Rules size limits

Each `.claude/rules/*.md` file: ≤40 lines, ≤12 bullets. Focus on constraints, decisions, and hard NOs. No narrative. Full narrative belongs in `docs/*.md`.

For exact `.claude/rules/` format details (globs, precedence, flat-folder rule), read [references/claude-code-native.md](references/claude-code-native.md) §`.claude/rules/`.

---

## Step 6: Install native `.claude/` artifacts

After rules, install the three Claude Code native artifacts that make the skill turn-key.

### Agent

Copy [assets/agents/doc-explorer.md](assets/agents/doc-explorer.md) → `.claude/agents/doc-explorer.md`. This subagent runs in isolated context (model: haiku) and handles doc audits, sync scans, and research without polluting the main session. Audit and sync modes delegate to it by default.

### Slash commands

Copy all three:

- [assets/commands/docs-audit.md](assets/commands/docs-audit.md) → `.claude/commands/docs-audit.md`
- [assets/commands/docs-sync.md](assets/commands/docs-sync.md) → `.claude/commands/docs-sync.md`
- [assets/commands/docs-migrate.md](assets/commands/docs-migrate.md) → `.claude/commands/docs-migrate.md`

Users invoke these as `/docs-audit`, `/docs-sync`, `/docs-migrate` — no need to remember skill mode syntax.

### Hook snippet (print-only)

**Never auto-merge** into `.claude/settings.json`. Print the contents of [assets/hooks/settings.snippet.json](assets/hooks/settings.snippet.json) to the user and say:

> Paste this `hooks` block into `.claude/settings.json` (merge with any existing hooks). The docs-architect skill does not modify settings.json.

The snippet adds:
- **SessionStart** hook: warns if CLAUDE.md >100 lines
- **PostToolUse** hook: flags presence of legacy `docs/_lite/` files after Write/Edit

For full hook event catalogue and JSON format, see [references/claude-code-native.md](references/claude-code-native.md) §Hooks.

---

## Step 7: Segment large files

Any `docs/*.md` file over **150 lines** should be segmented into subtopic files.

### Process

1. Read the full file.
2. Identify 3–6 logical topics.
3. Create `docs/<name>/` folder with one file per topic + `README.md` index.
4. **Keep the original file intact** — it remains the full reference.
5. Update the corresponding `.claude/rules/*.md` file only if the segmentation changed the underlying facts.

Templates, header format, and common segmentation patterns (which doc splits by what axis) live in [references/common-specs.md](references/common-specs.md) §Segmentation patterns.

**Sync rule**: the full doc is the source of truth. Never edit a segment without also editing the full doc.

---

## Step 8: Audit mode

When invoked with `/docs-architect audit`, delegate the file scan to `doc-explorer` subagent when possible, run all checks, then offer to auto-fix.

### Checks

1. CLAUDE.md over 100 lines → flag, propose trimming
2. CLAUDE.md containing `@docs/_lite/*` imports → stale v1 pattern, suggest `/docs-migrate`
3. CLAUDE.md missing `Documentation language` declaration → ask and add
4. Missing always-loaded `.claude/rules/*.md` files (business-context, coding-rules, tech-stack, architecture) → install from assets
5. `.claude/rules/*.md` files over 40 lines → flag, ask to trim
6. `.claude/rules/*.md` with `paths:` patterns matching zero files → dead scope, suggest removing or fixing the globs
7. Repo has backend/ or frontend/ or `**/Controllers/` but no matching path-scoped rule → missed token savings, offer to install from assets
8. Missing `.claude/agents/doc-explorer.md` when `docs/` has ≥10 files → install
9. Missing `/docs-audit`, `/docs-sync`, `/docs-migrate` slash commands → install from assets
10. Legacy `docs/_lite/*.summary.md` (not `.deprecated`) present → suggest `/docs-migrate`
11. `docs/*.md` files over 150 lines without segmentation → flag
12. Stories/bugs consistency: registry vs individual files (orphans, broken links, status mismatches)
13. `docs/README.md` missing or over 200 lines
14. Pending ideas in `ideas.md` ≥5 items → suggest grouping and promotion
15. Referenced `research/` files missing

See [references/audit-report.md](references/audit-report.md) for the output format.

### Auto-fix

After the report, offer to fix each issue. Group fixes by type and confirm before applying.

| Issue | Auto-fix action |
|---|---|
| Missing always-loaded rule | Copy from `assets/rules/_always/*.md` |
| Missing path-scoped rule (subtree detected) | Copy from `assets/rules/*.md` |
| Dead path pattern | Ask user to correct the glob or remove the rule |
| Rule >40 lines | Show top offenders, ask which bullets to cut |
| CLAUDE.md >100 lines | Identify offloadable content, propose moving it to `.claude/rules/` |
| Missing `docs/README.md` | Generate from template |
| Orphaned story/bug file | Add missing entry to registry |
| Registry points to missing file | Remove broken link |
| Status mismatch | Show both, ask which is correct, update the other |
| Legacy `_lite/` present | Offer to run `/docs-architect migrate` |
| Missing doc-explorer agent | Copy from assets |
| Missing slash commands | Copy from assets |

**Flow**: report → "Found X fixable issues. Fix all / fix individually / skip?" → apply selected fixes → re-run checks to confirm.

---

## Step 9: Sync mode

When invoked with `/docs-architect sync`, detect which docs and rules are out of date relative to code changes.

### Process

1. **Find the last commit that touched docs or rules**:
   ```bash
   git log --oneline --all -- docs/ .claude/rules/ | head -1
   ```

2. **Get all files changed since that commit**:
   ```bash
   git diff --name-only <last-docs-commit>..HEAD
   ```

3. **Delegate the mapping analysis to the `doc-explorer` subagent** if the change list is ≥20 files. Otherwise do it inline. Subagent runs in isolated context — its reads don't bloat the main session.

4. **Map changed code files to affected rules and full docs**:

| Changed files match | Update rule | Update full doc |
|---|---|---|
| `*.csproj`, `Directory.Packages.props`, `package.json`, `Cargo.toml`, `requirements.txt`, `go.mod` | `tech-stack.md` | `tech-stack.md` |
| `docker-compose*`, `Dockerfile*`, `.env*`, `web.config`, `nginx.conf` | (none — no rule mirror) | `deployment.md` |
| Controllers, routes, endpoints (`*Controller*`, `*Endpoint*`, `*Route*`) | `api.md` | `api-contracts.md` |
| Entity/model files, migrations (`*Migration*`, `*Entity*`, `*Model*`) | `database.md` | `database-schema.md` |
| Domain layer, patterns, middleware, interceptors | `architecture.md` | `architecture.md` |
| Naming conventions, validators, new patterns | `coding-rules.md` | `coding-rules.md` |
| Test files | `testing.md` | `coding-rules.md` (coverage section) |

5. **Output a sync report**:
```
## Docs Sync Report

Last docs update: <commit-hash> (<date>)
Code commits since: <count>

### Rules + docs needing update
- .claude/rules/tech-stack.md + docs/tech-stack.md — 3 package files changed (list)
- .claude/rules/api.md + docs/api-contracts.md — 2 controllers modified (list)
- docs/deployment.md (rule-less) — docker-compose.yml changed

### Current
- .claude/rules/architecture.md + docs/architecture.md ✓
- .claude/rules/coding-rules.md + docs/coding-rules.md ✓

### Action
Update affected files now? [yes / pick individually / skip]
```

6. **If user confirms**, read each affected rule + doc, read the changed code files, and apply the update. Dual update always — rule + full doc.

---

## Step 10: Migrate mode (v1 → v2)

When invoked with `/docs-architect migrate`, convert a v1 project (custom `_lite/` pattern) to v2 (`.claude/rules/`).

**Read [references/migration-v1-to-v2.md](references/migration-v1-to-v2.md) first.** It has the full mapping table, examples, and safety rules.

### Flow summary

1. Scan `docs/_lite/*.summary.md`, list files.
2. For each summary, propose a `.claude/rules/*.md` target (always-loaded vs path-scoped) based on the mapping table in the migration reference.
3. Show the full mapping to the user, ask for confirmation or edits.
4. Copy content into new `.claude/rules/*.md` files, adding `paths:` frontmatter where applicable, stripping `Source:` lines (replaced with `<!-- mirrors: docs/<file>.md -->`).
5. **Rename** originals to `docs/_lite/*.summary.md.deprecated`. Never delete.
6. Update `CLAUDE.md` to remove the old `_lite/` pointer table.
7. Update `docs/README.md` to describe the 2-layer v2 flow.
8. Run `/docs-audit` to verify.
9. Tell the user: "Migration complete. Originals preserved as `.deprecated`. Run `rm docs/_lite/*.deprecated` after verifying a fresh session loads context correctly."

### Safety

- Never deletes files
- Never writes to `.claude/settings.json`
- Never runs git commands
- Never modifies `docs/*.md` full files (only creates new `.claude/rules/*.md` and renames `_lite/` files)

---

## Execution guidelines

- **Use the `doc-explorer` subagent** for any task involving reading many files to answer one question (audits, syncs, coverage checks). Install it from [assets/agents/doc-explorer.md](assets/agents/doc-explorer.md) during `init` so it's always available.
- **Always read before writing** — understand existing content before restructuring.
- **Preserve originals** — migrations and segmentation are additive. Never delete.
- **Match project language** — read `Documentation language` from CLAUDE.md. If not declared, ask the user.
- **Commit atomically** — one commit per logical change.
- **Update `docs/README.md` last** — after all other files are created or updated.
- **Dual-update rule** — when a `.claude/rules/*.md` has a corresponding `docs/*.md`, update both in the same commit.
- **Never load multiple full docs at once** — the rules should be enough to orient. Read one full doc when detail is needed.

### New project (`/docs-architect init`)

1. Ask: project name, stack (backend / frontend / both), documentation language, which path-scoped rules apply (backend, frontend, api, database, testing — multi-select).
2. Create `CLAUDE.md` from [assets/CLAUDE.md.template](assets/CLAUDE.md.template).
3. Create `docs/README.md` from [assets/docs-README.md.template](assets/docs-README.md.template).
4. Create full docs (`architecture.md`, `api-contracts.md`, `database-schema.md`, `coding-rules.md`, `tech-stack.md`, `deployment.md`, `roadmap.md`, `backlog.md`, `bugs.md`, `ideas.md`). **No `_lite/` folder.**
5. Copy `assets/rules/_always/*.md` flat into `.claude/rules/` (4 always-loaded files).
6. Copy the user-selected path-scoped rules into `.claude/rules/`.
7. **Code-scan auto-fill** (see below) — populate both the new `.claude/rules/*.md` files AND the full `docs/*.md` files from real codebase content.
8. Copy `assets/commands/*.md` into `.claude/commands/`.
9. Copy `assets/agents/doc-explorer.md` into `.claude/agents/`.
10. **Print** the contents of [assets/hooks/settings.snippet.json](assets/hooks/settings.snippet.json) and tell the user to paste it into `.claude/settings.json`.

#### Code scanning for auto-fill

Scan the codebase to pre-populate both rules and docs with real content:

| Scan target | How to find | Pre-fills |
|---|---|---|
| **Stack & packages** | Read `*.csproj` + `Directory.Packages.props` (or `package.json`, `Cargo.toml`, `requirements.txt`, `go.mod`) | `docs/tech-stack.md` + `.claude/rules/tech-stack.md` |
| **Infrastructure** | Read `docker-compose*.yml`, `Dockerfile*`, `.env*` | `docs/deployment.md` |
| **Architecture** | List project folders + read key files (Program.cs, Startup, middleware, DI registration) | `docs/architecture.md` + `.claude/rules/architecture.md` |
| **API endpoints** | Read controllers/routes, auth filters, middleware registration | `docs/api-contracts.md` + `.claude/rules/api.md` |
| **Database schema** | Read entity/model files, DbContext, migrations | `docs/database-schema.md` + `.claude/rules/database.md` |
| **Coding patterns** | Read existing code for naming, patterns, validation, error handling | `docs/coding-rules.md` + `.claude/rules/coding-rules.md` |
| **Business context** | Read existing README, comments, domain entities | `.claude/rules/business-context.md` |

**Rules for auto-fill**:

- Mark auto-generated sections with `<!-- auto-generated from codebase scan -->` so the user knows what to review.
- If a source file doesn't exist (e.g., no docker-compose), skip that doc section — don't create empty placeholders.
- Always ask the user to review auto-filled content before committing.
- Prefer being incomplete over being wrong — if unsure, note as `TODO: verify` rather than guessing.

### Existing v1 project (`/docs-architect migrate`)

1. Read ALL existing docs and `_lite/` files before making any changes.
2. Follow Step 10 (migrate mode) exactly.
3. **Never delete content** — only restructure, rename, copy.
4. Always show the user the mapping table BEFORE applying it.

### Existing v2 project (`/docs-architect` or `/docs-architect audit`)

1. Read ALL existing docs and `.claude/rules/*.md` before making any changes.
2. **Never delete content** — only restructure, move, or update.
3. If CLAUDE.md is over 100 lines, identify what to offload to `.claude/rules/`.
4. Always show the user what you plan to change BEFORE doing it.
