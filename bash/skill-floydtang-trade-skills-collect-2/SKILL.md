---
name: trade-lead-screening
description: Normalize and screen scattered foreign-trade leads into a conservative, structured lead pool that can flow into customer-intel research. Use when an operator has company names, websites, emails, or contact clues from search results and needs a standardized output with missing-field warnings, review flags, next-step suggestions, and customer-intel-ready JSON.
---

# 线索整理 / 初筛 Skill

## Overview

用这个 Skill 把搜索阶段拿到的零散线索整理成统一格式，降低后续进入客户背调前的判断成本。

角色：`线索初筛员`

- 上游：`客户搜索skill/` 或人工整理的候选线索
- 下游：`客户背调skill/`
- 只做字段统一、质量门槛判断和下一步建议

## Standard Input

输入统一为 JSON：

```json
{
  "default_country_or_market": "",
  "operator_notes": "",
  "product_or_offer": "linen table textile",
  "target_customer_type": "importer",
  "industry_lens": "consumer",
  "seller_context": {
    "product_or_offer": "linen table textile",
    "value_propositions": ["small-batch design support"]
  },
  "leads": [
    {
      "company_name": "Nordic Home Textile AB",
      "company_website": "https://www.nordichometextile.example",
      "person_name": "Nadia",
      "email": "",
      "country_or_market": "Sweden",
      "source_url": "https://www.linkedin.com/company/nordic-home-textile-ab",
      "linkedin_url": "",
      "notes": "Found via home textile search results",
      "product_keywords": "linen table textile",
      "source_type": "linkedin",
      "source_name": "public search",
      "source_url_or_note": "LinkedIn company result",
      "freshness": "unknown",
      "confidence": "medium",
      "match_basis": "Matched upstream discovery query."
    }
  ]
}
```

## Workflow

1. Normalize each lead field into a stable shape.
2. Receive upstream search evidence and detect obvious missing fields and risky inconsistencies.
3. Separate identity completeness from `business_fit`; a complete but irrelevant lead must not be treated as qualified.
4. Classify the lead into a conservative bucket.
5. Suggest the next action:
   - `ready_for_customer_intel`
   - `needs_enrichment`
   - `hold_for_manual_review`
6. Keep a legacy-compatible action field for adapter compatibility.
7. Build a `customer_intel_input` payload that preserves seller context, industry lens, product offer, evidence grade, and business-fit reasons.
8. Output the result in JSON and optionally Markdown.

## Output Requirements

- 必须包含汇总统计
- 必须包含每条线索的标准化字段
- 必须包含 `evidence_grade`
- 必须包含独立的 `business_fit`，并说明匹配依据或为什么无法判断
- 必须包含缺失项
- 必须包含人工复核原因
- 必须包含下一步动作建议
- 必须包含 `legacy_recommended_next_action`
- 必须包含兼容客户背调 Skill 的桥接字段
- 不能仅因为公司名、官网和邮箱齐全就判定值得背调
- 不能把推断写成事实
- 不能越权替代 `客户背调skill/` 输出客户情报报告
- 不能越权替代 `开发信skill/` 生成触达文案
- 没有真实公开来源时，不能强行推进下一步

## Main Scripts

默认脚本入口：

- [build_lead_screening_report.py](./scripts/build_lead_screening_report.py)
- [build_customer_intel_batch_input.py](./scripts/build_customer_intel_batch_input.py)

### Example

```bash
python3 ./scripts/build_lead_screening_report.py --input-json ./examples/sample-leads.json
```

```bash
python3 ./scripts/build_customer_intel_batch_input.py --input-json ./examples/sample-output.json
```

```bash
python3 ./scripts/run_regression_checks.py
```

## Defaults

- 优先本地运行
- 不强依赖联网
- 输出偏保守
- 初筛结果只作辅助，不替代人工判断
- 默认阶段动作：`ready_for_customer_intel | needs_enrichment | hold_for_manual_review`

## Table and Rule Capture

- 本 Skill 输出线索标准化和初筛能力，不要求企业迁移到固定表格形态。
- 写入企业表格时，先沿用用户已有表头，再映射公司名、域名、来源、来源名称、匹配依据、新鲜度、可信度、缺失字段、证据等级、推荐下一步等标准字段。
- 用户没有可用表格时，龙虾可以按企业产品、市场和筛选流程新建够用表。
- 当用户确认新的字段、客户分级、放行规则、暂停规则或表头映射后，必须追问：`是否更新到对应 Skill 以便下次自动复用`。真实写入必须得到用户授权。

## Enhancement Entry

如需数据留存、统一编排、多代理协作或飞书落地，请查看飞书文档：

- <https://evenbetter.feishu.cn/wiki/W6GnwTZGFiUdJ0kXZv6cV4PSnpf>
