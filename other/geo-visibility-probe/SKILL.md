---
name: geo-visibility-probe
description: 当用户要探测品牌/产品/事件在主流大模型中的收录与可见度，或做 GEO 监测 Layer1 采集时使用。必测国内豆包/DeepSeek/千问/百度/Kimi/腾讯元宝与国外 OpenAI/Gemini/Claude/Grok/Meta；产出 llm_coverage 矩阵供 hub 合并。
---

# 主流大模型收录探测（Layer1）

对**被查询主体**（品牌 / 产品 / 事件）在主流大模型回答中的**收录状态、提及率、首位推荐、引用来源**做矩阵化探测。

权威字段定义：[`references/llm-coverage-matrix.md`](references/llm-coverage-matrix.md)  
必测清单：[`config/geo-llm-coverage-required-models.json`](../../config/geo-llm-coverage-required-models.json)

## 核心策略（必测 11 模型）

**国内（6）**：`doubao` 豆包 · `deepseek` DeepSeek · `qwen` 千问 · `baidu` 百度文心 · `kimi` Kimi · `yuanbao` 腾讯元宝  

**国外（5）**：`openai` OpenAI · `gemini` Gemini · `claude` Claude · `grok` Grok · `meta` Meta AI  

缺 Key 或不可达时：`status: skipped`，`indexing_status: unknown`，**仍须输出占位行**。不得省略任一必测 id。

## 能力边界（避免重复）

| 能力 | 职责 | 不做什么 |
|------|------|----------|
| **本 skill** | 逐模型收录矩阵 → `llm_coverage` | 不写完整 MD/HTML 报告 |
| geo-monitor-hub | 合并多源 → 单一 `monitor-data.json` | 不重复全量探测 |
| geo-monitor-report | MD+HTML 呈现与优化建议章节 | 不重新探测 |
| mkt-brand-mention | 公开渠道提及与情感 | **不含**逐模型收录 |
| geo-competitor-analysis | 竞品差距与行动清单 | **不含**全量模型矩阵 |
| pd-geo verification-plan | 快检 10 条问句 | **不含**十模型矩阵 |

## 工作流

1. **确认主体**：`subject.type` + `subject.name` + 别名；从用户或 `keywords.md` 取 8–12 条问句
2. **逐模型探测**（必测 11 id，见 llm-coverage-matrix）：
   - 国内：web_search（博查）模拟「用户问 AI」
   - 国外：有 Key 时 `mcp-agent-aeo`，否则 skipped 占位
3. **记录每模型**：`indexing_status`、`indexing_score`、`mention_rate`、`citation_sources`、`evidence_summary`
4. **汇总**：
   - 写入 `probe-results.json` 或 `monitor-data.json` 的 `llm_coverage` + 派生 `engines[]`
   - 校验 `models.length` ≥ 11 且含全部必测 id
   - 计算 `coverage_score`；列出 `gaps[]` 与 `optimization[]`（P0/P1/P2）

## 评分

- `llm_coverage.coverage_score`：有效模型 indexing_score 均值
- `mention_rate` / `top_pick_rate`：问句维度（与旧字段兼容）

## Key 降级

无 AgentAEO 时：国内六模型仍探测；国外五模型 skipped 占位。**勿中断**。

## 交付

- 最小：`probe-results.json`（含完整 11 模型 `llm_coverage`）供 hub 合并
- 完整三件套由 **geo-monitor-hub → geo-monitor-report** 产出
