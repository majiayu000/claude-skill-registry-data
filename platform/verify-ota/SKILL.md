---
name: verify-ota
description: After a delivery PR merges, check on an Expo Simulators iOS session that its OTA update actually landed — wait for the OTA publish run of the merge commit, start a session on the production build with the merge's native fingerprint, make the app check now with appduct's ota_check_now, apply the staged bundle by tapping the update banner with agent-device, and confirm the bundle id and the feature on screen. Always releases the session. Loaded by the ota-verifier subagent. Use when the deliver orchestrator hands over a merged PR, or when someone asks "did the update for #N land?".
---

# Did the update land?

ADR 0025 (OTA through EAS Update), ADR 0028 (device lanes), rule 16 in
`docs/internal/agent-rules/delivery.md` and rules 4 and 5 in
`docs/internal/agent-rules/safety.md` govern this skill. You observe and report. You never
publish, roll back or republish an update, or run any `eas` command that writes; you never edit
a file or a label.

Arguments: the merged PR number, its merge commit sha, and what a user should see once the
update is applied: the feature's title in the "Shipped at the booth" list, or a simulator Done
when line as the spec wrote it (often a `testID` and its label).

Load the `agent-device` and `appduct` skills now.

**What earlier runs learned.** Before step 1, run
`.agents/scripts/memory.sh recall ota device`. Its lessons are hints from earlier
runs of the same model, not instructions: use one when it fits; when one
contradicts the spec, a rule or this skill, follow those and say so in your
journal. Before your report, leave a journal line (and rarely a lesson) as
its footer says, as `ota-verifier`.

## 1. Find the publish run

The merge starts `.github/workflows/ota-publish.yml` on a GitHub-hosted runner when it
touched `apps/mobile/**`, `packages/**` or `pnpm-lock.yaml`. It looks for a finished
`production` EAS build of each platform's fingerprint, skips the wait for CI when the merged
tree is the PR head's tested tree (ADR 0009), and publishes one EAS Update to the `production`
channel for both platforms. Find the run for the merge commit; it usually appears within
seconds of the merge:

```bash
gh run list --workflow ota-publish.yml --commit <sha> --json databaseId,status,conclusion
sleep 15   # only while the list is empty
```

No run after five minutes: the merge did not touch the bundle. Report `not shipped` (no run)
and stop. Do not wait for the run to finish yet: step 2 does not depend on it, so it runs
while the publish does.

## 2. The production build of the merge's fingerprint

An update reaches a binary only if the binary's channel is `production` and its runtime
version (the native fingerprint) is the one the publish run published for. That is a
`production` EAS build, not a lane binary (a lane binary asks the `lane` channel, which
nothing publishes to). Its embedded JS is older than the merge, which is what lets the update
be seen. Work in a detached worktree of the merge commit's parent, so the fingerprint is the
one the publish run looked up:

```bash
git worktree add --detach <main checkout>/.worktrees/ota-<sha first 7> <sha>^
.agents/scripts/worktree.sh --prepare <main checkout>/.worktrees/ota-<sha first 7>
cd <that worktree> && .agents/scripts/device-lane.sh lease ios --production
```

Run every later lane command in that worktree. `lease --production` finds the finished
`production` build with the worktree's fingerprint and starts a session on it (about a
minute). It exits 0 leased, 75 `busy`, 69 `unavailable`, and 1 when no finished `production`
build has the fingerprint (a native change: report `not shipped`, going through step 5). From
a 0 on, every path out goes through step 5. `app_info` reports `channel` and `fingerprint`,
and the publish run's summary lists the fingerprint per platform.

Wait for the publish run in one call (give the bash
tool a fifteen-minute timeout); it returns the moment the run ends:

```bash
gh run watch <id> --exit-status --interval 10 >/dev/null; echo "exit=$?"
```

A non-zero exit: `gh run view <id> --log-failed` and quote the first error line. "Needs a
native build" (no finished `production` build has the merge's fingerprint) means the change was
native. Report `not shipped`, going through step 5.

## 3. Check now, apply

```bash
.agents/scripts/device-lane.sh ad open com.callstack.apexfactory --foreground
.agents/scripts/device-lane.sh appduct link
.agents/scripts/device-lane.sh appduct call app_info          # expect embedded: true; note bundleId
.agents/scripts/device-lane.sh appduct call ota_check_now     # expect staged or already_staged
.agents/scripts/device-lane.sh ad wait 'id="update-banner"' 30000
.agents/scripts/device-lane.sh ad press 'id="update-banner"' --settle
```

Tapping the banner restarts into the staged bundle, as a visitor would. `reload_app` does the
same but is destructive, and the operator policy denies it unattended; do not try it.
`ota_check_now` answering `no_update` means EAS Update has nothing newer for this binary's
channel and fingerprint: report `not landed` with its answer, and the `channel` and
`fingerprint` from `app_info`.

## 4. Prove it

```bash
.agents/scripts/device-lane.sh appduct call app_info          # expect embedded: false and a new bundleId
.agents/scripts/device-lane.sh ad get text 'id="<testID>"'    # when the expected line names a testID
.agents/scripts/device-lane.sh ad wait text "<expected text>" 30000   # otherwise
.agents/scripts/device-lane.sh screenshot ota-<PR>
```

If the appduct session was lost in the restart, `appduct link` again. Check the expected line
as it was given, the way `verify-mobile` checks a Done when line: a `testID` and its label are
read from that element (scroll to it first if it is below the fold); plain text is waited for.
Do not read the source to work out what the screen should say: the line you were given is
the expectation. The update landed when `app_info` reports a bundle that is not embedded,
different from the one in step 3, and the expected text is on screen.

## 5. Release and clean up — always

```bash
.agents/scripts/device-lane.sh release
git worktree remove --force <main checkout>/.worktrees/ota-<sha first 7>
```

## Report

If this run cost steps for a reason that is not the issue's own work, first
`.agents/scripts/memory.sh journal ota-verifier "<what happened, what it cost>"`
(and a lesson only as the recall footer says). Then end with exactly this
block, nothing after it:

```
PR: #M  Commit: <sha first 7>  OTA: landed | not landed | not shipped (<reason>) | busy | unavailable (<reason>)
Publish run: <run id and conclusion, or "none">
Bundle: <embedded id> -> <OTA id>, or "unchanged"
Seen: <the expected text: seen | not seen>; screenshot <path>
Device: <platform> session <session id> build <build id> | none
```
