---
name: llm-factory-design
description: LLM 中枢服务层设计规范。修改 services/llm/ 目录下任何文件时必须加载。涉及 LLM Provider 适配、工厂模式、API 调用方式变更时触发。
version: 1.0
---

**STOP AND READ THIS FIRST.**

你是本项目的核心开发 Agent。本目录下的所有 Markdown 文件构成了 `llm-factory-design` 的强制性技术规范（Technical Specification）。

在进行任何 LLM 服务相关代码编写、适配器修改或接口变更之前，你**必须**严格遵循以下路由规则，使用你的文件读取能力查阅对应的细节文档。

---

## 1. 模块需求概述

本模块的核心目标是在 `services/llm/` 目录下构建一个**高内聚、低耦合**的大模型调用中枢。

系统目前需要接入 OpenAI（或兼容其 SDK 格式的厂商，如 DeepSeek、阿里百炼等）以及 Anthropic (Claude)。由于各家大模型的官方 SDK 在参数结构、系统提示词传入方式、异步调用方法上存在巨大差异，本模块必须抹平这些底层差异，为上层业务逻辑提供一套标准、统一、类型安全的 Python 调用接口。

---

## 2. 编码前置依赖路由表

> **[ACTION REQUIRED]** 当我要求你开发或修改特定模块时，你必须先读取以下对应的文件。

### 模块 A：架构与设计哲学

如果你需要理解**整体架构思路、设计原则、代码目录结构**：

- [ ] **必须读取**: `architecture/design-philosophy.md` (依赖倒置原则、工厂模式、强制异步、代码目录拓扑)

### 模块 B：接口契约

如果你需要实现或修改**LLM 接口定义、新增方法**：

- [ ] **必须读取**: `interfaces/base-contract.md` (所有接口定义：chat、embedding、intent、token、stream)

### 模块 C：适配器实现

如果你需要实现或修改**特定 Provider 的适配器、工厂逻辑**：

- [ ] **必须读取**: `adapters/implementation.md` (OpenAI/Claude 适配器实现规范、工厂模式、依赖注入)

---

## 3. 严格的开发约束

1. **依赖倒置**：上层业务代码绝对不允许直接 `import openai` 或 `import anthropic`，只依赖于抽象基类。
2. **强制异步**：所有对外方法必须使用 `async/await`。
3. **结构化输出**：必须使用 JSON Mode 或 function calling 确保模型输出标准 JSON。
4. **统一工厂**：通过 `LLMFactory.get_provider()` 获取实例，禁止手动实例化 Provider。
