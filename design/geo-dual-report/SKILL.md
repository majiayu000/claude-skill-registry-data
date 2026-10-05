---
name: geo-dual-report
description: 当任意 GEO 技能已产出分析报告 MD（审计/调研/竞品/可引用性/技术/绩效等）后，须用本 skill 生成同 basename 的专业 HTML 可视化报告（Chart.js、KPI 卡、CSS 动效）。监测专用仍用 geo-monitor-report。
---

# GEO 分析报告 HTML 同步（双交付）

**规则**：凡 GEO Tab 下产出的**报告/分析类** `.md`（非成稿正文、非 llms.txt/schema），必须 **先完成 MD 落盘**，再同步生成 **同名 `.html`**。

**顺序（硬约束）**：`write_file {basename}.md` → `read_file` 确认 → `read_skill geo-dual-report` → `write_file {basename}.html`。禁止跳过 MD 直接写 HTML。

| MD 示例 | HTML |
|---------|------|
| `aeo-audit.md` | `aeo-audit.html` |
| `keywords.md` | `keywords.html` |
| `competitor-visibility.md` | `competitor-visibility.html` |
| `monitor-report.md` | 走 `geo-monitor-report` → `geo-monitor-report.html` |

权威绑定表：`config/geo-dual-report.manifest.json`

## 工作流（每份分析 MD 执行一次）

0. **前置**：确认 `{basename}.md` 已由上游 skill write_file 落盘；若不存在须先补写 MD，**禁止**本步替代写作
1. **读 MD**：`read_file` 提取标题、摘要、分数、表格、P0/P1 行动项
2. **写数据侧car**（可选但推荐）：`{basename}-data.json`
   ```json
   {
     "title": "报告标题",
     "subtitle": "品牌/站点 · 日期",
     "score": 78,
     "kpis": [{"label":"综合分","value":"78"}],
     "charts": [
       {"id":"main","kind":"dimensionRadar","title":"维度得分","labels":["技术","可引用"],"values":[80,65]}
     ],
     "sections": [{"heading":"发现","html":"<p>…</p>"}],
     "actions": [{"priority":"P0","text":"修复 llms.txt"}]
   }
   ```
3. **复制模板** [templates/geo-report-base.html](templates/geo-report-base.html) → `{basename}.html`
   - 同目录复制 [`geo-report-theme.css`](templates/geo-report-theme.css) 与 [`geo-chart-theme.js`](templates/geo-chart-theme.js)，或**内联** CSS/JS 以保证任务目录自包含
   - 区块容器保留 `data-ngrs-*` 与 `data-nova-block-id`（供 SuperPreview HTML Studio 结构化编辑）
4. **注入**：替换 `{{TITLE}}`、`{{SUBTITLE}}`、`{{REPORT_TYPE}}`；将 JSON 写入 `<script id="report-data" type="application/json">`
5. **校验**：HTML 含 ≥2 个图表（`charts[].kind` 来自 ChartCatalog）、KPI 区、行动项区；与 MD 结论一致

## 报告类型与 ChartCatalog

权威图表注册表：`config/geo-chart-catalog.json`  
视觉规范：**NGRS v1** — [`docs/geo-report-design-system.zh-CN.md`](../../docs/geo-report-design-system.zh-CN.md)

| type | 推荐 kind（≥2 张） |
|------|---------------------|
| audit | scoreGauge, dimensionRadar, severityStackedBar |
| research | keywordHorizontalBar, topicPolarArea, intentDoughnut |
| competitor | competitorGroupedBar, sovDoughnut, gapWaterfallBar |
| citability | sectionRadar, paragraphHorizontalBar, beforeAfterBar |
| technical | checklistProgressBar, severityDonut, dimensionRadar |
| performance | trendLineArea, kpiSparkGrid, channelGroupedBar |
| generic | summaryBar, distributionDoughnut |

- 使用 `kind` 字段（非自造 `type`）；旧 kebab id（如 `keyword-bar`）经 alias 仍可识别
- KPI 可附 `sparkline: [1,2,3,…]` 内嵌趋势迷你图
- **禁止**自造 Chart.js options 或配色

## 视觉规范（NGRS v1）

- Nova Graphite 冷色：见 `geo-report-theme.css`（`--ngrs-accent` 等 token）
- 深色模式 `prefers-color-scheme: dark` 自动适配
- 页面动效：fadeUp + stagger；图表：Chart.js animation preset；KPI：countUp + scoreGauge 环
- Chart.js 4.x CDN + `NGRS.createChart(kind, canvas, cfg)`

## 禁止

- 未 write_file / read_file 源 MD 即写 HTML
- 只交付 MD 无 HTML（分析/报告类）
- 用 `od-data-report` 替代 GEO 审计/调研类 HTML（监测除外且应用 geo-monitor-report）
- 成稿正文 `optimized.md`、平台 `drafts/*.md` 不强制 HTML（可选摘要页）

## 与其他 skill 关系

- **geo-monitor-hub** 聚合后 → **geo-monitor-report**（监测三件套，本 skill 不替代）
- 其他 GEO 分析 skill 写完 MD 后 → **本 skill**

## HTML Studio / `<html-edit>`（用户 UI 复杂改动）

当用户在 SuperPreview 选择「请 AI 协助修改版式」时，Composer 会注入：

```
@artifacts/.../report.html
<html-edit>具体修改说明</html-edit>
```

Agent 须：

1. `read_file` 目标 HTML 与 sibling `geo-report-theme.css` / `geo-chart-theme.js`
2. 用 `write_file` / `edit_file` 改文案与布局，**禁止**改 `<script id="report-data">` 内 Chart 数据结构除非用户明确要求
3. 保持 `data-ngrs-*` 与 `#report-data` JSON 字段一致
4. 完成后简短告知保存路径，勿贴整页 HTML
