---
name: processing-uat
description: Turn a completed UAT into a prioritised fix plan and then fix it. Reads a UAT markdown file (or its results.json) that a tester has filled in, diagnoses every failure, look-and-feel complaint and tester-reported finding against the actual code, and produces a plan grouped by severity. Use when a UAT has been submitted, when the user says "process the UAT", "the tester finished", "here are the UAT results", or points at a file with failed acceptance tests.
---

# Processing a completed UAT

Input: a UAT markdown file written by the **creating-uat** skill and filled in by a tester. Output: a
fix plan you can execute, grounded in the code rather than in guesses about what the tester meant.

## Phase 0 — Load and sanity-check the run

1. Find the file. If the user did not name one, look in `docs/uat/`, then `uat/`, and prefer the most
   recently modified `UAT-*.md`. If several exist, ask which one.
2. Read the summary block at the top (`<!-- uat:summary:start -->`). It gives run status, counts, the
   failed test IDs and the IDs carrying look-and-feel concerns.
3. Read the sidecar `<name>.results.json` if present — same data, already structured.
4. **Check the run status.**
   - `COMPLETE` — proceed.
   - `PARTIAL` — say so up front, list the unanswered IDs, and ask whether to proceed on what exists
     or wait for a full run. Untested surfaces are unknowns, not passes; never report them as passing.
   - No summary block, or every status is `_not answered_` — the tester has not submitted. Stop and
     say so.
5. Note the tester's name and `last_run` date from the meta block. If the code has moved on since,
   flag that some failures may already be fixed.
6. Read `tester_level` from the meta block — it changes how you read the evidence:
   - **novice** — notes are describing symptoms, not causes. "It didn't work" plus a screenshot may be
     the whole signal. Lean on the screenshot and reproduce the step yourself before concluding
     anything. Expect some failures to be the tester losing their way rather than the app breaking.
   - **intermediate** — notes usually name the screen and the error text. Trust them, verify in code.
   - **expert** — notes may already contain a diagnosis. Treat it as a strong hypothesis, not a
     finding: confirm it in the source before you act on it, and say so if you disagree.

## Phase 1 — Collect every issue

Three streams, all of which matter:

| Stream | Where it lives | Why it counts |
|---|---|---|
| **Failures** | tests with `**Status:** FAIL` | the app did not do what the checklist said it would |
| **Not done** | tests with `**Status:** NOT DONE` | usually blocked by an earlier failure — the note says why. These are untested surfaces, and often hide further bugs |
| **Look & feel concerns** | any `**Look & feel concern:** (Severity) ...` line, including on tests that **passed** | the app works and the user still does not want to ship it like that |
| **Tester findings** | the `<!-- uat:findings:start -->` section | problems no test asked about — often the most valuable items in the file |
| **In-app annotations** | `— Annotated …` lines inside a test's Notes | pins the tester dropped on the running app. Each carries the element it sits on (`button#save “Save”`), the URL, the viewport and any console error at that moment — the most directly actionable evidence in the file |

Read every screenshot the tester attached (`docs/uat/assets/<slug>/…`) with the Read tool. A picture
frequently contains the error text the tester paraphrased.

Annotated captures (`<id>-annot-<n>.png`) are **re-renders of the page, not photographs** — the tester
confirmed they looked right, but treat fine pixel detail with suspicion and trust the pin's element
selector over the picture. That selector is usually the fastest route into the code: search for the id,
class or text it names before reading anything else.

## Phase 2 — Diagnose each issue against the code

For every item, before proposing anything, decide which of these it is:

1. **A real defect** — the code is wrong. Find the root cause in the code; cite `file:line`. Do not
   propose a fix you have not located in the source.
2. **A checklist defect** — the test was wrong, ambiguous, or described a feature that does not work
   the way the UAT claimed. The fix is to the UAT, not to the app. Say so explicitly.
3. **An environment problem** — the tester's machine, a port already in use, a missing prerequisite,
   stale containers. The fix is usually a better setup step in the UAT plus a clearer error message.
4. **A deferred feature reached by accident** — the tester tested something out of scope. Fix the
   scope section, not the code.
5. **A design decision the tester disagrees with** — legitimate, but it is a product call. Surface it
   to the user, do not silently redesign.

Use the note the tester wrote and the screenshot as evidence, then confirm it in the code. When the
note is too vague to act on, list it as **needs clarification** with the exact question to ask the
tester — do not invent the missing detail.

## Phase 3 — Write the fix plan

Write `docs/uat/UAT-<slug>-fixplan.md` next to the UAT, ordered by severity:

```markdown
# Fix plan — <app> UAT, run <date> by <tester>

Source: docs/uat/UAT-myapp-2026-08-23.md (COMPLETE — 41 pass, 4 fail, 2 not done, 6 concerns, 3 findings)

## Blocking — the app is broken
### B1. Saving a report does nothing (UAT 3.2, screenshot attached)
- **What the tester saw:** clicked Save, nothing happened, no message.
- **Root cause:** `apps/web/src/report-form.tsx:88` — the submit handler swallows the 422 and never
  renders the error.
- **Fix:** surface the validation error and keep the form open.
- **Verify by:** re-running UAT 3.2; it must show the red "Title is required" message.

## Should fix — works, but the tester objected
### S1. Terminal output scrolls too fast to read (UAT 1.2, Annoying)
...

## Cosmetic
...

## Not a code problem
### N1. UAT 2.1 could not be done — blocked by B1, not a separate defect.
### N2. UAT 4.3 says the button is called "Export"; it is called "Download". Fix the checklist.

## Needs clarification from the tester
### Q1. Finding F2 says "it looked wrong" with no screenshot — ask which screen.
```

Rules for the plan:

- **Every entry cites its UAT id** so it can be traced back, and `file:line` where a code change is
  proposed.
- **Every entry names how to verify the fix**, ideally by re-running the same numbered test.
- Severity comes from the tester's own rating for concerns (`Blocks me` / `Annoying` / `Cosmetic`) and
  from your judgement for failures. Do not quietly downgrade something the tester called blocking.
- Group duplicates: several failures with one root cause become one entry listing every affected id.
- Nothing is dropped. If an item needs no action, it goes under "Not a code problem" with the reason.

## Phase 4 — Agree, then execute

1. Show the user the plan grouped by severity, with counts, and ask what to do: everything, blocking
   only, or a subset.
2. Work the agreed items in order, most severe first.
3. For each fix, make the change and verify it the way the plan said.
4. Update the checklist itself where the UAT was wrong (Phase 2 case 2 or 4) — a wrong test will waste
   the tester's time on every future run. After editing the `.md`, regenerate the form:
   `python docs/uat/tools/generate_uat_html.py docs/uat/UAT-<slug>-<date>.md`
5. Report what was fixed, what was left, and which UAT ids should be re-run.

## Phase 5 — Set up the re-run

A fixed app needs a clean re-run, not an edited old one. Start a fresh run by copying the checklist to
a new date, clearing the previous answers:

```bash
python docs/uat/tools/generate_uat_html.py docs/uat/UAT-myapp-<new-date>.md
```

Keep the completed old file — it is the record of what was found and when. If only a handful of tests
need re-checking, say which ids and let the tester use **Submit what I have so far**.

## Reference

The file format, marker syntax, status encoding and `results.json` shape are documented in the
**creating-uat** skill under `references/uat-file-format.md`.
