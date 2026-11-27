---
name: ars-rebuttal-audit
description: "ARS academic-paper `rebuttal-audit` mode — QA an existing rebuttal draft against reviewer comments（ARS 命令入口）"
disable-model-invocation: true
---
First invoke the skill 工具 with `skill: "academic-paper"`. Pass the mode and the user's request described below as its arguments. Use the loaded skill and its supporting files before producing the result.

Trigger the `academic-paper` skill in `rebuttal-audit` mode. Requires BOTH the reviewer comments AND an existing rebuttal/response draft to evaluate. Produces an advisory QA report (per-comment coverage + gaps + risk flags). Does NOT generate a new response, and does NOT emit Schema 11 / Material Passport / verified status (standalone invocation runs outside the pipeline). Fidelity spectrum, low oversight.

If only reviewer comments are present (no draft yet), use `revision-coach` instead.

Mode reference: `对应技能目录下的 `_shared/MODE_REGISTRY.md`` § academic-paper.
Skill entry: ``academic-paper` 技能`.

Resolve plugin resources from ``, not from the paper project's working directory. If the skill or a required file cannot be loaded, report the loading failure and stop; do not substitute this command summary for the mode instructions.
