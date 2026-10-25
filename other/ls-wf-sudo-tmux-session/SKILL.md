---
name: ls-wf-sudo-tmux-session
description: Automatically route sudo, root/admin elevation, require_escalated, pseudo-terminal/PTY handling, interactive sudo prompts, or managed tmux run tracking through the approved tmux workflow.
metadata:
  version: "1.1"
---

Use this workflow package for server or remote ops through tmux wrappers.
Primary source references: `ls/docs/ops/tmux-ops-managed.md` and `ls/docs/ops/tmux-ops-remote.md`. Installed packages expose the same references through the `localsetup://doc/ops/tmux-ops-managed.md` and `localsetup://doc/ops/tmux-ops-remote.md` aliases.

Load this workflow automatically before any command or retry that requests `sudo`, root/admin access, elevation, `require_escalated`, or a pseudo-terminal for privileged work. Treat a transcribed request for “pseudo” as a sudo trigger when the command needs privilege. Do not wait for a reminder, switch to direct SSH or raw tmux commands, or run an unprivileged-looking retry that still invokes sudo.

## When to use

Use this workflow when a command needs `sudo`, root/admin elevation, `require_escalated`, pseudo-terminal/PTY behavior, interactive sudo or elevated terminal password prompt handoff, or durable managed tmux run tracking through `ls/tools/tmux_ops`. Installed packages expose that tool through the `localsetup://tool/tmux_ops` alias.

Do not use this workflow for normal repo-local coding, API authentication, token setup, non-privileged file edits, or commands that can run safely without managed terminal state.

## Execution authorization boundary

Terminal and credential readiness do not authorize a command. Reuse the current
user-approved task scope and its exact target/effect checks. Routine necessary
work does not need another approval merely because sudo is required. Destructive
work retains the owning recovery plan and explicit scope approval. Never expand
command authority from a credential variable, a successful probe or a pane name.

## Managed pane sequence

1. Resolve the actual caller, canonical repository, exact target and live owner.
   Use the existing private task state root. Normal `pick` requires verified tmux
   caller context and does not create a separate operations session or tab.
2. Run `./ls/tools/tmux_ops pick`, supplying `--repository`, `--host-alias`,
   `--cwd` or `--state-dir` only when needed to bind the selected context. Retain
   the returned exact `target`, parent and ownership handles.
3. Reuse the controller-owned child directly below that parent. The root name is
   `<repo>-sudo`; an admitted host uses `<repo>-<exact-alias>-sudo`. Different
   controllers may have identical names. Ownership and native IDs distinguish
   them. The child occupies one third of the parent's original height without
   changing focus.
4. Run exact argv with `./ls/tools/tmux_ops run -t <target> -- <argv...>`.
   The managed Bash handler checks its primary prompt, empty Readline buffer,
   machine/TTY/shell generation and writer lease before executing a staged
   request. The adapter sends only the reserved trigger, never command text and
   Enter. Partial input, continuation prompts and unsupported shells stop input.
5. Direct privileged argv automatically uses the shared operation-bound sudo
   owner. It checks sudo availability and resolves only `GENERIC_SUDO_KEY` from
   the controller environment, then EnvMan when that variable is absent. An
   explicit empty or invalid environment value is authoritative. Values travel
   only as private transient input through the framed channel. Workload children
   do not inherit any `*_SUDO_KEY` variables.
6. Authentication and the exact authorized command share one `sudo -A`
   invocation; command stdin is preserved. Cached validation is an observation,
   never a guarantee for a separate invocation. Authentication has its own
   configurable budget, defaulting to 120 seconds with `run --auth-timeout
   <secs>`. Unknown prompts, owner loss or attempt exhaustion stop credential
   delivery without interrupting an already-running workload.
   To collect manual input inside that same invocation, supply an explicit owned
   family `--dialog-handle`, live `--owner-pid` and `--owner-starttime`, plus its
   `--agent-id` and `--dialog-state-root` when applicable. Only the qualified
   primary viewer receives the private password popup. Unavailable, empty or
   invalid generic input permits one dialog; an EnvMan loading error does not.
   A second sudo prompt after a rejected generic password requires
   `--single-password-qualified`, asserting a verified single-password policy.
   Never use it to advance an unknown or MFA challenge. The authentication budget
   includes human input time. This route never provides a manual rerun command;
   cancellation, expiry, owner loss and uncertain delivery stop further input.
7. Track the returned operation/run ID through `status`. A slow workload stays
   running after its observation timeout. Preserve its `status_handle` and use
   `status --status-handle <handle> --wait --timeout <secs>` to read the durable
   receipt, including after a directory change or controller restart. A
   completion receipt proves completion; dispatch acknowledgement does not.
   `busy` receives no new command, and `unknown` permits read-only
   reconciliation only. Never switch backends or repeat an uncertain request.

Herdr and tmux use the shared LocalSetup terminal core. FleetOps owns its exact
host admission, authority and receipts. Select a qualified SSH/tmux fallback
before dispatch when a Herdr endpoint is unavailable. A wrong-machine attachment
may detach or log out automatically only when its recorded ownership and idle
state are proven; verify the original local shell before changing directory or
connecting elsewhere.

Missing credentials, EnvMan load errors, expired authentication, unsupported
authentication, policy denial and uncertain outcomes have distinct safe
diagnostics. Without the private dialog route, use a manual fallback only when a run result explicitly says
`action_required` and includes
`sudo.manual_fallback`; that receipt proves the workload did not start. Run
that exact quoted command once in the qualified pane. For timeout, owner loss,
policy denial, `running`, or `unknown`, use read-only status reconciliation
only; never replay. An EnvMan loading error is blocked and never supplies a
manual rerun command; check EnvMan instead of treating the error as an absent
credential. Do not run a separate `sudo -v`, type a password into
command text, print it, write it to a file or treat `sudo ready` as an execution
grant.

`./ls/tools/tmux_ops capabilities` reports the local API. A probe reports stale
or incompatible remote helper versions separately from sudo policy or
credential failures.

The old standalone `ops*` session workflow is explicit compatibility only:
`pick --legacy-session` and `run --legacy-session -t <session>`. It is not the
normal automatic path. Do not infer legacy lifecycle from a binary override.

## Legacy sudo keepalive

For active privileged work where the user has already entered sudo in the same managed pane, use bounded one-shot keepalive commands instead of ad hoc loops.

1. Request a marker only after `probe` reports sudo `ready`:

   ```bash
   ./ls/tools/tmux_ops keepalive request -t <session> --owner <id> --ttl-seconds 7200 --max-refreshes 24 --reason "<reason>"
   ```

2. Refresh only as an explicit one-shot action while privileged work remains active and the managed pane is idle between commands:

   ```bash
   ./ls/tools/tmux_ops keepalive refresh -t <session>
   ```

3. Report state with `./ls/tools/tmux_ops keepalive status -t <session>`.
4. Clear the marker with `./ls/tools/tmux_ops keepalive clear -t <session> --owner <id>` when privileged work ends.

Keepalive is restricted to managed `ops*` sessions, caps TTL at 7200 seconds and refreshes at 24, and runs only hard-coded `sudo -n -v` during refresh. Its request path performs noninteractive checks only and never starts environment-key or password authentication. It must not start a background loop, prompt for a password, or refresh while a managed run is active, another refresh is in progress, or the pane is not idle.

Load the full procedure from **ls-wf-sudo-tmux-session** and **ls-wf-tmux-terminal-mode** before privileged commands. Environment credential presence, a successful probe, an attached operator, `sudo ready`, or cached sudo state confirms transport readiness only; it never authorizes a command.
