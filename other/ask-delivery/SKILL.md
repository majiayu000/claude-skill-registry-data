---
name: ask-delivery
description: 分析到交付的入口 — 根据你的目标(配置/澄清/BRD/PRD/合规/开发/审计/交接)路由到正确的 user-invoked skill。不确定该用哪个 analysis-to-delivery skill 时,从此入口进入。
disable-model-invocation: true
version: 4.0.0

---

# Ask Delivery — 路由

## Contract

- 输入: 用户目标,或不确定该用哪个 analysis-to-delivery skill
- 输出: 推荐的下一个 skill 名;若需要则附 1-2 个澄清问题
- 门控: 无
- Required rules: 无
- Required paths: 无
- 下一步: 选中的 skill 或 `/analysis-delivery-workflow`

## 我该用哪个 skill?

**告诉我你想做什么**,我从下面选一个:

| 你想做的事 | 用这个 skill |
|---|---|
| 首次给新项目接这套工作流 | `/setup-analysis-delivery` |
| 澄清一个需求 / 拉齐字段 | `/grill-task` |
| 出一份业务需求文档 (BRD) | `/to-brd` |
| 做合规评审 (GSP/HIPAA/SOX/...) | `/compliance-review` |
| 写测试用例 / 验收标准 | `/test-case-design` |
| 出一份产品需求文档 (PRD) | `/to-prd` |
| 出 FSD + 数据模型 + 开发设计 | `/dev-design` |
| 跑 QA 审计 | `/qa-audit` |
| 收尾生成交接文档 | `/handoff` |
| **走完整 9 阶段(新手/复杂项目)** | `/analysis-delivery-workflow` |
| **进入开发实施子流程** | `/using-superpowers` |

## 不确定?

用 `/analysis-delivery-workflow` — 它会按顺序自动调上面 9 个动作。
设计完成后,用 `/using-superpowers` 进入 superpowers 5 步实施。

## 路由方式

我会问你 1-2 个澄清问题,然后告诉你用哪个。如果你已经知道,直接 `/skill-name`。
