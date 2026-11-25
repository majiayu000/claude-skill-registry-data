---
name: long-task-callback
description: Run long jobs (training, benchmarks, builds, test suites, deployments, data jobs, child agents) under Long Task Callback (ltc) so they outlive this turn, and get woken in this same Claude Code session when they finish via a background `ltc wait`. Use instead of sleeping, polling logs, or leaving a job owned by the Bash tool whenever a command may take about a minute or longer. Also covers handling an `[ltc-status]` repair block and acknowledging `[long-task-callback]` results.
---

# Long Task Callback for Claude Code

LTC hands a long command to an independent OS task owner (launchd on macOS, systemd on Linux,
Task Scheduler on Windows) and queues a callback when it exits. In Claude Code you receive that
callback **in this live session** by running `ltc wait` as a background Bash command: Claude Code
wakes you when a background command exits, and `ltc wait` exits as soon as the callback is ready.

The full reference (all flags, platforms, recovery and goals) is in [REFERENCE.md](REFERENCE.md).
Read it only when you need details beyond this page. It is shared with other agents; where it
differs from this page about callback delivery, this page applies to Claude Code.

## When to use it

- Reliably done within 60 seconds → run it in the foreground once. No LTC.
- About a minute or longer, uncertain duration, or might need a second check → `ltc run` from the start.
- Never keep a job alive by polling it with `sleep`/`tail`, and never leave a long job owned by a
  `run_in_background` Bash shell: it dies with the session and is not recovered.

## The workflow

1. **Submit** (foreground; returns in a second or two):

   ```bash
   ltc run --cwd "$PWD" --task "train model" -- python train.py --config configs/exp.yaml
   ```

   stderr prints the task id, backend, log path, and a ready-made line:
   `ltc: Claude Code live callback: run in the background (run_in_background): .../ltc wait --queue-dir ... --task <id>`

   If it instead says the callback `arrives through the ltc channel`, this session was started with
   `ltc claude`: skip step 2. The callback is pushed into this session as a
   `<channel source="ltc">` event; handle it as in step 3.

2. **Wait** — run exactly that `ltc wait ... --task <id>` command with the Bash tool's
   `run_in_background: true`. Do not run it in the foreground (it blocks until the job ends), and do
   not poll its output. Then tell the user what is running and end your turn, or carry on with other
   work.

3. **Wake up** — when the job finishes, the background command exits and prints a callback:

   ```text
   [long-task-callback] <callback-id>
   Task: train model
   Result: finished; exit=0
   Files: <task dir>/ (attempt-1.log)
   Details: <path> (as needed | read before acting)
   Session: <this session id> (only)
   ```

   Read the background command's output, inspect the log and artifacts (read Details first when it
   says "read before acting"), decide `continue | stop_success | stop_blocked | ask_user`, then run
   the `ltc ack ...` command from the callback. ACK means "received and inspected", not "goal done".
   An exit code is process status, not proof that tests passed.

4. **Next step** — if you launch follow-up work, submit it with `ltc run` again and start a new
   background `ltc wait --task <new-id>`. Inspect existing processes and outputs first: delivery is
   at-least-once.

## Other entry points

- **Fresh child agent** (independent review, test authoring, a parallel fix):

  ```bash
  ltc agent claude --cwd "$PWD" --task "review parser" -- "Inspect parser.py and report concrete defects."
  ltc agent codex --template test --task "write parser tests" -- "Test the contract in docs/parser.md."
  ```

  Then background `ltc wait --task <id>` exactly as for `ltc run`. The child's result path is in the
  callback. A Claude child needs a standalone `claude` CLI that is signed in (`claude auth status`);
  the Claude desktop app's bundled CLI cannot authenticate on its own.

- **Work already owned elsewhere** (tmux, screen, Slurm, a script): add `ltc done` at its end.

  ```bash
  set +e; python train.py; status=$?
  ltc done --cwd "$PWD" --task "train model" --command "python train.py" --exit-code "$status"
  exit "$status"
  ```

  The callback id is not known in advance, so start a background `ltc wait` with no `--task`: it
  delivers the next unacknowledged callback bound to this session.

## Rules

- **Session binding is automatic** from `CLAUDE_CODE_SESSION_ID`. Never use `--last` or invent a
  session id. `ltc wait` refuses to run without a session.
- **One wait, one wake-up.** A wait exits after printing what it found; start a new one for the next
  task. Every unacknowledged callback of this session keeps coming back until you ACK it.
- **If the session closes**, nothing is lost: when no waiter is alive, the LTC daemon falls back to a
  headless `claude -p --resume <session>` from the session's original directory. That fallback needs
  a signed-in standalone CLI; otherwise the callback stays queued and the next `ltc wait` from this
  session (or `ltc status`) picks it up. After a live delivery, the daemon waits 30 minutes for the
  ACK before it falls back.
- `ltc wait` exists only for Claude Code. It refuses to run without `CLAUDE_CODE_SESSION_ID` and
  never touches callbacks bound to other agents.
- **Do not** call `claude -p --resume` yourself, add `--via-daemon`, or invent launch flags. Callback
  problems never change the task's own exit code unless the user asks for `--strict`.
- **Long objectives with several stages**: use `ltc goal start|check|ack` with a YAML plan file, see
  REFERENCE.md ("Goal acknowledgement"). Callback ACK never completes a goal.

## `[ltc-status]` blocks

If `ltc run`, `ltc agent` or `ltc done` prints JSON between `[ltc-status]` and `[/ltc-status]`, it is
addressed to you: fix the listed configuration issues yourself (do not hand routine setup back to the
user), run its `recheck_command`, then continue. Check `work.state` first — `task_persisted` or
`callback_queued` means the work already exists: repair around that id and **do not submit it again**.
For an explicit check: `ltc doctor --agent claude --session "$CLAUDE_CODE_SESSION_ID"`.

## Install and verify

```bash
python3 -m pip install "git+https://github.com/lz59970062/long-task-wakeup.git"
ltc setup --force --enable --now
ltc doctor --agent claude --session "$CLAUDE_CODE_SESSION_ID"
```

Useful commands: `ltc status` (unacknowledged callbacks), `ltc cancel --id <id>`,
`ltc retry --id <id>` (re-deliver a result without rerunning the task),
`tail -f <task log>` when the user asks to watch progress.
