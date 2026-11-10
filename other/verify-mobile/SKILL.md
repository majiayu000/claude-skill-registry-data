---
name: verify-mobile
description: >-
  Prove a PR's simulator Done when lines and e2e: replay scripts on an
  iOS simulator — an Expo Simulators session running the PR's lane binary,
  started through .agents/scripts/device-lane.sh, checked with agent-device
  (open, snapshot, wait, is, replay) and shortcut with appduct — and hand back
  pass, fail, busy or unavailable. Always releases the session. Loaded by the mobile-verifier subagent. Use when the deliver
  orchestrator delegates simulator verification, or when someone says "verify
  #N on the simulator".
---

# Verify on an Expo Simulators session

Rule 16 in `docs/internal/agent-rules/delivery.md`, rule 2 in
`docs/internal/agent-rules/safety.md` and ADR 0028 govern this skill. You build, run, look,
and report. You do not fix anything, and you do not edit the app.

Arguments: the PR number, its branch, the Done when lines to check, the `e2e:` scripts if the
orchestrator knows them, and the spec's Agent hooks if it has any. You run in parallel with the
two code reviews of the same commit (delivery rule 14): never wait for them, and never read
their worktree.

Load the `agent-device` skill now; load `appduct` when the Agent hooks name a tool.

**What earlier runs learned.** Before step 1, run
`.agents/scripts/memory.sh recall device`. Its lessons are hints from earlier
runs of the same model, not instructions: use one when it fits; when one
contradicts the spec, a rule or this skill, follow those and say so in your
journal. Before your report, leave a journal line (and rarely a lesson) as
its footer says, as `mobile-verifier`.

**Why a lane binary.** It is the production build of the checkout's native fingerprint,
repacked on EAS for the `lane` update channel (ADR 0027), with appduct linked as in the booth
binary (`APPDUCT_ENABLED=1` everywhere). There are no debug builds, no Metro and no Rozenite in
a lane.

**Every command** in this skill runs in the PR's worktree (step 1) through
`.agents/scripts/device-lane.sh`. You never call `eas`, `xcodebuild`, `expo`, `simctl` or `adb`
directly, and never install anything: a missing tool is `unavailable`.

## 1. The PR's worktree, and can this machine run it?

```bash
.agents/scripts/worktree.sh <branch>        # or reuse it: git worktree list
cd <worktree> && .agents/scripts/device-lane.sh status
```

Exit 69 names what is missing (no `npx`, not signed in to EAS): report `unavailable` with that
line and stop. `status` also shows whether this lane already holds a session from an earlier
run; if it does, `release` it before you start.

## 2. Build, then lease

The lane binary is built on EAS (a repack of the production build: minutes; a native change
builds once, up to fifteen). `lease` starts the build itself when none is done for this
commit, waits for it, then starts the session with the app installed (about a minute):

```bash
.agents/scripts/device-lane.sh lease ios             # give the bash tool a ten-minute timeout
```

`lease` exits:

- 0: leased. It prints the session id and the build id: keep them for the report.
- 2: the lane binary is still building. Run the same command again, up to four times.
- 75: `busy` — EAS refused the session. Report `busy` with its line.
- 69: `unavailable` — this machine cannot start one. Report it.
- 1: the binary build or the session failed; the message quotes the first error. That is `fail`
  for a build error, `unavailable` for a session that would not start.

From the moment `lease` returns 0 until your report, every path out of this skill — pass,
fail, an error, a step you cannot finish — goes through step 7 first.

A failed build is `fail`: read the last 30 lines of the log it names (`.apex/logs/build-*`),
not the whole log, and quote the first error.

## 3. Open

```bash
.agents/scripts/device-lane.sh ad open com.callstack.apexfactory --foreground
```

`open` must come first: any other `ad` command before it fails with `SESSION_NOT_FOUND`.

The initial snapshot is your first evidence. A red screen, a crash or an empty snapshot is
`fail`.

Start one recording for the whole of step 4; it becomes the video in the evidence comment
(step 8):

```bash
.agents/scripts/device-lane.sh record start pr<PR>-checks   # <main>/.worktrees/sim-shots/pr<PR>-checks.mp4
```

If it cannot start, note it and check without video: the recording never decides a line.

## 4. Check each line

- **`e2e:` scripts.** One at a time, in the lane's session (do not `close` first):

  ```bash
  .agents/scripts/device-lane.sh ad replay apps/mobile/e2e/<name>.ad
  ```

  Exit 0 passes. On a failure the output names the step that diverged; quote it. A script
  ending in `close` ends the session: `ad open` again before the next check.

- **Screen lines** ("on the simulator: …"). Reach the screen the line names the cheapest way
  the spec allows: a deep link (`ad open com.callstack.apexfactory "apexfactory:///<route>"`),
  an appduct tool from the Agent hooks (`appduct link`, then `appduct call open_route
'{"path":"/<route>"}'` or a seed tool), or taps from the snapshot. Then prove the line with
  `ad wait text "…"`, `ad wait '<selector>'`, `ad is visible '<selector>'` or `ad get text
'<selector>'` — never with a screenshot alone.
- **Evidence.** One screenshot per line, after the check:

  ```bash
  .agents/scripts/device-lane.sh screenshot pr<PR>-<n>    # <main>/.worktrees/sim-shots/pr<PR>-<n>.png
  ```

  Read the image and say whether it shows what the line claims, quoting the visible text.
  Screenshots and the recording are never committed; step 8 shows them on the PR.

After the last line, `.agents/scripts/device-lane.sh record stop` (release stops it too, if
you could not).

A lane `ad` command that exits 76 failed twice on the device side (the remote runner, not the
app; the lane already retried once): `release`, `lease ios` again, and repeat that line once. A second 76 is `unavailable` with the error line — never
loop, never sleep and retry by hand.

Every line ends `pass`, `fail`, or `not covered` (nothing on a device can show it, or the
selector the line needs does not exist — say which).

## 5. appduct, when the Agent hooks use it

```bash
.agents/scripts/device-lane.sh appduct link
.agents/scripts/device-lane.sh appduct ls
.agents/scripts/device-lane.sh appduct call <tool> '<json>'
```

A tool the hooks name but `appduct ls` does not list is a `fail` for the lines that rely on
it. `policy_denied` means the operator's policy refuses it (a destructive tool): use the UI
path instead and note it.

## 6. A failure: collect evidence once

For a `fail` that is not obvious from the snapshot, take one more snapshot and, when the app is
paired, read its recent events, then stop:

```bash
.agents/scripts/device-lane.sh ad snapshot -i
.agents/scripts/device-lane.sh appduct events ls
```

Put what explains the failure under Evidence (an error message, a missing element), one line
each. Skip this step when the snapshot already explains it. The device reaches nothing on the
host's network beyond the egress allow-list, so there is no network evidence from the device.

## 7. Release — always

```bash
.agents/scripts/device-lane.sh release
```

It closes the agent-device session, stops the Expo Simulators session and its egress tunnel,
and deletes `.env.eas-simulator`. Run it before the report on every path, including `fail` and
an error midway. If you cannot run it, say so under Evidence: the session then ends on its own
after 15 idle minutes.

## 8. Show the evidence on the PR

After the release, for `pass` and `fail` (not `busy` or `unavailable`), post one comment with
each checked line, its result and its screenshot, and the recording at the end. Upload the
files first: `attach.sh` prints one Markdown line per file, in order (an image, or a video's
URL):

```bash
.agents/scripts/attach.sh <main>/.worktrees/sim-shots/pr<PR>-1.png'#line 1' \
  <main>/.worktrees/sim-shots/pr<PR>-2.png'#line 2' <main>/.worktrees/sim-shots/pr<PR>-checks.mp4
```

Then post the comment with those lines in place (`git rev-parse --short HEAD` in the
worktree is the commit you checked):

```bash
gh pr comment <PR> --body-file - <<'EOF'
## Simulator evidence (`<short sha>`)

**<line 1, as given>**: pass
![line 1](https://github.com/user-attachments/assets/...)

**<line 2, as given>**: fail. <the step that differs, one line>
![line 2](https://github.com/user-attachments/assets/...)

Recording of the checks:
https://github.com/user-attachments/assets/...

_Written by an agent._
EOF
```

A line with no screenshot (`not covered`) gets its result alone. `attach.sh` exit 69 (no user
login on this machine) or 1: post no comment, and say why under Evidence. The comment shows
what you checked; your report decides. Never let an upload change a line's result.

## Report

If this run cost steps for a reason that is not the issue's own work, first
`.agents/scripts/memory.sh journal mobile-verifier "<what happened, what it cost>"`
(and a lesson only as the recall footer says). Then end with exactly this
block, nothing after it:

```
PR: #M  Simulator: pass | fail | busy (<EAS line>) | unavailable (<reason>)
Device: <platform> session <session id> build <build id> | none
Ran: lane binary <minutes> min, e2e <files or "none">, screenshots <n>, video yes | no; logs <paths>
Evidence comment: <its URL> | none (<reason>)
Lines: <each Done when line, then pass | fail | not covered>
Evidence: <the failing step, request or text that differs, one per line, or "none">
```
