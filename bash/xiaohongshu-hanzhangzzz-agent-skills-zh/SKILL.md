---
name: xiaohongshu
description: |
  小红书统一入口：管理多个自己的账号（矩阵号）各自的登录态、搜索帖子、翻自己的收藏与收藏夹、下载单篇或批量图文视频并提取口播、检索逐次积累的本地材料；也支持小红书文案起草、存平台草稿及已授权发布的浏览器指引。用于搜小红书、下载小红书、下载我收藏的帖子、提取口播、基于小红书材料回答、写小红书文案。不依赖独立小红书 CLI、MCP 或 RAG 服务。
license: Apache-2.0
metadata:
  trigger: /xiaohongshu
  compatibility: Codex, Claude Code; macOS/Linux, Python 3.10+
  version: "3.4.0"
---

# 小红书统一入口

只做意图路由、参数选择、材料筛选和带来源的回答。让 `scripts/xhs.py` 执行登录、搜索、下载、入库与召回；不要在对话中重新拼接 Cookie、签名或临时爬虫。

## 前置检查

- 从本 SKILL.md 的实际安装位置定位脚本；不假设安装在某个用户目录。
- 登录、搜索、正文读取、本地召回只需要 Python 3.10+ 标准库与内置签名源码；首次登录还需要 Google Chrome。当前不支持 Windows。
- 视频下载需要 yt-dlp、ffprobe；口播提取另需 Whisper medium 与 ffmpeg。除 PATH 外还会在 `~/.local/bin`、`/opt/homebrew/bin`、`/usr/local/bin`、`~/bin` 里找这些工具（cron、launchd 不读登录 shell 的 PATH）。仍找不到时报告 `MISSING_TOOL`，不要自动全局安装。
- 只在用户请求相应能力时使用媒体工具；普通搜索不自动下载全部帖子。
- 任何平台操作开始前先跑一次 `status`（要指定账号时用 `profiles` 先看标签）。拿到 `NEED_LOGIN` 就按下面的登录流程引导扫码，不要带着失效登录态往下跑。用户唯一需要做的动作是扫码，开窗口、等待、取 cookie、校验都由脚本完成。

示例中的 `$SKILL_DIR` 代表已定位的本 Skill 目录。所有命令输出单个 JSON 对象，包含 `ok`、`schema_version` 和 `data` 或 `error`。检查真实字段，不根据退出码独自推断内容完整。

## 路由

| 用户意图 | 执行 |
|---|---|
| 登录 | 先用一句话告诉用户「去新开的小红书专用 Chrome 扫码」，再执行 `python3 "$SKILL_DIR/scripts/xhs.py" login`。该命令开窗口并等扫码（默认最多 180 秒，`--wait` 可调），扫完自己收尾，不需要再跑第二条命令 |
| 登录检查 | `python3 "$SKILL_DIR/scripts/xhs.py" status` |
| 查看有哪些账号 | `python3 "$SKILL_DIR/scripts/xhs.py" profiles`；列出标签、昵称、登录是否有效、哪个是缺省账号 |
| 再加一个账号 | `python3 "$SKILL_DIR/scripts/xhs.py" --profile 标签 login`，同样是让用户扫码、脚本等待收尾。标签由用户起，只允许字母、数字、中文、下划线、连字符 |
| 用指定账号执行 | 任何命令前加 `--profile 标签`（放在子命令之前）；省略时用缺省账号 |
| 改缺省账号 | `python3 "$SKILL_DIR/scripts/xhs.py" profiles --set-default 标签` |
| 搜索帖子 | `python3 "$SKILL_DIR/scripts/xhs.py" search "关键词"`；可用 `--page`、`--sort general/popular/latest`、`--type all/video/image` |
| 读取并保存帖子正文 | `python3 "$SKILL_DIR/scripts/xhs.py" fetch "帖子链接或ID"`；一次传多个链接或 ID 即批量下载，逐篇处理 |
| 列出我的收藏夹 | `python3 "$SKILL_DIR/scripts/xhs.py" albums`；读专用浏览器里的个人主页收藏夹标签页（浏览器没开会自动后台启动），结果缓存供下次按名字取用 |
| 找我收藏过的帖子 | `python3 "$SKILL_DIR/scripts/xhs.py" collected`；`--album 收藏夹名` 只看一个收藏夹，`--keyword 词` 按标题预筛（可重复），`--limit`、`--pages` 控制取多少（收藏列表每页约 10 篇，收藏夹每页约 30 篇） |
| 下载单篇图文/视频 | 在 fetch 后加 `--media` |
| 下载视频并提取口播 | 在 fetch 后加 `--transcribe`；产物标记为未人工校对 |
| 查询已有材料 | `python3 "$SKILL_DIR/scripts/xhs.py" recall "关键词"`；离线关键词召回，最多默认5篇，不是向量语义检索。加 `--all-accounts` 查所有账号存过的材料 |
| 存成平台草稿 | `python3 "$SKILL_DIR/scripts/xhs.py" draft --title "标题" --body "正文"`；加 `--image 路径`（可重复，最多18张）存图文，加 `--video 路径` 存视频，都不加则走平台「写文字」生成文字卡片。正文长可用 `--body-file 路径` |
| 写文案、人工发布 | 阅读 `references/publishing.md`；draft 只存草稿，发布由用户在专用浏览器点击 |
| 结束使用专用浏览器 | `python3 "$SKILL_DIR/scripts/xhs.py" close` 关当前账号的；`close --all` 关所有账号的。用户还在查看或处理登录时保留窗口 |

## 多账号

一个标签 = 一个账号 = 一套 cookie + 一个独立 Chrome 用户目录；账号之间不共用浏览器，因为一份 cookie 只能登一个号。

- 用户说「用小号搜」「把这个存到工作号草稿」时，先 `profiles` 确认标签，再带 `--profile` 执行；标签对不上就问用户，不要猜。
- 搜索、收藏夹、下载、草稿都跟着 `--profile` 走。素材库按账号 ID 分目录，同一账号换标签登录仍复用已有材料。
- 同时最多两个账号在工作，第三个会收到 `BUSY`。不要为了快而并发铺开：每多一个号就多一个 Chrome 和一路来自同一 IP 的请求。
- 批量跑完提醒用户 `close --all`，不要留着多个 Chrome。
- 同机、同 IP 下多号轮转有真实的风控风险，无法量化。脚本只做账号隔离（独立浏览器目录、按账号独立节流），不做代理池和指纹伪造；出现 `RISK_CONTROL` 就停下并如实告诉用户，不要换号重试同一件事。

## 收藏夹批量下载

用户要「把收藏里关于某主题的几篇下载下来」时：

1. 先 `albums` 看有没有对应主题的收藏夹。有就 `collected --album 名字`；没有就 `collected --keyword 词`，词取用户说法及其常见写法（如 ui、UI、设计）。标题预筛只匹配标题，漏召回很正常，必要时放宽关键词或加大 `--pages`。
2. 读返回的标题自己判断哪几篇真属于该主题，再确认篇数；用户说「几篇」且没给数字时按最近 3–5 篇并说明取了几篇。平台返回的是收藏页顺序，脚本不另外按时间排序。
3. 把选中的 ID 一次性交给 `fetch ID1 ID2 ... --media`，需要口播再加 `--transcribe`。转录在 CPU 上大约是视频时长的 2–4 倍（实测 6 分钟视频约 22 分钟），先按这个量级告诉用户预计耗时，再开始跑。
4. 逐篇结果在 `notes` 里，失败的在 `failed` 里。报告实际成功几篇、落在哪个目录，不要把请求篇数当成功篇数。遇到 `RISK_CONTROL` 或 `NEED_LOGIN` 时脚本会停下并把其余标成 `SKIPPED`，照实报告。

## 搜索与回答

1. 根据问题先 recall 已有材料；需要新证据时再 search。默认最多三个搜索词，深入读取最多十篇，有足够证据就停止。
2. 根据标题和相关性选择帖子，调用 fetch 读正文。搜索卡片只能当线索。
3. 视频正文只有标签时，不能假装已经理解视频。重要视频用 `--transcribe`；图文信息主要在图片时，阅读已下载图片，说明图片文字尚未进入自动索引。
4. 将答案连接到实际读过的正文、口播或图片，并附帖子链接或本地 note.md。区分作者经验、评论、模型推断与转录错误；不把点赞量当真实性证明。
5. 缺少材料或作者说法冲突时明确指出；不用已有常识填充成“小红书搜索结论”。

## 数据与账号

数据默认放在用户主目录下 `.local/share/xiaohongshu`，可在子命令前用 `--data-dir` 指定。登录态按标签放在 `profiles/<标签>/`（cookie、浏览器端口、Chrome 用户目录、并发锁各自一份）；素材按账号 ID 放在 `accounts/<哈希>/`，各账号独立的 SQLite 和笔记目录。旧的单账号安装会在首次运行时自动迁到 `profiles/default`，不需要重新扫码；迁移前会先关掉还在跑的专用浏览器，避免移动正在使用的 Chrome 用户目录。Skill 源码与用户知识分离。

search、collected 保存候选记录与详情访问引用；收藏夹标称篇数可能大于接口实际能取到的篇数，已删除或已不可见的帖子仍计入显示数字，按返回的条目报告而不是按标称数字；只有 fetch 保存的完整材料进入本地召回。collected 不改动平台上的收藏，只读；收藏夹列表取自专用浏览器渲染的页面（平台没有可签名的列表接口），收藏夹里的帖子仍走接口。按帖子 ID 去重，已保存正文、媒体和字幕可复用，不重复跑转录。价格、日期等需要新鲜数据时不要把旧缓存当现状；当前需要更新单篇内容时先说明缓存范围，由用户决定是否重新获取。

账号凭证只保存在本地私有文件，不输出到回答、日志、Git 或外部模型。只连接本脚本创建的 Chrome endpoint，不扫描主浏览器、不注入旧 Cookie。不承诺登录永久有效。

draft 只写入草稿箱，不发布、不定时发布、不改动已发布笔记。草稿存在专用浏览器的本地存储里，不在账号云端：换浏览器或清除该 profile 数据即消失，也不会出现在手机 App。draft 会先关掉遗留的创作页标签，再开新标签操作，结束后回查草稿箱确认最新一条就是本次标题；标题未被确认时不会留下草稿。用户要求真正发布时，让其本人在专用浏览器里点击发布。

## 错误处理

- `NEED_LOGIN`：先告诉用户要扫码，再跑 `login`（会自己等待并收尾）；不自动切到别的账号。
- `LOGIN_TIMEOUT`：等待期内没扫完，窗口仍开着。确认用户是否还要登录，要就再跑一次 `login`；不要改用别的账号或别的方式绕过。
- `RISK_CONTROL`：停止本次平台请求，让用户查看专用浏览器，不更换代理、伪造验证或循环重试。
- `INCOMPLETE_RESPONSE`：响应缺少必要数据，不能报告“没有结果”或“帖子已删除”。
- `TOOL_FAILED`、`INVALID_VIDEO`：报告阶段未完成，保留已经保存的正文与部分文件；不要声称完整下载成功。
- `BUSY`：同一账号已有操作在跑，或已有两个账号在同时工作。等它结束，不绕开锁并行访问账号。
- `UPLOAD_FAILED`：素材未被编辑器接收，此时没有保存任何草稿；检查文件格式与大小后重试，不要声称已存草稿。
- `DRAFT_UNCONFIRMED`：没有拿到平台确认，或草稿箱里最新一条不是本次标题。报告未确认，让用户在专用浏览器核对；不要重复提交。
- `PAGE_CHANGED`：创作页结构与脚本预期不符，可能是平台改版。报告具体步骤，不要改用猜测的选择器硬点。
- `ALBUM_UNKNOWN`、`ALBUM_AMBIGUOUS`：收藏夹名没缓存或匹配到多个。先跑 `albums`，或用返回的完整名字、收藏夹链接重试；不要猜 ID。
- `PERMISSION_DENIED`：报告不可写的安装/数据边界，不尝试绕过。

## 单入口安装

先运行 `python3 "$SKILL_DIR/scripts/xhs.py" install` 查看迁移对象。用户已要求统一本机入口时执行 `install --apply`：旧小红书入口移到不可发现的备份目录，Codex 与 Claude 各保留指向同一源码的 xiaohongshu 链接。

换一台电脑时：代码跟仓库走，登录态不跟着走。新机器上先 `install --apply` 建链接，再 `login` 扫码登录每个要用的账号（`--profile 标签` 分别登），数据目录和素材库都是本机的，不与旧机同步。

恢复使用 `install --restore "返回的备份目录"`。安装程序不修改已有用户知识或 Chrome profile；安装成功不表示当前会话已经重新加载技能，必要时新开会话验证发现结果。

源码来源、许可证和修改范围见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
