---
name: trade-active-outreach-combo
description: "Run or resume a deliverable active-outreach workflow across lead discovery, screening, customer intel, and outreach email. Use when an operator or system pipeline needs durable run state, visible intermediate artifacts, evidence gates, report-bound human approval, and a final editable email draft that is never auto-sent."
metadata: {"openclaw":{"role":"workflow_owner","container_owner":"active_outreach_combo","container_mode":"container_neutral_with_feishu_sandbox_adapter","single_skill_policy":"attach_only","table_policy":"adapt_existing_or_create_minimal","rule_capture":"ask_before_skill_update"}}
---

# 主动开发工作流组合包

## Overview

用这个组合包把以下 4 个已可用节点串成一条可暂停、可续跑、可审计的主动开发闭环：

`客户搜索skill -> 线索整理skill -> 客户背调skill -> 开发信skill`

组合包不是为了让系统迷信“一次性跑满”。主代理负责声明工作区、安排子代理、维护状态和失败收口；真实落地时可以也应该按节点推进，先把单点能力跑稳，再扩大到链路。

只做三件事：

- 串联 4 个现有节点
- 保留中间产物
- 明确人工复核点
- 输出中立容器 bundle，再按需派生到课堂沙盘
- 适配企业已有表头，或在没有可用表格时创建够用表
- 让客户背调作为核心判断层，把近期客户信号、市场/合规信号和销售角度传给开发信
- 在用户确认字段、分级、背调规则或开发信风格后，先追问是否沉淀到对应 Skill

## Workflow

1. Use `run_workflow.py` with a config that matches `schemas/workflow-contract.schema.json`; keep `run_minimal_demo.py` only for fixed classroom and regression runs.
2. Convert discovery output into the lead-screening input shape.
3. Run lead screening and export the customer-intel batch payload.
4. Select one lead for the reviewed customer-intel stage.
5. In fixture mode, reuse the reviewed customer-intel fixture; in live mode, execute the real customer-intel builder.
6. Stop before email when intel gates fail or no `ANGLE-*` has explicit human approval bound to the reviewed report hash.
7. Bridge the approved angle, selected claims, and selected evidence into outreach-email input.
8. Generate editable English outreach drafts and review notes without inventing new customer facts.
9. Export `ContainerBundle` to JSON / Markdown / CSV and Feishu Sandbox Adapter.

## Recommended Rollout Pace

真实业务首跑推荐按这个节奏：

1. 先跑 1 个已知客户的客户背调，确认信号、风险和销售角度能被人工认可。
2. 再跑 3-5 条候选客户的搜索和线索整理，确认来源、证据等级和下一步动作。
3. 只把通过质量门槛的客户交给客户背调和开发信节点。
4. 任一阶段证据不足时，主代理应标记 hold、补证据或人工复核，不应强行推进到开发信。

这个节奏和课程最新版一致：先跑判断能力，再跑候选发现，最后再讲全链路收口。

## Table and Rule Policy

- Skill 是标准化能力，不是固定表格模板。
- 企业表格是企业个性化资产：优先沿用用户已有表头；没有可用表格时，龙虾按企业产品、市场和流程新建够用表。
- 标准字段和 Feishu Sandbox 只作为参考映射，不作为企业落地的强制前置。
- 当用户确认了新字段、客户分级、背调规则、开发信风格、禁用表达或行业习惯，必须追问：`是否更新到对应 Skill 以便下次自动复用`。真实写入必须得到用户授权。

## Output Requirements

- 必须生成阶段化中间产物
- 必须生成 `00-run-manifest.json`，供系统判断完成、等待审批、业务拦截或执行失败
- 必须保留人工复核点
- 必须同时保留固定回归模式和真实运行模式
- 真实模式不得自动批准销售角度，也不得绕过客户背调决策门槛
- 首次运行不得携带销售角度批准；批准只能在报告生成后，通过 `--resume` 绑定报告哈希、审核人与时间
- 续跑必须先核对 manifest 已登记产物的 SHA-256；产物缺失或被修改时失败关闭，不得用当前文件重写旧哈希
- `follow_up` 必须从配置取得真实 `previous_contact_context`，不得虚构历史触达
- 必须输出最终邮件草稿和中间桥接 JSON
- 必须输出容器中立的 `ContainerBundle`
- 背调节点必须给开发信提供可复核的近期信号、市场信号或保守销售角度
- 不能把推断写成确定事实
- 不能把邮件草稿写成可直接自动发送
- 不能让开发信节点自行编造“客户最近发生了什么”
- 不能把飞书写成唯一数据容器

## Main Script

- 生产入口：[run_workflow.py](./scripts/run_workflow.py)
- 课堂/回归入口：[run_minimal_demo.py](./scripts/run_minimal_demo.py)
- 配置、审批与 manifest 契约：[workflow-contract.schema.json](./schemas/workflow-contract.schema.json)

### Example

```bash
python3 ./主动开发链路组合包/scripts/run_workflow.py \
  --config /path/to/workflow.json \
  --output-dir /path/to/run
```

退出码 `10` 表示正常等待人工审批，不是执行故障。审核报告后使用 `--resume --approved-sales-angle-id ANGLE-XX --reviewer REVIEWER` 续跑；审批记录会绑定审核前报告的 SHA-256。

## Enhancement Entry

如需数据留存、统一编排、多代理协作或飞书落地，请查看飞书文档：

- <https://evenbetter.feishu.cn/wiki/W6GnwTZGFiUdJ0kXZv6cV4PSnpf>

仓库内不展开增强权益正文。
