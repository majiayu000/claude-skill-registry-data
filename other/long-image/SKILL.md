---
name: long-image
description: 长图：两种输入，两种长图。改写稿 content.json → 总结长图（页数由内容决定）（手机宽度单栏，每节配图表和数据面板，附执行清单；--wide 出 1200 宽双栏杂志版；--x 出发 X 用的 X 版：按内容类型另写的以文字为主的 X 稿（原文节选、编者短评、表格、要点），排成一整条，切成 1080 宽、约一屏高、X 不压缩的竖条；--x full 把手机版每页原样切条；13 套主推主题）；文章 article.md（原文、译文、逐字稿）→ 一字不改的原文长图（逐块读回校验，超长自动分张）。可以单独用（已有 content.json 或文章），也可以接在抓取、改写、翻译后面。Use when the user wants a 长图, 总结图, 杂志长图, X / 推特 / Twitter 长图, infographic pages, or 原文长图 / 全文长图 / 原文排版 / 一字不改 / -f from an article or an existing content.json; also to re-render a content.json in another theme (换主题、换风格).
argument-hint: <content.json|article.md|目录> [--theme 主题名|a,b|all] [--wide] [--x | --x full] [--page 1,3] [--out 目录]
allowed-tools: Bash(node ${CLAUDE_SKILL_DIR}/scripts/*)
version: "2.4.0"
---

# 长图（long-image）

> 路径约定：文中的 `${CLAUDE_SKILL_DIR}` 指本 SKILL.md 所在的目录。宿主没有替换这个变量时（命令里原样出现 `${CLAUDE_SKILL_DIR}`），把它换成这个目录的绝对路径再运行；`../<名字>/` 指同级的另一个 skill 目录。

| 输入 | 产出 |
|---|---|
| `content.json`（改写稿） | 总结长图：默认手机版，单栏、1080 宽，手机上不用放大就能读；`--wide` 出 1200 宽的双栏杂志版（适合电脑上看、打印、做展示图）；`--x` 出发 X 的 X 版（以文字为主，`<主题>-x/x-01-1.png …`），`--x full` 出 X 完整版（`<主题>-x-full/`）。`<目录>/<主题>/page-01.png …` |
| `article.md`（原文、译文、逐字稿、`rewrite.md`） | 原文长图：一字不改，1080 宽，`<目录>/full/full.png`（过长时 `full-01.png …`） |

参数：`$ARGUMENTS`

## 0. 先确定输入
- 已有 `content.json` → 总结长图；用户只给了文章、又说"原文 / 全文 / 一字不改 / -f" → 原文长图。
- 给的是链接、文件、粘贴的正文或视频 → 先用 `article-fetch` / `video-transcript` 取原文。
- 只有文章、用户没说原文还是总结 → 长图默认**改写**：先用 `article-rewrite` 写 content.json。原文是外文、又要原文长图 → 先用 `article-translate`。
- 判断规则、工作目录和调用其他能力的方式：`../article2media/references/pipeline.md`。

第一次使用先跑 `node ${CLAUDE_SKILL_DIR}/scripts/doctor.mjs`（Node 22+、Chrome）。

## 1. 总结长图（content.json）
```bash
node ${CLAUDE_SKILL_DIR}/scripts/long.mjs <目录>/content.json                    # 主题取 content.json 的 theme
node ${CLAUDE_SKILL_DIR}/scripts/long.mjs <目录>/content.json --theme midnight   # 用户指定主题
node ${CLAUDE_SKILL_DIR}/scripts/long.mjs <目录>/content.json --wide             # 1200 宽双栏杂志版（文字在左、图在右）
node ${CLAUDE_SKILL_DIR}/scripts/long.mjs <目录>/content.json --x                # X 版：content.json 里的 X 稿排成一整条再切成竖条 → <主题>-x/
node ${CLAUDE_SKILL_DIR}/scripts/long.mjs <目录>/content.json --x full           # X 完整版：手机版每页原样切成竖条 → <主题>-x-full/
node ${CLAUDE_SKILL_DIR}/scripts/long.mjs <目录>/content.json --theme all        # 全部主推主题，分目录输出
node ${CLAUDE_SKILL_DIR}/scripts/long.mjs --list                                 # 列出主题
```
- 每页输出 PNG 和同名 `.html`、`qa.json`，一页大约 4 秒。其他参数：`--page 1,3`、`--scale 2`、`--format jpeg --quality 90`、`--max-height 7600`（手机版默认 7600，宽版 4400）、`--brand brand.json`、`--out 目录`。
- 默认出手机版：用户在微信、朋友圈、微博里看长图，双栏的字在手机上太小。用户说"杂志版 / 宽版 / 双栏 / 电脑上看 / 要打印"时加 `--wide`。手机版一页很高（常见 9000–13000 px）；超过 16000 px 时会自动降低输出倍数并提示，这时把这一页拆成两页。
- **发 X（推特）一律用 `--x`，手机版长图不要发 X**：X 把每张图的长边压到 4096 以内（手机 App 默认只给 2048 版）。1080×9000 的手机长图到了 X 只剩 240–480 px 宽，手机上看不清，电脑上被放大回去也是糊的。
  - **`--x` 是 X 版（默认）**：X 上的人是刷过去的，一组拿掉了解释的图表对他们是猜谜，帖子里每多一张图就少一些人看完。所以 X 版以文字为主：先用 `article-rewrite` 按 `../article-rewrite/references/content-schema.md` 的「X 版」，判断内容类型（故事 / 教程 / 清单 / 报告 / 新闻），在 content.json 里另写一份 X 稿 `x`（原文节选、编者短评、正文、列表、表格、关键句、代码，图最多两张）。脚本把它排成手机宽度的一整条，切成 1080 宽、约一屏高（高不超过宽的 2.6 倍）的竖条：X 手机端把图缩进一屏看，这个高度正好铺满屏幕，正文约 12 pt。content.json 没有 `x` 时 `--x` 会报错并说明怎么写。
  - 标「原文」的段落会和同目录的 article.md 逐字核对，对不上就报错：只能删句、用「……」省略，不能改字。只发 X 时，content.json 可以只有 `title`、`source` 和 `x`。
  - **`--x full` 是完整版**：手机版每页原样切成 1080 宽、高约为宽 3 倍（最高 4096）的竖条，图表和面板都在，信息量和长图一样。用户说"完整版 / 全部内容都要 / 不要压缩"时用它。
  - 两种版本都只在内容块之间切，优先切在小标题（节）之间；标题和它下面的内容、图和图注、短评和它评的那段不会分开。版面检查报「切口」时，是某一块（常见是特别长的面板或清单）比一张图还高、中间又没有空隙，把它拆短。
  - 张数跟着内容走。X 一帖最多 20 张，通常一帖发完；超过 20 张时渲染结果和 `publish.md` 会列出分帖，第 2 帖起回复上一帖，接成线程。帖子文案里不要写死张数。
  - 输出 PNG-8（X 会原样保留，需要 ffmpeg；文件超过 5 MB 自动改 JPEG）。X 稿里有视频截图、照片这类图时加 `--format jpeg`：PNG-8 没有抖动，照片会出色带。交付时提醒用户：用电脑网页发，或在手机 App「设置 → 数据使用」里打开「高质量图片上传」。
  - 用户要"X 版"、说要发 X / 推特，或者原文是 X 链接、用户又没说只发微信时，总结长图和 `--x` 一起出（X 稿另写，出图多花约 5 秒）。
- content.json 没写主题、用户也没指定时，按 `../article2media/references/styles.md` 选一个，写进 content.json。
- 有 AI 插画还没生成时会出占位框并提示：用 `article-rewrite` 的 `illustrate.mjs` 生成，生成不了就去掉插画字段。

**检查与修正（出图 → 发现问题 → 改 content.json 或参数 → 再出图，算一轮；通常 1–2 轮就够。✗ 没修完就继续改；第 2 轮后还剩的 ⚠，交付时说明。只跑 check.mjs 不算）**
1. 版面检查：✗（图内溢出、文字截断、元素重叠、图片加载失败）必须修——缩短图内文字、减少项目，或换一种图；⚠「末行只剩一个字」给那句话增减两三个字；⚠「页面过高」删减内容或拆成两页。
2. **亲眼看图**：用 Read 打开每张 PNG，看图能不能一眼看懂、图和图注是不是一回事、有没有哪节太空或太挤。
3. 只改 `content.json`（字段写法见 `../article-rewrite/references/content-schema.md`、`figures.md`），然后重新渲染。不要手改 HTML。

## 2. 原文长图（article.md）
```bash
node ${CLAUDE_SKILL_DIR}/scripts/long.mjs <目录>/article.md                  # 白底阅读面
node ${CLAUDE_SKILL_DIR}/scripts/long.mjs <目录>/article.md --theme quiet    # 用主题的颜色与字体
```
读 `references/original-long.md`（阅读面规格）和 `../article2media/references/verbatim.md`（允许与禁止、逐块校验）。全文校验未通过（改字、调序、漏块、重复）就是错误，按提示修，不能靠目测放行。看 `full/review/` 里的重叠切片，逐张看完再交付。

## 3. 交付
- 每张图的绝对路径（原文长图加像素尺寸）；
- 总结长图：一行大纲（每页的 part）、用的主题（你选的就一句话说明理由）、怎么换：`--theme 名称`、`--theme all` 都不需要重写内容；要卡片用 `image-cards`，要公众号用 `wechat-layout`；
- 出了 X 版时：`<主题>-x/`（X 版）或 `<主题>-x-full/`（完整版）的张数和分帖（照渲染结果贴出），X 稿用的内容类型，并说明手机版 `page-NN` 是给微信、朋友圈、微博的，发 X 用 X 版；
- 原文长图：原文块数与全文校验结果（"45 / 45 块逐字一致"）、实际字体、分成了几张、生成图 0 张；
- 需要用户留意的地方（未核对的数字、抓取不全的段落）。
