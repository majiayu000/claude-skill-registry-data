---
name: ars-3w
description: "ARS deep-research `three-way-scan` mode — WHY / HOW / WHAT paper comparison（ARS 命令入口）"
disable-model-invocation: true
---
First invoke the skill 工具 with `skill: "deep-research"`. Pass the mode and the user's request described below as its arguments. Use the loaded skill and its supporting files before producing the result.

Trigger the `deep-research` skill in `three-way-scan` mode. Produces a compact paper shortlist compared by WHY / HOW / WHAT plus a cross-paper synthesis (common WHY, divergent HOW, strongest WHAT, unresolved gap). Lighter than `lit-review`; escalate to `lit-review` / `systematic-review` for full coverage. Fidelity spectrum, low oversight.

Mode reference: `对应技能目录下的 `_shared/MODE_REGISTRY.md`` § deep-research.
Skill entry: ``deep-research` 技能`.

Resolve plugin resources from ``, not from the paper project's working directory. If the skill or a required file cannot be loaded, report the loading failure and stop; do not substitute this command summary for the mode instructions.
