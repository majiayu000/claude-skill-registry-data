---
name: sealeap-athena-commerce-visual-design
description: "分析商品图片、属性、视觉相似度与品牌风格，或制作商品、服装、营销及成组展示图。按分析或生成模式选择工具，保持商品事实与素材权利边界。"
---

# 商品视觉分析与图片创作

分析商品图片、属性、视觉相似度与品牌风格，或制作商品、服装、营销及成组展示图。按分析或生成模式选择工具，保持商品事实与素材权利边界。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [商品多模态属性提取](references/capabilities/product-attribute-extraction/workflow.md) | 逐项识别可见属性并与一方规格表核对，区分观测和推测 |
| [商品视觉相似度比较](references/capabilities/product-visual-comparison/workflow.md) | 分别比较形态、结构、配件、比例和标识，再说明可见差异 |
| [图片内容识别](references/capabilities/image-content-recognition/workflow.md) | 检查图像质量，提取对象、布局与可读文字并标注位置 |
| [品牌视觉要素提炼](references/capabilities/brand-visual-profile/workflow.md) | 提取颜色、构图、字体倾向与产品呈现方式，形成可复用视觉说明 |
| [商品创意图生成](references/capabilities/product-image-generation/workflow.md) | 使用可用图像生成工具制作画面，完成后检查产品身份与文字清晰度 |
| [营销图片生成](references/capabilities/creative-image-generation/workflow.md) | 用可用图像工具生成初稿并检查文字、构图与交付尺寸 |
| [服装展示图生成](references/capabilities/apparel-image-generation/workflow.md) | 保持版型、图案与配件一致生成场景图，逐项核对服装还原度 |
| [商品展示图组制作](references/capabilities/commerce-product-image-set/workflow.md) | 按主图、细节、场景和尺寸说明分配图组，再核对一致性 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。分析与生成分模式；保留产品事实、素材权利、生成工具能力和调用费用边界。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
