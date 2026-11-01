---
name: drawing-checklist
description: "This skill should be used when the user needs a phase-specific drawing-set checklist for an architectural project — SD, DD, CD, or IFC. Trigger on 'make a checklist', 'drawing set review', 'CD checklist', 'DD set review', or pasted phase + project-type context. Generates a structured checklist markdown in `docs/checklists/` and updates the project checklist index."
license: MIT
metadata:
  title: "Drawing Checklist"
  summary: "Get a drawing-set checklist for the phase you are in"
  discipline: "construction-admin"
  tags: "Design"
---


# Drawing Checklist


## Overview


Generate a phase-specific drawing-set checklist (SD / DD / CD / IFC) for an architectural project, scoped to project type and primary discipline, with cross-discipline coordination flags. The checklist lives in `docs/checklists/` and serves as a working punch-list before issuing the set.


## Scope and limits — read first


**What this does.** Builds a checklist for one phase, one project type, and one
discipline: the sheet series that phase expects, the level of detail expected on
each, the items that commonly go missing, and the cross-discipline flags worth
raising now. It lands in `docs/checklists/` as a punch list to work through
before the set is issued.

**What this does not do.**

- **It does not open your drawings.** The checklist says what should be there.
  Confirming that it is there is the pass you make against your own set.
- It does not judge design quality. Completeness only; critique is
  `design-critic`.
- It does not check code compliance. A complete set can still fail code, and
  that is `code-compliance-review`.
- It does not produce structural or MEP checklists. Architecture is the primary
  discipline here and the others appear only as coordination flags.
- It does not know your contract's thresholds. The percent-complete figures are
  the industry convention, and where your agreement defines its own, yours
  govern.

**What you need before starting.** The phase, the project type, and the
discipline. If your office standards or your owner-architect agreement set their
own deliverable thresholds, have those in front of you.

## When to use


Trigger on:

- Phase + project-type context ("DD set for a 5-story commercial", "IFC review for civic project").
- Explicit asks: "make a checklist", "review the drawing set", "DD set review", "CD checklist", "drawing checklist for <phase>".
- Pre-issue review of a drawing set when the user wants a structured pass.

Do NOT trigger for design critique (use `design-critic`), RFI generation (use `rfi-writer`), or general drafting standards questions.


## Workflow


### Step 1 — Bootstrap if needed


Check `docs/checklists/index.md` exists. If not:


```bash
python scripts/init_checklist_workspace.py
```


### Step 2 — Gather context

- Read `docs/project.md` if present for site, program, scale, project type.
- Identify the **phase** (SD / DD / CD / IFC), **discipline** (architectural primary, with structural/MEP coordination notes), and **project type** (residential / commercial / civic / mixed-use / industrial).
- If the phase or project type is ambiguous, ask one clarifying question before continuing.

### Step 3 — Load references

- `references/phase_deliverables.md` — percent-complete and deliverable expectations per phase (AIA B101 / industry norm).
- `references/sheet_types.md` — required sheet content per phase by sheet series.
- `references/coordination_flags.md` — common architectural-to-structural and architectural-to-MEP coordination items.

### Step 4 — Compose the checklist


Build the checklist around:

- Required sheet types at this phase, by series (G / A / structural-coord / MEP-coord).
- Level of detail expected per sheet type at this phase.
- Common missing items: callouts, dimension strings, key plans, tags, north arrow consistency.
- Cross-discipline coordination flags: structural grid alignment, MEP chase locations, ceiling height conflicts, slab depressions, roof penetrations.
- Title block / sheet numbering / revision cloud hygiene.
- Phase-specific deliverable expectations (SD ~15-30%, DD ~35-50%, CD 100% biddable, IFC 100% issued).

### Step 5 — Write the checklist file


Read `assets/checklist-template.md`, fill placeholders. Filename:


`docs/checklists/<phase>-<discipline>-checklist.md`


Slug rule: lowercase, `[^a-z0-9-]` removed. Example: `dd-architectural-checklist.md`, `cd-architectural-checklist.md`. If a checklist with the same name exists, suffix `-<n>`.


### Step 6 — Update the checklist index


```bash
python scripts/append_to_index.py \
  --date 2026-05-06 \
  --phase DD \
  --discipline architectural \
  --project-type commercial \
  --slug dd-architectural-checklist
```


The script appends a row to `docs/checklists/index.md`. Do NOT edit the index manually.


### Step 7 — Report


Tell the user:

- Path to the checklist file.
- The 2-3 highest-risk items at this phase for this project type.
- Whether any cross-discipline coordination items need to be raised with consultants now.

## Rules

- Tie every item to either a sheet, a deliverable percent, or a coordination interface — no vague "make sure it's coordinated".
- Phase percent-complete is a guide, not a contract — note if the project's contract defines its own thresholds.
- Architectural is the primary discipline; structural and MEP appear only as coordination flags, not as full discipline checklists.
- For IFC, every "TBD" / "by others" / "VIF" callout is a defect. Flag explicitly.

## Anti-patterns

- Generic checklists that ignore project type (a residential CD set is not a civic CD set).
- Listing every conceivable sheet type regardless of project scope.
- Mixing critique with checklist — this skill checks completeness, not design quality.
- Editing `index.md` manually instead of using `append_to_index.py`.
- Restating CAD/BIM standards the office already enforces — focus on the per-phase delta.

## Resources

- `scripts/init_checklist_workspace.py` — bootstrap `docs/checklists/` and the checklist index
- `scripts/append_to_index.py` — append a row to `docs/checklists/index.md`
- `references/phase_deliverables.md` — SD / DD / CD / IFC deliverable expectations and percent-complete
- `references/sheet_types.md` — architectural sheet types with required content per phase
- `references/coordination_flags.md` — architectural-to-structural / architectural-to-MEP coordination items
- `assets/checklist-template.md` — checklist markdown template
