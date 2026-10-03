---
name: agent-refine-skill
description: Agent 炼化与主动同步技能。用于第三方 Agent（如 Cursor 等 cowork 后台不可直接监听的外部 Agent）手动调用，主动向 cowork 文档中心传输本次操作的输入、输出与结论。
version: 1.0.0
---

# Agent 炼化技能 (Agent Refine Skill)

## 技能说明
当使用第三方 Agent（如 Cursor、Claude Code 等 cowork 后台无法直接监听进程状态的外部工具）时，无法通过后台自动采集日志。
本技能由第三方 Agent 在完成任务或阶段性产出后**主动调用**，将本次改动的上下文、代码 diff 和最终结论写回 cowork 文档中心（会话 `ANNOUNCEMENT.md` / 群报告）。

## 调用方式

1. 从成员设置复制「炼化 Skill 指令」，或 `GET /api/docs/refine-prompt?sessionId=...`。
2. 本机工作台已启动时，用与前端相同的 `X-ACW-Token`（`POST /api/bootstrap`）调用：

```http
POST /api/docs/refine
Content-Type: application/json
X-ACW-Token: <local-token>

{
  "sessionId": "<当前会话 id>",
  "input": "本次用户需求",
  "output": "git diff 摘要 / 文件列表",
  "conclusion": "验证结果与下一步",
  "source": "agent-refine-skill"
}
```

3. 无 API 时，把同结构的「外部 Agent 炼化」章节追加到 `journals/sessions/{sessionId}/ANNOUNCEMENT.md`。

## 执行步骤
1. **收集结构化数据**：汇总【输入】、【输出/改动】与【结论】。
2. **主动上报写回**：优先 `POST /api/docs/refine`；失败再写群报告 Markdown。
3. **刷新文档中心**：工作台右侧「文档中心」会读到更新后的群报告。
