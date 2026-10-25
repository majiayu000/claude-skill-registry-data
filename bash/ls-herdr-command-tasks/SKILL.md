---
name: ls-herdr-command-tasks
description: "Run and observe commands in owned Herdr panes with real completion evidence; manage logs, waits, cancellation, and explicitly requested agent work. Start with ls-herdr-task-routing."
metadata:
  version: "1.0"
---

# Herdr tasks

Read the master first if needed:
[ls-herdr-task-routing](localsetup://package/ls-herdr-task-routing/SKILL.md)

Use `localsetup herdr task --help`. Load layout only when allocating or changing
the work area:
[ls-herdr-pane-layout](localsetup://package/ls-herdr-pane-layout/SKILL.md)

## Run a command and finish the job

For a finite command in a new owned pane:

```bash
localsetup herdr --workspace "$HERDR_WORKSPACE_ID" --pane "$HERDR_PANE_ID" \
  --state-dir "$task_state" task run --cwd "$PWD" --wait 5 -- \
  python3 -c 'print("ready")'
```

Replace the example argv with the requested command. `task_state` is the
existing task's absolute private state directory. Continue with returned
`result.task_id` using `task status <task-id>` or `task wait <task-id>`, then
`task cleanup <task-id>` after a confirmed terminal receipt. Cleanup preserves
the actual exit outcome; it is different from cancellation.

1. Resolve the explicit target and working directory. Use an owned, available
   shell pane; never type into a busy shell, editor, approval dialog, or agent.
2. Submit the literal argument vector through the task runner. Preserve the
   operation ID; do not replace it when a wait times out.
3. Use status/wait to obtain the operation-specific exit receipt and bounded
   output. A timeout means unfinished or unknown work, not permission to rerun.
4. Report the command's actual outcome. Clean up the owned pane when the work
   is complete unless a continuing process or visible result is intended.

Native `pane.run` acknowledges queue admission. Output matching can match old
text. An apparent shell prompt does not prove the submitted command finished.
The shared runner's receipt binds the operation and its exit status; use it.
Never replay after connection loss until read-only reconciliation proves what
happened.

## Logs, servers, and long operations

Keep a requested server or log follower in an owned pane, report its handle,
and leave it running when appropriate. Prefer bounded recent unwrapped output
for readable logs. Wait on native events or operation records rather than
writing an ad hoc busy polling loop. Refresh a snapshot after event loss.

Cancel only the exact owned operation when interruption is requested or already
covered by the task. Do not send Ctrl+C to a guessed pane, kill an entire Herdr
server, or treat disconnect as cancellation.

## Requested agent work

Pane layout and recognized-agent lifecycle are different. Native `agent start`
uses an existing available pane; it does not create one. Use returned agent
names/IDs, supported native agent operations, and the user's chosen client.
Do not select a model, expand delegation authority, bypass Plan Mode, or answer
another agent's approval/question UI on the user's behalf.

Native `agent prompt --wait` observes semantic states. `idle`, `done`, and
`blocked` are not shell exit codes or proof that every background task finished.
Read the relevant result and validate the requested deliverable. A stalled or
timed-out prompt may have been delivered; inspect before resubmitting.
