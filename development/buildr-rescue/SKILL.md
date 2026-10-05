---
name: buildr-rescue
description: |
  Takes an existing stuck, broken, or abandoned development project and
  gets it unstuck. Scans the codebase, diagnoses what's wrong, wraps a
  Buildr workspace around the existing code, and generates fix-waves
  that the executor can run.

  USE THIS SKILL when: the user has an existing project that has stalled,
  has bugs they can't solve, has architectural problems, was abandoned
  mid-build, or needs to be taken over from another developer/agent.

  Triggers on: "fixa detta projekt", "det har kört fast", "ta över",
  "hjälp med detta repo", "debug", "rescue", "stuck", "broken project",
  "take over", "fix this", "halfway done", "abandoned", "importera projekt",
  or when the user points at an existing codebase and needs help.

  The Operator starts from zero. The Rescue starts from broken.
---

# Buildr Rescue

## What This Skill Does

Takes a stuck project → diagnoses it → wraps Buildr around it → fixes it.

Unlike the Operator which starts from a blank canvas, the Rescue skill
starts with existing code. It doesn't rewrite — it understands, diagnoses,
and surgically fixes. The existing code is respected as work that was done
for a reason.

## The Pipeline

```
User points at an existing project
    ↓
Phase 1: INTAKE (scan structure, detect stack, map what exists)
    ↓
Phase 2: DIAGNOSE (find what's broken, missing, or stuck)
    ↓
Phase 3: TRIAGE (prioritize: what's blocking vs nice-to-fix)
    ↓
Phase 4: WRAP (create Buildr workspace around existing code)
    ↓
Phase 5: PLAN (generate fix-waves the executor can run)
    ↓
Phase 6: REGISTER (add to project registry as rescue origin)
```

---

## Phase 1: Intake

Scan the project without changing anything.

### Automatic Detection

```
1. Read directory structure (depth 3)
2. Detect stack:
   - package.json → Node/React/Next.js/Vue (read dependencies)
   - requirements.txt / pyproject.toml → Python
   - Cargo.toml → Rust
   - go.mod → Go
   - Gemfile → Ruby
   - *.sln / *.csproj → .NET
3. Detect framework from dependencies
4. Find entry points (index.html, app.py, main.ts, etc.)
5. Find config files (.env.example, docker-compose, CI configs)
6. Read README.md if it exists
7. Check git log — how much history? Last commit when? Who?
8. Count files, total LOC, languages used
```

### Intake Report (internal, not shown unless asked)

```
PROJECT: [name from package.json / directory name]
PATH: [absolute path]
STACK: [detected stack]
FRAMEWORK: [detected framework + version]
FILES: [count] files, [LOC] lines
LANGUAGES: [breakdown]
LAST_COMMIT: [date] by [author] — "[message]"
COMMIT_COUNT: [N] commits over [timespan]
HAS_TESTS: [yes/no — test files found?]
HAS_CI: [yes/no — CI config found?]
HAS_TYPES: [yes/no — TypeScript / type hints?]
HAS_LINT: [yes/no — eslint/ruff/prettier config?]
DEPENDENCIES: [count] deps, [count] devDeps
```

---

## Phase 2: Diagnose

Find what's actually wrong. This is the critical phase — do it thoroughly.

### Diagnostic Checks

#### 2.1 Build Health
```
1. Can it build? Run the build command.
   - package.json → npm install && npm run build
   - pyproject.toml → pip install -e . or python setup.py
   - If build fails → capture full error output
2. Can it start? Run the dev/start command.
   - If start fails → capture error
3. Are there TypeScript/lint errors?
   - Run tsc --noEmit if TypeScript
   - Run linter if configured
```

#### 2.2 Code Health
```
1. Read entry point files — follow the execution path
2. Check for:
   - Dead imports (imported but unused)
   - Circular dependencies
   - Files that import things that don't exist
   - Environment variables used but not in .env.example
   - Hardcoded URLs, API keys, or secrets
   - Empty catch blocks (swallowed errors)
   - TODO/FIXME/HACK comments (list them all)
   - Files over 300 lines (complexity smell)
```

#### 2.3 Completeness
```
1. Are there pages/routes that return 404 or blank?
2. Are there components that render nothing?
3. Are there API endpoints that return 500 or not implemented?
4. Are there database migrations that haven't been run?
5. Is there a .env.example with vars not in .env?
6. Are there features mentioned in README but not implemented?
```

#### 2.4 Architecture
```
1. Is there a clear separation of concerns? (or is everything in one file?)
2. Are there shared types/interfaces? (or is everything any/unknown?)
3. Is state management coherent? (or is it spread everywhere?)
4. Are API calls centralized? (or inline fetch() everywhere?)
5. Is there error handling? (or just happy path?)
```

### Diagnosis Output

For each issue found:

```
ISSUE: [short description]
SEVERITY: BLOCKER | MAJOR | MINOR
LOCATION: [file:line or general area]
EVIDENCE: [what you found — specific, not vague]
ROOT_CAUSE: [why this happened — if determinable]
FIX_COMPLEXITY: trivial | moderate | significant
```

Minimum: find at least 3 issues. If you find fewer, dig deeper.
Maximum: 20 issues. If you find more, group related ones.

---

## Phase 3: Triage

Sort issues by impact and create a fix plan.

### Priority Rules

```
1. BLOCKERS first — project can't run without these
2. Then MAJOR issues that affect core functionality
3. Then MINOR issues that affect quality
4. Group related issues into fix-units (one wave per group)
```

### Triage Output

```
## Fix Plan

### Wave 1: [title] — BLOCKER fixes
- Fix [issue 1]
- Fix [issue 2]
Expected: project builds and starts

### Wave 2: [title] — Core functionality
- Fix [issue 3]
- Fix [issue 4]
Expected: main features work

### Wave 3: [title] — Quality & completeness
- Fix [issue 5]
- Complete [incomplete feature]
Expected: production-ready

### Out of Scope (flagged but not fixing)
- [issue that requires human decision]
- [issue that requires external service access]
```

---

## Phase 4: Wrap

Create a Buildr workspace AROUND the existing project. The existing code
stays in place — the workspace is an overlay.

### Workspace Structure

```
[existing-project]/
├── [all existing files untouched]
│
├── .buildr/                    ← NEW: Buildr overlay
│   ├── WORKSPACE.md            ← Project overview + diagnosis summary
│   ├── PROJECT.md              ← Hard constraints (derived from existing code)
│   ├── SYSTEM.md               ← Design system (extracted from existing CSS/config)
│   ├── MEMORY.md               ← Diagnosis as Imperfektum memory (scars = found bugs)
│   ├── RUN.md                  ← Execution runbook for fix-waves
│   ├── AGENT.md                ← Agent protocol
│   │
│   ├── state/
│   │   └── orchestration.yaml  ← Wave tracking for fixes
│   │
│   ├── waves/
│   │   ├── 001-blockers.md     ← First fix-wave
│   │   ├── 002-core.md         ← Second fix-wave
│   │   └── ...
│   │
│   ├── qa/
│   │   ├── checklist.md        ← Per-wave verification
│   │   ├── gates.md            ← 3-phase quality gates
│   │   └── acceptance.md       ← Definition of "fixed"
│   │
│   ├── agents/                 ← Derived agent team
│   │   ├── agent-manifest.json
│   │   └── *.md
│   │
│   └── diagnosis/
│       ├── intake-report.md    ← Full intake scan results
│       └── issues.md           ← All diagnosed issues with evidence
```

### Key Principle: The .buildr/ directory is the ONLY thing Rescue creates.
The existing code is never restructured, moved, or reorganized during the
wrap phase. Changes to existing code happen ONLY during wave execution.

### MEMORY.md for Rescue Projects

The Imperfektum memory is special for rescue projects — it's based on
REAL discovered issues, not fabricated memories:

```markdown
## Scars (discovered during diagnosis)

### Scar: Build failure on missing dependency
**When:** During initial diagnosis
**What happened:** npm install fails because @types/node is missing from devDeps
**Consequence:** No developer could run this project after cloning
**Now we:** Always verify the project builds from a clean install before anything else

### Scar: Swallowed errors in API layer
**When:** Reviewing api/routes.ts
**What happened:** Every catch block was empty — errors silently disappeared
**Consequence:** Users saw blank screens with no feedback
**Now we:** Every catch block must either re-throw, log, or show user message
```

These are REAL scars from REAL diagnosis — the most powerful form of Imperfektum.

---

## Phase 5: Plan

Generate fix-waves that the Executor can run.

### Wave Design Rules for Rescue

1. **Wave 1 always makes the project buildable/runnable**
   - Dependency fixes, config fixes, environment setup
   - Exit criteria: `npm run dev` (or equivalent) starts without error

2. **Each subsequent wave fixes one category of issues**
   - Don't mix frontend bugs with API bugs in the same wave
   - Each wave has clear, testable exit criteria

3. **Waves are conservative**
   - Fix what's broken, don't refactor what works
   - Preserve existing patterns even if you'd do it differently
   - Only change architecture if it's the root cause of bugs

4. **Last wave is always verification**
   - End-to-end smoke test
   - All original diagnosis issues verified as fixed
   - Nothing new broken

### Wave Template for Rescue

```markdown
# Wave [N]: [Title]

## Intent
Fix: [list of issues from diagnosis this wave addresses]

## Constraints
- Do NOT change [files/patterns that work]
- Preserve existing [API contracts / UI patterns / data structures]
- Maximum [N] files modified

## Steps
1. [Specific fix with file:line reference]
2. [Specific fix]
3. [Verification step]

## Exit Criteria
- [ ] [Binary check that issue is fixed]
- [ ] [No regressions in adjacent features]
- [ ] Project still builds and starts cleanly
```

---

## Phase 6: Register

Register the project in the Buildr project registry.

```bash
bash memory-system/tools/project-registry.sh \
  --register \
  --name "[project-name]" \
  --path "[absolute-path]" \
  --category "[detected-category]" \
  --origin "rescue"
```

The `rescue` origin flag means:
- The project shows `[R]` in registry listings
- Other agents know this is existing code, not greenfield
- The workspace is in `.buildr/`, not at root level

---

## Output Summary Format

After completing all phases, present to the user:

```markdown
## Rescue Report: [Project Name]

### Intake
- Stack: [stack] / [framework] [version]
- Size: [files] files, [LOC] lines
- Last activity: [date] ([days] ago)

### Diagnosis
- [N] issues found: [N] BLOCKER, [N] MAJOR, [N] MINOR
- Root cause: [one-sentence summary of main problem]

### Fix Plan
- [N] waves planned
- Wave 1: [title] — makes it buildable
- Wave 2: [title] — fixes core issues
- Wave 3+: [titles]
- Estimated effort: [N] files to modify

### Workspace Created
- `.buildr/` directory with [N] files
- Ready for executor: `cd [project] && read .buildr/RUN.md`

### Out of Scope
- [Things that need human decisions]
- [Things that need access/credentials]
```

---

## Key Principles

1. **Respect the existing code.** Someone wrote it for a reason. Fix what's
   broken, don't rewrite what works. Preserve patterns and conventions.

2. **Diagnose before fixing.** Never start changing code until the full
   diagnosis is complete. The wrong fix is worse than no fix.

3. **The .buildr/ overlay is non-invasive.** It sits alongside the existing
   project. Removing `.buildr/` leaves the project exactly as it was
   (plus any fixes made during wave execution).

4. **Real scars are better than fabricated ones.** Rescue projects have
   genuine Imperfektum memories from actual diagnosis. Use them.

5. **Conservative fixes over ambitious refactors.** The goal is to get the
   project working, not to make it perfect. Ship working code, not
   aspirational architecture.

6. **Every fix is verifiable.** If you can't write a binary pass/fail check
   for a fix, the fix isn't concrete enough.
