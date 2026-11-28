---
name: cross-platform-care
description: Write scripts, paths, and file I/O that survive a machine they weren't developed on — path separators, shell dialects, quoting, line endings, case-sensitivity, missing or divergent tools, timezones. Use when writing shell or PowerShell scripts, CI steps, Makefiles or justfiles, path manipulation, file reads and writes, or install/setup instructions others will run. Not for pure in-memory logic.
---

# cross-platform-care

"Works on my machine" is an environment assumption you didn't notice making (environment-first is the cure; this is the prevention). Weak portability is a script tested once on the author's laptop; strong portability names its targets and checks against the one it isn't on.

## Before writing: name the targets

State which platforms and shells the artifact must run on (e.g. "Linux CI with `/bin/sh` = dash, macOS zsh, Windows PowerShell 7"). Check what the repo already commits to: CI matrix, existing shebangs, `.editorconfig`, `.gitattributes`, `engines` / `requires-python`. If it targets one platform only, say so in a comment at the top and stop portability work there.

## 1. Paths

Build paths with the path library, never string concatenation with `/` or `\`: `pathlib` / `os.path.join`, `path.join`, `filepath.Join`. Same for home (`~` doesn't expand everywhere), temp dirs (platform API or the session scratchpad), and current-dir assumptions (derive absolute paths from a known root such as the script's own location). On Windows also avoid reserved names (`CON`, `NUL`, `aux`) and trailing dots or spaces in filenames.

## 2. Shell dialect

Declare the shell you actually target. Bashisms (`[[`, arrays, `set -o pipefail`, `local`, `$'...'`) fail in POSIX `sh`; CI images often ship `dash` as `/bin/sh`; zsh differs on word splitting and globs. Use `#!/usr/bin/env bash` if you need bash, `#!/bin/sh` only if it is genuinely POSIX. PowerShell is a different language, not a dialect — never mix its syntax with sh.

## 3. Quoting and arguments

Quote every expansion (`"$var"`, `"$@"`); unquoted expansion breaks on the first path with a space, which is every macOS user directory. Put `--` before positional args to guard filenames with leading dashes. Never build a command by pasting user-supplied strings into a shell line — pass argv arrays.

## 4. Case-sensitivity

macOS and Windows filesystems are usually case-insensitive; Linux is not. `import utils` finds `Utils.py` locally and dies in CI. Imports, includes, asset URLs, and case-only renames must match the file's real casing — verify with `git ls-files`, not the editor's view.

## 5. Line endings and encodings

CRLF from Windows checkouts breaks shebangs, heredocs, and string comparisons; declare `*.sh text eol=lf` in `.gitattributes`. Declare encoding explicitly when reading or writing text (`encoding="utf-8"`); never inherit the platform default. Choose newline handling explicitly on write.

## 6. Tools and versions

Don't assume a tool exists or matches: GNU vs BSD flags differ (`sed -i ''`, `date -d` vs `-v`, `grep -P`, `readlink -f`, `xargs -r`); `python` may be v2, absent, or a Store alias on Windows. Probe with `command -v <tool>` and fail with a message naming what's missing; version-check anything whose behavior you depend on; prefer the portable subset when it's cheap.

## 7. Time

Servers run UTC; laptops don't. Code that formats, parses, or compares timestamps names its zone explicitly; tests that depend on "today" pin the clock (see edge-case-sweep).

## Exit check

Run a check under the target you're not on before shipping: `shellcheck` or `sh -n` / `bash -n` for a Linux target from macOS or Windows, WSL or a container for a full run, `pwsh -NoProfile -File` for PowerShell. Then answer: "would this run on a fresh Linux CI container and on a laptop with a space in the username?" Both, or the header says which one it targets.
