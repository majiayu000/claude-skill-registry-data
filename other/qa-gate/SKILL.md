---
name: qa-gate
description: Run this project's full local quality gate (lint/typecheck/test commands from .harness/project.json) and report pass/fail. Use before opening a PR, or whenever asked to run the full check/test suite.
context: fork
background: false
---

Run this project's quality gate and report the result. Nothing else — no restating the commands, no unrelated commentary.

1. Read `qa_gate_commands` from `.harness/project.json` — an ordered list of shell commands (e.g. `["make check", "make test"]` or `["ruff check .", "mypy .", "pytest"]`). If the file or field is missing, tell the user to fill it in (run `harness init`/`update` again, or edit `.harness/project.json` directly) and stop.
2. Read the optional `shell` field from the same file — `"bash"` (or the field absent) means this
   checkout runs commands through bash (Linux, macOS, or a Windows checkout where `bash` on `PATH`
   is really Git Bash/WSL and not the System32 WSL launcher stub); `"powershell"` means run them
   through PowerShell instead — pick this on a native Windows checkout where a bare `bash` resolves
   to that stub and fails with no WSL distro configured, even for a command that needs no shell at
   all. Run each command in order through the installed agent-facing wrapper, choosing the shell
   argv accordingly:

   ```bash
   # shell: "bash" (default)
   python .harness/skills/qa-gate/scripts/test_summary.py -- bash -lc '<exact command from qa_gate_commands>'

   # shell: "powershell"
   python .harness/skills/qa-gate/scripts/test_summary.py -- powershell -NoProfile -NonInteractive -Command '<exact command from qa_gate_commands>'
   ```

   On the first failure, stop. Return the wrapper's bounded summary — status, pytest totals, failed
   node IDs, structured diagnostics (traceback endings, explicit error messages, and compiler/linter
   errors), and its sanitized local log path — rather than command output or an arbitrary tail of
   the log. Do not run the remaining commands. Read a failure log only when the developer needs
   that particular diagnostic evidence. The wrapper works with every quality command; do not add
   a pytest JSON/XML reporting flag unless that command already owns and documents that artifact.
3. If every command succeeds, record the pass marker yourself: run `bash "$CLAUDE_PROJECT_DIR/.claude/hooks/record-qa-gate-pass.sh"`. Don't rely on the `mark-qa-gate-passed.sh` PostToolUse hook alone for this — this skill runs forked (see `context: fork` above), and the hook isn't guaranteed to fire for Bash calls made inside that fork.
4. Report a compact one-line PASS summary only — do not paste the passing output.
