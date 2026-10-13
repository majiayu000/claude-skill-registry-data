---
name: memory-setup
description: 启用并配置 Moltbot/Clawdbot 的持久化记忆搜索功能。当用户需要设置记忆功能、修复"金鱼记忆"问题，或配置 memorySearch 时使用。涵盖 MEMORY.md、每日日志和向量搜索的设置。
---

# 记忆设置技能

让你的 Agent 从金鱼变成大象。本技能帮助配置 Moltbot/Clawdbot 的持久化记忆功能。

## 快速设置

### 1. 在配置中启用记忆搜索

添加到 `~/.clawdbot/clawdbot.json`（或 `moltbot.json`）：

```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "voyage",
    "sources": ["memory", "sessions"],
    "indexMode": "hot",
    "minScore": 0.3,
    "maxResults": 20
  }
}
```

### 2. 创建记忆目录结构

在工作区中创建：

```
workspace/
├── MEMORY.md              # 长期精炼记忆
└── memory/
    ├── logs/              # 每日日志 (YYYY-MM-DD.md)
    ├── projects/          # 项目特定上下文
    ├── groups/            # 群聊上下文
    └── system/            # 偏好设置、安装笔记
```

### 3. 初始化 MEMORY.md

在工作区根目录创建 `MEMORY.md`：

```markdown
# MEMORY.md — 长期记忆

## 关于 [用户名]
- 关键信息、偏好、上下文

## 活跃项目
- 项目摘要和状态

## 决策与经验教训
- 做出的重要选择
- 吸取的教训

## 偏好
- 沟通风格
- 工具和工作流
```

## 配置选项说明

| 设置项 | 用途 | 推荐值 |
|---------|---------|-------------|
| `enabled` | 启用记忆搜索 | `true` |
| `provider` | 嵌入向量提供商 | `"voyage"` |
| `sources` | 索引范围 | `["memory", "sessions"]` |
| `indexMode` | 索引时机 | `"hot"`（实时） |
| `minScore` | 相关性阈值 | `0.3`（值越低结果越多） |
| `maxResults` | 最大返回片段数 | `20` |

### 提供商选项
- `voyage` — Voyage AI 嵌入向量（推荐）
- `openai` — OpenAI 嵌入向量
- `local` — 本地嵌入向量（无需 API 密钥）

### 数据源选项
- `memory` — MEMORY.md + memory/*.md 文件
- `sessions` — 历史会话记录
- `both` — 全部上下文（推荐）

## 每日日志格式

每天创建 `memory/logs/YYYY-MM-DD.md`：

```markdown
# YYYY-MM-DD — 每日日志

## [时间] — [事件/任务]
- 发生了什么
- 做出的决策
- 需要跟进的事项

## [时间] — [另一个事件]
- 详细信息
```

## Agent 指令（AGENTS.md）

将以下内容添加到 AGENTS.md 中以控制 Agent 行为：

```markdown
## 记忆回忆
在回答关于过往工作、决策、日期、人物、偏好或待办事项的问题前：
1. 使用 memory_search 进行相关查询
2. 需要时使用 memory_get 提取具体行
3. 如果搜索后信心不足，说明已检查过记忆
```

## 故障排除

### 记忆搜索不工作？
1. 检查配置中 `memorySearch.enabled: true` 是否已设置
2. 确认工作区根目录存在 MEMORY.md
3. 重启网关：`clawdbot gateway restart`

### 搜索结果不相关？
- 将 `minScore` 降低到 `0.2` 以获取更多结果
- 将 `maxResults` 增加到 `30`
- 检查记忆文件中是否有有意义的内容

### 提供商报错？
- Voyage：在环境变量中设置 `VOYAGE_API_KEY`
- OpenAI：在环境变量中设置 `OPENAI_API_KEY`
- 如无 API 密钥，使用 `local` 提供商

## 验证

测试记忆功能是否正常工作：

```
用户："你还记得关于 [过去的话题] 的什么事吗？"
Agent：[应该搜索记忆并返回相关上下文]
```

如果 Agent 没有记忆，说明配置未生效。请重启网关。

## 完整配置示例

```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "voyage",
    "sources": ["memory", "sessions"],
    "indexMode": "hot",
    "minScore": 0.3,
    "maxResults": 20
  },
  "workspace": "/path/to/your/workspace"
}
```

## 为什么这很重要

没有记忆：
- Agent 每次会话都会忘记一切
- 重复提问，丢失上下文
- 项目缺乏连续性

有记忆后：
- 能回忆过去的对话
- 了解你的偏好
- 追踪项目历史
- 随时间建立关系

金鱼 → 大象。🐘
