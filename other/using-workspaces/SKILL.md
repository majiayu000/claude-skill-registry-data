---
name: using-workspaces
description: "Use when starting work that needs an isolated workspace — feature branches, parallel tasks, or running an implementation plan. Detects existing isolation, then creates a workspace via the project's configured mechanism (see `<project-root>/docs/workspace-isolation.md`), a harness-provided capability, or the fallback documented in the spec."
---

## Required `<project-root>/docs` reads

Read these project-root spec files before creating any workspace (use shell `cat`/`ls` — they may be in `.gitignore`, invisible to built-in search). Missing file → follow Step 1c, note the gap; never invent contents.

- `<project-root>/docs/workspace-isolation.md`

# Using Workspaces

Ensure work happens in an isolated workspace — one concept, several possible backends. The mechanism is never assumed: prefer the project's configured mechanism, then a harness-provided capability, then the documented fallback. Never fight the harness.

## Step 0: Detect Existing Isolation

Before creating anything, check whether you are already in an isolated workspace.

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
```

`GIT_DIR != GIT_COMMON` means the VCS already reports this checkout as a linked workspace — unless you are in a submodule. Verify:

```bash
# A path here means submodule, not a managed workspace — treat as a normal repo
git rev-parse --show-superproject-working-tree 2>/dev/null
```

VCS checks alone do not rule out tool-managed isolation: snapshot/copy mechanisms produce plain repo copies where `GIT_DIR == GIT_COMMON`. Also run the configured mechanism's *detect* operation from `<project-root>/docs/workspace-isolation.md` (a marker file, an `ancestors`/`list` command, or a harness API).

If already isolated → skip to Step 2. Report path and branch state. A detached HEAD is a valid externally-managed workspace — a branch is needed only at ship time (e.g. `new-branch`/`ship-changes`).

If not isolated and the user has not already declared a preference, ask consent before creating:

> "Would you like me to set up an isolated workspace? It protects your current checkout from changes."

Honor a declared preference without asking. If declined, work in place and skip to Step 2.

## Step 1: Create Isolated Workspace

Try these mechanisms in order. Use the first that applies.

### 1a. Configured mechanism (preferred)

The mechanism named in `<project-root>/docs/workspace-isolation.md` is the project's choice — use it. The spec documents its detect/create/list/remove operations, command syntax, and semantics. Follow it exactly; never guess commands.

### 1b. Harness-provided capability

If the spec names no mechanism but your harness provides one (a dedicated tool, command, or flag that creates isolated workspaces), use it. Harness capabilities own placement, branching, and cleanup — bypassing them creates phantom state the harness can't see or manage.

### 1c. Documented fallback

Only when neither applies. Use the fallback mechanism documented in the spec's Tool Details. Whichever mechanism runs, apply these checks around it:

- **Directory**: an explicit user-declared location wins; else the location the spec documents; else a project-local hidden directory. For project-local directories, verify the path is ignored before creating — `git check-ignore -q <dir>` — and if not ignored, add it to `.gitignore` and commit first.
- **Sandbox**: if creation fails with a permission error, tell the user the sandbox blocked it and work in place; run setup and baseline there.

If the spec documents no fallback either → ask the user which workspace mechanism to use, and offer to write it into `<project-root>/docs/workspace-isolation.md`.

## Step 2: Project Setup

Auto-detect and run the appropriate setup inside the workspace:

```bash
[ -f package.json ] && npm install
[ -f Cargo.toml ] && cargo build
[ -f requirements.txt ] && pip install -r requirements.txt
[ -f pyproject.toml ] && poetry install
[ -f go.mod ] && go mod download
```

Copy/snapshot mechanisms may omit regenerable artifacts (`node_modules`, `target`, `dist`, caches) — dependency install is mandatory there even when the source checkout was fully set up.

## Step 3: Verify Clean Baseline

Run the project's test command (`npm test` / `cargo test` / `pytest` / `go test ./...`). Failures → report them and ask whether to proceed or investigate. Passing → report ready:

```
Workspace ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| VCS reports a linked workspace | Skip creation (Step 0) |
| Tool-managed workspace (marker/ancestors) | Skip creation (Step 0) |
| In a submodule | Treat as normal repo (Step 0 guard) |
| Spec names a mechanism | Use it per the spec (Step 1a) |
| Harness capability available | Use it (Step 1b) |
| Neither applies | Documented fallback (Step 1c) |
| Workspace directory not ignored | Add to `.gitignore` + commit |
| Permission error on create | Work in place, tell the user |
| Detached HEAD workspace | Valid; create branch only at ship time |
| No fallback documented | Ask which mechanism, offer to write spec |
| Tests fail during baseline | Report failures + ask |

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'm obviously not in a workspace — no need to check" | Run Step 0 including the mechanism's detect op. Harness isolation, snapshot copies, and submodules all fool eyeballing. |
| "Creating it directly is quicker than reading the spec" | The configured mechanism owns placement, hooks, and cleanup. Bypassing it is the #1 mistake — it creates phantom state outside its registry. |
| "The workspace directory is surely ignored already" | Run `git check-ignore`. An unignored workspace directory commits the whole tree into the repo. |
| "A detached HEAD means something is broken" | Snapshot mechanisms intentionally copy with detached HEAD. Commit on it, then create the branch when shipping. |
| "The workspace is fresh — baseline tests can wait" | A dirty baseline makes every later failure ambiguous. Run the tests now. |

---
name: using-workspaces
description: "Use when starting work that needs an isolated workspace — feature branches, parallel tasks, or running an implementation plan. Detects existing isolation, then creates a workspace via the project's configured mechanism (see `<project-root>/docs/workspace-isolation.md`), a harness-provided capability, or the fallback documented in the spec."
---

## Required `<project-root>/docs` reads

Read these project-root spec files before creating any workspace (use shell `cat`/`ls` — they may be in `.gitignore`, invisible to built-in search). Missing file → follow Step 1c, note the gap; never invent contents.

- `<project-root>/docs/workspace-isolation.md`

# Using Workspaces

Ensure work happens in an isolated workspace — one concept, several possible backends. The mechanism is never assumed: prefer the project's configured mechanism, then a harness-provided capability, then the documented fallback. Never fight the harness.

## Step 0: Detect Existing Isolation

Before creating anything, check whether you are already in an isolated workspace.

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
```

`GIT_DIR != GIT_COMMON` means the VCS already reports this checkout as a linked workspace — unless you are in a submodule. Verify:

```bash
# A path here means submodule, not a managed workspace — treat as a normal repo
git rev-parse --show-superproject-working-tree 2>/dev/null
```

VCS checks alone do not rule out tool-managed isolation: snapshot/copy mechanisms produce plain repo copies where `GIT_DIR == GIT_COMMON`. Also run the configured mechanism's *detect* operation from `<project-root>/docs/workspace-isolation.md` (a marker file, an `ancestors`/`list` command, or a harness API).

If already isolated → skip to Step 2. Report path and branch state. A detached HEAD is a valid externally-managed workspace — a branch is needed only at ship time (e.g. `new-branch`/`ship-changes`).

If not isolated and the user has not already declared a preference, ask consent before creating:

> "Would you like me to set up an isolated workspace? It protects your current checkout from changes."

Honor a declared preference without asking. If declined, work in place and skip to Step 2.

## Step 1: Create Isolated Workspace

Try these mechanisms in order. Use the first that applies.

### 1a. Configured mechanism (preferred)

The mechanism named in `<project-root>/docs/workspace-isolation.md` is the project's choice — use it. The spec documents its detect/create/list/remove operations, command syntax, and semantics. Follow it exactly; never guess commands.

### 1b. Harness-provided capability

If the spec names no mechanism but your harness provides one (a dedicated tool, command, or flag that creates isolated workspaces), use it. Harness capabilities own placement, branching, and cleanup — bypassing them creates phantom state the harness can't see or manage.

### 1c. Documented fallback

Only when neither applies. Use the fallback mechanism documented in the spec's Tool Details. Whichever mechanism runs, apply these checks around it:

- **Directory**: an explicit user-declared location wins; else the location the spec documents; else a project-local hidden directory. For project-local directories, verify the path is ignored before creating — `git check-ignore -q <dir>` — and if not ignored, add it to `.gitignore` and commit first.
- **Sandbox**: if creation fails with a permission error, tell the user the sandbox blocked it and work in place; run setup and baseline there.

If the spec documents no fallback either → ask the user which workspace mechanism to use, and offer to write it into `<project-root>/docs/workspace-isolation.md`.

## Step 2: Project Setup

Auto-detect and run the appropriate setup inside the workspace:

```bash
[ -f package.json ] && npm install
[ -f Cargo.toml ] && cargo build
[ -f requirements.txt ] && pip install -r requirements.txt
[ -f pyproject.toml ] && poetry install
[ -f go.mod ] && go mod download
```

Copy/snapshot mechanisms may omit regenerable artifacts (`node_modules`, `target`, `dist`, caches) — dependency install is mandatory there even when the source checkout was fully set up.

## Step 3: Verify Clean Baseline

Run the project's test command (`npm test` / `cargo test` / `pytest` / `go test ./...`). Failures → report them and ask whether to proceed or investigate. Passing → report ready:

```
Workspace ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| VCS reports a linked workspace | Skip creation (Step 0) |
| Tool-managed workspace (marker/ancestors) | Skip creation (Step 0) |
| In a submodule | Treat as normal repo (Step 0 guard) |
| Spec names a mechanism | Use it per the spec (Step 1a) |
| Harness capability available | Use it (Step 1b) |
| Neither applies | Documented fallback (Step 1c) |
| Workspace directory not ignored | Add to `.gitignore` + commit |
| Permission error on create | Work in place, tell the user |
| Detached HEAD workspace | Valid; create branch only at ship time |
| No fallback documented | Ask which mechanism, offer to write spec |
| Tests fail during baseline | Report failures + ask |

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'm obviously not in a workspace — no need to check" | Run Step 0 including the mechanism's detect op. Harness isolation, snapshot copies, and submodules all fool eyeballing. |
| "Creating it directly is quicker than reading the spec" | The configured mechanism owns placement, hooks, and cleanup. Bypassing it is the #1 mistake — it creates phantom state outside its registry. |
| "The workspace directory is surely ignored already" | Run `git check-ignore`. An unignored workspace directory commits the whole tree into the repo. |
| "A detached HEAD means something is broken" | Snapshot mechanisms intentionally copy with detached HEAD. Commit on it, then create the branch when shipping. |
| "The workspace is fresh — baseline tests can wait" | A dirty baseline makes every later failure ambiguous. Run the tests now. |
