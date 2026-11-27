---
name: test-queue
description: Use before running tests, typechecks, commits or pushes with heavy git hooks or any other resource-heavy command in a repo that has a configured queue (check with `tq queues`), or when a Bash command was denied with "Queue <name>". Runs the command through a machine-wide first-come-first-served queue so only one session at a time loads the laptop.
---

# test-queue

Several Claude sessions running test suites at once fill RAM and swap, and the
laptop grinds to a halt. `tq` is a machine-wide queue: a command run through it
waits until it is first in line, then runs. A PreToolUse hook on Bash refuses
commands that should be queued but aren't, in every session and teammate.

## Using it

```bash
tq status                                  # who is running, who is waiting
tq run <queue> -- <command...>             # wait for a turn, run, release
tq run <queue> -- bash -c '<compound command>'
tq run -- <command...>                     # queue guessed from the command and cwd; runs directly if none applies
```

- When a Bash call is denied with `Queue <name>: …`, re-run the command the
  message gives you. It is the original command wrapped in `tq run`.
- If `tq status` shows the queue busy, run with `run_in_background: true`.
  Otherwise the Bash tool timeout can kill the wait, and the command loses its
  place.
- While waiting, `tq` prints its position and what's running every 30 s. When
  the run starts it prints `your turn after …`. The exit code is the command's.
- Keep each turn short: queue only the heavy part (tests, typecheck, push), not
  a whole sequence of edits and checks. Don't hold a turn while you think.
- Don't skip a run because the queue is busy, and don't work around the queue:
  no splitting a command to dodge the match, no `--no-verify`.
- `TQ_BYPASS=1 <command>` skips the hook. Use it only when the user says so in
  this session.
- A nested `tq run` of the same queue (a script that queues itself inside a
  queued run) runs straight through rather than deadlocking.

## What the hook catches

For each simple command in the Bash line (split on `&&`, `||`, `;`, `|`, `&`,
newlines and `$(…)`, looking inside `sh -c '…'`, past env assignments and
`timeout`/`nohup`/`env`/`time`), it works out the kinds of work and the
directory. `cd`, `git -C` and `--cwd` count toward the directory.

| kind | matches |
|---|---|
| `test` | `vitest`, `jest`, `mocha`, `pytest`, `bun test`, `playwright test`, `go test`, `cargo test`, `<pm> [run] test…`, `turbo [run] test…` |
| `typecheck` | `tsc` (not `--version`/`--help`/`--init`), `vue-tsc`, `<pm> [run] typecheck…`/`type-check`/`tsc`, `turbo typecheck` |
| `lint` | `eslint`, `biome`, `depcruise`, `<pm> [run] lint…` |
| `build` | `<pm> [run] build…`, `turbo build` |
| `git-push` | `git push` without `--no-verify` (pre-push hooks run the suites) |
| `git-commit` | `git commit` without `--no-verify`/`-n`/`--dry-run` (for repos whose pre-commit hook lints or typechecks) |

`<pm>` is bun, npm, pnpm or yarn; `bunx`/`npx`/`pnpx` are looked through.
Heredoc bodies, comment lines and quoted arguments (`grep 'bun test'`) don't
match. A command already run through `tq` is allowed. If the hook fails for any
reason, it allows the command rather than blocking Bash.

## Configuring queues

Queues are JSON files, read on every call, so edits apply immediately:

- `~/.config/ai-private/queue-*.json`: org queues. Keep the file in the org
  store as `config/queue-<name>.json`; `ai-memory install` links it here.
- `~/.config/test-queue/*.json`: personal queues.

```json
{
  "queues": {
    "web-tests": {
      "description": "what this queue protects, shown by tq queues",
      "slots": 1,
      "repos": ["~/code/web"],
      "kinds": ["test", "typecheck", "git-push"],
      "match": ["^make e2e\\b"]
    }
  }
}
```

- `repos`: matched by git common dir, so every worktree of a repo counts,
  wherever it lives.
- `kinds`: any of the kinds in the table above.
- `match`: extra regexes, tested against each simple command, for other heavy
  runs (builds, migrations, Docker-backed suites).
- `slots`: how many runs at once (default 1).

To add a repo or a kind of run, edit or add a file. No hook or skill change is
needed.

## Files

- `scripts/tq`: the queue, the hook (`tq hook`) and the classifier
  (`tq classify -C DIR -- 'command'`, for checking a pattern). Linked as
  `~/.local/bin/tq`.
- State: `~/.local/state/test-queue/<queue>/*.json`, one ticket per waiting or
  running command.
  - A ticket counts while its wrapper is the same live process (pid plus a
    start time read in a fixed locale and timezone).
  - It also counts while any process of the command's own process group is
    still running.
  - Tickets of dead processes are pruned, so a crash never blocks the queue.
  - If `ps` fails, nothing is pruned.
- Signals: the command runs in its own process group. SIGINT, SIGTERM or
  SIGHUP to `tq` is forwarded to the whole group. After 10 s (`TQ_GRACE`)
  whatever is left gets SIGKILL, and only then is the turn released. If `tq`
  itself is SIGKILLed, the queue stays held until the orphaned command ends,
  so heavy runs never overlap.
- The deny message wraps the command in your login shell (`$SHELL -c`), so
  zsh syntax and globs behave as they would in the Bash tool.
- `tests/test-tq.sh`: runs on temporary config, state and repos.
