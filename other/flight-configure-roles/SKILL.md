---
name: flight-configure-roles
description: 在用户级或项目级检查、验证、显式设置或显式重置 Codex Flight Control 的角色模型与 reasoning effort 策略。仅当用户直接调用 $flight-configure-roles 时使用；禁止隐式触发，也禁止在普通飞控开发流程中顺便修改配置。
---

# 配置飞控角色模型

这是显式控制命令。`UserPromptSubmit` Hook 应注入一个 `authorization_id` 和一个一次性
`authorization_token`。该授权最多允许一次 `set` 或 `reset`，并不预选 scope、role、
model、reasoning effort 或 fallback 策略。禁止持久化、引用、记录或写入 token。

## 先只读检查

1. 调用 `flight_surface_status`。仅在本轮显式授权有效时，使用 exact Lead credential
   调用 `flight_surface_select` 选择 `ROLE_CONFIG`；禁止选择 `FULL_COMPAT`。
2. 调用 `flight_role_config_explain` 读取当前项目的有效策略。
3. 报告所有受影响角色的有效策略和来源；保留无关角色条目。
4. 只能使用 Host catalog 已验证的 model ID 和 reasoning effort。禁止凭记忆编造
   model slug，也禁止把 catalog 不可用解释为模型可用。
5. 明确说明：`inherit_lead` 使用 Host 默认继承链；显式 override 必须选择
   `on_unavailable: block` 或显式 `inherit_lead` 回退。

如果用户只要求查看或解释配置，在只读结果后停止。不得调用更新工具，也不得消费一次性
授权。

## 验证精确候选

执行显式 `set` 时：

1. 只按用户本轮要求选择 `USER` 或 `PROJECT` scope。
2. 构造一个 schema version 1 的稀疏 overlay，只包含本次目标策略。
3. 调用 `flight_role_config_validate`，并固定 `operation: SET`。
4. 遇到 schema 错误、阻断型 catalog 失败、model/effort 不可用或 `blocked` 说明时，
   立即停止。禁止静默替换其他 model 或 effort。

执行显式 `reset` 时，使用 `operation: RESET` 验证，且不得携带 configuration。
`reset` 只删除选定 override 层，绝不修改插件默认值。

## 只应用一次

仅当以下条件全部成立时，调用 `flight_role_config_update`：

- 用户在本轮明确要求 `set` 或 `reset`；
- Hook 提供当前一次性授权；
- Lead attestation 可用；
- exact scope、operation 和 overlay 已验证；
- `expected_layer_hash` 等于验证结果中的当前哈希；当前层不存在时必须传 `null`。

同一次精确变更重试必须使用稳定幂等键。哈希冲突、授权过期或已消费、恢复任务分歧、
不安全路径或发布失败都是阻断证据。禁止通过 shell 或文件工具直接编辑
`config.json` 绕过控制面。

成功后只报告：

- scope 和 operation；
- 应用后的 layer hash，或 reset 后不存在；
- 合并后的有效配置 hash；
- 哪些角色使用显式 override、Host 继承或显式不可用回退；
- 本次结果是否为幂等重放。

配置变更只影响未来 Run。禁止修改既有 Run 的不可变 role-model policy snapshot，也
禁止修改活动 Wave 的冻结引用。
