---
name: design-conformance
category: qa
description: Use when your context carries "The approved design this task builds" - comparing the running UI with the approved hand-off and mockup at each width and state, evidence screenshots attached to the task, Blocker/High/Medium/Nitpick findings and which of them fail the round
---
# Design Conformance

## Overview

A task built from an approved design is tested against that design too. A human approved it before any code was written, and its hand-off spec is the contract the developer built to — an oracle like the acceptance criteria and the analysis spec. You read the design documents, never the code (black-box-testing), and compare what the running product shows with what they say.

**Core principle:** The approved design is the expected result. Same widths, same states, side by side — every finding cites the hand-off line or the mockup frame it contradicts, and the screenshot that shows it.

## Inputs

- **The hand-off spec** — `handoff: <screen>`, first under "## The approved design this task builds": the components, the tokens, every state, the breakpoints, the exact copy. Its header names the chosen mockup, `design: <screen> · <letter>`; the other variant documents were not chosen — never test against them.
- **The chosen mockup** — its text rendition follows the hand-off in your context. To see a frame's look, render it under `$QA`, never the workspace: `list_task_documents <design key>` with `raw: true` (follow `next_offset` to the end), write it with a quoted heredoc (`mkdir -p "$QA/design"; cat > "$QA/design/<slug>.html" <<'TT_HTML'` … `TT_HTML`), serve it on loopback (`nohup python3 -u -m http.server 0 --bind 127.0.0.1 --directory "$QA/design" > "$QA/design.log" 2>&1 & echo $! > "$QA/design.pid"`, the port is in the log), `browser_navigate` there and screenshot the frame you compare. Stop it by its PID (stop-what-you-started).
- **The task's scope** — where the task description and the design disagree, the description is the narrower scope and wins for this task; a part of the design outside it is not a finding.

## Cases

Add them to the matrix before you boot anything (scenario-plan-first): category `visual`, title prefix `design:` (`design: invoices empty 375 -> matches #a-375-empty`), linked to the criterion that names the state or the copy when there is one — the designer's hand-off criteria usually do. One case per state the hand-off lists, per width:

- **Web:** 1440 (`browser_set_viewport {device:"desktop"}`), 768 (`{device:"tablet"}`), 375 (`{device:"mobile", width:375}`) — the design's widths. The four-width overflow check (360 · 768 · 1024 · 1440, ui-visual-evidence) still runs on its own.
- **Mobile:** the phone frames on the device — portrait, and landscape where the hand-off draws it — and the tablet frames when the device or simulator is a tablet. A width you cannot reach is `skipped` with the reason, never assumed to match.
- **States:** default, loading, empty, error, success, dark, the longest content — each one the hand-off lists, reached from the outside: an empty search, a filter with no result, an invalid submit, a failing dependency (frontend-manual-testing's `route` recipe). A state you cannot reach is `skipped`, "not reachable from outside: <why>".

## Compare, in this order

1. **Layout and hierarchy** — the regions, their order, what comes first, the one primary action.
2. **Copy** — every string verbatim against the hand-off's Copy table; a paraphrase is a deviation.
3. **Components** — the one the hand-off names, in its variant (`browser_read_dom` / `mobile_read_ui` shows its role and label).
4. **Tokens** — colour, type size, spacing, radius as the design system holds them (`get_design_system`); `browser_read_dom` with `as_text: false` shows the classes and styles an element carries. A colour the design system does not hold is a deviation.
5. **States** — every listed state present, and drawn as designed.
6. **Responsive behaviour** — per breakpoint the hand-off lists.
7. **Visible accessibility it names** — labels, focus ring, status never colour alone, touch targets.

## Evidence

Every comparison shot of the running UI goes on the task, where the human sees it: `browser_screenshot` (`full_page: true`, no `width` after `browser_set_viewport`) or `mobile_screenshot`, with `attach_to_task: true` and `title: "<screen>-<state>-<width>"` (`invoices-empty-375`). Cite it by that title in the case's `evidence` and the criterion note, with the URL, the viewport report and what it showed — a title, never a path.

## Severity — what fails the round

| Severity | Means | Example | Verdict |
|---|---|---|---|
| Blocker | the screen fails the approved design on a core path | the primary action missing at 375; the layout breaks at 768; body text fails contrast | case `failed`, criterion rejected, need_revision |
| High | a deviation users will notice, or a design-system violation | the wrong component; an off-token colour; a missing empty state; key copy wrong | case `failed`, criterion rejected, need_revision |
| Medium | noticeable, minor | spacing one step off; secondary copy paraphrased; alignment | case `passed`, the deviation in its `notes` and the criterion note |
| Nitpick | polish | icon optical alignment; a 1px border difference | same as Medium |

A Blocker or High fails the round like any other failure (bug-report-writing, qa-fail-to-need-revision): the case `failed` with `actual` = what the screen shows, the criterion it breaks rejected with expected (the hand-off line, or the frame id such as `#a-375-empty`) vs actual and the screenshot title, and one line in the numbered need_revision index — `3. [AC4 · case "design: invoices empty 375"] empty state has no "New invoice" action — High`. A failed design case with no criterion to reject still fails the round. Medium and Nitpick never fail the task: they are notes, like any polish beyond the floor.

Write each finding as a problem, not a prescription: what the design says, what the screen shows, where (URL + width + region) — never "change the class".

## Red Flags

- Testing against a variant document that was not chosen.
- A `design:` case passed with no attached screenshot at that width.
- A finding taken from the diff or the source instead of the running screen.
- Taste the approved design does not state, reported as a finding.
- Every deviation a Blocker — or none above Nitpick on a screen that visibly differs.
