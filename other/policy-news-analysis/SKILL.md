---
name: policy-news-analysis
description: Analyze policy documents and current affairs for decision signals using a seven-step framework with pre-analysis knowledge diagnosis and active knowledge-gap filling. Use for policy/event interpretation, impact analysis, and action-oriented briefings (not plain summaries). Supports source labeling ([数据库]/[推断]/[待验证]/[知识缺口]/[外部补充]/[外部补充:browser]) and SQLite knowledge sedimentation.
---

# Policy News Analysis Skill

1. Confirm audience first: investor / industry practitioner / business operator / researcher-media.
2. Run Step 0 before analysis: identify domain tags and explicit knowledge-gap hypotheses.
3. Query SQLite directionally (no full-table scans):
   - `domain_knowledge`
   - `historical_reference`
   - `current_state`
4. Execute workflow in strict order:
   - Step 1 anomaly scan
   - Step 2 self-explanation from source material
   - Step 3 external explanation for anomalies
   - Step 4 priority from ordering/structure
   - Step 5 logic-closure subtraction
   - Step 6 changed vs unchanged (must reach wording-level, not only policy-tone)
   - Step 7 global external calibration
   - Step 8 synthesize investor decision summary (delivery layer)
5. If a **critical-node** knowledge gap blocks the core logic chain, run active gap-filling flow (mandatory, cannot skip):
   - Level 1: SQLite retry
   - Level 2A: built-in web search/fetch (single factual query)
   - Level 2B: `agent-browser-clawdbot` only for deep page navigation
   - Evaluate source quality/time-validity/logic consistency before use
6. Mark sources and uncertainty explicitly:
   - `[数据库]` database-backed
   - `[推断]` analyst inference (not directly stated in source)
   - `[待验证]` uncertain external data
   - `[知识缺口]` missing critical knowledge
   - `[外部补充]` external search supplement
   - `[外部补充:browser]` browser-based supplement
7. Never mix `[推断]` into source-grounded conclusions.
8. Output full knowledge sedimentation content (records), then write to SQLite via script. Do not report counts only.
9. Follow reference markdown format strictly. Do not reorder/merge sections.
10. In knowledge sedimentation JSON, include source annotation fields for each record:
   - `source_type`: A(政策原文) / B(官方解读) / C(二手报道)
   - `source_url`: article URL
   - `source_title`: article title
   - `source_quote`: one directly supporting sentence excerpt from source
   - `source_date`: publication date if available
11. If `source_type` is B, append this marker to quote context: `[解读稿引用，非原文条款]`.
12. C-type sources are not allowed for sediment write-back.

## Output structure (required)

A. 分析日志（Step 0~7）
1. 核心信号摘要（<=3句）
2. 信号来源（第1-3步）
3. 核心逻辑链
4. 值得深挖的2-3个关键点（含行动意义）
5. 延续未变部分（含措辞层检查）
6. 知识缺口与待验证事项
7. 知识沉淀包（完整记录内容，不仅计数）

B. 交付摘要（Step 8，必须单独输出）
8. 投资决策摘要（按框架“受众专项输出”模板）

## Resources

- Main framework: `references/openclaw_policy_analysis_framework.md`
- DB init schema: `scripts/init_policy_kb.py`
- Minimal writer: `scripts/write_policy_knowledge.py`

## Commands

```bash
python3 skills/policy-news-analysis/scripts/init_policy_kb.py --db memory/policy_knowledge.db
python3 skills/policy-news-analysis/scripts/write_policy_knowledge.py --db memory/policy_knowledge.db --input /tmp/sediment.json
```
