# Telegram bot：上游设计证据与落地

核验日期：2026-10-16；本项目基线 `7275712d26df7f6a0853b63344278e54732c111e`。只读公开源码/官方文档；未安装或运行第三方代码。

## 成熟方案与直接证据

- [python-telegram-bot/python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)，GitHub 公共 API 实测 29,518 stars，最近 push `2026-10-11T05:56:32Z`；固定研读提交 `577e9c784607a42ff17746b9864b6416c3c30593`，不是同名 fork。
- [`src/telegram/ext/filters.py`](https://github.com/python-telegram-bot/python-telegram-bot/blob/577e9c784607a42ff17746b9864b6416c3c30593/src/telegram/ext/filters.py#L818-L825)：`Chat` 检查聊天，而 [`User`](https://github.com/python-telegram-bot/python-telegram-bot/blob/577e9c784607a42ff17746b9864b6416c3c30593/src/telegram/ext/filters.py#L2931-L2966) 检查 `message.from_user`；两者不是同一种授权。官方 [Message.sender_chat](https://core.telegram.org/bots/api#message) 明确匿名管理员等消息可能带假 `from`。
- [`_updater.py:338-366`](https://github.com/python-telegram-bot/python-telegram-bot/blob/577e9c784607a42ff17746b9864b6416c3c30593/src/telegram/ext/_updater.py#L338-L366)：传入 `_last_update_id` 拉取 updates，入队后设最后 ID + 1。它是传输层确认，不保证业务副作用恰好一次；此处不能直接照抄为磁力任务幂等。
- 官方 [getUpdates](https://core.telegram.org/bots/api#getupdates)：offset 高于 update_id 时确认旧 update；重复 update 应去重；空闲一周后新 ID 可随机选择。`allowed_updates` 不会清除旧类型。
- [`_utils/networkloop.py`](https://github.com/python-telegram-bot/python-telegram-bot/blob/577e9c784607a42ff17746b9864b6416c3c30593/src/telegram/ext/_utils/networkloop.py)：`RetryAfter` 尊重服务器等待、`InvalidToken` 停止、其他错误有上限退避；不应把永久认证错误当普通瞬态故障。
- [`examples/errorhandlerbot.py:20-21`](https://github.com/python-telegram-bot/python-telegram-bot/blob/577e9c784607a42ff17746b9864b6416c3c30593/examples/errorhandlerbot.py#L20-L21)：调高 httpx 日志级别，避免记录每个 GET/POST。示例的 traceback/完整 update 外发**未采纳**：本项目的异常正文、请求 URL、签名链接可能带秘密，且未获得开发者通知授权。

## 许可证与正式发行边界

- 固定提交 [`pyproject.toml:12-13`](https://github.com/python-telegram-bot/python-telegram-bot/blob/577e9c784607a42ff17746b9864b6416c3c30593/pyproject.toml#L12-L13) 声明 **LGPL-3.0-only**，license-files 为 LICENSE / LICENSE.dual / LICENSE.lesser。已只读核验 [`LICENSE.lesser`](https://github.com/python-telegram-bot/python-telegram-bot/blob/577e9c784607a42ff17746b9864b6416c3c30593/LICENSE.lesser)（LGPL v3）及 [`LICENSE`](https://github.com/python-telegram-bot/python-telegram-bot/blob/577e9c784607a42ff17746b9864b6416c3c30593/LICENSE)（被 LGPL 纳入的 GPL v3 正文）；不能仅因 LICENSE 的 GPL 标题把整个项目误判为 GPL-only。LICENSE.dual 的具体适用条款未在此独立核验，不猜测例外授权。
- 已只读核对公开正式发行元数据：[v22.8](https://github.com/python-telegram-bot/python-telegram-bot/releases/tag/v22.8)，以及端点 `GET /repos/python-telegram-bot/python-telegram-bot/releases/latest`（以纯文本记录，文档不含可点击的外部 API 链接，运行时也不发起该请求）。这不是研读 snapshot 与 tag 的祖先关系证明：**祖先关系、发行制品及运行兼容性未核验**，不把 snapshot 当作该 release。
- 本项目只借鉴授权/调度/去重机制，未安装或运行 PTB；若将来复制或分发上游代码，须另核完整许可证及文件级条件。Celery 的代码 BSD-3-Clause / 文档 CC BY-SA 4.0 证据见 guardian 的对应 references，不将“开源”视为无条件复制授权。

## 采纳 / 不采纳 / 实际落地

| 议题 | 选择与理由 | 代码与验证 |
|---|---|---|
| 发送者授权 | 采纳 chat 与 user 分离；私聊须 `from.id == chat.id`，群须额外 `PIKPAK_ALLOWED_USER_IDS`，缺 sender、bot、`sender_chat` 静默拒绝 | `process_message`；陌生成员、匿名、缺 sender 回归 |
| 更新确认与幂等 | 持久 offset + update ID + chat/message ID 双键；锁内原子写 `started` 后才调用 CLI；区分 `submitted/submission_unknown/uncertain`，未知永不自动重放 | `UpdateStore` / `process_updates`；同批/跨重启/不同 update 的同一消息、回复异常、落盘失败及同进程双线程竞争回归 |
| 异常与调度边界 | 所有 Telegram 方法共享持久 cooldown/fatal；发送 429/永久错误立即停批，未领取 update 不推进 offset；HTTP 200 的错误/未知结果也退避，不打印秘密 | `Telegram._call` / `TransportStore` / `process_updates` / `main`；整批、轮询/发送共用冷却、重启和 main 回归 |
| 空闲新序列 | 超过空闲阈值、旧账本无观察时间或低 ID 冲突先 fail closed；人工 `--resync` 无 offset 读取有效 pending 后才建立新 epoch，保留 chat/message 账本，不自动执行业务 | `UpdateStore.prepare_poll` / `resynchronize`；跨周阻塞→人工恢复→低 ID 完整循环，空响应不解锁 |
| 成功与送达 | 请求前仅称“正在请求”；CLI 错误 JSON、缺任务 ID 不称成功；sendMessage 必须返回 message_id，否则抛安全异常并留 uncertain receipt | `pikpak_json` / `handle_save` / `Telegram.send` |
| 目录完整性 | 查名遍历 `--token`，循环/重名拒绝；`/ls` 严格验证 files 数组、记录对象与 token，只有显式空数组且无后页才称空；任务/文件截断明确说明 | `find_folder_id` / `handle_tasks` / `handle_ls`；实际 subprocess→pikpak→pikpak_json→handle_ls 的未知 schema 回归 |
| 状态 | 按账号别名 + bot 数字 ID 的 SHA-256 命名；bot token 轮换不重置同一 bot 状态；文件 0600、新目录 0700、fsync + replace + 目录 fsync、POSIX flock；损坏不默默清空 | `UpdateStore`；账号隔离、损坏拒绝、落盘故障测试 |
| 框架依赖 | 不新增 PTB/httpx/Celery；只借鉴机制，维持标准库部署 | 未安装依赖、未运行上游代码 |

## 官方 CLI --help 契约（先前帮助证据，本轮未执行 CLI）

先前保存的帮助/版本证据为 `pikpak --version` = `v0.5.3`；本轮修复未运行任何 PikPak 命令，以下不代表重新实测。

- `task add <url> [-p/--parent <id>] [-F json]` 存在；没有幂等键参数。
- `task ls -s/--phase pending/running/error/complete`、`task get <taskID>` 存在。
- `ls --type folder --token <page-token>` 存在。
- bot 自己的 `--help` **没有 `--token`**；已移除文档的不存在参数，token 仅环境变量传入。
- [官方 CLI 页面](https://mypikpak.com/cli) → [官方帮助](https://mypikpak.com/en-US/help-center/connected_apps/pikpak_cli)。帮助参数不能证明 JSON 响应字段；`task_id`、嵌套 `task.id`、`next_page_token` 仅由合成契约测试覆盖，真实账号响应尚待另行授权核验。

## 验证与待验

共享账号调度补充：领取 update 时的检查不足以覆盖慢目录查询和 Telegram ACK；必须在最终 task add 边界重新以共享账号锁判定准入。已持久 started 的消息若准入被新冷却拒绝，保留 submission_unknown 而不重放。账号锁释放后才能运行 CLI/Telegram；准入是线性化调度点，不是撤回已获准或已在飞调用的承诺。成功仅在准入快照完全未变时清旧故障，failure_generation 兼容旧账本省略值 0，失败写入递增且不依赖有上限的 failures；未来 deadline 永不降低。回归以另一组件在慢 ACK/慢目录及 CLI 内写故障的确定性交错验证，另保留单 ID、多字段一致、仅 task.task_id 正例；冲突/坏型保留未知收据并门禁。可复用方法见 guardian 对应 references，所有交错均在硬离线门禁内完成。

独立运行：先将 `TMPDIR` 指向可信 scratch，再运行 `PYTHONDONTWRITEBYTECODE=1 python3 dev/test_maturity_automation.py`。入口和导入式 unittest 均在被测模块导入前启用 `offline_environment` 及 run/Popen/socket/urlopen/home 硬封锁；通知仅返回合成结果。全部消息、任务、token 和磁盘状态均为合成私有数据，不执行真实 CLI/Telegram/通知。

已离线覆盖：轮询/发送共享持久冷却、发送故障立即停批、未领取 offset 不推进、main 等待/停止；空闲阻塞与人工重同步完整低 ID 循环，空/坏 pending 保持阻塞；实际底层包装器的目录 schema。恢复是明确的 fail-closed 人工入口，不是自动恢复承诺。

仍需单独验收：真实 CLI JSON 契约；真实 Telegram 429、长轮询/重同步；跨进程崩溃/断电恢复；状态账本归档增长；无自动业务重放，也无“恰好一次”承诺；没有完成通知或与 guardian 自动共享来源。账号别名是操作者声明，不是已认证账号识别。状态目录须可信且私有；此实现不宣称抵御同用户恶意进程。
