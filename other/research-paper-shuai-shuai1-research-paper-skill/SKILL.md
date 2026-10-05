---
name: research-paper
description: Evidence-driven research-paper planning, writing, polishing, experiment-to-paper conversion, simulated peer review and re-review, reviewer-response handling, reproducibility auditing, and publication-quality scientific figures. Use for engineering, computer-science, and AI empirical manuscripts when Codex must audit claims against literature/data/logs; revise or polish sections without changing data meaning; apply generic, Chinese-core, or explicit Nature-family style profiles; turn experiments into defensible methods/results; create reproducible plots or editable diagrams; optionally generate a scientific bitmap concept with GPT Image 2 and reconstruct it in PowerPoint with render-difference QA; review a manuscript; respond to reviewers; or run a pre-submission consistency check.
---

# 科研论文

把论文视为可审计的证据系统，而不是语言生成任务。建立并维护以下链条：

`研究问题 -> 主张 -> 证据 -> 实验或文献 -> 正文 -> 图表 -> 结论边界`

默认面向工程、计算机和人工智能实证论文。若任务属于其他学科，保留证据与审计流程，但先读取目标期刊规范并调整章节结构、伦理要求和引用格式。

## 硬性边界

1. 不编造文献、数据、实验、统计显著性、运行结果或审稿意见。
2. 不把配置值、理论值、合成数据、smoke 运行或局部验证写成正式实测结论。
3. 不因润色而改变指标定义、比较对象、数据划分、随机种子、样本量或结论范围。
4. 不把同一测试集上的反复调参包装为独立验证。
5. 不以“首次”“显著优于”“充分证明”“完全解决”等措辞替代证据。
6. 不静默覆盖用户原稿、图件、数据或已编辑文档。先复制，再修改，再验证。
7. 不逐像素复制无授权的外部论文图。只对自有、授权或可公开复现的来源进行高保真复现；其他来源采用带引用的结构保真重绘。
8. 不让图像生成模型决定数值、坐标轴、公式、拓扑、器件连接或实验曲线。

## 选择模式

根据用户目标选择一个主模式；必要时串联其他模式。

| 模式 | 适用任务 | 主要输出 |
|---|---|---|
| `plan` | 研究材料零散、主线未定、需要逐章规划 | Paper Brief、章节计划、缺口清单 |
| `evidence-audit` | 判断现有材料能否支撑结论 | Evidence Ledger、Claim-Evidence Matrix、风险清单 |
| `experiment-to-paper` | 从代码、配置、日志和结果写方法/实验/结果 | 实验契约、可复现描述、结果段落、限制 |
| `write-revise` | 从零写作、局部改稿或论证重构 | 修改稿、保留口径、修改说明 |
| `polish` | 校对、清晰化、分层润色、翻译或期刊风格适配 | 润色稿、修改级别、风格配置、一致性报告 |
| `figure` | 数据图、模型图、系统图、流程图或重绘式复现 | Figure Package、源数据/代码、矢量/位图、图注 |
| `peer-review` | 投稿前模拟评审、方法专项审查或修改稿复审 | Major/Minor 问题、阻断项、问题台账、评审建议 |
| `review-response` | 拆解审稿意见并完成修改回复 | Revision Tracker、逐条回复、修改位置 |
| `pre-submit` | 投稿前终审 | 阻断项、警告项、通过项、提交建议 |

不确定时先运行 `evidence-audit`，不要直接进入全文生成。

## 读取最少必要参考

- 所有复杂任务：先读 [workflow-and-routing.md](references/workflow-and-routing.md)。
- 主张、数据来源、引用真实性或结论边界：读 [evidence-and-claims.md](references/evidence-and-claims.md)。
- 选章节结构、分配篇幅、设计叙事：读 [paper-architecture.md](references/paper-architecture.md)。
- 写作、改稿、摘要、结果和讨论：读 [academic-writing.md](references/academic-writing.md)。
- 论文校对、结构润色、全文一致性或期刊风格适配：额外读 [polishing-and-style-profiles.md](references/polishing-and-style-profiles.md)。
- 从实验代码或日志写论文：读 [experiment-reproducibility.md](references/experiment-reproducibility.md)。
- 统计图、曲线、混淆矩阵、消融图：读 [data-figures.md](references/data-figures.md)。
- 系统图、CNN 图、流程图、参考图重绘：读 [diagrams-and-reproduction.md](references/diagrams-and-reproduction.md)。
- GPT Image 2 生成后用 PPT 做可编辑高保真复现：额外读 [ppt-pixel-reproduction.md](references/ppt-pixel-reproduction.md)。
- 审稿意见、回复信和修改追踪：读 [revision-and-review.md](references/revision-and-review.md)。
- 模拟同行评审、方法专项审查或复审：读 [peer-review-and-rereview.md](references/peer-review-and-rereview.md)。
- 投稿前或交付前：读 [quality-gates.md](references/quality-gates.md)。

不要一次性加载全部参考文件。

## 总工作流

### 1. 建立论文契约

从用户材料中提取并确认：

- 一句话研究问题与中心主张；
- 论文类型、学科、语言、目标期刊和输出格式；
- 已有文献、数据、代码、日志、图表、草稿与审稿意见；
- 不允许改变的指标、数据口径、实验版本和人工修改；
- 公开、保密、版权和伦理边界。

材料不足但不影响方向时，明确假设后继续；缺失信息会改变研究主线、实验公平性或结论时，停下来请用户确认。

需要工作区时，运行：

```text
python scripts/init_paper_workspace.py <workspace> --title "<paper title>"
```

### 2. 建立证据台账

复制 `assets/templates/evidence_ledger.csv` 与 `claim_evidence_matrix.csv`。把每条证据标为：

- `MEASURED`：正式测量或正式实验；
- `LOGGED`：日志、归档或运行记录；
- `DERIVED`：由已知数据计算；
- `THEORETICAL`：公式或理论推导；
- `LITERATURE`：外部文献；
- `SYNTHETIC`：合成、演示或示意数据；
- `UNVERIFIED`：尚未核实。

用 `audit_evidence_ledger.py` 检查完整性。任何核心主张必须能回到证据 ID、来源定位和限制。

### 3. 冻结结构和主张

先形成章节计划和 Claim-Evidence Matrix，再写正文。把每个核心主张的允许措辞、反例、适用条件和图表位置写清楚。用户未确认主线或结构时，不批量生成全文。

### 4. 写作或修订

优先按“方法与实验条件 -> 结果 -> 讨论 -> 引言与相关工作 -> 摘要与结论”的顺序工作。局部修改时只改授权范围，并报告保留不动的数据口径。

正文中的重要事实可暂用 `[E:E001]` 形式关联内部证据台账；最终投稿前按期刊需要移除内部标签，但保留台账。

全文润色先锁定论文类型、章节任务、修改级别、语言和风格配置，再运行数字与术语一致性扫描。默认使用 `generic`；只有用户明确目标期刊时才启用对应期刊配置。

模拟评审先冻结输入包，再记录带 claim/evidence 指针和验收条件的问题。无法提供独立上下文时，只输出整合式评审并披露限制，不宣称多个审稿人相互盲审。

### 5. 生成图件

先填写 `assets/templates/figure_spec.md`，说明图要支持的主张、数据来源、图件类型、尺寸和输出格式。

- 数据图：代码优先，保存数据、脚本、SVG/PDF 和 PNG。
- 结构图：可编辑矢量优先，保留模块和连接关系。
- GPT Image 2 + PPT 可编辑复现：仅作为 `figure` 的可选分支；按 `ppt-pixel-reproduction.md` 执行生成、分层、PPT 重建、渲染、差分和迭代。

### 6. 运行交付审计

至少检查：主张证据、实验身份、数据划分、图文一致、术语单位、引用双向匹配、合成数据标记、版权、图件可读性和未解决占位符。可运行：

```text
python scripts/audit_manuscript.py manuscript.md --ledger evidence_ledger.csv
python scripts/audit_review_package.py review_issue_ledger.csv --recommendation MAJOR_REVISION
python scripts/figure_qa.py figure.png --output figure_qa.json
python scripts/compare_figure_renders.py reference.png candidate.png --output qa/compare.json
```

## 输出契约

除非用户只要求一个局部成品，按以下顺序交付：

1. 结论或修改后的成品；
2. 使用的证据及其性质；
3. 修改了什么，以及保留了什么；
4. 已完成的验证与结果；
5. 残余风险、缺失证据和结论边界；
6. 最小下一步。

Figure Package 至少包含：

- 图件文件；
- 可运行代码或可编辑源；
- 数据或数据来源；
- 图题与正文引用建议；
- `assumptions` 与版权/来源说明；
- QA 报告；
- 使用 GPT Image 2 时的最终提示词和模型路径说明；
- 使用 PPT 复现时的 `.pptx`、渲染 PNG、差分图、比较指标和偏差记录。

## 资源

### 模板

- `assets/templates/paper_brief.md`
- `assets/templates/evidence_ledger.csv`
- `assets/templates/claim_evidence_matrix.csv`
- `assets/templates/figure_spec.md`
- `assets/templates/terminology_metrics.csv`
- `assets/templates/revision_tracker.csv`
- `assets/templates/review_issue_ledger.csv`
- `assets/templates/reviewer_report.md`
- `assets/templates/ppt_reproduction_spec.md`

### 脚本

- `scripts/init_paper_workspace.py`：建立非覆盖式论文工作区。
- `scripts/audit_evidence_ledger.py`：检查证据类型、来源、状态和可追溯性。
- `scripts/audit_manuscript.py`：检查占位符、高风险措辞、数字主张和证据标签。
- `scripts/audit_review_package.py`：检查模拟评审问题、阻断标记、复审状态和建议的一致性。
- `scripts/figure_style.py`：提供可复用的 Matplotlib 期刊样式与溯源侧车文件。
- `scripts/figure_qa.py`：检查位图尺寸、DPI、对比度和空白占比。
- `scripts/compare_figure_renders.py`：对齐参考图与 PPT 渲染图并输出差分指标和图像。

脚本是确定性辅助工具，不替代人工的科学判断、版权判断和视觉检查。
