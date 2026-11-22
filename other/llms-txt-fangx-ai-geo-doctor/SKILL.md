---
name: llms-txt
description: 'Build the files AI reads first: llms.txt, facts.json, robots.txt, sitemap.xml and a static fact site generated from a fact card. Use when the user asks for llms.txt, wants a site agents can read without JavaScript, needs machine-readable facts about a product as files, or wants GitHub Pages to publish an AI-readable fact sheet from confirmed facts only. Starts from a fact card that already exists; reconciling scattered sources into that card is ai-content-writer. Generates the site, refuses unconfirmed facts, and explains what llms.txt can and cannot do. For crawl diagnostics, see ai-crawler-audit. For prose that gets cited, see ai-content-writer.'
license: MIT
metadata:
  version: "1.8.0"
  homepage: https://github.com/Fangx-AI/geo-doctor
---

# 给 AI 读的站点与 llms.txt

只做一件事：**把事实变成机器能直接读的文件和页面。** 一次生成，长期维护，不靠人工一页页改。

用用户的语言交流；本文件是中文的，读懂后用用户的语言转述。

## 什么时候用

- "帮我加个 llms.txt" / "llms.txt 该怎么写"
- "AI 读不懂我的官网" / "我的站全是 JS 渲染的"
- "有没有一个页面能让 AI 一次看清我是什么产品？"
- 想把事实卡变成可部署的静态站（GitHub Pages 也行）

不接的活：查为什么抓不到 → `ai-crawler-audit`；写文章 → `ai-content-writer`；发到第三方平台 → `geo-publish`。

## 两个必须先说清的前提

1. **`llms.txt` 不是官方标准，也没有公开证据表明主流 AI 已经普遍读取它。** 它值得做，因为成本极低、人和机器都能读；但不要说"加上就会被引用"。说这种话就是承诺结果。
2. **真正决定能不能被读懂的是正文在 HTML 里、robots 放行、内容可摘录。** `llms.txt` 是锦上添花，不是地基。

## 流程

以本 `SKILL.md` 所在目录为技能根，说明见 `references/llms-txt.md`，脚本 `scripts/geo-site.mjs`（零依赖）。

### 1. 先有事实卡

事实卡来自 `ai-content-writer`（`geo/fact-card.yaml`）。没有就先建：**只有状态为"已确认"的条目会进站点**，其余会让构建失败并点名——这是故意的。

### 2. 生成

```bash
node scripts/geo-site.mjs build --facts geo/fact-card.yaml --out dist --dry-run
node scripts/geo-site.mjs build --facts geo/fact-card.yaml --out dist --base-url https://you.github.io/brand/
```

产出：`index.html`（事实页）、`faq.html`、`llms.txt`、`facts.json`、`robots.txt`；给了 `--base-url` 才会写 `sitemap.xml` 和 canonical。`--drafts geo/drafts` 可把已确认的文章一起生成。

### 3. 部署

`node scripts/geo-site.mjs action` 会写一个 GitHub Actions 工作流：`geo/` 一变就重建、部署到 GitHub Pages、顺手体检。也可以把 `dist/` 部署到任意静态托管。

### 4. 部署后自检

用 `ai-crawler-audit` 体检线上地址，重点看三件事：正文在不在原始 HTML 里、robots 有没有放行、`llms.txt` 和 `facts.json` 能不能直接取到。**只生成不体检 = 没做完。**

## 不能运行脚本时

按 `references/llms-txt.md` 的清单手写这几个文件，并在对话里给出完整可复制内容、注明"待保存"。手写 `llms.txt` 的最小结构：一级标题（站点/产品名）、一句话摘要（这是什么、给谁用）、分节链接清单（每个链接后跟一句说明）。`facts.json` 至少包含产品名、一句话定位、价格、能力、明确不支持的事、更新日期，每条带来源。

## 产出

`dist/`（或用户指定目录）下的站点文件、`.github/workflows/geo-site.yml`（用 `action` 生成）。

## 结束时

用 3 到 5 行说明：生成了哪几个文件、哪几条事实因为未确认被挡住、线上地址是什么、下一步该验什么。
