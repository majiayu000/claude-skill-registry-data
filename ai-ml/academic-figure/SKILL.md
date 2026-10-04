---
name: academic-figure
description: "Create, revise, or audit academic data/result figures for CS/AI/ML papers. Data/result plots default to Python-generated editable SVG with CS/AI/ML-specific design rules for benchmarks, ablations, training dynamics, robustness, diagnostics, distributions, confusion matrices, and efficiency tradeoffs. Use when: generating plots from experiment results or numeric data, auditing publication figures, suggesting data-driven figure types, revising chart colors/layouts/labels, or preparing figure QA reports. Model framework diagrams, architecture diagrams, overview diagrams, and complex mechanism schematics are outside this skill's automatic drawing scope; provide only manual figure requirements or caption/blueprint notes when needed. Triggers on: 绘图, figure, chart, 画图, 实验图, 训练曲线, 消融实验, 对比图, 混淆矩阵, 结果图, 性能图, 鲁棒性图, 效率图, plot, publication figure, 数据可视化, generate plot, figure blueprint, 建议图表类型, figure audit, 审查图表, figure revision, 修改图表."
---

# Academic Figure

CS/AI/ML academic-figure router. 实验数据图默认交付 Python/matplotlib 可编辑 SVG，并执行 CS/AI/ML 图表设计 gate。模型框架图、架构图、overview 图和复杂机制图不属于本 skill 的自动绘制范围；如论文需要此类图，只能输出人工绘制需求、证据清单、caption 草案或 figure blueprint notes。

## Router Protocol

1. Read `manifest.yaml`. It declares `always_load` files, `axes`, and `references.on_demand`.
2. Read every file listed under `always_load`. These are the skill's binding rules — not reference material.
3. Apply the loaded material as constraints:
   - `stance.md` defines Python-only plotting, figure contract, visual policy, and scope.
   - `red-lines.md` defines absolute prohibitions. Do not negotiate these.
   - `output-contract.md` defines deliverables per mode.
   - `anti-patterns.md` defines known failure modes and their correct alternatives.
4. Select exactly one `mode` from the manifest. If ambiguous, ask one concise clarification only when data source or target use is missing. Requests for model framework, architecture, overview, or mechanism diagrams use `figure-blueprint` only to produce `manual_figure_needed` notes; never render images, SVG, or prompts.
5. Echo the selected mode to the user before executing.
6. Reach for `references/` only when the manifest's `references.on_demand` condition is satisfied.

## Modes

| Mode | Use when |
|---|---|
| `chart-from-data` | Data files or numeric results, needs publication plot with CS/AI/ML chart design gate |
| `figure-blueprint` | Wants figure suggestions for a paper section |
| `figure-audit` | Existing figure reviewed for publication readiness |
| `figure-revision` | Existing figure needs revision |

## Agent Dispatch

`agents/figure_agent.md` is dispatched by the orchestrator at Step 6.4. The agent returns figure artifacts, scripts, SVG paths, and reports; it must not independently edit project source code or experimental data.

## Completion Criteria

- `chart-from-data`: Figure Contract, CS/AI/ML chart design gate, Python script, source data, editable SVG, QA report — all pass.
- `figure-audit`: Every QA item has pass/fail status and concrete remediation.
- `figure-blueprint`: Every suggested figure maps to a paper claim and data/evidence source.
- `figure-revision`: Revised artifact or instructions, QA report, unchanged evidence traceability.
