---
name: analiz-task-workflow
category: workflow
description: Procedure for an analiz (analysis) task when you hold the analyst role. Use when a task with task_type analiz is assigned to you and add_task_document is in your tool list.
---
# Analiz Task Workflow

The system-architect normally owns analiz tasks. The human can grant a developer the analyst role for an area (Settings → Roles); when that happens, an analiz task is dispatched to you instead of the architect. Your prompt's step 1 already tells you how to tell the two cases apart: `add_task_document` in your tool list means you ARE the analyst for this task — follow this skill. Otherwise comment that it is misassigned and take no other action.

## Which instructions apply

An analiz task is not a code task. The standing acceptance criteria (build, suite, unit test), TDD, and the code_review hand-off that the rest of your prompt and columns describe do **not** apply here — the deliverable is a document, not a diff. File edits are discarded: an analiz task never publishes a branch and `commit_task_changes` refuses it — a run that produced edits on this task type has done the wrong job on the wrong task, and those edits reach nobody.

## Explore

Ground every claim in code you actually opened in this run: `get_repo_tree`, `codebase_search`, `grep_code`, `get_symbol_skeleton`, `expand_symbol_context`. Name the real files, symbols and interfaces you found. A document that describes a codebase you did not open is rejected.

## Deliverable

ONE report, via `add_task_document` with `format: "html"`, titled `analiz: <YYYY-MM-DD> <topic>`. Required sections, each with a stable id, in this order:

- `summary` — what is being built and why, in 3–6 sentences, plus one decision callout stating the chosen approach.
- `context` — current state, grounded in code you read: real file paths and symbols, with what each does today.
- `design` — proposed components with exact interfaces (names, parameter and return types), data flow, error handling, the 2–3 approaches you weighed with the one-line reason the chosen one won, and out-of-scope items named explicitly.
- `plan` — numbered implementation steps (`step-1`, `step-2`, …): files to create or modify, the interfaces each step consumes and produces, and the TDD cycle with the actual test code and the command that runs it. No placeholders — "add error handling", "similar to step 2" and "TBD" are plan failures.
- `split` — one row per repository/layer: the one-line scope of its implementation task, the plan steps it owns, and its order (`blocked_by` / `deploy_depends_on`).
- `risks` — each risk with its mitigation. Open questions never go here (or anywhere in the HTML) — see "Open questions" below.

This mirrors the system-architect's own analiz-html-report skill — follow its HTML rules (one self-contained document, no `<script>`, no external resources, light/dark via CSS variables, under ~150 KB) and its template.

## Open questions

A genuine product decision the code cannot settle is recorded with `record_open_questions` — never written into the report as prose, and never asked with `ask_user` (you do not hold `ask_user` on an analiz task). The system renders every recorded question as an answer box above your report; the human answers there, not in chat.

Each question is `blocking` (the analysis cannot responsibly continue without the answer — the exception: two incompatible product behaviours with no basis to choose, an external contract you cannot see, a scope choice that changes which repositories are touched) or non-blocking (a reasonable default exists — the default: record it with `recommended_answer` and keep working). `recommended_answer` is required whenever `blocking` is false.

A blocking question does not end the run early — explore everything else first and attach the report as far as it got (`add_task_document`/`update_task_document`), then `record_open_questions`, a summary comment, and STOP: the run ends in `blocked` instead of `analiz_review`, report attached. Re-dispatched after an answer (`resumed: "questions_answered"`, or new answers in your run context) — `list_open_questions` if you need the full picture — continue the SAME report with `update_task_document`, and withdraw or replace any question the answer made moot.

On a revision or in later runs: honour every answer, the same way you honour review comments. An unanswered non-blocking question means its `recommended_answer` stands — do not re-ask it.

## Revision

When the task comes back through `need_revision`: read the review comments (they are in your run context under "Review comments on your analysis document"; `list_document_annotations` with status `submitted` returns every one) and the report's current source (`list_task_documents` with the document's id and `raw: true`, following `next_offset` until you have it all). Fix every comment at its root — re-read the code where a comment questions a fact — with `update_task_document` on the SAME `document_id`: `edits` (each `old_text` copied exactly from the source) for targeted passages, `content` for a rewrite. Keep the section and step ids. Honour every answered open question the same way (see "Open questions" above). Never attach a second document — the card ends with ONE current report.

## Criteria

Tick only the acceptance criteria your report actually answers.

## Close

End the run with a summary comment: your approach, the report's title, and the project/task split you intend. Then STOP. When the run ends with the report attached and no pending blocking question, the system moves the task to `analiz_review` for you; a pending blocking question moves it to `blocked` instead. Never move it yourself, and never to `done`. Create no implementation tasks — the system-architect decomposes them after the human approves your report, the same way it does for its own analyses. No `git push`: nothing here is committed.

## Red Flags

- Editing repository files on an analiz task — they are discarded; write the document instead.
- A second `add_task_document` on a revision — revise the existing one with `update_task_document`.
- Moving the task yourself, or moving it to `done` or `code_review`.
- Writing a question as prose in the report, a task comment, or with `ask_user` instead of `record_open_questions` — you do not hold `ask_user` on an analiz task.
- A non-blocking question with no `recommended_answer` — refused; decide what you're proceeding on.
