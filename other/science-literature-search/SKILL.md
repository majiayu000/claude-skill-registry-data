---
name: science-literature-search
description: Use when starting a literature review, checking whether an idea is already published, or updating a topic search; covers query construction, multi-source coverage, deduplication, inclusion criteria, and what must be recorded so the search is reproducible.
---

# 文献检索（可复现的检索策略）

## 何时用
- 课题开局要做现状梳理；
- 有 idea 需要做新颖性（scoop）检查；
- 距离上次检索超过 3 个月，需要增量更新。

## 前置检查
1. `science_preflight` 已跑过，数据根与技能就位；
2. 确认检索源：`mcp__paper__*`、`mcp__arxiv__*`、`mcp__zotero__*` 是否可用；不可用则退化为 `web_search` + `web_fetch` 打公开 API（Crossref / OpenAlex / Semantic Scholar / PubMed E-utilities），并在结果里标注"覆盖度下降"。
3. 与用户确认三件事：**时间窗**、**语言**、**纳排标准**（哪些不算：预印本？综述？非同行评议？）。

## 步骤
1. **拆概念块**：把课题拆成 2–4 个概念块（PICO 或"方法 + 对象 + 指标"），每个块列同义词、缩写、上下位词。
2. **构造检索式**：块内 OR，块间 AND。例：
   - `("reinforcement learning" OR RL) AND (protein OR "protein design") AND (diffusion OR "generative model")`
   - 中文库另写一份（CNKI/万方用主题词 + 同义词）。
3. **多源执行**：至少 2 个源；确保 arXiv 覆盖预印本、PubMed 覆盖生物医学、OpenAlex 覆盖跨库引用。每个源记录：库名、检索式、时间、结果数。
4. **去重**：按 DOI → arXiv id → 标题指纹（去标点、小写、去副标题）+ 首作者 + 年份 三路去重。落库走 `science_lit_search`，重复项不要重复入库。
5. **两阶段筛选**：先标题+摘要（记录排除理由代码），再全文。排除理由必须可统计（PRISMA 流程图用）。
6. **滚雪球**：对纳入的每篇做前向（被引）+ 后向（参考文献）各一轮，重点找 2 篇最相关的。
7. **落库与汇报**：`science_lit_search` 落 `paper` 表；汇报只写：源与检索式、命中数、纳入数、最相关的 5 篇 + 一句话差异。

## 产出与落库
- `paper` 表：doi / arxiv_id / title / authors / year / venue / url / pdf_path / source / added_at
- 检索过程写进项目 `logs/search-<date>.md`（检索式、库、时间、命中数），供复现
- `science_novelty`：最接近的 10 篇 + 与 idea 的差异点

## 常见失败与降级
- **MCP 全挂**：走公开 API 兜底，明确告诉用户"只覆盖 X 库"。
- **命中 >500**：先收紧时间窗或加限定词，不要一次性拉全量（token 与速率都会崩）。
- **完全无命中**：这本身是结论（可能是真空白，也可能是检索式写得过窄）；换 2 套检索式再确认，然后如实报告"未检索到直接相关工作"。
- **警惕**：不要凭记忆补引用。任何作者/年份/DOI 都必须来自库内记录。
