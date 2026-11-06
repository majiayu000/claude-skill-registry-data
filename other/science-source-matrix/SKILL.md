---
name: science-source-matrix
description: Use when choosing which retrieval source to query, when a search returns suspiciously few results, when OpenAlex budget runs low, or when a source is rate-limited or blocked; covers per-source capability, quotas, fallback order, and how to tell "source broke" from "query too narrow".
---

# 检索源矩阵：谁查什么、什么时候换源

## 开局先做两件事
1. `science_source_status` —— 看谁在冷却、OpenAlex 还剩多少美元预算；
2. `science_lit_query` —— 本地库有没有现成的。**同一课题不要重复烧配额**。

## 源的能力分工

| 源 | 强在哪 | 弱在哪 | 用法 |
|---|---|---|---|
| **OpenAlex** | 覆盖面最广，带引用数、OA 位置、摘要倒排索引 | **有美元预算**（无 key $0.10/天） | 首选，但一次查询别超 25 条 |
| **Crossref** | DOI 权威、元数据最规范、出版信息全 | 无摘要（部分有）、检索是相关性排序非布尔 | 补 DOI 与卷期页；查不到某篇的准确出版信息时用它 |
| **Europe PMC** | 生物医学全覆盖，**直接给 OA 全文链接** | 非生物医学覆盖弱 | 医学/生物方向第一顺位；M1.1 全文链的第 4–5 级靠它 |
| **PubMed** | 临床与生物医学索引最严（MeSH） | 两步请求、无 OA 链接 | 系统综述的纳排标准靠它；配合 Europe PMC 拿全文 |
| **arXiv** | 预印本最快、PDF 直链可下 | 无同行评议、无引用数 | 追最新工作、抢 scoop 检查 |
| **DOAJ** | 只收 OA 期刊 → 质量过滤好 | 覆盖窄 | 找可合法全文的期刊版本 |
| **DataCite** | 数据集 DOI | 文章少 | 查"数据能不能拿到" |
| **Zenodo** | 作者自存版、软件、预印本 | 突发就 403 | 找作者自存 PDF 的最后一站 |
| **OpenAIRE** | 欧洲项目产出、软性成果 | 字段结构深、响应大 | 补 Crossref 漏掉的报告/数据集 |

## 换源顺序（预算或限流时）

```
openalex（有钱时）→ crossref → europepmc → pubmed → openaire → arxiv/doaj/datacite/zenodo
```

OpenAlex 预算见底（`science_source_status` 显示剩余 < $0.01）时：
1. 本轮只用 `crossref,europepmc,pubmed`（三者都无预算模型）；
2. 需要引用数就等重置（响应头 `resetInMs`）或用 `science_openalex_key` 申一个 key（$1/天）。

## 结果太少时，先分清是谁的问题

跑 `science_retrieval_doctor`：

- **探针就失败** → 源坏了或被封，换源，别改检索式。
- **探针 ok 但命中 0** → 检索式问题。按这个顺序放宽：
  1. 砍概念块（3 块 → 2 块）；
  2. 加同义词（`|` 分隔）；
  3. 去 `yearFrom`（很多源按年份硬过滤）；
  4. 去 `oaOnly`；
  5. 换语言（中文课题用英文概念再查一遍，反向也试）。
- **只有 1–2 个源有命中** → 概念太偏或拼写问题；用 Crossref 先确认这个领域到底怎么措辞。

## 硬规矩

- **一个概念块内不要放 4 个以上同义词**：绝大多数源的布尔上限会截断。
- **不要把整句摘要当检索式**：超过 8 个词后相关性排序会退化成噪声。
- 检索完必须落库（`science_search` 默认落库），并在汇报里写清：**源清单 + 时间窗 + 命中数 + 纳排标准**。这三样缺一样，这次检索就不可复现。
- 中文课题：`science_search` 的英文源先跑，再用中文库补；不要指望单个源跨语言。
