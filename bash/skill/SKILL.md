---
name: trade-customer-intel
description: Build bilingual, evidence-backed, SIEGER v2 customer intelligence reports for foreign-trade leads. Use when OpenClaw or a sales operator needs claim-level citations, decision gates, an industry-specific analysis lens, a non-fabricated verdict card, and sales angles that require approval before downstream outreach drafting.
---

# Trade Customer Intel

## Overview

Use this skill to turn sparse lead data into a structured public-web due-diligence report for sales development. This is the core judgment layer of the whole outreach chain: customer search finds candidates, lead screening cleans them, but this Skill decides what is actually worth saying before the email Skill drafts anything.

角色定位：

- `客户情报分析员`
- 负责基于公开网页证据完成客户背调与风险判断
- 负责识别近期客户动态、市场变化、合规/关税/贸易环境信号
- 负责给开发信 Skill 提供清晰、可引用、可复核的销售切入点
- 不负责批量搜客户，也不负责替代人工直接外发邮件
- 必须明确是否允许进入开发信阶段

上下游关系：

- 上游：`线索整理skill/` 输出的 `customer_intel_input`，或人工提供的稀疏 lead 信息
- 下游：`开发信skill/`

当前最稳的是公司级背调主线。联系人、职位和个性化信号只作辅助。

## Workflow

1. Normalize input into the standard shape:

```json
{
  "company_name": "",
  "person_name": "",
  "email": "",
  "company_website": "",
  "country_or_market": "",
  "product_or_offer": "",
  "industry_lens": "auto",
  "seller_context": {
    "company_name": "",
    "product_or_offer": "",
    "product_categories": [],
    "target_customer_types": [],
    "target_industries": [],
    "value_propositions": [],
    "proof_points": [],
    "authorized_materials": [],
    "forbidden_claims": []
  },
  "notes": ""
}
```

2. If only an email is present, extract the email domain and treat it as the first company clue.
3. Search in this order:
   - Official website and domain evidence
   - LinkedIn company page and personal profile
   - Facebook and Instagram
   - X/Twitter and YouTube
   - General web search and news
4. Extract recent and market signals:
   - Recent customer signals: LinkedIn updates, social posts, news, hiring, funding, expansion, new warehouse, channel changes, product launches.
   - Market signals: target-market regulation, certification, tariff, trade agreement, compliance, import/export rule changes.
   - Every signal must keep source, time or period when visible, freshness, confidence, and product relevance.
5. Resolve identities conservatively:
   - Prefer direct identifiers over inference.
   - Do not merge ambiguous people or companies unless multiple signals line up.
   - Mark weak conclusions as inference, not fact.
6. Convert raw sources into an `evidence_ledger`; every item receives an `EV-*` ID and source-quality label.
7. Convert facts, inferences, and hypotheses into a `claim_ledger`; every claim receives a `CL-*` ID and references its supporting evidence.
8. Apply the selected industry lens. Industrial accounts emphasize BOM and component clues; food accounts emphasize SKU, channel, certification, packaging, and cold-chain clues.
9. Run identity, evidence, seller-offer, product-fit, and risk decision gates.
10. Assemble the SIEGER v2 report using [report-template.md](./references/report-template.md).
11. Score only when at least three verdict dimensions have evidence-backed ratings; otherwise return `score = null` and `customer_grade = 未分级`.
12. Generate sales angles as `proposed`; this Skill must never approve its own angle.

## Main Script

Use [build_customer_intel_report.py](./scripts/build_customer_intel_report.py) as the default entrypoint.

Contracts:

- [customer-intel-input.schema.json](./schemas/customer-intel-input.schema.json)
- [customer-intel-report.schema.json](./schemas/customer-intel-report.schema.json)

### Example run

```bash
python3 ./scripts/build_customer_intel_report.py --input-json /path/to/input.json --markdown-out /tmp/customer-intel.md --json-out /tmp/customer-intel.json
```

Or pipe JSON directly:

```bash
cat <<'EOF' | python3 ./scripts/build_customer_intel_report.py
{
  "company_name": "Acme Industrial",
  "person_name": "Jane Smith",
  "email": "jane@acme-industrial.com",
  "country_or_market": "United States"
}
EOF
```

### Script behavior

- If `tvly` is installed, the script uses it first for web search.
- If `tvly` is not installed, the script falls back to DuckDuckGo HTML search.
- If evidence is sparse, the script still produces a report and explicitly flags low confidence.
- If one or more providers fail, preserve the errors in `collection_errors`; do not convert a collection outage into a successful intel decision.
- Reject malformed identity or nested context types instead of coercing them to strings.
- Create missing parent directories for requested JSON and Markdown outputs.

## Output Requirements

- Keep the report structured and CRM-friendly.
- Keep core analysis in Chinese.
- Include English wording in the `Executive Summary` and `Sales Angles` sections.
- Attach source URLs to every material claim when possible.
- Use `Low`, `Medium`, or `High` risk ratings only.
- Include `IntelDecision` with evidence sufficiency and next action.
- Include `decision_brief`, `evidence_ledger`, `claim_ledger`, and `decision_gates`.
- Every factual claim must reference at least one `evidence_id`.
- Preserve `seller_context` and the resolved `industry_lens` in the report.
- Include the SIEGER Verdict Card, but never fabricate a score to make the report look complete.
- Include `recent_signals` and `market_signals` where evidence supports them.
- Include sales angles with `angle_id`, claim/evidence references, authorized-material references, and `approval_status = proposed`.
- Apply BOM, motor/drive, ASRS, or engineering-fit language only when the resolved `industry_lens` is `industrial` and the selected claims plus seller offer support the concept; never leak that copy into food, consumer, or general reports.
- If the person match is weak, say so explicitly instead of inventing a firm personal profile.
- Keep outreach personalization conservative. Do not invent private preferences or present weak inferences as facts.
- Do not replace `客户搜索skill/` or `线索整理skill/` as the lead-entry stage.
- Do not imply the final outreach draft can skip human review.
- Do not imply stable support for precise personal email discovery.

## Openclaw Integration Notes

- Missing fields are allowed; the report header must list what was missing.
- Only use public internet sources. Do not imply private-data access.

## References

- Read [report-template.md](./references/report-template.md) before changing the output shape.
- Read [source-playbook.md](./references/source-playbook.md) before changing search order, confidence rules, or risk scoring.

## Defaults

- Standard depth, not exhaustive crawling.
- Public web only.
- Conservative entity matching.
- Conservative risk scoring.
- This is the flagship judgment layer in the outreach chain; email drafting should depend on this output instead of inventing recent events.
- The email bridge may only consume an angle after a human or authorized workflow changes its status to `approved`.
- Default intel-stage action: `ready_for_email_draft | hold_for_manual_review`

## Table and Rule Capture

- 本 Skill 输出客户背调和风险判断能力，不要求企业使用固定背调表模板。
- 写入企业表格或知识库时，先沿用已有表头和文档归口，再映射主体可信度、证据充分度、近期信号、市场信号、风险评级、推荐销售角度、推荐下一步、报告引用等标准字段。
- 用户没有可用表格时，龙虾可以按企业产品、市场和背调流程新建够用表。
- 当用户确认新的背调规则、风险分级、近期信号判断、市场信号来源、证据来源权重、行业习惯或表头映射后，必须追问：`是否更新到对应 Skill 以便下次自动复用`。真实写入必须得到用户授权。

## Enhancement Entry

如需数据留存、统一编排、多代理协作或飞书落地，请查看飞书文档：

- <https://evenbetter.feishu.cn/wiki/W6GnwTZGFiUdJ0kXZv6cV4PSnpf>
