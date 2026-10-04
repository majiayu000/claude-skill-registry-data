---
name: searchcans-rag-source-curator-zh
description: 使用 SearchCans 的地域化 Google 或 Bing 搜索、Reader 提取、文件提取和可选页面截图创建小规模、多样、可作为证据的 RAG 来源清单。适用于 grounding pack、来源策展、知识库入库和预入库证据检查。
metadata:
  author: SearchCans
  version: 1.1.0
  tags: [rag, reader-api, file-extraction-api, screenshot-api, chinese]
---

# SearchCans RAG 来源策展

建立经过严格限制的来源清单，而不是抓取整个网络。该 Skill 搜索 Google 或 Bing，选择域名尽量多样的候选来源，只用 Reader 读取选定页面，接受明确指定的 PDF/Office 文件 URL，并可为视觉审查保留截图 URL。

## 创建来源集合

从具体问题、市场、来源预算，以及该来源包被视为可用前所需的最少成功提取来源数开始。仅通过 `--file-url` 添加直接文件；不得从页面推断文件 URL。

```bash
python scripts/rag_source_curator.py "当前 SERP API 市场是什么样？" \
  --engine google --country us --language zh \
  --source-budget 4 --min-claim-ready 2 --include-content \
  --out rag-sources.json
```

使用 `--query` 建立小型查询矩阵。只有确实需要视觉审查时才使用 `--screenshot 1` 或 `2`。`--include-content` 会刻意增加输出体积；若只需元数据清单留待第二次读取，省略它。

## 执行证据质量门槛

只有 Reader/File Extraction 返回内容时，输出才将来源标为 `claim_ready`。仅当达到所请求最小数量时，`evidence_gate.status` 才为 `passed`。

不得把 SERP 摘要、未读取 URL、空响应或截图作为重要回答的充分证据。每个来源初始都为 `authority_assessment: unassessed`；权威性、时效性、权限和组织专属信任标签应由独立的人或策略审查指定。

决定输出能否写入 RAG 索引前，先阅读 [来源清单指南](references/source-manifest.md)。

## 控制成本与并发

默认 `--account-mode auto` 使用一次安全 Account API 预检，估算搜索和整个 Reader/File 来源预算，在可能时收缩来源数，并将 worker 限制为报告的 Parallel Lane。使用 `enforce` 在预算不足时停止，`warn` 记录但不收缩，只有在不适合账户检查时才使用 `off`。

从代理档位 0 开始。仅在确认访问问题时提升代理档位，因为这会改变 Reader 积分成本。来源清单不含账户身份或凭据。

## 官网

[SearchCans 官网](https://www.searchcans.com/)

## 资源

- `scripts/rag_source_curator.py`：生成搜索、选择、提取和质量门槛包。
- `references/source-manifest.md`：说明索引或回答前的必要审查。
