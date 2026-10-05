---
slug: openclaw-coach
version: 1.0.2
displayName: OpenClaw 教练（Openclaw Coach）
summary: 私人教练 - 每日文档同步技巧教学。用于 每天自动从官网同步最新文档到 Obsidian 知识库 每天早上 7发送 OpenClaw 使用技巧 每天晚上 21让用户选择想了解的技巧主题 检测 OpenClaw 版本更新并提醒
tags: clawhub
---

# OpenClaw 教练

你的私人 OpenClaw 教练，负责文档同步和每日技巧教学。

## 定时任务

| 时间 | 任务 | 脚本 |
|------|------|------|
| 03:21 | 文档同步 | `scripts/sync-docs.sh` |
| 21:05 | 技巧选择 | `scripts/pick-daily-tip.sh` |
| 07:21 | 发送技巧 | `scripts/send-daily-tip.sh` |

## 知识库结构

```
Obsidian/Docs/OpenClaw/
├── docs/                    # 官方文档
│   ├── gateway.md
│   ├── channels.md
│   └── ...
├── tips/                    # 技巧文章
│   ├── gateway-使用指南.md
│   ├── message-发送消息.md
│   └── ...
├── daily-tips.json         # 每日技巧选择
├── tips-log.md             # 发送日志
└── latest-version.txt      # 当前版本
```

## 技巧文章模板

```markdown
# 技巧标题

## 简介
简短介绍这个技巧是什么

## 使用场景
- 场景1
- 场景2

## 详细步骤
1. 步骤一
2. 步骤二

## 示例
\`\`\`bash
openclaw gateway start
\`\`\`

## 注意事项
- 注意1
```

## 用户交互流程

1. **晚上 21:05**: 发送3个技巧选项让用户选择
2. **用户回复数字**: 记录选择
3. **早上 7:21**: 发送选中技巧的详细内容 + 版本更新（如有）

## 事件处理

当收到以下系统事件时，自动执行对应操作：

| 事件 | 动作 |
|------|------|
| `sync` | 执行 `scripts/sync-docs.sh` |
| `pick-tip` | 执行 `scripts/pick-daily-tip.sh` |
| `send-tip` | 执行 `scripts/send-daily-tip.sh` |

## 手动命令

- `/sync` - 立即同步文档
- `/tip` - 查看今日技巧
- `/tips list` - 查看所有可用技巧
