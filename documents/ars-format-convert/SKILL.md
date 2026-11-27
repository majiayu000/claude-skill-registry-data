---
name: ars-format-convert
description: "ARS academic-paper `format-convert` mode — convert to LaTeX / DOCX / PDF / Markdown（ARS 命令入口）"
disable-model-invocation: true
---
First invoke the skill 工具 with `skill: "academic-paper"`. Pass the mode and the user's request described below as its arguments. Use the loaded skill and its supporting files before producing the result.

Trigger the `academic-paper` skill in `format-convert` mode. Converts a paper between LaTeX, DOCX (via Pandoc), PDF, or Markdown, and converts citation styles between major formats. Fidelity spectrum, low oversight.

Mode reference: `对应技能目录下的 `_shared/MODE_REGISTRY.md`` § academic-paper.
Skill entry: ``academic-paper` 技能`.

Resolve plugin resources from ``, not from the paper project's working directory. If the skill or a required file cannot be loaded, report the loading failure and stop; do not substitute this command summary for the mode instructions.
