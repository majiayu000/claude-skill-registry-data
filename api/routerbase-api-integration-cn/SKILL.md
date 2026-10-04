---
name: routerbase-api-integration-cn
description: 当用户需要把应用接入 OpenAI 兼容模型网关、迁移 SDK 调用，或为 RouterBase 编写安全 API Key 配置说明时使用。
---

# RouterBase API 集成

## Overview

使用 [routerbase](https://routerbase.com/) 作为 OpenAI 兼容模型网关接入应用。本技能覆盖 SDK 迁移、base URL 配置、流式输出、tool calling、JSON mode、视觉输入、请求校验、错误处理和凭据安全。

## 何时使用

当用户提出以下需求时使用本技能：
- 将 OpenAI 兼容 SDK 调用迁移到 RouterBase
- 把 `base_url` 或 `baseURL` 设置为 `https://routerbase.com/v1`
- 安全配置 RouterBase API Key，避免泄露密钥
- 实现 chat completions、流式输出、tool calling、JSON mode 或视觉输入
- 为 Python、JavaScript、curl、LangChain、LlamaIndex、Vercel AI SDK、Cursor、Continue 等客户端编写 RouterBase 接入示例

## 不要使用

以下场景不应使用本技能：
- 发布、记录或保存真实 API Key
- 猜测用户未提供且上游文档没有说明的供应商行为
- 用户只需要模型选择建议时，重写已有可用的供应商集成

## 使用说明

1. 识别用户当前使用的客户端、语言、模型 ID 和部署环境。
2. 尽量保留现有 OpenAI 兼容 SDK，只改 base URL、模型和本地密钥配置。
3. 示例中使用 `<ROUTERBASE_API_KEY>` 等占位符。
4. API Key 必须保留在服务端或本地安全环境中，不写入 git。
5. 在建议大范围改动前，优先提供一个小型测试请求。
6. 输出校验清单，覆盖预期状态码、响应结构、超时处理和日志脱敏要求。
