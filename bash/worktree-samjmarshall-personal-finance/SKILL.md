---
name: worktree
description: Create, list, and tear down per-branch git worktrees, each with an isolated Neon database branch and a portless dev URL, so multiple branches can be worked in parallel without DB or dev-server collisions. A worktree is named for its branch and can be optionally tagged with a GitHub issue number. Use when the user says "spin up / create a worktree for <branch>", "clean up the worktree", "list worktrees", invokes /worktree, or wants parallel isolated dev environments.
model: sonnet
effort: low
---

# Worktree

Manage the lifecycle of per-issue git worktrees. All state-changing logic lives
in the bundled `worktree.sh`; this skill only routes the subcommand, opens the
editor, and summarizes the result. Do not improvise around the script — it is
the deterministic, idempotent contract.

## Quick start

```
/worktree create drag-and-drop-categories       # provision + open a worktree for this branch
/worktree create drag-and-drop-categories 142    # …tagged with issue #142 → branch 142-drag-and-drop-categories
/worktree list                                   # show all worktrees
/worktree cleanup 142                            # tear down by issue# (guards against unsaved work)
/worktree cleanup drag-and-drop-categories       # …or by branch name
/worktree cleanup --merged                       # sweep all merged/closed worktrees
```

## How it works

A worktree lives at `.worktrees/<branch>`, where `<branch>` is a DNS-safe slug of
the given name, optionally prefixed with an issue number (`<issue#>-<slug>`). The
directory name doubles as the portless hostname prefix
(`<branch>.personal-finance.localhost`) and the Neon branch name
(`local/<branch>`). The Neon branch is provisioned by the `post-checkout` hook on
create and reaped by `teardown.yml` on branch delete — this skill never touches
the Neon API itself.

## Workflow

1. Parse the argument string into `<subcommand> <args>`. If empty or unknown,
   run `bash .claude/skills/worktree/worktree.sh --help` and stop.
2. Run the script, streaming its output:
   `bash .claude/skills/worktree/worktree.sh <subcommand> <args>`
3. **On `create` success only:** open the editor window with
   `code <WORKTREE_DIR>` (read `WORKTREE_DIR=` from the script's output).
4. Summarize for the user: branch, worktree path, `DEV_URL`, Neon branch
   (`local/<branch>`), and the next step:
   `cd <WORKTREE_DIR> && claude` (then `make start` for the dev server).
5. On any failure, surface the script's error verbatim and stop. No auto-retry,
   no calling the Neon API by hand, no force-removing on your own initiative.

No handoff doc or issue primer is written — the developer pulls issue context
themselves once `claude` is running in the worktree.

## Guardrails

- `create` requires `.env` in the main worktree (`make env_pull` if missing) and
  must run from the repo root, not a linked worktree. The script enforces both.
- `cleanup` refuses to remove a worktree with uncommitted changes or unpushed
  commits. Only pass `--force` if the user explicitly confirms the work is
  disposable.
- A never-pushed branch never triggers `teardown.yml`, so its Neon branch can
  orphan. If that matters, push the branch first or run
  `scripts/neon-branch.sh delete --all` periodically.
- Per CLAUDE.md, never run `make`/`yarn` verification here — that flows through
  `@agent-codebase-verification`.

## Verifying changes to this skill

The mutating paths touch real Neon branches (never mocked). To verify:

- **Automated:** `worktree.sh create <name> --dry-run` must print the resolved
  branch (`<slug>`, or `<issue#>-<slug>` when an issue number is passed), worktree
  dir, Neon branch, and dev URL with no mutation. Run `shellcheck worktree.sh` if
  available.
- **Manual smoke:** `create` a throwaway branch → confirm worktree, `.env`, Neon
  branch, dev URL, and `code` window → `list` shows it → `cleanup` blocks on a
  dirty file → `cleanup --force` removes it → `teardown.yml` reaps the Neon
  branch on delete.
- **Idempotency:** run `create <name>` twice; the second run must reuse, not
  duplicate or error.
