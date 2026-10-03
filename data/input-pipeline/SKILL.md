---
name: input-pipeline
description: Chat 对话保存流程设计。修改 API 路由、对话流程、用户识别逻辑时必须加载。涉及 chat API、多轮对话缓存、后端初始化处理时触发。
version: 1.0
---

**STOP AND READ THIS FIRST.**

你是本项目的核心开发 Agent。本目录下的所有 Markdown 文件构成了 `input-pipeline` 的强制性技术规范（Technical Specification）。

在进行任何代码编写、重构或 Bug 修复之前，你**必须**严格遵循以下路由规则，使用你的文件读取能力查阅对应的细节文档。**严禁凭空发明接口或脱离规范实现逻辑！**

---

## 1. 架构总览 (Architecture Overview)

核心数据流：

```
请求进入 → 身份校验 → 模态路由 → LLM 处理 → 记忆去重与缓存 → 持久化落库
```

---

## 2. 编码前置依赖路由表 (Pre-coding Reading Requirements)

> **[ACTION REQUIRED]** 当我要求你开发或修改特定模块时，你必须先读取以下对应的文件，确保你的代码与设计文档 100% 对齐。

### 模块 A：用户注册与初始化 (Onboarding)

如果你需要实现或修改**用户首次进入、画像提取、或分类初始化**相关的代码：

- [ ] **必须读取**: `workflow/identity-initialization.md` (严格按照此文件生成 user_prompt 和动态分类)
- [ ] **必须读取**: `config/categories.md` (确保代码中只包含这里定义的 4 个固定分类和 2 个动态分类)
- [ ] **必须读取**: `api/endpoints.md` (确保 Controller 层的路由和 JSON 响应格式与文档一致)

### 模块 B：对话路由与多模态 (Chat & Modality)

如果你需要实现**接收用户消息、判断消息类型**相关的代码：

- [ ] **必须读取**: `workflow/user-identification.md` (实现无 Token 时的拦截与引导逻辑)
- [ ] **必须读取**: `config/modality-rules.md` (根据不同 modality 应用不同的策略)

### 模块 C：记忆缓存与落库控制 (Caching & Persistence)

如果你需要实现**对话回合计数、Redis 缓存、或触发数据库 Save** 相关的代码：

- [ ] **必须读取**: `workflow/chat-caching.md` (严格实现 "chat 模态满 5 轮才落库" 的逻辑，以及异常落库保护)

### 模块 D：记忆检索、去重与衰减 (Core Memory Engine)

如果你需要实现**向量库写入、相似度对比、或定时清理记忆**相关的代码：

- [ ] **必须读取**: `workflow/memory-deduplication.md` (必须实现代码逻辑处理 0.90 和 0.75-0.90 这几个关键阈值，并正确实现 Append/Update/Insert 分支)
- [ ] **必须读取**: `workflow/forgetting-mechanism.md` (实现时间衰减判断逻辑)

---

## 3. 严格的开发约束 (Strict Constraints)

1. **API 契约神圣不可侵犯**：`api/endpoints.md` 中定义的字段名、类型和层级结构，在代码中必须一字不差地实现。
2. **拒绝幻觉**：如果规范中没有定义某个字段或逻辑，请在命令行中向我（人类开发者）提问，**不要自行脑补**。
3. **保持模块化**：请对照上述的业务模块，在后端的代码目录（如 Controller, Service, Repository 层）保持相应的解耦。

---

## 4. 外部系统对接

如果你在编写代码时需要用到数据库表名或前端表单字段，请跨目录查阅：

- **数据库表结构**：查阅 `database-schema` skill 目录
- **前端交互细节**：查阅 `frontend-design` skill 目录
- **检索逻辑、Rerank**：查阅 `retrieval-pipeline` skill 目录
- **重要性评分**：查阅原需求文档 `IMPORTANCE_SCORING.md`
