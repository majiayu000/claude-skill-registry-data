---
name: science-statistics-choice
description: Use when you have data and must decide which test to run — when someone asks "该用什么检验", when a reviewer says the analysis does not match the design, when assumptions are violated and you need the honest fallback instead of the convenient one, when the effect size or correction method is missing from the results, or when a p-value is being asked to carry a claim it cannot carry; also use before data collection to size the study, and when interpreting a result that is significant but tiny.
---

# 统计选择：设计决定检验，假设决定能不能用

## 三条不能破的铁律

1. **检验由设计决定，不由数据长什么样决定。**
   先有 `design`（几组、配对否、结局类型、是否重复测量），才有候选检验。
   拿到数据后试三种检验挑 p 最小的，那不是分析，是搜索。
2. **假设不满足时必须降级，不能默认继续。**
   每个检验都带 `assumptions` 与 `fallback`。假设没查或不满足，正确动作是
   **换 fallback 检验并在正文说明**，而不是「反正结果差不多」。
3. **p 值不是效应量。** 报告必须同时给：检验统计量、自由度、p、效应量、效应量的置信区间。
   缺效应量的结果在顶刊会被直接退回补充。

## 决策树怎么走

决策树只问**设计问题**，不问「你希望显著吗」。

```
根节点 outcome（结局类型：连续 / 二分类 / 计数 / 生存 / 有序 / 多元）
  → design-*（组数、配对、独立、重复测量）
    → 叶子：一个检验 id + 该检验的假设清单 + fallback 链
```

走不下去时通常是两个原因：结局类型没说清（"分数"是连续还是等级？），
或者设计里有嵌套（同一被试多次测量 → 那是重复测量，不是独立两组）。
这两个都要先答清楚，再回来走树。

每个叶子给出的是**检验 id**，用它去 `data/statistics.json` 取完整定义：
`requires` / `assumptions` / `fallback` / `effectSizes` / `power` / `py` / `reportAs` / `misuse` / `source`。

## 选检验时必须一起决定的四件事

### 1. 单双侧

双侧是默认。单侧只在**事前**有方向性假设且方向不可反时使用，
并且必须在方法里写明"单侧检验，方向为 X"。事后按结果挑方向 = p 值减半的作弊。

### 2. 多重比较

| 情况 | 用什么 | 为什么 |
| --- | --- | --- |
| 一个主假设 | 不校正，但必须声明"这是唯一主结局" | 校正会无谓损失功效 |
| 少数几个预设的次要结局 | Holm | 控制 FWER，比 Bonferroni 更有功效 |
| 探索性、大量指标（组学、脑影像体素） | BH（FDR） | 控制错误发现比例 |
| 相关性强（脑区、时间点） | BH 偏保守，考虑置换检验 | 独立性假设不成立 |

**绝不能做的事**：测了 12 个指标，只报 p<.05 的 3 个，不说测了 12 个。
这在方法上叫选择性报告，在结果上让「显著」变成必然事件。

### 3. 效应量与它的置信区间

效应量要和检验配套：t 检验配 Cohen's d、ANOVA 配 η²/偏 η²、卡方配 Cramér's V 或 OR、
生存配 HR 或 RMST 差、非参数配 rank-biserial 或中位数差。

「小/中/大」的标签（.2/.5/.8）是**跨领域的粗糙约定**，不是判决。
在心理学 d=0.3 可能很重要，在药物试验里 d=0.3 可能毫无临床意义——
判断标准是这个领域的**最小可觉察/最小临床重要差异**，不是标签。

### 4. 功效

功效必须**事前**算。给 `α`、目标 `power`（默认 .80，复制研究用 .90）、
以及**最小有意义的效应量**（不是文献里最大的那个），反推 n。
聚类设计还要乘设计效应 `1+(m-1)ρ`。

事后算功效没有意义：observed power 是 p 值的单调变换，不提供新信息。

## 假设检查：怎么查、查不过怎么办

| 假设 | 怎么查 | 不过时换什么 |
| --- | --- | --- |
| 正态性 | Shapiro-Wilk（n<50）/ 偏度峰度 + QQ 图（n≥50） | Mann-Whitney / Wilcoxon / 置换检验 |
| 方差齐性 | Levene | Welch t / Welch ANOVA（**不要**先检验再选方法，直接用 Welch） |
| 球形性 | Mauchly | Greenhouse-Geisser 校正 / 混合模型 |
| 独立性 | 看设计，不看数据 | 聚类稳健 SE / 混合模型 |
| 线性 | 残差 vs 拟合图 | 加非线性项 / 样条 / 分位数回归 |
| 比例优势 | 平行线检验 | 有序 probit / 多项 logit / 部分比例优势 |
| 比例风险（Cox） | Schoenfeld 残差 | 分层 Cox / 时间依赖系数 / RMST |
| EPV（每变量事件数） | 事件数 ÷ 预测变量数 | Firth 惩罚 / 减少变量 / 正则化 |

一个常见错误：**先做方差齐性检验，再决定用 t 还是 Welch**。
这个两阶段流程本身会让 α 失控。正确做法是**一律用 Welch**，它方差不齐时正确、方差齐时几乎无损。

## 本应用能直接跑的

`science_stats`（M6c）执行的是 `data/statistics.json` 里 `py` 字段的实现，
全部走 numpy/scipy/statsmodels，固定 `default_rng(seed)`，输出结构化 JSON（含检验统计量、
自由度、p、效应量、CI、假设检查结果、以及用到的 fallback）。

没装 `lifelines`、`pymc` 时，生存与贝叶斯走解析兜底（KM + log-rank、JZS Bayes 因子），
结果里会标 `method: "fallback"`——**看到这个标记要写进方法段**，不能当成库调用。

## 结果怎么写

```
Welch 双样本 t 检验：t(37.2) = 2.41，p = .021，Cohen's d = 0.72，95% CI [0.11, 1.33]。
假设检查：Shapiro-Wilk 提示对照组偏离正态（W = .91，p = .032），
以 Mann-Whitney U 复算结论一致（U = 214，p = .028，rank-biserial r = .31）。
```

四段齐全：**检验名 + 统计量(自由度) + p + 效应量 + CI**，然后假设检查，然后稳健性。
少任何一段，审稿人都有理由让你重做。

## 常见误用清单

- 拿 p>0.05 宣称「没有差异」→ 要用等效性检验（TOST）并预设等效界值
- 把 OR 当 RR 说（二分类结局常见率被高估）
- 在 8 个亚组里挑显著的讲机制（亚组必须是事前的，且要校正）
- 用完整案例分析处理缺失（MAR 下产生偏倚，且浪费样本）
- 只报均值不报分布（柱状图会藏掉离群与双峰，改用带散点的图）
- 相关当因果（横断面永远不行，纵向也只能排除部分方向）
- 中位数差当均值差报（分位数回归的系数不是均值效应）
