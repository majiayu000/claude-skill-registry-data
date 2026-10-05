---
name: geo-monitor-hub
description: 当用户要做 GEO/AEO 监测总编排、主流大模型收录矩阵聚合、多引擎可见度采集、竞品 SOV 对比、写入 monitor-data.json 时使用。Layer2 聚合：协调 geo-visibility-probe、mcp-agent-aeo、geo-rank-track、mkt-brand-mention 等，统一 llm_coverage 与指标 schema。
---

# GEO 监测总编排（Layer2）

将多源监测数据聚合为 **单一 `monitor-data.json`**（含 **`llm_coverage` 主流大模型收录矩阵**），供 `geo-monitor-report` 生成双格式报告。

## 何时触发

- 用户要「GEO 监测」「AI 可见度」「大模型收录分析」「可见度仪表盘」
- 流程模板 `geo-monitor-dashboard` / `geo-monitor-loop` / `geo-monitor-weekly`
- 已有 probe-results / 部分采集，需合并

## 能力边界

- **收录矩阵只合并一次**：以 `geo-visibility-probe` 的 `llm_coverage` 为主；`mcp-agent-aeo` 补国际引擎 citation；**禁止**在 hub 内重复跑全量问句探测
- `mkt-brand-mention` 仅补充公开提及摘要（可选字段），不写入 `llm_coverage.models`
- `geo-competitor-analysis` 产出独立报告，不替代 monitor 三件套

## 工作流

1. **确认主体**：`subject`（brand/product/event）+ 品牌/站点 + 竞品（≤3）+ 问句（8–12）
2. **采集**（按 Key 降级，`status: skipped` 仍保留占位行）：
   - **收录矩阵**：`read_skill geo-visibility-probe` → `llm_coverage`（必测 11 模型，见 `config/geo-llm-coverage-required-models.json`）
   - 国际 citation：`mcp-agent-aeo`（有 `AGENTAEO_API_KEY`）→ 合并到 models 中国际 id
   - 排名/公开提及：`geo-rank-track`、`mkt-brand-mention`（**不**重复矩阵）
   - 技术快照：可选 `geo-aeo-audit` 四维分 → `dimensions`
3. **聚合** → `monitor-data.json`（须符合 `config/geo-monitor-schema.json`）
   - 从 `llm_coverage.models` **派生** `engines[]`（id/name/score 对齐，避免双份维护）
   - 合并 `actions`：probe 的 `optimization[]` + 技术/竞品 P0/P1
4. **呈现**：`read_skill geo-monitor-report` → `monitor-report.md` + `geo-monitor-report.html`

## monitor-data.json 最小字段

```json
{
  "brand": "示例品牌",
  "subject": { "type": "brand", "name": "示例品牌", "aliases": [], "keywords": [] },
  "site": "example.com",
  "generated_at": "ISO8601",
  "overall_score": 0,
  "llm_coverage": {
    "coverage_score": 0,
    "summary": "",
    "models": [],
    "gaps": [],
    "optimization": []
  },
  "engines": [],
  "competitors": [],
  "queries": [],
  "dimensions": { "technical": 0, "citability": 0, "schema": 0, "entity": 0 },
  "trend": null
}
```

## 历史对比

若存在 `tools.geo.monitorHistoryDir` 下上次 JSON，写入 `trend.previous_run_at`、`score_delta`、`coverage_score_delta`。

## 交付（强制三件套）

- `monitor-data.json`（**必须含 `llm_coverage`**，**必测 11 模型 id 齐全**：国内 doubao/deepseek/qwen/baidu/kimi/yuanbao + 国外 openai/gemini/claude/grok/meta；缺 Key 须 skipped 占位）
- `monitor-report.md`（须含「主流大模型收录分析」与「优化建议」章节）
- `geo-monitor-report.html`

写入系统分配任务目录，禁止语义子目录 `artifacts/`。
