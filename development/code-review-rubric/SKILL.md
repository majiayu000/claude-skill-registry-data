---
name: code-review-rubric
category: quality
description: Use when a task is in code_review - how to read the diff, which findings block, and the verdict move
source: obra/superpowers (MIT), adapted
---
# Code Review Rubric

## Overview

Every task a developer finishes lands in code_review as a pull request. You are the last technical gate before QA. Review the PR diff against the task's acceptance criteria and the spec/plan — identify issues before they cascade.

**Review is reading, not running.** The PR link and its diff are in your context — the file list (`git diff --stat`) in full, the patch cut at 24,000 bytes, ending `…(truncated)` when it was. You do not boot the app, run a build, run a test suite, or verify behaviour by executing it — the pipeline did that before you and QA does it after you. You also never edit the diff: a finding is written down and handed back, never fixed by the reviewer.

## Before Reviewing

1. `list_task_comments` — the only way to see an earlier need_revision comment (yours, QA's or the pipeline's). A re-submission enters code_review from `in_progress`, so that history is NOT re-injected. If one exists, load root-cause-review.
2. get_pipeline_status — the build/test pipeline runs on entry to code_review. Red pipeline → the task cannot pass review regardless of the diff.
3. Read the task description, every acceptance criterion, the human's requirement comments on the task (injected as "The human's requirements written on this task"; `list_task_comments` shows them as `author_type=user`), the spec/plan reference, and any comment the developer left — a run that went cleanly leaves none, so the absence of one is normal and says nothing about the change.
4. Read the injected PR diff completely, including every file the 24,000-byte cut left out — `run_terminal`: `base=$(git merge-base HEAD origin/HEAD 2>/dev/null || git merge-base HEAD origin/main); git diff "$base" -- <path>` (reading, not running), or `read_file`. Never give feedback on code you didn't actually read, and never approve a file you did not see.
5. Check the repo's own `CLAUDE.md`/`AGENTS.md`/`CONTRIBUTING.md` for rules this diff might break — a violation is Important, quoted verbatim.

## What to Check

**Plan/AC alignment**
- Does the implementation match the plan, the acceptance criteria and the human's requirement comments? Is anything missing? Is anything extra beyond all of those (scope creep)?
- The human's comments on the task outrank its description: a later comment that widens or changes the scope ("show the logos in the marquee too") makes that work part of THIS task, even when the description's out-of-scope list says otherwise. Review it like any criterion; never flag it as a scope violation or ask for it to be reverted or split.
- Are deviations justified improvements or problematic departures? Flag them specifically so the developer can confirm intent.

**Code quality**
- Clean separation of concerns, proper error handling (no swallowed errors), type safety, DRY without premature abstraction, edge cases handled.

**Architecture**
- Sound design decisions, integrates cleanly with surrounding code, respects layer boundaries (hexagonal: domain imports no adapters).

**Domain impact (what the diff breaks outside itself)**
- The diff is the subject of the review; its blast radius is not limited to the diff. A change is only correct if the code that depends on it is still correct.
- Read outside the diff whenever it touches something shared — a domain type or its invariants, an interface or function signature, a DB query or migration, an API/event contract, auth or tenancy scoping, a default value, a shared component. Use grep_code for the exact symbol, expand_symbol_context to read the callers, codebase_search for the concept, get_symbol_skeleton for structure.
- Concrete questions: who else calls this and do they still hold? Does the migration break rows already in the table, or a reader deployed before it? Does a changed contract have a consumer in another repository (the task's project has more than one)? Did a renamed/removed field leave a stale reader? Does a new query bypass the tenant/user filter its neighbours apply?
- Report an impact finding like any other: name the file:line OUTSIDE the diff that now breaks, and what in the diff breaks it. "Might affect other callers" is not a finding — the callers are one grep away.
- Reading the repository for this is expected. Reviewing files the PR does not touch is not: unrelated pre-existing problems are at most a Minor note, never a reason to hand the task back.

**Security**
- Input validated at boundaries, parameterized queries, no secrets in code or logs, new endpoints behind the same auth as neighbors.
- Load security-review for anything touching input handling, auth, queries, files, outbound requests, secrets, dependencies or LLM calls — it has the full checklist and severity mapping.
- Load migration-and-contract-review for any migration, endpoint/DTO, event payload or shared-type change — a rollback here is a `git revert` that leaves the schema in place.

**Testing**
- Tests verify real behavior, not mocks. Edge cases covered. New behavior has tests in the same diff. Pipeline green.

**Frontend / UI changes (web)**
- Component placed at the right atomic level and reused instead of rebuilt — `INVENTORY.md` updated for any new component.
- Presentation-only below pages: atoms/molecules/organisms/templates take props in and callbacks out — no data hooks, no API calls.
- Semantic tokens only — no raw palette classes, no hex, no arbitrary px values; `ui-guard` green if the repo has it.
- Mobile-first classes (unprefixed = phone, `sm:`/`md:`/`lg:` upward) — no fixed pixel widths, no `h-screen`.
- Required states present: loading/empty/error on data views, hover/focus-visible/active/disabled on controls.
- Accessibility basics: visible labels, focus-visible rings, icon-only buttons have accessible names.
- The visual check is not yours to re-run or to demand: a frontend hand-off without a screenshot is refused by the system, and QA screenshots all four widths in in_qa. You judge the code that causes those bugs — a fixed pixel width or `w-[Npx]` on a layout box, `h-screen`, a `max-*:`-first layout, a flex/grid child holding text without `min-w-0`, a hover-only control, a missing loading/empty/error branch. Each is Important with the file:line.

**Mobile UI changes** (a mobile repository's diff is not judged by the web rules above)
- Component placed at the right atomic level for that repo's library, and `INVENTORY.md` updated.
- Theme tokens only (`ui-guard`-equivalent test green if the repo has one) — no hard-coded colours or sizes.
- Required states present: loading/empty/error.
- Touch targets ≥ 48dp (Android) / 44pt (iOS), and icon-only controls carry an accessible label.
- A size-matrix test exists for a changed layout (phone, tablet, both orientations).
- The closing message names the render path used (device/simulator/widget previewer) and the matrix it checked — that is the mobile equivalent of the web four-width evidence, and its absence on a layout change is a finding.

## Severity Calibration

Not everything is Critical:
- **Critical (must fix):** bugs, security issues, data loss risk, broken functionality, or a weakened/deleted test.
- **Important (should fix):** unmet acceptance criterion, architecture problems, missing error handling, real test gaps.
- **Minor:** style, optimization opportunities, polish. Never blocks and is never a comment on its own — list it only at the end of a need_revision comment under `Minor (optional):`.
- **Frontend specifics (must-fix, Critical or Important):** a duplicated/re-built component, raw or off-palette colours, a missing required state, or one of the layout bugs named above (fixed width, `h-screen`, missing `min-w-0`, …) found in the code.

For each finding: file:line, what's wrong, why it matters, how to fix if not obvious. In a need_revision comment you may add ONE line on what is right and should be kept, so the developer does not undo it — never a comment for praise alone.

## Worked Example (a finding done right)

> **Critical — internal/application/export/service.go:24.** `ListByProject` error is ignored (`tasks, _ := repo.ListByProject(...)`): on a DB failure the export returns an empty CSV as if the project had no tasks — silent data loss. Fix: propagate the error and map it to 500. Blocks: unmet AC2 (must surface failures) + swallowed error.

Contrast the useless version: *"improve error handling in the export service."* The good finding names the file:line, the exact mechanism, the user-visible consequence, and the fix — the developer can act without a second round-trip.

## Verdict (mandatory — never leave without one)

- Pipeline green AND no Critical/Important findings → `move_board_task` to **ready_for_qa** and write nothing: the move, the green pipeline and the history are the record (add_task_comment's own contract).
- Pipeline red OR any Critical/Important finding → move_board_task to **need_revision** with a numbered comment: each item quotes the acceptance criterion or exact defect location and states what must change. Put every Critical/Important finding in this ONE comment — a second round judges only the prior points plus what the new diff changed; three moves into need_revision without a human touch park the task automatically, so a real design disagreement belongs there, not a fourth round-trip.

## Never

- Say "looks good" without having read the diff.
- Run the app, a build, or a test suite to review it — reproducing the pipeline burns the run and answers a question that already has an answer.
- Fix a finding yourself, or push anything to the branch. You write findings; the developer writes code.
- Mark nitpicks as Critical, or block on Minor findings.
- Be vague ("improve error handling") — every finding is actionable.
- Approve by assumption — cite the diff and the pipeline result.
