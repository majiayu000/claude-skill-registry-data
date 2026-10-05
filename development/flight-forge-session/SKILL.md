---
name: flight-forge-session
description: 从当前任务、用户指定的 Codex 任务或用户导出的结构化材料中提取可观察事实，并显式熔炼一个项目级 Codex Flight Control Private Skill。仅当用户直接调用 $flight-forge-session 时使用；禁止自动把会话总结成 Skill。
---

# 从会话证据熔炼 Private Skill

这是显式创建命令。`UserPromptSubmit` Hook 必须注入 source kind 为 `SESSION` 的一次性
`forge_authorization_token`。没有该授权时，在读取其他任务或构造 Forge Job 前停止。

1. 调用 `flight_status`；必须满足 `private_skills: true`、持久状态健康并且 Lead
   session 已 attested。
2. 调用 `flight_surface_status`；仅在本轮 `SESSION` authorization 有效时，使用 exact
   Lead credential 调用 `flight_surface_select` 选择 `FORGE`。禁止选择
   `FULL_COMPAT`，也禁止在选择失败后读取其他任务。
3. 只能使用用户选定的一种模式：`CURRENT_TASK`、`SPECIFIED_TASK` 或
   `EXPORTED_ARTIFACT`。
4. 指定任务必须通过宿主支持的 task/thread 读取接口获取。接口不可用时，只能要求用户
   提供结构化导出物。禁止读取 Codex 私有 SQLite、cache、内部状态、transcript JSONL、
   debug dump 或未声明路径。
5. 只构造 `flight_forge_prepare` 接受的有界 `SESSION` capsule：目标、约束、显式决定、
   可观察错误、工具结果、diff 摘要、验证、稳定结果和 Guidance outcome。
6. 排除隐藏思维链、对隐藏推理的重建、secret、个人数据、无证据模型声明和不稳定中间
   猜测。只有被可观察证据支持的事实才能进入来源。
7. 使用注入 token，只调用一次 `flight_forge_prepare`。随后提交一个 trust 为
   `SESSION_OBSERVED` 的候选，并包含狭窄适用范围、前置条件、不变量、禁止动作、有序
   步骤、验证、停止条件、反例、fixtures 和 holdout tags。
8. 只有具备确定性证据时，才按顺序审查到 `SHADOW`。禁止自动把一次普通成功回答变成
   Skill，也禁止在产生该来源观察的同一 Wave 中使用候选。
9. 报告 source mode/digest、不可变 version ID/digest、隐私排除项、lifecycle 和
   评估证据。

如果选定任务无法通过受支持宿主接口读取，也无法安全导出，立即停止。禁止用私有 runtime
文件替代。
