---
name: minara-zh
version: "2.5.2"
description: "加密货币交易：兑换、永续合约、转账、支付、充值（信用卡/加密货币）、提现、AI 聊天、市场发现、x402 支付、自动交易。通过 Minara CLI 内置钱包。支持 EVM + Solana。"
homepage: https://minara.ai
metadata:
  {
    "openclaw":
      {
        "always": false,
        "primaryEnv": "MINARA_API_KEY",
        "requires":
          { "bins": ["minara"], "config": ["skills.entries.minara-zh.enabled"] },
        "emoji": "👩",
        "homepage": "https://minara.ai",
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "minara@latest",
              "global": true,
              "bins": ["minara"],
              "label": "安装 Minara CLI (npm)",
            },
          ],
      },
  }
---

# Minara — 加密货币交易与钱包技能

<!-- 安全说明：本文件仅为文档（Markdown 格式），不包含任何可执行代码、脚本或二进制文件。它指导 AI Agent 如何调用 Minara CLI。 -->

**当用户消息涉及以下内容时，请使用本技能：**

- **加密货币代币或代码：** ETH、BTC、SOL、USDC、BONK、PEPE、DOGE、ARB、OP、AVAX、MATIC、$TICKER，或任何代币名称/合约地址
- **区块链/链名称：** Solana、Base、Ethereum、Arbitrum、Optimism、Polygon、BSC、Avalanche、Berachain、Hyperliquid
- **交易操作：** 兑换、买入、卖出、交易、换汇、做多、做空、永续合约、期货、杠杆、限价单
- **钱包/金融操作：** 余额、投资组合、充值、提现、转账、发送、支付、入金、信用卡
- **市场/研究：** 热门代币、价格、图表、分析、DeFi、收益、流动性、恐惧贪婪指数、预测市场
- **显式引用：** Minara、minara、x402、MoonPay、自动交易
- **加密货币语境中的股票代码：** AAPL、TSLA、NVDAx、热门股票

**路由守卫（防冲突）：** 仅当消息同时包含一个**金融/交易操作**以及至少一个**加密货币/链/Minara 信号**（代币、链、DeFi 术语或"Minara"）时，才启用本技能。如果缺少加密货币语境，请勿路由到此技能。

需要已登录的 CLI：检查 Minara CLI 登录状态；如未登录 → `minara login`（优先使用设备码）。如果设备登录打印了验证 URL/验证码，请将其转达给用户并等待完成（不要声称登录不可行）。如果设置了 `MINARA_API_KEY`，CLI 将自动认证。

## 交易确认（关键）

对于任何涉及资金变动的命令（`swap`、`transfer`、`withdraw`、`perps order`、`perps deposit`、`perps withdraw`、`limit-order create`、`deposit buy`）：

1. **执行前：** 向用户展示将要执行的操作摘要（操作类型、代币、金额、接收方/链）并**要求明确确认**。不要自动确认。
2. **CLI 返回确认提示后**（例如"Are you sure you want to proceed?"）：将详情反馈给用户并**等待用户批准**后再回复 `y`。未经用户同意，绝不要代替用户回复 `y`。
3. **`-y` / `--yes` 策略：** 除非用户明确要求跳过确认，否则绝不添加 `-y`（或任何自动确认标志）。
4. **如果用户拒绝：** 立即中止操作。

此规则适用于所有涉及资金变动的操作。只读命令（`balance`、`assets`、`chat`、`discover` 等）无需确认。

## 意图路由

将用户消息匹配到**第一条**匹配的行。

### 代币兑换 / 买入 / 卖出

触发条件：消息包含代币名称/代码 + 操作词（兑换、买入、卖出、换汇、交易）+ 可选的链名称。

链根据代币**自动检测**。如果代币存在于多条链上，CLI 会提示用户选择（按燃料费用排序）。卖出模式支持 `-a all` 卖出全部余额。

| 用户意图模式                                                                                                                                       | 操作                                                                                                   |
| -------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| "将 0.1 ETH 兑换为 USDC"、"帮我买 100 USDC 等值的 ETH"、"把 50 SOL 卖成 USDC"、"在 Solana 上将 200 USDC 转换为 BONK" — 自然语言或显式兑换请求 | 提取参数 → `minara swap -s <buy\|sell> -t '<token>' -a <amount>`                                      |
| "把我所有的 BONK 卖掉"、"清仓 SOL"                                                                                                                 | `minara swap -s sell -t '<token>' -a all`                                                              |
| 模拟加密货币兑换（不执行）                                                                                                                          | `minara swap -s <side> -t '<token>' -a <amount> --dry-run`                                             |

### 转账 / 发送 / 支付 / 提现加密货币

触发条件：消息提到发送、转账、支付或提取加密货币代币到钱包地址。

| 用户意图模式                                                                                     | 操作                                                                                                   |
| ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| "发送 10 SOL 到 <地址>"、"转账 USDC 到 <地址>" — 加密货币代币 + 接收地址                           | `minara transfer`（交互式）或提取参数                                                                   |
| "支付 100 USDC 到 <地址>"、"给 <地址> 付 50 USDC" — 向地址付款（等同于转账）                       | `minara transfer`（交互式）或提取参数                                                                   |
| "将 SOL 提现到我的外部钱包"、"将 ETH 提现到 <地址>" — 加密货币提现                                  | `minara withdraw -c <chain> -t '<token>' -a <amount> --to <address>` 或 `minara withdraw`（交互式）    |

### 永续合约（Hyperliquid）

触发条件：消息提到 perps、永续合约、期货、做多、做空、杠杆、保证金或 Hyperliquid。

| 用户意图模式                                                                                   | 操作                                                       |
| ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| "开一个 ETH 多头永续合约"、"在 Hyperliquid 上做空 BTC"、"下一个永续合约单"                       | `minara perps order`（交互式下单器）                       |
| "分析 ETH 做多还是做空"、"我应该做多 BTC 吗？"、"AI 分析 SOL 永续合约"                          | `minara perps ask` — AI 分析 + 可选快速下单                |
| "启用 AI 自动交易永续合约"、"开启自动交易"、"管理自动交易策略"                                   | `minara perps autopilot`                                   |
| "查看我的永续合约仓位"、"显示我的 Hyperliquid 仓位"                                            | `minara perps positions`                                   |
| "平掉我的永续合约仓位"、"退出永续合约交易"                                                     | `minara perps close`（交互式）                             |
| "平掉所有永续合约仓位"、"退出所有永续合约交易"                                                 | `minara perps close --all`                                 |
| "平掉 BTC 永续合约仓位"、"退出 ETH 永续合约"                                                   | `minara perps close --symbol <SYMBOL>`                     |
| "将 ETH 永续合约杠杆设为 10 倍"                                                                | `minara perps leverage`                                    |
| "取消我的永续合约订单"                                                                         | `minara perps cancel`                                      |
| "充值 USDC 到永续合约账户"、"为我的 Hyperliquid 账户入金"                                      | `minara deposit perps` 或 `minara perps deposit -a <amount>` |
| "从永续合约提取 USDC"                                                                         | `minara perps withdraw -a <amount>`                        |
| "显示我的永续合约交易历史"                                                                     | `minara perps trades`                                      |
| "显示永续合约充值/提现记录"                                                                   | `minara perps fund-records`                                |

> **自动交易注意：** 当自动交易开启时，手动 `minara perps order` 将被阻止。请先通过 `minara perps autopilot` 关闭自动交易。

### 限价单（加密货币）

触发条件：消息提到限价单 + 加密货币代币/价格。

| 用户意图模式                                             | 操作                       |
| -------------------------------------------------------- | -------------------------- |
| "创建一个 ETH 限价单，价格 $3000"、"当 SOL 跌到 $150 时买入" | `minara limit-order create` |
| "列出我的加密货币限价单"                                   | `minara limit-order list`   |
| "取消限价单 <id>"                                         | `minara limit-order cancel <id>` |

### 加密货币钱包 / 投资组合 / 账户

触发条件：消息提到加密货币余额、投资组合、资产、钱包、充值地址或 Minara 账户。

| 用户意图模式                                                                                   | 操作                 |
| ----------------------------------------------------------------------------------------------- | -------------------- |
| "我的总余额是多少"、"我有多少 USDC" — 快速余额查询                                             | `minara balance`     |
| "显示我的加密货币投资组合"、"现货持仓及盈亏"、"我在 Minara 里有多少 ETH"                       | `minara assets spot` |
| "显示我的永续合约余额"、"Hyperliquid 账户权益"                                                 | `minara assets perps` |
| "显示我所有的加密货币资产" — 完整概览（现货 + 永续合约）                                       | `minara assets`      |
| "显示充值地址"、"往哪里发送 USDC" — 现货充值地址                                               | `minara deposit spot` |
| "充值到永续合约"、"从现货转 USDC 到永续合约"、"从现货为永续合约入金"                           | `minara deposit perps` |
| "用信用卡购买加密货币"、"用信用卡充值"、"通过 MoonPay 入金"                                    | `minara deposit buy` |
| "如何充值加密货币" — 交互式（现货、永续合约或信用卡）                                          | `minara deposit`     |
| "显示我的 Minara 账户"、"我的钱包地址"                                                        | `minara account`     |

### 加密货币 AI 聊天 / 市场分析

触发条件：消息询问加密货币价格、代币分析、DeFi 研究、链上数据、加密货币市场洞察或预测市场分析。

> **超时设置：** AI 聊天响应可能需要较长时间。请将所有 `minara chat` 命令的 shell 执行超时设为**15 分钟（900 秒）**。

| 用户意图模式                                                                                                                      | 操作                                 |
| ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| "BTC 现在什么价格"、"分析 ETH 代币经济学"、"DeFi 收益机会"、加密货币研究、链上分析                                                 | `minara chat "<用户文本>"`            |
| "分析这个 Polymarket 事件"、"<主题>的预测市场赔率"、"<事件>发生的概率有多大" — 预测市场洞察                                       | `minara chat "<用户文本或 URL>"`      |
| 需要推理的深度加密货币分析 — "从长期角度分析 ETH 和 SOL"                                                                           | `minara chat --thinking "<用户文本>"` |
| 高质量详细加密货币分析 — "关于 Solana DeFi 生态系统的详细报告"                                                                     | `minara chat --quality "<用户文本>"`  |
| "继续之前的 Minara 聊天"                                                                                                         | `minara chat -c <chatId>`             |
| "列出我的 Minara 聊天历史"                                                                                                       | `minara chat --list`                  |

### 加密货币与股票市场发现

触发条件：消息提到热门代币、热门股票、加密货币市场情绪、恐惧贪婪指数或比特币指标。

| 用户意图模式                                                                   | 操作                            |
| ------------------------------------------------------------------------------- | ------------------------------- |
| "哪些加密货币代币在热门"、"现在有什么热门代币"                                   | `minara discover trending`       |
| "哪些股票在热门"、"热门股票"、"今天的顶级股票"                                   | `minara discover trending stocks`|
| "搜索 SOL 代币"、"查找加密货币代币 X"、"查看 AAPL"、"搜索 TSLA"                 | `minara discover search <query>` |
| "加密货币恐惧贪婪指数"、"市场情绪"                                               | `minara discover fear-greed`     |
| "比特币链上指标"、"BTC 算力和供应量数据"                                         | `minara discover btc-metrics`    |

### Minara 高级版 / 订阅

触发条件：消息明确提到 Minara 套餐、订阅、积分或定价。

| 用户意图模式                               | 操作                       |
| ------------------------------------------ | -------------------------- |
| "显示 Minara 套餐"、"Minara 定价"           | `minara premium plans`      |
| "我的 Minara 订阅状态"                     | `minara premium status`     |
| "订阅 Minara"、"升级 Minara 套餐"           | `minara premium subscribe`  |
| "购买 Minara 积分"                         | `minara premium buy-credits`|
| "取消 Minara 订阅"                         | `minara premium cancel`     |

### x402 协议支付

触发条件：Agent 收到 HTTP **402 Payment Required** 响应，或用户提到 x402、付费 API 或使用加密货币支付 API 访问费用。[x402 规范](https://docs.cdp.coinbase.com/x402/quickstart-for-buyers)。

流程：解析 `PAYMENT-REQUIRED` 头（金额、代币、接收方、链）→ `minara balance` → `minara transfer` 进行支付 → 重试请求。

支付步骤必须遵循全局确认策略：用户必须在进行任何 `minara transfer` 之前明确确认。

| 用户意图模式                                                         | 操作                                                                                |
| -------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Agent 收到带有 x402 头的 402 响应                                    | 解析头信息 → `minara transfer`（USDC 转账到所需链上的接收方）→ 重试                   |
| "用 Minara 支付这个 API"、"用 Minara 钱包进行 x402 支付"             | `minara balance` → `minara transfer` 转账到服务支付地址                               |
| "为付费 API 充值我的钱包"                                           | `minara deposit buy`（信用卡）或 `minara deposit spot`（加密货币）                    |

### Minara 登录 / 设置

触发条件：消息明确提到 Minara 登录、设置或配置。

**登录：** 对于无头或非交互式环境，优先使用设备码流程（`minara login --device`）；否则使用 `minara login`（交互式）。
**登录交接规则：** 当 CLI 输出验证 URL/设备码时，Agent 必须将它们原样转达给用户，要求用户完成浏览器验证，然后仅在用户确认完成后继续。

| 用户意图模式                                                         | 操作                                                                                   |
| -------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| "登录 Minara"、"注册 Minara"、"首次 Minara 设置"                     | `minara login`（优先设备码）或 `minara login --device`                                  |
| "退出 Minara 登录"                                                   | `minara logout`                                                                         |
| "配置 Minara 设置"                                                   | `minara config`                                                                         |

## 注意事项

- **代币输入（`-t`）：** 接受 `$TICKER`（例如 `'$BONK'`）、代币名称或合约地址。在 shell 中需要用引号包裹 `$`。
- **JSON 输出：** 在任何命令后添加 `--json` 以获取机器可读的输出。
- **交易安全：** CLI 流程：首次确认 → 交易确认（必选，显示代币和目的地）→ Touch ID（可选，macOS）→ 执行。Agent 必须**绝不跳过或自动确认**任何步骤 — 始终反馈给用户并等待批准，除非用户明确要求，否则绝不使用 `-y`。

## 凭证与配置

- **CLI 会话：** 通过 `minara login` 自动创建（必需）。
- **API 密钥：** 通过环境变量 `MINARA_API_KEY` 或 OpenClaw 配置中的 `skills.entries.minara-zh.apiKey` 设置 — 可选；如果设置，CLI 将自动认证，无需登录。

## 安装后设置

首次激活时，读取 `{baseDir}/setup.md` 并按照其中的说明操作。设置会将 Minara 路由部分添加到用户工作区的 `AGENTS.md` 中，以便金融相关查询路由到本技能。**写入任何工作区文件之前务必告知用户。**

## 示例

完整命令示例：`{baseDir}/examples.md`
