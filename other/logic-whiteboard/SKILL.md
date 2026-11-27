---
name: logic-whiteboard
description: 白板论证：把一篇文章的推理过程摊成一条纵向主干的长图——问题在上，前提、证据、矛盾、转折、分支逐层往下，停在内容自身的收束处；每段原文都必须进入某一步或写明省略理由（论证账本 + 来源清单校验）。输入是文章（原文、译文、逐字稿）。可以单独用，也可以接在抓取、视频转文字、翻译后面。Use when the user wants a 白板, 论证图, 推理过程图, 思路图, argument map, "把这篇的逻辑画出来", or -w.
argument-hint: <article.md|目录> [--theme 主题名]
allowed-tools: Bash(node ${CLAUDE_SKILL_DIR}/scripts/*)
version: "2.4.0"
---

# 白板论证（logic-whiteboard）

> 路径约定：文中的 `${CLAUDE_SKILL_DIR}` 指本 SKILL.md 所在的目录。宿主没有替换这个变量时（命令里原样出现 `${CLAUDE_SKILL_DIR}`），把它换成这个目录的绝对路径再运行；`../<名字>/` 指同级的另一个 skill 目录。

呈现作者**怎样一步步走到结论**，不是摘要：读者只看成品，也应能复述"为什么下一步从上一步发生"。

参数：`$ARGUMENTS`

## 0. 输入
文章 `article.md`（原文、译文或逐字稿）。给的是链接、文件或视频时，先用 `article-fetch` / `video-transcript` 取原文（见 `../article2media/references/pipeline.md`）。不需要先改写。

第一次使用先跑 `node ${CLAUDE_SKILL_DIR}/scripts/doctor.mjs`（Node 22+、Chrome）。

## 1. 流程
1. `node ${CLAUDE_SKILL_DIR}/scripts/whiteboard.mjs <目录>/article.md`：生成来源清单 `whiteboard-source.json`（每段一个编号和哈希）。
2. **完整读一遍**文章，读 `references/mode-whiteboard.md`，写 `<目录>/whiteboard.json`（论证账本：每段原文必须进入某一步，或写明省略理由）。
3. `whiteboard.mjs <目录>/whiteboard.json --check` 通过后，`whiteboard.mjs <目录>/whiteboard.json` 渲染 → `<目录>/whiteboard/whiteboard.png`。
4. 讲概念、机制的内容，按 `../article-rewrite/references/writing-guide.md` 第 6 节把具体情形、判别依据、关系和结果接起来。

## 2. 审片与交付
- `whiteboard/review/` 里有覆盖全部高度的重叠切片，逐张看完再交付。
- 报告：PNG 路径与像素尺寸、来源、步骤数、可见转折数、来源段落的去向（几段进入步骤、几段省略及理由）。制作范围、是否核对过，写在交付回复里，不写进图里。
