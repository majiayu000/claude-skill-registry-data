---
name: service-design
description: Service 层架构设计规范。修改 services/ 目录（非 llm 子目录）时必须加载。涉及 Memory、Session、Retrieval、OSS 模块变更时触发。
version: 1.0
---

# SYSTEM DIRECTIVE FOR CLAUDE CODE

**STOP AND READ THIS FIRST.**

你是本项目的核心开发 Agent。本目录下的所有 Markdown 文件构成了 `service-design` 的强制性技术规范（Technical Specification）。

在进行任何 Service 层相关代码编写、模块修改或接口变更之前，你**必须**严格遵循以下路由规则，使用你的文件读取能力查阅对应的细节文档。

---

## 1. 模块需求概述

本模块的核心目标是在 `services/` 目录下构建**高内聚、低耦合**的业务服务层。

Service 层是所有业务逻辑的唯一所在地，负责协调 LLM 调用、数据库操作、缓存管理等底层能力，为上层 API 提供统一的服务接口。

---

## 2. 编码前置依赖路由表

> **[ACTION REQUIRED]** 当我要求你开发或修改特定模块时，你必须先读取以下对应的文件。

### 模块 A：整体目录结构

如果你需要理解**Service 层的代码组织方式**：

- [ ] **必须读取**: `architecture/directory-structure.md` (services/ 目录拓扑)

### 模块 B：Memory 服务

如果你需要实现或修改**记忆写入、Handler 处理器**相关的代码：

- [ ] **必须读取**: `modules/memory.md` (MemoryWriter、异步写入工作流、Handler 基类)

### 模块 C：Session 服务

如果你需要实现或修改**会话管理、用户识别**相关的代码：

- [ ] **必须读取**: `modules/session.md` (SessionState、SessionManager、UserIdentifier)

### 模块 D：Retrieval 服务

如果你需要实现或修改**记忆检索、上下文构建**相关的代码：

- [ ] **必须读取**: `modules/retrieval.md` (MemoryRetriever、动态类别判断)

### 模块 E：OSS 服务

如果你需要实现或修改**对象存储、文件上传**相关的代码：

- [ ] **必须读取**: `modules/oss.md` (BaseOSSClient、存储路径命名规范)

### 模块 F：监控与度量

如果你需要实现或修改**埋点、指标采集**相关的代码：

- [ ] **必须读取**: `observability/metrics.md` (核心指标、埋点位置)

---

## 3. 严格的开发约束

1. **Service 层唯一职责**：所有业务逻辑必须在 Service 层实现，API 层只负责路由和校验。
2. **异步优先**：所有 I/O 操作必须使用 `async/await`。
3. **依赖注入**：通过 FastAPI 的 `Depends()` 获取 Session 和 Repository 实例。
4. **跨模块引用**：Service 层可调用其他 Service 或 Repository，但禁止直接操作 ORM 模型。

---

## 4. LLM 模块说明

`services/llm/` 目录的设计详见 `llm-factory-design` skill。

**核心接口**：
- `generate_chat_response()` - 生成对话回复
- `get_embedding()` - 生成文本向量
- `extract_memory_intent()` - 提取记忆意图
