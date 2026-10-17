---
name: tigeropen-csharp
description: |
  Tiger Brokers OpenAPI C# SDK — complete skills for AI coding tools. Covers SDK setup, market data queries, trading, and real-time push subscriptions. Use when building trading applications in C#/.NET, querying market data, placing orders, or integrating Tiger Brokers API.
  老虎证券 OpenAPI C# SDK 完整技能集。涵盖 SDK 配置、行情查询、交易、实时推送订阅。适用于用 C#/.NET 构建交易应用、查询行情数据、下单交易。
  用户提到以下关键词时自动使用 / Auto-activate on these keywords: 行情、报价、K线、买入、卖出、下单、撤单、交易、持仓、资金、账户、订单、期权、期货、推送、订阅、C# SDK、csharp SDK、dotnet SDK、tigeropen csharp、openapi csharp、quote、price、K-line、order、buy、sell、trade、position、asset、option、future、push
license: Apache-2.0
compatibility: Requires .NET 10.0 (net10.0), C# 14 default
metadata:
  author: tigerbrokers
  version: "1.2.3"
  language: zh_CN, en_US
---

# Tiger Open API C# SDK

> 老虎量化开放平台 C# SDK 完整技能集 / Complete AI skill set for Tiger Brokers OpenAPI (C#)

> **安全警告 / Safety Warning**: 交易涉及真实资金。生成交易代码时默认使用**模拟账户**，除非用户明确要求实盘。实盘下单前必须与用户确认订单详情。
> Trading involves real money. Default to **Paper Trading** when generating trading code. Always confirm order details before live orders.

- Docs: https://quant.itigerup.com/openapi/zh/csharp/overview/introduction.html
- GitHub: https://github.com/tigerfintech/openapi-cs-sdk
- .NET 10.0 (net10.0), C# 14 default

## Language Rules / 语言规则

根据用户输入语言自动回复。技术术语（代码、API 名称、参数名）保持原文不翻译。
Reply in the user's language. Keep technical terms (code, API names, parameters) as-is.

## Reference Guides

- **[Quickstart](references/quickstart.md)** — NuGet install, config, client creation, error handling
- **[Market Data](references/quote.md)** — Real-time quotes, K-lines, depth, options, futures
- **[Trading](references/trade.md)** — Place/modify/cancel orders, positions, assets
- **[Real-time Push](references/push.md)** — TCP/WebSocket push for quotes, orders, positions
- **[Account Management](references/account.md)** — Account list, assets, positions, fund transfer, deposit/withdrawal
- **[Options Trading](references/option.md)** — Option chain, expirations, Greeks, multi-leg strategies

## Quick Start

```csharp
using TigerOpenAPI.Config;
using TigerOpenAPI.Common.Enum;
using TigerOpenAPI.Quote;
using TigerOpenAPI.Quote.Model;
using TigerOpenAPI.Trade;

// 1. 创建配置 / Create config
TigerConfig config = new TigerConfig()
{
    ConfigFilePath = "path/to/config/",
    Language = Language.en_US,
};

// 2. 查询行情 / Query quotes
QuoteClient quoteClient = new QuoteClient(config);
var request = new TigerRequest<QuoteRealTimeQuoteResponse>()
{
    ApiMethodName = QuoteApiService.QUOTE_REAL_TIME,
    ModelValue = new QuoteSymbolModel() { Symbols = new List<string> { "AAPL", "TSLA" } }
};
var response = await quoteClient.ExecuteAsync(request);

// 3. 查询订单 / Query orders
TradeClient tradeClient = new TradeClient(config);
var orderRequest = new TigerRequest<OrderBatchResponse>()
{
    ApiMethodName = TradeApiService.ORDERS,
    ModelValue = new QueryOrderModel() { Account = config.DefaultAccount }
};
var orderResponse = await tradeClient.ExecuteAsync(orderRequest);
```

## When to Use Each Reference

| Task | Reference |
|------|-----------|
| First time setup, NuGet install, auth config | [quickstart.md](references/quickstart.md) |
| Get stock/option/future quotes, K-lines | [quote.md](references/quote.md) |
| Place/modify/cancel orders, check positions/assets | [trade.md](references/trade.md) |
| Real-time streaming data via TCP socket | [push.md](references/push.md) |
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
