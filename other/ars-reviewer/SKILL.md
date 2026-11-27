---
name: ars-reviewer
description: "ARS academic-paper-reviewer `full` mode — simulated peer-review panel（ARS 命令入口）"
disable-model-invocation: true
---
First invoke the skill 工具 with `skill: "academic-paper-reviewer"`. Pass the mode and the user's request described below as its arguments. Use the loaded skill and its supporting files before producing the result.

Trigger the `academic-paper-reviewer` skill in `full` mode. Honor explicit alternate modes when present: `quick`, `methodology-focus`, `re-review`, `guided`, or `calibration`. Runs on the inherited session model — the v3.7.0 `opus` frontmatter floor was retired in the 2026-06 harness pass so a stronger session model is never silently downgraded.

Mode reference: `对应技能目录下的 `_shared/MODE_REGISTRY.md`` § academic-paper-reviewer.
Skill entry: ``academic-paper-reviewer` 技能`.

Resolve plugin resources from ``, not from the paper project's working directory. If the skill or a required file cannot be loaded, report the loading failure and stop; do not substitute this command summary for the mode instructions.
