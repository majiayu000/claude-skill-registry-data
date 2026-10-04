---
name: a2a-lite
description: Agent-to-Agent 轻量通信协议。仿 Google A2A 设计，但适配 Clawdbot/OpenClaw 生态。用于：(1) Agent 能力发现 (2) 跨 agent 任务协作 (3) 结构化的 agent 间消息交换。触发词：a2a、agent协议、agent通信、agent card、能力发现。
---

# A2A-Lite: Agent-to-Agent 轻量通信协议

基于 Google A2A 协议精简设计，适配 Clawdbot/OpenClaw 生态的 agent 间自然语言通信标准。

## 设计原则

1. **自然语言优先** — 协议消息是增强型自然语言，而非纯 JSON RPC
2. **渐进式采用** — 即使对方不支持协议，基本通信也能工作
3. **轻量级** — 不需要 HTTP 服务器，基于现有消息通道
4. **人类可读** — 所有协议消息人类也能理解

## 核心概念

### Agent Card（能力卡片）

每个 agent 维护一个 `agent-card.json`，描述自身能力：

```json
{
  "protocol": "a2a-lite/1.0",
  "agent": {
    "id": "jiajia",
    "name": "佳佳",
    "framework": "clawdbot",
    "version": "0.x"
  },
  "skills": [
    {
      "id": "research",
      "name": "调研助手",
      "description": "收集和分析特定主题的资料",
      "inputModes": ["text"],
      "outputModes": ["text", "file"]
    },
    {
      "id": "podcast-script",
      "name": "播客脚本",
      "description": "创作播客口播稿",
      "inputModes": ["text", "file"],
      "outputModes": ["text", "file"]
    }
  ],
  "capabilities": {
    "streaming": false,
    "fileTransfer": true,
    "asyncTasks": false
  },
  "channels": ["discord:jiajia"]
}
```

### 消息类型

#### 1. 能力查询 (discover)

```
[A2A:discover]
请告诉我你能做什么？
```

响应：
```
[A2A:card]
我是佳佳，运行在 Clawdbot 上。
我的主要能力：
- 调研助手：收集和分析特定主题的资料
- 播客脚本：创作播客口播稿
支持文件传输，不支持流式输出。
```

#### 2. 任务请求 (task)

```
[A2A:task id=research-001]
帮我调研一下 "AI Agent 生态的最新进展"，时间范围过去一周。
预计需要的输出：markdown 报告文件。
```

#### 3. 任务状态更新 (status)

```
[A2A:status task=research-001 state=working]
正在收集资料，预计还需要 10 分钟。
```

状态值：
- `accepted` — 任务已接受
- `working` — 处理中
- `input-required` — 需要更多输入
- `completed` — 已完成
- `failed` — 失败
- `cancelled` — 已取消

#### 4. 任务结果 (result)

```
[A2A:result task=research-001 state=completed]
调研报告已完成，见附件。
[附件: ai-agent-research-2026-02.md]
```

#### 5. 普通消息 (无标记)

不需要协议包装的日常交流正常发送，保持自然。

## 使用流程

### 发起协作

1. **检查本地 card** — 读取 `skills/a2a-lite/agent-card.json`
2. **发送 discover** — 了解对方能力（如果不确定）
3. **发送 task** — 用结构化格式描述任务
4. **跟踪状态** — 通过 status 更新了解进度
5. **接收结果** — 处理 result 消息和附件

### 响应协作请求

1. **识别协议消息** — 检查 `[A2A:...]` 标记
2. **解析请求** — 提取任务 ID 和内容
3. **评估能力** — 检查是否在自己的 skills 范围内
4. **响应或拒绝** — 用 status 回应
5. **执行并报告** — 完成后用 result 回应

## 协议消息格式

```
[A2A:<type> <params>]
<自然语言消息体>
[可选附件]
```

参数格式：`key=value`，多个用空格分隔

示例：
- `[A2A:discover]`
- `[A2A:task id=task-123 skill=research]`
- `[A2A:status task=task-123 state=working progress=50%]`
- `[A2A:result task=task-123 state=completed]`

## Agent Card 管理

### 创建/更新自己的 card

```bash
# Card 位置
skills/a2a-lite/agent-card.json
```

**必填字段：**
- `protocol` — 协议版本
- `agent.id` — 唯一标识
- `agent.name` — 显示名称
- `agent.framework` — 运行框架 (clawdbot/openclaw/other)
- `skills[]` — 能力列表
- `channels[]` — 可达通道

**可选字段：**
- `capabilities` — 支持的特性
- `limits` — 资源限制（如最大文件大小）

### 读取对方的 card

收到 `[A2A:card]` 响应时，可选择缓存到：
```
skills/a2a-lite/known-agents/<agent-id>.json
```

## 与现有机制的关系

### 与 cross-agent-collab 的区别

- **cross-agent-collab** — 行为规范（怎么做）
- **a2a-lite** — 通信格式（怎么说）

两者互补，a2a-lite 消息应遵循 cross-agent-collab 的原则。

### 与 sessions_send 的关系

A2A-Lite 消息通过现有通道发送：
- Discord 频道：正常发消息
- 跨 session：用 `sessions_send`

协议标记 `[A2A:...]` 是语义增强，不改变传输方式。

## 错误处理

### 对方不支持协议

如果对方未用协议格式回应，降级为普通自然语言交流。

### 任务无法完成

```
[A2A:status task=research-001 state=failed]
无法完成此任务：缺少访问 X 数据源的权限。
建议：请联系鲁伊科斯塔授权。
```

### 能力不匹配

```
[A2A:status task=video-edit-001 state=failed]
此任务超出我的能力范围。我的 skills 不包含视频编辑。
```

## 安全注意

1. **不传输凭据** — Agent card 和消息中不含 API key
2. **文件用附件** — 不假设对方能访问本地路径
3. **不跨系统操作** — 仅协调，不代执行对方系统命令

## 示例：完整协作流程

**佳佳 → Mexico:**
```
[A2A:discover]
你好！我想了解一下你的能力，看看我们能不能协作完成一个任务。
```

**Mexico → 佳佳:**
```
[A2A:card]
我是 Mexico，运行在 OpenClaw 上。
我的能力：
- 邮件发送：通过 SMTP 发送邮件和附件
- 日程管理：Google Calendar 操作
支持文件接收。
```

**佳佳 → Mexico:**
```
[A2A:task id=email-001 skill=email]
帮我把这份调研报告发给鲁伊科斯塔。
收件人：5155280@qq.com
主题：AI Agent 调研报告
正文：请查收附件中的调研报告。
[附件: ai-agent-research.md]
```

**Mexico → 佳佳:**
```
[A2A:status task=email-001 state=accepted]
收到，正在发送邮件。
```

**Mexico → 佳佳:**
```
[A2A:result task=email-001 state=completed]
邮件已成功发送到 5155280@qq.com。
```

## 参考资料

- **协议规范详情**: [references/protocol-spec.md](references/protocol-spec.md) — 完整的消息类型、状态值、Schema 定义
- **辅助脚本**: 
  - `scripts/parse_message.sh` — 解析协议消息为 JSON
  - `scripts/format_message.sh` — 生成协议消息

---

*版本: 1.0 | 创建: 2026-02-09 | 作者: 佳佳*
*灵感来源: Google A2A Protocol (a2aproject/A2A)*
