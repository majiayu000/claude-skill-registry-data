---
name: tigeropen-cpp
description: |
  Tiger Brokers OpenAPI C++ SDK — complete skills for AI coding tools. Covers SDK build setup, market data queries, trading, and real-time push subscriptions. Use when building trading applications in C++, querying market data, placing orders, or integrating Tiger Brokers API.
  老虎证券 OpenAPI C++ SDK 完整技能集。涵盖 SDK 编译配置、行情查询、交易、实时推送订阅。适用于用 C++ 构建交易应用、查询行情数据、下单交易。
  用户提到以下关键词时自动使用 / Auto-activate on these keywords: 行情、报价、K线、买入、卖出、下单、撤单、交易、持仓、资金、账户、订单、期权、期货、推送、订阅、C++ SDK、tigeropen cpp、openapi cpp、quote、price、K-line、order、buy、sell、trade、position、asset、option、future、push
license: Apache-2.0
compatibility: Requires C++14, CMake 3.15+, Boost 1.86, cpprestsdk, Protobuf 5.28.3, Abseil 20240722.0
metadata:
  author: tigerbrokers
  version: "1.3.0"
  language: zh_CN, en_US
---

# Tiger Open API C++ SDK

> 老虎量化开放平台 C++ SDK 完整技能集 / Complete AI skill set for Tiger Brokers OpenAPI (C++)

> **安全警告 / Safety Warning**: 交易涉及真实资金。生成交易代码时默认使用**模拟账户**，除非用户明确要求实盘。实盘下单前必须与用户确认订单详情。
> Trading involves real money. Default to **Paper Trading** when generating trading code. Always confirm order details before live orders.

- Docs: https://docs.itigerup.com/docs/prepare
- GitHub: https://github.com/tigerfintech/openapi-cpp-sdk
- C++14, CMake 3.15+, cross-platform (macOS/Linux/Windows)

## Language Rules / 语言规则

根据用户输入语言自动回复。技术术语（代码、API 名称、参数名）保持原文不翻译。
Reply in the user's language. Keep technical terms (code, API names, parameters) as-is.

## Reference Guides

- **[Quickstart](references/quickstart.md)** — Build setup, CMake, config, client creation
- **[Market Data](references/quote.md)** — Real-time quotes, K-lines, depth, options, futures
- **[Trading](references/trade.md)** — Place/modify/cancel orders, positions, assets
- **[Real-time Push](references/push.md)** — WebSocket push for quotes, orders, positions
- **[Account Management](references/account.md)** — Account list, assets, positions, fund transfer, deposit/withdrawal
- **[Options Trading](references/option.md)** — Option chain, expirations, Greeks, multi-leg strategies

## Quick Start

```cpp
#include "tigerapi/client_config.h"
#include "tigerapi/quote_client.h"
#include "tigerapi/trade_client.h"

using namespace TIGER_API;

int main() {
    // 1. 创建配置 / Create config
    ClientConfig config(false, "path/to/config/");

    // 2. 查询行情 / Query quotes
    QuoteClient qc(config);
    value symbols = value::array();
    symbols[0] = value::string(U("AAPL"));
    symbols[1] = value::string(U("TSLA"));
    value quotes = qc.get_brief(symbols);
    ucout << quotes << std::endl;

    // 3. 交易操作 / Trading
    TradeClient tc(config);
    value orders = tc.get_orders();
    ucout << orders << std::endl;

    return 0;
}
```

## When to Use Each Reference

| Task | Reference |
|------|-----------|
| First time setup, build, CMake, auth config | [quickstart.md](references/quickstart.md) |
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
