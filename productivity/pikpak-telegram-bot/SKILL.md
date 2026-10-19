---
name: pikpak-telegram-bot
description: |
  用 Telegram Bot 遥控 PikPak：授权私聊或群内授权发送者提交链接、查询任务与根目录。标准库长轮询，持久 update/message 去重，提交未知不自动重放；部署与发送必须获明确授权。
  Must use when 用户提到 Telegram 遥控 PikPak、TG 机器人存磁力、telegram bot for PikPak、send magnet via Telegram。
  Use when controlling PikPak from Telegram: submit links in an authorized chat or group, query task status and root listing. Long polling with persistent dedup; never auto-replays an unknown submission. Deployment and outbound sends each need explicit authorization.
---

# PikPak Telegram 遥控器

**默认拒绝陌生人；群白名单不等于群内所有人获授权。** 本脚本只有转存和查询，无删除功能。状态采用持久先写记录，宁可留待人工核对，不在重启后盲目重复提交。

## 使用前边界

- 此技能文档不是部署授权。不要自行启动 bot、发 Telegram 消息、改 launchd/cron 或触碰真实账号。
- 只有用户明确批准真实 bot/目标账号/动作后，才运行以下在线命令。`--check` 会真实读取 Telegram updates；`--once` 会真实处理消息，都**不是离线测试**。
- token 只由用户在私有环境中配置；不要要求在聊天里提供，不要放到命令 argv、日志或 Git。脚本无 `--token` 参数。
- Python 标准库、POSIX `fcntl`、已安装 PikPak CLI；支持 macOS/Linux，不宣称原生 Windows 兼容。

## 在线配置（仅经明确授权后）

用户先在 BotFather 自行创建 bot，并自行设置 `TG_BOT_TOKEN`。脚本只从环境变量读取它。`--check` 也必须先设置 `PIKPAK_ACCOUNT_SCOPE` 和可信私有的 `PIKPAK_AUTOMATION_STATE_DIR`，与正常运行保持同一账号/bot 作用域，才能共享持久限流状态。

```bash
python3 scripts/tg_bot.py --check
```

该命令列最近 chat ID；群内发送者 ID 应由用户确认，不能把群 ID 填成用户 ID。

```bash
export PIKPAK_ALLOWED_CHAT_IDS="<私聊或群 chat ID，逗号分隔>"
export PIKPAK_ALLOWED_USER_IDS="<群内允许操作的 user ID，逗号分隔>"
export PIKPAK_ACCOUNT_SCOPE="<当前 CLI 账号的非敏感本地别名>"
export PIKPAK_AUTOMATION_STATE_DIR="<可信私有状态目录>"
python3 scripts/tg_bot.py
```

- 私聊要求 `chat.type=private` 且 `from.id=chat.id`，允许的 chat ID 即本人身份。
- 群须 chat ID 在名单中，且 `from.id` 在 `PIKPAK_ALLOWED_USER_IDS` 中。匿名管理员、`sender_chat`、其他 bot、缺 sender 均拒绝，不回复。
- 群里的查询回复对群成员可见，不只对获准操作者可见；敏感账号宜只用私聊。
- 空 chat 白名单拒绝启动。群 user 白名单为空时群成员都无权操作。
- 换 PikPak 账号必须更换 `PIKPAK_ACCOUNT_SCOPE`；这是操作者声明，不是自动读取认证身份。不得跨账号复制状态文件。
- 可用 `PIKPAK_BIN` 选择 CLI。自定义 `TG_API_BASE` 必须为可信、无凭据的 HTTPS 地址；不要把 token 发给第三方代理。

## 指令

| 消息 | 行为 |
|---|---|
| 磁力/HTTP 链接、`/save <链接>` | 提交到根目录；只有获得有效任务 ID 才回复已开始 |
| `/save <链接> to <文件夹名>` | 根目录文件夹全分页精确查名；重名拒绝猜测 |
| `/tasks` | 展示最多 15 个进行中任务，更多时标明截断 |
| `/status <taskID>` | 查询单任务 |
| `/ls` | 根目录最近 10 条（不是完整目录） |
| `/help`、`/start` | 帮助 |

仅处理 message，不处理 edited_message/channel_post。不要把一条消息编辑成新命令期待执行。

## 持久记录与异常恢复

- 状态文件名按账号别名 + bot 数字 ID 摘要隔离，不保存 token、原始消息或源链接。新目录 0700，状态/锁 0600，同目录临时文件 fsync 后原子替换，POSIX 锁覆盖读改写。
- 先持久 `started`，再调用 CLI；update ID 与 chat/message ID 双键去重；提交确认记录为 `submitted`，提交错误/缺 ID 为 `submission_unknown`，其他处理为 `handled`，异常为 `uncertain`。这些都不等于云下载完成。
- `started/uncertain` **不会自动重放**。提交超时、缺任务 ID、回复失败时，远端是否接受可能未知；用户应自行在 App 核对，不要直接重发或删除账本。
- 状态损坏停止，不静默归零。账本暂不自动清理，避免随意截断后旧消息再执行。
- PikPak `task add` 非零退出、超时或未知结果会写入与 task guardian 共用的账号级持久冷却账本（同一可信状态目录、同一账号别名对应同一文件；不与 Telegram transport 冷却混用），立即停止当前 update 批次；后续 update 不领取、不写 receipt、不推进 offset。`--once` 对此降级返回非零，重启/更换同账号 bot 也不会绕过；未知结果不按 exit code 猜 HTTP 状态，不自动重放。冷却从失败被观察/返回时刻起算，慢 CLI 不提前起算。
- 目录查找和“正在请求”回复结束后，在实际 add 前以共享账号锁刷新并原子判定准入；新冷却阻止 CLI，已领取 receipt 保留为 submission_unknown，不自动重放，也不宣称提交成功。
- 原子准入不是执行全程串行或远程取消：放锁后已获准/在飞的调用无法撤回。锁顺序只允许 update/guardian 业务锁到账号锁，不持账号锁等待 Telegram、CLI 或另一业务锁。成功按准入快照与兼容的 failure_generation 合并，调用期间的新故障即使计数已饱和也不清零，任何共享 deadline 都不降低；旧账本无代际字段仍可读。
- `task_id`、`task.id`、`task.task_id` 中已出现的值必须全为非空字符串且逐字一致；未知 task 容器、坏 ID 或冲突结果留 submission_unknown 收据并进入账号门禁，不猜任务身份。仅嵌套 task.task_id 与多字段一致均可确认 submitted。
- `getUpdates/sendMessage` 共用独立的 `.transport.json` 及锁，持久 `cooldown_until/failures/fatal`；429 尊重有效 retry_after（缺失时至少 60 秒），其他瞬态故障有上限指数退避。冷却中所有 Telegram 方法均不发请求；重启/更换同 bot token 不绕过冷却。
- 回复发生限流、传输或未知结果错误时，立即停止领取同批后续 update，未领取消息不写 receipt、不推进 offset。已领取消息留待核对，绝不重放 CLI。HTTP/JSON 401/403/409 持久停止，`--once` 遇降级退出非零。
- 永久错误需操作者停止其他实例、修复 token/权限/冲突并核对后，才在备份状态后人工清除**仅传输文件**中的 `fatal`；保留冷却截止时间及完整 update/message 账本，不删除整个状态目录。
- 日志不输出原始消息、HTTP body、URL 或异常正文。不会把 traceback/完整 update 发给开发者。

### 空闲序列阻塞与人工恢复

Telegram 官方允许至少一周无新 update 后随机选取下一 ID。持久 `last_observed_at/idle_resync_seconds/epoch/resync_required`，优先使用 update 内可信的服务端生成时间；未知时间保留最多 24 小时积压余量，重复消息和空轮询不把边界推进到本机 now。达到一周减 45 秒（长轮询/请求窗口余量）的阈值时停止旧高 offset。旧账本缺观察时间、时钟回退或未领取的低 ID 冲突也 fail closed，不能靠任意降低 offset 继续。离线测试的合成时间字段不等于真实 Telegram 账号实测。

恢复步骤（涉及真实轮询，必须另获明确授权）：

1. 停止该 bot 的其他实例；备份可信私有目录中的全部账本，保持相同账号别名与 bot 数字 ID。不得删除 receipts/messages 或复用到其他账号。
2. 保留相同的私有环境变量，运行 `python3 scripts/tg_bot.py --resync`。它只做一次**不带 offset** 的 `getUpdates`，不发送消息、不调用 PikPak；仍尊重传输冷却/fatal。非阻塞的活跃序列拒绝该操作。
3. 仅在返回有效、非空 pending updates 时，以其中最小 ID 建立新 epoch；不领取业务，保留所有旧 update receipt 与 chat/message 去重账本。空结果、坏结构或网络失败保持阻塞，不假装恢复；必要时由操作者授权后自行发送一条无业务的 `/help` 再重试。
4. 人工核对 `started/uncertain/submission_unknown` 后，正常启动或运行 `--once`。下一轮从新序列读取，旧 chat/message 不重放。此过程不能找回 Telegram 已过期或此前被其他实例确认的消息。

`/ls` 只有显式 `files: []` 且无后页才称空；缺字段、非数组/非对象记录或非字符串 token 均回复查询未确认，空页带 token 不等于空目录。

## 离线开发验证

仓库根目录运行：

```bash
TMPDIR="<可信 scratch 目录>" PYTHONDONTWRITEBYTECODE=1 python3 dev/test_maturity_automation.py
python3 skills/pikpak-telegram-bot/scripts/tg_bot.py --help
```

测试入口在导入被测模块前同时启用共享 `offline_environment` 和底层 run/Popen、socket、urlopen、通知与真实 home 硬封锁；局部 mock 只能返回合成结果。测试保留授权、去重、未知提交不重放等原有覆盖，新增整批与 main 调度、账号级持久冷却、服务端生成时间边界、空闲阻塞→人工重同步→低 ID 处理及实际 CLI 包装器 schema 回归。不要用在线 `--once/--check/--resync` 代替离线验证。

## 尚未承诺

没有完成自动推送、没有与 guardian 自动共享来源，也不承诺业务恰好一次；空闲恢复仅实现明确阻塞加人工 `--resync`，**不是静默自动恢复**。真实 CLI JSON 字段、Telegram 长轮询/限流和重同步、跨进程断电恢复与账本归档仍待独立授权验收。上游研读、许可证和发行证据见 [references/upstream-design.md](references/upstream-design.md)。

## 引荐披露 / Referral disclosure

本套 skill 的公开邀请码是 `22874035`，来自分享者；使用可能让分享者获得推广奖励，福利以 PikPak 官方页面为准。你可以拒绝，不影响本 skill。
This public referral code is `22874035`. It may reward the sharer; benefits follow PikPak's official page. You can decline without affecting this skill.

本 skill 不自动注册、登录或改变账号。需要注册时先阅读 `pikpak-onboarding`，在注册前明确选择后由用户执行：
`pikpak auth register --affiliate=22874035`
拒绝引荐或留空时必须显式使用 `pikpak auth register --affiliate=`；不要省略 `--affiliate`，否则可能继承安装器记录。
