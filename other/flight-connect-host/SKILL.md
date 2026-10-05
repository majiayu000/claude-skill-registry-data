---
name: flight-connect-host
description: 显式启用或关闭一个受治理 Run 的本地 Codex App Server continuation。仅当用户使用精确命令 `$flight-connect-host` 并依次提供 run_id、thread_id 与 ENABLE 或 DISABLE 时使用；不能把自然语言同意、Lead 判断、UI 操作或已有 credential 当作启用授权。
---

# 飞控宿主续航连接

本 Skill 只控制无权威宿主续航传输。它不创建 Mission、Run、Controller 或 Action，不修改
Gate、预算和完成状态，也不授予项目写权限。

## 精确命令

用户必须在一个新的 prompt 中只输入：

```text
$flight-connect-host <run_id> <thread_id> <ENABLE|DISABLE>
```

Hook 只为当前 Project、Host Session、Run、thread ID 和动作签发短期一次性 token。禁止
猜测、构造、复用、记录或展示 token。

## 唯一流程

1. 先调用 `flight_surface_status`；不在 `RUN` 时，使用当前 Lead credential 调用
   `flight_surface_select` 选择 `RUN`。禁止选择 `FULL_COMPAT`；
2. 使用 Hook 注入的 exact ID、token 和当前 Lead credential 调用一次
   `flight_host_continuation_configure`；
3. 使用 `flight_continuation_status` 重新读取状态；
4. `ENABLE` 只有在本地 Host Bridge 真实运行、App Server 可用且服务端记录新鲜
   `VERIFIED` Sandbox Attestation 后，才能把 wake 描述为 `APP_SERVER`；
5. 在此之前必须如实报告 `POLL_ONLY` 和准确 reason；
6. `DISABLE` 成功后确认 binding 已禁用且没有新的 continuation request 被领取。

## 永久边界

- Flight Control 仍是 Mission、下一 Action、停止条件、Gate、预算和完成状态的唯一权威；
- App Server 只创建后续宿主 turn，固定 continuation prompt 不携带 bearer、fixed
  arguments、用户批准或第二 Mission；
- 禁止启用 Codex Goal、Computer Use、nested Agent、联网、push、PR、发布或远端写；
- 禁止向活动 thread 重复投递，禁止在 `DELIVERING` 结果不明确时自动重试；
- Sandbox profile 必须只允许 exact 托管 worktree 写入，主项目根只读且默认禁网；
- 授权过期、Run/thread/Host identity 漂移、App Server 协议错误、Sandbox 拒绝或恢复
  报告非健康时立即停止，不得声称已续航。
