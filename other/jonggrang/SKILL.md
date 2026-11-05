---
name: jonggrang
description: Deterministic AI development workflow orchestrator. Manages task boards (.jonggrang/jonggrang-tasks.json), runs 16-phase pipelines (BUGFIX/SMALL/MEDIUM/LARGE), installs lifecycle hooks for Claude Code and OpenCode, and coordinates five specialist roles (Lead/Developer/Reviewer/TestLead/Tester). Use when planning features, executing multi-step development workflows, or orchestrating AI coding agents. Run via npx jonggrang.
metadata: {"clawdbot":{"emoji":"🎭","os":["darwin","linux","win32"],"requires":{"runtime":"node","install":"npx jonggrang"}}}
---

# Jonggrang — AI Agent Instructions

You are working inside a project managed by **Jonggrang**, a deterministic AI development workflow orchestrator. This file is your operating manual. Read it completely before doing anything.

---

## How to Run Jonggrang

Use `npx` — no global installation required:

```bash
npx jonggrang <command>
```

If Jonggrang is already installed globally, you can also use `jonggrang <command>` directly. To check:

```bash
npx jonggrang version
```

---

## Your Role in This Project

Jonggrang runs in two modes. Know which one you are in:

### Mode 1 — Work Loop
You are a single agent executing tasks from `.jonggrang/jonggrang-tasks.json` one at a time. Each invocation is stateless — a fresh context window per task.

### Mode 2 — Orchestrate (16-Phase Pipeline)
You are a **specialist agent** assigned to a specific phase and role. You receive a crafted prompt that tells you your role, the current phase, and what the previous agent produced. You must emit a completion signal at the end of your output.

Check `.jonggrang/jonggrang-tasks.json` for your current task's `"role"` field, or look for role instructions in your prompt.

---

## Context Files — Read These First

| File | Purpose | Action |
|------|---------|--------|
| `AGENTS.md` | Project conventions, patterns, gotchas | **Read first. Follow all conventions.** |
| `.jonggrang/progress.txt` | Learnings from previous iterations | **Read. Avoid repeating mistakes.** |
| `.jonggrang/jonggrang-tasks.json` | Task board with current state | **Read. Find your assigned task.** |
| `.jonggrang/jonggrang.json` | Project config (stack, testing, tool) | **Read. Know your test command and stack.** |
| `skills/core/<name>/SKILL.md` | Core skill for your task type | **Read if task has `"skill"` field.** |
| `.jonggrang/.output/features/<id>/MANIFEST.yaml` | Orchestration phase state | **Read in orchestrate mode.** |

---

## Skill System — Two Tiers

Skills are prompt templates that encode expert knowledge. There are two tiers:

### Tier 1: Core Skills (`skills/core/`)
Always available. Loaded into your prompt for every task. Contains foundational patterns:
- How to orchestrate a feature
- How to dispatch parallel agents
- How to invoke the Gateway
- Domain gateway pointers (backend, frontend, api, testing, database)
- Scaffold templates (scaffold-api, scaffold-webapp, component, migration, auth, etc.)

### Tier 2: Library Skills (`skills/library/`)
Loaded on demand via the Gateway when you need deep domain knowledge.

| Domain | Available Skills |
|--------|-----------------|
| `backend` | developing-with-tdd, debugging-systematically, error-handling-patterns |
| `frontend` | debugging-react-hooks, optimizing-react-performance |
| `testing` | unit-testing-patterns, fixing-flaky-tests |
| `database` | safe-migrations |
| `api` | input-validation |
| `security` | rate-limiting |

### Using the Gateway

Before implementing, resolve the right library skill for your task:

```bash
node -e "
const gw = require('./lib/gateway');
const r = gw.buildGatewayResponse('YOUR TASK DESCRIPTION HERE', './skills');
console.log(r);
"
```

The Gateway returns `{ domain, skill_paths, instruction }`. Read each file in `skill_paths` before implementing.

---

## Work Loop — Task Execution Protocol

### Step 1: Understand
- Read all context files listed above
- Read the task description carefully — it contains acceptance criteria
- If the task has `"skill": "scaffold-api"`, read `skills/core/scaffold-api/SKILL.md`
- Check `blocked_by` — dependencies must already be completed

### Step 2: Invoke Gateway
Resolve the right library skills for your task domain:
```bash
node -e "
const gw = require('./lib/gateway');
const r = gw.buildGatewayResponse('<task description>', './skills');
r.skill_paths.forEach(p => console.log('Read:', p));
"
```
Read each returned skill file before proceeding.

### Step 3: Plan
- Identify which files to create or modify
- Check existing code patterns before writing new code
- Follow conventions in `AGENTS.md`
- Keep changes atomic — only touch files relevant to this task

### Step 4: Implement
- Write clean, working code
- Follow existing patterns in the codebase
- Use the project's existing dependencies (don't add unnecessary packages)
- Include proper types (no `any` in TypeScript)

### Step 5: Validate
```bash
# Typecheck
npm run typecheck    # or: tsc --noEmit, go vet, mypy, etc.

# Tests
npm test             # or: the command in .jonggrang/jonggrang.json -> testing.command

# Lint (if configured)
npm run lint
```

If validation fails: read the error, fix it, re-run. If stuck after 2 attempts, stop and report clearly.

### Step 6: Update State

**Update `.jonggrang/jonggrang-tasks.json`** — mark task completed:
```json
{
  "status": "completed",
  "passes": true,
  "completed_at": "<ISO timestamp>"
}
```

**Append to `.jonggrang/progress.txt`** — log learnings:
```
## task-XXX: Task Title
- What was implemented
- What was surprising or non-obvious
- Patterns discovered in the codebase
- Gotchas for future iterations
```

### Step 7: Commit
```bash
git add <specific files only>
git commit -m "type(scope): description"
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`

**Never:** `git add .` or `git add -A`, commit `node_modules/` or `.env`, amend previous commits.

---

## Orchestrate Mode — Role-Specific Instructions

In orchestrate mode you are assigned one of five roles. Your role determines what tools you have and what signal you must emit.

### Role Summary

| Role | Can Edit Files | Can Spawn Agents | Completion Signal |
|------|:-:|:-:|-------------------|
| **Lead** | no | YES (Task tool) | `ARCHITECTURE_PLAN_COMPLETE` |
| **Developer** | YES | no | `IMPLEMENTATION_COMPLETE` |
| **Reviewer** | no (read-only) | no | `REVIEW_COMPLETE` |
| **TestLead** | no | YES (Task tool) | `TEST_PLAN_COMPLETE` |
| **Tester** | YES | no | `ALL_TESTS_PASSING` |

### Phase → Role Mapping

| Phases | Role | What You Do |
|--------|------|-------------|
| 1–4 | *(orchestrator)* | Setup, triage, discovery — handled automatically |
| 5–7, 16 | Lead | Assess complexity, brainstorm, architect, finalise |
| 8 | Developer | Implement the feature end-to-end |
| 9–11, 15 | Reviewer | Verify design, compliance, quality, test quality |
| 12 | TestLead | Write the test plan |
| 13–14 | Tester | Execute tests, verify coverage |

### Completion Signal Protocol

Your **last output line** must be your role's completion signal. The orchestration engine waits for this signal before advancing to the next phase.

```
# Developer — after all code is written, typechecked, and tests pass:
IMPLEMENTATION_COMPLETE

# Tester — after all tests pass and coverage threshold met:
ALL_TESTS_PASSING

# Reviewer — after completing your review:
REVIEW_COMPLETE

# Lead — after producing architecture plan:
ARCHITECTURE_PLAN_COMPLETE

# TestLead — after producing test plan:
TEST_PLAN_COMPLETE
```

### Reading the MANIFEST

In orchestrate mode, the MANIFEST tracks phase state. Read it to understand context:

```bash
cat .jonggrang/.output/features/<feature-id>/MANIFEST.yaml
```

Key fields: `work_type`, `current_phase`, `phases` (per-phase status and output), `validation`.

---

## Rules

### DO
- Read all context files before starting
- Follow conventions in `AGENTS.md` exactly
- Invoke the Gateway to load the right library skill
- Keep changes minimal and focused on the task
- Write tests when the task requires them
- Run validation before committing
- Log learnings in `.jonggrang/progress.txt`
- Emit your completion signal as the final output line (orchestrate mode)

### DO NOT
- Modify files not related to your task
- Add dependencies without clear justification
- Change `AGENTS.md` directly — propose changes in `.jonggrang/progress.txt` instead
- Skip validation steps
- Make multiple commits per task (one atomic commit per task)
- Ignore errors — fix them or report them clearly
- Write `.md` files outside `.jonggrang/`, `AGENTS.md`, `.jonggrang/progress.txt`, `README.md`, `CHANGELOG.md`, or `docs/`

---

## File Ownership

Each task in `.jonggrang/jonggrang-tasks.json` has a `"files"` array listing the files it owns. **Do not modify files owned by other tasks** — this prevents merge conflicts in team mode.

---

## Jonggrang Commands Reference

```bash
# Setup
npx jonggrang init                               # Interactive setup wizard
npx jonggrang init --name x --type api --tool claude --autonomy balanced --force

# Work Loop
npx jonggrang plan "feature description"         # Decompose feature into tasks
npx jonggrang work                               # Run all pending tasks
npx jonggrang work --max-iterations 1            # Run one task only
npx jonggrang work --task task-003               # Run a specific task
npx jonggrang work --tool claude                 # Override AI tool
npx jonggrang work --dry-run                     # Preview prompt, no execution
npx jonggrang work --mode supervised             # Override autonomy

# Orchestrate (16-phase deterministic pipeline)
npx jonggrang orchestrate "description"          # Start full pipeline
npx jonggrang orchestrate --resume               # Resume interrupted pipeline
npx jonggrang orchestrate "..." --dry-run        # Preview all phase prompts
npx jonggrang orchestrate "..." --autonomy autonomous  # Skip human pauses

# Utilities
npx jonggrang status                             # Show task board
npx jonggrang review                             # Run code review
npx jonggrang version                            # Show version
npx jonggrang help                               # All commands and flags
```

---

## Example: Completing a Work Loop Task

Given this task in `.jonggrang/jonggrang-tasks.json`:

```json
{
  "id": "task-002",
  "title": "Add Todo CRUD endpoints",
  "description": "Create GET/POST/PUT/DELETE endpoints for /api/todos with in-memory storage",
  "skill": "scaffold-api",
  "files": ["src/routes/todos.ts", "src/types/todo.ts"],
  "blocked_by": ["task-001"]
}
```

Execution:

1. Read `AGENTS.md`, `.jonggrang/progress.txt`, `.jonggrang/jonggrang-tasks.json`, `.jonggrang/jonggrang.json`
2. Read `skills/core/scaffold-api/SKILL.md`
3. Run Gateway to resolve library skills for this task type
4. Read existing code (`src/app.ts`, other routes) to understand patterns
5. Create `src/types/todo.ts` with the Todo interface
6. Create `src/routes/todos.ts` with CRUD handlers
7. Register routes in `src/app.ts`
8. Run `npm run typecheck && npm test`
9. Update `.jonggrang/jonggrang-tasks.json` (status: completed, passes: true)
10. Append learnings to `.jonggrang/progress.txt`
11. `git add src/routes/todos.ts src/types/todo.ts src/app.ts .jonggrang/jonggrang-tasks.json .jonggrang/progress.txt`
12. `git commit -m "feat(todos): add CRUD endpoints with in-memory storage"`
