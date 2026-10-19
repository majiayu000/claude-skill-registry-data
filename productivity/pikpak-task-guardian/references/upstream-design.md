# Task guardian：上游设计证据与落地

核验日期：2026-10-16；基线 `7275712d26df7f6a0853b63344278e54732c111e`。只读公开 GitHub 与 Telegram/PikPak 官方资料，不安装依赖、不运行上游代码。

## 成熟方案与证据

- [celery/celery](https://github.com/celery/celery)，GitHub 公共 API 实测 28,989 stars，最近 push `2026-10-15T22:13:14Z`；固定提交 `ef37e616ef6726a2e08126635c000f3eacffcbc2`。
- [`celery/utils/time.py::get_exponential_backoff_interval`](https://github.com/celery/celery/blob/ef37e616ef6726a2e08126635c000f3eacffcbc2/celery/utils/time.py)：`min(maximum, factor * 2 ** retries)`，可 full jitter；说明退避有上界，避免所有任务同步重试。这里采纳有上界指数退避与抖动，不照搬允许 0 秒的 full jitter，防止即时重提。
- [`celery/app/autoretry.py`](https://github.com/celery/celery/blob/ef37e616ef6726a2e08126635c000f3eacffcbc2/celery/app/autoretry.py)：区分 `autoretry_for` / `dont_autoretry_for`，维护 request.retries 与 max_retries；重试不是所有异常一视同仁。这里只对用户精确登记且结果可确认的来源推进；提交未知直接停机待对账，不拿 backoff 掩盖重复副作用。
- [python-telegram-bot `_utils/networkloop.py`](https://github.com/python-telegram-bot/python-telegram-bot/blob/577e9c784607a42ff17746b9864b6416c3c30593/src/telegram/ext/_utils/networkloop.py)：永久 InvalidToken 不应无穷重试，瞬态故障按有界间隔重试。采纳巡检失败退避与业务提交异常隔离；不引入 PTB 异步框架。
- [PikPak 官方 CLI](https://mypikpak.com/cli) / [CLI 官方帮助](https://mypikpak.com/en-US/help-center/connected_apps/pikpak_cli)：官方入口可核对安装/能力。JSON 细节以单独授权后的实际结构为准，不从第三方 SDK 推断为官方契约。

## 许可证与正式发行边界

- 已只读完整核验固定提交 [`LICENSE`](https://github.com/celery/celery/blob/ef37e616ef6726a2e08126635c000f3eacffcbc2/LICENSE)：**代码 BSD-3-Clause**；源码再分发须保留版权、条件和免责声明，二进制发行须在随附材料保留，不得借作者/贡献者姓名背书。其 docs 渲染内容单独为 **CC BY-SA 4.0**；不能把代码许可证套到文档。
- 已只读核对正式发行元数据：[Celery v5.6.3](https://github.com/celery/celery/releases/tag/v5.6.3)，以及端点 `GET /repos/celery/celery/releases/latest`。**所研读 snapshot 与 tag 的祖先关系、发行制品及运行行为未核验**；此处不把 snapshot 冒充 release。
- 引用的 PTB 固定提交由 [`pyproject.toml:12-13`](https://github.com/python-telegram-bot/python-telegram-bot/blob/577e9c784607a42ff17746b9864b6416c3c30593/pyproject.toml#L12-L13) 明示 **LGPL-3.0-only**，并列出 LICENSE / LICENSE.dual / LICENSE.lesser；已读 [`LICENSE.lesser`](https://github.com/python-telegram-bot/python-telegram-bot/blob/577e9c784607a42ff17746b9864b6416c3c30593/LICENSE.lesser)。不能因 LICENSE 含 GPL v3 正文就误判整个 PTB 为 GPL-only；LICENSE.dual 的例外适用性未独立核验，不猜。
- PTB 正式发行元数据为 [v22.8](https://github.com/python-telegram-bot/python-telegram-bot/releases/tag/v22.8)（端点 `GET /repos/python-telegram-bot/python-telegram-bot/releases/latest`）；同样未核验 snapshot/tag 祖先关系或发行运行。仅借鉴机制、未安装运行上游；若将来复用代码或文档，需另核完整许可与文件级条件。

上述 GitHub API 端点以纯文本记录，文档不含可点击的外部 API 链接，运行时也不会按这些端点发起请求；它们是取证时人工读取的地址记录。

## 官方本机 CLI 帮助证据

以下沿用先前 `--help` / `--version` 证据（`v0.5.3`）；本轮修复未运行任何 PikPak 命令，不代表重新实测。

本 skill 只调用只读查询类子命令（任务状态与列表）。帮助文本中出现的其他子命令仅作为能力边界记录，**本 skill 不构造、不预览、不执行任何删除类调用**：

```text
只读查询（本 skill 实际使用）:
  task ls    -l/--limit, -s/--phase (pending/running/error/complete), --token
  task get   <task-id>
  task watch <task-id>

仅作边界记录（本 skill 不使用）:
  task add   订阅新的远端任务
  task 管理  移除任务记录；该子命令存在一个可选开关，可在移除记录的同时删除关联云端文件
```

本 skill 的源码回归（`test_guardian_no_file_ops`）逐字断言 `task_guardian.py` 中不出现删除类参数，因此上表的边界记录不会转化为运行时能力。

`task retry` **不在子命令表中**。尝试 `task retry --help` 会落回父帮助且退出 0，故“help 成功”不等于该命令存在。删除任务记录和删除关联文件也不是一件事；基线没传 `--delete-files`，不能声称它会删云文件。本次直接移除所有自动 `task rm`，保留原任务记录。

## 采纳与实际落地

| 主题 | 采纳理由及实现 | 离线验证 |
|---|---|---|
| 原生重试 vs 重提交 | 无原生 retry，不假装支持；默认只观察，`--retry-known --sources` 才启用精确 ID 映射的 `task add` 重提交；绝不按名称模糊匹配，也不先删后加 | 无映射/仅 note 不执行；相同源后继 ID 共享预算 |
| 预算与状态机 | 作业键为 URL+目标父目录指纹，账号在状态外层隔离；`submitting → submitted/unknown`，attempts 在 CLI 前持久化；最多 3 次，失败也消耗预算。`unknown/submitting` 不重放 | 超时未知不重提；新任务 ID 不重置额度；持久化快照先于调用 |
| 退避与账号调度 | 保留每源 60 秒指数/抖动 next_retry_at；每账号每轮最多 3 次，达到上限在 CLI 前持久 60 秒间隔；首次未确认提交立即停本轮并持久账号 cooldown，不把其他源污染为 unknown | 多源限流/服务/传输/unknown 故障、跨 once 重读、第三次中断前已落盘、main 等待和非零退出 |
| 故障真实性 | 只保留白名单 kind/retry_after，未知 exit 不推断 HTTP；once 区分 ok/limited/degraded，主循环不因查到列表清零提交故障 | 实际底层 subprocess 包装器回归；合成契约不冒充真实 CLI schema |
| 枚举 | 优先 phase，兼容 status；仅 pending/running/error/complete 与对应 PHASE_TYPE_ 前缀；其他 unknown，不猜成功 | PHASE_TYPE_COMPLETE 与 Complete 合成输入覆盖；真实返回字段待验 |
| 分页 | 遍历 --token，ID 去重；循环/坏结构/缺 ID/后页失败不返回伪完整列表 | 两页、重复 token、错误结构测试 |
| 通知代码/数据隔离 | 静态 AppleScript `on run argv`，任务名只作 argv；限制长度；非零/超时为 False；兼容字段 delivered 仅指 accepted_by_notifier，不证明 UI 送达 | 恶意名字不进入 -e，非零不视为命令成功；无真实 osascript |
| fixture 硬离线 | CLI 必须显式 --state-dir；禁止 sources/notify/retry 开关；库层即便开关传 True 也绝不执行 CLI/通知；不读默认 home 旧状态或 watch 源 | subprocess 硬拦截；fixture 加失败源也无调用 |
| 状态事务 | 账号 scope 校验、私有新目录/0600 临时文件、fsync/replace/目录 fsync，flock 覆盖读改写；损坏拒绝，不盲目重置去重 | 账号错配、坏 JSON、replace 失败保留旧文件、重复观察 |
| 产品承诺纠偏 | 不宣称已经实现每日 09:00 昨日报表、watch 消失自动重提、bot 来源共享；daily_report 只保留“累计观察”辅助函数 | 文档已删除不存在承诺 |

## 不采纳与理由

### 共享调度闭环回归方法

先在 `dev/test_maturity_automation.py` 的硬离线封锁内，于底层合成 CLI 的慢 ls、两次 add 间持久化、提交 intent 的 fsync 及 add 执行期间注入另一组件的共享故障，观察实际调用数与磁盘收据；每个缺陷先保存真实 RED 再做最小 GREEN，保留正常提交、默认观察、每源预算和本轮三次额度正例。账号锁只覆盖最终准入/共享预算及结果合并，绝不跨外部调用持有，避免另一组件写故障时死锁。准入后故障不能取消在飞调用；结果合并必须保留故障代际变化与未来 deadline。旧 schema 无 failure_generation 视作 0；两种写入者都递增代际，饱和计数不作版本号。冲突 task_id/task.id/task.task_id 是 unknown 而不是任选字段。此处均为合成离线交错，不宣称真实多进程/断电验证。

- 不安装 Celery、broker、数据库或后台托管：两项脚本规模不需要分布式队列，且用户禁止新依赖/部署。
- 不自动重试所有 CLI 非零/超时：无幂等键时无法证明远端未接受；最安全是持久 unknown 并人工对账。
- 不从未登记 task 名字猜原链接、不删旧任务、不读取真实账号探测 source：错误源比少自动化更危险。
- 不把通知失败降级日志叫“成功”；不伪造昨日日报。

## 验证与待验

运行前将 `TMPDIR` 指向可信 scratch，再执行 `PYTHONDONTWRITEBYTECODE=1 python3 dev/test_maturity_automation.py`。入口在导入被测模块之前启用共享 `offline_environment`，额外直接替换 run/Popen/socket/urlopen/home（不受 patch.stopall 撤销）；仅用合成返回替换指定调用，通知不实际发送。保留既有 39 项覆盖，新增账号每轮上限、持久账号冷却、首次共享故障停批、main 降级和嵌套账本 schema 回归。

待验：官方真实 JSON 枚举/分页/提交 ID/故障 envelope；真实限流行为与可用性；进程 kill/断电与多进程竞争；人工对账工作流；源链接变更后的预算政策；账本归档；真实通知送达。通知采用先 claim 防重，崩溃时可能漏发，不是恰好一次；delivered 只证明命令返回 0。账号别名不能自动识别 CLI 已换账号；状态目录必须可信私有。未部署 launchd/cron/bot。
