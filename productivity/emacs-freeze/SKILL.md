---
name: emacs-freeze
description: Diagnose a frozen, hung, beachballing, or unresponsive Emacs by sampling the process, reading server buffers when possible, and recommending recovery. Use when Emacs is stuck or not responding; do not use for ordinary Elisp errors while Emacs is responsive.
---

# Emacs freeze diagnosis

Establish what is unresponsive, identify the intended Emacs process, and separate
observations from competing explanations. A diagnosis request does not authorize
recovery or configuration edits. A slow server channel alone is not a frozen UI;
the user's report of working interactive input is evidence about a different
channel. Route ordinary responsive-session errors to the relevant debugging task.

Never signal an active Emacs without explicit confirmation for the exact target
and action. Recovery evaluations, input injection, restarts and debugger-setting
changes also need explicit authority. Revalidate process identity immediately
before an approved action; never use a name-wide signal or a broad kill alias.

Preserve the user's intentionally enabled global `debug-on-error` workflow.
Temporary suppression during authorized recovery needs a recorded restoration
plan and post-unwind verification, not a permanent debugger-off recommendation.

## 1. Identify the session

- Record the reported symptom, onset, preceding action, UI behavior, runtime/
  profile and known outstanding client requests.
- Enumerate candidate Emacs processes, accounting for executable-name case and
  GUI, terminal, daemon and batch instances. `pgrep -ix Emacs` is a starting point,
  not proof that every build is covered or that one match is the intended session.
- Check candidate executable, owner, arguments and start time. `--init-directory`
  selects configuration, not a GUI session. Do not choose the first or busiest
  PID by heuristic when multiple sessions remain plausible.
- Bind the chosen PID to available window/profile/socket evidence. If safe
  self-service checks cannot disambiguate it, ask which session is affected.
  A vanished or reused PID invalidates the target; do not reuse old commands.

## 2. Collect bounded, private evidence

Create a fresh owner-only diagnostic directory outside Drive, such as
`mktemp -d /tmp/emacs-freeze.XXXXXX`. Use a restrictive umask for files, preserve
the exact directory path and record command status/time alongside each artifact.
Do not reuse a predictable per-PID directory or overwrite pre-existing samples.
Raw paths, buffer text and stack arguments may be sensitive; keep them local and
redact any shared summary. Follow the secrets policy if credentials are involved.

On macOS, collect a short `/usr/bin/sample PID 5 -file PATH` and targeted
`ps -p PID -o pid=,pcpu=,rss=,etime=,state=` readings. Quote actual paths and
validate the numeric PID first. Sampling briefly suspends/resumes the target;
record permission failures or incomplete output rather than escalating blindly.

Collect additional open-file/socket/thread information only when it helps a
specific hypothesis. Avoid silently discarding stderr or presenting `head -80`
as a complete inventory. For socket discovery, `lsof -nP -a -p PID -U -F0pftn`
provides machine-readable fields: parse complete NUL-delimited records and types,
not whitespace-separated final fields. Count thread rows without the header.

Repeat relevant observations after an interval while continuing useful work.
macOS `ps` CPU is a recent decaying average, not a lifetime average; label the
platform and sampling interval. RSS movement indicates resident-memory changes,
not proof of progress, and stable RSS does not establish a deadlock.

## 3. Probe the correct server cautiously

Resolve the actual server endpoint from this process's evidence. Do not assume
the default socket, silently select the first matching pathname, expose TCP
server authentication files, or confuse a regular file with a listening socket.
Use a verified `emacsclient` executable with an explicit endpoint and
`--alternate-editor=/usr/bin/false`; do not use the local `emacs-client` wrapper
or an empty alternate editor, which can launch another Emacs.

Use [scripts/run-client.py](scripts/run-client.py) for a parent-enforced wait on
one owned client process:

```sh
python3 /ABS/SKILL/scripts/run-client.py 5 /ABS/emacsclient \
  --alternate-editor=/usr/bin/false --socket-name=/ABS/VERIFIED-SOCKET \
  --eval '(emacs-pid)'
```

Substitute exact quoted absolute paths; the script takes a finite deadline in
seconds greater than zero and at most 300, followed by literal argv. Redirect
bounded diagnostic replies to private files
when needed. A tool-level deadline must leave time for the helper's cleanup;
use asynchronous execution/polling for long waits so updates are not blocked.

The helper kills/reaps only its own client on a deadline, not Emacs or a process
group. Inspect its diagnostic as well as exit status: 124 denotes its deadline,
127 launch failure, 130 interrupted waiting, and 125 unconfirmed cleanup.
Cleanup gets at most five additional seconds. Other client exit codes are
preserved, so no numeric code alone proves a server outcome. If cleanup is
unconfirmed, stop additional requests and reconcile the reported owned PID.

First send a cheap `(emacs-pid)` probe and require its returned PID to match the
identified process. Only then collect small, bounded state such as
`(recursion-depth)` and relevant debugger values. If useful, request capped
head/tail excerpts of `*Backtrace*` and `*Messages*`, checking buffer existence
and reporting size, truncation and collection time. Do not dump an entire huge
backtrace, print arbitrary Lisp objects or evaluate package code for diagnostics.

A deadline means no client reply within that interval. It does not prove a dead
server, frozen UI, cancelled evaluation or successful recovery. Terminating a
client cannot retract a queued or already running server request. Keep at most
one diagnostic client outstanding and reconcile its outcome before another
request; do not pile up a compulsory 5/30/120-second ladder. Longer observation
can be useful for an intermittently serviced server, but no threshold turns a
timeout into proof of death. Continue out-of-band analysis when replies are absent.

## 4. Interpret evidence without turning heuristics into verdicts

- Match sample and buffer timestamps to the same process/session. Identify the
  actual main thread; distinguish sample counts from textual frame occurrences.
  A stable sampled stack can be a tight busy loop, an I/O wait or ordinary idle
  input. Branching stacks do not prove healthy progress. Correlate CPU, repeated
  samples, user-visible behavior and plausible wait conditions.
- Debugger frames establish debugger involvement, not sole causation or a
  computation-free freeze. Inspect their surrounding call paths, errors and
  intervening timers, filters, sentinels, GC or redisplay; those can cause,
  amplify or merely accompany the problem.
- Debugger rendering can precede `recursive-edit`. Report observed frame counts
  and returned recursion depth separately; they are not interchangeable or
  quantities to subtract into an exact count of unfinished debuggers.
- Investigate hot paths even when debugger frames exist. Repeated recursion,
  expensive printing, `symbol-file` lookup, GC and blocked I/O are hypotheses,
  not universal causes. Do not import fixed per-frame timings or quadratic-cost
  claims from a previous incident without measurements and a supported model.
- Check stack-walk warnings, missing symbols, optimization and truncation limits.
  Missing `main` or `read_char` alone does not prove truncation. The outermost
  visible package is not automatically the originating error.
- Decode native-comp symbol names only when their encoding is confirmed for
  this build. Use a literal hex decoder, not shell evaluation of sampled text.
- Buffer dumps can be stale, partial or captured after the sampled state changed.
  Resolve conflicts through timing and source evidence; neither samples nor
  buffers categorically override the other. Leave unknown origins unknown.

Check relevant installed source/docstrings or authoritative documentation for
version-sensitive semantics. A batch probe must not be presented as evidence
about interactive debugger behavior that its harness suppresses.

## 5. Recovery only with explicit authority

Present the least invasive plausible option and its consequences before acting.
Say plainly whether it terminates Emacs. Do not recommend a kill or debugger
interrupt merely because a client timed out.

- Waiting or an observed user-visible quit may be appropriate for a busy command.
  An `emacsclient` evaluation of `(keyboard-quit)` is not a generic interruption
  of the suspended command: server request handling can catch that quit locally.
- For confirmed nested recursive edits with a usable execution channel,
  `top-level` can abort all recursive edits and the current computation without
  terminating Emacs. It can abandon the normal client reply. Neither that missing
  reply nor exit 142 establishes success; independently verify the resulting
  UI, server and recursion state. It is not a rollback of prior side effects.
- SIGUSR2 normally requests debugger entry when `debug-on-event` is configured
  for it; it is not intended to terminate Emacs. Check the actual build/setting
  and explain that another debugger entry can worsen debugger recursion.
  In Emacs 30.2 the matching signal also sets `debug-on-quit` true and requests
  a quit while clearing `inhibit-quit`; do not promise unchanged debug state.
- SIGTERM terminates Emacs. Orderly shutdown may run hooks and attempt autosave,
  but a wedged process, settings, ineligible buffers or I/O failure can prevent
  preservation. Hooks or visited-file autosaving can write original files.
  Do not promise that every buffer is saved or that only `#file#` files change.
- SIGKILL terminates immediately, without shutdown hooks or a fresh autosave.
  Unsaved state not already recoverable can be lost. Keep this warning out of
  casual copy-paste command blocks and require exact explicit confirmation.

Before a terminating action, assess modified file and non-file buffers,
subprocesses, autosave eligibility and available recovery files if accessible.
A zero modified-file-buffer count is not zero session risk; inaccessible state
means unknown risk. After an approved restart, inspect actual autosave paths and
use appropriate file/session recovery. Do not guarantee `recover-session`:
orderly shutdown can remove the session's autosave-list file.

If temporary debugger suppression is necessary, record intended values and the
binding context before changing them. Dynamic bindings may unwind assignments;
do not assume changes persist or restore automatically. Verify and restore the
intended post-recovery `debug-on-error`, `debug-on-quit` and `inhibit-debugger`
state, and report any restoration gap instead of leaving the debugger disabled.

Use direct user-visible/runtime acceptance for any recovery performed. A prompt
reply alone does not prove the originally reported UI problem disappeared.

## 6. Prevention, report and cleanup

A diagnosis-only request ends with evidence and recommended remedies. Implement
only separately authorized fixes. For a demonstrated recurring async error,
consider narrow containment of the identified path with explicit error reporting;
do not hide failures, broadly disable debugging, or add advice already present in
the user's configuration. Verify canonical source, loaded state and the exact
behavior before claiming a preventive change works.

Report observations, supported inference, material unknowns, recovery authority/
outcome and any remaining data or debugger-state risk. Answer direct questions
such as whether an option kills Emacs before elaborating.

Preserve useful evidence for unresolved cases. Once disposable diagnostics are
no longer needed, trash only this run's known owned directory; never delete
pre-existing samples or unrelated contents. Retain a private evidence summary
and report any diagnostic path that remains intentionally available.

Primary references: [recursive edits](https://www.gnu.org/software/emacs/manual/html_node/elisp/Recursive-Editing.html),
[Emacs 30.2 signal handling](https://github.com/emacs-mirror/emacs/blob/emacs-30.2/src/keyboard.c#L7750),
[shutdown](https://github.com/emacs-mirror/emacs/blob/emacs-30.2/src/emacs.c#L2809),
and [autosaving](https://www.gnu.org/software/emacs/manual/html_node/elisp/Auto_002dSaving.html).
