---
name: worktree
description: "Create a git worktree under .agents/worktrees/ named for the branch, with the pm store wired in and dependencies installed, for an isolated parallel checkout. Skip in-place edits that need no isolation."
argument-hint: "<target-branch> [base-branch]"
allowed-tools: Bash, Read, Glob, Grep
disable-model-invocation: true
---

Create, reuse, validate, or safely prune a managed worktree through the shared engine.
Never reproduce Git-path, symlink, pointer, reservation, or cleanup logic in the skill.

Arguments: $ARGUMENTS
- `<id>`: stable kebab-case plan/item id (required)
- `[base-ref]`: explicit base branch/ref (required when intent is ambiguous)

## Setup

Resolve the repository root and use the shared engine:

```bash
root="$(git rev-parse --show-toplevel)" || exit 1
engine="$HOME/.config/ai/lib/worktree.mjs"
```

Fetch an explicitly remote base before `ensure`; do not silently fall back after a
failed fetch. Local-only refs may be passed directly.

```bash
git fetch origin <base-ref>
node "$engine" ensure --root "$root" --id <id> --base <base-ref>
```

The JSON result is authoritative and contains `base_branch`, immutable `base_commit`,
immutable `start_commit`, `branch`, `worktree`, and `execution_root`. `ensure` reuses an exact branch/path match,
creates a reservation before Git mutation, initializes the main `tasks/` and `plans/`
stores, wires only those directories into the worktree, creates a real local `state/`,
and updates Git-common excludes. A legacy `ROADMAP.md` returns `migration_required`
before creating PM directories.

## Finish setup

Run dependency installation, `.worktreeinclude` copying, and the project baseline from
the returned `execution_root`. Prefer lockfile-based installs. A failed install or
baseline is reported; never hide it.

Report:
- execution root and branch;
- base ref and 40-character base commit;
- created versus reused;
- shared `tasks/plans` and local `state` status;
- copied files, dependency result, and baseline result.

## Existing plan operations

```bash
PM_SESSION_TOOL=<claude|codex> PM_SESSION_ID="<exact id>" node "$engine" resolve-session --root "$root" --tool <claude|codex>
PM_SESSION_TOOL=<claude|codex> PM_SESSION_ID="<exact id>" node "$engine" ensure-session --root "$root" --tool <claude|codex>
PM_SESSION_TOOL=<claude|codex> PM_SESSION_ID="<exact id>" node "$engine" bind-session --root "$root" --tool <claude|codex> --plan <plan-path>
PM_SESSION_TOOL=<claude|codex> PM_SESSION_ID="<exact id>" node "$engine" unbind-session --root "$root" --tool <claude|codex>
node "$engine" resolve-current --root "$root"       # launcher/checkout projection only
node "$engine" ensure-current --root "$root"        # explicit legacy maintenance only
node "$engine" assert-root --root "$root" --plan <plan-path>
node "$engine" sync-state --root "$root" --plan <plan-path>
node "$engine" validate --root "$root"
node "$engine" validate --root "$root" --all  # repository-wide ownership audit
```

Adoption always creates or reuses a dedicated worktree; the main checkout is never a
plan execution target. `--base` is the human-readable historical-base label.
`--base-commit` optionally pins an older 40-character diff base while requiring it to
remain an ancestor of the base ref tip and target/source HEAD. `--start` controls only
the source of a newly created adoption branch; existing callers that pass only `--base`
still start at its resolved commit.

```bash
node "$engine" adopt --root "$root" --plan <plan-path> --base <base-ref> \
  [--base-commit <40-char-oid>] [--start <ref-or-oid>] \
  [--branch <branch>] [--path <managed-path>] [--select]
```

Candidate discovery scans only Git-registered non-main worktrees whose local
`state/current.txt` exactly names the legacy plan. Zero candidates creates new topology
only when branch/path are unoccupied; one candidate is reused without changing its
branch or HEAD; multiple candidates stop before writes. Explicit branch/path options
may confirm the unique candidate but never claim a pointerless checkout, and `--start`
is rejected for candidate reuse. Dirty main project files block only new creation, not
reuse of the exact candidate.

Prompt adapters call `ensure-session` with a strict tool namespace and exact, unsanitized
session id. A valid binding resolves its exact canonical plan; without a binding, only a
non-main checkout whose local pointer resolves back to itself may supply plan context.
An unbound main checkout is always plan-free: its `current.txt` is launcher-only and is
never an implicit session owner. `ensure-session` may normalize an unambiguous legacy plan
only from that non-main local checkout. Ambiguous, dirty, detached, occupied,
foreign-owned, malformed, or staged-residual states remain typed failures. Direct
`resolve-session` and `resolve-current` remain physically read-only.

Session binding files are ephemeral and private. Their identity is the strict tool,
canonical-main-root digest, and exact-session-id digest; bindings for the same session in
two repositories cannot share a file or lock. Binding loss returns `unbound`, never a
launcher fallback. `ensure-session` prunes only the exact stale binding after rechecking
its bytes under the per-binding owner lock.

Adoption serializes reservation → PM-store → target/main current through token-owned
directory locks. Successful handoff removes its reservation last and reports topology
`created|reused` plus `adopted_selected|adopted_parked`; a parked result preserves the
newer main selection while the target remains the valid plan owner.

## Cleanup

Use explicit lifecycle commands. Cancellation removes only a clean, commit-free,
unowned provisional worktree. Terminal prune refuses a dirty/current/mismatched target
and keeps the branch.

```bash
node "$engine" cancel-provisional --root "$root" --id <id>
node "$engine" prune --root "$root" --provisional --id <id>
node "$engine" prune --root "$root" --plan <terminal-plan-path>
```

`validate` lists clean provisional reservations separately and fails on abandoned
dirty/committed/current/missing worktrees, incomplete ownership handoffs, invalid
mappings, and orphan reservation stage/temp artifacts. Provisional prune is the same
safe operation as cancellation; it never removes a current, dirty, committed, or
plan-owned worktree. Untouched detection compares HEAD with reservation `start_commit`
(`base_commit` only for legacy reservations). Terminal prune derives the branch/worktree from a `done` or
`dropped` plan under the PM lock; a caller-supplied terminal flag is never trusted.

Never call `git worktree remove --force` by default. `--force` is explicit-user-only.

## Rules

- Do not create managed worktrees outside `.agents/worktrees/`.
- Do not hand-edit `.agents/tasks`, plan mappings, reservations, or current pointers.
- Hooks use `ensure-session` only. It may perform the one lock-protected checkout-local
  lazy adoption described above; hooks never invoke raw topology or lifecycle commands.
- **Sandbox**: Claude uses `dangerouslyDisableSandbox`; Codex uses a workspace-write
  session that includes `.agents/worktrees`.
