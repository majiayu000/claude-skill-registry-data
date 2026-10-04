---
name: ddev-local-runtime
description: 'Mandatory rule that all local project commands for the ndestates-io repository run inside the DDEV runtime, not on the host shell. Apply when about to run php, composer, artisan, npm, node, python3, pip, mysql, pest, phpunit, or any project tooling locally.'
user-invocable: true
disable-model-invocation: false
---

# DDEV is the local runtime — host shell is not supported

The full DDEV local runtime rules and command table are contained in this SKILL.md (originally sourced from the project's .github/skills/ for dual compatibility). Follow the mandatory DDEV wrappers, pre-flight, allowed host exceptions, and Python rules exactly as documented in the body of this file.

## Grok notes
- This is non-negotiable per `.github/copilot-instructions.md` §2.
- Use `/load-project-cache-first` to absorb CONVENTIONS/TESTING before running project cmds.
- Only host cmds allowed: ddev control, git/gh, doctl/aws, docker (for prod images), read-only rg/grep/find.
- For Python: always `ddev exec python3 scripts/...` or pip via ddev.
- Before any project cmd: `ddev status`; if down, baseline git status, start, recheck.
- Tests: always via ddev + confirm test DB.

State reason and ask if you must ever deviate. Default: prefix with ddev.
