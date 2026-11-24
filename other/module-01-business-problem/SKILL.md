---
name: module-01-business-problem
description: 'Bootcamp Module 1: Discover the Business Problem. Use when the bootcamper starts or resumes Module 1, or wants to define their entity-resolution business problem, data sources, and success criteria.'
---

# Module 1: Discover the Business Problem

> **MCP grounding (mandatory — applies to this entire skill).** Every Senzing fact you present —
> SDK method and attribute names, config options, error codes, and entity-resolution specifics —
> MUST come from the Senzing MCP tools, never from training data, memory, or speculation.
> **Pre-response checklist:** if a reply contains any Senzing specific, you MUST have called an MCP
> tool this turn to obtain it; if not, stop and call it first. This has the same precedence as a ⛔
> gate. The full rule and tool routing are the "MCP-first invariant" in
> `../bootcamp-onboarding/ground-rules.md`.

Follow `../bootcamp-onboarding/ground-rules.md` throughout (👉 one-question-at-a-time,
MCP-first, file placement, checkpointing). Execute every numbered step one at a time, in
order. Never skip, combine, or abbreviate a step containing a 👉 question: this has the same
absolute precedence as a ⛔ mandatory gate.

**First:** Read `config/bootcamp_progress.json`, then (per ground-rules) show the module start
banner, journey map, before/after framing, a brief numbered overview of this module's steps, and an estimated time-to-complete (INV-096), before any module work.

**Before/After:** You may have seen a demo, but you don't yet have a defined problem or plan.
After this module you'll have a documented business problem, identified data sources, and clear
success criteria: the roadmap for everything that follows.

**Prerequisites:** None.

**Success indicator:** ✅ Business problem documented in `docs/business_problem.md` + data
sources identified + success criteria defined + bootcamper confirmation.

## Error handling

When the bootcamper hits an error during this module:

1. **SENZ error code** (INV-414; message contains `SENZ` + digits, e.g. `SENZ2027`): call
   `explain_error_code(error_code="<code>", version="current")` and present the fix. If it
   returns nothing, continue to step 2.
2. Present the matching pitfall/fix for this module (full `common-pitfalls` reference is a
   later porting phase; for now, use `search_docs` to look up the symptom).

## Phases

- **Phase 1: Discovery** (steps 1–6): `phase1-discovery.md`
- **Phase 2: Document and Confirm** (steps 9–17): `phase2-document-confirm.md`

(The former standalone steps 7–8 — the software-integration and deployment-target questions — are
now asked in **Phase 2 as Step 10a** (after the scenario is identified, before the problem statement
is written), per INV-097; Phase 1 ends at step 6 and Phase 2's numbering starts at 9.)

Read `current_step` from `config/bootcamp_progress.json` and resume at the right phase.
