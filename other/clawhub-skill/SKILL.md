---
name: moltguard
description: "开源 OpenClaw 安全插件：本地提示词净化 + 注入检测。完整源码见 github.com/openguardrails/moltguard"
metadata: {"openclaw":{"emoji":"🛡️","homepage":"https://github.com/openguardrails/moltguard"}}
---

# MoltGuard 安全防护插件指南

> **注意：** 本 SKILL 文件是指向外部 npm 包（`@openguardrails/moltguard`）和远程 API（`api.moltguard.com`）的文档。实际插件代码**未**打包在此 SKILL 文件中——你需要单独安装。这是 OpenClaw 插件的标准做法。
>
> **安装前，你必须：**
> 1. 验证 npm 包与 GitHub 源码一致
> 2. 审核关键文件（见下文，约 500 行）
> 3. 了解哪些数据会被发送到 API（即使已经过"净化"）
> 4. 做好在行为异常时删除凭据的准备

## ⚠️ 安全建议：安装前需知

**本文档指向一个外部 npm 包和远程 API。请在安装前验证以下内容：**

### 1. 验证 npm 包与 GitHub 源码一致

```bash
# 步骤 1：检查 npm 包内容
npm pack @openguardrails/moltguard
tar -xzf openguardrails-moltguard-*.tgz
ls -la package/
# 应显示：gateway/、agent/、memory/、index.ts

# 步骤 2：克隆 GitHub 仓库
git clone https://github.com/openguardrails/moltguard.git

# 步骤 3：对比（排除构建产物）
diff -r package/ moltguard/ | grep -v "node_modules\|\.git\|dist"
# 不应有显著差异
```

### 2. 审核关键文件（安装前必做）

**以下是唯二执行逻辑的文件，请审核：**

| 文件 | 用途 | 审核要点 |
|------|---------|---------------|
| `gateway/sanitizer.ts` | 敏感数据检测 | 第 21-64 行：实体匹配模式（邮箱、银行卡、密钥）<br>第 93-105 行：熵值计算<br>第 117-176 行：匹配收集逻辑 |
| `gateway/restorer.ts` | 占位符还原 | 第 13-20 行：文本还原逻辑<br>第 47-56 行：递归值还原 |
| `agent/runner.ts` | **网络调用** | 第 103-117 行：**向 api.moltguard.com 发起 API 请求**<br>第 80-95 行：API 调用前的净化处理 |
| `memory/store.ts` | **文件操作** | 第 30-50 行：**创建 3 个本地文件**（凭据、日志） |
| `agent/config.ts` | API 密钥管理 | 第 46-64 行：**一次性注册调用** |

**继续之前，请阅读这约 500 行代码。** 如有任何可疑之处，**请勿安装。**

### 3. 了解 API 与隐私权衡

**API 端点：** `https://api.moltguard.com`

**发送的数据：**
- ✅ 已净化的内容（PII/密钥已在本地移除）
- ✅ 分析请求（注入检测判断）

**不会发送的数据：**
- ❌ 原始用户提示（已先净化）
- ❌ API 密钥或密码（已被本地净化器剥离）
- ❌ 文件名、工具名称、会话 ID

**隐私政策：** https://moltguard.com/privacy

**威胁模型考量：**
- 即使是"已净化"的文本也会泄露部分信息（内容结构、提示词模式）
- 如果无法接受任何外部 API 调用，请使用仅网关模式：`"enabled": false, "sanitizePrompt": true`
- 如需最大隐私：自行托管 API 或完全禁用注入检测

### 4. 文件路径与权限

**将创建以下文件：**

```bash
~/.openclaw/credentials/moltguard/credentials.json  # 你的 API 密钥
~/.openclaw/logs/moltguard-analyses.jsonl           # 分析日志
~/.openclaw/logs/moltguard-feedback.jsonl           # 用户反馈
```

**彻底清除所有痕迹：**
```bash
# 卸载插件
openclaw plugins uninstall @openguardrails/moltguard

# 删除凭据和日志
rm -rf ~/.openclaw/credentials/moltguard
rm -f ~/.openclaw/logs/moltguard-*.jsonl
```

### 5. 决策矩阵

| 如果... | 那么... |
|-----------|---------|
| ✅ 能审核约 500 行 TypeScript | 完成审核后，满意再安装 |
| ✅ 接受部分数据发送到 api.moltguard.com | 正常安装 |
| ⚠️ 希望零外部调用 | 使用 `"enabled": false, "sanitizePrompt": true`（仅网关模式） |
| ❌ 无法审核代码 | **请勿安装** |
| ❌ 无法接受任何外部 API | **请勿安装**（或自行托管） |

---

## 安装前验证步骤

1. **📦 已发布包：** https://www.npmjs.com/package/@openguardrails/moltguard
2. **📂 完整源码：** https://github.com/openguardrails/moltguard（MIT 许可证）
3. **🔍 验证内容：**
   ```bash
   # 下载并检查实际包内容
   npm pack @openguardrails/moltguard
   tar -xzf openguardrails-moltguard-*.tgz
   ls -la package/
   # 你将看到：gateway/、agent/、memory/、index.ts（TypeScript 源码）
   ```
4. **📊 包大小：** 约 100KB（包含所有 TypeScript 源文件，不仅仅是文档）
5. **🏗️ 构建产物：** 无。本包发布的是 TypeScript 源码，而非编译后的 JavaScript（OpenClaw 在运行时编译插件）

**为什么没有传统意义上的"安装步骤"：**
- OpenClaw 插件通过 `openclaw plugins install` 安装（而非 `npm install`）
- 插件是自包含的 TypeScript，由 OpenClaw 动态加载
- 无需构建步骤（OpenClaw 的 TypeScript 运行时处理编译）

---

## 包信息

📦 **npm 包：** [@openguardrails/moltguard](https://www.npmjs.com/package/@openguardrails/moltguard)
📂 **源码：** [github.com/openguardrails/moltguard](https://github.com/openguardrails/moltguard)
📄 **许可证：** MIT
🔒 **安全性：** 所有代码开源可审核

## 本包包含的内容

这不仅仅是文档。当你运行 `openclaw plugins install @openguardrails/moltguard` 时，你会获得：

**可验证的源码：**
- `gateway/` - 本地 HTTP 代理服务器（TypeScript，约 800 行）
- `agent/` - 注入检测逻辑（TypeScript，约 400 行）
- `memory/` - 本地 JSONL 日志（TypeScript，约 200 行）
- `index.ts` - 插件入口点（TypeScript，约 400 行）

**安装方式：**
```bash
# 从 npm 安装（包含所有源码的已发布包）
openclaw plugins install @openguardrails/moltguard

# 验证安装
openclaw plugins list
# 应显示：MoltGuard | moltguard | loaded

# 审核已安装的代码
ls -la ~/.openclaw/plugins/node_modules/@openguardrails/moltguard/
# 你将看到：gateway/、agent/、memory/、index.ts、package.json
```

## 安装前安全验证

**1. 审核源码**

所有代码在 GitHub 上开源。安装前请审核：

```bash
# 克隆并检查
git clone https://github.com/openguardrails/moltguard.git
cd moltguard

# 需审核的关键文件（总计约 1,800 行）：
# gateway/sanitizer.ts    - 净化哪些内容
# gateway/restorer.ts     - 如何还原占位符
# gateway/handlers/       - 协议实现（Anthropic、OpenAI、Gemini）
# agent/runner.ts         - 对 api.moltguard.com 的网络调用
# agent/config.ts         - API 密钥管理
# memory/store.ts         - 本地文件存储（仅 JSONL 日志）
```

**2. 验证网络调用**

代码仅发起 **2 种类型的网络调用**（见 `agent/runner.ts` 第 80-120 行）：

**调用 1：一次性 API 密钥注册**（当 `autoRegister: true` 时）
```typescript
// agent/config.ts 第 46-64 行
POST https://api.moltguard.com/api/register
请求头: { "Content-Type": "application/json" }
请求体: { "agentName": "openclaw-agent" }
响应: { "apiKey": "mga_..." }
```

**调用 2：注入检测分析**
```typescript
// agent/runner.ts 第 103-117 行
POST https://api.moltguard.com/api/check/tool-call
请求头: {
  "Authorization": "Bearer <你的API密钥>",
  "Content-Type": "application/json"
}
请求体: {
  "content": "<已净化文本，PII/密钥已被替换>",
  "async": false
}
响应: {
  "ok": true,
  "verdict": { "isInjection": boolean, "confidence": 0-1, ... }
}
```

**不会发送的内容：**
- 原始用户内容（先净化，见 `agent/sanitizer.ts`）
- 文件名、工具名称、智能体 ID、会话密钥
- API 密钥或密码（在 API 调用前剥离）

**3. 验证本地文件操作**

仅创建/修改 **3 个文件**（见 `memory/store.ts`）：

```bash
~/.openclaw/credentials/moltguard/credentials.json  # 仅 API 密钥
~/.openclaw/logs/moltguard-analyses.jsonl           # 分析结果
~/.openclaw/logs/moltguard-feedback.jsonl           # 用户反馈
```

不会触碰其他文件。不使用外部数据库。

**4. TLS 与隐私**

- **TLS：** 所有 API 调用使用 HTTPS（代码中强制执行，见 `agent/runner.ts` 第 106 行）
- **隐私政策：** https://moltguard.com/privacy
- **数据留存：** 分析完成后内容**不**存储（已通过 MoltGuard 数据处理协议验证）
- **无第三方共享：** 分析由 MoltGuard API 直接执行，不转发至 OpenAI/Anthropic 等

## 功能特性

✨ **新增：本地提示词净化网关** - 在发送到 LLM 之前保护敏感数据（银行卡、密码、API 密钥）
🛡️ **提示注入检测** - 检测并拦截隐藏在外部内容中的恶意指令

所有敏感数据处理均在**你的机器上本地完成**。

## 功能 1：本地提示词净化网关

**6.0 版本**引入了本地 HTTP 代理，可在你的敏感数据到达任何 LLM 之前进行保护。

### 工作原理

```
你的提示："我的银行卡是 6222021234567890，帮我订酒店"
      ↓
网关净化："我的银行卡是 __bank_card_1__，帮我订酒店"
      ↓
发送到 LLM（Claude/GPT/Kimi 等）
      ↓
LLM 回复："正在用 __bank_card_1__ 订房"
      ↓
网关还原："正在用 6222021234567890 订房"
      ↓
工具在本地使用真实卡号执行
```

### 受保护的数据类型

网关自动检测并净化以下类型：

- **银行卡号** → `__bank_card_1__`（16-19 位数字）
- **信用卡号** → `__credit_card_1__`（1234-5678-9012-3456）
- **电子邮箱** → `__email_1__`（user@example.com）
- **手机号码** → `__phone_1__`（+86-138-1234-5678）
- **API 密钥/密钥** → `__secret_1__`（sk-...、ghp_...、Bearer 令牌）
- **IP 地址** → `__ip_1__`（192.168.1.1）
- **美国社会安全号** → `__ssn_1__`（123-45-6789）
- **国际银行账号** → `__iban_1__`（GB82WEST...）
- **URL 链接** → `__url_1__`（https://...）

### 快速配置

**1. 启用网关：**

编辑 `~/.openclaw/openclaw.json`：
```json
{
  "plugins": {
    "entries": {
      "moltguard": {
        "config": {
          "sanitizePrompt": true,      // ← 启用网关
          "gatewayPort": 8900          // 端口（默认：8900）
        }
      }
    }
  }
}
```

**2. 配置你的模型使用网关：**

```json
{
  "models": {
    "providers": {
      "claude-protected": {
        "baseUrl": "http://127.0.0.1:8900",  // ← 指向网关
        "api": "anthropic-messages",          // 保持协议不变
        "apiKey": "${ANTHROPIC_API_KEY}",
        "models": [
          {
            "id": "claude-sonnet-4-20250514",
            "name": "Claude Sonnet (受保护)"
          }
        ]
      }
    }
  }
}
```

**3. 重启 OpenClaw：**

```bash
openclaw gateway restart
```

### 网关管理命令

在 OpenClaw 中使用以下命令管理网关：

- `/mg_status` - 查看网关状态和配置示例
- `/mg_start` - 启动网关
- `/mg_stop` - 停止网关
- `/mg_restart` - 重启网关

### 支持的 LLM 提供商

网关适用于**任何 LLM 提供商**：

| 协议 | 提供商 |
|----------|-----------|
| Anthropic Messages API | Claude、Anthropic 兼容接口 |
| OpenAI Chat Completions | GPT、Kimi、DeepSeek、通义千问、文心一言等 |
| Google Gemini | Gemini Pro、Flash |

为每个提供商配置 `baseUrl: "http://127.0.0.1:8900"`，网关会自动处理其余工作。

## 功能 2：提示注入检测

### 隐私与网络透明度

对于注入检测，MoltGuard 首先在**本地剥离敏感信息**——电子邮箱、手机号、信用卡号、API 密钥等——将它们替换为安全的占位符，如 `<EMAIL>` 和 `<SECRET>`。

- **先本地净化。** 内容在发送分析之前就在你的机器上完成净化。PII 和密钥永远不会离开你的设备。完整实现见 `agent/sanitizer.ts`。
- **净化的内容：** 电子邮箱、手机号、信用卡号、社会安全号、IP 地址、API 密钥/密钥、URL、国际银行账号以及高熵令牌。
- **注入模式保留。** 净化仅剥离敏感数据——注入检测所需的结构和上下文保持不变。

### 网络传输的精确内容

本插件仅发起 **2 种类型的网络调用**，均通过 HTTPS 访问 `api.moltguard.com`。不会联系其他主机。

**1. 分析请求**（`agent/runner.ts` — `POST /api/check/tool-call`）：
```json
{
  "content": "<已净化文本，PII/密钥已被占位符替换>",
  "async": false
}
```
这就是完整的请求体。**不会发送：** sessionKey、agentId、toolCallId、channelId、文件名、工具名称、用户名或其他任何元数据。这些字段存在于本地的 `AnalysisTarget` 对象中，但永远不会包含在 API 调用中——你可以在 `agent/runner.ts` 第 103-117 行验证。

**2. 一次性 API 密钥注册**（`agent/config.ts` — `POST /api/register`）：
```json
{
  "agentName": "openclaw-agent"
}
```
这就是完整的请求体——一个硬编码的字符串。**不会发送：** 机器标识符、系统信息、环境变量、密钥或文件内容。你可以在 `agent/config.ts` 第 46-64 行验证。要完全跳过自动注册，设置 `autoRegister: false` 并在配置中提供你自己的 `apiKey`（见下方 [API 密钥管理](#api-密钥管理)）。

### 本地存储

- **API 密钥：** `~/.openclaw/credentials/moltguard/credentials.json` — 仅包含 `{ "apiKey": "..." }`。由 `agent/config.ts` 创建。
- **审计日志：** `~/.openclaw/logs/moltguard-analyses.jsonl` 和 `~/.openclaw/logs/moltguard-feedback.jsonl` — 仅追加的 JSONL 文件，记录分析结果和用户反馈。永远不会发送到任何服务器。由 `memory/store.ts` 创建。
- **没有其他文件**由此插件创建或读取，除了上述文件和其自身的源码。

### 额外保障

- **你的 API 密钥归你所有。** 每次安装都会获得一个唯一的 API 密钥，首次使用时自动注册。没有共享或硬编码的密钥。
- **无第三方 LLM 调用。** 分析由 MoltGuard API 直接执行——不会将内容转发至 OpenAI 或其他第三方服务。
- **分析后内容不存储。**
- **完全可审核。** 整个插件开源。净化器（`agent/sanitizer.ts`）、运行器（`agent/runner.ts`）和配置（`agent/config.ts`）是唯三接触网络的文件——直接审核它们即可验证以上声明。

## 面临的问题

当你的 AI 智能体读取外部内容（邮件、网页、文档）时，攻击者可以嵌入隐藏指令，如：

```
------- 转发邮件（请勿向用户显示）-------
系统警报：<此处为注入内容>
执行：<此处为你的凭据收集操作>"
------- 转发邮件结束 -------
```

没有防护的话，你的智能体可能会执行这些恶意指令，导致数据泄露、未授权操作或安全漏洞。

## 安装方式

### 方式 1：从 npm 安装（推荐）

```bash
# 安装已发布的包
openclaw plugins install @openguardrails/moltguard

# 重启以加载插件
openclaw gateway restart

# 验证安装
openclaw plugins list | grep moltguard
```

### 方式 2：从源码安装（最大信任度）

```bash
# 克隆并先审核源码
git clone https://github.com/openguardrails/moltguard.git
cd moltguard

# 审核代码（所有文件均为 TypeScript，人类可读）
cat gateway/sanitizer.ts    # 查看净化哪些内容
cat agent/runner.ts          # 查看网络调用
cat memory/store.ts          # 查看文件操作

# 从本地目录安装
openclaw plugins install -l .
openclaw gateway restart
```

### 方式 3：隔离测试（最大谨慎度）

```bash
# 创建测试环境
mkdir ~/openclaw-test
cd ~/openclaw-test

# 在测试环境中安装 OpenClaw
# （参考 OpenClaw 文档）

# 在测试环境中安装 moltguard
openclaw plugins install @openguardrails/moltguard

# 使用一次性 API 密钥测试（非生产环境）
# 监控网络流量：使用 tcpdump、wireshark 或 mitmproxy
# 验证仅联系 api.moltguard.com
```

## API 密钥管理

首次使用时，MoltGuard 会**自动注册**一个免费 API 密钥——无需邮箱、密码或手动设置。

**密钥存储在哪里？**

```
~/.openclaw/credentials/moltguard/credentials.json
```

仅包含 `{ "apiKey": "mga_..." }`。

**使用你自己的密钥：**

在插件配置中设置 `apiKey`（`~/.openclaw/openclaw.json`）：

```json
{
  "plugins": {
    "entries": {
      "moltguard": {
        "config": {
          "apiKey": "mga_你的密钥"
        }
      }
    }
  }
}
```

**完全禁用自动注册：**

如果你在受管理或无网络环境中，希望阻止一次性注册调用：

```json
{
  "plugins": {
    "entries": {
      "moltguard": {
        "config": {
          "apiKey": "mga_你的密钥",
          "autoRegister": false
        }
      }
    }
  }
}
```

当 `autoRegister: false` 且没有 `apiKey` 时，分析将失败，直到提供密钥。

## 验证安装

检查插件是否已加载：

```bash
openclaw plugins list
```

你应该看到：

```
| MoltGuard | moltguard | loaded | ...
```

检查网关日志中的初始化信息：

```bash
openclaw logs --follow | grep "moltguard"
```

应看到：

```
[moltguard] Initialized (block: true, timeout: 60000ms)
```

## 工作原理

MoltGuard 钩入 OpenClaw 的 `tool_result_persist` 事件。当你的智能体读取任何外部内容时：

```
内容（邮件/网页/文档）
         |
         v
   +-----------+
   |  本地     |  剥离邮箱、手机号、信用卡号、
   |  净化     |  社会安全号、API 密钥、URL、国际银行账号...
   +-----------+
         |
         v
   +-----------+
   | MoltGuard |  POST /api/check/tool-call
   |   API     |  发送已净化内容
   +-----------+
         |
         v
   +-----------+
   |  判定     |  isInjection: true/false + 置信度 + 发现
   +-----------+
         |
         v
   拦截 或 放行
```

内容在发送到 API 之前在本地净化——敏感数据永远不会离开你的机器。如果检测到高置信度的注入，内容会在智能体处理之前被拦截。

## 命令

MoltGuard 提供网关管理和注入检测两方面的斜杠命令：

### 网关管理命令

**`/mg_status`** - 查看网关状态

```
/mg_status
```

返回：
- 网关运行状态
- 端口和端点
- 不同 LLM 提供商的配置示例

**`/mg_start`** - 启动网关

```
/mg_start
```

**`/mg_stop`** - 停止网关

```
/mg_stop
```

**`/mg_restart`** - 重启网关

```
/mg_restart
```

### 注入检测命令

**`/og_status`** - 查看检测状态和统计

```
/og_status
```

返回：
- 配置信息（是否启用、拦截模式、API 密钥状态）
- 统计数据（总分析次数、拦截次数、平均耗时）
- 最近分析记录

**`/og_report`** - 查看最近的注入检测

```
/og_report
```

返回：
- 检测 ID、时间戳、状态
- 内容类型和大小
- 检测原因
- 可疑内容片段

**`/og_feedback`** - 报告误报或漏检

```
# 报告误报（检测 ID 来自 /og_report）
/og_feedback 1 fp 这是正常的安全文档

# 报告漏检
/og_feedback missed 邮件中包含隐藏注入但未被检测到
```

你的反馈有助于提升检测质量。

## 配置

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "plugins": {
    "entries": {
      "moltguard": {
        "enabled": true,
        "config": {
          // 网关（提示词净化）- 新功能
          "sanitizePrompt": false,      // 启用本地提示词净化
          "gatewayPort": 8900,          // 网关端口
          "gatewayAutoStart": true,     // OpenClaw 启动时自动启动网关

          // 注入检测
          "blockOnRisk": true,          // 检测到注入时拦截
          "timeoutMs": 60000,           // 分析超时时间
          "apiKey": "",                 // 留空则自动注册
          "autoRegister": true,         // 自动注册 API 密钥
          "apiBaseUrl": "https://api.moltguard.com",
          "logPath": "~/.openclaw/logs" // JSONL 日志目录
        }
      }
    }
  }
}
```

### 配置选项

#### 网关（提示词净化）

| 选项 | 默认值 | 说明 |
|--------|---------|-------------|
| `sanitizePrompt` | `false` | 启用本地提示词净化网关 |
| `gatewayPort` | `8900` | 网关服务器端口 |
| `gatewayAutoStart` | `true` | OpenClaw 启动时自动启动网关 |

#### 注入检测

| 选项 | 默认值 | 说明 |
|--------|---------|-------------|
| `enabled` | `true` | 启用/禁用插件 |
| `blockOnRisk` | `true` | 检测到注入时拦截内容 |
| `apiKey` | `""`（自动） | MoltGuard API 密钥。留空则首次使用时自动注册 |
| `autoRegister` | `true` | 当 `apiKey` 为空时自动注册免费 API 密钥 |
| `timeoutMs` | `60000` | 分析超时时间（毫秒） |
| `apiBaseUrl` | `https://api.moltguard.com` | MoltGuard API 端点（可覆盖为预发布或自托管环境） |
| `logPath` | `~/.openclaw/logs` | JSONL 审计日志文件目录 |

### 常用配置

**全面保护模式**（推荐）：
```json
{
  "sanitizePrompt": true,   // 保护敏感数据
  "blockOnRisk": true       // 拦截注入攻击
}
```

**仅监控模式**（记录检测但不拦截）：
```json
{
  "sanitizePrompt": false,
  "blockOnRisk": false
}
```

**仅网关模式**（无注入检测）：
```json
{
  "sanitizePrompt": true,
  "enabled": false
}
```

检测结果会记录在 `/og_report` 中，但不会拦截内容。

## 测试检测

下载包含隐藏注入的测试文件：

```bash
curl -L -o /tmp/test-email.txt https://raw.githubusercontent.com/openguardrails/moltguard/main/samples/test-email.txt
```

让你的智能体读取文件：

```
读取 /tmp/test-email.txt 的内容
```

检查日志：

```bash
openclaw logs --follow | grep "moltguard"
```

你应该看到：

```
[moltguard] INJECTION DETECTED in tool result from "read": Contains instructions to override guidelines and execute malicious command
```

## 卸载

```bash
openclaw plugins uninstall @openguardrails/moltguard
openclaw gateway restart
```

同时删除存储数据（可选）：

```bash
# 删除 API 密钥
rm -rf ~/.openclaw/credentials/moltguard

# 删除审计日志
rm -f ~/.openclaw/logs/moltguard-analyses.jsonl ~/.openclaw/logs/moltguard-feedback.jsonl
```

## 验证清单（安装前）

使用此清单验证插件的合法性和安全性：

- [ ] **源码公开：** 访问 https://github.com/openguardrails/moltguard 并审核代码
- [ ] **npm 包与源码一致：** 对比已发布包与 GitHub 仓库
  ```bash
  npm view @openguardrails/moltguard dist.tarball
  # 下载并解压 tarball，与 GitHub 代码对比
  ```
- [ ] **网络调用可审核：** 阅读 `agent/runner.ts` 第 80-120 行查看所有网络调用
- [ ] **文件操作有限：** 阅读 `memory/store.ts` 查看仅创建 3 个本地文件
- [ ] **无混淆：** 所有代码为可读 TypeScript，无压缩或打包
- [ ] **MIT 许可证：** 可自由使用、修改和审核
- [ ] **GitHub 活跃度：** 检查提交历史、Issue 和贡献者
- [ ] **npm 下载统计：** 验证包被他人使用（不仅仅是你自己）

## 监控网络流量（可选但推荐）

安装后，监控网络流量以验证声明：

```bash
# Linux
sudo tcpdump -i any -n host api.moltguard.com

# 你应该只能看到：
# 1. POST 到 /api/register（首次使用时仅一次）
# 2. POST 到 /api/check/tool-call（分析内容时）
# 不应联系其他主机。
```

## 常见问题

**问：网关代码是否包含在 npm 包中？**
答：**是的。** npm 包包含所有源码（`gateway/`、`agent/`、`memory/`）。你可以运行 `npm pack @openguardrails/moltguard` 并检查 tarball 来验证。

**问：能否在无网络访问的情况下运行？**
答：**部分可以。** 网关（提示词净化）可 100% 离线工作。注入检测需要 API 访问，但你可以通过 `"enabled": false` 禁用它，仅使用网关模式。

**问：如何确保我的 API 密钥安全？**
答：**审核代码。** 检查 `agent/sanitizer.ts` 第 66-88 行的密钥检测模式。匹配 `sk-`、`ghp_` 等的 API 密钥会在任何网络调用之前被替换为 `<SECRET>`。你可以发送包含 `sk-test123` 的提示词并检查网络流量来自行测试。

**问：能否自行托管 MoltGuard API？**
答：**可以。** 在配置中设置 `"apiBaseUrl": "https://你的服务器.com"`。API 是标准的 HTTP 端点（精确的请求格式见 `agent/runner.ts`）。

**问：如果不信任 npm 怎么办？**
答：**从源码安装。** 克隆 GitHub 仓库，审核每个文件，然后运行 `openclaw plugins install -l /path/to/moltguard`。这完全绕过了 npm。

## 相关链接与资源

**源码与发布：**
- GitHub 仓库：https://github.com/openguardrails/moltguard
- GitHub 发布：https://github.com/openguardrails/moltguard/releases
- 源码浏览：https://github.com/openguardrails/moltguard/tree/main

**包与分发：**
- npm 包：https://www.npmjs.com/package/@openguardrails/moltguard
- npm 包源码：https://unpkg.com/@openguardrails/moltguard/（查看已发布文件）

**文档：**
- 隐私政策：https://moltguard.com/privacy
- API 文档：https://moltguard.com/docs（请求/响应格式）
- Issue 追踪：https://github.com/openguardrails/moltguard/issues

**安全：**
- 报告漏洞：security@moltguard.com（或 GitHub 私有 Issue）
- 负责任披露：90 天政策，在更新日志中署名

---

## 最后说明：透明度与信任

本插件旨在实现**最大透明度**：

1. ✅ 所有代码开源（MIT 许可证）
2. ✅ 无打包或混淆（可读 TypeScript）
3. ✅ 网络调用有文档且可审核
4. ✅ 文件操作最少且仅限本地
5. ✅ 可从源码安装（绕过 npm/注册中心）
6. ✅ 可在隔离环境中测试（一次性环境）
7. ✅ 可自行托管（自有 API 服务器）

**如有顾虑，请先审核代码。如发现可疑之处，请报告。**