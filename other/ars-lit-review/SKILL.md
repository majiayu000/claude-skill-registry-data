---
name: ars-lit-review
description: "ARS academic-paper `lit-review` mode — annotated bibliography in paper format（ARS 命令入口）"
disable-model-invocation: true
---
First invoke the skill 工具 with `skill: "academic-paper"`. Pass the mode and the user's request described below as its arguments. Use the loaded skill and its supporting files before producing the result.

Trigger the `academic-paper` skill in `lit-review` mode. Produces an annotated bibliography rendered as a literature review section. Fidelity spectrum, medium oversight.

Stay in `academic-paper` `lit-review` mode and do not reopen the choice of workflow: if the papers or sources the request refers to are missing, ask the user for them or offer to search for them within this mode.

The skill's review-form note (#921) belongs to this mode and does not reopen that choice: show it and wait when the skill says to, and continue in `lit-review` mode if the author skips it.

Mode reference: `对应技能目录下的 `_shared/MODE_REGISTRY.md`` § academic-paper.
Skill entry: ``academic-paper` 技能`.

Resolve plugin resources from ``, not from the paper project's working directory. If the skill or a required file cannot be loaded, report the loading failure and stop; do not substitute this command summary for the mode instructions.
