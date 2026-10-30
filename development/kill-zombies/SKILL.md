---
name: kill-zombies
description: >-
  Find and terminate an orphaned process that is holding a file lock or a listen port after a crashed or
  interrupted session, so the next operation can proceed. Triggers when an operation fails because a file "is
  being used by another process", when a server or bridge cannot bind its port with "address already in use",
  when an error names the holder in a `Name (PID)` form, or when the user says "kill zombies", "release the
  lock", "the port is stuck", or "it is hung".
license: Apache-2.0
metadata:
  author: Marc Taccolini
  version: 1.1.0
---

# Kill zombies: release a lock blocking an operation

## Why this exists

After a crashed or interrupted session, a spawned process can outlive its parent and keep a file or
a listen port locked. The next attempt then fails for a reason that looks unrelated to the crash.
Hunting the process by hand is slow, and the error message usually already names what to kill. This
skill mechanizes find, confirm, kill, verify, with a safety filter so it never takes down something
you are actively using.

Treat this as the manual, mid-session fallback. The automated case belongs to hooks, and the event
matters: Claude Code's `Stop` hook fires after every reply, not at the end of a session, so a cleanup
wired to `Stop` kills your processes in the middle of the work. The safe shape is three parts:

- `SessionStart` snapshots the processes already running, which are the operator's and are never touched.
- `Stop` only **records** the processes this session started (for example, those whose parent chain
  contains this session's Claude Code process). It stops nothing. `Stop` does not run after an
  interrupt, so record once more at `SessionEnd` before stopping anything.
- `SessionEnd` **stops** the recorded processes that are still running, checking PID, name and start time
  so a reused PID is never hit.

`SessionEnd` also fires on `/clear` (reason `clear`) and on an interactive `/resume` (reason `resume`),
while the same Claude Code process keeps running. If your processes should survive those, check `reason`
in the script and stop nothing for those two. SessionEnd hooks get 1.5 seconds by default, so set a
`timeout` on a cleanup that verifies its kills.

Processes started by another session, a shared bridge, or by hand are never in this session's record.
The hooks handle session end. This skill helps when you are blocked right now.

## When this triggers

- An operation fails because a file is held by another process.
- A server, bridge, or dev process cannot bind its port with "address already in use".
- An error names the holder in the `Name (PID)` form.
- The user says: "kill zombies", "release the lock", "the port is stuck", "it is hung".

Do not trigger when the failure is not a lock (a compile error, a missing dependency, a wrong path),
when a debugger is live, or when another session may legitimately own the file or the port. A
force-kill on a live session destroys unsaved work. Confirm first.

## Process

### 1. Identify the holder

If the error names a PID, parse it. A pattern like `\b([\w\.\- ]+) \((\d+)\)` against the "locked by"
line captures the process name and the PID.

If it does not, enumerate candidates by process name, or find the process LISTENING on the port. Never
take every process with a socket on the port: that includes connected clients, such as a browser or
another session.

```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort <port> -State Listen).OwningProcess
```

```bash
lsof -nP -iTCP:<port> -sTCP:LISTEN -t
```

### 2. Show the kill list first, always

Echo what is about to be killed before anything dies, even when you intend to proceed
automatically. The user has to see the list.

### 3. Safety filter: names that are never auto-killed

Hard-skip any PID whose process name matches:

- OS-critical: `explorer`, `dwm`, `winlogon`, `csrss`, `services`, `lsass`, `svchost`, `launchd`, `kernel_task`
- Editors and IDEs likely active: `devenv`, `rider`, `idea`, `code`, `cursor`, `claude`, `pycharm`, `webstorm`, `goland`, `clion`, `eclipse`
- The shell hosting this session: `pwsh`, `powershell`, `cmd`, `bash`, `zsh`, `wsl`

If a hard-skip name is the holder, STOP and surface it. The user decides whether to close it cleanly
or to override.

### 4. Stop the remaining processes

Batch every PID into one invocation. On macOS and Linux, ask first with a plain `kill`, and use `kill -9`
only on survivors after the step 5 pause.

```powershell
Stop-Process -Id 23660,2260 -Force
```

```bash
kill 23660 2260
```

### 5. Verify, with a pause

The Windows process table updates with a slight delay, so an immediate re-check can report false
survivors.

```powershell
Start-Sleep -Milliseconds 500
Get-Process -Id 23660,2260 -ErrorAction SilentlyContinue
```

```bash
sleep 0.5; ps -p 23660,2260
```

An empty result means the kills landed. If a PID persists, retry once after a one-second pause (on macOS
and Linux, this is where `kill -9` is used). If it still holds, surface it.

### 6. Suggest the next step

Once the locks release, offer to re-run the operation that failed.

## Anti-patterns

- Killing without showing the list first.
- Killing a process you cannot confirm is an orphan. It may be another session's live work. Check
  start time or parent before force-killing, and when unsure, stop and ask.
- Looping forever on a stuck PID. Retry once, then escalate.
- Skipping the verify pause, which reports stale state.
- Running `taskkill /F` from a Git Bash or MSYS shell on Windows. The shell rewrites `/F` into a
  path like `F:/` and the command fails. Use PowerShell `Stop-Process`, or wrap it as
  `cmd /c "taskkill /F /PID 1234"`. This one was found in first live use.
- Running this on a CI runner. PIDs there are ephemeral and the runner's own host may be in the list.
- Treating an ordinary document lock as a zombie. A locked PDF or spreadsheet is the user's active
  session.

## Source and rationale

This is a packaged form of the general technique: find the process holding the lock, then release it.
The parts worth keeping are reading the holder PID straight from the error message, batching the
kill into one call, the verify pause, and the safety filter that separates an orphan from an editor
or another live session.
