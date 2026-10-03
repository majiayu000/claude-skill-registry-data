---
name: jshell
description: Use when running Java snippets in JShell or using JShell as a Java REPL or scratchpad.
---

# JShell

Run JShell in an agent-controlled terminal and own its lifecycle. Record its pid when it starts,
keep the terminal session, and do not finish the task until that session has exited.

## Resolve the executable

Run `jshell --version` before the first evaluation. On macOS, `/usr/bin/jshell` can be a launcher
that reports no Java runtime even when an SDK-managed JDK is installed. In that case, resolve an
installed JDK and use its absolute `bin/jshell` path for the rest of the task.

If a requested JShell option is uncertain, inspect that executable's `--help` or `--help-extra`.

## Start and use JShell

Start this command in a terminal with TTY enabled, replacing the final argument with the resolved
absolute path:

```sh
/bin/sh -c 'printf "JSHELL_PID=%s\n" "$$" >&2; exec "$1" --execution local --feedback concise' sh /absolute/path/to/jshell
```

Save both the returned terminal-session id and the printed `JSHELL_PID`. `exec` replaces the shell
with JShell without changing the pid, while `--execution local` keeps evaluation in that tracked
process.

Send Java snippets to the terminal session with a trailing newline. Poll a running session with an
empty write. A returned live-session id only means the command is still running; it does not prove
that JShell is waiting at a prompt.

## Finish the session

Never send `/exit`. When no more evaluation is needed:

1. From a separate terminal command, send `TERM` to the recorded numeric pid. For example, if
   JShell printed `JSHELL_PID=16438`, run `kill -TERM 16438`.
2. Poll the original terminal session with empty writes for at most five seconds.
3. If it has not exited after those five seconds, confirm that the same pid is still the tracked
   JShell process, send `KILL` to that pid, and poll the original session again until it exits.

Never abandon a live JShell terminal session. Do not use `pkill jshell` or `killall`; terminate only
the pid recorded for the current task.
