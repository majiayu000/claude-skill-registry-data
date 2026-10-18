---
name: qwen38-code-gate
description: "Done-gate for any code change by a small model. Run it before saying a change is finished: the brief table for code (the test that goes red then green, the error path, the doc line, no new dependency), then six commands with pass conditions — scope of the diff, placeholders, secrets, the repo's tests with the last line pasted, lint/typecheck if configured, and the RED line before the GREEN one. Slice 1 of xeno-skills #355."
target-model: Qwen3.8
triggers:
  - /qwen38-code-gate
  - code gate
  - ก่อนบอกว่าแก้โค้ดเสร็จ
  - ตรวจโค้ดก่อนส่ง
---

# Code gate (`qwen38-code-gate`)

**Run this before you say a code change is finished.** Fill the table, run every command, paste each output. A check you did not run is a check that failed. Report `CODE GATE: n/6` with the outputs under it.

## 0. Brief table — before the first edit

| the brief names or implies | file(s) that deliver it |
|---|---|
| each change the brief asks for | the file and function |
| **a test that fails before the change and passes after** | the test file — **always a row, even when the brief does not say "test"** |
| the error paths — **one row each**: wrong type · negative or out of range · empty · missing file or key | where each raises or returns, and the test for each. (2026-09-05 16:49: with one combined row the model tested garbage input and skipped the negative amount the hidden test caught; enumerated rows are the fix) |
| the doc line, if the repo has a README or docstrings for this area | the line |
| new dependency | **none** unless the brief allows one; write "none" |

Edit only the files in the right-hand column. Anything else you think needs changing goes in the report as a note, not in the diff.

## 1–6. The checks

`D` is the diff of your change: `git diff` if the repo is a git checkout (make a commit or `git add -N .` first so new files show), otherwise the list of files you wrote.

**1. Scope.** Pass: every path printed is in the brief table.
```sh
git diff --name-only HEAD
```

**2. No placeholders.** Pass: nothing prints. (The bare-stub half is its own alternative: `^\+` cannot appear in the middle of an alternation, and while it did, `+    pass` never matched and the gate printed a passing `placeholders 0` over a stub-filled diff. Found in review 2026-09-06.)
```sh
git diff HEAD | grep -nE "^\+\s*(pass|\.\.\.)\s*$|^\+.*(TODO|FIXME|XXX|NotImplemented|raise NotImplementedError|console\.log\(\"debug|print\(\"debug)"
```

**3. No secrets or machine paths.** Pass: nothing prints.
```sh
git diff HEAD | grep -nE "^\+.*((api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"]{8,}|C:\\\\Users\\\\|/home/[a-z]+/)"
```

**4. The repo's tests, last line pasted.** Use the repo's own command (`python -m pytest -q`, `npm test`, `bun test`, `go test ./...`, `cargo test`); do not invent one. Pass: the last line reports 0 failed and the count is not lower than before your change.
```sh
python -m pytest -q 2>&1 | tail -3
```

**5. Lint / typecheck when the repo has a config.** Pass: exits 0, or write "no config" when none of these files exists: `pyproject.toml [tool.ruff]`, `.eslintrc*`, `eslint.config.*`, `tsconfig.json`, `.flake8`, `mypy.ini`.
```sh
ls pyproject.toml .eslintrc* eslint.config.* tsconfig.json .flake8 mypy.ini 2>/dev/null
```
Then the matching command: `ruff check .` · `npx eslint .` · `npx tsc --noEmit` · `flake8` · `mypy .`

**6. RED before GREEN.** Paste the test command's last line from **before** you changed the source (the new test failing) and from **after** (passing). If you wrote the test after the code, write "test written after code" — that is a fail of this check, not a reason to hide it.

## Report

```
THINK: assumptions <k> · flaws checked 3 · found <n> · pushback: <yes: the line | no>   <- first, from qwen38-think, when it was loaded
CODE GATE: n/6  (scope ok · placeholders 0 · secrets 0 · tests: <last line> · lint: <ok|no config> · red-then-green: yes)
brief table: k rows, all filled
```
A brief the three-flaw check found impossible does not get a `CODE GATE: 6/6`; it gets the `Pushback:` line, the possible part, and an honest gate for that part.
Paste the six outputs under it. `CODE GATE: 6/6` with no outputs is not a pass.

## Rules that apply here as everywhere (`using-qwen38`)

Never install a package or a tool to satisfy a check; if the command is missing, write one line saying so and continue. Never spawn an agent. Stop at the report.

## What this does not touch

How to design the change, name things, or structure a module — `karpathy-guidelines` and the repo's own conventions own that. This file only says whether a change may be called finished.
