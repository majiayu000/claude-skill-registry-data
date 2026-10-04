---
name: laohan-xiazai
description: 从互联网拿内容一站式——视频下载、音频提取+转文字、字幕下载、评论采集、博主数据、网页抓取、搜索聚合、跨平台发布与数据分析，覆盖 30+ 平台（抖音/TikTok/YouTube/B站/小红书/知乎/公众号/视频号/微博/Reddit/HackerNews/即刻/知识星球/雪球/贴吧/头条/Twitter等），按降级链自动选择最优工具。Use when 用户说"下载""下个视频""帮我抓""抓一下""爬""爬取""读一下""读这个链接""看看这个网址""转文字""转录""听写字幕""评论""看看评论""抓评论""博主数据""博主更新""up主""谁谁最近发了什么""封面""发抖音""发小红书""定时发布""草稿""账号数据""粉丝数""给我截图""网页正文""这个页面讲了啥"，或给出任意 URL / 短链接 / BV号 / 视频号链接 / 公众号文章链接 要求获取内容，或提到抖音/TikTok/YouTube/B站/小红书/知乎/公众号/视频号/微博 等具体平台名要求下内容、搜内容、读评论、抓数据，以及任何涉及从互联网拿内容的操作。优先按降级链选工具：搜索走 anysearch→opencli→agent-reach；下载按平台路由；抓取走 Scrapling→browser-use→web-access。纯技术查证/搜教程心得类搜索（不带平台名、不取内容）让位 laohan-sousuo（Jeffrey 2026-10-02 拍板）。
version: "1.3.1"
---

# 从互联网拿内容

按平台选择正确方法，一步到位。先看平台路由表，再读对应 reference 文件。平台方法不行时，按品类降级链逐层深入——每层解决不同问题，能浅不深。

## 核心理念

能浅不深——先用最轻的方法（HTTP 请求），不行再加重量（浏览器渲染→反检测→AI 操作→手动控制）。成本递增，每层解决不同问题，不要跳层。

## 不适用场景

- 批量爬取/爬虫开发 → 这不是爬虫框架，是一次性内容获取工具
- 需要登录才能访问且用户未登录 → 告诉用户先登录对应平台，web-access CDP 可以接管已登录的 Chrome
- 下载付费内容/会员内容 → 不处理侵权场景

## 前置检查（定期更新，命令报错时必做）

> opencli 高频发版（每周 2-3 次），但**不需要每次使用都更新**——定期（如每周）更新，或命令报错/找不到新命令时再更新即可。

### 第1步：更新 opencli（npm 包）
```bash
npm update -g @jackwener/opencli
```

### 第2步：更新 opencli skills（npx 管理）
```bash
npx skills update -g -y
```
opencli 自带 4 个辅助 skill，随 opencli 仓库更新但独立于 npm 包。必须单独更新：
- **opencli-usage**：查命令总览，不确定有什么命令时用
- **opencli-autofix**：命令失败时自动诊断修复（SELECTOR 错误、页面结构变化等）
- **opencli-browser**：浏览器自动化操作
- **opencli-adapter-author**：写新的 opencli 适配器

### 第3步：查最新命令比对文档
```bash
opencli <platform> --help
```
opencli 经常加新命令（如 4 月加了 bilibili download、xiaohongshu download），SKILL 文档可能滞后。**发现新命令时更新对应 reference 文件。**

### 第4步：检查 Browser Bridge
```bash
opencli doctor
```
3 项全绿（Daemon + Extension + Connectivity）才能用 Cookie 命令。失败时排障：
1. `opencli doctor` 看哪项失败
2. daemon 没跑 → `opencli daemon restart`（opencli 自带 daemon 管理，**不要用 launchctl**——opencli 不提供 LaunchAgent）
3. daemon 在跑但扩展未连 → 让用户 `chrome://extensions/` 关开 OpenCLI 扩展
4. 都 OK 还连不上 → `opencli daemon stop` 后再跑任意 `opencli <命令>` 触发 daemon 自启

### 命令失败时的处理

1. 先用 **opencli-autofix** skill 诊断：`OPENCLI_DIAGNOSTIC=1` 重跑失败命令
2. 修复成功 → 更新 reference 文件记录正确方法
3. 修复失败 → 按降级链切换方法

## 快速路由

### 场景 A：下载（视频/音频/字幕/博主数据）

先判断平台，再读对应的 reference 文件：

| 关键词 | 平台 | reference 文件 |
|--------|------|---------------|
| 抖音 / douyin | 抖音 | `references/douyin.md` |
| TT / tiktok / TikTok | TikTok | `references/tiktok.md` |
| YouTube / youtube / 油管 | YouTube | `references/youtube.md` |
| B站 / bilibili / BV | B站 | `references/other-platforms.md` |
| 小红书 / xhs | 小红书 | `references/other-platforms.md` |
| 知乎 / zhihu | 知乎 | `references/other-platforms.md` |
| 公众号 / 微信文章 | 微信公众号 | `references/other-platforms.md` |
| 视频号 / 微信视频号 | 微信视频号 | `references/other-platforms.md` |

不确定平台时，默认尝试 `yt-dlp <url>`，失败再按平台路由。

> `references/douyin.md` 除下载/转录外，还含**发布自动化**（publish/draft/update）与账号数据分析——发布需求直接读该文件对应章节。

### 场景 B：搜索/阅读（文章/评论/帖子/搜索结果）

不走 reference 文件，直接走平台封装降级。注意：场景B 的首选方法与第一层降级表（下载场景）不同——搜索/阅读优先用 opencli 搜索命令或 agent-reach，下载才用移动端 UA / fetch.py 等。

| 平台 | 第1选 | 第2选 | 第3选 | 第4选 |
|------|-------|-------|-------|-------|
| 公众号 | `opencli weixin search/download` | agent-reach | fetch.py | Jina Reader |
| 知乎 | opencli zhihu | agent-reach | Jina Reader | — |
| 小红书 | opencli xiaohongshu | agent-reach | Scrapling stealthy | — |
| 微博 | opencli weibo | agent-reach | Jina Reader | — |
| B站 | opencli bilibili | agent-reach | Jina Reader | — |
| 抖音 | `opencli douyin search`（视频流搜索，仅 likes 真实） | `dy-cli`（statistics 字段全，pip 装+扫码，见 `references/douyin.md`） | 同命令 trace/autofix + `opencli browser` 绑定当前登录页只读取证 | douyin-session（评论） |
| TikTok | opencli tiktok（需 Browser Bridge） | agent-reach | Scrapling stealthy | — |
| 任意平台 | agent-reach（13平台搜索/阅读，含 GitHub/RSS/V2EX/Twitter/Reddit/小宇宙/Exa 等 opencli 不覆盖的） | web-content-fetcher | Jina Reader | Scrapling stealthy |

**agent-reach 触发场景**：用户说"读一下这个链接""这个公众号文章"，或给出非视频的社交平台链接。纯技术查证类搜索不进本 skill（让位 laohan-sousuo）。

## 降级链

### 第一层：平台路由（Layer 2 平台封装）

每个平台方法失败时，按以下顺序降级，直到成功或全部失败才报错给用户：

| 平台 | 第1选 | 第2选 | 第3选 | 最终兜底 |
|------|-------|-------|-------|---------|
| 抖音 | 短链解析 + Playwright 抓 aweme/detail | `opencli douyin` | douyin-session（评论） | Scrapling stealthy |
| TikTok | tikwm API | `yt-dlp` | `opencli tiktok`（需 Browser Bridge） | — |
| YouTube | `yt-dlp`（需 `--cookies-from-browser chrome`） | `opencli youtube transcript`（字幕） | — | — |
| B站 | `opencli bilibili download`（需 Browser Bridge） | Jina Reader | — | — |
| 小红书 | `opencli xiaohongshu download`（需 Browser Bridge） | agent-reach | Jina Reader | — |
| 知乎 | `opencli zhihu` | Jina Reader | — | — |
| 公众号 | `opencli weixin download`（导出 Markdown） | `fetch.py` | agent-reach | Jina Reader |
| 视频号 | wx_video_download（MITM 代理） | — | — | — |
| 未知平台 | `yt-dlp` | Scrapling MCP（get） | Scrapling stealthy | Jina Reader |

降级时注意：
- 抖音不存在 yt-dlp 降级路径（已验证无效），不要浪费时间尝试
- 抖音纯 HTTP 通道 2026-08 起全部关闭（iesdouyin SSR / douyin_tiktok_scraper 均失效），单视频下载走短链解析 + Playwright 抓包（见 `references/douyin.md`）
- B站 yt-dlp 已被 HTTP 412 全面拦截（2026-04-28 验证），不要尝试 yt-dlp 下载B站视频
- YouTube 无 cookies 会被 bot 检测拦截，必须加 `--cookies-from-browser chrome`
- 每步失败后简要告诉用户换了个方法，不要静默切换
- 全部失败时，告诉用户具体哪步失败了、可能的原因、建议用户做什么

### 第二层：品类降级（平台路由全部失败时）

平台方法全部失败后，按能力从轻到重逐层深入。每层解决一个不同的问题：

```
平台封装已试过（opencli / agent-reach / yt-dlp 全部失败）
  ↓ 问题：普通网页抓取即可
轻量抓取 → Scrapling MCP get（普通 HTTP 请求，无 JS 渲染）
  ↓ 问题：页面需要 JS 渲染
JS 渲染抓取 → Scrapling MCP fetch（Playwright 浏览器渲染）
  ↓ 问题：被反爬拦截
反检测抓取 → Scrapling stealthy_fetch（绕过检测 + 提取内容）
  ↓ 问题：页面结构未知，写不出选择器
AI 浏览器 → browser-use（AI 理解页面结构、自主操作）
  ↓ 问题：需要登录态，或要多步交互（点击/翻页/表单/上传）/视频帧采样
CDP 接管 → web-access（接管用户日常 Chrome，天然登录态；已知需登录时跳过 browser-use 直接来这层）
  ↓ 问题：需要代码级精确控制，或要独立无登录态浏览器做隔离
手动驱动 → ECC Playwright MCP（代码级精确控制每一步）
```

**每层解决的问题不同，不要跳层**：
- 普通网页 → Scrapling get（最轻，HTTP 直接请求）
- JS 渲染 → Scrapling fetch（需要浏览器但不需隐身）
- 反爬拦截 → Scrapling stealthy（隐身模式绕过检测）
- 页面看不懂 → browser-use（AI 理解能力）
- 需要登录态 / 多步交互 / 视频采样 → web-access（用户日常 Chrome 的真实登录态 + 确定性 CDP API）
- 精确操作 → Playwright（人工级控制）

**成本递增，能浅不深**：Scrapling get（HTTP 秒级）< Scrapling fetch（浏览器秒级）< Scrapling stealthy（反检测）< browser-use（需调 LLM API）< web-access（需 CDP 连接）< Playwright（需写代码）

## 评论采集

> 详查命令见 `references/other-platforms.md`。opencli 是评论主力（read 8 平台 / write 3 平台），MediaCrawler 只抓不写且禁商业，不装。

| 平台 | read 评论 | write 评论 | 命令 |
|------|----------|-----------|------|
| B站 | ✅（含楼中楼 `--parent`） | ✅ 发评论/回复 | `opencli bilibili comments <bvid>` / `comment <bvid> <msg>` |
| 小红书 | ✅（楼中楼） | ❌ | `opencli xiaohongshu comments <note-id>` |
| 知乎 | ✅ `answer-comments` | ✅ `comment <target> <text>` | 回答评论列表 / 发评论 |
| 微博 | ✅ | ❌ | `opencli weibo comments <id>` |
| 即刻 | ✅（post 含评论） | ✅ `comment <id> <text>` | `opencli jike post <id>` / `comment` |
| 知识星球 | ✅（topic 含评论） | ❌ | `opencli zsxq topic <id>` |
| 雪球 | ✅ | ❌ | `opencli xueqiu comments <symbol>` |
| 贴吧 | ✅（read 含回复） | ❌ | `opencli tieba read <id>` |
| 抖音 | △（user-videos 含热门评论，无独立 comments） | ❌ | `opencli douyin user-videos`；深度评论用 douyin-session adapter |
| **快手** | ❌ opencli 无此平台 | ❌ | **唯一真缺口**，需另调研（移动端 UA / web-access CDP） |

批量评论/批量主页采集属爬虫框架范畴，不在本 skill（见「不适用场景」）；按需取评论走 opencli。

## 通用兜底

| 方法 | 工具 | 场景 |
|------|------|------|
| agent-reach | `agent-reach`（pipx/pip 安装，官方推荐 pipx） | 13 平台搜索/阅读统一入口（Tier0 零配置：Web/YouTube/GitHub/RSS/Exa/V2EX/雪球；Tier1 需登录态：Twitter/Reddit/B站/小红书用 Cookie，小宇宙用免费 Groq Key）。管"读/搜"，与 opencli（管"下载/操作"）互补 |
| Jina Reader | `curl -sL "https://r.jina.ai/<url>"` | 通用网页内容提取 |
| web-content-fetcher | `/web-content-fetcher` skill | agent-reach 失败时的三级降级抓网页 |
| Scrapling stealthy | MCP stealthy_fetch | 反爬场景 |
| yt-dlp | `yt-dlp <url>` | 通用视频下载 |
| browser-use | `/open-source` skill | AI 自主操作浏览器，全新/未知页面 |
| web-access | `/web-access` skill | CDP 接管已登录日常 Chrome（localhost:3456），覆盖：登录态内容、复杂交互（点击/翻页/表单/上传）、视频帧采样、本地书签历史检索 |
| Playwright 手动 | ECC Playwright MCP | 精确手动控制，最后兜底 |

### web-access 调用要点（降级链中唯一连用户日常浏览器的工具）

降级链其余工具（Scrapling / browser-use / Playwright MCP）都开**独立无状态浏览器**，唯独 web-access 直连用户日常 Chrome，天然带登录态、书签、历史。触发 `/web-access` 加载后按此调用：

1. **启动 CDP proxy**：`node "${CLAUDE_SKILL_DIR}/scripts/check-deps.mjs"`（Node 22+ 必需，脚本自动启动并等待 proxy 就绪）
2. **操作前必须向用户展示封禁须知**：部分站点对浏览器自动化检测严格，存在账号封禁风险，已内置防护但无法完全避免，继续操作即视为接受。
3. **curl 调 localhost:3456 API**：`/new`（后台 tab，URL 走 POST body 保留完整参数）/`/eval`（读写 DOM，递归穿透 Shadow DOM·iframe）/`/click`·`/clickAt`（真实鼠标手势，触发文件对话框）/`/scroll`（触发懒加载）/`/screenshot`（含视频当前帧）/`/setFiles`（上传，绕过对话框）/`/close`（关闭自建 tab，保留用户 tab）
4. **本地浏览器检索（web-access 独有）**：用户说"我之前看过的""公司内部系统"等公网搜不到的目标 → `node "${CLAUDE_SKILL_DIR}/scripts/find-url.mjs" 关键词 [--only bookmarks|history] [--since 7d]` 查 Chrome/Edge 书签+历史

**何时优先 web-access**：需登录态 / 多步 GUI 交互（点击·翻页·表单·上传）/ 视频帧采样 / 本地浏览器检索——这四类其余工具都做不了或不如它。仅当页面结构完全未知、需 AI 自主探索时才用 browser-use；需代码级隔离测试时才用 Playwright MCP。

## 工具速查

### 语音转文字

| 优先级 | 工具 | 命令 | 说明 |
|--------|------|------|------|
| 1 | 硅基流动 API | `curl -X POST https://api.siliconflow.cn/v1/audio/transcriptions -H "Authorization: Bearer $SILICONFLOW_API_KEY" -F "model=FunAudioLLM/SenseVoiceSmall" -F "file=@audio.mp3"` | 秒级，免费，中文优化 |
| 2 | whisper-cli | `whisper-cli -m model.bin -f audio.mp3 -l zh` | 本地 C++，快 |
| 3 | whisper Python | `python3 -c "import whisper; ..."` (small 模型) | 本地，最准 |
| 4 | whisper-timestamped | `python3 -c "import whisper_timestamped; ..."` | 精确时间戳，字幕制作用 |

### 语音合成 / 音视频处理

| 操作 | 命令 |
|------|------|
| 语音合成（TTS） | `edge-tts --text "文本" --voice zh-CN-XiaoxiaoNeural --write-media output.mp3` |
| 音视频转码 | `ffmpeg -i input.mp4 -vn -acodec libmp3lame output.mp3` |
| OCR | `tesseract image.png stdout -l chi_sim+eng` |
| PDF 提取文本 | `python3 -c "import fitz; doc=fitz.open('file.pdf'); [page.get_text() for page in doc]"` |
| 图片处理 | `magick input.png -resize 800x600 output.png` |

### 搜索兜底

> 注：`smart-search`/`web-search`/`multi-search-engine`/`baidu-search` 位于 `~/.openclaw/skills/`，**需 OpenClaw 环境已安装**；`anysearch` 在 `~/.agents/skills/`（通用，无 OpenClaw 也可用）。无 OpenClaw 环境时优先 anysearch。

| 工具 | 场景 | 说明 |
|------|------|------|
| anysearch | 实时搜索+垂直领域+批量并行+URL全文提取 | 16 个垂直领域（股票/CVE/DOI/法律/学术等；Stock/CVE/DOI 是触发标识符非 domain），`~/.agents/skills/anysearch/`，`/anysearch` |
| smart-search | opencli 搜索路由 | 基于 opencli 的智能搜索，覆盖社交/技术/新闻/购物，`~/.agents/skills/smart-search/` |
| web-search | 通用网页搜索 | DuckDuckGo API，轻量搜索，`~/.openclaw/skills/web-search/` |
| multi-search-engine | agent-reach + Jina 都搜不到时 | 17 搜索引擎聚合对比，`~/.openclaw/skills/multi-search-engine/` |
| baidu-search | 中文内容搜索 | 百度 AI 搜索，中文场景优于通用引擎，`~/.openclaw/skills/baidu-search/` |

**搜索优先级**：通用搜索/事实查询/垂直领域 → **anysearch**（最轻最快）→ opencli（平台结构化数据）→ agent-reach（opencli 未覆盖的平台兜底）。

### Scrapling 调用路径

| 环境 | 方式 | 说明 |
|------|------|------|
| Claude Code 主会话 | MCP 直调 `mcp__ScraplingServer__stealthy_fetch` | 直接可用 |
| OpenClaw 子 agent | mcporter 桥接 `mcporter call ScraplingServer.stealthy_fetch url=<url>` | 子 agent 无 MCP 权限，需桥接 |

## 关键注意事项

- 抖音反爬极强，yt-dlp/Jina/纯 HTTP 全部无效（2026-08 升级后 iesdouyin SSR 与 douyin_tiktok_scraper 也失效），单视频下载走短链解析 + Playwright 抓包（见 `references/douyin.md`）
- TikTok 用 tikwm API，CDN URL 临时，获取后立即下载
- YouTube 字幕首选 `opencli youtube transcript`（返回干净文本免清洗），备选 yt-dlp 的 VTT 需 `clean_vtt.py` 清洗（见 `references/youtube.md`）
- opencli Cookie 命令需要 Browser Bridge 运行（排障：`opencli doctor`）
