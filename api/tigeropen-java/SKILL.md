---
name: tigeropen-java
description: |
  Tiger Brokers OpenAPI Java SDK — complete skills for AI coding tools. Covers SDK setup, market data queries, stock/futures/options trading, real-time push subscriptions, account management, and strategy examples. Use when building Java trading applications, querying market data, placing orders, or integrating Tiger Brokers API.
  老虎证券 OpenAPI Java SDK 完整技能集。涵盖 SDK 配置、行情查询、股票/期货/期权交易、实时推送订阅、账户管理、策略示例。适用于构建 Java 交易应用、查询行情数据、下单交易、或集成老虎 API。
  用户提到以下关键词时自动使用 / Auto-activate on these keywords: 行情、报价、价格、K线、快照、买卖盘、深度、买入、卖出、下单、撤单、改单、交易、持仓、资金、账户、订单、委托、期权、期权链、到期日、期货、推送、订阅、选股、筛选、tigeropen、tiger API、Java SDK、quote、price、K-line、order、buy、sell、trade、position、asset、account、option、future、push、scanner
license: Apache-2.0
compatibility: Requires Java JDK 1.8+, Maven or Gradle, and a Tiger Brokers developer account
metadata:
  author: tigerbrokers
  version: "2.6.0"
  language: zh_CN, en_US
---

# Tiger Open API Java SDK

> 老虎量化开放平台 Java SDK 完整技能集 / Complete AI skill set for Tiger Brokers OpenAPI (Java)

> **安全警告 / Safety Warning**: 交易涉及真实资金。生成交易代码时默认使用**模拟账户**（Paper Trading），除非用户明确要求实盘。实盘下单前必须与用户确认订单详情。
> Trading involves real money. Default to **Paper Trading** account when generating trading code unless the user explicitly requests live trading. Always confirm order details with the user before live orders.

- Docs: https://docs.itigerup.com/docs/prepare-java
- GitHub: https://github.com/tigerbrokers/openapi-java-sdk
- SDK: Maven `io.github.tigerbrokers:openapi-java-sdk` | Java 1.8+

## Language Rules / 语言规则

根据用户输入语言自动回复。用户使用英文提问则用英文回复，使用中文提问则用中文回复。技术术语（代码、API 名称、参数名）保持原文不翻译。
Reply in the user's language. Keep technical terms (code, API names, parameters) as-is.

## Reference Guides

This skill is organized into focused reference files. Load the relevant guide based on your task:

- **[Quickstart](references/quickstart.md)** — SDK install (Maven/Gradle), authentication, client setup, basic examples, object reference, strategy examples
- **[Market Data](references/quote.md)** — Stock/futures/fund/crypto/warrant quotes, K-lines, depth, ticks, scanner, fundamentals, corporate actions
- **[Trading](references/trade.md)** — Place orders (market/limit/stop/algo), order management, contracts, assets, positions, fund transfers
- **[Options](references/option.md)** — Option expiration dates, chains, Greeks, K-line, tick data
- **[Real-time Push](references/push.md)** — Subscribe to quote/depth/tick/K-line/order/position/asset changes via WebSocketClient
- **[Account](references/account.md)** — Account queries, assets, positions, analytics, P&L

## Quick Start

```java
import com.tigerbrokers.stock.openapi.client.config.ClientConfig;
import com.tigerbrokers.stock.openapi.client.https.client.TigerHttpClient;
import com.tigerbrokers.stock.openapi.client.https.request.quote.QuoteMarketRequest;
import com.tigerbrokers.stock.openapi.client.https.response.quote.QuoteMarketResponse;

// 1. Configure / 配置
ClientConfig clientConfig = ClientConfig.DEFAULT_CONFIG;
clientConfig.tigerId = "your_tiger_id";
clientConfig.defaultAccount = "your_account";
clientConfig.privateKey = "your_private_key_content";

// 2. Create client / 创建客户端
TigerHttpClient client = TigerHttpClient.getInstance().clientConfig(clientConfig);

// 3. Query market status / 查询市场状态
QuoteMarketResponse response = client.execute(QuoteMarketRequest.newRequest(Market.US));
```

## When to Use Each Reference

| Task | Reference |
|------|-----------|
| First time setup, SDK install, auth config | [quickstart.md](references/quickstart.md) |
| Get stock/option/future quotes, K-lines, screener | [quote.md](references/quote.md) |
| Place/modify/cancel orders, check positions/assets | [trade.md](references/trade.md) |
| Option chains, Greeks, expiration dates | [option.md](references/option.md) |
| Real-time streaming data via WebSocket | [push.md](references/push.md) |
| Account info, assets, positions, P&L analytics | [account.md](references/account.md) |

## Common Symbols / 常见标的速查

当用户使用中文名称或英文简称时，按下表映射。不在表中的标的根据上下文判断。
Map user's natural language to symbols. For unlisted symbols, infer from context.

### 港股 HK

| 常见称呼 | 代码 Symbol |
|---------|------------|
| 腾讯 | 00700 |
| 阿里巴巴、阿里 | 09988 |
| 美团 | 03690 |
| 小米 | 01810 |
| 京东 | 09618 |
| 比亚迪 | 01211 |
| 快手 | 01024 |
| 百度 | 09888 |
| 网易 | 09999 |
| 中芯国际 | 00981 |
| MINIMAX | 00100 |
| 智谱 | 02513 |

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
| 台积电 / TSM | TSM |
| AMD | AMD |
| 老虎证券 / Tiger / TIGR | TIGR |
| 阿里巴巴（美股）/ BABA | BABA |
| 京东（美股）/ JD | JD |
| 拼多多 / PDD | PDD |
| 标普500 ETF / SPY | SPY |
| 纳指 ETF / QQQ | QQQ |
