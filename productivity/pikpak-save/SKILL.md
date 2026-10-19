---
name: pikpak-save
description: |
  PikPak 手工转存操作卡与离线任务收据检查器：链接提交、按确切 ID 查询、分享选择性恢复。
  用户说存到 PikPak、云下载、保存分享链接时使用。不是有持久账本的一键批量作业系统。
  Use when saving a magnet link, URL or share link into PikPak, or checking the status of a specific task by exact ID. Not a persistent batch job system.
---

# PikPak 转存操作卡

**类型：人工指引 + stdin JSON 检查器。** `-w` 是 CLI 终端观察，不是后台通知/持久自动化。本 skill 没有持久账本、自动去重或自动重试。想要可恢复的单资源管道，用 `pikpak-magnet-pipeline`。

## 1. 账户与输入边界

先确认当前账号归属和用户对“保存到该账号”的授权。未核证稳定官方账号 ID，账号 scope 只能是用户明确声明的非敏感别名；每个 task/share 云操作都重新确认当前账号与本次收据归属，不把 `logged_in: true` 当身份证明。来源不明账号只看 `--help`，不查列表。用户授权后才能 `pikpak auth status -F json`；未登录由用户浏览器登录，不读取凭据。

链接必须是用户有权获取的资源，完整 URL 用安全 argv 传递，不拼 `eval`、不拆空格、不修改原始链接/参数。不承诺所有种子/站点链接都受支持。

## 2. 单次提交，记录确切 ID

```bash
pikpak task add '<用户确认的链接>' -p <folderID> -F json
```

提交前在手工台账记录用户明确声明的非敏感 account scope 别名，并标明 `account_scope_binding=operator_declared_unverified`；这是防误混用的收据字段，不是官方账号身份验证，且本 skill 不会从 `logged_in` 推导它。不指定目录时以服务端实际结果为准，不宣称一定存根目录。随后保存返回 task ID，再跟踪；不要把创建和无限等待混在一起。

**创建不是幂等操作。** 相同链接也不保证服务端去重。超时、断网、退出码非零或缺失 `task_id` 不证明未创建；此时停止，人工对账原始链接、目录、时间和确切任务 ID，不能按同名/首条任务猜测，不能循环 `task add`。重复意图在人工台账中标记“已提交/结果未知”，待确认后才决定是否重新授权一次创建。

```bash
pikpak task get <taskID> -F json
# 在当前 skill 目录下，检查器无网络/CLI 调用：
pikpak task get <taskID> -F json | python3 scripts/inspect_task.py --task-id <taskID>
```

检查器只接受 JSON 对象及明确 task ID；会把顶层与嵌套 `task_id`/`id`/`file_id` 视为同一包络并要求一致，`status`/`phase` 规范化后也必须一致；`ok=false`、`success=false` 或出现 `error` 的显式失败/畸形包络一律拒绝，不输出成功下一步。`pending/running` 给出继续查询；`complete` 必须有有效 file ID；`error` 退出 2；畸形 JSON、缺 ID、错配 ID、未知状态退出 1。错误只给分类，不回显错误正文、URL 或令牌。**这是本地防误配逻辑，不是服务端 JSON schema 已实测的证明。**

人工等待可用 `pikpak task watch <taskID>`（Ctrl+C 只退出观察），或同 ID 有界轮询；约定等待次数/总时长，到期回报仍进行中，不能无限重提。`task ls -s running,pending` 只作概览，默认一页不是全部任务，不能据此判定创建不存在。

确认 `complete` 和匹配 `file_id` 后：

```bash
pikpak play <fileID>
# -o 必须是完整文件路径；先检查路径存在/覆盖风险
pikpak download <fileID> -o ./downloads/confirmed-file.bin
```

多文件 BT/目录不假定 download 会递归；先核对类型，改用批量备份方案。失败不擅自去掉 `-o` 回退当前目录。不要自动 `task rm`；任务记录和云文件不同，尤其不要加 `--delete-files`。

## 3. 分享：先完整预览，再恢复批准的 ID

```bash
pikpak share get <shareID> -F json
pikpak share get <shareID> --token <下一页token> -F json
pikpak share get <shareID> --parent <子目录ID> -F json
# 用户批准确切 file ID 和目标目录后：
pikpak share restore <shareID> -f 'id1,id2' --parent <folderID>
```

- 帮助确认 `--token/-l/--parent`；下一页字段来自实际响应，不能假造。逐页/子目录预览，重复 token 或无法拉全就标“预览不完整”，不以一页预览批准全量恢复。
- 不省略 `-f` 除非用户明确批准完整分享；空 `-f` 表示全部，是范围扩大。
- `-p` 在 share 命令表示提取码（task add 中则是目录）；让用户在自己终端处理，密码可能暴露于历史/进程参数，不记录或复述。无需把提取码提交第三方。
- restore 超时同样可能已生效；先核对原分享、批准 ID、目标目录和恢复历史，不自动再 restore。`share history` 默认一页，必要时用 `--token`，并保留“不完整”标记。
- 恢复后读回目标中批准对象再报成功；不能只凭 CLI 退出 0。此次开发未访问账号，未验证服务端恢复语义。

## 4. 多链接是手工批次，不叫自动队列

先冻结去重后的输入清单（不改链接文本），每项记来源/目录/确认状态/task ID/结果；逐个“提交一次→记录 ID”，成功、失败、未知分开。中断后从台账已知任务 ID 继续查询；未知项不重提，配额或容量错误立即停止本批次。没有台账就不能宣称可恢复。

配额和分享是否计次数以平台当前结果/官方政策为准，不承诺“分享不占次数”或固定免费额度。不收集直链/凭据，任务详情只保留必要 ID 和状态。

来源、固定源码/许可证、发行证据与取舍：[upstream-design](references/upstream-design.md)。rclone 与 cli/cli 的 MIT 和发行记录不代表固定快照/tag 关系已核验，也不证明真实分享恢复能力；仅借鉴机制，不复制或执行上游。

## 引荐披露 / Referral disclosure

本套 skill 的公开邀请码是 `22874035`，来自分享者；使用可能让分享者获得推广奖励，福利以 PikPak 官方页面为准。你可以拒绝，不影响本 skill。
This public referral code is `22874035`. It may reward the sharer; benefits follow PikPak's official page. You can decline without affecting this skill.

本 skill 不自动注册、登录或改变账号。需要注册时先阅读 `pikpak-onboarding`，在注册前明确选择后由用户执行：
`pikpak auth register --affiliate=22874035`
拒绝引荐或留空时必须显式使用 `pikpak auth register --affiliate=`；不要省略 `--affiliate`，否则可能继承安装器记录。
