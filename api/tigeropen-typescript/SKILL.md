---
name: tigeropen-typescript
description: |
  Tiger Brokers OpenAPI TypeScript SDK — complete skills for AI coding tools. Covers SDK setup, market data queries, trading, and real-time push subscriptions. Use when building trading applications in TypeScript/Node.js, querying market data, placing orders, or integrating Tiger Brokers API.
  老虎证券 OpenAPI TypeScript SDK 完整技能集。涵盖 SDK 配置、行情查询、交易、实时推送订阅。适用于用 TypeScript/Node.js 构建交易应用、查询行情数据、下单交易。
  用户提到以下关键词时自动使用 / Auto-activate on these keywords: 行情、报价、K线、买入、卖出、下单、撤单、交易、持仓、资金、账户、订单、期权、期货、推送、订阅、TypeScript SDK、tigeropen typescript、quote、price、K-line、order、buy、sell、trade、position、asset、option、future、push
license: MIT
compatibility: Requires Node.js 16+, supports ESM and CommonJS
metadata:
  author: tigerbrokers
  version: "0.5.4"
  language: zh_CN, en_US
---

# Tiger Open API TypeScript SDK

> 老虎量化开放平台 TypeScript SDK 完整技能集 / Complete AI skill set for Tiger Brokers OpenAPI (TypeScript)

> **安全警告 / Safety Warning**: 交易涉及真实资金。生成交易代码时默认使用**模拟账户**，除非用户明确要求实盘。实盘下单前必须与用户确认订单详情。
> Trading involves real money. Default to **Paper Trading** when generating trading code. Always confirm order details before live orders.

- Docs: https://docs.itigerup.com/docs/prepare
- npm: `npm install @tigeropenapi/tigeropen` | Node.js 16+, ESM/CommonJS

## Language Rules / 语言规则

根据用户输入语言自动回复。技术术语（代码、API 名称、参数名）保持原文不翻译。
Reply in the user's language. Keep technical terms (code, API names, parameters) as-is.

## Reference Guides

- **[Quickstart](references/quickstart.md)** — SDK install, config, client setup, error handling
- **[Market Data](references/quote.md)** — Real-time quotes, K-lines, depth, options, futures
- **[Trading](references/trade.md)** — Place/modify/cancel orders, positions, assets
- **[Real-time Push](references/push.md)** — WebSocket push for quotes, orders, positions
- **[Account Management](references/account.md)** — Account list, assets, positions, fund transfer, deposit/withdrawal
- **[Options Trading](references/option.md)** — Option chain, expirations, Greeks, multi-leg strategies

## Quick Start

```typescript
import {
  createClientConfig,
  HttpClient,
  QuoteClient,
  TradeClient,
} from '@tigeropenapi/tigeropen';

// 1. 创建配置 / Create config
const config = createClientConfig({
  tigerId: 'your_tiger_id',
  privateKey: 'your_rsa_private_key',
  account: 'your_account',
});

// 2. 查询行情 / Query quotes（注意：接收请求对象，不是数组）
const httpClient = new HttpClient(config);
const qc = new QuoteClient(httpClient);
const quotes = await qc.getBrief({ symbols: ['AAPL', 'TSLA'] });
console.log(quotes);

// 3. 交易操作 / Trading
const tc = new TradeClient(httpClient, config.account);
const orders = await tc.getOrders({ limit: 20 });
console.log(orders);
```

## When to Use Each Reference

| Task | Reference |
|------|-----------|
| First time setup, SDK install, auth config | [quickstart.md](references/quickstart.md) |
| Get stock/option/future quotes, K-lines | [quote.md](references/quote.md) |
| Place/modify/cancel orders, check positions/assets | [trade.md](references/trade.md) |
| Real-time streaming data via WebSocket | [push.md](references/push.md) |
| Account info, assets, fund transfer, deposit/withdrawal | [account.md](references/account.md) |
| Option chain, Greeks, expirations, multi-leg orders | [option.md](references/option.md) |

## Common Symbols / 常见标的速查

### 港股 HK

| 常见称呼 | 代码 Symbol |
|---------|------------|
| 腾讯 | 00700 |
| 阿里巴巴 | 09988 |
| 美团 | 03690 |
| 小米 | 01810 |

### 美股 US

| 常见称呼 | 代码 Symbol |
|---------|------------|
| 苹果 / Apple | AAPL |
| 特斯拉 / Tesla | TSLA |
| 英伟达 / NVIDIA | NVDA |
| 微软 / Microsoft | MSFT |
| 谷歌 / Google | GOOGL |
| 亚马逊 / Amazon | AMZN |
| Meta | META |
| 老虎证券 / TIGR | TIGR |
| 标普500 ETF / SPY | SPY |
| 纳指 ETF / QQQ | QQQ |
