---
name: check
description: Run this repo's CI locally - ruff, each module imported with only boto3, pytest - plus project-rule checks CI doesn't have (read-only AWS calls, lazy optional imports, View conventions, IAM permissions listed in README, copies of the shared code). Use after changing src/aws_analyzer/ or tests/, before saying the work is done, and before committing.
argument-hint: "[matrix] [pytest args, e.g. -k policy]"
allowed-tools: Bash(.venv/bin/python .claude/skills/check/run.py:*), Bash(python .claude/skills/check/run.py:*), Bash(.venv/bin/python .claude/skills/check/rules.py:*), Bash(python .claude/skills/check/rules.py:*), Bash(.venv/bin/python .claude/skills/check/snapshot.py:*), Bash(python .claude/skills/check/snapshot.py:*)
---

# Check

Run everything CI runs, locally, and fix what it finds.

## Run it

Use `.venv/bin/python` if it exists, otherwise `python`:

```bash
.venv/bin/python .claude/skills/check/run.py                  # ruff, imports, package, rules, pytest
.venv/bin/python .claude/skills/check/run.py --matrix         # + pytest on CI's other Python versions (uv)
.venv/bin/python .claude/skills/check/run.py -- -k policy     # arguments after -- go to pytest
```

Arguments: `$ARGUMENTS`. If they include `matrix`, pass `--matrix`. Pass anything else to pytest after `--`.

The full run takes about a minute, mostly pytest. `--matrix` builds a throwaway uv environment for each Python in
`.github/workflows/ci.yml` other than the local one. The first build of each takes about a minute, and later runs
reuse it. The first line of the output names the local Python. On 3.10 the local run covers pandas 2 /
IPython 8, and on 3.11+ it covers pandas 3 / IPython 9. The matrix covers the other versions. Use `--matrix`
after touching anything that uses pandas, IPython or version-specific stdlib, or when asked for the full run.

## Steps

| Step | Fails when | Usual fix |
|---|---|---|
| `ruff` | `ruff check .` finds a real error (E4/E7/E9/F) or breaks a code style rule (B006, BLE001, ERA001, C901, PLR0912/0913/0915) | Fix the code: split the function, name the condition, catch the specific error. Don't add `noqa` or a file to ruff.toml's per-file-ignores; take a rule off a file there once the file passes it |
| `imports` | a module of the package (`aws_analyzer.s3`, ...), imported in a fresh interpreter, doesn't import with only boto3 (the same as CI's job) | Move the optional import inside the function that needs it, through `_require(module, purpose)` |
| `package` | the wheel `pyproject.toml` builds fails `twine check --strict`, or doesn't import with only boto3 (skipped when `build` isn't installed; building fetches hatchling, so it needs the network) | A new analyzer needs its module in `_MODULES` and its classes in `src/aws_analyzer/__init__.py`; a README that doesn't render on PyPI shows in twine's message |
| `rules` | `rules.py` finds an error: a write API call, a top-level non-stdlib import, an import of another analyzer (or `_kit` importing one), a copy of a helper `_kit` has, missing `from __future__ import annotations`, section banners out of order, a public View method without `@_friendly_errors` (a companion window's: `@_window_errors`) or a docstring, or `print` / `display` outside the rendering plumbing; in a service split into a package, also its core importing the UI, its analysis importing its analyzer, or a function defined in two of its modules | Follow the message. Each one names the rule from CLAUDE.md (a package's: "Architecture of a service package") |
| `pytest` | a test fails (`tests/test_style.py`: a docstring with text beside its quotes, or a file with more `#` comments than `COMMENTS_LEFT` allows, or fewer, which means lowering its number) | Find the root cause. Change a test's expectation only when the behaviour change was intended, and say so |
| `py3.X` | (`--matrix`) a test fails on that Python only | Usually pandas 2 vs 3 (copy-on-write, the default `str` dtype) or stdlib added after 3.10 |

Rule **warnings** don't fail the run, but deal with each one that the current change caused:

- *needs `svc:Action`, which README.md's IAM permissions don't list*: add the permission to that service's
  IAM section in `README.md` and in `docs/<service>.md`. For S3, the action is often not the operation name
  (`ListObjectsV2` → `s3:ListBucket`). `rules.py --apis` prints the mapping.
- *execute_statement runs any PartiQL*: the analyzer must refuse anything but `SELECT` before calling it. Once
  it does, mark the call's line `# read-only: <how it's guarded>`.
- *imports X directly*: use `_require("X", "what it's for")`, so a missing package turns into a note that says
  what to pip install.
- *not annotated -> None*: View methods render and return nothing.

If a warning was already there before this change, mention it once in the report and leave it alone.

## Refactors: prove nothing a user sees changed

For a change that shouldn't change any output (moving code, sharing a helper), compare snapshots of every
report before and after. `snapshot.py` runs about 150 View commands on the demo data (the figures in `shots.py`,
the cases in its own `DEMO_CASES`, and `help()`), each in text and in HTML, with the clock stopped and random IDs
fixed, so two runs of the same code are identical. It also records the names each module has and the AWS
operations `rules.py` finds. It needs time-machine (`pip install time-machine`), and takes about two minutes.

```bash
git worktree add <scratchpad>/main-wt origin/main                                    # the code before the change
.venv/bin/python .claude/skills/check/snapshot.py run <scratchpad>/snap/main --root <scratchpad>/main-wt
.venv/bin/python .claude/skills/check/snapshot.py run <scratchpad>/snap/new          # this checkout
.venv/bin/python .claude/skills/check/snapshot.py compare <scratchpad>/snap/main <scratchpad>/snap/new
```

`compare` exits 1 and shows the diff for every output that changed, every name a module lost and any change in
the AWS operations. A private name removed on purpose (a dead copy of a helper) is named with
`--allow-lost s3._band ...`, so it's reported without failing. An unexpected difference is a bug in the change: find it, and don't move the baseline. When a
difference is intended, say which outputs changed and why. Use the same `snapshot.py` for both runs (the one in
this checkout), so both run the same cases.

## Report

Give one line per step (PASS / FAIL / time), then for each failure the cause and what you changed. Don't
report "all green" unless the last run shows it. If you fixed something, run the check again and report that
run. Don't commit unless asked.
