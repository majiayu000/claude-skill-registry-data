---
name: pikpak-magnet-pipeline
description: |
  PikPak 单资源持久分步管道：一次创建、按任务 ID 查询、单文件落盘收据、人工核验后仅打印清理建议。
  适用于磁力/链接到本地及临时云副本。目录型 BT、无人值守删除和服务端 exactly-once 不在实现范围。
  Use when downloading one magnet or link from PikPak to local disk in explicit steps, then deciding what to clean up in the cloud. One resource, one state file, one receipt; folder BT, unattended deletion and exactly-once are out of scope.
---

# PikPak 单资源管道

**语言 / Language**: 本 skill 的说明、帮助文本与错误信息以简体中文为主，面向中文用户；这是有意的区域定位，不是强制。仓库同时提供英文 README（`README.en.md`），英文用户可据此了解全部能力边界；脚本的机器可读输出（`--json`、`-F json`）与退出码不依赖语言，可直接被其他语言的调用方解析。如需其他语言的支持，请以机器可读输出为准，不要把中文提示文本作为程序接口。

This skill's documentation, help text and error messages are primarily Simplified Chinese and target a Chinese-speaking audience by design. English readers can use `README.en.md` for the full capability and limitation overview. Machine-readable output (`--json`, `-F json`) and exit codes are language-independent and are the supported interface for non-Chinese callers.

本地执行器，不是“来去无痕迹”服务。**一项资源一个 --state 文件**；同一状态文件记录来源指纹→task ID→file ID→本地路径/大小/SHA-256，并记录非敏感 `account scope` 别名、`account_scope_binding=operator_declared_unverified` 和当前登录身份的域隔离 SHA-256。别名只是操作者声明，不是身份验证；脚本只接受 `auth status -F json` 白名单位置中的稳定账号 ID，缺失或冲突就停止，不回显或保存原值。正式 CLI 的实际 JSON 字段尚未按真实账号验收确认，中性假 CLI 不代表实盘兼容。

## 本地执行环境与文案边界

`PIKPAK_BIN`、`PATH`、Python 解释器、脚本文件及其父目录必须由当前操作者控制；子进程默认继承环境。不要在不可信 CI、多租户或提权服务中直接运行，除非宿主已固定并核验可执行文件与环境。仓库不假称 `permissions` / `allowed-tools` 等 frontmatter 字段会被所有宿主强制执行；实际最小权限由部署宿主负责。

命令帮助和错误摘要可能是中文；这是当前 CLI 适配器的文案事实，不代表强制用户语言。Agent 应按用户语言解释结构化结果，不应为降低扫描告警而删除安全校验或伪造国际化。

## 使用前

先取得用户对当前本人账号、资源、目标目录、云写入与本地下载的明确授权。`--account-scope <别名>` 只记录操作者声明；step1/2/3/4 每次都必须显式传入与收据相同的别名，并重新读取当前登录身份哈希，缺失、旧收据缺身份收据、不一致或 `logged_in` 但没有稳定 ID 都拒绝。来源不明账号不查询。脚本每一步都会运行 `auth status -F json`；没有账号授权或 CLI 未返回受支持的稳定 ID 时不要启动。`--help` 不访问账号。注册/安装由用户自己完成。

以下命令从本 skill 目录运行；所有步骤保持同一个状态文件。链接是用户确认的合法来源，不提供未核验演示 magnet。

```bash
python3 scripts/magnet_pipeline.py step1-add '<授权链接>' --account-scope <当前账号别名> --state ./job-1.json
# 可加 --folder <folderID>；本 CLI 不支持 add 改名，已删除无效 --name
python3 scripts/magnet_pipeline.py step2-status <返回的taskID> --account-scope <同一账号别名> --state ./job-1.json
python3 scripts/magnet_pipeline.py step3-download <确认的fileID> --dest ./downloads --account-scope <同一账号别名> --state ./job-1.json
# 只有用户确认本地内容正确后才加此标记；仍然不执行任何删除
python3 scripts/magnet_pipeline.py step4-cleanup <同一fileID> --verified-local --account-scope <同一账号别名> --state ./job-1.json
```

## 可验证状态与故障出口

| 状态/情形 | 行为与恢复 |
|---|---|
| 首次 add | 调用前原子记录 submitting；返回有效 ID 才记 submitted |
| 相同链接+目录再 add | 复用已记录 task ID，不发第二次创建 |
| 换链接/目录却复用 state | 拒绝；新资源请显式选择新状态文件 |
| add 超时/退出码异常/响应缺 ID | 保留 submitting；可能已经创建，禁止盲目再 add |
| status | state 必须已有完整 fingerprint/目录/有效 task ID/account scope 且与请求严格一致；缺 ID 在 task get 前拒绝，不自动认领；响应中外层/嵌套 `task_id`/`id`/`file_id` 若冲突、`status`/`phase` 规范化后冲突、字段畸形或显式 `ok=false`/`success=false`/`error` 均失败；旧 ready/downloaded 收据遇此类观察会安全撤销为 blocked，保留本地收据但不能继续下载/清理 |
| task get 超时/查询失败 | CLI 超时以退出分类 124 返回给 step2；旧 ready/downloaded 撤销为 blocked，移除 latest_task_status=complete，记录 query_failure；保留来源/目录/账号/task/file 绑定和本地字节/收据；再次同一有效 complete 并核验本地收据前阻止下载与清理 |
| pending/running | 记录 latest_task_status 与 waiting；保留原 file ID 和本地收据，但撤销下载/清理资格；单次退出，无无限循环 |
| error | 保留 failed，退出 2，不自动删任务/重提 |
| complete | 记录 latest_task_status=complete 与确切 file ID；同一 file ID 的本地大小/hash 复核成功可恢复 downloaded，否则 ready；新 file ID 不继承旧本地收据；指定 folder 若响应没有可核验目录字段则标记 `folder_verification=unknown`，并同时阻止下载与清理；有字段则必须与请求 folder 严格一致 |
| folder fields | 仅对响应实际提供的 `folder_id`/`parent_id` 等已出现字段做一致性检查；多个字段冲突拒绝。未核证官方 schema，不把 mock/第三方字段当平台保证 |
| response errors | 只输出错误分类，不回显响应正文、message、URL 或 token；不把同时存在的陈旧成功字段当作成功 |
| download 失败 | 非零退出；保留 .part，不换目的地，不生成清理建议 |
| 下载退出 0 但没实际普通文件 | 拒绝记成功，不生成清理建议 |
| 清理 | 完整来源/task ID/file ID/account scope 绑定、最近有效观察仍 complete、目录绑定为 matched（未指定 folder 除外）、已下载且 ID 唯一匹配、本地大小/SHA-256 未变、--verified-local 才打印；只打印，不删除 |

`submitting` 的人工恢复：先停止写入并保存状态副本，在官方界面对账**原链接、目录、时间、当前账号与确切 task ID**；不要按文件名/首个任务猜。只有用户确认当前 CLI 返回的稳定账号 ID 与原收据属于同一账号后，才可在本地私密状态副本保留原 fingerprint、同一非敏感 account scope、`account_scope_binding=operator_declared_unverified` 和身份哈希，补 `task_id` 并置 `stage` 为 `submitted`（version 保持 1）；缺 scope、声明标记或身份哈希的旧收据不得静默补写。之后每一步仍须显式传入该 scope 并重新核对身份再跑 step2。脚本没有自动认领或跨账号恢复；无法核对就停，不新建 state 绕过去重。

step3/4 不接受孤立的 ready/downloaded 标志；两步都要显式传入与收据一致的 account scope，并且收据必须带 `account_scope_binding=operator_declared_unverified` 与当前身份哈希。旧收据缺少 `latest_task_status`、account scope、声明标记或身份收据时，先停并人工核对，不能手填 complete/scope/身份绕过；pending/running 或查询超时后即便本地文件还在，也须重新观察同一 complete 并核验收据才恢复资格。指定 folder 但观察不到可核验目录字段时虽可标 `unknown`，但 step3 下载和 step4 清理都会阻止，不能生成清理预览。

CLI 入口用独占 `.lock` 防同一 state 并发；崩溃遗留锁不自动抢占，用户核对进程与远端后再移走旧锁。同一资源使用不同 state/机器仍可能重复，**本地防重复不是服务端幂等键/全局 exactly-once**。状态文件不包含原始 URL/凭据，但仍应私密保留，不放分享目录。

## 下载收据的真实含义

`download -o` 接受完整输出文件，不是目录。本脚本用 `<dest>/<fileID>.part` 下载，成功后不覆盖地落为 `<dest>/<fileID>`，保留原 ID 命名避免文件名注入/碰撞；不会失败后去掉 `-o` 偷偷下载到 cwd。已有目标/中断文件不覆盖，人工核验或移走后重试，不承诺断点续传。文件夹/多文件 BT 未实现，使用批量备份。

本地 SHA-256 只证明“清理预览时仍是下载后同一份字节”，**不证明与服务端源内容一致**。仍需用户核对来源、大小、可用的可信校验值/内容；输出为 `downloaded_unverified`，不能把 CLI 退出 0 当成完整性证明。不支持恶意本地用户并发替换文件的威胁模型。

## 清理边界

step4 先只读 `auth status -F json` 核对当前身份摘要；不查询 task/file、不回读云对象、不删除。必须使用本次收据的唯一 file ID、匹配的 account scope 和身份哈希，以及（若指定 folder）已验证为 `matched` 的目录；全部 ID 验证后才打印，不能传 shell 片段。账号切换拒绝已在受支持字段的中性 fixture 合同内验证，官方稳定 ID 字段的真实 schema 尚未验收；不能因此移除身份门禁或声称真实账号兼容。最后执行删除仍是独立的用户授权动作；人工执行前核对当前账号和云端对象。

`pikpak rm --help` 只写“删除”，**未保证回收站、可恢复或立即释放容量**。本脚本不会清空回收站、不会用 `task rm --delete-files`、也不会承诺“云端不留痕迹”。跨设备账号变化不能靠本地收据验证，清理预览不是自动执行授权。

机制来源、固定许可证、发行证据与不采纳项见同目录下 `references/upstream-design.md`（纯 Markdown 文本，随本 skill 一同分发，可直接用文本编辑器完整阅读；其中不含脚本、不联网、不在运行时执行任何外部请求）。rclone 为 MIT，固定研读快照与发行 tag 的祖先关系未核验；AutoOfflineDownloadBot 许可未确认，仅作行为对照，不复制代码、不安装运行。

## 引荐披露 / Referral disclosure

本套 skill 的公开邀请码是 `22874035`，来自分享者；使用可能让分享者获得推广奖励，福利以 PikPak 官方页面为准。你可以拒绝，不影响本 skill。
This public referral code is `22874035`. It may reward the sharer; benefits follow PikPak's official page. You can decline without affecting this skill.

本 skill 不自动注册、登录或改变账号。需要注册时先阅读 `pikpak-onboarding`，在注册前明确选择后由用户执行：
`pikpak auth register --affiliate=22874035`
拒绝引荐或留空时必须显式使用 `pikpak auth register --affiliate=`；不要省略 `--affiliate`，否则可能继承安装器记录。
