---
name: douyin-comments
description: 抓取抖音单条视频的完整评论区（一级评论 + 全部楼中楼回复）和视频详情，可选下载视频，输出按点赞排序的「评论全文.md」和原始 JSON。在已登录抖音的真实浏览器里运行（Claude in Chrome，或 Grok Bot 等 Agent 自带、能执行页面脚本的浏览器），借页面自带 SDK 签名，不需要 TikHub、Playwright 或 a_bogus 逆向。用户给出抖音视频链接（douyin.com/video/…、带 modal_id 的主页链接、v.douyin.com 短链），并说"看评论区""抓评论""拉评论""评论区有什么质疑/疑问""参考评论区"时使用。只适用于抖音单条视频；小红书、B 站、批量采集博主全部作品不适用。
---

# 抖音评论区抓取

## 原理（为什么这样做）

- 抖音 Web 接口要带 a_bogus 签名、msToken、uifid、x-tt-argus 等风控参数。页面里的 SDK 会给页面内发出的 XHR 自动补签名，所以请求都在用户的真实 Chrome 页面里发，指纹和登录态都是真的。
- 只带 `device_platform/aid` 直接调楼中楼接口，会**立刻弹文字点选验证码**，请求挂起（2026-10-30 实测）。原因是缺了页面正常请求才有的公共参数（channel、version_code、浏览器信息、msToken 等）。所以：
  - **主路线** `page_fetch.js`：先拦截页面自己发出的一次真实评论请求当模板，之后只替换 `aweme_id / cursor / comment_id`，其余参数照抄。
  - **兜底路线** `page_ui_expand.js`：在评论区逐个点「展开N条回复」，由页面自己发请求，我们只截获响应。慢，但实测不触发风控。
- 思路借鉴 MediaCrawler（公共参数集、x-tt-argus/uifid、先一级后逐楼、请求间 sleep）。它的许可证是非商业学习许可，**不要复制它的代码或 douyin.js**。

## 硬规则

- **验证码绝不代点**。出现验证码就停下，请用户在 Chrome 里手动完成，然后继续。
- **节奏**：请求间隔 2～4 秒随机，每 15 次请求额外停 8～15 秒。不要为了快去改小间隔；同一视频不要重复整轮重抓（触发验证码的主因之一）。
- **隐私墙**：输出默认写到当前项目的 `.internal/抖音评论/<aweme_id>/`。源链接、作者、原文评论只留在 `.internal/`；给成稿用的归纳文件不写源信息。
- javascript_tool 约 45 秒超时、输出约 1000 字截断：长任务一律是不 await 的后台 IIFE，进度挂在 `window.__dyc` 上轮询，数据经本地接收服务落盘。
- 用完关闭自己开的标签页，并停掉接收服务。

## 步骤

下文 `$SK` = 本 skill 目录，`$OUT` = 输出目录。下面的步骤按 Claude Code + Claude in Chrome 写（实测过的环境）；在 Grok Bot 等其他 Agent 里用，先看文末「在其他 Agent 里用」。

### 1. 解析视频 ID，启动接收服务

- `douyin.com/video/<id>` → id；主页链接带 `modal_id=<id>` → id；`v.douyin.com/…` 短链先在 Chrome 打开，看跳转后的 URL。
- 后台启动接收服务（`run_in_background`，端口被占就换一个，并在页面设 `window.__DYC_RECV`）：
  ```bash
  python3 -I "$SK/scripts/recv.py" --out "$OUT/raw" --port 8765
  ```

### 2. 打开页面，注入拦截

1. `tabs_context_mcp` → `tabs_create_mcp` 新开标签页 → navigate 到 `https://www.douyin.com/video/<id>`。扩展未连接时，请用户在 Claude Code 里执行 `/chrome` 连接。
2. 用 javascript_tool 执行 `page_hook.js` 的全文（读文件后原样传入），返回 `hooked`。**刷新或跳转页面后必须重新注入。**
3. 截图确认没有验证码。点视频下方的评论图标（或往下滚动），让评论区加载出来；这一步页面会发出真实的一级评论请求，被拦截成模板。
4. 可选但推荐：设 `window.__DYC_UI_MAX = 1`，执行 `page_ui_expand.js`，让页面真实展开一个楼，拿到楼中楼模板。不做的话，主路线会用一级模板派生。
5. 检查 `Object.keys(window.__dyc.templates).join(',')`，至少要有 `top`。不要在 javascript_tool 里打印模板 URL：带 Cookie 和查询串的输出会被工具拦截。要看参数，读 `$OUT/raw/template_top.json`。

### 3. 主路线

```js
window.__DYC_CFG = { awemeId: '<id>' };   // 可选 skipDetail: true；skipThreads: [已抓全的 cid]
```
然后执行 `page_fetch.js` 全文。每 20～40 秒用一次 browser_batch（几个 10 秒 wait + 一次 javascript_tool 读 `JSON.stringify(window.__dyc)`）轮询，同时看 `$OUT/raw/_recv.log` 的增长。耗时大约是：总请求数 × 3 秒。

- `done` → 进入第 5 步
- `fallback` → 先截图。有验证码就请用户手动过，再走第 4 步；没有验证码，说明这一页返回为空或被拒（看 `reason`），也走第 4 步
- `need_template` → 回到第 2 步第 3 小步，让评论区加载出来

### 4. 兜底路线（主路线失败或抓不全时）

1. 刷新页面 → 重新注入 `page_hook.js` → 点开评论区。
2. 执行 `page_ui_expand.js`（不设 `__DYC_UI_MAX`）。状态 `ui_captcha` 表示又弹了验证码：请用户手动过，脚本会自动继续。
3. 状态 `ui_done` 后进入第 5 步。主路线和兜底路线的数据会自动合并去重。

### 5. 汇总与校验

```bash
python3 -I "$SK/scripts/build_report.py" "$OUT"
```
- 退出码 0：全部抓齐。退出码 2：会列出没抓全的楼，用兜底路线补抓后重跑。
- 「一级 + 回复」比视频显示的评论数略少是正常的：被删、被折叠或仅作者可见的评论不会返回。
- 需要视频时：`python3 -I "$SK/scripts/download_video.py" "$OUT"`（720p，带 Referer，不需要 Cookie）。转写用本机 mlx_whisper 或你手边的语音识别工具；看画面就抽帧拼联系表直接看图，不要跑 OCR。

### 6. 交付

- 汇报：一级和回复各多少条、走了哪条路线、有没有触发验证码、耗时。
- 用户要「参考评论区」时，读 `评论全文.md`，按「质疑 / 疑问 / 对比 / 使用经验」归类，归纳文件放在项目根目录，不写源信息。

## 实测记录

| 日期 | 视频 | 路线 | 结果 |
|---|---|---|---|
| 2026-10-30 | 7 分钟 AI 工具视频，195 条评论 | 主路线，先展开 1 个楼拿模板 | 83 + 112 = 195，与此前 UI 兜底抓到的结果逐条一致；35 次请求，138 秒，无验证码 |
| 2026-10-30 | 46 分钟教程，135 条评论 | 主路线，楼中楼模板由一级模板派生 | 77 + 58 = 135；63 次请求，252 秒，无验证码；720p 视频下载正常 |
| 2026-10-31 | 4.5 分钟教程，358 条评论 | 主路线，模板派生 | 161 + 197 = 358，全齐；65 次请求，无验证码 |
| 2026-10-31 | 2 分钟口播，1067 条评论（八成是「求指南」刷屏） | 主路线，模板派生 | 735 + 88 = 823。一级翻到 offset 约 500 之后每页开始大量重复；加 `sort_type=1` 再翻一遍，合并后只多 11 条，剩下约 240 条应是被折叠的评论，接口拿不到。约 150 次请求，无验证码 |

已知限制：上千条评论的视频，一级评论 offset 超过约 500 后接口会返回重复内容，被折叠的评论也拿不到，所以总数会明显少于显示的评论数（实测 823 / 1067）。需要更全时，可以在 `__DYC_CFG` 之外手动加 `sort_type: 1` 再翻一遍，`build_report.py` 会自动去重合并。

还没覆盖到的情况：单个楼超过 20 条回复的翻页；`ui_captcha` 状态的自动检测。遇到时把结果补进上表。

## 产出

```
$OUT/
├── raw/                 # 模板、每页原始响应、_recv.log（可删）
├── comments_top.json    # 一级评论（去重）
├── comments_replies.json
├── 评论全文.md           # 按点赞排序，楼中楼缩进在下面
└── 参考视频.mp4          # 可选
```

## 在其他 Agent 里用（Grok Bot、Muse、Dot、Hermes、OpenClaw 等）

脚本本身不依赖 Claude，只要 Agent 具备这三样就能跑：

1. **一个已登录抖音的真实浏览器**。登录（扫码）必须由用户本人完成，Agent 不代填账号密码。
2. **能在当前页面里执行一段 JS**，并能读回 `window.__dyc` 的值。
3. **能在同一台机器上后台跑一个 Python 进程**，并且页面能访问 `127.0.0.1`（接收服务 `recv.py`）。

步骤对照：

| 上面的步骤 | Claude Code + Claude in Chrome | 其他 Agent（以 agent-browser 为例） |
|---|---|---|
| 开页面 | `tabs_create_mcp` + navigate | `agent-browser open https://www.douyin.com/video/<id>` |
| 注入脚本 | javascript_tool 传入文件全文 | `agent-browser eval "$(cat $SK/scripts/page_hook.js)"` |
| 读进度 | javascript_tool 读 `JSON.stringify(window.__dyc)` | `agent-browser eval "JSON.stringify(window.__dyc)"` |
| 截图看验证码 | computer screenshot | `agent-browser screenshot <路径>` |
| 接收服务、汇总 | Bash 后台跑 `recv.py`，跑 `build_report.py` | 云电脑终端里同样执行 |

注意：

- **在 Grok Bot 上还没有实测过。** 第一次用请先小步验证：先抓一条评论少的视频，核对条数。
- agent-browser 一类工具驱动的是自动化浏览器，比日常用的 Chrome 更容易被识别，验证码可能更频繁。出现验证码一律停下，请用户亲自处理，**不要代点**。
- Agent 自带的「电脑操控」如果不能执行页面脚本，就只能走兜底路线：由 Agent 逐个点「展开 N 条回复」，但仍需要 `page_hook.js` 截获响应，所以至少要能注入一次脚本。
