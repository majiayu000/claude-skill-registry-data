---
name: check
description: "Runs the ai-toolkit pre-PR checks that AGENTS.md requires for the files changed on this branch, and lists the hand-written per-agent files that may need mirroring. Run it from the ai-toolkit checkout before opening a PR. Never runs on its own."
argument-hint: "[base ref, default origin/main]"
disable-model-invocation: true
---

# Toolkit pre-PR checks: $ARGUMENTS

Run the checks `AGENTS.md` requires for the files this branch changes, and report each result. Fix nothing. The report is the deliverable.

## Procedure
1. **Scope.** Confirm the working directory is the ai-toolkit checkout (`.claude-plugin/marketplace.json` has `"name": "ai-toolkit"`). The base ref is the argument, or `origin/main` when none is given. Run `git fetch origin`, `git diff --name-only <base>...HEAD` and `git status --porcelain`. The version check reads commits only, so list uncommitted files in the report.
2. **Every change.** Run `python3 scripts/build/build.py --check`, `python3 scripts/ci/check_repo.py`, `python3 scripts/ci/check_style.py`, `python3 scripts/ci/check_plugin_versions.py --base <base>`, `python3 tools/freshness.py` and `python3 tools/source_anchors.py --lint`.
3. **By changed path.** Add the checks this table names for each path the diff touches:

| Changed path | Also run |
|---|---|
| `shared/hooks/` or any plugin `hooks/` | `python3 -m unittest discover -s shared/tests` and `bash claude/tests/test-guards.sh` |
| `claude/install.sh` or `claude/home/` | `python3 -m unittest discover -s claude/tests` |
| `claude/plugins/<name>/` or `.claude-plugin/` | `claude plugin validate . --strict` and `claude plugin validate claude/plugins/<name> --strict` |
| `codex/` | `python3 codex/scripts/validate.py` and `python3 -m unittest discover -s codex/tests` |
| `antigravity/` | `python3 antigravity/scripts/validate.py` and `python3 -m unittest discover -s antigravity/tests` |
| `tools/` | `python3 -m unittest discover -s tools/tests` |
| `shared/install_common.py` | `python3 -m unittest discover -s shared/tests`, `python3 -m unittest discover -s codex/tests` and `python3 -m unittest discover -s antigravity/tests` |
| `src/` or `scripts/build/` | `python3 scripts/build/build.py --check` and `python3 -m unittest discover -s scripts/build/tests` |

   Run each check as its own command from the repository root, without `cd` or chaining, so each failure points at one check.
4. **Generated files and mirroring.** `python3 scripts/build/build.py --check` fails when a generated file is stale, missing or edited by hand, so a change to a generated path must come from its source under `src/` or `shared/`. For the hand-written per-agent files, such as plugin manifests, hook registration, home instructions and installers, compare the changed paths across `claude/`, `codex/` and `antigravity/`, and list each layer that has no change where another layer does. The PR description must name anything not mirrored and why.
5. **Report.** Give a table of check, result (pass, fail or not run) and, for a failure, the first lines of output that show the cause. A check that cannot run, such as one that needs a missing CLI, is "not run" with the reason. Then list the hand-written per-agent files that may need mirroring and the uncommitted files.

## Rules of the check
- Run the commands. Never report a check as passing from reading the code.
- Do not edit files, refresh stamps or run any `--write` mode. A failure goes in the report for the user to fix.
