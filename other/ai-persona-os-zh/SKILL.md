---
name: persona
description: "AI 人格操作系统统一入口 — 设置向导、聊天指令、上下文保护、监控和学习系统。输入 'persona setup' 开始配置，'persona status' 查看仪表盘，或 'persona help' 查看所有命令。"
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - AskUserQuestion
  - Task
---

# 人格网关

这是 AI 人格操作系统插件的统一命令入口。根据意图检测将用户请求路由到对应的技能模块。

## 工作原理

1. 读取意图映射配置
2. 将用户输入与关键词模式匹配
3. 路由到正确的技能
4. 如果没有匹配则显示回退帮助信息

## 实现方式

```pseudocode
# 第一步：加载意图映射
intent_config = READ ${CLAUDE_PLUGIN_ROOT}/commands/persona/intent-mapping.yaml

# 第二步：解析用户输入
user_input = LOWERCASE(args)
matched_intent = NULL

# 第三步：匹配关键词
FOR EACH intent IN intent_config.intents:
  FOR EACH keyword IN intent.keywords:
    IF keyword IN user_input:
      matched_intent = intent
      BREAK

# 第四步：路由到技能或显示帮助
IF matched_intent IS NOT NULL:
  TASK(
    skill: matched_intent.skill,
    args: args
  )
ELSE:
  # 显示回退帮助信息
  PRINT intent_config.fallback.message
```

## 可用命令

- **persona setup** — 首次运行向导，配置你的 AI 助手
- **persona status** — 查看系统健康仪表盘
- **persona help** — 列出所有可用命令
- **persona checkpoint** — 立即保存当前上下文
- **persona heartbeat** — 运行环境健康检查
- **persona learn** — 记录一条学习或错误以供回顾

## 示例

```bash
/persona setup
/persona status
/persona help
/persona checkpoint
/persona learn "记住在文件操作前检查权限"
```
