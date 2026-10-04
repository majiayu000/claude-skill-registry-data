---
name: backend-manual-testing
category: qa
description: Use when the task touches a backend API, database or worker - booting it from the task branch, driving real requests and verifying side effects (DB rows, outbound calls, logs) as evidence
---
# Backend Manual Testing

## Overview

Manual verification of a backend task means booting the real service (and its worker, if the repo has one) from the task branch and executing your scenario plan against it. The scenario plan comes first and comes from the task description and acceptance criteria alone (scenario-plan-first) — you never derive cases from the diff or the source.

**Preconditions:** case matrix recorded with `record_test_cases` (scenario-plan-first); environment chosen per test-environment-selection (local by default — side effects are only observable there — else the repository's stage deploy target; never prod).

## Booting in the workspace

1. **Learn how the project runs** — in this order: `search_memory` (scope=project) for a boot recipe from an earlier round, `get_project_brief` for the components/commands/ports, the repository's `build_command`/`test_command`/`verify_command` settings, README / Makefile / docker-compose / example env files, and any comment the developer left (a clean run leaves none). `list_links` shows what this component talks to — the side effects you'll need to verify and the dependencies to stub. Do not guess ports, flags, or env vars when the project declares them.
2. **Provision dependencies.** Database and other infrastructure run as disposable containers when a container runtime (podman/docker) is available; run the project's real migrations and a minimal seed. External third-party services are stubbed so failure scenarios are drivable (test-data-and-stubs).
3. **Start the processes**: the API server, and every worker/consumer process the repo defines (see worker-job-testing). Keep their logs streaming to a per-task scratch file: `QA=${TMPDIR:-/tmp}/tt-<task-key>/qa; mkdir -p "$QA"; ... > "$QA/api.log" 2>&1 &`.
4. **Smoke check** before scenarios: health endpoint answers, migrations applied, worker connected. A failed boot is itself a finding — capture the exact error output.

## Executing scenarios

For each scenario in the plan, in order:

- **Drive the real surface**: `curl`/httpie against the running API (api-contract-testing). Record the exact request and the exact response — status, body, headers that matter.
- **Verify side effects, not just responses**: the DB row that should exist (`psql -c "select ..."`), the outbound call that should have been made (the stub's received-requests log), the file/event that should have been produced. A 200 with the wrong side effect is a FAIL.
- **Watch the logs during every scenario.** Stack traces, ERROR/WARN lines, or panics count as findings even when the HTTP response looks correct.
- Cover the implied cases too: invalid input, missing/wrong auth, empty state, duplicate submission (boundary-negative-testing).

## Evidence and wrap-up

- Every scenario gets PASS/FAIL with the executed command and observed output (qa-verify-before-verdict).
- After targeted scenarios, run the regression sweep (regression-checklist).
- Stop the processes you started; the workspace must not keep orphan servers running.
- Automation is out of scope this iteration (manual-only-testing): the same scenarios are not added to a suite. A red existing pipeline (`get_pipeline_status`) is a finding; green is not a substitute for this round.
- Once booting took real effort, save the recipe to project memory (`save_memory`, scope=project) so the next round on this repo starts faster.

## Red Flags

- You are about to form a verdict without having booted anything → that is code review, not QA.
- The response is right but you never checked the DB/log/stub side → half-tested.
- Boot instructions missing and you improvised a config → post what is missing instead; untestable is not done (test-environment-selection).
