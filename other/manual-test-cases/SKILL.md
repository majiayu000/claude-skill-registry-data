---
name: manual-test-cases
description: >
  Write or review manual test cases that a non-technical product owner can execute by following
  exact click paths. Use whenever the user says "manual test cases", "test cases for product owner",
  "steps a non-tester can follow", "review the test cases", or asks for human-runnable test
  documentation. Every named entity is validated against seeders before delivery; ambiguous steps
  are rejected and rewritten. Output goes to tasks/manual_test_cases.md.
---

# Manual Test Cases — For a Product Owner

The reader has no testing experience and no codebase knowledge. If a step can be misread, it is wrong. If a named business, button, or page doesn't exist exactly as written, the case is broken.

**Scope:** write cases for what the user names (module, feature); no argument = full coverage with a module table first.

## Phase 1 — Map Reality

1. Rescan the codebase (within scope) for the real module/submodule list — never trust a stale doc. Produce a module table first when coverage is the goal.
2. Read the seeders. Build an inventory of every entity they create: names, states, relationships. This inventory is the only source of test data.
3. Read the views for the features under test: exact button labels, exact page titles, exact locations ("Full Preview & Edit — in the card footer").
4. When `tasks/requirements.md` acceptance criteria or `tasks/user_journeys.md` exist, they define the behaviors that must have cases — map each criterion/journey step to a case id, and flag any that can't be covered.

## Phase 2 — Write Cases

Per case, this exact shape:

- **ID** — module prefix + number (`BIZ-07`, `REV-03`), stable once assigned.
- **Title** — states the behavior under test, unambiguous on its own.
- **Preconditions** — exact setup commands (`php artisan migrate:fresh --seed`, which seeder class, which services must run: `queue:work`, `schedule:work`). Named data the case relies on, confirmed present in the seeder.
- **Steps** — numbered clicks. Step 1 is always an entry point: a full URL ("Open http://localhost:8000/businesses") or a named case's end state. Every step names its UI element exactly as rendered: "Click **Full Preview & Edit** (in the card footer)". Every entity by its real seeded name.
- **Expected result** — what the tester sees, concretely: badge color, banner text, row count, redirect target.
- **Result** — empty `PASS / FAIL: ____` line the product owner fills in during execution.

When the UI shows a failure branch (validation message, permission denial, empty state), that branch gets its own case — a PO can verify an error message as easily as a success banner.

### Rejection rules — fix before delivery, never ship these

1. **Phantom data** — a named entity not created by the referenced seeder. Either extend the seeder (say so explicitly as a precondition note) or rename to an existing entity.
2. **Impossible cases** — steps requiring UI that is hidden in the case's state (a button hidden for suppressed records). Flag and rewrite or drop; never leave an unexecutable case.
3. **Ambiguous references** — "the card", "the button", "the page" without an exact label and location.
4. **Hidden dependencies** — a case depending on a prior case's side effect must name that case in preconditions ("requires BIZ-14 executed first: that business is now suppressed").
5. **Duplicates** — two cases proving the same behavior; keep the clearer one.

## Phase 3 — Validate the Set

Before delivery, sweep the whole file:

- every entity name → confirmed in seeder inventory
- every button/page label → confirmed in views
- every case independently understandable, or its dependency explicitly named
- consistent ID numbering, no gaps or collisions

## Output Contract

1. Cases appended/updated in `tasks/manual_test_cases.md`, grouped by module.
2. A consistency note: entities validated, cases rewritten for clarity, impossible cases flagged, seeder changes required (if any).

## Review Mode

When asked to review existing cases instead of writing: apply the Phase 2 rejection rules case by case, list each violation as "CASE-ID — problem — proposed rewrite", and apply fixes on approval.
