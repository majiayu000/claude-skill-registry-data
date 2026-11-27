---
name: planners-method-wiki
description: 检索、应用并维护 Markdown 版可复用策略方法库（Karpathy LLM Wiki）。供 Proposal、Bypage、Video Idea 等内容流程调取分析视角与页面表达结构，也用于从实战方案或方法资料中沉淀新方法。方法库只存通用方法，不提供当前项目的事实或答案。
---

# Planners Method Wiki

> 由阿祖不看 TVC 创建与维护。个人网站 [demyth.info](https://demyth.info)，联系邮箱 `Lawyif@163.com`。

## 目标（OKR）

把策略洞察与「某一页怎么表达、先讲什么后讲什么」的知识沉淀为 **Karpathy LLM Wiki**（Markdown 真源），让 LLM 与人都能直接读写、检索、交叉引用，并生成单文件离线阅读页。

- **真源形态**：`<wiki_dir>/` 包含 `SCHEMA.md`、`index.md`、`log.md` 与 `lenses/<lens_id>.md`（默认自带 `<Skill>/base-wiki`，11 个模块、33 个基础方法、22 个变体）。
- **铁律**：只存去项目化的思考框架、判断条件、失效边界与 `页面表达结构`；绝不替当前项目捏造事实结论或跳过 `planners-fact-check`。

## 工具（3 个脚本，零 JSON 审阅中间层）

| 命令 | 用途 |
|---|---|
| `node "<Skill>/scripts/query-wiki.mjs" --query "<关键词>" [--wiki-dir <Wiki>] [--module <mod_id>] [--limit 5] [--text]` | 按中英文分词检索 `lenses/*.md`，返回匹配分数、原文绝对路径与页面表达摘要 |
| `node "<Skill>/scripts/lint-wiki.mjs" [--wiki-dir <Wiki>] [--text]` | 校验 `SCHEMA.md`/`index.md`/`log.md`、`lenses/*.md` 的 frontmatter、7 个必填段落、断链与孤儿页（错误退出码 1，`页面表达结构` 待补充出 warn） |
| `node "<Skill>/scripts/build-wiki-viewer.mjs" [--wiki-dir <Wiki>] [--output <wiki-viewer.html>]` | 将 Markdown Wiki 编译为单文件离线阅读页 `wiki-viewer.html` |

## 剧本（Playbook）

### 1. 查询与应用（Query）

1. **确定目标库**：优先使用调用方指定的 `<Wiki>`；未指定时读 `<Skill>/base-wiki`。
2. **两步定位**：先读 `<Wiki>/index.md` 概览模块，或运行 `query-wiki.mjs --query "..."` 找到候选 `lens_id`，再直接 `read_file` 打开对应 `lenses/<id>.md` 全文。
3. **检查适配度**：核对 `适用条件 / 跳过条件 / 所需输入 / 分析操作步骤 / 页面表达结构 / 失效模式`。缺失输入时向调用方提出补证需求，不把方法假设当项目事实。
4. **交接下游**：
   - **Proposal**：采用分析视角检验主线判断，必要时记录采用了哪个 `lens_id`。
   - **Bypage**：重点读取 `## 页面表达结构`，把该方法对应的页面信息排布转化为可编程 PPT 页面的块结构。

### 2. 沉淀与维护（Ingest）

从优秀方案、结案或外部方法资料沉淀新知识时，按 `<Wiki>/SCHEMA.md` 直接编辑 Markdown：

1. **先读规范与现状**：读 `<Wiki>/SCHEMA.md`、`<Wiki>/index.md` 与 `<Wiki>/log.md` 末尾，确认是否已有同类方法或应新增变体。
2. **去项目化抽象**：剔除品牌名、预算数字与当期结论，只保留通用问题、判断条件、操作步骤与 **`## 页面表达结构`**（`P1 · ...` 的论证目的/回答问题/所需证据）。
3. **写页与建链**：新建或修订 `<Wiki>/lenses/<lens_id>.md`（新方法默认 `status: draft`），同步更新 `<Wiki>/index.md` 的对应模块列表，并在 `<Wiki>/log.md` 顶部/尾部追加一条日期记录（含变更说明与来源说明）。
4. **Lint 与交付阅读页**：运行 `lint-wiki.mjs --wiki-dir <Wiki> --text`（零 error）与 `build-wiki-viewer.mjs --wiki-dir <Wiki>`，用浏览器打开 `wiki-viewer.html` 供用户审阅确认后再将 `draft` 改为 `approved`。

## 注意事项

- **不要手写或修改 JSON 索引**：旧版 `wiki-index.json` / `modules/*.json` / 审阅变更集协议已退役，`index.md` 与 `lenses/*.md` 是唯一真源。
- **`build-wiki-viewer.mjs` 只读 `assets/viewer.{css,js}`** 嵌入离线 HTML，不产生网络外链。
