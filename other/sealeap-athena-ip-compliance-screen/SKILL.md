---
name: sealeap-athena-ip-compliance-screen
description: "在用户要求商品知识产权或上市合规初筛时，检查图片权利、商标、外观、技术专利、诉讼和受限商品线索，按权利类型和法域保留证据缺口。"
---

# 商品知识产权与受限品初筛

在用户要求商品知识产权或上市合规初筛时，检查图片权利、商标、外观、技术专利、诉讼和受限商品线索，按权利类型和法域保留证据缺口。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [图片权利来源初筛](references/capabilities/image-rights-screen/workflow.md) | 先核对权利链，再检索疑似相似作品并记录权利人和登记证据 |
| [图形商标初筛](references/capabilities/graphic-mark-screen/workflow.md) | 提取显著图形特征并检索目标法域相关商标，按商品服务范围比较 |
| [受限商品图片初筛](references/capabilities/restricted-product-image-screen/workflow.md) | 识别可能触发平台限制的商品特征，再核对当前官方销售规则 |
| [外观设计权初筛](references/capabilities/design-right-screen/workflow.md) | 以产品类别和外观要点检索设计权，再逐视图记录相同与不同点 |
| [文字商标初筛](references/capabilities/word-mark-screen/workflow.md) | 检索完全一致与近似文字，核对权利人、类别及当前状态 |
| [技术方案专利初筛](references/capabilities/utility-patent-screen/workflow.md) | 把技术方案拆为检索概念，检索专利后定位独立权利要求与法律状态 |
| [商品诉讼线索初筛](references/capabilities/product-litigation-screen/workflow.md) | 在可用公开案件与权利登记资料中匹配主体和案件，核对文件内容 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。版权、商标、外观、技术专利、诉讼和受限品分模式；所有结论仅初筛。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
