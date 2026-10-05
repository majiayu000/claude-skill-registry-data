---
name: padosoft-cross-platform-scripting
description: >-
  Use this skill when writing or reviewing a script that has to run in more than one place — a developer's
  Windows machine and a Linux CI runner, a Makefile, a validator, a hook, a release script — and whenever the
  user says it works locally but fails in CI (or the reverse), a command reported success while the step
  failed, a path is not found on one platform only, a dotfile is invisible, a file with an accented name is
  skipped, or a regex misses lines on one checkout. It covers exit-code propagation, path and case semantics,
  interpreter discovery and how not to parse another tool's human output. Do not use it to choose a scripting
  language, for container or deployment configuration, or for CI workflow design.
license: MIT
compatibility: >-
  Any scripting language. The worked examples are PowerShell, POSIX shell and Python, because that is the mix
  that produced them.
metadata:
  version: 0.1.0
  author: Padosoft
  summary: The ways a Windows workstation and a Linux runner disagree silently.
  profiles: devops
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: powershell, bash, cross-platform, ci, exit code, paths, encoding, windows, linux
---

# Cross-platform scripting

The script runs on a Windows workstation and on a Linux runner. Everything below is a way those two disagree
**silently** — the script does not crash, it reports success while having done something else.

---

## 1. Exit codes: capture each one, immediately

```powershell
# ❌ only the last command's status is checked — the first failure is invisible
tool-a ; tool-b ; if ($LASTEXITCODE -ne 0) { exit 1 }

# ✅
tool-a ; $a = $LASTEXITCODE
tool-b ; $b = $LASTEXITCODE
if ($a -ne 0 -or $b -ne 0) { exit 1 }
```

Two traps, both from the same variable:

- **It persists.** `$LASTEXITCODE` keeps the value of the last native command run anywhere in the script,
  **even when that failure was handled** and the script went on to succeed. A wrapper that propagates it at
  the end turns a handled error into a failed job.
- **A non-terminating error is not a failure** in PowerShell: suppressing the *message* does not change the
  status, and conversely a cmdlet that "failed" may leave the previous native exit code untouched.

In POSIX shell the equivalents are `set -o pipefail` (a failing command mid-pipe is otherwise invisible) and
checking `${PIPESTATUS[@]}` when you need each stage.

## 2. Never parse another tool's human output

An error renderer is a UI: it carries ANSI codes, wraps lines where the terminal ends, and inserts context
between the message and the path. Stripping ANSI is not enough, because the line breaks are the renderer's
too, and they move when the terminal width does.

**Invoke through a wrapper that emits only the machine-readable part** — the exception message, the exit
code, a JSON payload — and normalise ANSI as defence in depth, not as the strategy.

Same rule for listings: use the machine-readable mode (`-z`, `--porcelain`, `--json`). A listing meant for
humans **quotes or escapes** non-ASCII and control characters, and treating that display form as a literal
path makes the file unreachable — the script then reports clean on a file it never opened.

## 3. Paths

- **Build paths with the platform's join**, never by concatenating with a literal separator. A literal
  backslash inside a join argument is Windows-only even when the local run passes.
- **Case sensitivity is a property of the filesystem, not of the language.** A case-insensitive containment
  check is correct on Windows and admits a case-different sibling on Linux. Select the comparison from the
  **running OS**, and keep a test that rejects a hard-coded case-insensitive containment.
- **Containment is not enough to know what a path is.** An existing directory can satisfy "inside the
  repository" and then reach a file-writing API, which fails with a generic OS error. Validate the **kind**
  of the destination, not only its location.
- **Hidden files need the explicit flag.** A metadata call that finds a dotfile on one platform returns
  nothing on another without a force/hidden flag — and the script concludes the file is absent.

## 4. Interpreter and dependency discovery

**Finding an executable named `python3` does not prove it runs your code.** A syntax feature or a keyword-only
argument added in a later version raises the real minimum above the one your type hints imply, and the
failure appears as a parse error in CI, far from the check that "found" the interpreter.

Probe the **interpreter and the pinned dependency together**, and keep the production script and its own test
harness on the **same requirement** — a harness that hard-requires `python` while the script accepts
`python` or `python3` produces a host that can validate but cannot run its own tests.

A pinned requirements file governs CI's installation, not an already-provisioned local interpreter. If a
parser version matters, **assert it at runtime**.

Guard third-party imports at module entry and emit one stable remediation message: an import that fails
before the program's error boundary prints a traceback instead of the instruction to install something.

## 5. Language-specific shapes that bite

**PowerShell collection unrolling.** A branch that emits one item yields a scalar, so indexing `[0]` returns
the first *character* of a string rather than the first element. Initialise the array and assign `@(...)`
inside the branch, and test with one item and with several.

**Passing a path object where a string API is expected** relies on an implicit, provider-dependent
conversion. Resolve once and pass the resolved string.

**Line endings in multiline regex.** In several engines `$` matches before `\n` but *after* a preceding
`\r`, so a pattern ending in a class that excludes `\r` silently misses every CRLF line while handling LF
ones. Make line-ending tolerance explicit, and keep a CRLF fixture — see also
**`padosoft-git-commit-integrity`** for why both endings exist in the same repository.

**Environment inherited by subprocesses.** A fixture that spawns a child inherits the parent's CI variables
and takes the CI branch of its own code. Neutralise CI-only variables at the boundary, restore them in a
`finally`, and run the harness once *with* the variables simulated before pushing.

---

## Gotchas

- **"It works on my machine" is a statement about your machine's tool versions, antivirus, filesystem
  casing and line endings** — four things the runner does differently.
- **A script that only ever ran green has not been tested.** Make it fail on purpose on both platforms.
- **Timing differs by an order of magnitude** when endpoint protection inspects every process launch: a loop
  that spawns one process per case is sub-second on the runner and minutes on a protected workstation. Batch
  the work rather than micro-optimising it.
- **The platform difference usually surfaces at a distance** from its cause: a skipped file becomes a clean
  security report, a lost exit code becomes a green deploy.

## Checklist

- [ ] Each native command's exit code captured immediately; no reliance on a persisting last-status variable
- [ ] `pipefail` (or the equivalent) where pipelines matter
- [ ] No parsing of human-rendered errors or listings; machine-readable modes used
- [ ] Paths built with the platform join; no literal separators in fragments
- [ ] String comparison chosen from the running OS; destination kind validated, not just containment
- [ ] Hidden/dotfile access uses the explicit flag
- [ ] Interpreter **and** pinned dependency probed; script and harness share one requirement
- [ ] Imports guarded with a stable remediation message
- [ ] CRLF and LF fixtures for anything line-based
- [ ] CI-only variables neutralised at subprocess boundaries and restored
- [ ] Run once on each target platform, including a deliberate failure

## Final report

```
Script: <path>  ·  runs on: <platforms>
Exit-code handling: per-command | last-status (why)
External output parsed: none | <which, machine-readable?>
Path/case/hidden-file handling: <what was chosen and why>
Interpreter + dependency probe: <what is asserted>
Verified on: <platform> <platform> · deliberate failure: yes | no
```
