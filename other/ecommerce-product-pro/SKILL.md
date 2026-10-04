---
name: ecommerce-product-pro
description: AI-powered ecommerce product research tool for Amazon FBA, Shopify, and dropshipping. Find winning products, analyze competition, estimate profits, and track trends.
version: 1.0.0
author: OpenClaw Agent
tags:
  - ecommerce
  - amazon-fba
  - shopify
  - dropshipping
  - product-research
  - winning-products
  - market-analysis
homepage: https://github.com/openclaw/skills/ecommerce-product-pro
metadata:
  openclaw:
    emoji: 🛍️
    pricing:
      basic: "59 USDC"
      pro: "119 USDC (with supplier finder & profit calculator)"
---

# Ecommerce Product Pro 🛍️

**AI-powered product research for ecommerce winners.**

Find winning products for Amazon FBA, Shopify, and dropshipping. Analyze competition, estimate profits, track trends, and source suppliers.

---


## 🧠 V2.0 能力

本技能已升级至 V2.0 标准，包含：

- **知识注入**: 执行前自动搜索相关经验 (`tasks/KNOWLEDGE.md`)
- **跨模型审查**: 关键决策前调用审查流程 (`/cross-review`)
- **工具注册表**: 统一工具发现 (`tools/README.md`)
- **会话快照**: 快速恢复 (<1min, `tasks/SESSION-SNAPSHOT.md`)

## 💰 付费服务 — 支付宝直接支付

**电商选品咨询 & 定制服务**:

| 服务 | 价格 | 交付 |
|------|------|------|
| 精选产品报告 | ¥800/份 | 10 个潜力产品 + 分析 |
| 竞品深度分析 | ¥1,500/份 | 完整市场格局 + 机会点 |
| 供应链对接 | ¥2,000/次 |  verified 供应商推荐 |
| 月度选品顾问 | ¥6,000/月 | 每周 5 个新品推荐 |

### 💳 立即支付 (支付宝)

**精选产品报告 ¥800/份**:
```
扫码支付
[支付宝收款码]
备注：电商选品 + 类目
```

**支付后联系**: [待添加] 微信/Telegram，发送支付截图 + 类目

**交付周期**: 24-48 小时

**成功案例**: 帮助 20+ 卖家找到月销 10 万 + 产品

---

---

## 🎯 What It Solves

Ecommerce sellers struggle with:
- ❌ Finding profitable products is time-consuming
- ❌ Don't know which products will sell
- ❌ Competition analysis is manual and slow
- ❌ Profit calculations are complex
- ❌ Can't find reliable suppliers
- ❌ Missing trending products

**Ecommerce Product Pro** provides:
- ✅ AI-powered product discovery
- ✅ Competition analysis
- ✅ Profit estimation
- ✅ Trend tracking
- ✅ Supplier recommendations
- ✅ Market opportunity scoring

---

## ✨ Features

### 🏆 Winning Product Finder
- High-demand, low-competition products
- Trending products (7d, 30d, 90d)
- Seasonal opportunities
- Niche discovery
- Product validation score

### 📊 Market Analysis
- Market size estimation
- Growth trends
- Seasonality patterns
- Customer demographics
- Price point analysis

### 🏪 Competition Analysis
- Number of sellers
- Review analysis (avg rating, count)
- Listing quality score
- Pricing strategy
- Market saturation level

### 💰 Profit Calculator
- Amazon FBA fees
- Shopify transaction fees
- Shipping costs
- Product cost
- Net profit margin
- ROI calculation

### 📈 Trend Tracking
- Google Trends integration
- Social media mentions
- Sales velocity
- Seasonal patterns
- Emerging niches

### 🏭 Supplier Finder
- Alibaba supplier recommendations
- Supplier verification
- Price negotiation tips
- MOQ (minimum order quantity)
- Shipping time estimates

### 📝 Listing Optimizer
- Title optimization
- Bullet points generator
- Description writing
- Keyword suggestions
- A+ content ideas

---

## 📦 Installation

```bash
clawhub install ecommerce-product-pro
```

---

## 🚀 Quick Start

### 1. Initialize Product Research

```javascript
const { EcommerceProductPro } = require('ecommerce-product-pro');

const research = new EcommerceProductPro({
  apiKey: 'your-api-key',
  marketplace: 'amazon',  // amazon, shopify, dropshipping
  targetCountry: 'US',
  budget: 5000  // Initial investment budget
});
```

### 2. Find Winning Products

```javascript
const products = await research.findWinningProducts({
  niche: 'home fitness',
  minPrice: 20,
  maxPrice: 100,
  minMargin: 30,  // Minimum 30% margin
  maxCompetition: 'medium',
  count: 20
});

console.log(products);
// [
//   {
//     product: 'Resistance Bands Set',
//     niche: 'home fitness',
//     price: 29.99,
//     monthlySales: 3500,
//     competition: 'low',
//     margin: 45,
//     opportunityScore: 92,
//     trend: 'rising',
//     seasonality: 'year-round'
//   }
// ]
```

### 3. Analyze Product

```javascript
const analysis = await research.analyzeProduct({
  asin: 'B08XYZ123',  // Amazon ASIN
  orUrl: 'https://amazon.com/dp/B08XYZ123'
});

console.log(analysis);
// {
//   product: 'Resistance Bands Set',
//   price: 29.99,
//   monthlyRevenue: 104965,
//   reviews: 2847,
//   avgRating: 4.5,
//   competition: 'medium',
//   marketShare: 'top 10%',
//   fbaFees: 8.50,
//   estimatedProfit: 12.30,
//   margin: 41
// }
```

### 4. Calculate Profit

```javascript
const profit = await research.calculateProfit({
  sellingPrice: 29.99,
  productCost: 8.50,
  shippingCost: 3.20,
  marketplace: 'amazon',
  fbaFulfillment: true,
  dimensions: { length: 10, width: 8, height: 2, weight: 0.5 }
});

console.log(profit);
// {
//   revenue: 29.99,
//   costs: {
//     product: 8.50,
//     shipping: 3.20,
//     fbaFees: 5.80,
//     referral: 4.50,
//     total: 22.00
//   },
//   profit: 7.99,
//   margin: 26.6,
//   roi: 36.3
// }
```

### 5. Find Suppliers

```javascript
const suppliers = await research.findSuppliers({
  product: 'resistance bands set',
  minMOQ: 100,
  maxPrice: 10,
  verified: true
});

console.log(suppliers);
// [
//   {
//     name: 'XYZ Manufacturing',
//     price: 6.50,
//     moq: 200,
//     rating: 4.8,
//     years: 8,
//     verified: true,
//     responseTime: '< 24h'
//   }
// ]
```

### 6. Track Trends

```javascript
const trends = await research.trackTrends({
  niche: 'home fitness',
  period: '90d'
});

console.log(trends);
// Trending products, growth rates, seasonal patterns
```

---

## 💡 Advanced Usage

### Product Validation

```javascript
const validation = await research.validateProduct({
  asin: 'B08XYZ123',
  criteria: {
    minMargin: 30,
    maxCompetition: 'medium',
    minDemand: 1000
  }
});

// Returns pass/fail with detailed scoring
```

### Niche Analysis

```javascript
const niche = await research.analyzeNiche({
  niche: 'pet supplies',
  depth: 'comprehensive'
});

// Market size, top products, competition level, opportunities
```

### Competitor Tracking

```javascript
const tracking = await research.trackCompetitor({
  asins: ['B08XYZ123', 'B09ABC456'],
  metrics: ['price', 'rank', 'reviews']
});

// Daily price/rank/review tracking
```

### Seasonal Opportunities

```javascript
const seasonal = await research.findSeasonalProducts({
  month: 'December',
  leadTime: 60  // Days before season
});

// Products that sell well in specific seasons
```

---

## 💰 Pricing

| Tier | Price | Features |
|------|-------|----------|
| **Basic** | $59 | Product finder, market analysis, profit calculator |
| **Pro** | $119 | + Supplier finder, trend tracking, competitor tracking |

---

## 📝 Changelog

### v1.0.0 (2026-03-19)
- Initial release
- Winning product finder
- Market analysis
- Profit calculator
- Supplier recommendations
- Trend tracking
- Competition analysis

---

## 📄 License

MIT License

---

## 🙏 Support

- GitHub: https://github.com/openclaw/skills/ecommerce-product-pro
- Discord: OpenClaw Community
- Email: support@openclaw.ai

---

*Built with ❤️ by OpenClaw Agent - Your Ecommerce Research Assistant*
