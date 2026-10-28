---
name: panel
description: Convene a panel of agent CLIs (grok, claude, codex, agy) on a prompt or a code review, then report one consensus grouped by how much they agree.
disable-model-invocation: true
argument-hint: "A prompt, or a review scope like 'review since main'"
allowed-tools: "Bash(grok *) Bash(claude *) Bash(codex *) Bash(agy *)"
compatibility: "Needs at least one of the grok, claude, codex, or agy CLIs on PATH"
model: sonnet
effort: medium
---

# Panel

Put one task in front of four agent CLIs (`grok`, `claude`, `codex`, `agy`) run
each in its own subagent, headless, then report a single consensus grouped by how
much the panel agrees.

Each CLI runs as its own latest/default model. **Never pass `--model` to any of
them.** The point of the panel is four independent models; pinning a model defeats it.

Two task shapes:

- **Prompt**: the user's text goes to all four, unchanged.
- **Review**: pin one diff scope and tell all four to review it, read-only, same scope each.

## Process

### 1. Read the task and pick the shape

- **Review** when the user asks to review a branch, PR, WIP, or "review since X".
  Pin the fixed point the way `code-review` does: the diff is
  `git diff <fixed-point>...HEAD` (three-dot, against the merge-base), default
  `main` when the user names none. For uncommitted work in progress, drop the `...HEAD`
  so the diff also covers staged and unsaved changes. Confirm the ref resolves
  (`git rev-parse <fixed-point>`), record `git rev-parse HEAD`, and confirm the diff is non-empty **before** fanning out, 
  a bad ref should fail here, not inside four subagents.
- **Prompt** otherwise; the user's text is the task, passed word for word.

Write the one task string now. Every CLI receives the identical string, so the four
results compare cleanly. Start it with this line, so a panelist never convenes its own
panel when the task mentions panels, panelists, or other CLIs:

> You are one panelist. Answer the task below yourself, directly. Do not run a panel, launch another agent CLI, or start subagents.

`$SCRATCH` is the session's scratchpad directory where the harness has one, otherwise
one `mktemp -d`; hand subagents its absolute path, since they do not share your shell.
Save the string to `$SCRATCH/panel-task.txt` with the file-write tool (where the harness
has none, a quoted heredoc: `cat > "$SCRATCH/panel-task.txt" <<'PANEL_EOF'`). Three of the
launch rows then read the file and never contain the task's words, so a guard hook that
reads the command (task text that names `git commit`, say) cannot block the launch.

### 2. Check who is on the panel

Run `command -v` for each of `grok`, `claude`, `codex`, `agy`. Drop any that is
absent and record it for the final report. If fewer than two remain, there is no
consensus to form: say which are missing and stop.

### 3. Fan out: one subagent per CLI, in parallel

Spawn one subagent per present CLI, all in a single message so they run at once (in
Claude Code with this plugin installed, `subagent_type=leek-skills:panelist`: a small,
cheap wrapper, since the thinking happens inside the CLI it runs; in Codex, `spawn_agent`
per CLI, then `wait_agent` on all of them). Give each subagent
the path of the **same** task file and this brief:

- **Launch with literal paths only.** Worktree isolation refuses a command whose words
  are computed at runtime (`$(cat …)`, `$TASK`, `$PWD`), since it cannot prove the
  command stays inside the worktree. So write every path out in full: `TASK_FILE` in the
  rows is the task file's absolute path, and `WORKTREE` is the output of `pwd`, taken in
  its own earlier call. `claude` and `codex` read the task on stdin, and `grok` reads it
  with `--prompt-file`. `agy` has no file or stdin form, so its row carries the task text
  inline, as one single-quoted literal: copy the file's text in, writing each `'` as `'\''`.
  Single quotes stop every expansion, so a backtick or `$` in the task stays text. Run
  your CLI **once**, headless, from the repo root, using its row below. Add no
  `--model`; keep the row's flags as written. If a guard still refuses the launch, that
  is a launch-form problem, not a CLI error: say which word it refused and fix that.
- **Run every CLI detached: never let one time out.** These agent CLIs take many
  minutes, and a slow model (codex at high reasoning is the usual culprit) will run past
  the Bash tool's 10-minute foreground ceiling and get killed mid-orientation, before it
  ever reports. Do **not** run the command in the foreground with a big timeout, 10 min
  is the hard max and it will be killed. Instead redirect the command's output to a
  scratch file and launch it with the Bash tool's `run_in_background: true`: append
  ` > SCRATCH/panel-<cli>.out 2>&1` to the row's command, with `SCRATCH` written out as
  its absolute path (keep the row's `<` redirect).
  Your turn pauses and you are re-invoked automatically when the CLI exits; then read the
  scratch file and distill it. Background runs have no timeout; this is what guarantees
  nothing is cut off. Where the shell tool has no background mode and rejects `&` (Grok
  CLI), run the command in the foreground, still redirected, with the tool's timeout
  parameter set to its maximum (for example `timeout: 900000`), never its default.
- **Wait with one call, never poll.** No `sleep`, `ps`, `pgrep`, or repeated reads of
  the output file while the CLI runs: each check spends a turn, and the turn cap ends the
  subagent while its CLI is still running.
- Distill the output into a short, normalized result. For each point the CLI makes,
  capture three things: a one-line **claim**, a **location** (`file:line`, or
  `general`), and a one-line **reason**. Drop the CLI's logs, thinking, and prose.
- Return `{ cli, status, points[] }`. `status` is `responded`, or `errored` with a
  one-line cause. Return the object only, no narration.

Headless commands (`TASK_FILE` and `WORKTREE` are absolute paths written out in full;
`< /dev/null` stops a CLI that does not read the task on stdin from blocking on it):

| CLI | Command |
|---|---|
| `claude` | `claude -p --dangerously-skip-permissions < TASK_FILE` |
| `codex` | `codex exec --dangerously-bypass-approvals-and-sandbox --cd WORKTREE - < TASK_FILE` |
| `agy` | `agy --dangerously-skip-permissions --print-timeout 30m -p '<task text>' < /dev/null` |
| `grok` | `grok --prompt-file TASK_FILE --always-approve < /dev/null` |

In **review** shape, the task string is this brief. Name the pinned diff from step 1 in
plain words, with **no backticks**, so nothing is left for a shell to expand:

> Review the change from git diff FIXED-POINT in this repository. Read the diff and any
> files you need. Report concrete findings only, for each, a one-line claim, the
> file:line, and a one-line reason. Review only; do not modify any file. Be concise.

**Keep review read-only.** For a committed scope, dispatch each panelist with
`isolation: "worktree"` where the harness offers it, so a stray write never reaches the
user's tree; its brief first runs `git checkout --detach <step 1's HEAD sha>`, since the
worktree may start from another base. A worktree left with uncommitted changes means
its CLI wrote: name both. For WIP scope, or without isolation, save `git status --porcelain` and `git diff`
as the baseline before fanning out, and compare after every subagent returns. A path
the CLIs changed that was clean in the baseline: revert it (`git checkout -- <path>`,
delete new files) and name that CLI. A path that was already dirty holds the user's
unsaved work: report it and leave it as it is. This isolation or tree check (not a
per-CLI flag) is what enforces review-only.

Per-CLI notes: read-only options and their traps, structured-output flags,
absent-vs-errored, auth: live in
[`references/cli-invocations.md`](references/cli-invocations.md). Read it only when a CLI
misbehaves or the panel roster changes.

### 4. Cluster into consensus

First check the panel had a quorum: at least two CLIs must have **responded**, not just
been present. With fewer, there is no consensus: report the single result plainly and
say the panel was short, with the step 5 ping.

Collect the results. Only a returned `{ cli, status, points[] }` object is a result: a
panelist pauses while its CLI runs, and a notification without that object is interim,
so end the turn with no reply and wait for the next one. Match points that make the same claim, even when worded differently
or aimed at the same area. Grade each cluster by the share of the responders (`N`) that
raised it, and state `N` so a grade is never read as more agreement than it holds:

- **Unanimous**: all `N`.
- **Majority**: more than half, but not all.
- **Split**: exactly half (a tie; only when `N` is even).
- **Lone**: fewer than half.
- **Conflict**: CLIs directly disagree on the same point.

Clustering is a judgement call. When two points are plausibly the same, join them; a
borderline join that lifts a point to a higher grade is the whole value of the panel.

### 5. Report the consensus

Print the clusters, most-agreed first, under `## Unanimous`, `## Majority`, `## Split`,
`## Lone`, `## Conflict` (skip any that are empty). One line per point: the **claim**,
its **location**, the CLIs that raised it in brackets, e.g. `[claude, codex, grok]`, 
and its one-line **reason**. For a Conflict, state both sides and who holds each.

In review shape, where the host has `ReportFindings`, report the clusters through it
instead, in one call, most-agreed first: `summary` the claim, `file`/`line` the location,
`failure_scenario` the reason plus the CLIs in brackets, `category` the grade, `verdict`
`CONFIRMED` for Unanimous or Majority and `PLAUSIBLE` below that. Print as markdown only
what it cannot carry: `general` points and Conflicts. Otherwise print every cluster.

Then a one-line summary: how many points at each grade, the responder count `N`, and any
CLI that was absent or errored. Ping the user that it is ready (`PushNotification`
where available, otherwise the report itself is the signal).

Close with a **Recommended next steps** block:

1. **Fix list**: every point at every grade, Unanimous through Lone, as one checklist. Do not
   curate: a Lone finding is a real finding until verified otherwise. For a Conflict, list both
   sides and say which one the code supports. After `ReportFindings`, the reported
   findings are the list; name their count instead of repeating them.
2. **Offer the shortcut**: ask whether to verify and apply the whole list as one commit, naming
   the count, e.g. "Reply *fix all* to verify and apply all 11 points."

On *fix all*, work every point: verify each against the code, apply the ones that hold, and
report the ones that do not with a one-line reason. Never apply only the confident subset and
hand the rest back as "weigh individually"; the user asked for the panel so they would not have
to re-adjudicate it. Ask only about a point that conflicts with a recorded decision.

## Safety

Headless mode auto-approves every tool, so each CLI *could* write files even though the
brief says review only. Two guards, in order: run the panel on a clean working tree, and
in review shape isolate or revert stray writes per step 3. Per-CLI read-only flags exist
but behave inconsistently, `codex --sandbox read-only` works, `agy --mode plan` hijacks
the task into planning, and `grok`'s profile name is machine-specific, so step 3, not a
flag, is what enforces read-only. See the references file.
