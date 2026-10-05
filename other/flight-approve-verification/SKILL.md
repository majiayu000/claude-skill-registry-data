---
name: flight-approve-verification
description: 为一个已经创建的受治理 Run，显式批准或拒绝一个指定的 Manual Verification 条目。仅当用户本人针对明确命名的人工门禁作出决定时使用；禁止代替用户调用，也禁止用它替代可由命令验证的证据。
---

# 飞控人工验证

本 Skill 是严格、狭窄的用户权限边界。它不会启动 Run、执行命令、推断用户同意，也不
会一次批准整个 Mission。

【唯一合法语法】

`$flight-approve-verification <run_id> <entry_id> <APPROVE|REJECT>`

`UserPromptSubmit` Hook 注入一次性授权后，严格按以下顺序执行：

1. 调用 `flight_surface_status`。当前 Surface 不是 `RUN` 时，只使用当前 Lead
   credential 调用 `flight_surface_select` 选择 `RUN`；禁止选择 `FULL_COMPAT`。
2. 核对注入的 `run_id`、`entry_id` 和决定与用户本轮输入完全一致。
3. 仅调用一次 `flight_manual_verification_record`。原样传递固定值、注入的
   `project_id`、`host_session_id`、`authorization_token`，再提供简短事实性
   `evidence_summary` 和新的幂等键。
4. 只在当前内存中保留 bearer。禁止把它复制到文件、日志、子代理提示、诊断、本地
   commit 或面向用户的回复。
5. 禁止把 `REJECT` 改成 `APPROVE`，禁止替换条目、重放 token，也禁止把沉默、模型
   置信度或 Lead 判断解释为用户决定。

【停止条件】

如果 Hook 没有注入与本轮输入完全匹配的一次性授权，立即停止。只向用户显示上面的精确
调用语法；禁止调用记录工具，也禁止自行生成授权。

Manual Verification 只适用于确定性宿主执行无法建立的验收事实。格式化、lint、类型、
测试、构建、安全、迁移、恢复、打包等可由命令验证的义务，必须继续使用
`HOST_EXECUTED` 证据。
