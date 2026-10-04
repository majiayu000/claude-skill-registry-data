---
name: model-fallback
description: 为 Hermes Agent 配置模型故障转移，自动切换到备用模型。类似于 FreeRide 的"速率限制自动切换"概念，但专为 Hermes Agent 设计。
version: 1.0.0
author: Hermes Agent Community
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: []
  api_keys: []
metadata:
  hermes:
    tags: [model, fallback, openrouter, free-ai, redundancy]
    homepage: https://github.com/openclaw/openclaw
---

# Model Fallback — 模型故障转移技能

本技能帮助你在 Hermes Agent 中配置模型故障转移，当主模型不可用时自动切换到备用模型。类似于 FreeRide"速率限制自动切换"的理念。

---

## 核心功能

1. **自动故障转移** — 主模型 Rate Limit / 503 / 529 时自动切换
2. **多提供商支持** — OpenRouter、OpenAI Codex、Nous 等
3. **免费模型优先** — 优先使用免费/低成本模型
4. **手动切换** — 可随时手动切换当前模型

---

## 工作原理

Hermes Agent 内置 `fallback_model` 配置，支持：

| 触发条件 | 行为 |
|---------|------|
| 429 Rate Limit | 自动切换到 fallback |
| 529 Service Overloaded | 自动切换到 fallback |
| 503 Service Unavailable | 自动切换到 fallback |
| 连接失败 | 自动切换到 fallback |

---

## 快速配置

### 方案一：OpenRouter 免费模型（推荐）

OpenRouter 提供多个免费模型，适合日常使用。

**1. 获取 OpenRouter API Key**
```bash
# 访问 https://openrouter.ai/keys 免费注册
# 生成 API Key
```

**2. 配置 fallback_model**

编辑 `~/.hermes/config.yaml`：

```yaml
fallback_model:
  provider: openrouter
  model: anthropic/claude-3.5-haiku  # 免费模型首选
  # 或使用其他免费模型：
  # - google/gemini-flash-1.5
  # - meta-llama/llama-3-8b-instruct
  # - mistralai/minitrue
```

**环境变量**（在 `~/.hermes/.env` 中添加）：
```bash
OPENROUTER_API_KEY=sk-or-v1-xxxxx
```

### 方案二：OpenAI Codex（免费额度）

如果你有 OpenAI 账号，Codex 有免费配额：

```yaml
fallback_model:
  provider: openai-codex
  model: gpt-4o-mini
```

需要通过 Hermes Auth 配置 OAuth：
```bash
hermes auth openai-codex login
```

### 方案三：Nous Portal（免费）

Nous 提供免费模型访问：

```yaml
fallback_model:
  provider: nous
  model: hermes-3-llama-3-8b
```

---

## 免费模型列表

| 模型 | 提供商 | 上下文 | 备注 |
|------|--------|--------|------|
| claude-3.5-haiku | OpenRouter | 200K | Anthropic 官方，免费额度 |
| gemini-flash-1.5 | OpenRouter | 1M | Google 官方，速度快 |
| llama-3-8b-instruct | OpenRouter | 8K | Meta 开源模型 |
| mistral-7b-instruct | OpenRouter | 32K | Mistral 开源 |
| hermes-3-llama-3-8b | Nous | 8K |Nous 自定义，免费 |

---

## 手动切换模型

### 查看当前状态
```bash
hermes model status
```

### 临时切换（当前会话）
```bash
hermes model switch openrouter:anthropic/claude-3.5-haiku
```

### 持久切换（修改默认模型）
编辑 `~/.hermes/config.yaml`：
```yaml
model:
  default: openrouter/anthropic/claude-3.5-haiku
  provider: openrouter
  base_url: https://openrouter.ai/v1
  api_key: env:OPENROUTER_API_KEY
```

---

## 监控与日志

### 查看模型切换历史
```bash
hermes logs --filter model-fallback
```

### 测试故障转移
```bash
hermes model test-fallback
```

---

## 故障排除

| 问题 | 解决方案 |
|------|---------|
| 切换后仍然失败 | 检查 API Key 是否有效 |
| 模型响应慢 | 切换到更快的模型如 gemini-flash-1.5 |
| 认证失败 | 重新运行 `hermes auth login` |
| 账单超标 | 限制每日使用量或使用纯免费模型 |

---

## 与 FreeRide 的区别

| 特性 | FreeRide | Model Fallback |
|------|----------|----------------|
| 目标平台 | OpenClaw | Hermes Agent |
| 切换机制 | 速率限制触发 | Rate Limit / 503 / 529 触发 |
| 配置方式 | 配置文件 | config.yaml fallback_model |
| 模型源 | OpenRouter | OpenRouter + 多提供商 |
| 自动排名 | 是 | 否（手动选择） |

---

## 下一步

1. 选择一个免费模型提供商（推荐 OpenRouter）
2. 获取 API Key
3. 配置 fallback_model
4. 测试切换功能

需要我帮你完成哪一步？