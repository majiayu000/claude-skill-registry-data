---
name: vibe-init
description: >
  Onboards an existing or legacy codebase into the vibe-* skills framework.
  Reads actual source files, infers architecture and patterns, generates the full vibe/ folder
  so vibe-add-feature, vibe-fix-bug, vibe-review, and all vibe-* skills work immediately.
  Triggers on "vibe-init", "onboard this project", "init the vibe folder",
  "set up vibe for this project", "this is a legacy project", "retrofit this codebase",
  "I want to use vibe skills on an existing project", "add vibe to this repo",
  "the vibe folder doesn't exist", "can we use vibe skills here".
  Always use when the user has an existing codebase with no vibe/ folder and wants
  to use any vibe-* skill — even without the exact trigger phrases.
  Single agent session — reads everything, generates everything, no staged checkpoints.
  Produces CLAUDE.md and full vibe/ folder grounded in actual code.
  SPEC.md marked PROVISIONAL — verify before first vibe-review run.
  DECISIONS.md starts from today — all prior decisions untracked by design.
---

# Vibe Init Skill

Reverse-engineers the vibe-* framework scaffold from an existing codebase.
Reads actual source files. Infers everything from code. Documents only what is observed.
Produces a complete vibe/ folder that immediately unblocks all vibe-* skills.

> **Autonomous / headless mode.** At startup resolve the settings with
> `python3 ~/.claude/skills/vibe-mode/scripts/vibe_state.py mode`. If `vibe_mode` is
> `autonomous`, every "wait", "ask", "confirm" and approval step in this skill follows
> vibe-mode's `references/HEADLESS.md` §2 instead: take the recommended option, accept your
> own draft after one self-check, log each choice to `vibe/DECISIONS.md`, never ask the
> user, and stop — writing `vibe/.run_state.json` — only when a person is genuinely required.

**Run in agent mode (Claude Code / Cursor). Requires filesystem access.**
**Single session — reads everything, generates everything, no staged checkpoints.**

---

## The contract this skill establishes

**Code is the source of truth.** Nothing is invented. If it's in ARCHITECTURE.md,
it was observed in the codebase. If it's in CODEBASE.md, the file exists.

**The past is untracked. The future is fully tracked.**
DECISIONS.md starts with one bootstrap entry dated today.
Every decision made through vibe-* skills from this point forward gets logged.
Prior decisions are acknowledged as unknown — not fabricated.

**SPEC.md is provisional.**
It describes observed behaviour, not planned requirements.
It is marked clearly. vibe-review will flag it until a human verifies it.
This is honest — encoding bugs as requirements is worse than flagging uncertainty.

---

## Pre-flight — confirm project root

Before reading anything:

```bash
pwd
ls -la
```

Confirm you are at the project root (the directory containing the source code).
If not, stop and ask the user to navigate there first.

Check if vibe/ already exists:
```bash
ls -d vibe/ 2>/dev/null && echo "EXISTS" || echo "NOT FOUND"
```

If vibe/ already exists:
> "A vibe/ folder already exists in this project. Running vibe-init will overwrite it.
> Do you want to continue and regenerate from the current codebase state?"
Wait for explicit confirmation before proceeding.

---

## Large codebase protocol

Run this immediately after the pre-flight check — before any file reading.

```bash
find . -type f \
  ! -path '*/node_modules/*' ! -path '*/.git/*' \
  ! -path '*/dist/*' ! -path '*/build/*' \
  ! -path '*/__pycache__/*' ! -path '*/.next/*' \
  ! -path '*/coverage/*' ! -path '*/vendor/*' \
  | wc -l
```

**Classify by file count and set reading budget:**

| Size | Files | Stage 2 anchor reads | Stage 3 sample per folder |
|------|-------|---------------------|--------------------------|
| Small | < 50 | All anchor files | 3 files |
| Medium | 50–200 | All anchor files | 2 files |
| Large | 200–500 | Anchor files — max 25 total | 1 file |
| XL | 500+ | Anchor files — max 15 total | 1 file (critical folders only) |

**For Large (200–500 files):**
- Cap Stage 2 at 25 total file reads across all categories
- Prioritise: package manifest → entry points → schema files → 2 route files → 2 service files
- Stage 3: sample 1 file per folder type, skip folders with < 3 files
- Add to all generated docs: `⚠️ Large codebase — sampled [N]/[total] files`

**For XL (500+ files):**
- Cap Stage 2 at 15 total file reads
- Prioritise: package manifest → entry point → schema file → 1 route file only
- Stage 3: skip — infer patterns from Stage 2 anchor files only
- Add to all generated docs: `⚠️ XL codebase — [N] files. CODEBASE.md covers critical paths only.`
- Tell the user: "This is a large codebase ([N] files). I'll document the critical paths.
  Run `document:` on specific modules to fill gaps progressively."

Store the size classification. Apply the budget throughout Stages 2 and 3.

---

## Stage 1 — Topology scan

**Goal:** Understand the full shape of the project without reading file contents.
Fast. Covers everything.

```bash
find . -type f \
  ! -path '*/node_modules/*' \
  ! -path '*/.git/*' \
  ! -path '*/dist/*' \
  ! -path '*/build/*' \
  ! -path '*/__pycache__/*' \
  ! -path '*/.next/*' \
  ! -path '*/coverage/*' \
  ! -path '*/vendor/*' \
  | sort
```

Also run:
```bash
find . -maxdepth 3 -type d \
  ! -path '*/node_modules/*' \
  ! -path '*/.git/*' \
  ! -path '*/dist/*' \
  ! -path '*/build/*' \
  | sort
```

From the topology, extract:

**Tech stack indicators** (file extensions, config filenames):
- `package.json` → Node.js ecosystem
- `requirements.txt` / `pyproject.toml` / `Pipfile` → Python
- `go.mod` → Go
- `pubspec.yaml` → Flutter/Dart
- `Gemfile` → Ruby
- `pom.xml` / `build.gradle` → Java/Kotlin
- `composer.json` → PHP

**Framework indicators** (folder names, config files):
- `pages/` or `app/` + `next.config.*` → Next.js
- `src/routes/` + `svelte.config.*` → SvelteKit
- `resources/views/` → Laravel
- `app/controllers/` → Rails
- `manage.py` → Django
- `main.py` + `routers/` → FastAPI

**Structural pattern** (from folder names):
- `components/` + `pages/` + `hooks/` → feature-type frontend
- `controllers/` + `services/` + `models/` → MVC backend
- `features/` or `modules/` with sub-folders → feature-based
- flat `src/` → unstructured (note this explicitly)

**Database indicators:**
- `prisma/schema.prisma` → Prisma ORM
- `migrations/` or `alembic/` → SQL migrations present
- `models/` with ORM patterns → ORM-based
- `*.sql` files → raw SQL

Log your topology findings internally. Do not generate any output files yet.

---

## Stage 2 — Anchor file deep read

**Goal:** Read the highest-signal files in full to confirm stack, entry points, and core patterns.

Read every file in this list that exists. Do not skip any that are present.

**Package / dependency manifests (read in full):**
- `package.json`
- `package-lock.json` or `yarn.lock` (dependencies only — skip lockfile hashes)
- `requirements.txt` / `pyproject.toml` / `Pipfile`
- `go.mod`
- `pubspec.yaml`
- `Gemfile`
- `composer.json`

**Configuration files (read in full):**
- `.env.example` or `.env.sample` (NEVER `.env` — never read secrets)
- `docker-compose.yml` / `docker-compose.yaml`
- `Dockerfile`
- `.eslintrc*` / `eslint.config.*`
- `tsconfig.json`
- `vite.config.*` / `next.config.*` / `nuxt.config.*` / `svelte.config.*`
- `tailwind.config.*`
- `jest.config.*` / `vitest.config.*` / `pytest.ini` / `pyproject.toml` (test section)

**Entry points (read in full):**
- `src/index.*` / `index.*` (root level)
- `src/main.*` / `main.*`
- `src/app.*` / `app.*`
- `src/server.*` / `server.*`
- `src/App.*` (React/Vue root component)

**Route / controller files (read in full — max 5 files):**
- Any file in `routes/`, `controllers/`, `api/`, `pages/api/`, `routers/`
- Prefer the file with the most routes (largest)

**Schema / model files (read in full — max 5 files):**
- `prisma/schema.prisma`
- Any file in `models/`, `schemas/`, `types/`, `db/`
- `src/types/index.*`

**README (read in full if present):**
- `README.md` / `README.rst`
Note: README may be outdated. Cross-check against actual code. Flag discrepancies.

**Security rule — never read:**
- `.env`
- Any file named `secrets.*`, `credentials.*`, `*.key`, `*.pem`, `*.p12`
- Any file in `certs/` or `keys/`

---

## Stage 3 — Pattern sampling

**Goal:** Confirm patterns by reading representative files from each major folder.

For each distinct folder type identified in Stage 1, read 2–3 files in full.
Choose the largest or most centrally-named files — they tend to show the most patterns.

Standard sampling targets:

| Folder type | Files to read | What to extract |
|-------------|--------------|----------------|
| `components/` | 2 representative components | Props patterns, styling approach, composition style |
| `hooks/` or `composables/` | 2 custom hooks | State management patterns, side effect handling |
| `services/` | 2 service files | API call patterns, error handling, data transformation |
| `utils/` or `lib/` | 2 utility files | Helper patterns, shared logic |
| `middleware/` | All (usually small) | Auth patterns, request handling |
| `tests/` or `__tests__/` | 2 test files | Testing patterns, coverage approach |
| `migrations/` | Most recent migration | Schema evolution approach |

**Sampling budget — apply the size classification from large codebase protocol:**
- Small: 3 files per folder type
- Medium: 2 files per folder type
- Large: 1 file per folder type
- XL: skip Stage 3 — patterns inferred from Stage 2 anchor files only

**What to extract from each sampled file:**
- Naming conventions (files, functions, variables, components)
- Import patterns (absolute vs relative, barrel exports)
- Error handling approach
- TypeScript usage (strict, any usage, custom types)
- Code organisation within files
- Comments and documentation style

---

## Stage 4 — Synthesise findings

Before writing any files, internally consolidate everything from Stages 1–3:

**Confirmed stack:**
`[runtime] + [framework] + [database] + [key libraries]`

**Structural pattern:**
`[feature-based / MVC / type-based / flat / mixed]`

**Naming conventions observed:**
- Files: `[camelCase / kebab-case / PascalCase / snake_case]`
- Functions: `[camelCase / snake_case]`
- Components: `[PascalCase]`
- Variables: `[camelCase / snake_case]`

**State management:** `[local state only / Context / Zustand / Redux / Pinia / none observed]`

**Testing:** `[Jest / Vitest / pytest / none observed]` — coverage: `[present / absent]`

**Code quality tooling:** `[ESLint / Prettier / Ruff / Flake8 / none observed]`

**Key integration points observed:**
`[external APIs, auth provider, payment system, storage, etc.]`

**Honest gaps — things not observed:**
List anything the code doesn't make clear. These become flagged unknowns in the docs.

---

## Stage 5 — Generate vibe/ folder

Now write all files. Write them in this exact order — each file informs the next.

### 5A — vibe/ARCHITECTURE.md

Read `references/ARCHITECTURE_RETROFIT.md` for the full template.

Fill from Stage 4 synthesis. Every section must be grounded in observed evidence.
For each architectural decision, note: `[Observed in: filename or pattern]`

Key sections to populate:
- Architecture overview (ASCII diagram of actual layers)
- Folder structure (exact observed structure with rules inferred from patterns)
- Naming conventions (from Stage 3 sampling — specific, not generic)
- State management (observed approach + rules)
- Error handling (observed patterns)
- Testing philosophy (what exists, what coverage looks like)
- Code quality (observed tooling + inferred rules)
- Tech stack (confirmed from Stage 2)

Mark the file header:
```
> 📥 Generated by vibe-init on [date] from codebase analysis.
> Reflects patterns observed in the actual code — not planned decisions.
> Update this file as new patterns are deliberately introduced.
```

### 5B — vibe/CODEBASE.md

Read `references/CODEBASE_RETROFIT.md` for the full template.

This is the most important file for unblocking vibe-add-feature and vibe-fix-bug.
Be thorough. Every key file should be in here.

Sections to populate:
1. **Tech stack** — confirmed from Stage 2
2. **Commands** — dev, build, test, lint (from package.json scripts or Makefile)
3. **Folder map** — every significant folder with one-line purpose
4. **Key files** — every file that other files depend on (entry points, shared utils, config)
5. **Routes / endpoints** — every route observed in Stage 2 + 3
6. **Data model** — every schema/model observed in Stage 2
7. **Key components** — significant UI components with props and purpose
8. **Services / modules** — external integrations, business logic modules
9. **Integration points** — external APIs, auth, payments, storage
10. **Patterns** — the specific patterns confirmed in Stage 3 (with file examples)

Mark each section that was partially sampled:
`> ⚠️ Partially sampled — [N] files read from [folder]. Update as more files are touched.`

### 5C — vibe/SPEC.md

Read `references/SPEC_RETROFIT.md` for the full template.

Add this banner at the very top — it must be visible:
```
> ⚠️ PROVISIONAL SPEC — generated by vibe-init from observed code behaviour.
> This describes what the code DOES, not necessarily what it was INTENDED to do.
> Verify this spec before using vibe-review — incorrect specs will pass broken code.
> Last verified: [unverified — pending human review]
```

Sections to populate from code observation:
1. **Overview** — inferred purpose of the application (2-3 sentences from README + entry points)
2. **Observed features** — what the code demonstrably does (routes, UI flows, data operations)
3. **Data model** — entities and relationships as observed in schema files
4. **Tech stack** — confirmed
5. **Integrations** — external services observed
6. **Out of scope** — explicitly unknown (not inferred — mark as "not determined during init")
7. **Conformance checklist** — leave empty, to be filled by the team

Every feature listed must have a note: `[Inferred from: file/route/component name]`

### 5D — vibe/SPEC_INDEX.md

Generate compressed map of SPEC.md. Follow same format as vibe-new-app.
Add provisional banner at top.

### 5E — vibe/DECISIONS.md

```markdown
# DECISIONS — [Project Name]
> Append-only. Every drift, scope change, tech choice — logged with full context.
> Onboarded via vibe-init on [date]. All decisions prior to this date are untracked.

## Decision types
- drift — deviated from ARCHITECTURE.md
- blocker-resolution — impossible; workaround found
- tech-choice — chose between valid approaches
- scope-change — added/removed via change: command
- discovery — unexpected finding affecting future tasks

## Format
### D-[ID] — [Short title]
- **Date**: · **Task**: [TASK-ID] · **Type**: [type]
- **What was planned**: · **What was done**: · **Why**:
- **Alternatives considered**: · **Impact on other tasks**:
- **Approved by**: human | agent-autonomous

---

### D-001 — Project onboarded via vibe-init
- **Date**: [today] · **Task**: vibe-init · **Type**: discovery
- **What was planned**: N/A — legacy project, no prior vibe context
- **What was done**: Generated vibe/ scaffold from codebase analysis.
  Stack: [confirmed stack]. Pattern: [confirmed pattern].
  Files read: [N] files across [N] directories.
- **Why**: Retrofitting vibe-* skills framework onto existing codebase.
- **Alternatives considered**: Manual documentation (rejected — too slow and error-prone)
- **Impact on other tasks**: All vibe-* skills now operational.
  SPEC.md is provisional — verify before first vibe-review run.
- **Approved by**: human (triggered vibe-init)
```

### 5E-bis — vibe/IMPLEMENTATION_LOG.md

Create `vibe/IMPLEMENTATION_LOG.md` from the canonical template in
`../vibe-new-app/references/IMPLEMENTATION_LOG_MD.md` (the **FILE TEMPLATE** block, verbatim).
It is the append-only **implementation-decision** log (code-altitude "why this approach,
why this library") — the companion to DECISIONS.md's spec/scope log. On a retrofit it starts
empty (prior implementation decisions are untracked by design, like DECISIONS.md); the build
skills append to it going forward, and `Touches:` lines link entries to vibe-graph nodes.

### 5F — vibe/TASKS.md

Generate a minimal but honest TASKS.md:

```markdown
# TASKS — [Project Name]
> Onboarded via vibe-init on [date].
> This project was not built using the vibe-* framework.
> TASKS.md starts here. All future work tracked from this point forward.

## What we're working with
[2-3 sentences describing the project as inferred — stack, purpose, approximate scale]

## Active work
(nothing yet — add a feature with `feature:` or fix a bug with `bug:`)

## Completed
(prior work not tracked — project onboarded on [date])

## Phase gates
(not applicable — project pre-dates vibe-* framework)

## What's next
Run `review:` on the current codebase to establish a quality baseline.
Then use `feature:` or `bug:` to start tracking work normally.
```

### 5G — Create remaining folders

```bash
mkdir -p vibe/reviews
mkdir -p vibe/features
mkdir -p vibe/bugs
mkdir -p vibe/backlog
```

Create `vibe/reviews/backlog.md`:
```markdown
# Review backlog
> Started on [date] via vibe-init.
> Run `review:` to populate this file with the first quality baseline.
## Outstanding P1 issues
(none yet — run review: to establish baseline)
## Outstanding P2 issues
(none yet)
## Resolved issues
(none yet)
```

### 5H — CLAUDE.md (project root)

Read `references/CLAUDE_RETROFIT.md` for the full template.

Generate CLAUDE.md at **project root**.

Key differences from greenfield CLAUDE.md:
- Session startup reads `vibe/CODEBASE.md` first (existing code, not scaffolded)
- Phase gates section replaced with: "No phase structure — this is an existing project. Use vibe-review on demand."
- Active feature section still present — used by add-feature and fix-bug normally
- Note at top: "Onboarded via vibe-init on [date]"

Commands section must be populated from actual observed scripts:
```bash
# From package.json scripts / Makefile / observed patterns
dev:   [actual dev command]
build: [actual build command]
test:  [actual test command]
lint:  [actual lint command]
```

If a command wasn't observed, write: `# Not observed during init — confirm with team`

---

## Stage 6 — Spec review gate

`vibe-spec-review` documents "Trigger 3 — after vibe-new-app or vibe-init", and a
retrofit is exactly where it matters most: the SPEC.md was inferred from code and is
marked PROVISIONAL. Invoke it **before** presenting the completion report — the gate
runs first, not after you've told the user the job is done.

> "vibe/ folder generated from the codebase. Running spec-review — the SPEC.md is
>  PROVISIONAL, so this checks it before you build on it..."

Invoke `vibe-spec-review`:
- Trigger source: `vibe-init`
- Scope: SPEC.md + ARCHITECTURE.md + BRIEF.md (all that exist)

It will flag the PROVISIONAL SPEC.md as a P1 to verify — expected for a retrofit, not
a failure. Present findings, then continue to the report.

---

## Stage 7 — Post-generation report

After spec-review has run, output a single consolidated report in the conversation:

```
✅ vibe-init complete — [Project Name]

GENERATED FILES
  CLAUDE.md                   ← project root
  vibe/ARCHITECTURE.md        ← [N] patterns documented
  vibe/CODEBASE.md            ← [N] files mapped, [N] routes, [N] models
  vibe/SPEC.md                ← PROVISIONAL — [N] features inferred
  vibe/SPEC_INDEX.md
  vibe/DECISIONS.md           ← D-001 bootstrap entry
  vibe/IMPLEMENTATION_LOG.md  ← empty; implementation decisions logged from here on
  vibe/TASKS.md
  vibe/reviews/backlog.md

WHAT WAS READ
  Stage 1: [N] files in topology scan
  Stage 2: [N] anchor files read in full
  Stage 3: [N] files sampled across [N] folder types

CONFIRMED
  Stack:     [e.g. Next.js 14 + TypeScript + Prisma + PostgreSQL]
  Pattern:   [e.g. Feature-based, MVC-ish]
  Routes:    [N] endpoints documented
  Models:    [N] data models documented
  Commands:  dev / build / test / lint [confirmed / partially confirmed]

FLAGGED UNKNOWNS
  [List anything not determined — honest gaps]

⚠️  BEFORE RUNNING vibe-review:
  Scan vibe/SPEC.md and verify the inferred features are correct.
  Incorrect specs will cause review: to pass broken code.
  When verified, remove the PROVISIONAL banner and update "Last verified" date.

WHAT WORKS NOW
  ✅ vibe-add-feature  — CODEBASE.md and ARCHITECTURE.md ready
  ✅ vibe-fix-bug      — CODEBASE.md and ARCHITECTURE.md ready
  ✅ vibe-review       — works, but note PROVISIONAL SPEC warning above
  ✅ vibe-design       — CODEBASE.md ready; DESIGN_SYSTEM.md generated on first design: run
  ✅ vibe-progress     — TASKS.md ready (starts from today)
  ✅ vibe-change-spec  — SPEC.md ready (verify first)
  ✅ vibe-graph        — dependency graph built from CODEBASE.md

SUGGESTED FIRST STEP
  review:              ← establishes quality baseline on the existing codebase
```

---

## Post-completion — Build dependency graph

After spec-review and the completion report, invoke `vibe-graph: build`.

This converts the CODEBASE.md just written into a queryable dependency graph.
No extra file reads — the information was just extracted for CODEBASE.md.
The graph enables vibe-fix-bug, vibe-test, and vibe-review to query
relationships directly instead of loading the full CODEBASE.md.

```
vibe-graph: build complete
  Files indexed from CODEBASE.md: [N]
  Concepts mapped: [N]
  Graph: vibe/graph/ (3 files generated)
  Next update: automatic after next vibe-add-feature or vibe-fix-bug
```

---

## Absolute rules

**Never invent.** If a pattern wasn't observed, it doesn't go in the docs.
Use "not observed during init" over leaving a section blank.

**Never read secrets.** `.env`, `*.key`, `*.pem`, `credentials.*` — skip unconditionally.

**Never overstate certainty.** "Pattern observed in 3 of 4 service files" is more honest
than "the project uses service-layer pattern."

**Never generate PLAN.md.** That's a greenfield document — phases and scaffolding
don't apply to existing code. Its absence will not break any vibe-* skill.

**Flag every gap explicitly.** Unknowns in the docs are features, not failures.
They tell the next agent exactly where to look when something doesn't make sense.

**Large codebase caveat is mandatory.** Any project with 200+ files must carry the
partial sampling warning in ARCHITECTURE.md, CODEBASE.md, and the post-generation report.
