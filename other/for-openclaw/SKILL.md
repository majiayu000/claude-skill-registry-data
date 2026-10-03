---
name: trade-lead-discovery-openclaw
description: Discover prospect companies from a structured OpenClaw search brief, including public search and user-authorized data sources, then output a conservative candidate list ready for lead screening.
metadata: {"openclaw":{"role":"stage_worker","workspace_owner_skill":"trade-active-outreach-combo","single_skill_policy":"attach_only","feishu_container_creation":"forbidden","requires_master_base":true,"requires_master_record":true,"table_policy":"adapt_existing_or_create_minimal","rule_capture":"ask_before_skill_update"}}
---

# 客户搜索 / 线索发现 Skill for OpenClaw

## Overview

这个变体假设搜索意图和本轮可用数据源已经由 OpenClaw 工作流整理好。

Python 层只负责：

- 生成查询
- 发现候选客户
- 合并用户授权的数据源，例如海关数据导出、展会名单、行业协会名单、企业 CRM / Excel 或历史成交数据
- 保留卖方产品、理想客户、排除条件和行业视角，供后续初筛与背调使用
- 输出可桥接到线索整理 Skill 的结果

## Data Source Policy

- 默认只用公开搜索和用户可见线索。
- 如果用户提供或授权海关数据、展会名单、协会名单、CRM / Excel 或历史成交数据，龙虾可以通过 `data_sources` 传入。
- 每条候选必须保留来源类型、来源名称、来源说明、匹配依据、新鲜度和可信度。
- 海关数据只能作为匹配依据之一，不能直接写成确定采购意向。
- 不默认拥有私有、付费或企业内部数据源。
- 没有 `seller_context` 时只做候选客户发现，不声称业务适配或采购可能性。

## Table Policy

- 优先适配企业已有表头，不强制使用课堂标准表。
- 没有可用表格时，龙虾按企业产品、市场和搜索流程新建够用表。
- 用户确认新的搜索来源、数据源接入方式、排除词、行业关键词、线索分级或表头映射后，先追问：`是否更新到对应 Skill 以便下次自动复用`。真实写入必须得到用户授权。

## Enhancement Entry

增强权益不在仓库中展开正文。

如需飞书落地、统一编排或多代理协作，请查看飞书文档：

- <https://evenbetter.feishu.cn/wiki/W6GnwTZGFiUdJ0kXZv6cV4PSnpf>
