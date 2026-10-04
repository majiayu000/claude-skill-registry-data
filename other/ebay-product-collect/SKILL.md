---
name: ebay-product-collect
description: 按关键词采集 eBay 商品详情，输出 JSON 数据
title: eBay商品采集
example: 采集 eBay 上关于 “Nintendo Switch” 售价排名前10的商品信息，包含价格、已售数量和卖家评级。
version: 1.0.1
---
# eBay 商品信息采集 Skill

## 角色定位

自动化 eBay 商品信息采集工具。根据关键词在 eBay 搜索商品，从列表页提取基础信息，
并逐个进入详情页补充采集物品状况、库存、已售量、退货政策、主图URL、好评率等字段。
支持指定采集数量和起始偏移，自动计算翻页，结果以 JSON 返回。

## 前提条件

1. ManAI 已启动，或项目内 `BrowserWorker` 可由 `run.py` 自动启动。
2. 本技能通过 BrowserWorker 插件浏览器执行 `browser.goto/evaluate/scroll/wait_ms/request_help/detect_page_state`，不依赖用户机器安装 ChromeDriver、Playwright、Selenium 或 BeautifulSoup。
3. 网络可正常访问 eBay（https://www.ebay.com/）。
4. 如需登录 eBay 账号以查看特定内容，按插件浏览器中的人工协助提示完成登录。
5. action 使用 BrowserWorker 框架级 `detect_page_state(domain_hint=...)` 判断登录、验证码、地区确认、风控、空结果等通用状态；如果页面已有可见商品链接，会忽略隐藏元素导致的 captcha 误报。

## 调用方式

```bash
# 采集前 10 个商品（默认）
python skills/ebay-product-collect/run.py collect --keywords "Nintendo"

# 从第 10 个商品开始，采集 20 个
python skills/ebay-product-collect/run.py collect --keywords "Nintendo" --count 20 --offset 10

# 多关键词 + JSON 参数
python skills/ebay-product-collect/run.py collect '{"keywords": "Nintendo\niphone", "count": 5}'
```

## 适用场景

- 竞品调研：采集某品类前 N 个商品的价格、销量、好评率
- 选品分析：通过多个关键词搜索对比商品热度
- 价格监控：定期采集特定关键词下的商品价格
- 分页浏览：通过 offset 实现翻页式浏览，避免一次采集过多

## 方法速查表

| 方法 | 说明 | 必填参数 | 可选参数 |
|------|------|----------|----------|
| `collect` | 按关键词搜索并采集商品信息 | `keywords` | `ebayUrl`, `count`, `offset` |

## 核心接口

### collect

按关键词在 eBay 搜索商品，采集列表页 + 详情页信息，以 JSON 返回。

**输入参数：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `keywords` | string | ✅ | — | 搜索关键词，多个关键词用换行 `\n` 分隔 |
| `ebayUrl` | string | ❌ | `https://www.ebay.com` | 指定访问的 eBay 站点 URL（如 `https://www.ebay.co.uk`） |
| `count` | number | ❌ | `10` | 每个关键词要采集的商品数量 |
| `offset` | number | ❌ | `0` | 从搜索结果的第几个商品开始采集（0-based） |

**输出字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `items` | array | 采集到的商品列表 |
| `items[].title` | string | 商品标题 |
| `items[].price` | string | 商品价格 |
| `items[].reviewCount` | string | 商品评论数量 |
| `items[].detailUrl` | string | 商品详情页地址 |
| `items[].condition` | string | 物品状况（New/Used/Refurbished 等） |
| `items[].stock` | string | 库存数量 |
| `items[].soldCount` | string | 已售量 |
| `items[].returnPolicy` | string | 退货政策 |
| `items[].imageUrl` | string | 主图URL |
| `items[].positiveRate` | string | 卖家好评率 |
| `items[].searchKeyword` | string | 对应的搜索词 |
| `totalCount` | number | 实际采集数 |
| `keywordsUsed` | array | 实际使用的关键词列表 |

## 参数校验规则（调用守门）

| 参数 | 必填 | 校验规则 | 失败提示 |
|------|------|----------|----------|
| `keywords` | ✅ | 非空字符串，按换行分割后至少有一个非空关键词 | `缺少必填参数 keywords（搜索关键词列表，多个关键词用换行分隔）` |
| `ebayUrl` | ❌ | 若提供，必须以 `https://www.ebay.` 或 `https://ebay.` 开头 | `参数 ebayUrl 格式不合法，请提供合法的 eBay 站点URL` |
| `count` | ❌ | 正整数，默认 10 | 使用默认值 |
| `offset` | ❌ | 非负整数，默认 0 | 使用默认值 |

## 使用示例

### 示例 1：采集前 10 个商品

```bash
python skills/ebay-product-collect/run.py collect --keywords "Nintendo Switch"
```

### 示例 2：从第 20 个开始采集 15 个

```bash
python skills/ebay-product-collect/run.py collect --keywords "Nintendo Switch" --count 15 --offset 20
```

### 示例 3：多关键词各采集 5 个

```bash
python skills/ebay-product-collect/run.py collect '{"keywords": "iPhone 15\nSamsung Galaxy S24", "count": 5}'
```

## 执行策略

1. **搜索阶段**：依次对每个关键词在 eBay 执行搜索，模拟人工输入和点击
2. **定位阶段**：根据 offset 自动计算起始页，翻页跳过前面的商品
3. **列表页采集**：通过 BrowserWorker 插件浏览器的 `browser.evaluate` 批量提取商品标题、价格、评论数、详情链接；兼容旧 `.s-item` 和新版 `s-card` 结构
4. **详情页采集**：在新标签页打开每个商品详情页，提取物品状况、库存、已售量、退货政策、主图URL、好评率
5. **数量控制**：采集到指定 count 数量后立即停止，不会多采
6. **节奏控制**：所有操作之间使用高斯随机延迟，模拟真人操作节奏

## 常见失败场景

| 场景 | 原因 | 解决方式 |
|------|------|----------|
| 搜索框未找到 | eBay 页面改版或加载不完整 | 重试或手动导航到 eBay 首页 |
| 列表页提取为空 | CSS 选择器失效 | 检查 eBay 页面结构是否变更，更新选择器 |
| 详情页加载超时 | 网络慢或 eBay 反爬限制 | 增加延迟，减少 count，使用代理 |
| offset 超出结果总数 | 搜索结果不够多 | 减小 offset 或更换关键词 |
| 部分详情字段为空 | 该商品详情页缺少对应信息 | 正常情况，字段为空字符串 |
| 页面状态提示登录/验证码/风控 | eBay 要求人工处理或隐藏验证信号误判 | 有可见商品链接时 action 会继续；否则按 `request_help` 提示人工处理，不要自动反复刷新 |
