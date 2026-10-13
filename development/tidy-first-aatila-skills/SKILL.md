---
name: tidy-first
description: 'Make the change easy, then make the easy change. Kent Beck''s tidy-first: prepare the landing zone for one imminent change. Use when you''ve picked an issue and are about to touch code (prefactoring), or when another skill (tdd, implement) needs the landing zone prepared. NOT a codebase-wide cleanup sweep (improve-*).'
---

# Tidy First

> **Make the change easy, then make the easy change.** — Kent Beck

Prepare the landing zone for a single imminent change, then make the change. The structural prep and the behavioral change are **two separate acts, two separate commits** — never one tangle.

Per issue, as the **zero step of implementation**:

```
pick issue → context_builder (blast radius + direction) → tidy-first → tdd (red → green → refactor)
```

## The two gates (this is the whole skill)

A candidate tidying may only be done if it passes **both**:

1. **Change-scope gate** — tidy *only what makes THIS change easier*. Not about to touch that code for this issue? You don't tidy it, no matter how messy — paying now for an option on an uncertain future change rarely covers its cost. A tidy with no behavioral change waiting behind it is a **sweep**.
2. **Direction gate** — tidy *only what is stable across your chosen approach*. If approach A and approach B would tidy different things, your direction isn't locked — resolve the fork (`grill-me` or a spike) first.

A candidate that fails either gate is **dropped** — but make the decision *explicit*: file it now if it's actionable and worth tracking (route to `improve-*` or the tracker), or consciously let it go. Never leave it as invisible "later" — that's how a codebase accrues chronic under-tidying.

## Tidy on green only

- **Suite red?** Get it green first. On a failing suite you can't tell a behavior-preserving move from a behavior-changing one — the one thing this skill keeps separate.
- **No tests on the blast radius?** Then "green" is meaningless. Write a characterization test to pin current behavior, or limit yourself to mechanical, tool-verified moves (IDE rename/extract) that preserve behavior by construction.

## Process

**0. Restate the change in one sentence.** *"I am about to change X so that Y."* This is the target both gates bite on. Can't write it? That's a `context_builder` / `grill-me` problem, not a tidying one.

**1. Curate the blast radius with `context_builder`** in **clarify** mode (or a directional `question`) — surface the files, functions, and seams this lands on, plus enough direction to judge the direction gate. **Not `plan` mode**: a line-level plan built against messy code bakes in the hard version of the change and defeats the skill. Directional thinking belongs here; the detailed steps emerge later, from the now-easier code. Fall back to `file_search` + `read_file` only when `context_builder` is unavailable or the change lands in one function you can already see whole.

**2. Find candidate tidyings inside the blast radius** — small, behavior-preserving legibility moves only. Run each through both gates; keep the survivors. Done when **every file in the blast radius has been read against this catalog** — not when you have "some" candidates.

   - **Guard clauses** — flatten nested conditionals into early returns
   - **Dead code** — delete unreached branches, unused params, stale flags
   - **Normalize symmetry** — make things that do the same thing look the same
   - **Reading order** — reorder so it reads as a reader needs; put things that change together next to each other
   - **Extract helper** — pull a confusing chunk into a named function
   - **Explaining variable / constant** — name a magic value or dense subexpression
   - **Rename** — give a vague name the domain word for what it does
   - **Chunk statements** — blank-line a long run into labelled paragraphs
   - **Delete redundant comments** — when a rename or extract made them noise

**3. Present the shortlist — and stop.** Each item gets one line: *why it makes THIS change easier* (not "cleaner"). Can't articulate that link? It fails the change-scope gate. Fifteen candidates is a sweep. **This shortlist is the skill's primary output. Do not edit yet.**

**4. Apply now, or hand off — the user's call.**
   - **Execute now.** Behavior must not change: same inputs, outputs, side effects. Run the existing tests/checks after tidying to confirm, then commit the tidy **in its own commit, separate from the behavioral change** — so a reviewer can read structure and behavior independently and revert either alone (squashing at the PR boundary is fine; the discipline is in how you author it, not the merge artifact). Continue to step 5.
   - **Hand off.** Don't touch code. Ask the user to run `/handoff` to capture the one-sentence change, the curated blast radius, and the approved shortlist (each item with its rationale, plus the execute discipline above) for a fresh session to execute. The skill ends here.

**5. Hand off to TDD** (only if you executed). Say: *"Structural prep committed separately — the change is now easy. Starting TDD."* Call the Skill tool with `tdd`, then make the easy change through red → green → refactor.

## Worked examples

Scenario throughout: *"I am about to add a `priorityFee` to the checkout total."*

- **Passes both gates.** `calculateTotal()` interleaves subtotal/tax/discount math over 40 lines; your change adds one term. Extract `applyDiscounts(subtotal)` so the slot for `priorityFee` becomes obvious and isolated. Easier *and* stable across approaches. **Do it.**
- **Fails change-scope.** `formatReceipt()` has the same interleaving — but your change never touches it. No behavioral change behind it. **Drop; file an issue only if genuinely worth it.**
- **Fails scope, wrong skill.** The real friction is pricing spread across three modules that "should" be one `Pricing` service. True, but that's a risky depth refactor. **File it, route to `improve-codebase-architecture`. Don't smuggle it in.**

## Boundaries

- **`improve-codebase-architecture` / `improve-codebase-colocation`** — codebase-wide depth/placement sweeps; tidy-first is bound to one imminent change.
- **`aa-commit-clarity`** — splits code you *already* mixed (reactive); tidy-first sequences the work so structure and behavior are never mixed to begin with (proactive).
- **`tdd`'s post-green refactor** — that's tidy-*after*. tidy-first tidies *before* the first red; the two bookend the loop.
