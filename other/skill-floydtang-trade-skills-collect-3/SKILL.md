---
name: trade-outreach-email
description: Generate conservative, editable English outreach drafts for foreign-trade sales from structured lead inputs and customer-intel signals. Use when an operator needs a first-touch or follow-up email draft that calls confirmed recent/customer-market signals from the customer-intel Skill, with subject options, review notes, and explicit reminders not to present unconfirmed facts as facts.
---

# 开发信 Skill

## Overview

用这个 Skill 把结构化客户信息和客户背调信号转换成可人工修改后发送的英文邮件草稿。

当前定位：`复核型开发信工作台`

角色定位：

- `开发信策略员`
- 上游：人工整理输入，或 `客户背调skill/` 输出的桥接结果
- 下游：人工复核与实际发送动作
- 不负责自动发送，也不负责替代上游做搜索、初筛和背调
- 不负责重新查“客户最近发生了什么”；近期动态、市场变化和销售切入点必须来自 `客户背调skill/`

当前只覆盖两个场景：

- `first_touch`：首轮开发信
- `follow_up`：跟进邮件

它不是自动发送工具。目标是把零散输入整理成更稳定、更易复核的英文草稿。

## Standard Input

输入统一为 JSON：

```json
{
  "email_type": "first_touch",
  "customer_name": "Anna",
  "company_name": "Acme Foods",
  "product_or_offer": "frozen mixed vegetables",
  "goal": "introduce our factory and ask whether they are open to new suppliers",
  "country_or_market": "Poland",
  "customer_profile_summary": "Company website shows private-label frozen food focus in EU retail.",
  "previous_contact_context": "",
  "tone": "professional,warm",
  "sender_name": "Leo",
  "sender_company": "Ningbo FreshGrow Foods",
  "signature": "",
  "constraints": ""
}
```

## Workflow

1. Normalize the input fields.
2. Validate the input against the local JSON schema and confirm `email_type` is `first_touch` or `follow_up`.
3. When `source_context` comes from customer intel, require `draft_authorization = approved` and one approved `selected_sales_angle`.
4. Build subject options based on scenario, product, and company name.
5. Generate one main draft and one lighter alternative draft.
6. Preserve the selected `ANGLE-*`, `CL-*`, and `EV-*` references in the review package.
7. Attach review notes for any claim that depends on summary, historical context, pricing, capability, or other unconfirmed details.
8. If `source_context` includes recent customer signals or market signals, use them only when a dated source URL and medium/high confidence are present.
9. Output in the structure defined in [output-template.md](./references/output-template.md).

## Output Requirements

- 必须包含邮件类型
- 必须包含 2 个标题候选
- 必须包含至少 1 个英文正文草稿
- 必须包含中文复核提示
- 必须包含 `evidence_signals_used`
- 必须包含 `unconfirmed_fact_checklist`
- 必须包含 `send_policy = manual_review_only`
- 公司级线索缺少联系人时使用自然的公司团队称呼；不得输出 `Dear there`、`Dear unknown` 等占位语
- 最终 JSON 必须保留批准的 `ANGLE-*`、对应 `CL-*` 与 `EV-*` 结构化对象，不只保留文本摘要
- 批准角度属于内部策略与审计上下文，不得把 `Open by...`、`Connect the note...` 等写作指令原样复制到客户正文
- 工业场景默认只使用通用应用与参数确认表达；BOM、automation module、motor/drive、ASRS 或物料搬运等细节必须同时有上游主张和证据支持
- `follow_up` 必须消费真实 `previous_contact_context`；缺失时阻断，不得自动补写历史沟通
- `follow_up` 默认只承诺产品详情与规格；只有卖方能力、证明或授权资料明确支持样品时才能使用 sample 表达
- 必须包含 `workflow_guidance`
- 必须回显关键输入依据
- 如引用近期动态、市场变化或合规信号，必须来自上游 `source_context`
- 背调桥接场景必须有明确批准的销售角度；未批准时脚本直接拦截，不生成草稿
- 必须保留被选中的 claim 和 evidence，而不是只传来源标题
- 不能把不确定信息写成确定事实
- 不能越权替代人工执行发送
- 不能越权替代 `客户背调skill/` 编造客户事实
- 不能自行生成“客户最近发生了什么”
- 不能把弱证据包装成个性化事实

## Main Script

默认脚本入口是 [build_email_draft.py](./scripts/build_email_draft.py)。

### Example

```bash
python3 ./scripts/build_email_draft.py --input-json ./examples/first-touch.json
```

```bash
python3 ./scripts/run_regression_checks.py
```

## Defaults

- 本地模板生成优先
- 不强依赖联网
- 不联网背调；只消费输入和 `source_context`
- 输出默认偏保守
- 不覆盖报价邮件
- 发送前必须人工复核
- 默认下游动作：`ready_for_manual_send | hold_for_manual_review`

## Table and Rule Capture

- 本 Skill 输出开发信草稿和复核清单能力，不要求企业使用固定邮件结果表。
- 写入企业表格、知识库或邮箱草稿箱时，先沿用已有表头和归口，再映射标题候选、草稿引用、近期信号、市场信号、证据依据、待确认项、发送策略等标准字段。
- 用户没有可用表格时，龙虾可以按企业产品、市场和跟进流程新建够用表。
- 当用户确认新的开发信风格、禁用表达、行业话术、跟进节奏或表头映射后，必须追问：`是否更新到对应 Skill 以便下次自动复用`。真实写入必须得到用户授权。

## Enhancement Entry

如需数据留存、统一编排、多代理协作或飞书落地，请查看飞书文档：

- <https://evenbetter.feishu.cn/wiki/W6GnwTZGFiUdJ0kXZv6cV4PSnpf>
