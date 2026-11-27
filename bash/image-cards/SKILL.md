---
name: image-cards
description: 卡片：固定比例的图文卡片组——小红书 3:4（1080×1440）、Instagram 4:5、方图 1:1、竖屏 9:16，附总览图和发帖文案。两种输入：改写稿 content.json → 总结卡片（封面 + 每节一卡 + 清单 + 要点总结，13 套主推主题）；文章 article.md（原文、译文、逐字稿）→ 原文卡片（整篇按顺序分页成卡片，一字不改，逐块校验）。可以单独用，也可以接在抓取、改写、翻译后面。Use when the user wants 小红书图文, 轮播卡片, 知识卡片, 3:4 / 4:5 / 1:1 / 9:16 cards, Instagram carousel, 朋友圈方图, or 原文卡片 / 全文卡片 / 把全文做成小红书 — from an article or an existing content.json.
argument-hint: <content.json|article.md|目录> [--ratio 3:4|4:5|1:1|9:16 或 小红书/IG] [--covers] [--form quotes|onepage|qa|digest] [--theme 主题名|a,b|all] [--out 目录]
allowed-tools: Bash(node ${CLAUDE_SKILL_DIR}/scripts/*)
version: "2.4.0"
---

# 卡片（image-cards）

> 路径约定：文中的 `${CLAUDE_SKILL_DIR}` 指本 SKILL.md 所在的目录。宿主没有替换这个变量时（命令里原样出现 `${CLAUDE_SKILL_DIR}`），把它换成这个目录的绝对路径再运行；`../<名字>/` 指同级的另一个 skill 目录。

| 输入 | 产出 |
|---|---|
| `content.json`（改写稿） | 总结卡片：`<目录>/<主题>-3x4/card-01.png …`、`overview.jpg`、`caption.md` |
| `article.md`（原文、译文、逐字稿、`rewrite.md`） | 原文卡片：`<目录>/full-3x4/card-01.png …`、`overview.jpg`、`caption.md` |

参数：`$ARGUMENTS`

**比例怎么定**：用户提到小红书、RED、xhs、抖音图文、3:4 → `--ratio 3:4`（默认）；Instagram、IG、4:5 → `4:5`；方图、正方形、朋友圈、1:1 → `1:1`；竖屏、Stories、快拍、9:16 → `9:16`。

## 0. 先确定输入
- 已有 `content.json` → 总结卡片；用户只给了文章、又说"原文 / 全文 / 一字不改" → 原文卡片。
- 给的是链接、文件、粘贴的正文或视频 → 先用 `article-fetch` / `video-transcript` 取原文。
- 只有文章、用户没说原文还是总结 → 卡片默认**改写**：先用 `article-rewrite` 写 content.json（卡片专用字段按 `references/xhs-guide.md` 写）。原文是外文、又要原文卡片 → 先用 `article-translate`。
- 判断规则、工作目录和调用其他能力的方式：`../article2media/references/pipeline.md`。

第一次使用先跑 `node ${CLAUDE_SKILL_DIR}/scripts/doctor.mjs`（Node 22+、Chrome）。

## 1. 总结卡片（content.json）
读 `references/xhs-guide.md`：封面、每张卡只讲一件事、发帖文案（`cover`、`xhs`、`card` 字段）。
```bash
node ${CLAUDE_SKILL_DIR}/scripts/cards.mjs <目录>/content.json --ratio 3:4 --check   # 只校验：会出几张
node ${CLAUDE_SKILL_DIR}/scripts/cards.mjs <目录>/content.json --ratio 3:4           # 出图，一组大约 5 秒
node ${CLAUDE_SKILL_DIR}/scripts/cards.mjs <目录>/content.json --ratio 3:4 --theme brutal
node ${CLAUDE_SKILL_DIR}/scripts/cards.mjs <目录>/content.json --covers                # 只出封面的几个版本，供挑选或对比发布
node ${CLAUDE_SKILL_DIR}/scripts/cards.mjs <目录>/content.json --form onepage          # 轻量形态：onepage 一页看完 | quotes 金句图 | qa 问答卡 | digest 图文速览（X 单帖，最多 4 张）
```
- **封面多版本、轻量形态、品牌包**（头像、品牌色、期号）：xhs-guide.md 第 2.5 节。用户说"多出几个封面""金句图""一张图讲完""问答形式""加上我的头像 / 做成系列"时用；要发 X、转发文章配一组总结图、"最多 4 张讲完"时用 `--form digest --ratio 4:5 --scale 3`。
- 主题：content.json 的 `theme`（可写成 `{"long": …, "cards": …}` 分开指定）；都没有时按 `../article2media/references/styles.md` 选。卡片场景的主题调整见 styles.md 第 3 步。
- **检查（出图 → 发现问题 → 改 content.json 或参数 → 再出图，算一轮；通常 1–2 轮就够。✗ 没修完就继续改；第 2 轮后还剩的 ⚠，交付时说明。只跑 check.mjs 不算）**：先看 `overview.jpg`，有问题再打开单张卡。✗ 必须修；报「内容超出」「已自动省略」「图只放大到 x 倍」时，按 xhs-guide.md 第 2 节的顺序处理（缩短 `card.text`、改 `split`、`skip` 次要的节）。**出图阶段最多 2 轮，到了就停**：剩下的 ⚠ 写进交付说明，不要为了让提示归零删掉面板、图或正文（内容比提示数要紧）。check.mjs 的内容提示仍然处理到 0。只改 content.json 再重渲，不手改 HTML。

## 2. 原文卡片（article.md）
读 `references/original-cards.md` 和 `../article2media/references/verbatim.md`。
```bash
node ${CLAUDE_SKILL_DIR}/scripts/cards.mjs <目录>/article.md --ratio 3:4
node ${CLAUDE_SKILL_DIR}/scripts/cards.mjs <目录>/article.md --ratio 3:4 --theme quiet   # 用主题的颜色与字体
```
全文校验未通过就是错误，不能靠目测放行。看 `overview.jpg` 检查断开的位置；张数超过上限时按 original-cards.md 处理，不删原文。

## 3. 交付
- 卡片目录、张数、每张的尺寸；`overview.jpg` 路径；
- 把 `caption.md` 里的标题、正文和标签**直接贴在回复里**，方便复制（原文卡片要你补标签、必要时缩短标题）；
- 总结卡片：用的主题和理由；换主题 `--theme 名称`、换比例 `--ratio 4:5` 都不用重写内容；
- 原文卡片：原文块数与全文校验结果、生成图 0 张；
- 需要用户留意的地方。
