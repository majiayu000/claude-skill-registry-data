---
name: sealeap-athena-temu-order-fulfillment
description: "核对 Temu 美国区、欧洲区或全球区订单，按明确授权处理发货或取消。地区流程和查询、发货、取消三类动作分别验证。"
---

# Temu 订单、发货与取消

核对 Temu 美国区、欧洲区或全球区订单，按明确授权处理发货或取消。地区流程和查询、发货、取消三类动作分别验证。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [Temu 美国区 订单核对](references/capabilities/temu-us-orders/workflow.md) | 读取订单头与行项目，按订单 ID 对齐支付、费用、取消和履约状态 |
| [Temu 美国区 订单发货](references/capabilities/temu-us-fulfillment/workflow.md) | 读取待发货订单并核对地址/包裹数量；按授权提交发货并回读每件状态 |
| [Temu 美国区 订单取消](references/capabilities/temu-us-cancel-order/workflow.md) | 先读订单状态与可取消资格，展示后果，再处理被授权的取消请求并回读 |
| [Temu 欧洲区 订单核对](references/capabilities/temu-eu-orders/workflow.md) | 读取订单头与行项目，按订单 ID 对齐支付、费用、取消和履约状态 |
| [Temu 欧洲区 订单发货](references/capabilities/temu-eu-fulfillment/workflow.md) | 读取待发货订单并核对地址/包裹数量；按授权提交发货并回读每件状态 |
| [Temu 欧洲区 订单取消](references/capabilities/temu-eu-cancel-order/workflow.md) | 先读订单状态与可取消资格，展示后果，再处理被授权的取消请求并回读 |
| [Temu 全球区 订单核对](references/capabilities/temu-global-orders/workflow.md) | 读取订单头与行项目，按订单 ID 对齐支付、费用、取消和履约状态 |
| [Temu 全球区 订单发货](references/capabilities/temu-global-fulfillment/workflow.md) | 读取待发货订单并核对地址/包裹数量；按授权提交发货并回读每件状态 |
| [Temu 全球区 订单取消](references/capabilities/temu-global-cancel-order/workflow.md) | 先读订单状态与可取消资格，展示后果，再处理被授权的取消请求并回读 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。订单查询不隐含发货/取消；每个地区维护独立操作参考。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
