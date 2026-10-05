---
name: flight-control-run
description: 显式暂停、恢复或取消一个受治理 Run 的 exact Mission Controller。仅当用户使用精确命令 `$flight-control-run` 并依次提供 run_id、controller_id、expected_controller_version 与 PAUSE、RESUME 或 CANCEL 时使用；不能把自然语言意图、Lead credential、Controller 的 allowed_next_actions 或历史授权当作本次用户授权。
---

# 控制飞控运行

本 Skill 只执行一次 Controller 生命周期控制。它不修改 MissionSpec、Verification
Manifest、Wave 计划或完成判据，也不允许模型自行决定暂停、恢复或取消。

## 精确命令

用户必须在一个新的 prompt 中只输入：

```text
$flight-control-run <run_id> <controller_id> <expected_controller_version> <PAUSE|RESUME|CANCEL>
```

Hook 只为当前 Project、Host Session、exact Run、Controller、version 和 command 签发短期
一次性 authorization。禁止猜测、构造、复用、记录或向用户展示 token。

## 唯一流程

1. 调用 `flight_surface_status`。当前 Surface 不是 `RUN` 时，只使用当前 Hook 注入的
   Lead credential 调用 `flight_surface_select` 选择 `RUN`；禁止选择 `FULL_COMPAT`。
2. 原样使用 Hook 注入的 `authorization_id`、`authorization_token`、`run_id`、
   `controller_id`、`expected_controller_version` 和 `command`。
3. 只调用一次 `flight_controller_control`。工具不接受调用方提供 `actor` 或
   `reason_code`；服务端固定记录 `user:controller-control` 与
   `USER_EXPLICIT_CONTROL`。禁止加入模型推断或其他审计身份、理由。
4. 成功响应必须包含同一 Controller 的新 canonical state、递增 version 和
   `replayed`。报告该控制结果后停止；不要在同一 turn 继续推进 Run。
5. 如果工具返回 version、state、Host、Surface 或 authorization 不匹配，立即停止。
   下一步只能重新读取状态，并等待用户基于新 ID/version 再次显式调用本 Skill。

## 命令边界

- `PAUSE` 只允许 `RUNNING` Controller；
- `RESUME` 只允许 `PAUSED` 或 `BLOCKED` Controller；
- `CANCEL` 只允许非终态 Controller，且不可逆地终止 Controller 推进；
- 一次 authorization 只能消费一次，且不能换用另一个 command；
- Lead token 只证明当前 Lead 会话，不能替代用户 authorization；
- 禁止直接写数据库、调用隐藏原始控制目标或用旧 receipt 冒充本次控制；
- 禁止顺带执行 `flight_engine_advance`、`flight_action_execute`、Wave、Agent、
  Computer Use、remote Git write、push、PR、发布或任何其他副作用。
