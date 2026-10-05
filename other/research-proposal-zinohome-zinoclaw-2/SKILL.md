---
name: research-proposal
description: >
  撰写学术研究计划（Research Proposal）。
  触发词：写研究计划、research proposal、PhD proposal、博士申请、研究方案、撰写开题报告。
  支持 STEM、人文、社科领域，中英文输出。
metadata:
  author: openclaw-community
  version: 2.0.0
requires:
  bins:
    - node
    - curl
allowed-tools:
  - exec
  - Read
  - Write
  - Edit
  - AskUserQuestion
  - Glob
  - Grep
---

# Research Proposal Generator

**所有文献搜索必须且只能通过 exec 执行下面的 node 命令。禁止使用 web_fetch、web_search 或任何其他工具搜索文献。**

## 文献搜索命令（三个数据库）

```bash
# arXiv（理工科、CS、物理、数学）
node {{SKILL_DIR}}/scripts/search_arxiv.mjs "<关键词>" [数量]

# PubMed（生物医学、生命科学）
node {{SKILL_DIR}}/scripts/search_pubmed.mjs "<关键词>" [数量]

# Semantic Scholar（全学科，含引用数）
node {{SKILL_DIR}}/scripts/search_semantic.mjs "<关键词>" [数量]

# 获取单篇论文详情（含参考文献列表）
node {{SKILL_DIR}}/scripts/fetch_paper.mjs <id_type> "<id>"
# id_type: arxiv | doi | pmid | s2
```

数量默认 10，最大 30。

## 用户意图 → 你的动作

| 用户说 | 你做什么 |
|--------|----------|
| 写研究计划/proposal | 进入 Phase 1 收集信息 |
| 搜文献/找论文 | 用上面的搜索命令 |
| 某篇论文的详情 | 用 fetch_paper.mjs |

---

## 工作流程（5 个阶段）

### Phase 1: 收集需求

用 AskUserQuestion 收集：

1. **研究方向** — 核心问题是什么？
2. **学科领域** — STEM / 人文 / 社科
3. **输出语言** — English / 中文
4. **目标字数** — 默认 ~3,000 词
5. **目标院校**（可选）
6. **已有材料**（可选）— 用户可粘贴文献列表或摘要

### Phase 2: 文献搜索

根据学科选择数据库：

| 学科 | 优先数据库 | 补充数据库 |
|------|-----------|-----------|
| CS/AI/数学/物理 | arXiv | Semantic Scholar |
| 生物/医学 | PubMed | Semantic Scholar |
| 社科/人文 | Semantic Scholar | PubMed |
| 跨学科 | Semantic Scholar | arXiv + PubMed |

**搜索策略：**
1. 用 2-3 组不同关键词搜索，每组 10 篇
2. 对高引用论文用 fetch_paper.mjs 获取详情和参考文献
3. 从参考文献中发现更多相关论文（滚雪球法）
4. 将文献分为 5 类：背景、前沿、缺口、方法、相关工作

**文献数量目标：收集 30-50 篇，最终引用 ≥ 25 篇**

> 注意：AI 生成的引用信息可能不完全准确。在 proposal 末尾提醒用户核实所有参考文献的准确性。

### Phase 3: 生成大纲

按学科生成结构化大纲，参考 `references/STRUCTURE_GUIDE.md`。

**标准结构：**
```
Abstract (150-300 词, 5-10%)
1. Introduction (500-800 词, 15-20%)
   1.1 Background  |  1.2 Problem  |  1.3 Objectives  |  1.4 Scope
2. Literature Review (500-1000 词, 20-25%)
   2.1 Theoretical Framework  |  2.2 Current State  |  2.3 Gap  |  2.4 Positioning
3. Methodology (500-800 词, 20-25%)
   3.1 Design  |  3.2 Data Collection  |  3.3 Analysis  |  3.4 Limitations
4. Timeline (200-300 词, 5-10%)
5. Significance (200-400 词, 10-15%)
References (≥ 25 篇)
```

**必须等用户确认大纲后才能进入 Phase 4。**

### Phase 4: 撰写正文

**写作风格（关键）：**
- 学术散文体，不要用大量列表和要点
- 段落 4-8 句，有主题句 → 证据 → 分析 → 过渡
- 使用学术谦逊语言（may, might, suggests, indicates）
- 引用融入正文：(Author et al., Year)
- 包含 3-5 个图表建议（用 blockquote 格式）
- 参考 `references/WRITING_STYLE_GUIDE.md` 和 `references/DOMAIN_TEMPLATES.md`

**中文写作要点：**
- 使用"本研究旨在…"而非"我认为…"
- 使用"有望表明"而非"肯定会证明"
- 参考文献格式遵循 GB/T 7714

**英文写作要点：**
- 保持 British/American English 一致性
- 使用 hedging language
- APA/MLA/Chicago 格式根据学科选择

### Phase 5: 输出与检查

1. 生成 Markdown 文件：`proposal_{topic}_{YYYY-MM-DD}.md`
2. 用 `references/QUALITY_CHECKLIST.md` 自查
3. 提供格式转换命令：`pandoc proposal.md -o proposal.docx`（不要加 -N 参数）
4. **提醒用户核实参考文献的准确性**

---

## 参考文件

| 文件 | 用途 |
|------|------|
| `references/STRUCTURE_GUIDE.md` | 各章节详细写作指南 |
| `references/DOMAIN_TEMPLATES.md` | STEM vs 人文 vs 社科差异 |
| `references/WRITING_STYLE_GUIDE.md` | Nature Reviews 学术写作风格 |
| `references/QUALITY_CHECKLIST.md` | 质量检查清单 |
| `assets/proposal_scaffold_en.md` | 英文模板 |
| `assets/proposal_scaffold_zh.md` | 中文模板 |

---

## 故障处理

| 问题 | 解决 |
|------|------|
| 搜索无结果 | 换关键词、换数据库、扩大搜索范围 |
| API 限速 (429) | 等待 30 秒后重试 |
| 用户提供了自己的文献 | 直接使用，用 fetch_paper.mjs 补充详情 |
| 题目太宽泛 | 引导用户缩小范围 |
