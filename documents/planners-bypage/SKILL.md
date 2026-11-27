---
name: planners-bypage
description: 将已确认的 Storyline（.planners/storyline.md）或原始多源资料展开为适合编程 PPT 的完整逐页文案（.planners/by-page.md），后台补全来源审计副本并通过独立 planners-fact-check 核查，在实时文字工作台逐块打磨后直接交给 planners-ppt-hell 制作 SVG 与 PPTX。
---

# Planners Bypage

> 由阿祖不看 TVC 创建与维护。个人网站 [demyth.info](https://demyth.info)，联系邮箱 `Lawyif@163.com`。来源信息不默认写入客户交付物。

## 目标（OKR）

做两件事且做到极致：
1. **写出真正适合编程 PPT 的逐页文案（`.planners/by-page.md`）**：不是复述大纲，而是用 `slide-copy` 锤炼结构与金句、参考 `planners-method-wiki` 中方法页的 `## 页面表达结构` 排布页面信息，写清每页的 `正文 / 口播 / 制作`、视觉配图需求与末尾来源出处。
2. **后台完备核查、零未解错交接**：自动补全深层审计副本（`audit_companion`），调用独立 `planners-fact-check` 核查员彻底查验数据、主体、时间、单位与引文后交付文字工作台；人工确认定稿后把 `.planners/by-page.md`（及 `.planners/assets/`）直接交给 `$planners-ppt-hell`。

## 入口路由（复用 vs 新建）

| 入口场景 | 处理方式 |
|---|---|
| 承接 `planners-proposal` 已定稿主线 | **沿用同一** `<Project>/.planners/` 工作目录（含 `storyline.md`、`project-memory.md` 与 `source-index.json`），运行 `import-storyline-doc.mjs` 生成 `.planners/by-page.md` 骨架后展开全文，不得新建另一套目录割裂记忆 |
| 从 `planners-ppt-hell` 或用户直接给零散资料进入 | 建立**新项目工作目录** `<Project>/.planners/`，登记 `source-index.json`（`source-index/2.1.0`）、`project-memory.md` 与 `by-page.md`，不要求前置 Proposal |

## 工具

`<B>` 为本 Skill 根目录，`<K>` 为 `planners-review-core` 根目录，`<D>` 为 `<Project>/.planners/by-page.md`。

| 阶段 | 命令 |
|---|---|
| 从 Storyline 导入 By-page 骨架 | `node "<B>/scripts/import-storyline-doc.mjs" --storyline "<Project>/.planners/storyline.md" --output "<D>"` |
| 后台补全文档提取底账（PDF/Office） | `node "<B>/scripts/prepare-audit-sources.mjs" --source-index "<Project>/.planners/source-index.json"` |
| 校验来源索引（`source-index/2.1.0`） | `node "<B>/scripts/validate-source-index.mjs" "<Project>/.planners/source-index.json"` |
| 校验事实审计接缝 | `node "<B>/scripts/validate-fact-audit.mjs" --audit "<Project>/.planners/fact-audit.json" --copy "<D>"` |
| 校验 By-page 文档结构与页末出处 | `node "<B>/scripts/validate-bypage-doc.mjs" "<D>" [--assets "<Project>/.planners/by-page.assets.json"]` |
| 渲染与校验 Mermaid 示意 SVG | `node "<B>/scripts/render-diagrams.mjs"` / `node "<B>/scripts/validate-diagrams.mjs"`（传 `--manifest`、`--copy "<D>"`，可选 `--assets "<Project>/.planners/by-page.assets.json"`） |
| DSH 侧栏：生成 surface 后调 `review_open` | `node "<K>/scripts/doc-surface.mjs" "<D>"` 与 `doc-command.mjs`（`tasks \| claim \| patch \| complete \| conflicts`） |
| 本地独立宿主：启动文字工作台与收件箱 | `node "<K>/scripts/doc-workbench.mjs" "<D>" --open` 与 `doc-inbox.mjs` |

## 剧本（Playbook）

1. **接手与后台补底账**：接手 `.planners/` 后（或新建 `.planners/`），核对 `source-index.json`；若上游只写了轻量台账，后台运行 `prepare-audit-sources.mjs` 为重点 PDF/Office 文档提取 `audit_companion` 审计底账并更新至 `source-index/2.1.0`。
2. **检索表达结构并写可编程 PPT 正文**：针对每类页面，查 `planners-method-wiki` 方法页的 `## 页面表达结构` 获取页面信息排布参考，并结合 `slide-copy`（高信息密度、结构清晰、短句/对比表/量化结论，避免大段散文）写出 [`contracts/by-page.md`](contracts/by-page.md) 规范的 `.planners/by-page.md`：
   - **正文中不留任何核查角标**（核查结论留在 `.planners/fact-audit.json` 与对话中）。
   - `### 正文` 必填且写清口径、单位、时间与限定；`### 口播` 与 `### 制作` 按需填写（需要示意图时可经 `render-diagrams.mjs` 生成 `.planners/assets/*.svg` 并写明 `source_id`）；每页末尾用 `>` 引用列出出处。
   - 若上游采用简写引用或新引入图片，在 [`templates/content-brief.md`](templates/content-brief.md) 或 `project-memory.md` 中对好对应页码后再落稿。
3. **独立事实核查门禁（交付前必过）**：调动独立的 `planners-fact-check`（代理规则**按该 Skill 的规则复用**；不自己核查自己的稿子），核查 `.planners/by-page.md` 对照 `source-index.json` 生成 `.planners/fact-audit.json`。有已确认错误（`confirmed`）或未覆盖（`no_source`）必须先修稿复核，并运行 `validate-fact-audit.mjs` 通过。
4. **交付实时文字工作台审阅与返修**：先过 `validate-bypage-doc.mjs` 再启动工作台（DSH 用 `doc-surface.mjs` + `review_open`，本地用 `doc-workbench.mjs --open`）。接到批注任务时先看 `task.diff` 识别人的整页增删或拖拽重排，再按锚点加锁并局部 `patch`；正文或来源被改动后必须重新复核事实并更新 `fact-audit.json`。工作台用法见 [工作台操作](references/workbench.md)。
5. **直接交接 `$planners-ppt-hell`**：用户确认 `.planners/by-page.md` 定稿且最新核查通过后，把 `.planners/by-page.md` 与同目录 `assets/`（及 `by-page.assets.json`、`fact-audit.json`、`source-index.json`）直接交给 `$planners-ppt-hell`。`planners-ppt-hell` 的 `init_svg_project.py --source` 会直接解析该 Markdown 生成制作工程。

## 详情参考

- [工作台操作](references/workbench.md) · [交接与返修](references/content-handoff.md) · [事实核查接缝](references/verification.md)
- [图片与图资产](references/image-lifecycle.md) · [示意图渲染](references/diagram-lifecycle.md) · [来源阅读](references/source-reading.md) · [职责与接口](references/architecture.md)
