---
name: math-model-selector
description: 数学建模竞赛「题型→模型」选择路由器（国赛/美赛/华数杯/电工杯/MathorCup）。按题型主类、数据规模、约束特征推荐模型框架与 Python 库，输出「子问题|模型|原因|Python库|备选」选择表。触发：选题/用什么模型/模型选择/题型判断/方法推荐/怎么建模。由 contest-orchestrator 主控调用；与 topic-scorer（选题评分）分工，math-modeling 仅作兼容入口。
metadata:
  version: "2.0"
---

# math-model-selector — 竞赛题型 → 模型路由

## Contest-Orchestrator Adapter

本技能只负责已选题目的模型框架选择；`contest-orchestrator` 保持模式、范围、任务卡和最终裁决的唯一权威。调用时读取项目工作区中的 `problem_condition_ledger.yaml`、`problem_graph.md`、数据审计和已登记证据，输出可写入 `model_blueprint.yaml`/`model_contract.yaml` 的结构化候选。

- 每个候选必须给出题面或文献证据定位、适用条件、失效条件、复杂度/求解风险和 baseline；不得凭空添加模型、参数或库。
- 对涉及数据规模、指标或参数的候选登记 `numeric_source_map` 数值来源；需要随机求解时同时登记 `seed`。
- 返回 `status`、`active_mode`、`task_card`、`artifacts`、`evidence`、`checks`、`blockers`、`next_node` 节点包；候选与选择依据登记到项目工作区的 `run_manifest` 和 `result_registry`，不写入 skill 安装目录。
- 模型、符号、数据和引用缺证据时返回 `BLOCKED_INPUT`；不替主控启动求解、论文或交付流程。
- 节点包和任何项目成品不得包含负回响、元话语或内部交流内容；新符号必须在论文首用处定义。

`active_mode: full-contest-mathorcup` 时，M1 只依据 `problem_statement.md`、`data_overview.yaml`、`task_kpi.yaml` 和题面证据提出逐问候选与指标/数据需求，不替用户批准最终路线；M3 由唯一 solver 结合 M2 `eda_report.md`、`features.yaml`、`leakage_audit.yaml` 和已确认文献用途确定统一 baseline、候选、分割策略、指标及计算预算。每个候选说明跨问输入输出和参数传递；题型、指标或样本结构不支持的方法不进入候选。候选表是决策依据，不是已执行结果；实际运行、数字与最终结论只由 M3 求解证据和独立验证确定。通用速查表及实现优先级仅作参考，不构成固定算法顺序。

## 定位与分工（避免与兄弟 skill 打架）

MathorCup 选择路线前，按 `data-science-stack/references/mathorcup_experiment_protocol.md` 核对当前安装版本、实际估计器 API、损失、目标耦合与拟合数量。多输出接口不自动证明利用目标相关性，旧版包装器也不证明当前估计器不支持多输出。算法比较和特征变换消融分别设计；候选是否采纳以预登记标准和完整对照为依据，不为新颖性强行引入未采用的方法。

| 决策 | 归属 |
|---|---|
| 选**哪道题**（多题评分/经验覆盖） | `contest-orchestrator` 的 **topic-scorer** |
| 选定题目后选**什么模型框架** | **本技能** |
| 全流程执行（建模/求解/论文） | `contest-orchestrator` 主控（`math-modeling` 仅作兼容入口） |

> 本技能只在"题目已定、开始设计模型"时介入；不替代选题评分，不写论文。

## 输入

- 题目描述 + 问题分解（来自 `contest-orchestrator` problem-parser 的 problem_graph；兼容 `math-modeling` 阶段1 输出）
- 关键信息：子问题列表、数据规模（<100 / 100-1w / >1w）、约束类型（线性/非线性/整数/动态/空间/时序）、目标（单/多/模糊/鲁棒）

## 工作流（4 步）

1. **判题型主类**（对照下方速查表）：
   - 优化/规划 / 预测 / 评价/决策 / 分类/聚类 / 微分方程(机理) / 图/网络 / 时间序列 / 统计/相关 / 排队论 / 博弈论
2. **看数据与约束**：数据规模决定 ML 还是机理；整数/非线性决定求解器（精确 vs 启发式）
3. **查速查表**选主模型 + 备选（备选必须来自表格或文献，禁止现场发明）
4. **输出模型选择表**（子问题 | 模型 | 原因 | Python库 | 备选方案），喂给求解阶段

## 详细决策参考（按需加载）

- 速查表覆盖 10 大题型主类；需要 **95+ 细分场景**（数据规模、约束类型、目标冲突、参数建议）时，加载 `references/model-selection-matrix.md`（模型决策矩阵，含冲突裁决规则与快速决策速查）。矩阵是知识参考，最终选择必须结合题目约束与团队判断。
- 需要 **实现路由决策**（选完模型后决定由哪个子 skill 落地：pyomo / heuristic-algorithms / data-science-stack / 解析求解）时，加载 `references/model-selection-matrix-harness.md`（harness 版矩阵，含实现路由列与三问裁决：题目特征、问题规模、用户背景优先）。
- **防炫技方法选择**（通用扎实方法优先级表 P0-P3、复杂度升级树、炫技检测清单 8 项、模型-假设一致性检查、方法选择 7 问）时，加载 `references/anti_flashy_method_guide.md`。核心原则：方法适配问题，而不是越复杂越好；复杂方法不是默认候选，而是"经论证后获得准入资格"的候选。

## 题型→模型速查表

| 问题类型 | 竞赛频率 | 推荐模型 | Python 库 |
|---------|:---:|---------|--------|
| 优化/规划 | 极高 | LP/MILP/NLP、遗传算法、PSO | pyomo, pulp, scipy.optimize, geatpy |
| 预测 | 高 | XGBoost、随机森林、ARIMA、LSTM、GM(1,1) | sklearn, statsmodels, xgboost |
| 评价/决策 | 高 | AHP、TOPSIS、熵权法、模糊综合评价 | numpy 手写 |
| 分类/聚类 | 中 | K-Means、SVM、DBSCAN、层次聚类 | sklearn |
| 微分方程(机理) | 中 | ODE/PDE 数值求解、SIR、传热/光学模型 | scipy.integrate |
| 图/网络 | 中 | 最短路径、最大流、最小生成树 | networkx |
| 时间序列 | 中 | ARIMA、SARIMA、Prophet、LSTM | statsmodels, prophet |
| 统计/相关 | 低 | Pearson、Spearman、灰色关联、主成分 | scipy.stats, numpy |
| 排队论 | 低 | M/M/1、M/M/c 模型 | simpy, 手写 |
| 博弈论 | 低 | Nash 均衡、演化博弈 | nashpy, 手写 |

**快速路由规则**：
- 「产量最大/损失最小 + 容量/预算限制」→ 优化（先 LP/MILP，超时切启发式）
- 「历史数据 + 未来值」→ 预测/时间序列（先 baseline，再 ARIMA/XGBoost）
- 「实测离散数据 + 几何/物理要素标注」→ 统计/数据处理或机理反演（先判题型再选）
- 「物理/工程背景 + 连续演化」→ 微分方程/机理建模（ODE 起步）
- 「排名/评价/多指标」→ 综合评价（熵权+AHP+TOPSIS 组合）

## 输出格式

```markdown
## 模型选择表
| 子问题 | 模型 | 原因 | Python库 | 备选方案 |
|--------|------|------|----------|----------|
| Q1 | ... | ... | ... | ... |

求解优先级：精确（pyomo）→ 启发式（heuristic-algorithms）→ 简化/近似
```

## 与现有体系对接

- **求解实现**：精确用 `pyomo`；超时/不可行切 `heuristic-algorithms`（GA/SA/PSO/蒙特卡洛/ODE）
- **C 题数据链路**：EDA→预处理→统计→ML→时序 走 `data-science-stack`
- **结果可视化**：数据结果图 scipilot-figure-skill → modelviz → scipilot-figure-skill；所有非数据图 tikz-scientific-figures；Draw.io 仅用户明确要求时使用
- **竞赛全流程**：作为 `contest-orchestrator` planner 的模型选择器调用（兼容 `math-modeling` 阶段2 入口）

## 边界（不做）

- ❌ 选题评分（那是 `contest-orchestrator` topic-scorer）
- ❌ 文献调研（用 web 搜索）
- ❌ 写论文（`contest-orchestrator` 主控下的 `mathmodel-latex-skill` / `latex-paper-en`）
