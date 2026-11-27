---
name: article2media
description: 把文章或视频一键做成中文视觉内容的总入口：按推荐组合把 10 个可单独使用的能力串起来——文章抓取、视频转文字、改写（总结）、全文翻译、长图、卡片（小红书 3:4 / 4:5 / 1:1 / 9:16）、公众号排版、口播视频、白板论证、漫画。常用组合：原文→改写→长图（默认）、原文→改写→小红书卡片、原文→公众号排版、原文→总结→公众号、外文→翻译→公众号、原文长图 / 原文卡片（一字不改）、视频→逐字稿→改写→长图或卡片、一稿多发（长图 + 小红书 + 公众号）、文章→口播视频。输入：X/Twitter 长文与线程、网页、微信公众号、本地 Markdown、粘贴的正文；抖音、YouTube、B 站链接、本地视频/音频、.srt/.vtt。13 套主推主题，不指定时按内容选。Use when the user gives an article, URL, long post, video link or file and wants it turned into 总结图, 长图, 知识卡片, 小红书图文, 公众号排版, 口播视频, 原文排版, 白板, 漫画 — or wants several of them, or names a combo (一键、组合、全套、一稿多发) — e.g. "把这篇文章做成图/小红书/公众号/视频", "把这个抖音视频做成小红书", "翻译成中文发公众号".
argument-hint: <url|视频链接|文件|粘贴的正文> [组合名] [-f 原文|-w 白板|-c 漫画] [--ratio 3:4|4:5|1:1|9:16 或 小红书/IG] [公众号] [视频] [--style 主题名|all] [--illustrate] [--verify]
allowed-tools: Bash(node ${CLAUDE_SKILL_DIR}/engine/scripts/doctor.mjs), Bash(node ${CLAUDE_SKILL_DIR}/scripts/*), Bash(node ${CLAUDE_SKILL_DIR}/../article-fetch/scripts/*), Bash(node ${CLAUDE_SKILL_DIR}/../video-transcript/scripts/*), Bash(node ${CLAUDE_SKILL_DIR}/../article-rewrite/scripts/*), Bash(node ${CLAUDE_SKILL_DIR}/../article-translate/scripts/*), Bash(node ${CLAUDE_SKILL_DIR}/../long-image/scripts/*), Bash(node ${CLAUDE_SKILL_DIR}/../image-cards/scripts/*), Bash(node ${CLAUDE_SKILL_DIR}/../wechat-layout/scripts/*), Bash(node ${CLAUDE_SKILL_DIR}/../explainer-video/scripts/*), Bash(node ${CLAUDE_SKILL_DIR}/../logic-whiteboard/scripts/*), Bash(node ${CLAUDE_SKILL_DIR}/../article-comic/scripts/*)
version: "2.4.0"
---

# article2media：推荐组合

> 路径约定：文中的 `${CLAUDE_SKILL_DIR}` 指本 SKILL.md 所在的目录。宿主没有替换这个变量时（命令里原样出现 `${CLAUDE_SKILL_DIR}`），把它换成这个目录的绝对路径再运行；`../<名字>/` 指同级的另一个 skill 目录。

article2media 由 10 个能力组成，**每个都是独立的 skill**，可以单独用，也可以按任意顺序组装。本 skill 是总入口：听懂用户要什么，选一个组合，依次调用各个能力，最后统一交付。本目录的 `engine/` 是所有能力共用的脚本、主题和版式。

参数：`$ARGUMENTS`

## 能力

| skill | 能力 | 输入 → 产出 |
|---|---|---|
| `article-fetch` | 文章抓取 | X 长文 / 网页 / 公众号 / 本地文件 → `article.md` |
| `video-transcript` | 视频转文字 | 抖音、YouTube、B 站、本地音视频、.srt/.vtt → `article.md`（逐字稿） |
| `article-rewrite` | 改写（总结） | `article.md` → `content.json`（改写稿），可导出 `rewrite.md` |
| `article-translate` | 全文翻译 | `article.md` → `article.zh.md`（不删减，逐块对应） |
| `long-image` | 长图 | `content.json` → 总结长图；`article.md` → 原文长图 |
| `image-cards` | 卡片 | `content.json` → 总结卡片；`article.md` → 原文卡片（3:4 / 4:5 / 1:1 / 9:16） |
| `wechat-layout` | 公众号排版 | 文章（原文、译文或 `rewrite.md`）→ 可粘贴的图文 + 封面 |
| `explainer-video` | 口播视频 | 文章（可参考 `content.json`）→ 1080×1920 竖屏讲解视频 |
| `logic-whiteboard` | 白板论证 | `article.md` → 把推理摊成纵向主干的长图 |
| `article-comic` | 漫画 | `article.md` → 黑白漫画 + 3:4 卡片（需要出图能力） |

能力之间只通过工作目录里的文件交接；交接文件、"原文还是改写"的默认判断、怎么调用别的能力，都在 `references/pipeline.md`。**开始前先读它。**

## 推荐组合

| 组合 | 用户通常这么说 | 链路 |
|---|---|---|
| **总结长图**（默认） | 做成图、长图、总结图 | 取原文 → 改写 → 长图 |
| **小红书总结** | 做成小红书、卡片、3:4、IG | 取原文 → 改写 → 卡片 |
| **公众号排版** | 排成公众号、公众号排版 | 取原文 → 公众号排版 |
| **公众号总结** | 总结成一篇公众号 | 取原文 → 改写 → 导出 `rewrite.md` → 公众号排版 |
| **外文搬运** | 翻译成中文发公众号 | 取原文 → 翻译 → 公众号排版 |
| **原文长图** | 原文排版、全文长图、一字不改、`-f` | 取原文 → 长图（原文） |
| **原文卡片** | 全文做成小红书卡片、原文卡片 | 取原文 →（外文先翻译）→ 卡片（原文） |
| **视频转图文** | 这个视频做成长图 / 小红书 | 视频转文字 → 改写 → 长图或卡片 |
| **视频转文字** | 视频转文字、逐字稿 | 视频转文字（交付 `article.md`） |
| **X 图文** | 发 X、推特、转发配一组总结图 | 取原文 → 改写时另写以文字为主的 X 稿 → 长图 `--x`（按内容类型写原文节选、短评、表格、要点，切成 X 不压缩、约一屏高的竖条；`--x full` 把手机版原样切条） |
| **一稿多发** | 长图、小红书、公众号都要 | 取原文 → 改写一次 → 长图 + 卡片 + 公众号（`rewrite.md`） |
| **文章转口播** | 做成视频、口播、视频号 | 取原文 → 口播视频 |
| **白板 / 漫画** | 论证图、`-w`；漫画、四格、`-c` | 取原文 → 白板 / 漫画 |
| **批量** | 一次给多个链接、"这周这几篇都做成…"、links.txt | `batch.mjs init` → 逐条按同一规格做 → 发布清单（见「批量」） |

- **取原文**：文章用 `article-fetch`，视频用 `video-transcript`；用户直接粘贴正文时，自己写 `article.md`（见 pipeline.md 第 1 节）。
- 用户可以点名组合（`/article2media 小红书总结 <链接>`），也可以自己组装（"先翻译，再出原文卡片""改写后只要 1:1"），按用户说的顺序调用即可，表里没有的组合同样成立。
- 用户没点名组合时，按 pipeline.md 第 2 节的默认表判断原文还是改写，再从上表挑最接近的组合。**输入和输出分开判断**：给视频只说明原文是视频，产出仍按用户说的定。
- **手机版长图不发 X**：X 会把它压到几百 px 宽，看不清。用户要发 X、要"X 版"，或原文是 X 链接、用户又没说只发微信时，总结长图同时出 `--x`，交付时说清哪个目录发哪里。
- 以前的参数照样有效：`-f` = 原文长图，`-w` = 白板，`-c` = 漫画，`--ratio` / 平台名 = 卡片，"公众号" = 公众号排版，"视频" = 口播视频；`--style`、`--illustrate`、`--verify`、`--pages`、`--lang` 交给对应的能力。

## 流程

1. **环境检查**（本会话第一次）：`node ${CLAUDE_SKILL_DIR}/engine/scripts/doctor.mjs`。缺的是要用户自己安装的依赖时，把修复建议转告用户，然后停下；其他失败先自己排查、重试一次。`local-fonts` 一行显示没装本地字体、而用户网络不稳定（出图报"字体没有加载"）时，建议他运行一次 `node ${CLAUDE_SKILL_DIR}/scripts/fonts.mjs`（约 65 MB，可加 `--mirror <主机>`）：这是下载，要用户同意再跑；之后出图不再联网加载字体。
2. **定组合**：不需要先跟用户确认，除非 pipeline.md 第 2 节说要问。
3. **依次调用能力**：按 pipeline.md 第 3 节调用每个 skill，照它的 SKILL.md 做完、检查通过（✗ 全部修完），再进入下一步。所有能力用同一个工作目录。
4. **一份改写稿多处用**：一稿多发时只改写一次；同一篇已有 `content.json` 时不要重写，只补新版式需要的字段。
5. **交付**：把每个能力的交付项合在一起说，按产物分组：
   - 每个产物的绝对路径；
   - 走了哪条组合（例如"原文 → 改写 → 3:4 卡片"）；
   - 用了哪个主题（你选的就一句话说明理由），以及怎么换主题、换版式；
   - 卡片贴出发帖文案，公众号贴出标题、摘要和封面路径；
   - 需要用户留意的地方：未核对的数字、抓取不全的段落、识别可能出错的专有名词、翻译检查的提示。
   - 产物是要发布的（卡片、长图、公众号、视频）时，最后加一句："发布后把链接和数据告诉我，我记下来"（见「发布之后」）。

## 批量

用户一次给多个链接（或一个 links.txt）时用。规格整批固定，脚本管抓取、队列和状态，**改写和出图仍由你一条一条按各能力的 SKILL.md 做**。

```bash
node ${CLAUDE_SKILL_DIR}/scripts/batch.mjs init links.txt --name 本周 --spec "cards:3:4,long,wechat"   # 也可以直接写几个链接；--theme 整批固定主题
node ${CLAUDE_SKILL_DIR}/scripts/batch.mjs next 本周        # 下一条内容 + 确切的下一步（能直接跑的会给出命令）
node ${CLAUDE_SKILL_DIR}/scripts/batch.mjs status 本周      # 从磁盘重新计算状态，更新看板 queue.md
node ${CLAUDE_SKILL_DIR}/scripts/batch.mjs checklist 本周   # 给做完的每一条写发布清单 publish.md
```

1. **init**：`--spec` 按用户说的定（`cards[:比例]` 总结卡片、`long` 总结长图、`x` X 版（要发 X 时加上，先写 X 稿）、`x-full` X 完整版、`wechat` 公众号原文排版、`wechat-rewrite` 公众号总结、`full` 原文长图、`full-cards` 原文卡片、`video`、`whiteboard`、`comic`；没说就是 `long`）。已抓过的链接自动跳过（`--refetch` 重抓），视频链接记为"待转写"，不会让整批失败。用户说了自己打算几点发，才写 `--schedule "xhs=周二 20:00"`；不要替用户编发布时间。
2. **循环**：运行 `next` → 照它说的做这一步（改写用 `article-rewrite`，出图用对应能力，检查的 ✗ 修完）→ 再运行 `next`。**一次只做一条内容**，做完一条再做下一条；主题没固定时每篇各自按 styles.md 选。
3. **停下来问用户，不要自己决定**：`next` 末尾列出的"等用户确认"的条目——抓取失败（换链接、粘贴正文，或 `skip`）、正文偏短或疑似付费墙（看一眼 `article.md`，确认内容完整才 `confirm`，否则请用户粘贴正文）。其余条目照常做完，最后一起问，不要让一条坏链接卡住整批。
4. **收尾**：`next` 显示"能做的都做完了"后运行 `checklist`，再运行 `status`，把看板（`article2media-out/batches/<批次>/queue.md`）的表格贴给用户：每条的产物路径、失败和跳过的原因、发布清单里的 ✗ / ⚠。

## 发布之后

- **发布清单**：单篇也可以出，`node ${CLAUDE_SKILL_DIR}/scripts/batch.mjs checklist <工作目录>` 写 `publish.md`：每个平台按顺序上传哪些文件、标题候选（`content.json` 的 `xhs.title` / `wechat.title` 加 `publish.titles` 里的备选）、正文、标签、封面，以及平台硬性限制的 ✓ / ✗（小红书标题 ≤ 20、正文 ≤ 1000、图 ≤ 18；公众号标题 ≤ 64、摘要 ≤ 120）。有 ✗ 先改 content.json 再出。
- **记数据**：用户说"发了"或报数据时，记到这篇的工作目录里（`publish.json`）。发了什么（形式、主题、封面版式、张数、标题）脚本自己从产物里读，只有读错时才用 `--form / --theme / --cover / --title` 改；用户没给的数字不要填、不要估。
  ```bash
  node ${CLAUDE_SKILL_DIR}/scripts/stats.mjs add <工作目录> --platform xhs --url <链接> --views 1200 --likes 80 --saves 150 --comments 9 --shares 12 --follows 5
  node ${CLAUDE_SKILL_DIR}/scripts/stats.mjs list <工作目录>
  node ${CLAUDE_SKILL_DIR}/scripts/stats.mjs report            # 汇总 ./article2media-out 下所有记录，写 stats-report.md
  ```
  平台：`xhs` 小红书、`wechat` 公众号、`x`、`douyin` 抖音、`channels` 视频号、`weibo`、`other`。数据名各平台叫法不同：`--views` 阅读 / 曝光 / 播放，`--likes` 点赞，`--saves` 收藏，`--comments` 评论，`--shares` 转发 / 分享，`--follows` 涨粉。同一篇过几天再报数据，再运行一次 `add` 就多一次快照。
- **看报告**：用户问"哪种效果好"时运行 `report`，把结论照实说：n < 5 的组报告里标着"样本不足，仅供参考"，转述时要带上这句，不要把两三条帖子的差别说成规律。选主题时怎么用这份报告，见 `references/styles.md` 的选择指南。
