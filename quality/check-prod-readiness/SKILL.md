---
name: check-prod-readiness
description: Run a production-readiness checklist on the repo — config hygiene, code checks, and Python quality gates. Use when asked whether changes are ready for production, before merging to a production branch, or on "check prod readiness" / "is this prod-ready".
compatibility: Quality gates assume a Python repo with nox and pre-commit; config and code checks are stack-agnostic.
---

# Check Production Readiness

Run through this checklist before merging changes intended for production.

## Config checks
If the repo has any json/yml/yaml/toml/cfg/ini or any other configuration files, evaluate them for these conditions:

- [ ] No URI / link values are hardcoded. If any are constructed, make sure they are secure (no http, ssh, ftp or another insecure protocol)
- [ ] File paths are relative. Raise a flag for any hardcoded absolute paths.
- [ ] No Windows paths
- [ ] No secrets, passwords, API keys, or anything that resembles secrets. Before flagging a "secret" check if it looks like a placeholder value; it is sometimes evident from the value of a secret/password config key.

## Code checks

- [ ] No dangerous calls to external www links, no calls anyone's private IP or box URL
- [ ] No hardcoded local paths (`D:\`, `C:\tmp`, etc.) in production-path code

## Quality gates

- [ ] `nox -s tests` passes with 100% coverage (if no 'tests' session, check noxfile.py for a unit-tests-resembling session)
- [ ] `nox -s lint` passes with zero Ruff errors
- [ ] `pyproject.toml` updated if new dependencies were added
- [ ] Pre-commit hooks pass (`pre-commit run --all-files`)

## Final verdict

End the report with a short, concise summary (a few lines at most) followed by a single overall verdict:

**PROD-READY: PASS** or **PROD-READY: FAIL**

FAIL if any check found a real issue; checks that don't apply to the repo count as pass. On FAIL, list the blocking issues, one line each.
