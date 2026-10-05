---
name: loop
description: >-
  Work toward a goal on one branch with a team of workers: cut the goal's branch, give each
  ready task a worker on a child branch, merge each finished child up once its check passes,
  and hand the owner one command to land the goal's branch. Also lists and writes local task
  files. Use for "run the loop", "start the team", "dispatch workers", "fold", "land it".
---

# loop

A branch is the only unit of work. The loop is one way to repeat work until a goal is done;
it does not own the calendar.

1. **The goal gets a branch.** `dev-loop start <owner/repo> <type/slug>` cuts an ordinary branch
   from the base, for example `feat/snake-game`. This is the rig branch. Its worktree is
   `.claude/worktrees/rig-<type>-<slug>` in the checkout.
2. **Each task gets a child branch.** `dev-loop go` gives every ready task a worker (headless, or
   an OpenRig seat) in its own worktree, on a `type/slug-N` branch cut from the rig branch.
3. **Finished children merge up.** `dev-loop fold <owner/repo> N` merges a finished child into the
   rig branch. The control seat or any directed session may run it. It releases the worker's seat,
   runs the repository's check on the branch (a pass the worker recorded counts), and refuses a
   running or blocked worker, a dirty worktree, a branch that commits `.worker-*` files or
   OpenRig's managed context, and a conflict. It never touches the base.
4. **The rig branch lands once, by the owner.** `dev-loop close <owner/repo> --merge` (local) or
   `close --push` (GitHub) runs in the owner's terminal. It checks the rig branch head, writes
   `pr.md` with one `Closes #N` per folded task, and then merges locally or pushes the rig branch
   under its own name and opens one pull request. The title comes from the branch:
   `feat/snake-game` becomes `feat: snake game (#1, #2)`.

When every worker is folded, the control seat tells the owner once: which children merged into
the rig branch, where to read the diff (`git diff <base>...<rig branch>`), and the one command.

## Who runs what

| Verb | Who |
| --- | --- |
| `status`, `state` (the same facts as JSON), `plan`, `tasks` | anyone |
| `start`, `go`, `resume`, `pause`, `collect`, `fold` | a session or control seat on the owner's word |
| `close --merge`, `close --push` (professional), `finish`, `tidy --apply` | the owner, in a terminal; an agent is refused |
| `close --push` without `--ready` in a personal repository | the assistant may run it |

The header of `dev-loop` (the script) is the full verb table; this table follows it. Every lever
is also in the `ai` menu under a project's Development loop: the goal branch, each worker
branch under it (diff, report, open or release its seat, resume, merge up), dispatch, landing,
tasks and tidy. The menu is the owner's terminal, so it runs the owner verbs after asking.

## Setup, once per machine

`~/.config/dev-platform/repos.conf`: one line per repository, `owner/repo checkout-path
local|owner|bot [base-branch]`, separated by spaces or tabs. `new-repo --register` writes it.
`local` never touches GitHub. `owner` makes the two GitHub writes (`pr create` at close, `issue
close` at finish) with the owner's own `gh` login; `bot` uses the machine user's token.
`~/.config/dev-platform/brief.conf` sets `LOOP_STATE_DIR` (default
`~/.local/state/dev-platform/loop`). A project is named the same everywhere: `dev-loop` takes
`owner/repo`; `ai-work loop` takes `owner/repo`, the project id, or the checkout path.

## Local and GitHub, one motion

The steps above are the same for both. The differences:

- Tasks: `docs/tasks/<N>-<slug>.md` files on the base (local), or GitHub issues labeled
  `sprint-ready` (GitHub). `dev-loop tasks <repo> [list|next|new|check]` writes and checks local
  task files; the `intake` skill decides what they are.
- `start` fetches the base first only for GitHub.
- Landing: `close --merge` merges locally and moves the folded task files to `docs/tasks/done/`;
  `close --push` opens the pull request, and after the owner merges it on GitHub,
  `finish <owner/repo> <pr>` closes the folded issues and removes the rig branch.
- A professional repository gets the ghost check before anything reaches GitHub.

## Task conventions

Every task carries `Scope: <comma-separated path prefixes>` and `Depends on: #N, #M` or `Depends
on: none`. Only ready tasks with both lines are selected. Scopes must be pairwise prefix-disjoint
within one dispatch; dependencies must be done, or already folded into the rig branch.

The specification changes only through a spec task (`Labels: spec`). A build task may move the
status marker of the items it cites and any lock line, and nothing else under `docs/spec/`,
`docs/decisions/` or `docs/tasks/`; fold refuses the branch and shows the lines otherwise. A
worker that finds the spec wrong writes `.worker-blocked.md`, and the fix becomes a spec task.

## Workers

A worker has one task, one worktree, one branch. It commits, runs `hooks/check-once.sh` (which
records the passing tree), writes `.worker-pr.md` with the four template sections and `Closes
#N`, and stops. It never pushes, opens a pull request or comments. A worker that finds the fix
outside its scope, or the task already done, writes `.worker-blocked.md` and stops.

With `LOOP_SEAT_RIG=<running rig>`, dispatch gives each task an interactive seat in that rig's
`workers` pod (`dev-workspace add-worker`; `LOOP_SEAT_RUNTIME` claude or codex; a Codex seat takes
`LOOP_SEAT_ACCOUNT` or its native home) and records the rig, so fold can release the seat. A
blocked worker is never folded, so its seat stays until the owner or control seat releases it with
`dev-workspace remove-worker --rig <rig> --cwd <worktree>`. See `docs/rig-working-branches.md`.

## Other verbs

- `dev-loop status <owner/repo>`: steer, the rig branch, running workers, worker branches and their
  state, folded tasks, the pull request; with none open, the last rig branch that landed.
- `dev-loop collect <owner/repo>`: the CYCLE report, with seat workers counted.
- `dev-loop tick <owner/repo>` does what `go` does from a schedule, only when the steer says `go`.
  The steer is the gate: first word `go` or `pause`; a missing file means pause. Landing writes
  `pause`.
- `dev-loop tidy <owner/repo>`: read-only list of merged branches and clean, unused worktrees;
  `--apply` bundles every ref first, then deletes.

Writes to GitHub go through `scripts/ghx <owner/repo> <gh args>`, which picks the identity from
`repos.conf` and refuses merge, ready and review on every repository.

## Base and limits

The fourth `repos.conf` column pins the base. Without it, a personal repository uses its remote
default branch; a professional repository uses `develop`. An open rig branch keeps its recorded
base. One rig branch is open per repository at a time. `LOOP_WORKER_MAX_TURNS`,
`LOOP_WORKER_MAX_SECONDS` and `LOOP_WORKER_TOKEN_CEILING` bound workers; the token ceiling is a
prompt budget, not a spending cap. A quota failure stops the lane rather than switching accounts.
Worker models come from `bin/pstack-model`, which reads `~/.config/dev-platform/pstack-models.md`
when `/setup-pstack` wrote it and its own tier defaults otherwise (see `docs/models.md`).
