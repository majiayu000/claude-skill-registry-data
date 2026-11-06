---
name: science-top-journal-writing
description: Use when drafting or restructuring a manuscript for a high-impact journal, when a paper was rejected for "limited conceptual advance" or "not of broad interest", or when the abstract and title need to carry the claim; covers the C-C-C structure, the five-sentence abstract, figure-first ordering, and the Introduction funnel.
---

# 顶刊写作：让编辑在 60 秒内看懂你在主张什么

## 唯一的判据：标题是不是一个断言

编辑初筛只做一件事——读标题和摘要，判断"这篇稿子提出了什么主张，这个主张重要吗"。

- ✗ `A Study of Chaperone Effects on Protein Folding`（话题）
- ✓ `Chaperone concentration sets the folding rate of globular proteins`（断言）

断言的三个条件：有主语、有方向、可被证伪。满足这三条的标题，摘要和正文会自动变得好写，因为你知道了要证明什么。

## C-C-C 递归：每个尺度都做同一件事

**context → content → conclusion**，在四个尺度上重复：

| 尺度 | context | content | conclusion |
|---|---|---|---|
| 全文 | 领域现状 | 你做了什么 | 改变了什么认知 |
| 一节 | 这节要解决什么 | 具体内容 | 所以呢 |
| 一段 | 上一段留下的问题 | 本段论证 | 本段结论 |
| 一句 | 已知信息 | 新信息 | ——（新信息放句尾，重音位置） |

最常见的失败：段首直接给结果，读者不知道这结果在回答什么问题。把 context 补上，段落立刻可读。

## 摘要 5 句（写完就有 80% 的送审率差异）

1. **背景**：这个领域已经知道什么（一句，不要文献综述）
2. **空白**：还不知道什么、为什么重要（**这句最容易漏，也是编辑判断"为什么现在"的依据**）
3. **做法**：我们做了什么（一句，给关键方法名）
4. **关键结果**：**带数字**——效应量、n、CI
5. **意义**：改变了什么判断

`science_paper_audit` 的 GEN-03/04 查长度与数字，GEN-21 提示你人工确认第 2 句。

## Figure-first：先定 Figure 1 的一句话

不是"先做图再写"，是**先用一句话写下 Figure 1 要传达的信息**，然后：

1. Figure 1 = 全文的核心发现（不是示意图、不是流程图）
2. 每个后续图 = 一个支撑性论证，且图注能独立看懂
3. 正文按图的顺序组织，不按你做的顺序组织

判据：把 Figure 1 和标题一起给别人看，他能否说出你在主张什么。不能就重画。

GEN-13 会查"声明的图数是否都被正文引用"，GEN-22 提示你人工确认 Figure 1。

## Introduction 漏斗（三段，不超过 4 段）

1. 领域现状：**只写支撑你这条断言的文献**，不写"自 1990 年以来……"
2. 具体空白：别人做到哪一步、缺哪一块（引用要精确到具体结论，不是"已有大量研究"）
3. 我们做了什么：一句话给结论，**不列贡献清单**（"本文的贡献有三点"是审稿人反感的写法）

## Discussion：给边界，不复述

- 第一段：一句话重述主张（不是重述结果）
- 中段：与既有工作对比——**你同意谁、修正谁、反对谁**
- 局限性：三条具体局限，每条说明它影响哪个结论、不影响哪个结论（GEN-17 查有没有这段）
- 最后：可检验的下一步，不要"具有重要意义"这种空话

## 送审前最后一次通读的四个检查

1. 每段第一句是不是该段的结论？（不是就重排）
2. 有没有"clearly / obviously / it is well known"？（GEN-15 会抓，删掉换证据）
3. 有没有把"统计显著"写成"证明"？（GEN-16 会抓）
4. 每个数字是否有 n 和不确定性陪着？

## 硬规矩

- 不要靠形容词提重要性。"novel/robust/comprehensive"在标题和摘要里一律删（GEN-02 会抓）。
- 不要写"首次"。除非你做过检索并能在 cover letter 里给出检索式与日期。
- 字数服从期刊上限（GEN-14 只查 8000 词的兜底线，真实上限以目标刊为准，用 `science_journal_fit` 的 `limits` 分项）。
- 语言润色解决不了结构问题。被拒理由若是 "limited advance"，改语法没用，要改主张。
