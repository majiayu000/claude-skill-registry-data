---
name: amazon-browser-extraction
description: 当 API 工具（AlphaShop、Jungle Scout、卖家精灵）不可用或过度时，通过浏览器直接导航 Amazon 搜索/榜单页面 + JavaScript 提取结构化商品数据，作为零成本的选品发现和竞品监控降级方案。
title: Amazon 浏览器端数据提取
example: |-
  ### 提取连衣裙品类的畅销榜数据
  
  1. 导航到 Amazon 搜索结果并按畅销排序：
     ```
     browser_navigate(url="https://www.amazon.com/s?k=dress&i=fashion-womens&s=exact-aware-popularity-rank")
     ```
  
  2. JavaScript 提取结构化数据：
     ```javascript
     browser_console(expression=`(() => {
       const items = [];
       document.querySelectorAll('[data-component-type="s-search-result"]').forEach((card, i) => {
         if (i >= 20) return;
         items.push({
           rank: i+1,
           asin: card.getAttribute('data-asin'),
           title: card.querySelector('h2')?.textContent?.trim()?.substring(0,80),
           price: card.querySelector('.a-price .a-offscreen')?.textContent?.trim(),
           rating: card.querySelector('.a-icon-alt')?.textContent?.trim(),
           purchaseBadge: card.querySelector('.a-size-base.a-color-secondary')?.textContent?.trim(),
         });
       });
       return items;
     })()`)
     ```
  
  3. 输出结构化表格，含价格带分析、品牌集中度、热销特征归纳。
version: 1.0.0
---
# Amazon 浏览器端数据提取

> 零成本降级方案：当付费/需凭证的 API 工具不可用时，用浏览器直接提取 Amazon 商品数据。

## 何时使用

- **API 不可用**：AlphaShop 未配置凭证、Jungle Scout 未订阅、卖家精灵 Key 缺失
- **快速验证**：不需要完整分析报告，只需快速扫一眼品类热销榜
- **实时数据**：需要最新榜单（Amazon 每小时更新）而非工具缓存

## 操作流程

> 快速提取脚本：`scripts/amazon-search-extract.js` — 可直接在 `browser_console` 中执行。

### Step 1：导航到目标页面

```python
# 方案 A：关键词搜索 + 畅销排序
browser_navigate(url="https://www.amazon.com/s?k={keyword}&i=fashion-womens&s=exact-aware-popularity-rank")

# 方案 B：Best Sellers 分类页
browser_navigate(url="https://www.amazon.com/Best-Sellers-{category}/zgbs/{node_id}")
```

**常用 URL 参数**：
| 参数 | 含义 | 示例 |
|------|------|------|
| `s=exact-aware-popularity-rank` | 按畅销排序 | — |
| `i=fashion-womens` | 限定女装分类 | — |
| `rh=n%3A{node_id}` | 限定子分类节点 | `n%3A1045024`（Dresses） |

### Step 2：JavaScript 提取（核心）

```javascript
// 从搜索结果卡片提取完整字段 — 一段脚本即可
(() => {
  const items = [];
  const cards = document.querySelectorAll('[data-component-type="s-search-result"]');
  cards.forEach((card, i) => {
    if (i >= 20) return;
    const asin = card.getAttribute('data-asin') || '';
    const title = card.querySelector('h2')?.textContent?.trim() || '';
    const priceEl = card.querySelector('.a-price .a-offscreen');
    const price = priceEl ? priceEl.textContent.trim() : 'N/A';
    const originalPriceEl = card.querySelector('[data-a-strike="true"] .a-offscreen');
    const originalPrice = originalPriceEl ? originalPriceEl.textContent.trim() : '';
    const ratingEl = card.querySelector('.a-icon-alt');
    const rating = ratingEl ? ratingEl.textContent.trim() : 'N/A';
    const purchaseBadge = card.querySelector('.a-size-base.a-color-secondary')?.textContent?.trim() || '';
    const bestSeller = card.querySelector('.a-badge-text')?.textContent?.trim() || '';
    const coupon = card.querySelector('.s-coupon-highlight-color')?.textContent?.trim() || '';
    items.push({ rank: i+1, asin, title: title.substring(0, 80), price, originalPrice, rating, purchaseBadge, bestSeller, coupon });
  });
  return items;
})()
```

### Step 3：分析输出

提取数据后按以下框架呈现：

1. **结构化表格**：排名 | ASIN | 商品 | 价格(≈USD) | 评分 | 月销量信号
2. **价格带分析**：低价带/主力带/高端带分布
3. **热销特征**：高频关键词（材质、款式、功能点）聚类
4. **品牌集中度**：Top 品牌占据席位
5. **选品信号**：低竞争高评分、价格空白带、功能差异化机会

## 注意事项（Pitfalls）

| 问题 | 表现 | 解决 |
|------|------|------|
| **配送地址非美国** | 价格显示 JPY/GBP 而非 USD | 点击 "配送至" → 输入美国邮编 10001 |
| **评分字段取不到** | `.a-icon-alt` 返回空 | 分两次 `browser_console` 调用，尝试不同选择器 |
| **页面截断** | snapshot 只显示前几个商品 | 先 `browser_scroll(direction="down")` 再 snapshot |
| **反爬/验证码** | 页面加载异常 | 降低频率，避免 5 秒内多次刷新同一页面 |
| **Best Sellers URL 重定向** | 导航到分类页但跳回上级 | 改用关键词搜索 + 畅销排序更稳定 |

## 数据可信度标注

| 字段 | 性质 | 可信度 |
|------|------|:--:|
| 价格（前台展示价） | 真实数据 | 🟢 高 |
| 评分/评论数 | 公开数据 | 🟢 高 |
| 月销量标签（"700+ bought"） | Amazon 官方标签，非精确数字 | 🟡 中 |
| 搜索排序 | 受配送地址、个性化影响 | 🟡 中 |

> ⚠️ 此方法不适合需要精确 BSR 排名或销量估算的场景——这些应使用 Jungle Scout / Keepa API。

## 与其他工具的互补

| 场景 | 推荐工具 |
|------|---------|
| 精确 BSR + 销量估算 | Jungle Scout / Keepa |
| 关键词流量反查 | 卖家精灵 |
| 跨平台榜单对比 | AlphaShop |
| 快速扫榜 + 零成本 | **本方案（浏览器提取）** |
| 评论深度分析 | amazon-review-scraper |
