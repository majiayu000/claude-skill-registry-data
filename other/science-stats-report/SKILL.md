---
name: science-stats-report
description: Use when a statistical result has to leave the analysis tool and enter a manuscript — when writing the statistics paragraph, the table notes, or the figure caption that carries a p-value; when someone asks how to report a test, an effect size, or a confidence interval; when a result is significant but the assumption check failed; when a chi-square had Yates correction or not and the value differs between tools; also use when a reviewer asks for the numbers behind a claim.
---

# 把统计结果写成审稿人认的句子

## 一句话标准

一个结果要能独立成立，必须同时给出：**样本量 → 统计量 + 自由度 → p → 效应量 + 置信区间 → 用的是哪个检验、为什么**。
缺任何一项，这一段就会被要求补充；缺效应量最常见。

## 模板（照抄结构，别照抄数字）

```
Welch 双样本 t 检验比较咖啡因组（n = 24，M = 421 ms，SD = 52）与安慰剂组
（n = 24，M = 452 ms，SD = 55）的简单反应时，两组差异未达显著，
t(44.79) = −1.95，p = .058，Cohen's d = −0.57（95% CI −1.15 至 0.02）。
```

要点：

- `t(44.79)` 的自由度带小数，因为用的是 Welch 而不是合并方差 t。写成整数说明你用了等方差假设，或者算错了。
- `p = .058` 不写 `p = 0.058`（多数刊要求省略前导零），`p < .001` 才用小于号。
- 效应量后面必须括号给 CI。**CI 跨 0 时不能说"有趋势"**——趋势是没做检验的说法。
- 组统计量（M、SD、n）写在括号里，读者不用回表。

## 不同检验的报法

| 检验 | 统计量格式 | 效应量 | 常见错 |
| --- | --- | --- | --- |
| Welch t | `t(df) = x.xx` | Cohen's d + CI | df 写成整数 |
| 配对 t | `t(n−1) = x.xx` | Cohen's dz + CI | 用独立样本 d 代替 dz |
| ANOVA | `F(df1, df2) = x.xx` | η² 或 partial η² | 只报 F 不报 η² |
| 卡方 | `χ²(df) = x.xx` | Cramér's V | 不说明有没有 Yates 校正 |
| Mann-Whitney | `U = x.xx` | rank-biserial r | 报成"中位数检验" |
| 回归 | `β = x.xx, SE = x.xx, t = x.xx` | 调整 R²（整体）/ 半偏 r²（每个系数） | 只报 p 不报系数与 SE |
| Logistic | `OR = x.xx (95% CI …)` | McFadden R² / AUC | OR 与 RR 混用 |
| 生存 | `HR = x.xx (95% CI …)` | 中位生存 / RMST | 不做比例风险检查就报 HR |

## 卡方：Yates 校正是必须先声明的

同一个 2×2 表，校正与否统计量差很多（例：7.92 vs 9.09）。`science_stats` 默认用 Yates 并同时给出未校正值，
写在 `uncorrected` 里。正文要说清用的是哪个：

> `χ²(1) = 7.92，p = .005（Yates 校正）；未校正 χ² = 9.09，p = .003。`

两个都给不丢人，只给一个又不说哪个才是问题。

## 假设不满足时怎么报

不能说"虽然不满足正态性，但 t 检验通常稳健"——这句话在有离群点的小样本里是错的。

正确写法：

> 反应时分布右偏（Shapiro-Wilk，p < .001），故改用 Mann-Whitney U 检验：
> U = 118，p < .001，rank-biserial r = −0.74。结论方向与 t 检验一致。

关键在最后一句：**换检验后方向一致，本身就是一个稳健性证据**。方向变了，那才是要坐下来想的事。

## 多重比较

- 主假设一个：不校正，在方法里写"主结局单一，未作多重比较校正"。
- 次要结局多个：事前声明校正方法（Holm 优先于 Bonferroni；探索性分析用 BH 控 FDR）。
- 事后补的校正要说明是事后补的。审稿人分得清。

## 不该出现的句子

- "接近显著"（marginally significant）、"有趋势" → 都是没做检验的判断。
- "p = .06，说明有边缘效应" → p 是连续量，没有边缘。
- "证明" → 统计只能不拒绝，不能证明。用"支持""与……一致"。
- "由于样本量小，结果仅供参考" → 要么做功效分析说清能检测多大效应，要么别写这句挡箭牌。

## 交付前自查

1. 正文每个 p 都能在 `science_exp_query { what: 'analyses' }` 里找到对应记录吗？
2. 每个效应量都有 CI 吗？
3. 表注里写清误差棒是 SD / SEM / 95% CI 了吗？
4. 换了检验的地方，方向是否一致？不一致有没有解释？
5. 有没有哪个数字是从旧版结果里抄来的？
