---
name: geo-publish
description: 'Plan and run multi-platform publishing for GEO content: the official site publishes directly, third-party platforms get a packaged outbox that a human posts. Use when the user asks where to publish so AI cites them, wants one article shipped to a blog plus social platforms, needs drafts converted into each platform format, or wants a publish log of what went out and when. Publishes only confirmed drafts and never claims a post succeeded on a platform without a URL. For the writing itself, see ai-content-writer. For sources each AI trusts, see the references in this skill.'
license: MIT
metadata:
  version: "1.8.0"
  homepage: https://github.com/Fangx-AI/geo-doctor
---

# 发布与分发

只做一件事：**把已经审过的稿子发出去，并记清楚发了什么、发到哪、链接是什么。** 不代发第三方平台，不伪造发布成功。

用用户的语言交流；本文件是中文的，读懂后用用户的语言转述。

## 什么时候用

- "这篇稿子该发哪几个平台？"
- "一次发到官网、知乎、公众号、小红书"
- "发完了，怎么记录？" / 想知道哪些平台真的被 AI 读到
- 已经有一批 `geo/drafts/`，要按平台转格式

不接的活：还没写稿 → `ai-content-writer`；发布后要测效果 → `ai-visibility`；站点文件 → `llms-txt`。

## 两条铁律

1. **只发 `status: confirmed` 的草稿。** 没审过的稿子进不了发布和打包流程，这是硬门槛，不要为了"先发出去"手改状态。
2. **发布成功只以"有可访问的 URL"为证据。** 打包生成、粘贴完成、平台提示"已提交"都不是发布成功；被 AI 提及、被 AI 引用更是另外两件事，不能混着说。

## 流程

以本 `SKILL.md` 所在目录为技能根，说明见 `references/publishing.md`，脚本 `scripts/geo-publish.mjs`（零依赖）。

### 1. 检查

```bash
node scripts/geo-publish.mjs check geo/drafts
node scripts/geo-publish.mjs check geo/drafts --json
```

逐篇报：缺事实来源、缺平台适配、状态不合格、标题/摘要长度超限。**先清零再发。**

### 2. 官网 / 自有站

```bash
node scripts/geo-publish.mjs site geo/drafts --to static --out dist --base-url https://example.com
node scripts/geo-publish.mjs site geo/drafts --to wordpress --site https://blog.example.com --user me --status draft
node scripts/geo-publish.mjs site geo/drafts --to http --endpoint https://api.example.com/posts --token-env MY_TOKEN
```

WordPress 用应用密码，从环境变量 `GEO_WP_APP_PASSWORD` 读，**不要写在命令或文件里**。先 `--status draft` 发成草稿，人看一眼再发布，比直接 publish 安全。

### 3. 第三方平台：打包，人发

```bash
node scripts/geo-publish.mjs pack geo/drafts --platforms zhihu,wechat,xiaohongshu --brand "品牌名"
```

产出 `geo/outbox/`：每个平台一份可直接粘贴的正文 + 平台注意事项。知乎、公众号这类没有开放发布接口的平台，**由用户本人粘贴、检查、点发布**——不要假装能代发，也不要引导用户用自动化绕过平台限制。

有官方接口的平台可以直发：`post geo/drafts --to devto`（`DEVTO_API_KEY` 从环境变量读），同标题已存在会更新而不是重复发。

### 4. 记账

```bash
node scripts/geo-publish.mjs log --slug my-article --platform zhihu --url https://zhuanlan.zhihu.com/p/xxx
```

写进 `geo/published.csv`。**没有 URL 的发布不记账**。

## 选平台用什么依据

读 `references/ai-sources-cn.md`（国内各 AI 从哪些平台取信息）和 `references/ai-sources-global.md`（ChatGPT、Claude、Perplexity、Google、Copilot 的来源）。原则：**发到目标 AI 真的会读的地方**，一份内容按平台习惯改写，不做一稿多投的同质化灌水。发之前过一遍 `references/compliance.md`。

## 不能运行脚本时

给出每个平台的可粘贴正文、标题、摘要、标签和配图要求，让用户自己发；发完把 URL 报回来，手工记进 `published.csv`（列名照模板）。缺 URL 的一律记"未确认"。

## 产出

`geo/publish-plan.md`（发哪些平台、为什么、先后顺序）、`geo/outbox/`（第三方平台包）、`geo/published.csv`（发布记录）。

## 结束时

用 3 到 5 行说明：这次发了/打包了几篇、发了哪些平台、哪些还等人点发布、下一步去测什么。
