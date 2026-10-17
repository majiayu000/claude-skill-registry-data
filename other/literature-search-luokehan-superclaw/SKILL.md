---
name: scite-literature-search
description: 双路学术文献搜索技能 — Scite MCP（主路，Smart Citations + 全文搜索）+ Grok 4.20（辅路，推理式网络搜索）。用于学术调研、文献综述、论文查找、引用验证等场景。当用户要求搜索论文、文献、学术研究时，必须优先使用此技能。
keywords:
  - 论文
  - 文献
  - 学术
  - paper
  - literature
  - research
  - citation
  - scite
  - 搜索论文
  - 文献综述
---

# 学术文献搜索（双路并进）

当用户需要搜索学术文献、论文、引用、科学研究时，使用此双路策略。

## 架构

| 路线 | 工具 | 优势 | 适用场景 |
|------|------|------|----------|
| **主路** | Scite MCP (`mcporter call scite.search_literature`) | 1.4B+ 引用数据库，Smart Citations，全文搜索，引用验证 | 精确文献检索、引用分析、事实核查 |
| **辅路** | Grok 4.20 推理搜索 (`web_search`) | 实时网络搜索，推理能力强，覆盖预印本和最新发表 | 最新研究、预印本、综合分析 |

## 执行流程

### 步骤 1：双路并发搜索

同时发起两路搜索：

**主路 — Scite MCP：**
```bash
mcporter call scite.search_literature \
  --args '{"term": "搜索关键词", "limit": 10}'
```

Scite 搜索参数：
- `term`: 搜索词（支持布尔语法：AND, OR, NOT）
- `limit`: 返回数量（默认 10）
- `dois`: 指定 DOI 列表直接查询
- `sort`: 排序方式（relevance, date, citations）

**辅路 — Grok 推理搜索：**
使用 `web_search` 工具搜索相同主题，侧重：
- arXiv 预印本
- Google Scholar 结果
- 最近 1-2 年的最新发表
- 会议论文（NeurIPS, ICML, ACL 等）

### 步骤 2：结果合并与去重

1. 以 DOI 为主键合并两路结果
2. 优先采用 Scite 的 Smart Citation 数据（支持/对比/提及计数）
3. 补充 Grok 搜索中 Scite 未覆盖的预印本和最新论文

### 步骤 3：结果呈现

每篇论文展示：
- **标题** + DOI 链接
- **作者** + 发表年份 + 期刊/会议
- **Smart Citation 摘要**（如有）：X 篇支持 / Y 篇对比 / Z 篇提及
- **关键发现** 1-2 句
- **全文可达性**：OA / 机构访问 / 付费

### 步骤 4：引用验证

对关键论文使用 Scite 验证：
```bash
mcporter call scite.search_literature \
  --args '{"dois": ["10.xxxx/xxxxx"], "term": "specific claim"}'
```
检查该论文的引用是否被后续研究支持或反驳。

## 注意事项

- Scite 需要 Premium 订阅认证（Bearer token），如果调用返回认证错误，回退到纯 Grok 搜索
- 使用 APA 格式引用
- 始终提供参考文献列表
- 引用 Smart Citation 原文片段作为证据
- 检查撤稿和勘误通知
- 对于中文用户，搜索时使用英文关键词，结果用中文呈现
