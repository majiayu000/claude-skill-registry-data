---
name: sealeap-athena-shopee-catalog-media
description: "处理 Shopee 商品、全球商品映射、店内分类、媒体上传和媒体空间，按资源类型生成具体变更并在授权范围内执行。"
---

# Shopee 商品目录与媒体管理

处理 Shopee 商品、全球商品映射、店内分类、媒体上传和媒体空间，按资源类型生成具体变更并在授权范围内执行。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [Shopee 全球商品映射](references/capabilities/shopee-account-global-product/workflow.md) | 核对源商品和各市场刊登映射，补足当地类目属性，再准备授权同步 |
| [Shopee 媒体上传处理](references/capabilities/shopee-account-media/workflow.md) | 验证选定素材格式并通过官方能力上传或处理，核对结果及引用关系 |
| [Shopee 媒体资源管理](references/capabilities/shopee-account-media-space/workflow.md) | 盘点已授权媒体资源，检查引用后生成新增、整理或删除预览 |
| [Shopee 商品管理](references/capabilities/shopee-account-product/workflow.md) | 读取商品现状与当前类目 schema，生成字段级变更预览，验证后执行授权范围并回读 |
| [Shopee 店内分类](references/capabilities/shopee-account-shop-category/workflow.md) | 读取店内分类和商品分配，预览移动或排序后按授权应用 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。商品、全球映射、分类和媒体的资源 ID 与上传要求分别保存。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
