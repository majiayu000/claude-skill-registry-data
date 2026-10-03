---
name: lint
description: Deterministic, differential hygiene gate. Runs static-analysis / style / spelling tools over the files a change touches and reports ONLY newly-introduced findings, so pre-existing debt never blocks. Run it before spending model-review budget (cpp-abi-guard, cycles-parity-reviewer, pr-reviewer) on mechanical issues. Never installs anything; a missing linter is 'unavailable', never a silent pass.
---

# lint

A cheap, deterministic pass that catches the mechanical defect class model
reviewers systematically miss (formatting, dead code, obvious cppcheck-class
bugs, malformed markdown, comment typos, trailing whitespace). Run it **before**
the expensive Opus-tier reviewers so their attention goes to what only they can
judge — ABI footguns, physics parity — not style nits.

It is **advisory**, not a merge gate: nothing in CI or `pr-reviewer` blocks on
it. It is a local tool you (or an implementer agent) run before opening a PR.

## What it does

`scripts/lint.py check` finds the files your change touches (vs `origin/main` by
default), runs each applicable tool over them, and — the important part — runs
the same tools over the same files at the base ref (checked out into a throwaway
detached `git worktree` in the system temp dir) and **subtracts** the base
findings. You see only what your change newly introduced. Legacy debt in the
C++ core therefore never drowns the signal.

```powershell
# lint everything changed on this branch vs origin/main (the default)
python .claude/skills/lint/scripts/lint.py check

# diff against a specific base
python .claude/skills/lint/scripts/lint.py check --base main

# lint specific files regardless of git state
python .claude/skills/lint/scripts/lint.py check --paths src/foo.cpp include/bar.h

# scan the whole tracked tree (non-differential — noisy, for audits only)
python .claude/skills/lint/scripts/lint.py check --all

# make a missing linter a hard failure instead of a warning
python .claude/skills/lint/scripts/lint.py check --require-coverage
```

## Tools in the registry

| Tool             | Files                         | Notes                                              |
|------------------|-------------------------------|----------------------------------------------------|
| `ruff`           | `.py`                         | default ruff ruleset (pyflakes + pycodestyle core) |
| `cppcheck`       | `.cpp .cc .cxx .hpp .hh .h`   | `.cu`/`.cuh` excluded — they need nvcc flags        |
| `clang-format`   | C/C++/CUDA                    | **only runs if a root `.clang-format` exists**      |
| `markdownlint`   | `.md`                         | `markdownlint-cli2`                                 |
| `codespell`      | code + docs                   | spelling in identifiers/comments/prose             |
| `shellcheck`     | `.sh .bash`                   | JSON output                                         |
| `git-diff-check` | any                           | trailing whitespace / conflict markers (built-in)  |

## Non-negotiable invariants

- **Never installs anything.** A missing tool is reported `unavailable` with an
  install hint and (if `--require-coverage`) a coverage gap — it is **never**
  counted as a pass.
- **A crashing tool is an `error`, never a pass.**
- **Nothing is auto-fixed.** No `--fix`, no `--write-changes`. It reports; you fix.

## Exit codes

`0` clean · `1` new findings · `2` a tool errored · `3` coverage gap
(only with `--require-coverage`). Precedence when several apply:
**error(2) > coverage-gap(3) > findings(1)**.

## Enabling full coverage on a machine (per-machine, one time)

The script and this skill sync via OneDrive, but the **linters themselves are
per-machine binaries that live outside the repo** — they are not synced. On a
fresh machine the gate still runs and still refuses to lie (missing tools show
`unavailable`), but to get real coverage install the tools once:

```powershell
python -m pip install ruff codespell          # Python lint + spelling
npm install -g markdownlint-cli2              # Markdown
choco install llvm shellcheck                 # clang-format + shellcheck
choco install cppcheck                        # C++
```

- **`clang-format`** stays dormant until a root `.clang-format` exists — without
  a project style it would emit noise against LLVM defaults. Add one deliberately
  if/when the team wants C++ formatting enforced.

## When to invoke

- An implementer runs `/lint` after finishing a package and before opening the
  PR, so mechanical findings are fixed before `cpp-abi-guard` /
  `cycles-parity-reviewer` / `pr-reviewer` ever look at the diff.
- Any time you want a fast, deterministic read on "did I add anything sloppy?"
  without waiting on a model review.

## Anti-patterns

- Treating `unavailable` as "clean" — it means *unchecked*. Install the tool or
  accept the gap knowingly (`--require-coverage` makes the gap loud).
- Running `--all` and trying to fix every pre-existing finding — that's the debt
  the differential mode exists to keep out of your way. Fix what your change adds.
- Wiring this into CI or `pr-reviewer` as a blocking gate without a tuning pass
  first — cppcheck throws false positives on template-heavy path-tracer code, so
  it earns trust before it earns a veto.
