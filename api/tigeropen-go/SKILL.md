---
name: tigeropen-go
description: |
  Tiger Brokers OpenAPI Go SDK — complete skills for AI coding tools. Covers SDK setup, market data queries, stock/futures/options trading, real-time push subscriptions, and raw API calls. Use when building trading applications in Go, querying market data, placing orders, or integrating Tiger Brokers API.
  老虎证券 OpenAPI Go SDK 完整技能集。涵盖 SDK 配置、行情查询、股票/期货/期权交易、实时推送订阅。适用于用 Go 语言构建交易应用、查询行情数据、下单交易。
  用户提到以下关键词时自动使用 / Auto-activate on these keywords: 行情、报价、价格、K线、快照、买卖盘、深度、买入、卖出、下单、撤单、改单、交易、持仓、资金、账户、订单、委托、期权、期货、推送、订阅、Go SDK、golang、tigeropen go、quote、price、K-line、order、buy、sell、trade、position、asset、account、option、future、push
license: Apache-2.0
compatibility: Requires Go 1.20+
metadata:
  author: tigerbrokers
  version: "0.5.1"
  language: zh_CN, en_US
---

# Tiger Open API Go SDK

> 老虎量化开放平台 Go SDK 完整技能集 / Complete AI skill set for Tiger Brokers OpenAPI (Go)

> **安全警告 / Safety Warning**: 交易涉及真实资金。生成交易代码时默认使用**模拟账户**，除非用户明确要求实盘。实盘下单前必须与用户确认订单详情。
> Trading involves real money. Default to **Paper Trading** when generating trading code. Always confirm order details before live orders.

- Docs: https://docs.itigerup.com/docs/prepare
- GitHub: https://github.com/tigerfintech/openapi-go-sdk
- Module: `github.com/tigerfintech/openapi-go-sdk` | Go 1.20+

## Language Rules / 语言规则

根据用户输入语言自动回复。技术术语（代码、API 名称、参数名）保持原文不翻译。
Reply in the user's language. Keep technical terms (code, API names, parameters) as-is.

## Reference Guides

- **[Quickstart](references/quickstart.md)** — SDK install, config, client setup, enums, error handling
- **[Market Data](references/quote.md)** — Real-time quotes, K-lines, depth, options, futures
- **[Trading](references/trade.md)** — Place/modify/cancel orders, query positions and assets
- **[Real-time Push](references/push.md)** — WebSocket push for quotes, orders, positions, assets
- **[Account Management](references/account.md)** — Account list, assets, positions, fund transfer, deposit/withdrawal
- **[Options Trading](references/option.md)** — Option chain, expirations, Greeks, multi-leg strategies

## Quick Start

```go
package main

import (
    "fmt"
    "log"

    "github.com/tigerfintech/openapi-go-sdk/client"
    "github.com/tigerfintech/openapi-go-sdk/config"
    "github.com/tigerfintech/openapi-go-sdk/model"
    "github.com/tigerfintech/openapi-go-sdk/quote"
    "github.com/tigerfintech/openapi-go-sdk/trade"
)

func main() {
    // 1. 创建配置 / Create config
    cfg, err := config.NewClientConfig(
        config.WithTigerID("your_tiger_id"),
        config.WithPrivateKey("your_rsa_private_key"),
        config.WithAccount("your_account"),
    )
    if err != nil {
        log.Fatal(err)
    }

    // 2. 创建 HTTP 客户端 / Create HTTP client
    httpClient := client.NewHttpClient(cfg)

    // 3. 查询行情 / Query quotes
    qc := quote.NewQuoteClient(httpClient)
    briefs, err := qc.GetRealTimeQuote(model.BriefRequest{
        Symbols: []string{"AAPL", "TSLA"},
    })
    if err != nil {
        log.Fatal(err)
    }
    for _, b := range briefs {
        fmt.Printf("%s latest=%.2f\n", b.Symbol, b.LatestPrice)
    }

    // 4. 交易操作 / Trading
    tc := trade.NewTradeClient(httpClient, cfg.Account)
    orders, err := tc.Orders(model.OrdersRequest{Limit: 20})
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("orders:", len(orders))
}
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
