---
name: science-journal-selection
description: Use when choosing where to submit, when a paper was desk-rejected without review, when deciding between a top journal and a solid sub-journal, or when planning the submission chain; covers the three-tier strategy, why scope beats prestige, format red lines, and how to use transfer and portable-review routes.
---

# 选刊：先算 desk reject 概率，再谈影响因子

## 第一原则：desk reject 的头号原因不是「不够好」，是「投错刊」

编辑初筛以分钟计，只回答一个问题：**这篇稿子在这个刊的读者群里成立吗？**
所以选刊的第一步永远是 scope 匹配，不是影响因子排序。

用 `science_journal_fit` 跑一次，看三档：

- **reach**：档位更高 **且有主题命中**。没有主题命中的综合刊不会进 reach——那不是冲刺，是碰运气。
- **target**：档位匹配、分数够。正常情况下这里是你的第一投。
- **safe**：降 1–3 档且设计兼容。用于时间压力（毕业、结题、抢 priority 窗口）。

`science_journal_fit` 的分数可以逐项拆开，投之前先读它给你的 `matchedTopics` / `missingTopics`：

- 目标刊的 scope 关键词命中 ≥ 一半 → scope 没问题，问题在重要性陈述；
- 命中 0 个 → **换刊，不要改稿**去迁就一个不匹配的刊。

## 第二原则：格式红线比内容更早杀死你

`format` 分项 < 1 就是超限。真实退稿里，超字数、超图数、超参考文献数是最容易被"即时退回"的一类，因为它不需要判断学术价值。

投前必查（`journals.json` 里 `limits` 就是这些）：

- 正文词数（不含参考文献、图注）
- 图表总数（很多刊把"图+表"合并计数）
- 参考文献条数
- 摘要词数、是否有结构化要求

## 第三原则：三个加速通道比"写得更好"更省时间

**1. Registered Reports（若你的研究是假设检验型）**

stage 1 过审即 **in-principle acceptance**，结果不影响录用（除非你偏离注册方案或质量不达标）。300+ 期刊支持。
- 适合：RCT、心理学实验、神经影像、生态学野外实验、任何"结果可能为负"的研究
- 收益：把"结果不好看"这个最大拒稿风险提前消除
- 代价：stage 1 要写清假设、样本量论证、分析计划；中途改分析要标注为 exploratory

**2. Portable review（Review Commons / PCI / eLife Reviewed Preprints）**

一次期刊无关的评审，被十几家期刊承认（eLife、EMBO J、EMBO Reports、LSA、JCB、MBoC、PLOS Biology、PLOS Genetics、Genetics、G3、Genome Biology、Genes & Dev、Open Biology、J Gen Physiol 等）。
- 收益：省掉 2–3 轮重复外审，每轮通常 2–4 个月
- 前提：预印本（评审对象是 bioRxiv/medRxiv 上的版本）
- 用法：`science_journal_fit` 传 `needsPortableReview: true`，看哪些 target 刊接受

**3. Transfer / cascade**

被拒后用出版社的转投服务，带着审稿意见走，不重新排队。
- Nature 系：Nature → Nature Communications → Scientific Reports
- Cell 系：Cell → Molecular Cell / Cell Reports → iScience
- Elsevier / Springer 也有各自的 article transfer service
- **注意**：transfer 前先确认审稿意见对新刊仍然适用；不要把针对 Nature 的"importance"批评原封不动带到子刊

## 第四原则：投稿顺序是一次决策，不是一连串反应

写下来再投：

```
1. target（第一投）          预计 desk 决定 X 天
2. reach（可选，仅当有主题命中且你有时间）  
3. target 的第二选择（不同出版社，避免同一编辑群）
4. safe（保底）
```

每一档都要提前想好：**如果在这里被 desk reject，理由最可能是什么，我下一步改不改稿？**
如果答案是"不改"，说明这档本来就不该投。

## 硬规矩

- 不要同时投两家（一稿多投在所有目标刊都是红线）。
- 预印本先发不违反多数期刊政策，但 NEJM/JAMA 等对"已公开"有额外解释，投前查当期政策。
- 不要在 cover letter 里写"本研究首次……"却不给检索证据；编辑会当场怀疑。
- `journals.json` 的 `acceptRate` / `deskRejectRate` 是**量级估计**，只用于排序。不要拿它算"我投 5 次能中 1 次"。
- 画像超过 12 个月未核验时，工具会降置信度；此时字数与图数上限以官网为准。
