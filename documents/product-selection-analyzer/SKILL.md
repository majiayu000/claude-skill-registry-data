---
name: product-selection-analyzer
description: 多渠道采集Amazon、TikTok、Google Trends、1688和目标平台数据，通过6维度100分制自动量化商品赚钱潜力，筛出高利润低竞争蓝海爆款，彻底告别凭感觉选品。
license: MIT
compatibility: Python3 + openpyxl。WebSearch + Web Reader MCP（跨平台榜单采集）。目标平台Seller MCP
  Server（后台数据）。1688 MCP Server（1688商品和采购价数据，可选）
metadata:
  author: kilig
  version: 1.0.0
  category: e-commerce
  tags:
  - product-research
  - scoring
  - cross-border
  - sourcing
  - profit-calculation
  - competition-analysis
  - data-driven
title: ManAI选品评分
example: "在Claude Code中直接说：**开始选品，钓鱼用品**  \n技能将自动执行以下步骤：  \n1. WebSearch采集 `\"钓鱼用品\
  \ ozon топ продаж\"`、`\"钓鱼用品 amazon bestsellers\"`、`\"钓鱼用品 tiktok trending products\"\
  ` 等6大榜单  \n2. Ozon Seller MCP 拉取后台销量、流量数据  \n3. 1688 MCP 获取采购价和新品标签  \n4. 匹配物流通道计算毛利，按跨平台热度、竞争、利润、新品信号、榜单排名、趋势走向6维度打分\
  \  \n5. 生成包含S/A/B/C/D评级、成本、利润和推荐理由的Excel和Markdown报告  \n示例输出：  \n新增15个商品，淘汰8个（4个毛利不达标，3个竞争过激，1个趋势下降）\
  \  \nS级2个：Shimano纺车轮（低竞争+Amazon热销#3）、硅胶假饵（TikTok爆款+新品标签）  \n文件路径：/选品结果/钓鱼用品_2026-03-20.xlsx"
version: 1.0.0
---
# 跨境电商选品打分（6维度100分制）

多渠道采集 Amazon、TikTok、Google Trends、1688、目标平台（Ozon/Shopee/AliExpress等）的商品数据，6维度100分制智能评分，筛选高利润低竞争蓝海商品，输出 Excel + Markdown 分析报告。

## 前置要求

| 依赖 | 用途 | 必填 |
|------|------|------|
| **Claude Code CLI** | 运行环境 | 必填 |
| **WebSearch** | 搜索 Amazon Bestsellers、TikTok Trending、Google Trends 等公开榜单 | 必填 |
| **Web Reader MCP** | 读取榜单页面，提取商品名、价格、排名 | 必填 |
| **目标平台 Seller MCP** | 拉取后台数据（商品搜索、详情、销量、流量分析） | 必填 |
| **1688 MCP Server** | 1688 商品搜索、采购价、新品标签（用于采购价和毛利计算） | 推荐 |
| **Python3 + openpyxl** | Excel 输出 | 必填 |

**以 Ozon 为例，Seller MCP 需要支持：**
- `ozon_search` — 前台商品搜索
- `ozon_product_details` — 商品详情（上架时间、价格）
- `analytics_data` — 销量、流量、转化率分析
- `product_info` / `product_info_list` — 商品信息批量查询
- `prices_info` — 价格信息

**以 1688 MCP 为例，需要支持：**
- `search_goods` — 1688 商品搜索
- `goods_detail` — 商品详情（采购价、起批量）
- `new_goods` — 1688 新品查询

**首次使用前请配置：**
1. 目标平台的 Seller API 密钥（在对应 MCP Server 中配置）
2. 选品结果 Excel 的存放路径
3. 毛利计算参数（默认汇率、物流通道费率等）

## 指令

### 第 1 步：确定品类和天数

询问用户：
1. **选什么品类？**（如"钓鱼用品"、"咖啡豆"）
2. **选几天内的商品？**（默认30天，只影响新品筛选时间窗口）

如用户未指定品类，展示几个建议品类让用户选择。用户未提及的额外条件不加。

### 第 2 步：多渠道数据采集

#### 2.1 WebSearch 采集（必须执行）

对用户指定品类，搜索以下内容并标记来源：

```bash
# 1. 目标平台热卖（以Ozon为例，用俄语搜索）
WebSearch: "{品类} ozon топ продаж"         → 标记「热卖趋势」

# 2. 供应链趋势
WebSearch: "{品类} 跨境电商 热卖 2026"        → 标记「供应链趋势」

# 3. Amazon 热销榜
WebSearch: "{品类} amazon bestsellers"       → 标记「Amazon热销#位次」

# 4. TikTok 热销榜
WebSearch: "{品类} tiktok trending products"  → 标记「TikTok热销#位次」

# 5. Google 趋势
WebSearch: "{品类} google trends rising"      → 标记「Google趋势上升」

# 6. 目标市场本地化趋势（以俄语区为例）
WebSearch: "{品类} ozon новинки тренд 2026"   → 标记「俄语区趋势」
```

用 Web Reader 读取找到的榜单/文章，提取商品名、链接、价格、排名。备注列必须注明具体来源文章名。

预期输出：每个来源采集到 N 个候选商品，共计 M 个去重后商品。

#### 2.2 目标平台后台采集

用目标平台 Seller MCP 拉取后台数据：

```
# 以 Ozon 为例
ozon_search(keyword="{品类}")               → 前台搜索商品
ozon_product_details(product_id=...)        → 获取上架时间、详情
analytics_data(metrics=["revenue","ordered_units","hits_view"],
               dimension=["sku"],
               sort=[{"key":"ordered_units","order":"DESC"}])  → 销量排行
```

预期输出：目标平台热销品列表（含销量、浏览量、上架时间）。

#### 2.3 1688 采购数据采集

用 1688 MCP Server 搜索对应商品：

```
search_goods(keyword="{品类关键词}")         → 搜索1688商品
goods_detail(goods_id=...)                  → 获取采购价、起批量
new_goods(keyword="{品类关键词}")             → 获取1688新品标签
```

预期输出：每个候选商品的 1688 采购价、是否新品。

### 第 3 步：毛利计算

对每个采集到的商品计算毛利：
- 从 1688 MCP 获取采购价
- 根据重量自动匹配国际物流通道（多通道运费自动匹配）
- 按实时汇率折算（WebSearch 查询汇率）
- 计算毛利率（毛利率<15%在评分环节得0分）

### 第 4 步：6维度智能评分

对每个商品按以下6个维度打分（满分100分）：

| 维度 | 分值 | 评估内容 |
|------|------|----------|
| 跨平台热度 | 20分 | Amazon + TikTok 销量验证，多平台验证降低误判 |
| 竞争程度 | 20分 | 目标平台同款数 + 卖家销量（通过 Seller MCP 查询） |
| 利润空间 | 20分 | 毛利率（1688采购价 vs 目标平台售价），毛利率<15%得0分 |
| 新品信号 | 15分 | 1688新品标签 / 目标平台新品标签 |
| 榜单表现 | 20分 | Amazon/TikTok/目标平台榜单的位次排名 |
| 趋势方向 | 5分 | Google Trends 走势（上升/平稳/下降） |

**等级划分：**
- **S级**（90+）：强烈推荐，多维度验证的蓝海爆款
- **A级**（75-89）：优质选品，2-3个维度突出
- **B级**（60-74）：可考虑，有一定竞争力
- **C级**（50-59）：谨慎，存在风险
- **D级**（<50）：淘汰

### 第 5 步：筛选规则

| 来源 | 上架时间 |
|------|----------|
| 热卖趋势/供应链趋势 | ≤ 30天 |
| 后台看板 | ≤ 15天 |
| 店铺数据 | ≤ 7天 |

### 第 6 步：去重与写入 Excel

与已有选品结果按商品链接去重，用 openpyxl 写入 Excel：
- 每行包含：评分+等级、商品名、来源、成本、毛利、目标平台链接、竞争分析、推荐理由

### 第 7 步：生成 Markdown 报告

输出分析报告，包含：
- 本次新增商品数、按来源分布
- 淘汰不达标商品数及淘汰原因
- S/A 级商品重点分析
- 累计商品总数

### 第 8 步：输出报告

告诉用户：
- 新增商品数、淘汰数、累计总数
- S/A 级商品推荐摘要
- Excel 和报告文件路径

## 示例

### 示例 1：首次选品

用户说："开始选品，钓鱼用品"

操作：
1. WebSearch 搜索钓鱼用品在 Amazon/TikTok/Google Trends 的热卖趋势
2. Ozon Seller MCP 拉取钓鱼品类近 30 天销量数据
3. 1688 MCP 搜索钓鱼用品采购价和新品
4. 对每个商品计算毛利（多通道运费匹配）
5. 6维度评分，淘汰不达标商品
6. 写入 Excel + 生成分析报告

结果：
```
新增 15 个商品
淘汰 8 个（4个毛利不达标，3个竞争过激，1个趋势下降）
S级 2个：Shimano纺车轮（低竞争+Amazon热销#3）、硅胶假饵（TikTok爆款+新品标签）
A级 5个：...
文件路径：<用户配置的路径>
```

### 示例 2：追加选品

用户说："再加几个咖啡豆相关的"

操作：同流程，自动与已有 Excel 去重，只追加新品。

### 示例 3：指定目标平台

用户说："帮我选几款适合Shopee东南亚的防晒霜"

操作：目标平台切换为 Shopee，WebSearch 搜索东南亚市场热卖趋势，Shopee Seller MCP 拉后台数据，同流程评分。

## 故障排查

### WebSearch 采集不到数据
错误：搜索结果为空
原因：品类关键词过于小众或搜索词需要调整
解决方法：尝试用目标市场本地语言关键词搜索（如俄语、泰语），或换用更宽泛的品类词

### Seller MCP 连接失败
错误："Connection refused" 或 "API key invalid"
原因：目标平台 Seller MCP Server 未启动或 API 密钥失效
解决方法：
1. 确认 MCP Server 在运行
2. 确认 API 密钥有效
3. 尝试重连 MCP Server

### 平台 API 限频
错误：API 请求频率过高
原因：平台 API 限频（如 Ozon 约 10 次/分钟）
解决方法：增加请求间隔（默认 5 秒），分批采集

### 毛利全部不达标
错误：所有商品毛利低于阈值
原因：1688 采购价偏高或物流费用高
解决方法：尝试寻找更低价供应商，或调整物流通道选择

### Excel 写入冲突
错误：文件被其他程序占用
原因：Excel 文件正在被打开
解决方法：关闭 Excel 后重试

## 执行原则

- **每步确认** — 每完成一个步骤，把中间结果发给用户确认后再继续
- **数据真实** — 所有评分基于实际采集数据，不猜测不编造
- **淘汰透明** — 被淘汰的商品要说明淘汰原因和具体维度得分
- **毛利保守** — 运费按最贵通道计算，确保实际利润不低于预估
- **去重严格** — 与已有选品结果按商品链接去重，避免重复选品
