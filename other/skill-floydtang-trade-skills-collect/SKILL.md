---
name: trade-lead-discovery
description: Find the first batch of foreign-trade prospect companies from public web, LinkedIn, and user-authorized data sources such as customs exports, trade show lists, association directories, CRM/Excel files, or historical customer data, then output a conservative, structured candidate list ready for lead screening.
---

# 客户搜索 / 线索发现 Skill

## Overview

用这个 Skill 把“知道大概要找哪类客户，但不会系统搜客户”的问题，变成可复用的候选客户发现流程。

默认能力是公开网页和 LinkedIn 线索发现；当用户提供或授权更好的数据源，例如海关数据导出、展会名录、行业协会名单、同行内推清单、企业 CRM / Excel 或历史成交数据时，本 Skill 会把它们接入同一套来源证据分层。

角色：`客户搜索员`

- 负责找出第一批候选客户线索
- 下游对接 `线索整理skill/`
- 不负责深度背调、客户价值判断或开发信生成
- 当前定位是候选客户发现，不是精准客户承诺

## Standard Input

输入统一为 JSON：

```json
{
  "product_or_offer": "frozen mixed vegetables",
  "target_market": "Poland",
  "customer_type": "importer",
  "industry_lens": "food",
  "seller_context": {
    "company_name": "Ningbo FreshGrow Foods",
    "product_or_offer": "frozen mixed vegetables",
    "product_categories": ["frozen vegetables"],
    "target_customer_types": ["importer", "private-label buyer"],
    "target_industries": ["frozen food"],
    "value_propositions": ["stable specifications", "supply reliability"],
    "authorized_materials": ["authorized capability sheet"]
  },
  "search_keywords": [
    "frozen food importer",
    "private label frozen vegetables"
  ],
  "must_include": [
    "retail"
  ],
  "exclude_terms": [
    "job",
    "recruitment"
  ],
  "max_results": 6,
  "notes": "",
  "data_sources": [
    {
      "source_type": "customs",
      "source_name": "Poland frozen vegetable customs export",
      "authorization_status": "user_provided",
      "input_format": "records",
      "source_url_or_note": "User-provided export file",
      "records": [
        {
          "importer_name": "GreenHarvest Foods",
          "country": "Poland",
          "hs_code": "0710",
          "product_keywords": "frozen vegetables",
          "trade_period": "2025 Q4"
        }
      ]
    }
  ]
}
```

## Workflow

1. Normalize search inputs, seller context, industry lens, available data sources, and authorization status.
2. Build public search queries when public search is available.
3. Search public-web results and LinkedIn company-result clues.
4. Merge user-authorized data sources such as customs exports, trade show lists, association directories, CRM/Excel files, or historical customer data.
5. Dedupe raw results by URL, website, LinkedIn URL, or normalized company name.
6. Group results into candidate companies using website, LinkedIn URL, normalized company name, or imported source record.
7. Grade each candidate conservatively with `evidence_grade` and `next_action`.
8. Build a structured candidate list with source links, source type, source name, match basis, freshness, confidence, visible contact clues, evidence summary, and follow-up suggestions.
9. Generate a lead-screening bridge payload that preserves `product_or_offer`, `seller_context`, target customer type, and `industry_lens`.

## Output Requirements

- 必须包含查询摘要
- 必须包含结构化候选名单
- 必须包含来源链接
- 必须包含至少官网或 LinkedIn 线索字段
- 必须包含 `evidence_grade`
- 必须包含 `match_reason`
- 必须包含 `missing_fields`
- 必须包含 `evidence_summary`
- 必须包含 `next_action`
- 必须包含 `follow_up_suggestion`
- 必须包含 `source_type`
- 必须包含 `source_name`
- 必须包含 `source_url_or_note`
- 必须包含 `match_basis`
- 必须包含 `freshness`
- 必须包含 `confidence`
- 必须包含可桥接到 `线索整理skill/` 的输出
- 必须把我方产品和授权资料上下文完整传给线索整理，不在阶段切换时丢失
- 不能把搜索结果写成客户价值判断
- 不能越权替代 `线索整理skill/` 做标准化初筛
- 不能越权替代 `客户背调skill/` 做证据驱动背调
- 没有真实公开来源时，不能强行推进下一步
- 不能声称默认拥有私有、付费或企业内部数据源
- 海关数据只能作为线索匹配依据，不直接等同为采购意向

## Main Scripts

- [build_lead_discovery_report.py](./scripts/build_lead_discovery_report.py)
- [build_lead_screening_input.py](./scripts/build_lead_screening_input.py)

### Example

```bash
python3 ./scripts/build_lead_discovery_report.py --input-json ./examples/frozen-food-search.json
```

```bash
python3 ./scripts/build_lead_screening_input.py --input-json ./examples/frozen-food-output.json
```

```bash
python3 ./scripts/run_regression_checks.py
```

## Defaults

- 允许联网
- 默认只用公开结果，不用登录态
- 用户提供或授权数据源后，可合并海关数据、展会名单、行业协会名单、CRM / Excel 和历史成交数据
- 只做候选发现，不做深度背调
- 默认输出搜索阶段状态：`ready_for_screening | needs_enrichment | hold_for_manual_review | reject_low_evidence`

## Table and Rule Capture

- 本 Skill 输出标准化候选线索能力，不要求企业使用固定表格模板。
- 写入企业表格时，先沿用用户已有表头，再映射 `company_name`、`company_website`、`source_url`、`source_type`、`source_name`、`match_basis`、`freshness`、`confidence`、`evidence_grade`、`next_action` 等标准字段。
- 用户没有可用表格时，龙虾可以按产品、市场和搜索流程新建够用表。
- 当用户确认新的搜索来源、数据源接入方式、排除词、行业关键词、线索分级或表头映射后，必须追问：`是否更新到对应 Skill 以便下次自动复用`。真实写入必须得到用户授权。

## Data Source Principle

同样的工具，企业自己的数据源越好，跑出来的候选客户就越快、越准。本 Skill 会持续保留更多数据源接入位，但不会默认拥有海关数据账号、付费数据库或企业内部客户资料；这些来源必须由用户提供、授权或以公开方式可访问。

## Enhancement Entry

如需数据留存、统一编排、多代理协作或飞书落地，请查看飞书文档：

- <https://evenbetter.feishu.cn/wiki/W6GnwTZGFiUdJ0kXZv6cV4PSnpf>
