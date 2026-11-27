---
name: agnos-meta-qa
description: "AGNOS maintainer skill. Writes a code quality report on this repository's Python and JavaScript, as JSON for an AI or a tool to correct from, using pinned ruff, complexipy and ESLint with SonarJS rules. USE FOR: an explicit request from a human or an instruction, typically before a commit or a push, to avoid corrections in the pull request. It runs on an explicit request only, never blocks anything and never changes the code."
argument-hint: "setup | check [--all] [<path>...] [--out <file>]"
---

# AGNOS Code Quality Report

<!-- FTR-QLT-001; RQ-QLT-001 to RQ-QLT-008 / ADR-QLT-001 (DEC-QLT-001 to DEC-QLT-007) -->

A maintainer skill, like `agnos-meta-demo`: it reports, and whoever reads the report corrects. No hook, commit or push depends on it, so
call it only when a human asks or an instruction says to. Canonical procedure, shared by GitHub Copilot
(`.github/skills/agnos-meta-qa/`) and Claude Code (`.claude/skills/agnos-meta-qa/`, which points here).

## Procedure

Run from the repository root (`python3` on `linux` / `macos`, `python` on `windows`).

1. The first time, and after the versions in `assets/` change, install the analysers. This needs network access and Node.js, and writes only
   to `.agnos-qa/`, which git ignores:

   ```
   python .github/skills/agnos-meta-qa/scripts/qa.py setup
   ```

2. Run the report:

   ```
   python .github/skills/agnos-meta-qa/scripts/qa.py check                # the changed files, staged or not, untracked included
   python .github/skills/agnos-meta-qa/scripts/qa.py check --all          # every script git knows
   python .github/skills/agnos-meta-qa/scripts/qa.py check <path>...      # these files or folders
   ```

   Tests, fixtures, vendored files and the demo's content are left out, unless a file is named directly.

3. Check the exit code. `0`: the report is written, whatever it holds. `1`: the analysis could not complete, the cause is on the error stream, and
   no report exists: report it. Do not read an older report.
4. Read `.agnos-qa/report.json`, or the `--out` file, and act on what was asked: report the findings, or correct them. To correct, keep the
   behaviour, run the tests of what changed, then run `check` again. Never change the code when asked only for a report.
5. In VS Code with a diagnostics tool, read the diagnostics of the changed files, especially HTML, and report them apart: SonarQube finds there
   what the command line lacks. They depend on the editor and on what is open, so they never enter the report.

## The report

```json
{
  "schemaVersion": 1,
  "head": "3a014c6",
  "scope": "changed | all | paths",
  "files": ["path/from/the/root.py"],
  "tools": {"ruff": "0.17.3", "complexipy": "8.3.0", "eslint": "10.14.0", "eslint-plugin-sonarjs": "4.2.2"},
  "limits": {"cognitiveComplexity": 15},
  "summary": {"total": 2, "open": 1, "exceptions": 1, "openByRule": {"E501": 1}},
  "findings": [{
    "file": "path/from/the/root.py", "line": 12, "column": 121, "endLine": 12, "endColumn": 130,
    "tool": "ruff", "rule": "E501", "severity": "warning", "message": "Line too long (129 > 120)",
    "fixable": false, "exception": null
  }]
}
```

- Findings are sorted by file, line, column and rule. `endLine` and `endColumn` can be null.
- `severity`: `error` when the code is wrong (undefined name, parsing error), else `warning`.
- `fixable`: the analyser could fix it itself. The skill never applies the fix.
- `exception`: null for an open finding, else the reason it stays. Do not correct it.

## Exceptions

When a finding must stay, say why in a comment on its line or the line above, in the file's comment syntax. A comment without a reason, or for
another rule, leaves the finding open. Prefer a correction: an exception is a decision someone will read.

```python
# agnos-qa-exception: E501 a table reads better on one line
```

## Rules

The rule set and its reasons are in the process's decisions. <!-- DEC-QLT-006 --> `assets/ruff.toml` and `assets/eslint.config.mjs` hold it; `COMPLEXITY_MAX` in `scripts/qa.py`
holds the complexity limit. Change a version or a rule by editing the assets, then run `setup`.
