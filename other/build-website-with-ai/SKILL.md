---
name: build-website-with-ai
description: Build polished websites with AI from a rough idea through clarification, visual reference analysis, page structure, asset matching, iteration, responsive QA, and deployment readiness. Use when the user wants to create, redesign, or improve a website, landing page, portfolio, product site, local service site, ecommerce showcase, course page, AI tool directory, or any web project where the agent should guide the user like a product strategist and design director before coding.
---

# Build Website With AI

## Overview

Use this skill to turn vague website ideas into real, usable websites through a director-style workflow: clarify the project, analyze references, build a structured draft, map real assets, iterate in small passes, verify desktop/mobile quality, and prepare for deployment.

Do not jump straight to code unless the user has already supplied a clear project brief, visual direction, content, and build target. The main value of this skill is making AI ask the right questions and preserve design intent during implementation.

## Workflow

### 1. Clarify Before Building

Start by asking 8-12 high-leverage questions when the project is vague. Cover:

- target users
- user intent on arrival
- desired conversion action
- competitor or category difference
- homepage message
- required pages or sections
- must-have content
- visual personality
- missing information needed to make the site feel real

If the user cannot answer, make explicit reasonable assumptions and label them as assumptions.

Convert the answers into a project positioning brief:

- one-line positioning
- target users
- pain points
- core offer or selling points
- conversion goal
- page structure
- homepage section order
- visual keywords
- required content
- deferred content

Read `references/prompts.md` when you need ready-to-use Chinese prompts for the clarification and positioning phase.

### 2. Design the Information Architecture

Before coding, produce a table with:

- section order
- section name
- what the user sees
- why the user keeps reading
- required assets

Make the homepage read like a natural decision path, not a pile of generic modules. Each section must answer a user question, build trust, or move the user toward the conversion action.

### 3. Analyze Visual References

If the user provides screenshots, websites, app screens, posters, brand images, or competitor pages, analyze them before building. Do not copy them directly.

Extract:

- style keywords
- color and contrast behavior
- typography hierarchy
- spacing and layout rhythm
- cards, buttons, nav, section patterns
- image-to-text ratio
- motion or premium-feel cues
- what fits this project and what should be discarded

Synthesize a visual direction that fits the user's project. Preserve useful qualities such as whitespace, hierarchy, restraint, rhythm, and motion, while redesigning the structure and copy for the actual business goal.

### 4. Build the Website Skeleton

Create a runnable first version with complete section order, real headings, draft copy, calls to action, basic interactions, and image placeholders.

For each placeholder, label the intended image type, such as hero visual, product photo, case study image, team image, process diagram, logo, testimonial portrait, or background texture.

Prioritize:

- project logic
- page rhythm
- first-screen clarity
- visual direction
- responsive structure
- readable, specific copy

Do not wait for perfect images before producing a useful draft.

### 5. Process and Match Images

When the user supplies many images, ask them to place originals in `assets/raw-images/`. Preserve original files.

Then:

1. inspect image content
2. classify by likely use
3. rename or copy processed versions with clear English filenames
4. place optimized web-ready versions in `assets/processed/`
5. match images to page sections
6. avoid stretched or distorted images
7. keep uncertain placements as placeholders and explain what is missing

Output an image assignment table before or alongside the code changes. When the user corrects image placement, change only the mapping and necessary styles; do not rewrite the whole page.

### 6. Iterate Like a Design Director

Review the result visually, not just the code. Check:

- whether the first screen explains who this is for and what is offered within 3 seconds
- whether module order supports a natural sales or trust-building path
- whether copy sounds specific rather than generic AI marketing text
- whether images match the content
- whether buttons and conversion paths are clear
- whether desktop and mobile layouts both work
- whether text overlaps, images distort, or spacing feels chaotic

Prefer small iterations of 3-5 issues at a time. Preserve strong visual traits that already work, such as hierarchy, whitespace, card rhythm, and restrained motion.

Read `references/checklists.md` when preparing final QA or when the user asks what to inspect.

### 7. Verify and Prepare for Launch

Before calling the site complete:

- run the build or static validation command available in the project
- inspect desktop and mobile views when a browser tool is available
- check image paths, links, buttons, forms, and navigation
- remove unused placeholder-only content if real content exists
- report remaining assumptions or missing assets

For deployment, choose the platform that matches the project or user request, such as Vercel, Netlify, Cloudflare Pages, GitHub Pages, or an existing hosting setup. Do not delete source assets during cleanup.

## Suggested Project Folders

Use or adapt this structure when starting from scratch:

```text
my-website/
  references/        visual references and competitor screenshots
  assets/
    raw-images/      untouched original images
    processed/       optimized web-ready images
  notes/             project notes and copy
  prompts/           saved prompts and decisions
  website/           generated website code
```

## Common Starting Points

- Portfolio: clarify personal positioning, work categories, services, proof, and contact path.
- Product site: clarify product name, pain point, differentiation, proof, and conversion path.
- Local service site: clarify service area, trust evidence, booking or consultation flow.
- Ecommerce showcase: clarify product categories, buying motivations, card content, and detail-page structure.
- Course landing page: clarify learner pain, promised outcome, curriculum, proof, pricing, and signup path.
