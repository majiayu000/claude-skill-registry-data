---
name: pm-uat-review
category: pm
description: Use when a task is in pm_uat - verify every acceptance criterion and the human's comments yourself in the browser, on a device, or over a loopback HTTP request, record a verdict per criterion, then move to human_uat or need_revision
---
# PM UAT Review

## Overview

pm_uat is the PM's own gate, not a rubber stamp on QA's work. You have no code-reading tools here — `codebase_search`, `grep_code`, `get_repo_tree`, `read_file` and the rest are gone in this column — so your verdict can only come from evidence you produced yourself this run: a browser walk-through, a device walk-through, or a direct HTTP request. There is no backend exception: a criterion with no screen still gets your own executed evidence, never a pass on QA's word alone.

## 1. Inputs

- The task's ORIGINAL description and every acceptance criterion.
- The human's requirement comments on the task (injected as "The human's requirements written on this task"). Where they disagree with the original description or a criterion, **the comment wins** — and what it asks for needs evidence like any criterion.
- QA's evidence: the `review_criterion` note on each criterion, and `list_test_cases` for `passed` cases matching `criterion_id`. Both are a **cross-check**, never a substitute — you still walk every criterion yourself, covered or not.

## 2. Get a URL — never production

First one that applies: `get_task_preview` — a preview that is `ready` AND `built_from_pr_head` (its `open_url`); else `get_deploy_target` with `env="stage"`, if this repository has a stage environment recorded; else `start_task_preview` and use its `url` once one appears (call it again if the URL isn't there yet — it will not restart a preview already starting).

## 3. Walk each criterion

**UI-observable criteria:** `browser_navigate` → `browser_wait_for` → `browser_fill`/`browser_click` through the flow, `browser_screenshot` as evidence. Check at phone (`browser_set_viewport {device:"mobile", width:360}`) and desktop at minimum for anything visual.

**API-only criteria (no screen to walk, usually `task_type: "technical"` or a backend criterion on a `task`/`bug`):** boot the task branch with `start_task_preview`, then use `http_request` against that preview's `http://127.0.0.1:<port>` URL (the tool refuses anything that is not this machine, so a stage or production URL is never an option for it; a read-only stage check is `fetch_url`) to exercise exactly what the criterion asks: happy path, invalid input, unauthorized/forbidden, whatever the criterion names. This is not optional and not QA's job to cover for you — every API criterion gets your own request in this run.

**Evidence note format** (cite it in that criterion's own `review_criterion` note):
- UI: `Observed: <exact text/value/state> at <url> [360px|desktop|device] — <what the screenshot showed>`
- API: `Observed: <METHOD> <path> [+ body if relevant] → <status> <content-type>; <response excerpt that proves or disproves the criterion>`

A note that only says "verified" or "works" is a Red Flag — it has to name what you saw.

## 4. Mobile path

The PM holds the `mobile_*` tools — use them on a mobile repository, mirroring QA: `mobile_launch_app` → `mobile_wait_for` → `mobile_tap`/`mobile_type_text`/`mobile_swipe` → `mobile_screenshot`/`mobile_read_ui` → `mobile_release_device`, always last, whether the walk-through passed or failed. Check portrait and landscape (`mobile_rotate`) at minimum per UI criterion. If any `mobile_*` call reports the device in use, stop — the run is parked and resumes by itself; never retry or guess at a verdict without the device. `mobile_launch_app` installs the build registered on the repository's deploy target, not necessarily your exact task branch — say in the note which build you observed if that distinction matters to the criterion.

## 5. Stakeholder-eyes pass

One walk of the original request as the requester would make it, independent of the criteria list. Look for:
- wrong content language (not the product audience's language)
- placeholder text (`lorem`, `TODO`, `{{…}}`)
- a broken image or a bare "?" icon
- horizontal overflow (the `browser_set_viewport` report lists overflowing elements)
- a missing empty or error state the request implies but no criterion named

## 6. Classify every finding

- **Breaks a criterion, a human comment, or the original request** → a gap → reject the criterion(s), `need_revision`.
- **A new idea not asked for** → `create_board_task` in backlog (priority low, same repository/project). Never a gap, never blocks approval.

## 7. A human comment supersedes a criterion

Use `cancel_criterion` with a reason quoting the comment, then verify the comment's own version of the behaviour and cite it in the note of the criterion closest to it.

## 8. Re-entry after need_revision

Re-walk the previously rejected criteria first, then all the rest — moving goalposts is not allowed in either direction. A new gap found on re-entry must trace to a criterion, a human comment, or the original request; otherwise it's a backlog task (step 6), not a reason to bounce the task again.

## 9. Output

- **Pass:** every criterion has your own executed evidence and is approved via `review_criterion`. Move to `human_uat`. Write **no comment** — the move and the approved criteria are the verdict.
- **Fail:** reject the failing criteria via `review_criterion` with expected vs actual, one numbered `add_task_comment` gap list, move to `need_revision`.

Never approve by reading code. Never approve off QA's notes, a passed test case, or the diff alone — "I looked at the code and it looks good" and "QA already tested this" are both forbidden; only evidence you executed yourself, this run, counts.

## Worked Example

Task: "Add task export endpoint" (`task_type: "technical"` — skips pm_uat, routed to human_uat by QA directly) vs. "Add export button to the project board" (`task_type: "task"`, UI-facing):
- AC: "Given the board, When I click Export CSV, Then `<project>-tasks.csv` downloads and the row count matches the board." → `browser_navigate` to the preview, `browser_click` Export, confirm the download, screenshot. Approved, note: "Observed: `acme-web-tasks.csv` downloaded at <url> desktop — 42 rows, matches board count."
- AC: "Given the export is in progress, When I click Export again, Then the button is disabled and no second file downloads." → walked, button stayed enabled, a second file downloaded. Rejected, note: "Expected: disabled during export. Actual: button stayed clickable, two files downloaded." One gap-list comment, `need_revision`.

## Common Mistakes

- Treating a `passed` QA test case as enough — you still have to run it yourself.
- Skipping an API-only criterion because "nothing to click" — use `http_request`.
- Writing "verified" in a note instead of the exact observable.
- A "PM UAT passed" comment on a clean pass — the column wants no comment at all.
- Editing `acceptance_criteria` here instead of `cancel_criterion` when a human comment supersedes one.
- Re-litigating an already-approved criterion on re-entry instead of focusing on the rejected ones.

## Red Flags

- A `review_criterion` note that says only "works" or "verified".
- An approval with zero tool calls in this run's transcript.
- A gap list comment with no expected-vs-actual.
- A new idea folded into the gap list instead of a new backlog task.
