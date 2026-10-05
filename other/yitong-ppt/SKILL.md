---
name: yitong-ppt
description: "Plan, design, create, revise, and validate clear editable PPTX presentations. Use when the user asks for 学术汇报, 论文分享, 组会, 答辩, tutorial, 项目汇报, 阶段总结, 领导汇报, 路演, proposal, progress review, or an evidence-led slide deck, including image-first visual exploration followed by editable PowerPoint delivery."
---

# 异瞳PPT

Create presentation decks that help a specific audience understand, decide, or act. 异瞳 means eyes of different colors and is the name of the white cat behind this skill. Apply two views on each key slide: check the evidence behind the claim, then check what the audience will understand. Ground the narrative in the current task's materials, keep one main idea per slide, and prefer visible evidence over decorative filler.

## Choose the report route

- **Academic report**: paper presentation, literature tutorial, group meeting, defense, seminar, or conference talk. Read [references/academic-report.md](references/academic-report.md).
- **Project report**: proposal, progress review, leadership or client update, engineering review, delivery report, roadmap, or pitch. Read [references/project-report.md](references/project-report.md).
- **Mixed report**: choose the route that matches the primary audience and decision; borrow only necessary page types from the other route.

Always read [references/design-system.md](references/design-system.md) before creating or substantially redesigning slides.

## Workflow

1. Inspect the supplied documents, data, images, videos, code outputs, experiments, and existing decks. Separate verified facts, interpretation, targets, plans, and missing evidence.
2. Determine the audience, duration, presentation setting, desired outcome, and the one message the audience should retain.
3. Create a page map before drawing. Give every slide one role, one main idea, one dominant visual, and one spoken takeaway. For each key slide, ask both: "What supports this?" and "What will this audience take away?" Remove pages that do not advance the narrative.
4. Reuse an approved master or existing deck when supplied. Learn its layout and visual grammar without copying unsupported facts or claims.
5. Choose the production path:
   - Build simple text, chart, table, and comparison pages directly as editable slides.
   - For complex overview, architecture, mechanism, or hero pages, use the image-first workflow in [references/image-first-workflow.md](references/image-first-workflow.md) when image generation is available.
6. Build the final deck as editable PPTX. Keep titles, labels, shapes, arrows, charts, tables, and major relationships native whenever practical. Follow [references/editable-delivery.md](references/editable-delivery.md).
7. Render and inspect the final deck when layout-sensitive creation or major editing was performed. Verify factual accuracy, hierarchy, readability, citations, image integrity, and editability.

If the user asks for end-to-end delivery, continue through the editable PPTX without pausing after a draft unless a missing decision would materially change the result.

## Evidence boundary

- Never invent measurements, citations, dates, identities, completion status, customer feedback, experimental results, or business outcomes.
- Label measured results, estimates, targets, plans, and illustrative concepts distinctly.
- Treat generated visuals as illustration, not evidence.
- Preserve metric definitions, dataset or business scope, comparison conditions, and limitations near the claims they qualify.
- Use source figures and screenshots only when their provenance and reuse context are appropriate.

## Tool adaptation

- Use the host's presentation tooling for PPTX creation and rendering.
- Use image generation only for visual exploration, covers, or supported conceptual illustrations.
- Use live PowerPoint control when available and useful; it is optional, not a requirement.
- If the environment cannot create PPTX files, provide a complete slide specification and state the limitation instead of claiming delivery.

## Deliverables

For a full creation task, provide the editable PPTX and rendered previews. Mention any important source gaps and any regions that remain raster images. Do not call a storyboard, draft image, or unverified file a completed presentation.
