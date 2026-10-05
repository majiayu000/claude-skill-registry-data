---
name: sealeap-athena-marketplace-research
description: "研究 Walmart、Ozon、Etsy、eBay、Shopify 或 Mercado Libre 的商品、店铺与市场。按明确平台选择独立参考与数据源，保留币种、样本和指标口径；不执行商家后台写入。"
---

# Walmart/Ozon 等平台商品研究

研究 Walmart、Ozon、Etsy、eBay、Shopify 或 Mercado Libre 的商品、店铺与市场。按明确平台选择独立参考与数据源，保留币种、样本和指标口径；不执行商家后台写入。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [Walmart 类目市场研究](references/capabilities/walmart-category-market/workflow.md) | 先确认类目节点，再对同一批商品比较价格、卖家与需求集中度 |
| [Walmart 商品趋势分析](references/capabilities/walmart-product-analysis/workflow.md) | 串联商品详情、历史趋势与变体估算，解释变化对应的时间段 |
| [Walmart 关键词研究](references/capabilities/walmart-keyword-research/workflow.md) | 拓展相关关键词并核对搜索结果与商品相关性，记录需求和竞争代理指标 |
| [eBay 商品检索](references/capabilities/ebay-product-discovery/workflow.md) | 使用已授权官方检索工具或公开页面，区分在售与已售并核对商品状态 |
| [Etsy 类目定位](references/capabilities/etsy-category-map/workflow.md) | 用当前官方类目资料或可访问页面确认名称、层级和适用属性 |
| [Etsy 商品检索](references/capabilities/etsy-product-discovery/workflow.md) | 使用可用 Etsy 搜索工具或公开页面，核对商品类型与变体价格 |
| [Etsy 店铺观察](references/capabilities/etsy-shop-analysis/workflow.md) | 核对店铺身份、商品组合和公开评价，保留观察时间 |
| [Shopify 商品页面观察](references/capabilities/shopify-product-observation/workflow.md) | 读取公开商品与可见变体，核对价格、库存可见性和配送提示 |
| [Shopify 独立站研究](references/capabilities/shopify-store-observation/workflow.md) | 比较公开目录、导航、内容与转化路径，并区分实测和推断 |
| [Walmart 商品搜索](references/capabilities/walmart-product-discovery/workflow.md) | 检索商品后逐项检查 ID、变体、售价与配送条件 |
| [Walmart 报价与变体核对](references/capabilities/walmart-offer-detail/workflow.md) | 核对选中变体、卖家、价格、配送及可用需求估计 |
| [Ozon 商品条件检索](references/capabilities/ozon-product-discovery/workflow.md) | 按明确条件检索商品并核对 SKU、价格、需求估计和筛选覆盖 |
| [Ozon 商品详情核对](references/capabilities/ozon-product-detail/workflow.md) | 核对单商品规格、价格、销量估计、库存代理和类目 |
| [Ozon 商品历史趋势](references/capabilities/ozon-product-trend/workflow.md) | 获取逐日销售和库存序列并标注缺口、促销与异常 |
| [Ozon 品牌商品研究](references/capabilities/ozon-brand-catalog/workflow.md) | 按品牌检索商品并核对品牌归属，分析已取样本的组合结构 |
| [Ozon 类目商品研究](references/capabilities/ozon-category-products/workflow.md) | 确认类目路径再查询商品，比较价格带、卖家和需求集中度 |
| [Ozon 卖家商品组合](references/capabilities/ozon-seller-products/workflow.md) | 仅在接口支持卖家筛选时查询，逐项核对卖家和商品关系 |
| [Ozon 市场关键词研究](references/capabilities/ozon-market-keywords/workflow.md) | 查询可用关键词频率并核对搜索指标与时间定义 |
| [Ozon 相关词挖掘](references/capabilities/ozon-keyword-expansion/workflow.md) | 从有出处的相关词和搜索建议扩展，核对真实需求数据 |
| [Ozon 商品关键词反查](references/capabilities/ozon-reverse-keywords/workflow.md) | 读取商品关联关键词与位置，按时间和相关性整理 |
| [Ozon 店铺检索与核对](references/capabilities/ozon-shop-discovery/workflow.md) | 使用当前可用官方或授权店铺搜索核对身份和公开经营信息 |
| [Ozon 类目发现](references/capabilities/ozon-category-discovery/workflow.md) | 先从当前类目资料确定路径，再查询相关商品验证类目匹配 |
| [Ozon 报价规格比较](references/capabilities/ozon-offer-comparison/workflow.md) | 核对不同 SKU 的包装数量、价格、履约与可用需求指标 |
| [Ozon 商品研究报表](references/capabilities/ozon-product-report/workflow.md) | 把详情、趋势和关键词按相同 SKU 与期间汇总，逐项对账 |
| [Mercado Libre 市场研究](references/capabilities/mercado-market-research/workflow.md) | 使用该市场官方或授权数据检索商品并核对币种、配送和需求证据 |
| [Etsy 单商品详情核对](references/capabilities/etsy-listing-detail/workflow.md) | 使用可用 Etsy 工具或公开页核对标题、材质声明、价格和交付方式 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。只合并研究入口；Walmart、Ozon、Etsy、eBay、Shopify 与 Mercado Libre 各用独立参考，禁止跨平台替代字段与混算指标。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
