---
name: scenario-plan-first
category: qa
description: Use at the start of every QA round - recording the case matrix with record_test_cases (categories, criterion links, rejected cases) before touching the app, then executing all of it
---
# Case Matrix First

Before you boot anything or call anything, derive the cases — from the task description and its acceptance criteria, never from the code or the diff (techniques and sources: test-scenario-design) — and write them onto the task with `record_test_cases` (`status=planned`). Never post the plan as a comment; the card is where it lives.

The criteria are the floor, not the ceiling. They summarise the request in a few lines, so start from them and then ask what the person asking would expect to be true once this is built:

- One or more cases per acceptance criterion (happy path), linked with `criterion_id`.
- The implied cases nobody wrote down, with `criterion_id` empty (boundary-negative-testing for the data catalogue).
- Backend: the worker/async cases the request implies (worker-job-testing).
- Frontend: the visual cases at all four widths, empty/loading/error states (frontend-manual-testing).
- A regression case for the adjacent behaviour this change could break (regression-checklist).
- The cases you considered and REJECTED, as `status=invalid` with the reason in `notes`.

Then execute the matrix in this same run and record every verdict (`set_test_case_result`): `passed`, `failed` with what you actually observed, or `skipped` with what blocked it. A case still `planned` when you try to hand the task on refuses the move.

## Category mapping

The category enum has no accessibility/performance/security/contract value of its own — map them: a11y → `visual` + title prefix `a11y:`; performance → `other` + `perf:`; authz/security → `auth`; contract/compatibility → `negative` or `happy_path` depending on the case; concurrency/duplicate submission → `negative`; worker/async → `async`.

## Title convention

`<surface>: <action> -> <expected>`, e.g. `settings: rename to 81 chars -> 422`. Titles are the case's identity across rounds — keep them stable so a re-test (retest-after-revision) matches the right history.

## An untestable criterion

Is not a case you invent a proxy for. When there is a concrete choice between two readings, `ask_user` with the readings as options and leave it unapproved meanwhile. When it is unclear with no concrete reading to offer, reject it via `review_criterion` ("untestable as written: <why> — needs a sharper criterion") so the move to need_revision puts it in front of the human — a comment asking the PM to sharpen it reaches nobody, since the PM does not subscribe to in_qa.
