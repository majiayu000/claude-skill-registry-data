---
name: geo-monitor-report
description: 当用户需要 GEO 监测可视化报告、主流大模型收录分析、HTML 仪表盘、monitor-report.md 结论页时使用。读取 monitor-data.json（含 llm_coverage），产出 MD+HTML 双交付；监测类流程末步须 read_skill 本 skill，勿用 od-data-report 凑页。
---

# GEO 监测双格式报告（Layer3）

从 **`monitor-data.json`**（含 **`llm_coverage`**）生成：

| 文件 | 用途 |
|------|------|
| `monitor-report.md` | 结论先行、**主流大模型收录矩阵**、缺口与优化建议、P0/P1/P2 |
| `geo-monitor-report.html` | KPI 卡、收录图表、≥4 图表、NGRS v1 |

## 工作流

1. 读取任务目录内 `monitor-data.json`（若无则先跑 `geo-monitor-hub`）
2. 复制并填充 [templates/geo-monitor-report.html](templates/geo-monitor-report.html)
3. 同目录复制 NGRS 资源：[`../geo-dual-report/templates/geo-report-theme.css`](../geo-dual-report/templates/geo-report-theme.css)、[`../geo-dual-report/templates/geo-chart-theme.js`](../geo-dual-report/templates/geo-chart-theme.js)（或内联）
4. 写 `monitor-report.md`（**固定章节顺序**）：
   - 摘要（主体类型、coverage_score、overall_score）
   - **主流大模型收录分析**（**必测 11 模型**表格：豆包/DeepSeek/千问/百度/Kimi/腾讯元宝 + OpenAI/Gemini/Claude/Grok/Meta；含收录状态/得分/证据）
   - 收录缺口（`llm_coverage.gaps`）
   - **优化建议**（`llm_coverage.optimization`，按 P0→P2）
   - 引擎 SOV / 四维雷达 / 竞品 / 问句命中（简表，不重复矩阵全文）
   - 行动项（合并 `actions`）
5. 校验 HTML：KPI 区 + 至少 4 chart；有 `llm_coverage` 时首图须为 `llmIndexingBar`

## HTML 要求（NGRS v1）

- 视觉规范：[`docs/geo-report-design-system.zh-CN.md`](../../docs/geo-report-design-system.zh-CN.md)
- `NGRS.renderReport` / `NGRS.monitorDataToCharts`（有 `llm_coverage` 时自动用收录条形图）
- 禁止硬编码 Chart options；禁止在本 skill 内重新探测模型

## 模板变量

- `{{BRAND}}`、`{{SITE}}`、`{{OVERALL_SCORE}}`
- 注入完整 `monitor-data.json` 到 `<script id="monitor-data" type="application/json">`

## 禁止

- 不要只交付 Markdown 而无 HTML
- 不要用 `od-data-report` 替代本 skill
- 不要重复编写第二份收录矩阵（矩阵只来自 probe → hub 的 JSON）
