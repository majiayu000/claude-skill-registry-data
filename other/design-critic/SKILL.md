---
name: design-critic
description: "This skill should be used when the user shares an architectural project (concept text, plans, sections, renderings, references) and asks for critique, feedback, or a second opinion. Trigger on 'design critique', 'review this design', 'critique this', 'second opinion', or when context implies the user wants challenge over validation. Generates a structured critique markdown in `docs/reviews/` and appends to the project review index."
license: MIT
metadata:
  title: "Design Critic"
  summary: "Get a structured critique of a design"
  discipline: "design-building-types"
  tags: "Design"
---


# Design Critic


## Overview


Review an architectural project against six core axes and produce a written critique that lives in `docs/reviews/`. The critique is a working document — pointed, specific, with a bounded set of "issues to address" and concrete next moves.


## Scope and limits — read first


**What this does.** Reads a design you share against six axes and writes a
critique to `docs/reviews/` naming the two or three issues worth acting on, each
tied to the axis it came from and to something actually visible in the work.

**What this does not do.**

- **It does not design.** It points at the next move, not at a different
  project, and it produces no plans, options, or alternatives.
- **It does not grade a dimension the project never claimed.** A scheme that
  makes no sustainability claim is not marked down for sustainability.
- It does not check code, zoning, cost, or buildability. Those are `code-compliance-review`,
  `zoning-summary`, `value-engineering-advisor`, and `constructability-review`.
- It does not describe what it cannot see. When an image arrives with no
  context it asks once for site, program, and concept rather than inferring
  them, and it does not critique material the user only alluded to.
- It does not rank the work against other projects or score it out of ten.

**What you need before starting.** The work itself, in whatever form it exists,
plus the site, the program, and the concept as you would state it. Optionally a
tone: mentor, harsh, or encouraging.

## When to use


Trigger on:

- Pasted concept descriptions paired with plans/sections/renderings.
- Image attachments of a design with brief context.
- Explicit asks: "critique", "review my design", "second opinion".
- Project file/folder paths the user wants reviewed.

Do NOT trigger on questions about how to design something. This skill _reviews_ existing work, it does not generate new designs.


## Workflow


### Step 1 — Bootstrap if needed


Check that `docs/reviews/index.md` exists. If not:


```bash
python scripts/init_review_workspace.py
```


### Step 2 — Gather context

- Read `docs/project.md` if it exists for site, program, brief, constraints.
- Read any provided design files (text descriptions, image paths, plan/section .md or .pdf files).
- Note the user's stated tone preference: `mentor` (default) / `harsh` / `encouraging`.

### Step 3 — Apply six-axis critique


Load `references/six_axes.md` for the full framework with sub-criteria. Quick reference:

1. **Concept consistency** — Does the stated intention show up in form, material, and detail, or only in the diagram?
2. **Scale & proportion** — Right size for what it claims to be? Relationship to user, neighbors, program.
3. **Circulation & program** — Logic of movement and adjacency. Public/private, served/servant resolved?
4. **Material & detail** — Material choice supports concept or fights it? Detail level consistent with intent?
5. **Context** — Site, climate, culture. Building aware of where it is?
6. **Innovation vs feasibility** — How much of the ambition is buildable on the implied budget and schedule?

Focus on the 2-4 axes with real signal. Do not score every axis on every project.


## Tone calibration

- **mentor (default)**: Warm but pointed. State weaknesses clearly, suggest direction.
- **harsh**: Critic mode. Lead with the strongest objection. No softening language.
- **encouraging**: Lead with strengths. Frame issues as "things to develop." For students or early-stage work.

### Step 4 — Write the critique


Read `assets/review-template.md`, fill placeholders. Filename:


`docs/reviews/<YYYY-MM-DD>-<topic-slug>.md`


Slug rule: lowercase, `[^a-z0-9-]` removed, max 40 chars, derived from project name or design phase (`tower-mass`, `lobby-rev3`). If a critique with the same date+slug already exists, suffix `-<n>`.


### Step 5 — Update the review index


```bash
python scripts/append_to_index.py \
  --date 2026-05-06 \
  --slug tower-mass \
  --tone mentor \
  --primary-axes "concept,scale,context"
```


The script appends a row to `docs/reviews/index.md`. Do NOT edit the index manually with the Edit tool — table alignment breaks easily.


### Step 6 — Report


Tell the user:

- Path to the critique file
- The 1-2 most pressing issues
- Suggested next study or sketch

## Rules

- Every issue cites WHY, rooted in one of the six axes — never "this feels off" without a reason.
- Refuse to grade dimensions the designer did not claim. If the project does not claim sustainability, do not critique sustainability.
- If only an image is provided with no context, ask once for site, program, and concept before critiquing.
- Specifics over generalities. "The cantilever conflicts with the structural grid in the section" beats "structure feels weak."

## Anti-patterns

- Saying "interesting" or "promising" without specifying what and why.
- Listing 10 issues — pick the 3-5 that matter most.
- Suggesting a complete redesign. Critique points to the next move, not a new project.
- Critiquing image content the user did not share (do not hallucinate from a vague description).
- Editing `index.md` manually instead of using `append_to_index.py`.

## Resources

- `scripts/init_review_workspace.py` — bootstrap `docs/reviews/` and the review index
- `scripts/append_to_index.py` — append a row to `docs/reviews/index.md`
- `references/six_axes.md` — detailed six-axis critique framework with sub-criteria
- `assets/review-template.md` — critique markdown template
