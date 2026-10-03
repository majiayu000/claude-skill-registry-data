---
name: retrieval-pipeline
description: 记忆检索设计。修改检索逻辑、相似度计算时必须加载。涉及 LLM 分类判断、向量检索、分类内检索、检索分数计算、上下文构建时触发。
version: 1.0
---

**STOP AND READ THIS FIRST.**

你是本项目的核心开发 Agent。本目录下的所有 Markdown 文件构成了 `retrieval-pipeline` 的强制性技术规范（Technical Specification）。

在进行任何检索相关代码编写、重构或 Bug 修复之前，你**必须**严格遵循以下路由规则，使用你的文件读取能力查阅对应的细节文档。

---

## 1. 检索流程概览

采用 **LLM 驱动的双层检索** 架构：

```
用户查询
    │
    ▼
┌─────────────────────────────────────────┐
│ 1. LLM 分类判断                          │
│    "这个问题属于哪些类别？"               │
│    → 动态输出 1-N 个相关类别             │
│    → 例如：[项目研发] 或 [核心自我, 考试与升学] │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ 2. Category 层向量检索（第一层）          │
│    在 LLM 指定的类别中检索 Category 表    │
│    按 content_vector 相似度 + importance 排序 │
│    → 返回 Top-K 原子化记忆               │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ 3. LLM 充足性判断                        │
│    "这些记忆足够回答问题吗？"             │
│    → 足够：直接构建上下文回答             │
│    → 不足：进入 Resource 层检索           │
└─────────────────────────────────────────┘
    │ (不足时)
    ▼
┌─────────────────────────────────────────┐
│ 4. Resource 层向量检索（第二层）          │
│    根据已检索 Category 关联的 Resource   │
│    按 description_vector 相似度 + importance 排序 │
│    → 返回 Top-K 对话摘要                 │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ 5. 结果合并与上下文构建                  │
│    合并 Category + Resource 检索结果     │
│    作为 system prompt 上下文供 LLM 回答   │
└─────────────────────────────────────────┘
```

---

## 2. 编码前置依赖路由表

> **[ACTION REQUIRED]** 当我要求你开发或修改特定模块时，你必须先读取以下对应的文件。

### 模块 A：LLM 分类判断

如果你需要实现或修改**分类判断 Prompt、返回格式**相关的代码：

- [ ] **必须读取**: `workflow/category-classification.md` (分类判断 Prompt + 返回示例)

### 模块 B：Category 层向量检索

如果你需要实现或修改**Category 表向量检索、SQL 查询**相关的代码：

- [ ] **必须读取**: `workflow/category-search.md` (Category 层 SQL 实现 + 排序权重)

### 模块 C：LLM 充足性判断

如果你需要实现或修改**判断检索结果是否足够回答问题**相关的代码：

- [ ] **必须读取**: `workflow/sufficiency-check.md` (充足性判断 Prompt + 判断逻辑)

### 模块 D：Resource 层向量检索

如果你需要实现或修改**Resource 表向量检索、关联查询**相关的代码：

- [ ] **必须读取**: `workflow/resource-search.md` (Resource 层 SQL 实现 + 关联逻辑)

### 模块 E：上下文构建

如果你需要实现或修改**检索结果拼接、System Prompt 构建**相关的代码：

- [ ] **必须读取**: `workflow/context-building.md` (上下文构建逻辑 + System Prompt 示例)

### 模块 F：分数计算与阈值

如果你需要实现或修改**检索分数公式、相似度阈值**相关的代码：

- [ ] **必须读取**: `config/scoring.md` (综合检索分数公式 + 向量相似度阈值 + 重要性过滤)

### 模块 G：性能优化

如果你需要实现或修改**缓存策略、预过滤**相关的代码：

- [ ] **必须读取**: `optimization/caching.md` (缓存策略 + 预过滤)

### 模块 H：检索 API

如果你需要实现或修改**检索接口路由、响应格式**相关的代码：

- [ ] **必须读取**: `api/endpoints.md` (POST /v1/retrieve 定义)

---

## 3. 严格的开发约束

1. **双层检索顺序**：必须先检索 Category 层，再根据充足性判断决定是否检索 Resource 层。
2. **category_name 位置**：`category_name` 字段在 `categories` 表，不在 `resources` 表。
3. **向量字段位置**：
   - Category 表：`content_vector` (原子化记忆内容的向量)
   - Resource 表：`description_vector` (对话摘要的向量)
4. **可配置四因子乘法评分**：详见 `config/scoring.md`，默认 `similarity_power=1.5`。
5. **阈值过滤**：当前实现以综合分数阈值过滤为主，默认 `FOUR_FACTOR_THRESHOLD_LOW=0.03`；`importance_score` 使用 0-3 分制，检索默认不因低重要性提前丢弃语义相关结果。

---

## 4. 与其他 Skills 的关系

| 本文档位置 | 相关 Skill | 说明 |
|------------|------------|------|
| 上下文构建 | input-pipeline | user_prompt_template 加载机制 |
| 分类判断 | service-design | MemoryRetriever 实现 |
| 向量存储 | database-schema | Vector(1536) 字段 |
| LLM 调用 | llm-factory-design | generate_chat_response |

---

## 5. 实现优先级

| 优先级 | 功能 | 理由 |
|--------|------|------|
| P0 | LLM 分类判断 | 决定检索范围 |
| P0 | Category 层向量检索 | 第一层检索核心能力 |
| P0 | LLM 充足性判断 | 决定是否需要第二层检索 |
| P1 | Resource 层向量检索 | 第二层兜底检索 |
| P1 | 检索分数计算 | 必要的排序逻辑 |
| P1 | 上下文构建 | 连接检索与回答 |
| P2 | 缓存优化 | 性能提升 |
