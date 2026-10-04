---
name: logo-design-board
description: Use when creating, critiquing, or iterating logo and brand-mark concepts through a designer-distillation board, including brand intake, public-source designer lenses, concept territories, visual prompts, and logo quality scoring.
---

# Logo Design Board

## Overview

Use this skill to turn a brand brief into original logo directions through a compact designer board: public-source designer lenses, brand strategy, concept generation, critique, scoring, and production handoff.

Treat designer distillation as a method for extracting decision criteria, not as impersonation. Never copy a designer's work, a client logo, or a protected mark.

## When to Use

Use this skill when the user wants to:

- Design a logo, brand mark, wordmark, monogram, app icon, favicon, or visual identity direction.
- Turn project background, product positioning, or founder notes into logo concepts.
- Use distilled design thinking from public designers or studios to guide logo decisions.
- Compare logo directions, critique a generated mark, or improve a rough symbol.
- Produce image-generation prompts, vector construction notes, and brand-guide starter notes for a logo concept.

## Do not use

Do not use this skill as the primary workflow for:

- Legal trademark clearance, infringement opinions, or final IP approval.
- Copying an existing logo, designer style, brand system, mascot, or protected character.
- General poster, illustration, landing-page, UI, or marketing image work where logo identity is not the core task.
- Producing final production files without human review, vector cleanup, optical correction, and legal checks.

## Instructions

For full logo work, read both references before producing final recommendations:

- `references/designer-lens-framework.md`: use when choosing or distilling designer lenses.
- `references/logo-quality-rubric.md`: use before scoring concepts or selecting finalists.

For small critique requests, use the workflow below directly and load the rubric reference only if a scored recommendation is needed.

## Workflow

1. Establish the brand brief:
   - Brand or product name.
   - Category and target audience.
   - Core promise in one sentence.
   - Brand personality with tensions, such as precise but warm, premium but approachable, playful but credible.
   - Competitors and category visual codes.
   - Required uses: app icon, favicon, website header, social avatar, packaging, merch, print, signage, or motion.
   - Constraints: words that must appear, initials, symbols to avoid, color restrictions, cultural or accessibility constraints.

2. Fill gaps conservatively:
   - Ask at most three targeted questions when missing details would change the design direction.
   - If the user wants speed, proceed with explicit assumptions and mark them as assumptions.
   - Do not ask for a questionnaire when the brief is already enough to start.

3. Set the designer board:
   - Default board:
     - Paul Rand lens: idea-led simplicity, memorable symbols, wit without clutter.
     - Massimo Vignelli lens: discipline, grid, reduction, timeless systems, typographic restraint.
     - Paula Scher lens: expressive typography, cultural energy, scale, attitude, category presence.
   - Add one optional lens only when useful:
     - Saul Bass for narrative symbols, motion-friendly silhouettes, and cinematic reduction.
     - Michael Bierut for client context, implementation systems, and real-world usage ecology.
   - Label these as public-method lenses. Do not claim to speak for the real person.

4. Distill or adapt the lenses:
   - Use user-provided sources first: books, interviews, portfolios, talks, case studies, notes, or screenshots.
   - If the user names a specific living or current designer and accuracy matters, gather current public sources before distilling.
   - Extract principles, recurring judgments, red flags, and design questions. Avoid extracting only surface style.
   - Reject any lens that only produces a visual costume rather than design decisions.

5. Define the logo strategy:
   - State the logo's job: what it must signal, where it must work, and what it must avoid.
   - Identify the category code to borrow and the category code to break.
   - Convert vague adjectives into designable tensions.
   - Decide whether the strongest route is a wordmark, monogram, pictorial symbol, abstract mark, mascot-like icon, or flexible identity system.

6. Generate concept territories:
   - Produce three to five directions, not one generic logo.
   - For each direction include:
     - Name of the territory.
     - Strategic thesis.
     - Mark type.
     - Visual construction in plain language.
     - Typography direction.
     - Color direction and one-color behavior.
     - Which designer lenses support it and which challenge it.
     - Image-generation prompt for rough exploration.
     - Vector construction notes for redrawing.
     - Main risks and how to test them.
   - Prompts must request original marks, flat/vector-friendly forms, simple geometry, clean edges, and no imitation of existing logos.

7. Critique like a board:
   - Create a table with each lens as a row and each concept as a column.
   - Separate praise, risk, and required revision.
   - Remove concepts that fail small-size recognition, one-color use, or category distinction.
   - Use the rubric reference to score finalists when the user needs a recommendation.

8. Prepare handoff:
   - Recommend one or two finalists and explain the tradeoff.
   - Provide final prompt language for image exploration.
   - Provide vector redrawing notes, including grid, stroke, negative space, and optical correction concerns.
   - Provide usage tests: 16 px favicon, 32 px app icon, 120 px social avatar, website header, black on white, white on black, grayscale, print, embroidery or stamp when relevant.
   - State that raster output is concept art; final delivery requires vector cleanup and trademark search.

## Output Format

Use this structure for a full logo request:

```markdown
## Brand Read
[brief synthesis and assumptions]

## Designer Board
[selected lenses and why]

## Strategy
[logo job, category code, design tension]

## Concept Territories
[3-5 directions with prompts and vector notes]

## Board Critique
[lens-by-concept critique table]

## Recommendation
[top 1-2 directions, scoring summary, next iteration]

## Handoff
[prompt, vector notes, usage tests, legal/IP caveat]
```
