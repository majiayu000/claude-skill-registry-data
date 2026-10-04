---
name: qa-verify-before-verdict
category: qa
description: Use before any review_criterion approval or column move - the evidence each verdict needs, how to treat skipped, blocked and intermittent cases, and which exit a blocker takes
source: obra/superpowers (MIT), adapted
---
# Verify Before Verdict

No verdict without fresh executed evidence in this run.

- Every case on the task gets a result you recorded yourself: `passed` or `failed` with the exact command and its observed output (`actual`), UI cases additionally with a one-line evidence string (width/device, URL, viewport report, what it showed — never a screenshot path, there isn't one; frontend-manual-testing / mobile-manual-testing). The result belongs on the case (`set_test_case_result`), not in a comment — that is where the next reader looks, and it survives the run.
- A case you could not execute is `skipped` with what blocked it (no device, no stage deploy, missing credential), never `passed`. A case still `planned` when you try to hand the task on refuses the move.
- A pass verdict rests on ONE thing this iteration: every case executed manually by you, with its evidence. Writing automated tests is out of scope for now — do not add suites and do not hold a verdict waiting for one. The repository's existing pipeline is still read (`get_pipeline_status`): red is a finding, green is not a substitute for your own run.
- A criterion is approved (`approved=true`) only when you executed and observed it pass this run AND at least one `passed` test case carries its `criterion_id` — an approval with no linked passed case is what pm_uncovered_criterion rejects at PM UAT. A criterion you could not execute is never approved: say which one, what blocked it and what would unblock it.
- Both verdicts are moves out of `in_qa` — the column you took the task into before testing. All cases green → move it to pm_uat with the evidence on the cases and the criteria approved — except a task whose `task_type` field is `technical`: move it straight to human_uat instead, same evidence, same "no comment" rule. A backend-only, API-only or infra `task` or `bug` still goes to pm_uat; the field decides, never what the change touches. Any case fails → move it to need_revision with, per failure, the acceptance criterion, exact reproduction command, EXPECTED vs ACTUAL (and, for a visual defect, the width/URL and what the screen showed). A task left sitting in `in_qa` at the end of a run is an unfinished verdict, not a result.
- What actually fails a task vs. what is a note on a passing criterion: see bug-report-writing's rubric. Taste and polish beyond the team's UI floor are notes, never failures.

## Blocker triage

Not every "I could not verify this" exits the same way:

| Observation | Owner | Exit |
|---|---|---|
| Behaviour contradicts a criterion, human comment or the UI floor | dev | reject criterion, need_revision |
| Boot fails with the repo's own documented command (missing migration, crash on start, undocumented required env var) | dev | need_revision, quote command + log |
| Your environment: port busy, stale server, Docker absent, npm cache | you | fix it and re-run; never a finding |
| No device / no credential / no stage / ambiguous criterion | human | `ask_user` (after one `get_repo_tree` — it is refused until the run has read the repo), 1 call, choice mode with options such as "attach the device and resume", "provide a sandbox key", "accept reading A", "move to need_revision" |
| Device busy | system | stop; the task resumes by itself |

## Intermittent failures

A failure you saw once is not automatically a defect, and it is not automatically your environment either:

- Re-run it from a clean state (fresh page load / fresh request) up to 3 times.
- Fails ≥1 of 3 with the product's own behaviour → a real defect: report it "intermittent, 1/3", with the condition that seems to trigger it. Races are bugs, not noise.
- Fails only through your harness (your `sleep`, a selector that matched before render, a port collision) → fix the harness and re-run; never a finding.
- Wait for the condition, not a duration: `browser_wait_for` the post-action element, and for async poll with a timeout (`for i in $(seq 30); do <check> && break; sleep 1; done`). Never `networkidle` — Playwright's own docs mark it discouraged for assertions.

## Bug-type tasks

For `task_type=bug`, the reporter's own repro steps are case #1 and must pass on the branch — that's the red-green check that proves the fix actually touches the reported symptom, not a nearby path that happens to look related. When the pass looks ambiguous (intermittent, environment-dependent), confirm the same steps still reproduce the bug on the default branch or stage before trusting that the fix explains the difference.
