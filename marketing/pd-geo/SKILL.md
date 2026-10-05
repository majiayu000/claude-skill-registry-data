---
name: pd-geo
description: 当用户希望品牌在 AI 搜索与对话（如 ChatGPT、通义、豆包等）里被优先、准确提及，或要做 AI 搜索可见度、GEO 内容优化、关键词策略、多平台成稿、内容评分与可见度验证、可见度周报时使用。也适用于「AI 里搜不到我们」「想让大模型推荐我们」等表述。执行前请先 read_skill mkt-ai-seo 获取审计框架；评分用 geo_api，验证须先 web_search 再博查（见 references/search-verify.md）。
---

<!-- NOVA-EXEC-BEGIN -->
## Nova Ai-Studio 集成

- 所有产物写入 **`<task-artifact-dir>/`**（STDA；勿自建语义目录 geo/brand）。
- 首文件须为 `geo-aeo-audit-checklist.md`（alias: `audit-checklist.md`）；关键词 `keywords.md`；成稿 `optimized.md` 等保持 Hub 契约 basename。
- **禁止** ask_user_question 挡交付；检索 `web_search` → 博查 fallback（勿 Perplexity）。
- 报告类 `.md` 须 `read_skill geo-dual-report` 同步 `.html`。
<!-- NOVA-EXEC-END -->

# AI 搜索可见度（GEO 总控）

帮助品牌在生成式 AI 回答中被更可靠地引用。通过对话完成全链路，产物写入系统分配的 taskArtifactDir（basename 如 keywords.md、aeo-audit.md）。

## 何时触发

- 要做 AI 搜索可见度审计、关键词矩阵、多平台结构化成稿
- 需要 0–100 内容评分或 AI 搜索提及验证
- 需要可见度周报（可配合 od-data-report）
- 用户提到 GEO、AEO、AI SEO、大模型推荐、AI 搜索验证

## 联网检索顺序（强制）

见 [references/search-verify.md](references/search-verify.md)：

1. **`web_search`**（大模型自带联网，已开启）
2. **博查 Bocha**（`BOCHA_API_KEY` / `tools.webSearch.provider: bocha`；主检索失败时自动 fallback）
3. **勿用** Perplexity API Key、Google 自定义搜索等额外 Key

## 工作流

每步结束检查 [references/resilience.md](references/resilience.md)；**至少落盘一份文件**即视为部分成功。

### 1) 审计框架

`read_skill mkt-ai-seo`，输出可见度审计要点清单 → `audit-checklist.md`（可结合 CORE-EEAT / `geo-aeo-audit`）

### 2) 关键词矩阵

基于品牌、核心优势、竞品（用户未给则用【品牌】占位，不反复问卷），产出口语化长尾与对比型问句 → `keywords.md`

### 3) 多平台成稿

按 [references/platforms/](references/platforms/) 选 1–2 个平台模板，生成结构化稿件 → `drafts/<platform>.md`

### 4) 结构化数据

`read_skill mkt-schema` 或按 skill 内清单，产出 FAQ/Article JSON-LD → `schema.jsonld`

### 5) 优化稿

E-E-A-T、事实密度、品牌自然提及 2–4 次 → `optimized.md`

### 6) 评分与验证

**评分**：调用 **`geo_api`** action `score`（勿自造分数）；`scoring_mode: quick` 时叠加 CORE-EEAT 自检。

**验证**（按 search-verify 顺序）：

1. 对 `keywords.md` 中验证问句逐条 **`web_search`**
2. 可选：调用 **`geo_api`** action `verify`（有博查 Key 时 CLI 可代拉摘要）
3. 汇总 → `verify-report.json`、`report.md`

```json
{"action":"score","brand":"…","advantages":"…","platform":"知乎","content_path":"optimized.md"}
```

```json
{"action":"verify","brand":"…","queries":["最好的 XX 是什么","XX 和 YY 哪个好"]}
```

若 `geo_api` 不可用，按 resilience 写 `score-estimate.md` 与 `verification-plan.md`。**禁止**向用户说明「未配置 Perplexity Key」。

### 7) 可选交付

- **分析报告 HTML 同步**：凡产出报告/分析类 `.md`（审计、调研、竞品、可引用性、技术、绩效等），须 **先 write_file MD 落盘**，再 `read_skill geo-dual-report` 读取 MD 生成同名 `.html`；绑定表见 `config/geo-dual-report.manifest.json`
- HTML 周报（监测专用）：`read_skill geo-monitor-report` → `geo-monitor-report.html`
- 国内草稿：`read_skill yixiaoer`，仅草稿、不公开发布
- 品牌资料入库：`geo_api` `rag_ingest`（有资料时）

## PilotDeck 约定

详见 [references/pilotdeck-setup.md](references/pilotdeck-setup.md)。

## P0 自检

见 [references/checklist.md](references/checklist.md)。

## 用户手册

非技术说明见仓库 `docs/aigeo-user-guide.md`。
