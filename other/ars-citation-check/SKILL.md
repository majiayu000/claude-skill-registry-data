---
name: ars-citation-check
description: "ARS academic-paper `citation-check` mode — citation error report（ARS 命令入口）"
disable-model-invocation: true
---
First invoke the skill 工具 with `skill: "academic-paper"`. Pass the mode and the user's request described below as its arguments. Use the loaded skill and its supporting files before producing the result.

Trigger the `academic-paper` skill in `citation-check` mode. Produces a citation error report (missing references, mismatched in-text citations, format errors). Fidelity spectrum, low oversight.

Mode reference: `对应技能目录下的 `_shared/MODE_REGISTRY.md`` § academic-paper.
Skill entry: ``academic-paper` 技能`.

Resolve plugin resources from ``, not from the paper project's working directory. If the skill or a required file cannot be loaded, report the loading failure and stop; do not substitute this command summary for the mode instructions.
