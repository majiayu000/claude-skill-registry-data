---
name: ls-wf-tmux-terminal-mode
description: Use for observable agent shell sessions, tmux availability, command recovery, application profiles, or terminal-mode setup; privileged commands retain the sudo workflow.
metadata:
  version: "1.2"
---

Use this workflow for observable ordinary commands and tmux configuration. Native
permissions and sandboxing still govern execution. For `sudo`, elevated
permission, or privileged interactive handoff, load `ls-wf-sudo-tmux-session`;
its controller-owned lower pane remains a separate protected lifecycle.

## Observable agent commands

1. Inspect `localsetup shell --help` and its capability result. Missing tmux is a
   distinct unavailable state: optionally suggest installation for observability,
   without installing it or bypassing native execution restrictions.
2. Ensure an agent-owned session through the shell API. Use its returned handle,
   machine identity and verified created/joined result. Names are labels, not
   ownership proof. Announce "Created session <name> on <machine>" or "Joined
   session <name> on <machine>" only after that result.
   Supply the long-lived native agent PID and process start time from verified
   ancestry, never a transient CLI/helper identity. Unknown ownership permits
   observation rather than mutation.
3. Show the returned local join command alongside the safely displayed workload
   and repeat it at least once every five minutes during long-running work.
   Keep the join command discoverable in periodic progress messages; reserve the
   native status row for layout controls before optional activity telemetry.
   State which machine it runs on; never
   prepend SSH or assume the user is connected. Attachment observes existing work
   in a read-only interactive terminal and must not create a replacement or
   replay an operation.
4. Run each ordinary command in a fresh owned shell pane in the root family
   window. Admit subagents through the root-issued invitation and their live
   owner bindings. Existing legacy sessions retain their compatibility layout.
   Preserve operation IDs and
   status handles. A wait timeout or lost acknowledgement is not failure proof:
   reconcile the existing operation and inspect bounded output instead of retrying.
5. Read at most the newest 200 lines and 32 KiB of UTF-8 output text per response,
   whichever limit is reached first. These are aggregate limits, including a
   single oversized line. Use explicit bounded pages for earlier retained
   history, or `screen` for the current rendering; `view` reads captured output.
   Respect cursors and truncation gaps rather than automatically expanding context.
6. Before normal exit, close eligible owned resources and report verified cleanup
   or `cleanup pending`. Preserve live silent work and human observers. Disconnect
   alone never proves abandonment; uncertain identity permits observation only.
   Report retained collector receipts on the next startup after a crash.

For a user-authorized durable collector, use `shell schedule install` with an
explicit grant ID and qualified enrollment owner. Inspect `schedule status` and
its run receipt; preserve unrelated crontab entries. The fixed every-minute job
continues after the enrolling agent exits, skips overlap and stops on source or
runtime drift. Reboot requires an explicit same-host rebind. `schedule disable`
revokes future dispatch; do not silently renew changed authority.

Construct advertisements in the CLI from verified session and machine data,
never by hand: center the hostname with one space on either side in the top
hash border, place the unmodified command alone between blank lines, and use a
final hash border. Derive the border width from the command display width,
expanding only to fit the hostname. Multiple entries use their common maximum
width and share each following hostname border with the preceding entry. Color
is optional and respects terminal capability and NO_COLOR.

## Application profiles

Use `localsetup app-profile --help` to inspect, save, resolve and apply named JSON
preferences. Framework defaults and private user overrides have separate owners;
inspect effective values, origins and digest before native changes. The tmux
agent-shell default enables mouse support, bottom session/window status, a
20,000-line history target and views bounded by both 200 lines and 32 KiB of
output text. Family sessions report a lower effective native history capacity
when needed for their byte budget and reserve guarded viewer key bindings.
Never rewrite unrelated user sessions
or global tmux configuration. Active sessions retain their resolved settings;
apply a changed session profile explicitly while idle.
Changing pane history capacity requires a new session; inspect native readback
instead of treating an option value as proof that an existing pane was resized.

## Native canvas layout

New sessions default to the native canvas. Inspect `localsetup shell layout --help`
for its controls. Reuse
each session's recorded presentation; never migrate running legacy or rendered
canvas sessions implicitly. In the native canvas, `follow` reveals active work,
`stable` keeps the selected operations, and `fixed` also retains saved proportions.
Manual selection enters stable mode; ratio changes enter fixed mode. Only the
qualified primary viewer may change the shared view through its controls.

Keep application panes alive when hidden. Copy mode, short overlays and mediated
input defer rearrangement; inspect pending layout state rather than replaying a
layout whose acknowledgement is uncertain. Native screen history and bounded
durable logs have separate retention limits. Report gaps and unavailable capture
without treating them as complete retained output. Attachment remains observation
only; application input still uses the authorized input and lease APIs.

The older terminal-mode setup still controls whether new IDE terminals or shell
sessions launch inside tmux. It is not the ordinary-command process supervisor.

Checkout references: [TMUX_TERMINAL_MODE.md](../../docs/TMUX_TERMINAL_MODE.md)
and [tmux_terminal_mode](../../tools/tmux_terminal_mode).
For installed use, resolve `localsetup://doc/TMUX_TERMINAL_MODE.md` and
`localsetup://tool/tmux_terminal_mode`.
