---
name: aiwf-avoid-ai-illustrations
description: AIWF generated-image quality guardrail for avoiding obvious AI illustration and image artifacts. Use when planning, prompting, reviewing, editing, or accepting generated images, illustrations, logos, icons, diagrams, charts, infographics, visual text, portraits, people, hands, fingers, anatomy, skin texture, photorealism, product images, or final image deliverables. Triggers for "avoid AI-looking images", "AI artifacts", bad hands, extra fingers, missing fingers, distorted faces, overdone pores, cyst/pimple-like skin artifacts, fake logos, misspelled text, broken diagrams, wrong chart values, impossible shadows, composition failures, and generated-image QA.
---

# AIWF Avoid AI Illustrations

## Overview

Use this skill to prevent generated images from looking broken, fake, or semantically wrong. It is an AIWF skill-pack lane for image-generation planning and final QA, not a broad UI/design cleanup skill.

## Workflow

1. Classify the surface before prompting or reviewing:
   - freeform illustration or mood image
   - photoreal person, face, hands, or product
   - logo, icon, signage, or visual text
   - diagram, flowchart, architecture figure, or process map
   - chart, quantitative infographic, or data visualization
2. Read `references/failure-modes.md` for the relevant artifact categories.
3. Read `references/surface-playbooks.md` before generating, editing, or recommending an implementation route.
4. Read `references/review-checklist.md` before accepting a final asset.
5. Decide the exactness level:
   - Flexible mood, scene, texture, and style can use normal image generation.
   - Exact text, brand marks, charts, diagrams, anatomy-critical images, product claims, and instructional visuals need references, masks/control inputs, structured/vector rendering, code-backed charts, or explicit final inspection.
6. Prefer correction over regeneration when the concept is good but a local defect exists: crop, inpaint, mask, replace text, redraw vector elements, or rerender charts from data.

## Hard Rules

- Do not accept a generated chart as final unless values, axes, labels, title, and scale are checked against the source data.
- Do not accept generated logos or signage as final typography. Use generated output for concept direction, then render final text and marks as vector or editable design elements.
- Do not accept diagrams that need logic, arrows, labels, or editability as flat image guesses. Prefer Mermaid, Graphviz, SVG, draw.io, Figma, or code-backed layout.
- Do not assume high aesthetic quality means semantic correctness. Inspect prompt-critical entities, object counts, body parts, hands, text, labels, shadows, and object interactions.
- Do not over-prompt skin with extreme micro-detail when the user wants clean realism. Terms like "visible pores" can over-amplify blemish-like marks; prefer "natural, subtle skin texture" plus explicit absence of unwanted blemishes when that is the intent.

## Output

For planning or prompt work, return the route, artifact risks, prompt/control guidance, and final QA gates.

For review work, return pass/fail findings by surface and state exactly what must be regenerated, inpainted, redrawn, or rendered deterministically.
