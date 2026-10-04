---
name: rag
description: 通用 RAG 方法论 Skill 集合（9 模块，跨项目可迁移）：加载 / 摄取 / 查询理解 / 检索 / 重排 / 生成防幻觉 / 多轮对话 / GraphRAG / 评估。每篇「通用原则 + 落地建议」。
license: MIT
metadata:
  author: Sectrend (experience distilled from iKnow paper, Huawei Cloud)
  tags: [rag, retrieval, vector-db, llm, typescript, methodology]
  based_on: "iKnow: an Intent-Guided Chatbot for Cloud Operations with RAG (ASE 2025, Huawei Cloud; PDF: https://jun-jie-huang.github.io/assets/papers/ase25_iknow.pdf)"
---

# RAG（检索增强生成）

> **通用 RAG 方法论 Skill 集合**（跨项目可迁移，与具体项目解耦）。每篇为「通用原则（适用于任何 RAG 项目）+ 落地建议（项目无关的参考命名 / 结构 / 参数）」。项目专属绑定由所在项目侧 `.agents/rules/rag-*.md` 提供（不在本 skill 内），本 skill 保持项目无关。论文依据：华为云 + 港中文的 iKnow 经验论文（ASE 2025，PDF 见 references）——对 2000 条真实云运维查询的实证发现 **过半 RAG 失败源于查询侧**（不完整 32% / 超范围 10% / 无效 9%），**知识缺失 27%** 是第二大根因并直接诱发幻觉。故标准 RAG 上应增加「查询理解与改写」「缺失知识检测」两层。

## 通用 RAG 生命周期（不依赖任何项目）

```
加载 loader → 摄取/分块 ingestion → 查询理解 query → 检索 retrieval → 重排 rerank → 生成 generation → 评估 evaluation
 (rag-loader)   (rag-ingestion)   (rag-query)   (rag-retrieval)  (rag-rerank)   (rag-generation)  (rag-evaluation)
        ↑ 多轮对话 rag-multi-turn（横切：每轮先做历史改写再进查询理解）
        ↑ GraphRAG rag-graphrag（进阶：跨文档/全局性问题时替代 chunk 级检索）
```

各环节投入优先级不同（论文实测）：**查询理解与评估**是性价比最高、最易被忽略的两环——前者修复 32% 的查询侧失败，后者让所有改进可验证；重排/GraphRAG/多轮属**按需启用**的进阶能力。

## 模块导航（遇到什么问题 → 读哪篇）

| 遇到的问题 | 模块 | 篇目 |
| --- | --- | --- |
| 加载多格式文档（PDF/HTML/Office/图片） | rag-loader | `references/rag-loader.md` |
| 分块 / 去重 / 批量嵌入 / 入库 | rag-ingestion | `references/rag-ingestion.md` |
| 检索前把模糊问题改写为语义完整问题 | rag-query | `references/rag-query.md` |
| 混合检索（dense + keyword + RRF 融合） | rag-retrieval | `references/rag-retrieval.md` |
| 检索后精排（候选集大 / 专有名词多时） | rag-rerank | `references/rag-rerank.md` |
| 防幻觉生成 + 溯源（prompt / 生成链路） | rag-generation | `references/rag-generation.md` |
| 多轮对话（追问改写 / 历史压缩） | rag-multi-turn | `references/rag-multi-turn.md` |
| 跨文档 / 全局性问题（图谱聚合） | rag-graphrag | `references/rag-graphrag.md` |
| 验收 / 回归 / 评估指标 | rag-evaluation | `references/rag-evaluation.md` |
| 想了解论文原始数据 / 结论细节 | 论文笔记 | `references/iknow-paper-notes.md` |

## 论文经验 → 通用对策（为什么这么设计）

| 论文发现（iKnow，2000 条真实查询） | 占比 | 通用对策 |
| --- | --- | --- |
| 查询不完整（如只输入一个名词） | 32% | **检索前查询改写**：LLM 按意图把模糊问题改写为语义完整的问题（rag-query） |
| 知识缺失（知识库无对应内容 → 幻觉） | 27% | **缺失知识检测 + 降级回答**：判断上下文是否足够，不足则明示"暂无相关信息"（rag-generation） |
| 查询意图与失败强相关（术语解释类 58.8% 败于不完整） | — | **意图分类**：5 类意图，改写 prompt 按意图定制（rag-query） |
| 检索不准确（相关文档不在 top-k） | 11% | **双通道混合检索 + RRF 融合**：dense + keyword 互补（rag-retrieval） |
| 生成不准确 | 11% | 注入"原始问题 + 改写问题 + 上下文"三段 prompt，约束仅依据给定上下文回答（rag-generation） |
| 超范围 / 无效查询 | 19% | 意图分类识别无效 / 越界问题，路由到降级回答（rag-query） |