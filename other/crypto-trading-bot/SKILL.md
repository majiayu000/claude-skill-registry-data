---
name: crypto-trading-bot
description: 加密貨幣交易機器人開發 - 幫你整自動交易Bot，支持Pine Script、Python、CCXT API對接。適用於：(1)整TradingView信號Bot (2)CEX/DEX API自動化 (3)套利機器人 (4)止盈止損策略
---

# Crypto Trading Bot Developer

幫你整加密貨幣自動交易機器人

## 核心功能

### 1. TradingView Pine Script 信号 Bot
- 接收TradingView webhook信號
- 自動執行買賣指令
- 支持多交易所對接

### 2. CEX 自動化交易
- Binance, Bybit, OKX API 對接
- 現貨/合約自動化
- 網格交易策略

### 3. DEX Arbitrage
- 跨DEX套利機會檢測
- Flash loan 整合（如適用）
- 風險評估

### 4. 智能止盈止損
- 移動止損
- 分批止盈
- Time-based exit

## 使用流程

```
1. 用戶話「整交易Bot」
2. 問清楚：
   - 目標交易所
   - 交易對 (e.g., BTC/USDT)
   - 策略類型
   - 預算
3. 提供報價同timeline
```

## 報價參考

| 類型 | 價格範圍 |
|------|----------|
| 簡單信號Bot | $200-500 |
| 網格交易 | $300-800 |
| 複雜策略 | $1000-3000 |
| 月費維護 | $100-300/月 |

## 技術栈

- Python (CCXT, pandas)
- Pine Script
- Node.js
- API Webhooks
