---
name: trade-outreach-email-for-openclaw
description: OpenClaw-native version of the foreign-trade outreach email skill. Use structured operator input plus customer-intel source context to generate conservative first-touch or follow-up email drafts without overstating inferred facts or inventing recent customer events.
metadata: {"openclaw":{"role":"stage_worker","workspace_owner_skill":"trade-active-outreach-combo","single_skill_policy":"attach_only","feishu_container_creation":"forbidden","requires_master_base":true,"requires_master_record":true,"table_policy":"adapt_existing_or_create_minimal","rule_capture":"ask_before_skill_update"}}
---

# 开发信 Skill for OpenClaw

## Overview

这个版本面向 OpenClaw 云端工作流。

它假设操作员输入、公开资料摘要、近期客户信号和市场/合规信号已经由上游客户背调节点整理好，然后由当前脚本进行保守合并，并调用根目录里的核心草稿生成器输出统一结构的邮件包。

## Table Policy

- 优先适配企业已有表头、知识库归口或邮箱草稿箱，不强制使用课堂标准表。
- 没有可用表格时，龙虾按企业产品、市场和跟进流程新建够用表。
- 用户确认新的开发信风格、禁用表达、行业话术、跟进节奏或表头映射后，先追问：`是否更新到对应 Skill 以便下次自动复用`。真实写入必须得到用户授权。

## Inputs

最终输入应为：

```json
{
  "operator_input": {},
  "public_context": {}
}
```

其中：

- `operator_input` 提供邮件场景、产品、目标、发件人等明确业务输入
- 卖方样品能力、禁用承诺等只能来自 `operator_input.seller_context`；公开客户上下文不能替卖方授权
- `public_context` 提供完整五门决策、人工复核状态，以及已批准且证据绑定的 `selected_sales_angle`、`selected_claims`、`selected_evidence`
- `draft_authorization=approved` 只是输入声明；脚本会重新核对五门、SIEGER 状态、风险、主体置信度和 Claim/Evidence 引用，单独一个批准字段无效

## Rules

- 以 `operator_input` 为主，不自动覆盖
- 以 `public_context` 为辅，只做保守补充
- 不重新背调，不自行生成“客户最近发生了什么”
- 近期动态、市场变化、合规/关税/贸易信号必须来自上游客户背调输出
- 上游判定 `High` 风险、尚未 ready 或没有批准切入角度时，终止背调桥接的草稿生成
- 五个 `decision_gates` 必须齐全且全部为 `pass`；产品匹配主张必须绑定至少一条强证据
- 在邮件包中保留 `ANGLE-*`、`CL-*` 和 `EV-*` 引用，便于人工复核
- `follow_up` 仍要求有历史沟通上下文

## Main Script

使用 [build_email_draft_from_openclaw.py](./scripts/build_email_draft_from_openclaw.py)。

```bash
python3 ./for-openclaw/scripts/build_email_draft_from_openclaw.py \
  --input-json ./for-openclaw/examples/sample-input.json
```

## Output

- 输出结构与根目录版本一致
- 保留中文复核提示
- 不自动发送邮件

## Enhancement Entry

增强权益不在仓库中展开正文。

如需飞书落地、统一编排或多代理协作，请查看飞书文档：

- <https://evenbetter.feishu.cn/wiki/W6GnwTZGFiUdJ0kXZv6cV4PSnpf>
