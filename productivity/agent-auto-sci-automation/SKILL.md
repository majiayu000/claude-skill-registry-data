---
name: agent-auto-sci-automation
description: "科研自动化与长期记忆子 skill。用于把 AutoSci/OmegaWiki 的论文摄入、知识库、idea 生成、novelty 检查、实验设计、失败经验、论文计划、review/rebuttal、可视化和进化记录流程转化为本地 Codex 科研工作流。触发于科研自动化、跨项目记忆、source manifest、wiki式知识库、paper ingestion、idea pipeline、experiment lifecycle、checkpoint、API 配置等任务。"
---

# Agent Auto Sci Automation

Use this subskill to convert a one-off research task into a persistent workflow.

## Fast Workflow

1. Define the project root, source folders, output folders, and ownership boundaries.
2. Create or update a source manifest: papers, notes, data, scripts, figures, manuscripts.
3. Convert sources into structured memory: tables, indexes, concept notes, method notes, failed attempts.
4. Route the task to literature, idea, experiment, analysis, writing, review, or archive stages.
5. Add checkpoints for long-running workflows.
6. Update the evolution archive after workflow improvements.

Read `references/autosci_workflow_and_memory.md`.

For deeper AutoSci encapsulation:

- `references/autosci_command_mapping.md`: local mapping of AutoSci `/init`, `/ideate`, `/novelty`, `/exp-design`, `/paper-plan`, `/review`, `/rebuttal`, and visualization flows.
- `references/api_and_checkpoint_templates.md`: source manifest, checkpoint, API role, and failure-memory templates.

## Default Memory Entities

- `sources`: PDFs, data, notes, web pages.
- `papers`: structured paper records, DOI, topic, method, findings.
- `concepts`: definitions, boundaries, related concepts.
- `methods`: reusable analytical or writing methods.
- `ideas`: proposed, rejected, validated, or failed research ideas.
- `experiments`: empirical or computational tests, including failed runs.
- `outputs`: manuscripts, figures, tables, posters, slides.
- `reviews`: reviewer comments, internal critiques, response strategies.
- `evolution`: skill changes, new workflows, validation evidence.

## Quality Rules

- Checkpoint before long workflows.
- Do not overwrite user-curated source boundaries without explicit instruction.
- Record failed ideas and weak evidence, not only successful outputs.
- Do not write secrets into logs or HTML.

