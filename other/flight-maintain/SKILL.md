---
name: flight-maintain
description: 显式授权一个已经由 Codex Flight Control 封存、用户可见且 hash 精确匹配的本地维护计划。仅当用户原样输入 `$flight-maintain` 并依次提供 plan_id 与 plan_hash 时使用；不能用自然语言同意、模型判断或 UI 点击替代。
---

# 飞控显式维护

本 Skill 只授权一个既有不可变 Maintenance Plan。它不能扫描新目标、增加 item、扩大
item kind，也不能替用户决定删除什么。

## 必须先满足

1. `flight_maintenance_plan` 已返回 `SEALED` plan；
2. 用户已经阅读 plan 中每个 item 的 kind、聚合身份、owner proof、precondition hash、
   target summary 和可恢复性；
3. 用户在新的 prompt 中只输入：

```text
$flight-maintain <plan_id> <64位plan_hash>
```

Hook 只为 exact Project、Host Session、plan/hash 和已有 item kind 签发一个短期一次性
token。禁止构造、复用、记录或展示 token。

## 唯一流程

1. 使用 Hook 注入的身份调用 `flight_maintenance_status`；
2. 调用 `flight_surface_status`；只有当前 plan 授权仍有效时，才使用 exact Lead
   credential 调用 `flight_surface_select` 选择 `MAINTENANCE`。禁止选择
   `FULL_COMPAT`；
3. 只有 plan 仍为 `AUTHORIZED`、hash 完全相同且 item 没有漂移时，调用一次
   `flight_maintenance_apply`；
4. 逐项阅读服务端结果；
5. 只有 plan 为 `VERIFIED` 且全部 item 都是 `APPLIED`，才能报告维护完成；
6. `PARTIAL`、`BLOCKED`、`FAILED` 或 `APPLYING` 必须如实停止并保留现场。

## 永久禁止

- 自动运行维护；
- `rm -rf`、Git `--force`、`reset`、`clean` 或猜测路径；
- 删除或移动 `main`、用户分支、当前主工作区、dirty worktree 或 remote ref；
- push、PR、发布、fetch 或任何远端写；
- 更换 plan/hash、增加 item、跳过前置条件或把模型/UI 行为当作用户授权；
- 在文件、日志、消息、子代理任务或最终回复中暴露授权 token。

维护事务只能处理服务端重新证明由插件拥有的 exact 本地资产。任何 identity、路径、ref、
commit、clean 状态、Host Session 或 TTL 漂移都必须失败关闭。
