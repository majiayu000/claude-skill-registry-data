---
name: incremental-context-building
description: Use when entering a large unfamiliar codebase. Build understanding in layers, not all-at-once.
---

# Incremental Context Building — Layered Exploration

When you land in an unfamiliar codebase (>50 files, or any project you haven't seen this session), do NOT immediately Read 20 files into context. That blows up your context budget and leaves you trying to reason across a wall of code with no mental model.

## Iron Law

**Build understanding in layers, decide at each layer whether to go deeper. Never Read a file unless you have a specific question it will answer.** "I should familiarize myself with the code" is not a specific question.

## The Three Layers

### L1 — Orientation (1-2 minutes, <5K tokens)

Goal: know what this project IS and where to look next.

Read or Glob:
- `README.md` (first 100 lines is usually enough)
- `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` / `pom.xml` — whatever declares the stack
- Top-level directory listing — names alone reveal a lot
- `CLAUDE.md` if present — project-specific instructions

Output of L1: a 2-sentence mental model. "This is a Python FastAPI service with a Postgres backend. Entry point looks like `src/app/main.py`. Tests live in `tests/`."

If you can't say that after L1, do one more L1 pass (don't escalate to L2 blindly).

### L2 — Shape (3-5 minutes, ~15K tokens)

Goal: know the major modules and how they connect.

Read:
- The entry point file (e.g., `main.py`, `index.ts`, `App.tsx`)
- 1-2 representative core modules (e.g., one route handler, one model, one service)
- Config files (settings, environment, build config) — skim, don't memorize
- The test for ONE feature, to see how testing is structured

Output of L2: you know which file owns which concern. "Auth is in `src/auth/`, broken into `routes.py` (HTTP layer), `service.py` (business logic), `models.py` (DB). They use SQLAlchemy ORM."

### L3 — Deep Dive (only when needed)

Goal: solve a specific problem.

Read:
- The exact file(s) relevant to the user's question
- Tests for the area you're modifying
- Closely related files (the function being called, the type being passed)

L3 happens **on demand**, driven by a real question. Never as preparation.

## Dispatch a Subagent for L1/L2 — MUST for Large Repos

For repos >100 files or when the user is asking an open-ended exploratory question, **don't burn your main context on exploration**. Dispatch a subagent:

```
Task: "Explore <repo> at <path>. Run L1 and L2 from incremental-context-building.
Return a 200-word summary covering:
- Stack and primary frameworks
- Entry point and overall architecture
- Where <user's area of interest> lives
- Any non-obvious gotchas you noticed
Do not return file contents — only the summary."
```

The subagent burns its own context, returns a tight summary, and your main thread stays focused on the actual task.

See `[[dispatching-parallel-agents]]` and `[[lean-context]]` for more.

## Slicing Files — Use offset/limit

Even at L3, you rarely need the full file. The Read tool supports `offset` and `limit`:

- Top of a 2000-line file → `offset: 0, limit: 100` first to see imports + top-level declarations
- Searching for a symbol → use Grep to find the line, then Read with `offset: <line-30>, limit: 60`

## Red Flags

- User asks "how does X work?" → you Read 20 files before writing anything. WRONG. Find the file that defines X (Grep), Read it, follow its references on demand.
- You Read a file "to get a feel for the codebase" without a specific question. WRONG — that's L1's job, and L1 doesn't read files, it reads metadata.
- Your context is 50% "let me explore" file contents and 0% actual work. Restart the approach.
- You Read all 14 files in a directory because they're "related". They might be — but you only need the one that answers your current question.
- You skipped L1 because "I roughly know what kind of project this is". Knowing it's a "Python web app" is not knowing what THIS project does.

## Examples

### Good

User: "Fix the bug where logging in with an unverified email crashes the server."

```
L1: Glob src/**, read package.json. → Express + Prisma + TypeScript. Probably /api/auth.
L2: Read src/api/auth/login.ts. → Sees a route handler calling AuthService.login.
L3: Read src/services/auth.ts where login() is defined.
   → Find the crash: user.emailVerified is undefined when account exists but unverified.
   → Read the test file src/services/auth.test.ts to mirror style.
   → Fix + test.
```

Files read: ~4. Token cost: ~12K.

### Bad

Same user, bad approach:

```
Glob **/*.ts
Read 25 files into context "to understand the codebase"
Then start looking for the auth bug across all that code
```

Files read: 25. Token cost: ~80K. You can't see the forest for the trees, and the actual bug is in 1 of those 25 files.

### Good — exploratory question, use subagent

User: "Is this codebase using any deprecated APIs?"

```
Dispatch subagent:
  "Audit <repo>. Run L1/L2 from incremental-context-building.
   Then Grep for deprecation patterns:
     - JS/TS: 'deprecated' in comments, removed React APIs (componentWillMount, etc.)
     - Python: __future__ flags, removed stdlib modules
   Return a list of files + line numbers and which APIs are deprecated."

Subagent returns: "Found 4 instances: ..."
Main thread acts on the summary.
```

Main context spent on exploration: ~0. Main context spent on action: ~5K.

## Special Cases

- **Small project (<20 files)**: skip the layers, just read everything. Overhead of being incremental exceeds the cost.
- **Monorepo**: do L1 on the root, then L1 again on the specific sub-package. Treat each package as its own project.
- **Vendored code / node_modules / target/**: don't explore. Almost never relevant.
- **Generated code**: identify and ignore (e.g., `*.pb.go`, `*.generated.ts`, `dist/`). Read the source it generates from.

## See Also

- `[[lean-context]]` — read slices, compress aggressively.
- `[[dispatching-parallel-agents]]` — push exploration off the main thread.
- `[[root-cause-tracing]]` — once you've narrowed to a file, trace the bug along the call chain instead of reading more files.
