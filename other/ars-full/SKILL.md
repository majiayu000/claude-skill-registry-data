---
name: ars-full
description: "ARS full pipeline — research → write → review → revise → finalize（ARS 命令入口）"
disable-model-invocation: true
---
First invoke the skill 工具 with `skill: "academic-pipeline"`. Pass the mode and the user's request described below as its arguments. Use the loaded skill and its supporting files before producing the result.

Trigger the `academic-pipeline` orchestrator (`(pipeline)` in `对应技能目录下的 `_shared/MODE_REGISTRY.md`` — the orchestrator has no named mode of its own). Loads the skill and executes the complete academic research workflow (10-stage orchestration: deep-research → academic-paper → integrity → academic-paper-reviewer → revision → re-review → final integrity → finalize).

Mode reference: `对应技能目录下的 `_shared/MODE_REGISTRY.md`` § academic-pipeline.
Skill entry: ``academic-pipeline` 技能`.

Resolve plugin resources from ``, not from the paper project's working directory. If the skill or a required file cannot be loaded, report the loading failure and stop; do not substitute this command summary for the mode instructions.
