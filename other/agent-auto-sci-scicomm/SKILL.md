---
name: agent-auto-sci-scicomm
description: "科学交流与学术写作子 skill。用于论文结构、IMRAD、综述写作、图表叙事、英文润色、投稿信、审稿意见拆解、rebuttal、学术海报、PPT、研究汇报、图形摘要和文献引用管理。触发于 scientific writing、paper draft、paper plan、peer review、rebuttal、poster、slides、cover letter、citation management 等任务。"
---

# Agent Auto Sci Scientific Communication

Use this subskill when the output is a manuscript, response, slide deck, poster, abstract, or research narrative.

## Fast Workflow

1. Define target audience and venue.
2. Build a claim-evidence map before drafting.
3. Choose structure: empirical IMRAD, systematic review, scoping review, bibliometric review, policy agenda, or presentation.
4. Draft in paragraphs, not bullet lists, unless preparing an outline.
5. Check every claim against evidence.
6. Translate methods and results into field value.
7. After scientific content stabilizes, run the Academic Prose Style Guard to check positive-first framing, defensive-contrast clustering, and semantic repetition without weakening boundaries.
8. Run reviewer-risk and citation checks.

Keep these checks internal by default. Surface only issues that materially change scientific interpretation, estimand, sample, result, or conclusion; request author input only when safe continuation is impossible or a material scientific choice is theirs to make. Do not turn routine checks into a user-facing QC log. In manuscript prose, omit workflow/status terms such as `gate`, `guard`, `PASS`, `FAIL`, `NOT_VERIFIED`, `blocking`, `routing`, and `QC` unless they are formal research-method terms. Retain only material limitations in the manuscript and avoid repeating a boundary already stated unless the section needs it independently or the underlying judgment changes.

Read `references/scientific_communication_workflows.md`.
Read `references/academic_prose_style_guard.md` whenever generating manuscript prose, review synthesis, abstracts, conclusions, rebuttals, or substantial academic interpretation.

For full paper projects, this skill owns title, abstract, highlights, IMRAD structure, paragraph logic, figure-text narrative, journal matching, cover letter, reference/citation checks, response-to-reviewers, and final submission readiness. Use `sport-geography-sci-writing` for field-specific empirical manuscript logic.

For deeper K-Dense-style encapsulation:

- `references/k_dense_scicomm_mapping.md`: how scientific writing, peer review, slides, schematics, and citation-management skills are adapted.
- `references/sport_geography_communication_playbook.md`: Cities/SCS/Nature-family style positioning, claim-evidence maps, rebuttal, and presentation routes.

## Related Helper Skills

- `scientific-writing`
- `peer-review`
- `scientific-slides`
- `scientific-schematics`
- `citation-management`
- `sport-geography-sci-writing`
- `sport-geography-review-bibliometric`

## Must Not Do

- Do not let text polish hide weak evidence.
- Do not invent citations or journal requirements.
- Do not make policy claims without mechanism and evidence boundary.
- Do not write final manuscripts as bullets.
