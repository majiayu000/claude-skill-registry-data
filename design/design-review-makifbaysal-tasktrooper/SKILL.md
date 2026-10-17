---
name: design-review
category: design
description: Use when a design task asks you to compare a built screen with its approved design - screenshots at 1440, 768 and 375 attached to the task, Blocker/High/Medium/Nitpick triage, evidence per finding, problems not prescriptions
---
# Design Review

## Overview

A design review answers one question: does the built screen match the design the human approved? It is a comparison against a contract, not a fresh critique — taste that is not in the approved design is not a finding. You report problems; the developers decide the fix.

**Core principle:** Same widths, same states, side by side — every finding cites what the approved design says and what the build shows.

## Inputs

- **The approved design:** the design task this review points at (its key is in the description, `blocked_by` or `derived_from`; its documents are in your context under "## The approved design this task builds" when this task is blocked by it) — `list_task_documents <key>`: the `handoff: <screen>` spec, which names the chosen `design: <screen> · <letter>` mockup, and that mockup (`raw: true` for its source, to render it). The other variant documents were not chosen; never review against them.
- **The built screen:** the URL the description names (a preview or staging address), or the app started locally the way `get_project_brief` says — detached, its log under `/tmp/tt-<task key>/`, on loopback. Installing dependencies to run it is not a change; editing a source file is.
- `get_design_system` for the repository — the tokens the build must use.

## Procedure

1. Render the approved mockup (screen-mockup-html's self-check) and open the built screen in the same browser session, one after the other.
2. At each width — `browser_set_viewport` `{device: "desktop"}` (1440), `{device: "tablet"}` (768), `{device: "mobile", width: 375}` — `browser_screenshot` the built page (`full_page: true`, no `width`, `attach_to_task: true`, `title: "<screen>-built-<width>"`, plus `-<state>` for a state: `invoices-built-375-empty`) and the matching mockup frame (no need to attach it — it is on the design task already).
3. Reach every state the build allows from the outside: an empty search, a filter with no results, an invalid form submit, the error a disconnected API produces if the brief names one. A state you cannot reach is listed as "not reviewed", never assumed to match.
4. Compare in this order: layout and hierarchy → content and exact copy → components (the right one, the right variant) → tokens (colour, type, spacing, radius — `browser_read_dom` with `as_text: false` shows the classes an element carries) → states → responsive behaviour → visible accessibility (labels, focus ring, text alternatives, touch target size).
5. Triage every difference:

| Severity | Means | Example |
|---|---|---|
| Blocker | the screen fails the approved design on a core path | the primary action is missing at 375; the layout breaks at 768; body text fails contrast |
| High | a deviation users will notice, or a design-system violation | wrong component; an off-token colour; a missing empty state; key copy wrong |
| Medium | noticeable, minor | spacing one step off; secondary copy paraphrased; alignment |
| Nitpick | polish | icon optical alignment; a 1px border difference |

6. Write each finding as a problem, not a prescription: what the approved design says (`#a-375-empty`, or the hand-off line), what the build shows, where (URL + viewport + region). "Overdue status is shown by colour alone; the approved design pairs it with the word Overdue (handoff: Accessibility)" — not "add a span to InvoiceRow.tsx".

## The document

ONE document on the design task, titled `design review: <screen>`: a verdict line at the top (matches / does not match, counts per severity), the findings table (id · severity · width · where · expected · actual · screenshot), the states not reviewed and why, and one line on what matches. Each finding's evidence is the attached screenshot by its title, the URL, the viewport and what the screenshot showed; say them exactly — a title, never a path.

Then stop like any design task. On approval (`done`), the Blocker and High findings become one bug task per repository; Medium and Nitpick stay in the document unless the human asked for them.

## Common Mistakes

- Reviewing against your own taste instead of the approved design.
- Comparing the 1440 build with the 375 mockup frame.
- Prescribing code ("change the class to …") instead of naming the gap.
- Calling a state "fine" that you never managed to open.

## Red Flags

- A finding with no width, no URL or no attached screenshot.
- Every finding rated Blocker — or none rated anything but Nitpick on a screen that visibly differs.
