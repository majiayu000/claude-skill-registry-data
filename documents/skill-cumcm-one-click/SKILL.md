---
name: cumcm-one-click
description: "Use when the user provides a mathematical modeling contest problem (数学建模国赛 CUMCM / 高教社杯 / 美赛 MCM-ICM / 研赛 / 五一赛 / 电工杯等赛题、题目、真题) and wants it completed end to end - including 一键完成、帮我建模、从赛题到论文、写论文、数据处理、模型选择、求解、验证、敏感性分析、图表和 Word/LaTeX 交付。"
metadata:
  agent_created: true
---

# 数学建模竞赛一键建模

## 使用协议

将本 skill 视为“问题到可审校论文”的完整流水线，而不是模型名称列表。每次触发后：

1. 读取 [manifest.yaml](manifest.yaml)。
2. 读取 `always_load` 指定的核心规则。
3. 根据用户请求选择 `manifest.yaml` 中的阶段；完整论文任务按默认顺序加载全部阶段。
4. 仅在当前阶段需要细节时读取 `references/` 中的深层参考。
5. 将中间表、代码、图片、日志和审计报告收束到完整论文及可复现支撑材料。

阶段顺序为：读题 -> 数据预处理与探索 -> 模型建立 -> 结果可视化 -> 敏感性分析 -> 模型检验 -> 模型创新 -> 论文撰写。用户只要求局部修改时，只加载受影响阶段及其必要前置阶段。

若题目、附件、约束、目标输出或交付格式缺失，先输出简短 alignment block：已知信息、关键缺口、当前理解、最多 2-3 个必须确认的问题；不要在错误前提上直接生成完整论文。

## 不可跳过的纪律

1. **证据优先**：每个关键数字绑定到 `results/` 文件、运行日志、公式、图或表；维护 `Claim -> Data / Formula / Figure / Validation / Sensitivity` 溯源表。
2. **不伪造**：不编造数据、结果、参考文献、约束、假设、排名或官方成绩；内部模拟、合成数据和示例结果必须明确标注。
3. **先基线后改进**：先用可解释、可复现的基线模型闭环，再加入最多一处能被对比验证的有效改进；复杂模型必须有精度、可行性、稳健性或解释性收益。
4. **模型要能写清**：每个模型都必须说明建模目的、变量/参数、数据输入、公式、目标或损失、约束、求解步骤、参数依据、输出转译、检验指标和适用边界。
5. **检验不能形式化**：预测做误差/残差/基准比较，优化做可行性/目标/收敛检查，评价做权重/排序稳定性，分类聚类做匹配指标，仿真做重复性/边界/历史对照；根据模型类型选择证据。
6. **敏感性必须服务结论**：只扰动会影响结论的权重、参数、阈值、边界、初值或数据；说明扰动理由、范围、变化量、阈值和稳健性边界。
7. **图表是证据**：主体数据图用 Python 可复现绘图库生成；每图/表有编号、单位、来源、图注和紧邻解释，不用装饰图、截图、默认 Excel/PPT 图或 AI 图替代数据图。
8. **格式服从当届官方规则**：当前国赛默认正文不超过 30 页、摘要页为第 1 页、正文不设目录；若当届官方规则变化，以官方文件为准。不要把外部资料中的“正文不少于 30 页”当作硬性要求。
9. **AI 合规**：按 `references/ai-compliance.md` 执行。参考文献前放当届规定的 AI 工具使用声明；使用 AI 时生成文件名为 `AI工具使用详情.pdf` 的 PDF，所有核心内容经人工核验。
10. **交付前闭环**：运行 `references/checklist.md` 全项检查，并输出 `results/self-review.md` 和完成度报告。

## 一键执行流程

### 1. 建立问题台账

- 通读题面和全部附件（PDF、图片、Excel、CSV、文本），不要只看题干摘要。
- 对每个小问记录：原题要求、任务类型、输入、输出、显性/隐含约束、评价标准、模型方向和必须呈现的结果。
- 识别问题之间的衔接，例如“先预测后优化”“先评价后决策”。
- 输出 `problem/problem-brief.md`，包含背景、问题拆解、附件用途、路线图和风险。

### 2. 建立数据台账并审计

- 先列文件、字段、类型、单位、时间/空间范围、样本量及其服务的小问，再合并多源数据。
- 运行：

  ```bash
  python scripts/audit_data.py --data data/ --out tables/data-audit.md
  ```

- 检查缺失、重复、异常、单位/统计口径、时间泄漏和题目要求但数据未直接提供的变量。
- 原始数据保留在 `data/raw/`；清洗、填补、缩尾、修正、标准化和特征构造的理由写入台账，不机械删除或填补。
- 探索性图表只保留能影响模型选择或论文结论的图。

### 3. 设计模型路线

- 读取 `references/model-cookbook.md` 和当前阶段深层参考。
- 为每个小问写出候选模型、选择理由、变量、目标/评价函数、约束、输入输出衔接和检验计划。
- 小样本优先统计/灰色/可解释模型；中等样本可用传统机器学习；时间序列先检验趋势、周期、平稳性和泄漏；优化先验证可行域；仿真先说明状态、转移、随机分布和重复次数。
- 先实现基线，再做一处有效改进并给出改进前后数值对照。

### 4. 求解与复现

- 默认 Python（pandas/numpy/scipy/scikit-learn/networkx/statsmodels/pymoo），必要时使用 MATLAB；记录依赖版本、随机种子、输入文件 SHA-256、求解参数、停止条件和异常处理。
- 每个脚本有明确输入/输出，运行命令唯一；结果按小问落盘到 `results/`，图表到 `figures/`，表格到 `tables/`。
- 多模型串联时明确前一模型输出如何成为后一模型输入，不能把代码顺序当作论文逻辑。

### 5. 验证、敏感性与可视化

- 按模型类型选择检验指标，报告数值、比较对象和含义，不只贴指标。
- 运行 `python scripts/sensitivity.py` 做有理由的 OAT、情景、权重、约束或随机扰动；写出结果变化和稳定性边界。
- 为每个小问建立“结论-证据-图型”清单；主体图使用 matplotlib/seaborn/plotly/networkx/scipy/statsmodels/pandas，至少 300 DPI，统一字体、颜色和线宽。
- 每张图后说明可见事实、对应题目、支撑结论、现实含义和不确定性；若无法支撑结论，删除或重画。

### 6. 撰写完整论文

- 论文按题目问题组织，不按脚本运行顺序组织。默认结构：

  ```text
  题目 -> 摘要/关键词 -> 问题重述 -> 问题分析 -> 模型假设 -> 符号说明
  -> 数据预处理与可视化 -> 模型建立与求解 -> 结果分析与可视化
  -> 敏感性分析 -> 模型检验 -> 模型创新 -> 模型优缺点与推广
  -> 结论 -> 参考文献 -> 附录
  ```

- 摘要按“解决什么问题 -> 用什么模型/算法 -> 具体数值结果 -> 结论/意义”写，覆盖所有小问，禁止“效果较好”等无数值空话。
- 每问开头呼应题目并说明思路，正文给出原理、公式、求解和结果，每问结尾明确回答原题并说明对后续问题的作用。
- 公式使用可编辑公式对象，不以程序文本或截图替代；变量首次出现必须解释，符号含义保持一致。
- 交付 Word 时按需运行：

  ```bash
  python scripts/verify_docx_math.py paper/final.docx
  python scripts/verify_docx_typography.py paper/final.docx
  python scripts/verify_docx_figures.py paper/final.docx
  ```

  脚本通过后仍需渲染 Word/PDF 逐页检查公式、字体、标题颜色、图例、清晰度和图文衔接。

### 7. 评委式自评与交付

- 按 `references/checklist.md` 输出 `results/self-review.md`：百分制得分、扣分点、预估位次区间和优先修改建议。位次只能写内部估计，不能冒充官方排名。
- 最终目录至少包括 `paper/`、`figures/`、`tables/`、`results/`、`src/`、`README-复现.md`；按当届规则准备匿名论文、支撑材料清单、程序代码和 `AI工具使用详情.pdf`（如适用）。
- 输出完成度报告：逐问闭环状态、关键数字溯源状态、验证/敏感性状态、格式检查结果和仍需人工确认的事项。

## 症状分诊（按需加载）

| 任务 / 症状 | 加载 |
|---|---|
| 读题、拆小问、提取隐藏约束 | `references/problem-reading.md` |
| 数据清洗、缺失处理、特征构造 | `references/data-preprocessing-visualization.md` |
| 选模型族、变量/目标/约束设计 | `references/model-cookbook.md` + `references/model-construction.md` |
| 检验怎么配（预测/优化/评价/聚类/仿真） | `references/model-validation.md`（敏感性分析已并入其末尾） |
| 扰动参数、稳健性写作 | `references/model-validation.md` 末尾「敏感性分析」节 |
| 图怎么选、配色、图注、图表密度 | `references/result-visualization.md` + `references/paper-depth-visual-density.md` |
| 论文结构、摘要/结论规则、附录 | `references/paper-writing.md` |
| 排版：字体/公式/OMML/图生成 | `references/typography-and-python-figures.md` + `references/word-latex-formulas.md` |
| 页数压不下来、Word/PDF 生成报错、交付细节踩坑 | `references/practice-lessons.md` |
| 当届官方页数/匿名/格式 | `references/paper-requirements.md`（顶部为当届快照，过期核对 mcm.edu.cn） |
| 评审策略、赛程、交卷检查 | `references/judging-and-strategy.md` + `references/contest-insights.md` |
| AI 工具声明与合规 | `references/ai-compliance.md` |
| 交付前自评 | `references/checklist.md` |

论文骨架以 SKILL.md「撰写完整论文」节的 16 段结构为权威完整版；`assets/paper-skeleton.md` 为最小骨架（可扩展，不含数据预处理专章时按完整版补齐）。

复用脚本：`scripts/audit_data.py`（输出 `tables/data-audit.md`）、`scripts/sensitivity.py`、三个 `verify_docx_*.py`（各自输出审计表，通过后再人工渲染检查）。

> 逐阶段路由（哪个阶段先加载哪些文件）由 `manifest.yaml` 机器可读定义；本表是人工可读的速查版，两者不一致时以 `manifest.yaml` 为准。

## 常见错误与纠正

| 错误 | 纠正 |
| --- | --- |
| 没有问题/数据台账就选模型 | 先锁定输入、输出、约束、单位和评价标准 |
| 只写模型名称或只贴公式 | 按“机制 -> 数学抽象 -> 公式 -> 求解 -> 输出 -> 检验边界”展开 |
| 复杂算法没有基线和对照 | 先做简单基线，再给改进前后误差/目标值/可行性对比 |
| 敏感性分析扰动无关参数 | 只扰动会改变结论的参数，并说明范围来源 |
| 图表孤立、无单位或由截图拼成 | 用 Python 生成，补齐图注/单位/来源，并在图后解释 |
| 把“正文不少于 30 页”当作国赛硬规则 | 以当届官方规则为准，当前默认正文不超过 30 页 |
| Word 公式只是 `t_ij` 或 `$...$` 文本 | 转成真实 OMML 结构并运行 `verify_docx_math.py` |
| 标题保留蓝色或 Word 默认字体 | 统一中文宋体、英文数字 Times New Roman，标题黑色，并运行字体审计 |
| 未经人工核验的 AI 输出进入核心成果 | 记录使用、逐项核验，按当届规则生成声明和详情 PDF |
| 正文超页就删模型内容 | 先砍与摘要重复的叙述、把含公式段落行距改为“最小值”、收紧标题间距；删模型内容是下策 |
| 手工编辑生成的 docx | 改动回到源头（Markdown 或构建脚本），改完按构建链重跑，手工改动下次重建即丢失 |
| 正文汇总数字与明细表加总不一致 | 交付前做数字对账，每个汇总数字都要能由论文表格或结果文件复现 |
