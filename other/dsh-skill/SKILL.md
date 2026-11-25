---
name: long-task-callback
description: Run long jobs (training, benchmarks, builds, test suites, deployments, data jobs, child agents) under Long Task Callback (ltc) so they outlive this turn, and get woken in this same DeepSeek Harness session when they finish through a background `ltc wait` job. Use instead of sleeping, polling logs, or leaving a job owned by the foreground shell whenever a command may take about a minute or longer. Also covers handling an `[ltc-status]` repair block and acknowledging `[long-task-callback]` results.
---

# Long Task Callback (ltc) for DeepSeek Harness

LTC hands a long command to an independent OS task owner (launchd on macOS, systemd on Linux,
Task Scheduler on Windows) and queues a callback when it exits. In DeepSeek Harness you receive
that callback **in this live session** by starting `ltc wait` as a DSH background job: DSH
notifies the conversation when a background job finishes, and `ltc wait` exits as soon as the
callback is ready.

The full reference (all flags, platforms, recovery and goals) is in [REFERENCE.md](REFERENCE.md).
Read it only when you need details beyond this page. It is shared with other agents; where it
differs from this page about callback delivery, this page applies to DeepSeek Harness.

## When to use it

- Reliably done within 60 seconds → run it in the foreground once. No LTC.
- About a minute or longer, uncertain duration, or might need a second check → `ltc run` from the start.
- Never keep a job alive by polling it with `sleep`/`tail`, and never start a long job with a plain
  foreground Bash call: it blocks the conversation and dies with the turn.

## The workflow

1. **Submit** (foreground; returns in a second or two):

   ```bash
   ltc run --cwd "$PWD" --task "train model" -- python train.py --config configs/exp.yaml
   ```

   stderr prints the task id, backend, log path, and a ready-made line:
   `ltc: DeepSeek Harness live callback: run as a background job (run_in_background: true): .../ltc wait --queue-dir ... --task <id>`

2. **Wait** — run exactly that `ltc wait ... --task <id>` command with the Bash tool's
   `run_in_background: true` (the `bash` tool's `run_in_background` argument). Do not run it in
   the foreground (it blocks until the job ends), and do not poll its output. Then tell the user
   what is running and end your turn, or carry on with other work. Start it right after the
   submission; the queue keeps the callback until a waiter appears.

3. **Wake up** — DSH notifies this conversation when the background job finishes. Read that job's
   output with the `job_output` tool (use the job id from the notification). It contains:

   ```text
   [long-task-callback] <task-id>-c1
   Task: train model
   Result: exited 0 · 2h 3m 32s
   From: run on systemd-user
   Files: <task dir>/ (attempt-1.log)
   Details: <path> (as needed | read before acting)
   Session: <this session id> (only)
   ACK after inspection: ltc ack <task-id>-c1
   ```

   Inspect the log and artifacts (read Details first when it says "read before acting"), decide
   `continue | stop_success | stop_blocked | ask_user`, then run the `ltc ack ...` command from
   the callback. ACK means "received and inspected", not "goal done". An exit code is process
   status, not proof that tests passed.

4. **Next step** — if you launch follow-up work, submit it with `ltc run` again and start a new
   background `ltc wait --task <new-id>`. Inspect existing processes and outputs first: delivery
   is at-least-once.

## Other entry points

- **Fresh child agent** (independent review, test authoring, a parallel fix):

  ```bash
  ltc agent dsh --cwd "$PWD" --task parser-review -- "Inspect parser.py and report concrete defects."
  ltc agent codex --template test --task parser-tests -- "Test the contract in docs/parser.md."
  ```

  Then background `ltc wait --task <id>` exactly as for `ltc run`. A DSH child runs
  `dsh --profile headless`; that profile uses `DEEPSEEK_API_KEY`, credentials restored in the
  headless profile or a provider route in `cordis.patch.yml`, not the desktop app's saved sign-in.
  If it cannot authenticate, the child callback reports the error — do not retry blindly. The child
  can write only inside `--cwd`, and nobody can approve an escalation.

- **Work already owned elsewhere** (tmux, screen, Slurm, a script): add `ltc done` at its end.

  ```bash
  set +e; python train.py; status=$?
  ltc done --cwd "$PWD" --task "train model" --command "python train.py" --exit-code "$status"
  exit "$status"
  ```

  The callback id is not known in advance, so start a background `ltc wait` with no `--task`: it
  delivers the next unacknowledged callback bound to this session.

## Rules

- **Sandbox**: in DSH's default `workspace-write` mode every `ltc` command that touches `~/.ltc` is
  denied (`Read-only file system`), including `ltc wait` and `ltc ack`. Retry that exact command once
  with `sandbox_permissions` and a `justification`, as DSH's shell tool describes, then pass them
  from the first attempt on later `ltc` commands in this session: a denied background `ltc wait` only
  tells you so after spending a wake-up. A denial is not a broken install, so do not run the
  `[ltc-status]` repair command for it, and do not move the queue.
- **After `--` comes one command, not shell code**: for `;`, `&&`, pipes or redirection use
  `-- bash -c '...'` (`ltc run --task check -- bash -c 'sleep 720; python3 report.py'`).
- **Heredoc scripts work**: input piped into `ltc run` (`-- python3 - <<'EOF'`) becomes the task's
  stdin. Without piped input the task's stdin is empty.
- **Session binding is automatic** from `DSH_SESSION_ID`. Never invent a session id. `ltc wait`
  refuses to run without a live session id.
- **One wait, one wake-up.** A wait exits after printing what it found; start a new one for the next
  task. Every unacknowledged callback of this session keeps coming back until you ACK it.
- **There is no headless fallback for DSH.** The daemon never opens a second writer for a DSH
  conversation, because DSH refuses to resume a desktop-preset session non-interactively. If this
  session closes before a waiter starts, the callback stays queued; it is delivered the next time
  this session runs `ltc wait`, or you can inspect it with `ltc status`.
- **Wait exit code 4 does not occur for DSH** (there is no headless resume to divert the callback).
  Exit code 3 means the wait timed out; the callback is still queued.
- **Do not** call `dsh --profile headless --session-id` yourself to pick up a callback, add
  `--via-daemon`, or invent launch flags. Callback problems never change the task's own exit code
  unless the user asks for `--strict`.
- **Long objectives with several stages**: use `ltc goal start|check|ack` with a YAML plan file, see
  REFERENCE.md ("Goal acknowledgement"). Callback ACK never completes a goal.

## `[ltc-status]` blocks

If `ltc run`, `ltc agent` or `ltc done` prints JSON between `[ltc-status]` and `[/ltc-status]`, it is
addressed to you: fix the listed configuration issues yourself (do not hand routine setup back to the
user), run its `recheck_command`, then continue. Check `work.state` first — `task_persisted` or
`callback_queued` means the work already exists: repair around that id and **do not submit it again**.
For an explicit check: `ltc doctor --agent dsh --session "$DSH_SESSION_ID"`.

## Install and verify

```bash
python3 -m pip install "git+https://github.com/lz59970062/long-task-wakeup.git"
ltc setup --with-dsh --force --enable --now
ltc doctor --agent dsh --session "$DSH_SESSION_ID"
```

`ltc setup --with-dsh` installs this skill under `${DSH_HOME:-~/.dsh}/skills/long-task-callback` and
records the `dsh` launcher for the daemon. If the desktop app did not put `dsh` on `PATH`, pass
`--dsh-bin "/Applications/DeepSeek Harness.app/Contents/Resources/runtime/cli/bin/dsh"`.

Useful commands: `ltc status` (unacknowledged callbacks), `ltc cancel --id <id>`,
`ltc retry --id <id>` (re-deliver a result without rerunning the task),
`tail -f <task log>` when the user asks to watch progress.
