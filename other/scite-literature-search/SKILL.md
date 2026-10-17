---
name: scite-literature-search
description: 整合 Scite MCP 与 Web Search 的双路学术搜索模式，实现深度引用分析与实时进展追踪。
version: 1.0
evolution_type: CAPTURED
---

# scite-literature-search

## 适用场景
- 进行高可信度的学术调研或文献综述。
- 验证特定科学断言（Scientific Claims）的证据支持情况。
- 追踪某一研究领域的最新进展（弥补学术数据库索引延迟）。
- 识别某一领域的核心论文及其被引用语境（支持、反对或提及）。

## 步骤
1. **定义核心查询**：将研究问题拆解为关键词组合，并确定是否需要针对特定断言进行验证。
2. **执行 Scite 深度搜索**：
   - 使用 `scite_search` 工具。
   - 重点关注 `citing_paper_count` 和 `tallies`（supporting, contrasting, mentioning）。
   - 提取核心论文的 DOI 和摘要。
3. **执行 Web Search 实时补位**：
   - 使用 `web_search` 搜索过去 12-24 个月内的最新论文、Preprints（如 arXiv, bioRxiv）或顶级会议（如 NeurIPS, ICML）的最新录用名单。
   - 搜索关键词应包含 "2023..2024" 或 "latest" 等时间限定词。
4. **交叉验证与合成**：
   - 对比 Scite 中的经典文献与 Web Search 中的最新趋势。
   - 检查最新进展是否对旧有结论提出了挑战或补充。
5. **输出综述**：标注引用来源，区分“经过同行评审的结论”与“最新预印本观点”。

## 工具和命令
- **Scite 搜索**：
  `scite_search(query="your academic query", limit=10)`
- **Web 搜索**：
  `web_search(query="site:arxiv.org OR site:researchgate.net 'your query' 2024")`
- **引用分析**：
  查看 Scite 返回的 `tallies` 对象，识别争议性研究（contrasting 计数较高的论文）。

## 注意事项
- **引用偏见**：高引用量不代表绝对正确，务必检查 `contrasting` 引用。
- **时间差**：Scite 的索引可能存在数月的延迟，必须配合 Web Search 捕获当月发布的成果。
- **关键词优化**：学术搜索应优先使用术语而非自然语言提问。
- **DOI 优先**：在进一步追踪特定论文时，优先使用 DOI 进行精确匹配。

## 示例
**场景**：调研“大语言模型在代码生成中的幻觉问题”。

1. **Scite 步骤**：
   `scite_search(query="LLM code generation hallucination", limit=5)`
   *发现 2022-2023 年的基础研究，确认其被引用语境多为支持。*

2. **Web Search 步骤**：
   `web_search(query="LLM code hallucination detection benchmarks 2024")`
   *发现上个月刚发布的最新 Benchmark 论文。*

3. **结果整合**：
   “根据 Scite 的引用分析，早期研究（如 [Author, 2023]）确立了幻觉分类学（支持引用 20+）；而最新的 Web 搜索显示，2024 年 5 月的研究已开始转向动态检测技术...”