---
name: tigeropen
description: |
  Tiger Brokers OpenAPI Python SDK — complete skills for AI coding tools. Covers SDK setup, market data queries, stock/futures/options trading, real-time push subscriptions, CLI command-line tool, and MCP server integration. Use when building trading applications, querying market data, placing orders, using the tigeropen CLI, or integrating Tiger Brokers API with AI editors.
  老虎证券 OpenAPI Python SDK 完整技能集。涵盖 SDK 配置、行情查询、股票/期货/期权交易、实时推送订阅、CLI 命令行工具、MCP Server 集成。适用于构建交易应用、查询行情数据、下单交易、使用 tigeropen CLI、或将老虎 API 集成到 AI 编辑器。
  用户提到以下关键词时自动使用 / Auto-activate on these keywords: 行情、报价、价格、K线、快照、买卖盘、深度、买入、卖出、下单、撤单、改单、交易、持仓、资金、账户、订单、委托、期权、期权链、到期日、期货、推送、订阅、选股、筛选、tigeropen、tiger API、quote、price、K-line、order、buy、sell、trade、position、asset、account、option、future、push、scanner
license: Apache-2.0
compatibility: Requires Python 3.8+, pip, and a Tiger Brokers developer account
metadata:
  author: tigerbrokers
  version: "3.7.1"
  language: zh_CN, en_US
  openclaw:
    requires:
      env:
        - TIGEROPEN_TIGER_ID
        - TIGEROPEN_PRIVATE_KEY
        - TIGEROPEN_ACCOUNT
      bins:
        - pip
        - python
    primaryEnv: TIGEROPEN_TIGER_ID
---

# Tiger Open API Python SDK

> 老虎量化开放平台 Python SDK 完整技能集 / Complete AI skill set for Tiger Brokers OpenAPI

> **安全警告 / Safety Warning**: 交易涉及真实资金。生成交易代码时默认使用**模拟账户**（Paper Trading），除非用户明确要求实盘。实盘下单前**必须**：1) 调用 `preview_order()` 展示预估佣金；2) 以表格展示订单详情；3) **停止并等待用户明确确认后**才能调用 `place_order()`。
> Trading involves real money. Default to **Paper Trading** unless the user explicitly requests live trading. Before any live `place_order()` call: 1) call `preview_order()` and show estimated fees, 2) display order details in a table, 3) **stop and wait for explicit user confirmation** — never auto-submit.

- Docs: https://docs.itigerup.com/docs/prepare
- GitHub: https://github.com/tigerfintech/openapi-python-sdk
- SDK: `pip install tigeropen` | Python 3.8 - 3.14

## Language Rules / 语言规则

根据用户输入语言自动回复。用户使用英文提问则用英文回复，使用中文提问则用中文回复。技术术语（代码、API 名称、参数名）保持原文不翻译。
Reply in the user's language. Keep technical terms (code, API names, parameters) as-is.

## Reference Guides

This skill is organized into focused reference files. Load the relevant guide based on your task:

- **[Quickstart](references/quickstart.md)** — SDK install, authentication, client setup, enums/objects, error codes, FAQ
- **[Market Data](references/quote.md)** — Real-time quotes, K-lines, depth, ticks, capital flow, fundamentals, scanner
- **[Trading](references/trade.md)** — Place orders (market/limit/stop/algo), order management, assets, positions, fund transfers
- **[Options](references/option.md)** — Option chains, Greeks, single-leg/multi-leg combos, option calculator
- **[Real-time Push](references/push.md)** — Subscribe to quote/depth/tick/K-line/order/position/asset changes via PushClient
- **[CLI Tool](references/cli.md)** — Command-line interface: config, quote, trade, account, push commands with table/json/csv output
- **[MCP Server](references/mcp.md)** — Expose Tiger API as MCP tools for Cursor, Claude Code, Kiro, Trae

## Quick Start

```python
from tigeropen.common.consts import Language, Market
from tigeropen.tiger_open_config import TigerOpenClientConfig
from tigeropen.common.util.signature_utils import read_private_key
from tigeropen.quote.quote_client import QuoteClient
from tigeropen.trade.trade_client import TradeClient

# 1. Configure / 配置
# 方式一：配置文件(推荐) / Method 1: Config file (recommended)
config = TigerOpenClientConfig(props_path='/path/to/your/config/')

# 方式二：代码赋值 / Method 2: Code assignment
# config = TigerOpenClientConfig()
# config.tiger_id = 'your_tiger_id'
# config.private_key = read_private_key('/path/to/your_private_key.pem')
# config.account = 'your_account'
# config.language = Language.en_US

# 2. Query quotes / 查询行情
quote_client = QuoteClient(config)
quote = quote_client.get_market_status(Market.US)

# 3. Place order / 下单
trade_client = TradeClient(config)
# See references/trade.md for order examples
```

## When to Use Each Reference

| Task | Reference |
|------|-----------|
| First time setup, SDK install, auth config | [quickstart.md](references/quickstart.md) |
| Get stock/option/future quotes, K-lines, screener | [quote.md](references/quote.md) |
| Place/modify/cancel orders, check positions/assets | [trade.md](references/trade.md) |
| Option chains, Greeks, combo strategies | [option.md](references/option.md) |
| Real-time streaming data via WebSocket | [push.md](references/push.md) |
| CLI commands: query data, manage orders from terminal | [cli.md](references/cli.md) |
| Set up MCP Server for AI editor integration | [mcp.md](references/mcp.md) |

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
