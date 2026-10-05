---
name: flight-diagnose
description: 使用有界本地报告诊断 Codex Flight Control 的安装、runtime、文档、持久状态、Wave、Guidance、Private Skill、角色策略、托管工作区、Evidence、Completion Gate 和恢复状态。用户询问飞控状态、健康、支持信息、恢复分析或阻断原因时使用；禁止上传数据或执行破坏性修复。
---

# 诊断 Codex Flight Control

诊断只能解释当前证据，不能制造成功状态。解释 `BLOCKED` 或 `CORRUPT` 报告前，先阅读
[支持协议](references/support-protocol.md)。

## 先读取聚合报告

1. 调用 `flight_diagnostics_report`。
2. 首先报告 runtime 支持、持久化状态与健康、release state 和 `report_sha256`。
3. 明确说明报告已省略绝对路径、prompt、源码正文、Private Skill、bearer token 和
   自动上传。
4. 如果 persistence 为 `NOT_INITIALIZED`，禁止为了“让报告完整”而创建数据库。改用
   `flight_status` 解释文档与 runtime 预检。
5. 如果 persistence 为 `BLOCKED`，只能使用返回的 reason code 和对应有界状态工具。
   禁止建议删除或替换状态数据库。
6. 需要读取任一非 Bootstrap 诊断工具时，调用 `flight_surface_status`，再使用当前
   Lead credential 调用 `flight_surface_select` 选择 `DIAGNOSTIC`。禁止选择
   `FULL_COMPAT`；选择失败时只能保留聚合报告，不得直接调用隐藏工具。

## 按用户意图选择一个只读路径

以下词语是本 Skill 内的意图路由，不代表插件存在任意顶层斜杠命令：

- `status`：先调用 `flight_status`，再读取聚合报告；
- `run`：先用 `flight_runs_list` 找回 ID，再用已知 ID 调用 `flight_wave_status`；
- `mailbox`：在 Lead attestation 下调用 `flight_guidance_status`；
- `skills`：在 Lead attestation 下调用 `flight_private_skill_list`；
- `config`：调用 `flight_role_config_explain`，禁止从诊断流程更新配置；
- `workspace`：对已知 Slice、Wave 或 Mission scope 调用 `flight_completion_status`；
- `recovery`：仅当用户明确检查或迁移既有本地状态库时调用 `flight_state_status`。

禁止猜测 ID。必须先从控制面重新发现 Run，再使用返回的 ID。

## 隐私边界

- 禁止粘贴数据库、完整命令输出、源码文件、prompt、Private Skill 正文、capability、
  authorization token、permit nonce、`PLUGIN_DATA` 路径或用户配置路径。
- 本地报告属于用户控制的材料。插件没有上传器；用户选择分享时也只能分享有界结构化
  结果。
- 禁止通过项目外的环境文件搜索“补充”报告。
- 除非用户明确要求并指定安全目的地，否则禁止把诊断保存为文件。
- 禁止声称报告“匿名”；只能准确说明省略了哪些字段。

## 只建议恢复，不执行恢复

`DEGRADED` 时，指出稳定 reason code 和侵入性最低的既有控制面动作。`BLOCKED` 或
`CORRUPT` 时，停止写操作并保留当前数据库与恢复材料。

禁止自动执行：

- 删除或移动 `PLUGIN_DATA`；
- 覆盖活动数据库或选择恢复候选；
- reset、clean、merge、checkout、push 或删除 Git worktree/branch；
- ACK Guidance、revoke Skill、修改角色策略或完成 Gate；
- 创建 issue、发送 telemetry、上传报告或发布包。

以最小、证据充分的恢复边界结束。如果需要法律、产品或用户数据决定，明确指出需要用户
决定，禁止代替用户选择。
