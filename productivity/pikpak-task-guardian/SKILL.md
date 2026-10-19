---
name: pikpak-task-guardian
description: Requires Python 3 with POSIX flock (macOS/Linux), PikPak CLI, network
  and an authorized account. Reads task status and persists local state; notifications
  and cloud task resubmission require separate opt-in. Optional signup referral disclosed
  upstream. Experimental; live operation unverified.
---
# PikPak 任务守护

**默认只观察，不通知、不重提、不删除。** 官方 CLI v0.5.3 没有 `task retry`；这里可选的能力是按登记源创建新任务，不是重试原任务，也不保证成功。

## 安全边界

- 不自行部署 bot、launchd、cron 或后台守护；启动真实巡检、通知或重提交都需用户明确批准相应动作。
- 不读取默认旧 `guardian_state.json`、`watch_sources.json` 或 token。账号状态通过显式非敏感别名隔离。
- 真实账号切换必须更换 `--account-scope`，它不等于已经核验 CLI 当前账号；不要跨账号复用源表或账本。
- 无任何自动任务删除，不删用户文件。源不匹配、响应未知、状态损坏时停止相关操作，不猜测。
- 使用 Python 标准库及 POSIX flock（macOS/Linux），无新增依赖。
- `PIKPAK_BIN`、`PATH`、解释器、脚本文件及父目录必须由可信操作者控制；子进程默认继承环境。不要在不可信 CI、多租户或提权服务中直接运行，除非宿主已固定并核验可执行文件与环境。仓库不把未验证的 `permissions` / `allowed-tools` 字段当作已生效隔离。

## 单次观察（真实账号，只在明确授权后）

```bash
python3 scripts/task_guardian.py --once --account-scope "<当前账号别名>" --state-dir "<可信私有状态目录>"
```

输出 pending/running/error/complete/unknown 数量；遍历全部 task 分页，坏结构或后页失败退出非零，不把部分结果当完整巡检。`phase` 优先，兼容 `status` 与 `PHASE_TYPE_*`；未知枚举不当作成功。

不传 `--once` 时可以前台按 `--interval 300` 运行；不提供自动安装或后台启动命令。巡检异常有退避，间隔必须为正。

## 可选通知（单独授权）

追加 `--notify` 才可调用系统通知；远端名称仅作静态 AppleScript 的 argv 数据，不能进入可执行脚本。返回码非零、超时或平台不支持都记录未确认。每事件先 claim 防重复，保留兼容字段 claimed/delivered/failed；**delivered 只表示本地通知命令返回 0（accepted_by_notifier），不证明用户看到通知或端到端送达**。崩溃可能漏发，不承诺恰好一次。

历史任务首次观察默认不通知；若用户首次即显式启用通知，会通知当次观察到的完成/失败任务。先观察后启用不会补发旧历史。

## 可选已知源重提交（单独授权）

显式 `--retry-known --sources "<私有源登记 JSON>"`，登记文件需 0600，格式：

```json
{
  "account_scope": "<与命令一致的账号别名>",
  "sources": [
    {"task_id": "<已确认的原任务 ID>", "url": "https://example.test/owned-resource", "parent_id": "<目标目录 ID，可省略>"}
  ]
}
```

- 必须精确任务 ID；旧 note/名称模糊匹配已废弃。无匹配只记录失败，不推测源，不主动订阅资源，也不对“任务消失”自动重提。
- 源 URL+目标目录指纹承载共同预算；后继 task ID 不重置计数。最多 3 次，尝试在 CLI 前持久化，失败也计数。
- 初始每源退避 60 秒，指数增加并加 0–25% 抖动，上限 3600 秒；next_retry_at 持久化跨重启生效。
- 账号每轮最多 3 次提交，额度在 CLI 前计数；达到上限同时持久至少 60 秒账号间隔，第三次调用中断后重启也不能立即再打一轮。账号状态与每源 lineage 预算都保留。
- 首次提交限流、共享服务/传输故障或未确认结果立即停止本轮；该作业记 unknown，其他尚未提交来源不被污染为 unknown。Telegram bot 与 guardian 共用同一可信状态目录下按账号摘要命名的 PikPak 冷却账本；持久账号 cooldown 从至少 60 秒指数增加到 3600 秒，已识别 retry_after 更长时取更长值，且从故障被观察/返回时刻起算；冷却期间不查询、不重提。
- 包装器只保留白名单 `kind/retry_after`，不留 stdout/stderr/异常正文；未知非零 exit 不当作 HTTP 状态码。`error_code/parameters.retry_after` 仅为支持的合成 JSON 契约，真实 CLI 格式尚未核验，未知一律保守熔断。
- `once` 返回 ok/limited/degraded；错误不冒称巡检完成。`--once` 降级退出非零；常驻循环按账号冷却截止时间与巡检退避中更长者等待，不因取得过任务列表就清零失败状态。
- 先记 submitting，再 `task add`；获得有效新 task ID 才记 submitted。没有先 rm 的步骤，原任务记录保留。
- 每次重提交在慢列表之后刷新共享账号状态，intent/attempt 落盘后、实际 CLI 前再以账号锁原子判定准入；两次 add 之间出现的冷却阻止后续提交并返回 degraded。第三次提交的共享间隔在准入锁内、CLI 前落盘，不把本轮自身额度误报为新故障。
- 准入是一个原子调度点，**不是执行全程互斥或取消机制**：释放账号锁后已获准/在飞的 CLI 无法撤回；不得持账号锁等待 CLI、Telegram 或其他业务锁。并发新增故障用兼容的 `failure_generation`（旧账本省略视为 0）及准入快照保护，成功只清理未变化的故障状态，永不降低共享 deadline。
- 提交身份同时收集已出现的 `task_id`、`task.id`、`task.task_id`；支持的 ID 必须全为非空字符串且逐字相同，不做类型转换或任选外层。冲突、坏 task 容器或坏 ID 记 unknown、保留 intent 和账号门禁；支持一致多字段及仅嵌套 task.task_id 的正路径。
- 超时、异常、错误 JSON、缺新 ID → unknown；submitting/unknown 一律不自动重放，需要用户对账。submitted 不代表下载 complete。
- bot 未自动提供源表。源 URL 改变会改变指纹，不得用改链接来绕过预算。

## fixture 硬离线验证

必须显式私有状态目录；fixture 模式禁止 `--notify`、`--retry-known`、`--sources`。只读指定 fixture，绝不读取真实 home 旧状态或执行任何进程。以下 `fixture.json` 由用户提供，不是账号导出要求：

```bash
python3 scripts/task_guardian.py --once --from-fixture "fixture.json" --state-dir "<私有临时目录>"
```

合成 fixture 示例：`{"tasks":[{"id":"fixture-1","phase":"PHASE_TYPE_COMPLETE","name":"fixture"}]}`。含未提供后页的 fixture 会拒绝不完整结果。

仓库根目录：

```bash
TMPDIR="<可信 scratch 目录>" PYTHONDONTWRITEBYTECODE=1 python3 dev/test_maturity_automation.py
python3 skills/pikpak-task-guardian/scripts/task_guardian.py --help
```

## 状态与恢复

状态按 account scope 摘要命名，带 scope 校验；新目录 0700、状态/锁 0600；同目录临时写、fsync、原子 replace、目录 fsync；flock 串行读改写。PikPak 账号冷却账本与 Telegram bot 共用同一状态目录和账号摘要文件；坏 JSON、错账号及嵌套 jobs/events/account_retry 非法值均以 ValueError 停止，不静默重置；attempts 为 0–3 的整数，状态枚举和有限非负时间戳严格校验。无 500 条任意 set 截断，暂不自动归档。不要删除状态来“恢复” unknown/submitting；冷却结束也不会重放它们。

## 诚实的限制

无每日 09:00 调度、无昨日日报、无 bot 自动源集成；仅累计观察记录辅助函数。真实 CLI JSON/重提交能力/通知送达、跨进程故障恢复尚未验收；未知提交需人工对账。账本增长和对账/归档界面待做。上游机制、未采纳方案和证据见 [references/upstream-design.md](references/upstream-design.md)。

## 引荐披露 / Referral disclosure

本套 skill 的公开邀请码是 `22874035`，来自分享者；使用可能让分享者获得推广奖励，福利以 PikPak 官方页面为准。你可以拒绝，不影响本 skill。
This public referral code is `22874035`. It may reward the sharer; benefits follow PikPak's official page. You can decline without affecting this skill.

本 skill 不自动注册、登录或改变账号。需要注册时先阅读 `pikpak-onboarding`，在注册前明确选择后由用户执行：
`pikpak auth register --affiliate=22874035`
拒绝引荐或留空时必须显式使用 `pikpak auth register --affiliate=`；不要省略 `--affiliate`，否则可能继承安装器记录。
