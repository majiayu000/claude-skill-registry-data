---
name: sealeap-athena-amazon-store-operations
description: "处理 Amazon 账户授权检查、经营报表、订单核对、外部履约和相关政策查询。根据用户目标选择对应模式；订单读取本身不授权发货。"
---

# Amazon 店铺报表、订单与履约

处理 Amazon 账户授权检查、经营报表、订单核对、外部履约和相关政策查询。根据用户目标选择对应模式；订单读取本身不授权发货。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [Amazon 账户授权检查](references/capabilities/amazon-account-auth/workflow.md) | 先读取既有连接的非敏感状态；需要新授权时通过官方流程绑定明确账户，再回读身份 |
| [Amazon 经营报表](references/capabilities/amazon-account-report/workflow.md) | 优先读取同口径已有报告；必要时按授权创建报表任务，追踪任务 ID 后下载并核对总量 |
| [Amazon 订单核对](references/capabilities/amazon-account-orders/workflow.md) | 读取订单头与行项目，按订单 ID 对齐支付、费用、取消和履约状态 |
| [Amazon 外部履约](references/capabilities/amazon-account-external-fulfillment/workflow.md) | 确认当前资格、订单行和仓库映射，核对库存及履约状态后执行已授权动作 |
| [Amazon 政策更新核对](references/capabilities/amazon-policy-monitor/workflow.md) | 查看当前官方公告并区分发布时间、生效时间及适用站点 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。订单读取不隐含履约授权；授权检查、报表和政策核对作为相应任务模式。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
