---
name: review-00-controller
description: Orchestrate a stepwise SCI/narrative/systematic review workbench. Use when the user wants to start, resume, audit, or verify a medical literature review workflow with gated steps, deliverables, and next-skill routing.
---

# Review 00 Controller

## Purpose

Act as the master controller for a medical review project. Do not write manuscript content unless the relevant upstream evidence files exist. Route the user to the next numbered review skill only after the previous step has a concrete deliverable.

## Workflow

1. Identify the current project folder, review type, topic, target journal if known, and latest completed checkpoint.
2. Inspect the project-level `项目看板.md` and the folder for the active stage. In the standard six-step template, these are `01_选题_期刊_框架`, `02_文献_Zotero_PDF`, `03_正文撰写_框架填充`, `04_图表制作_素材管理`, `05_投稿材料_终审`, and `06_返修回复_再投稿`.
3. Classify status as `not_started`, `in_progress`, `blocked`, or `passed`.
4. State the missing files or decisions before proceeding.
5. Recommend the next skill by exact name, for example `$review-03-search-string`.
6. Before submission or major revision, route to `$review-21-personal-qc` even if `$review-20-reviewer-response` is not needed.

If the user asks for a simplified six-step course/demo workflow, a no-plugin workflow, or a "six steps to complete a review" explanation, route to `$review-28-six-step-workbench` first.

## Completion Gate

The step may pass only when:

- The previous step has a dated output file.
- The file contains source information or an explicit "not yet available" note.
- Human decisions are recorded when choices are required.
- Claims are not presented as evidence unless linked to a paper, dataset, or user-provided material.

## Output

Return a short progress note with:

- Current stage.
- Files checked.
- Pass/fail decision.
- Next action and next skill.

## Stop Rules

Stop and ask for user input if the research question, disease/domain, review type, or target journal constraints are absent and cannot be inferred from existing project files.

## Personal Workflow Memory

When the user asks to improve the workbench or distill their own writing process, read `references/personal-review-workflow.md` if present and use it to update checklists, gates, and final-audit logic.
