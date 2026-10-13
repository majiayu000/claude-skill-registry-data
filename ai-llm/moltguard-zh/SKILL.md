---
name: moltguard-zh
description: OpenClaw 原生安全插件——通过 MoltGuard API 检测工具结果与消息中的提示注入，可选本地净化网关在发送前脱敏 PII（银行卡/密码等），首次使用自动注册 API 密钥
tags: [security, protection, prompt-injection-detection]
permissions: [network]
metadata:
  clawdbot:
    requires:
      env: []
    files: []
  capabilities:
    allow:
      - network: ["api.moltguard.com"]
      - read: [workspace/**]
      - write: [workspace/**]
    deny:
      - execute: ["!*"]
  env_declarations:
    - name: MOLTTGUARD_API_KEY
      required: false
      description: "MoltGuard API 密钥（可选 — 留空则自动注册）"
---

# MoltGuard 安全防护

> OpenClaw 原生安全插件，检测和防止提示注入攻击

## 🛡️ 功能特性

- **提示注入检测** - 通过 MoltGuard API 分析工具结果和消息中的恶意提示注入
- **本地净化网关** - 可选的本地提示词净化，在发送到 LLM 前保护敏感数据
- **自动注册** - 首次使用时自动注册 API 密钥
- **灵活配置** - 支持超时、日志记录、拦截策略等高级配置

## 🚀 快速开始

### 基本配置

启用基本防护：

```json
{
  "enabled": true
}
```

### 启用本地净化网关

```json
{
  "enabled": true,
  "sanitizePrompt": true,
  "gatewayAutoStart": true
}
```

## ⚙️ 配置选项

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `enabled` | boolean | `true` | 启用或禁用防护 |
| `sanitizePrompt` | boolean | `false` | 启用本地提示词净化网关 |
| `gatewayPort` | number | `8900` | 本地净化网关端口 |
| `gatewayAutoStart` | boolean | `true` | 插件加载时自动启动网关 |
| `blockOnRisk` | boolean | `true` | 检测到注入时拦截工具调用 |
| `apiKey` | string | - | MoltGuard API 密钥（可选） |
| `timeoutMs` | number | `60000` | 分析超时时间（毫秒） |
| `autoRegister` | boolean | `true` | apiKey 为空时自动注册 API 密钥 |
| `apiBaseUrl` | string | `https://api.moltguard.com` | MoltGuard API 基础 URL |

## 🔍 工作原理

### 1. 检测模式

- **工具结果分析** - 扫描工具执行结果中的恶意注入内容
- **消息检测** - 检测输入消息中的提示注入攻击
- **风险评估** - 基于上下文评估风险级别

### 2. 净化模式（可选）

- **本地网关** - 在本地运行提示词净化服务
- **PII 脱敏** - 自动检测并脱敏敏感信息
- **隐私保护** - 确保敏感数据不会发送到 LLM

## 🛡️ 安全特性

### 防护机制

- **拦截策略** - 检测到风险时自动拦截工具调用
- **日志记录** - 详细的安全事件日志
- **实时监控** - 实时监控工具执行和消息内容

### 合规性

- **数据本地化** - 敏感数据本地处理，不上传外部服务
- **透明度** - 所有可能的拦截都会记录日志
- **可控性** - 用户可以随时调整安全级别

## 📊 使用建议

### 高安全性场景

```json
{
  "enabled": true,
  "sanitizePrompt": true,
  "blockOnRisk": true,
  "logPath": "~/.openclaw/logs/security"
}
```

### 严格环境（无网络）

```json
{
  "enabled": true,
  "sanitizePrompt": true,
  "autoRegister": false,
  "blockOnRisk": true
}
```

## 🔧 故障排除

### 常见问题

1. **API 密钥问题**
   - 确保网络连接正常
   - 检查 API 密钥是否正确
   - 查看日志文件了解详情

2. **网关启动失败**
   - 检查端口是否被占用
   - 确保 gatewayAutoStart 设置正确
   - 查看系统日志了解错误信息

3. **性能问题**
   - 调整 timeoutMs 参数
   - 启用日志记录查看性能瓶颈

## 📝 日志记录

所有安全事件都会记录到 JSONL 格式的日志文件中：

```bash
# 默认日志位置
~/.openclaw/logs/

# 查看日志
cat ~/.openclaw/logs/moltguard-*.jsonl | jq '.'
```

日志内容包括：
- 检测到的时间戳
- 风险级别
- 检测到的内容
- 处理结果
- 相关上下文

---

**注意**: MoltGuard 需要网络连接以进行 API 调用。在严格隔离的环境中，可仅使用本地净化功能。