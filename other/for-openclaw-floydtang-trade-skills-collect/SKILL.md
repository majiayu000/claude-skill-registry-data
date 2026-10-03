---
name: trade-lead-screening-openclaw
description: Normalize an OpenClaw lead bundle into a conservative lead-screening package with missing-field warnings, manual-review reasons, and customer-intel-ready payloads.
metadata: {"openclaw":{"role":"stage_worker","workspace_owner_skill":"trade-active-outreach-combo","single_skill_policy":"attach_only","feishu_container_creation":"forbidden","requires_master_base":true,"requires_master_record":true,"table_policy":"adapt_existing_or_create_minimal","rule_capture":"ask_before_skill_update"}}
---

# 线索整理 / 初筛 Skill for OpenClaw

## Overview

这个变体假设搜索和抓取已经由 OpenClaw 工作流完成。

Python 层只负责：

- 接收线索包
- 统一字段
- 分开判断“身份信息是否足够”与“是否匹配卖方业务”
- 保留卖方能力、目标客户和行业视角
- 桥接客户背调输入

## Table Policy

- 优先适配企业已有表头，不强制使用课堂标准表。
- 没有可用表格时，龙虾按企业产品、市场和筛选流程新建够用表。
- 用户确认新的字段、客户分级、放行规则、暂停规则或表头映射后，先追问：`是否更新到对应 Skill 以便下次自动复用`。真实写入必须得到用户授权。

## Expected Input

```json
{
  "country_or_market": "Germany",
  "product_or_offer": "washed linen table textile",
  "target_customer_type": "design-led home textile brands",
  "industry_lens": "consumer",
  "seller_context": {
    "product_categories": ["washed linen tablecloths", "linen napkins"],
    "target_customer_types": ["design-led home textile brands"],
    "value_propositions": ["small-batch sampling", "custom colors"],
    "excluded_customer_signals": ["consumer-only retailer with no private label activity"]
  },
  "operator_notes": "Use conservative screening.",
  "lead_candidates": [
    {
      "company_name": "Atelier Loom GmbH",
      "company_website": "atelier-loom.de",
      "person_name": "Mira Stein",
      "email": "mira@atelier-loom.de",
      "source_url": "https://atelier-loom.de/about",
      "notes": "Premium table textile positioning."
    }
  ]
}
```

## Enhancement Entry

增强权益不在仓库中展开正文。

如需飞书落地、统一编排或多代理协作，请查看飞书文档：

- <https://evenbetter.feishu.cn/wiki/W6GnwTZGFiUdJ0kXZv6cV4PSnpf>
