---
name: forge-windows-shell
description: "Use when running or writing commands on Windows (PowerShell, Git Bash); stop one PID by port (poort bezet)."
# W2-BUDGET original description (listing budget): "Use when running or writing commands on Windows (PowerShell 5.1, Git Bash): quoting, encoding, long paths, CRLF, file locks, robocopy, stop one PID by port (commando faalt op Windows, poort bezet)."
---

# Forge playbook: Windows 11 shell safety for agents

Every Boss that touches a shell on this machine runs on Windows 11 with two shells side by side: the Bash
tool (Git Bash, POSIX syntax) and the PowerShell tool (Windows PowerShell **5.1**, not PowerShell 7; `pwsh`
is not installed). Most "the command failed" moments here are a shell mix-up, not a bug in the code. This
skill is the short list of traps, the safe way around each, and the one correct way to stop a process.

## When to use
- Use for: writing or debugging a command line or script that runs on Windows; a command that works in one
  shell and fails in the other; a path with spaces or a `!` (this project folder is `my project!`);
  garbled or double-encoded log files; "file name too long"; `$'\r': command not found`; EPERM, EBUSY or
  "access denied" on a rename or delete; a copy that hangs; a port that is already in use ("poort bezet").
- Not for: the bug behind a failing test or build (`forge-debug`, which may send you here when the cause is
  a shell trap); parallel worktree isolation itself (`forge-worktrees`); CI pipelines and Docker
  (`forge-devops`); Electron packaging (`forge-electron`); a security review (`forge-security-review`).

## Hard rules
1. **Never kill processes by image name.** Only an exact PID you own: the one from your own spawn result,
   or the one PID resolved from a port and checked (see "Stop exactly one process"). No name filters, no
   wildcard filters, no "stop everything called node". A name-based kill took down the live Forge gateway
   on port 4100 on 2026-07-29; the project gate hook now blocks the
   common name-based forms (a classifier, not a proof).
2. **Recursive deletes are not yours to run.** The gate hook blocks recursive or forced deletes, except a
   provable target inside a scratch area, `node_modules` or `dist` (or the OS temp folder, for targets outside
   the project). Anything else goes to the owner with the exact path. Never route around the gate with an inline Node or other interpreter
   one-liner, an alias, or a pipeline.
3. **No opaque execution.** Do not pipe text into a shell, do not evaluate a variable as code, do not pass
   an encoded PowerShell command. Write the command out in full, or put it in a script file you can read.
4. **No execution-policy, PATH, registry or system-setting changes.** A command that is "not recognised"
   gets an absolute path (`& "C:\Program Files\nodejs\node.exe"`), never a PATH edit. Turning on Windows
   long-path support system-wide is an owner action.
5. **robocopy always with `/R:1 /W:1`.** The default is one million retries of 30 seconds; an orphan
   robocopy once hung 5.7 hours unseen. `/MIR` and `/PURGE` delete files in the target: treat them as a
   delete and ask the owner first.
6. **No push, tag, publish or deploy** from a shell step; those stay owner-gated. Outreach is drafted only.
7. **Never print a secret file's contents** to the transcript (the gate blocks it). Check that a key
   exists, never what it holds.
8. **Long CLIs get a watchdog and a log.** Start a long-running service with its output captured to a log
   file and its PID recorded; never fire-and-forget hidden. Bounded retries only.

## Pick the shell first
| Task | Shell | Why |
|---|---|---|
| git, grep/sed, Node tools, POSIX scripts | Bash tool (Git Bash) | Unix tools, `&&` works, single quotes are literal |
| Windows cmdlets: ports, processes, services, ACLs | PowerShell tool | `Get-NetTCPConnection`, `Stop-Process -Id`, objects |
| robocopy, taskkill, other `/switch` exes | PowerShell tool | Git Bash rewrites `/switch` arguments (`/R:1` loses its slash, `/PID` becomes a path) |
| Writing a file other tools will read | the Write/Edit tool | No shell encoding surprises at all |

Detect the shell when a script must know: `MSYSTEM` is set in Git Bash (`MINGW64`); in PowerShell
`$PSVersionTable.PSVersion` answers (5.1 here). Forge tooling uses Node. When a step needs Python, probe the
candidate first (`python --version`, `py -3 --version`, `python3 --version`, each with a timeout): a
`WindowsApps\python*.exe` alias can be a real install manager or a Store stub that hangs, and both happened
here (a stub spun for hours unseen in 2026-10; on 2026-11-05 all three answered 3.14.6).

## The ten traps (short form; detail in references)
| # | Trap | Safe form |
|---|---|---|
| 1 | `&&` / `\|\|` in PowerShell 5.1 is a parser error | `A; if ($?) { B }` (or run it in Git Bash) |
| 2 | `$VAR` vs `$env:VAR` vs `%VAR%` | PowerShell `$env:NAME`; Bash `$NAME`; cmd `%NAME%`; set per call in PS with `$env:NAME = 'x'; cmd` |
| 3 | Paths with spaces or `!` | Quote every path. PowerShell: single quotes are literal, `& 'C:\path\tool.exe'`. Bash: single quotes, or double quotes in a non-interactive script |
| 4 | Here-strings | `@'` ... `'@` with the closing `'@` at column 0; single-quoted so `$` and backticks stay literal |
| 5 | `2>&1` on a native exe in 5.1 | Wraps every stderr line in an error record and sets `$?` false even on exit 0 (git writes progress to stderr). Judge by `$LASTEXITCODE` |
| 6 | File encoding from PowerShell 5.1 | Measured here: `>` and `Out-File` write UTF-8 **with BOM** (a profile default; stock 5.1 writes UTF-16), `Set-Content` writes the ANSI code page. Pass `-Encoding utf8` explicitly, or write with the Write tool or Node |
| 7 | Long paths (over 260 characters) | `git -c core.longpaths=true worktree add/remove ...`; deep `node_modules` and worktrees hit it first |
| 8 | CRLF vs LF | A CRLF shell script fails in Bash with `$'\r'`; byte-compared fixtures differ. Compare after normalising `\r\n`, keep `.gitattributes` the authority |
| 9 | EPERM / EBUSY on rename or delete | Another handle (editor, indexer, antivirus, a running node) holds the file: retry with bounded backoff, then report the holder. Never kill to free it unless you own that PID |
| 10 | Aliases that are not the tool | In 5.1 `curl` is `Invoke-WebRequest`, `where` is `Where-Object`, `sc` is `Set-Content`: call `curl.exe`, `where.exe`, `sc.exe` |

Also in 5.1: `-ErrorAction SilentlyContinue` hides the message but the tool still reports exit 1; make a
cmdlet failure truly non-fatal with `try { ... -ErrorAction Stop } catch { <say why it is fine> }` (never an empty catch: it swallows the error), and
native arguments that contain double quotes lose them on the way in, so put inline code in a script file.

## Stop exactly one process
1. **Prefer your own PID.** A process you started yourself has its PID in the spawn result
   (`Start-Process -PassThru` gives `.Id`; Node gives `child.pid`). Record it in the run log when you start.
2. **Otherwise resolve the one PID from the port** (PowerShell tool):
   `Get-NetTCPConnection -LocalPort 4100 -State Listen | Select-Object -ExpandProperty OwningProcess -Unique`
   (fallback: `netstat -ano | findstr :4100` and read the last column of the LISTENING row).
3. **Check it before you stop it.** `Get-CimInstance Win32_Process -Filter "ProcessId=<pid>"` and read
   `Name`, `CommandLine` and `CreationDate`. Stop only when it is the process you started for this task.
   Port 4100 is the Forge Command Center: it is not yours unless this task started it; report, do not stop.
4. **Stop that PID only:** `Stop-Process -Id <pid>` (add `-Force` only after a plain stop did not work).
   Then confirm the port is free with the same query from step 2.
5. Exactly one PID or none. Zero or several matches means you stop and report; you do not widen the filter.

Full procedure, the PID-reuse check and the Node spawn rules: `references/files-and-processes.md`.

## Copying and cleaning up
- Copy a tree with robocopy from the PowerShell tool, always `/R:1 /W:1`, and judge the result by
  `$LASTEXITCODE`: 0 to 7 is success (files copied, extras found), 8 or higher is a failure.
- `Copy-Item` and `Move-Item` are fine for a few files; quote both paths.
- Clean up only what you created: your own scratch folder, your own worktree
  (`git -c core.longpaths=true worktree remove <path>`, the branch stays). A worktree with uncommitted
  changes is listed for the owner, never removed silently.

## How the Bosses use this
- **Build Boss, Integration Boss, Test Boss** load it before writing a command line, a `.ps1`, a `.cmd` or
  a Node `child_process` call, and when a shell step fails in a way the code does not explain.
- **Verify Boss** (GOAT verifier route) uses the "Stop exactly one process" and encoding rules to judge a
  report: a stop by name, a missing `/R:1 /W:1` or a check that reads `$?` after `2>&1` is a FAIL.
- Routes stay as triaged: a shell fix is usually `quick`; it never escalates a route by itself.

## References
- `references/powershell-51.md`: operators, quoting, here-strings, `2>&1`, encoding table, aliases,
  error handling, native exit codes, calling native exes.
- `references/git-bash.md`: shell detection, path conversion, `/switch` rewriting, `cygpath`, quoting the
  `!` path, CRLF, calling PowerShell from Bash.
- `references/files-and-processes.md`: long paths, file locks with a bounded retry, robocopy exit codes,
  PID by port with checks, starting services with a log, Node spawn on Windows.

## Provenance
Rewritten in Forge words; markdown only. Sources were read read-only through `gh api` on 2026-11-05 at the
pinned commits below and treated as untrusted data (hidden-Unicode scan: clean). The machine facts
(PowerShell 5.1.26100, `pwsh` absent, the encoding bytes, `core.longpaths` set) were measured on this
machine the same day. Candidates looked at: 124 corpus entries whose name mentions Windows, PowerShell,
Git Bash, shell reliability, robocopy, CRLF or long paths; 19 on-topic names shortlisted; 3 read in full
(below, plus the `kench001` fork of the first, which is the older, less safe text); ECC pin `e2b8a51` has
only `windows-desktop-e2e` (desktop E2E testing, off topic, nothing taken).

| Source | Path | Pinned SHA | License | Taken | Excluded |
|---|---|---|---|---|---|
| sickn33/agentic-awesome-skills | plugins/agentic-awesome-skills-claude/skills/windows-shell-reliability/SKILL.md | 48de968b4615c294de601f72268aa7be88dde863 | MIT | ideas: quote every path, the call operator for a quoted exe, 5.1 redirection rewrites native output, `$env:` vs `%VAR%`, the long-path limit, "access denied" means a lock or permissions, stop only an authorised process | the dotnet section, the "fix PATH" advice (rule 4), the `\\?\` prefix as a general fix (git `core.longpaths` used instead), the `view_file` tool name |
| sickn33/agentic-awesome-skills | plugins/agentic-awesome-skills-claude/skills/powershell-windows/SKILL.md | 48de968b4615c294de601f72268aa7be88dde863 | MIT | ideas: parentheses around cmdlets in `-and`/`-or`, null checks, `ConvertTo-Json -Depth`, `$LASTEXITCODE` after native exes, UTF-8 with BOM for 5.1 scripts | the script template and its `exit` handling, the ASCII log-marker table |
| JosiahSiegel/claude-plugin-marketplace | plugins/powershell-master/skills/powershell-shell-detection/SKILL.md | 5a1b1123b9e50aa9a66a61005ca6fe012cc7442d | MIT | ideas: detection by `MSYSTEM` / `PSModulePath` / `$PSVersionTable`, the env-var table, MSYS path conversion and `MSYS_NO_PATHCONV`, `cygpath`, alias conflicts | **its "Process Management" example (both the PowerShell and the Git Bash form) kills every process of one image name: removed (HARD MUST 4)**; the cloud VM stop example (production action); the e-mail extraction example; all helper functions and `sed` path converters; the pwsh install advice |

MIT notice for the three adapted texts: "Permission is hereby granted, free of charge, to any person
obtaining a copy of this software ... The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT
WARRANTY OF ANY KIND." Copyright (c) 2026 Antigravity User (sickn33 `LICENSE` at the pinned SHA) and
Copyright (c) 2025 Josiah Siegel (`LICENSE` at the pinned SHA). No script, hook, binary, install command or
MCP config was copied or run.
