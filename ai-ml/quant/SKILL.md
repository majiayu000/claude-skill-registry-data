---
name: quant-trading
description: "量化交易核心skill套件 — 因子挖掘、Alpha衰减监控、多市场套利、订单路由、压力测试、归因分析、仓位管理、样本外验证、A股T0、加密资金费率套利、Polymarket机器人。对标国际顶级量化基金（Renaissance/Two Sigma/Citadel/DE Shaw）的工程与策略水平。"
---

# 量化交易 Skill Suite

> 烛龙核心武器库 — 对标全球顶级量化对冲基金的工程化策略体系

## 定位

本目录包含 **14个量化交易专用skill文件**，覆盖因子挖掘→Alpha衰减→策略归因→风控→执行的完整闭环。每个skill均可通过 `#skill:quant/xxx` 直接引用。

## 目录索引

### 🔬 因子与Alpha
| 文件 | 核心功能 | 对标机构 |
|------|---------|---------|
| `factor-mining-cluster.md` | 多因子挖掘与特征工程，CART/G.fmm/AutoEncoder三维框架 | Two Sigma, WorldQuant |
| `alpha-decay-monitor.md` | 实时监控Alpha衰减，分级告警，自动化响应 | Renaissance, DE Shaw |
| `alpha-factor-review.md` | 因子验收检查清单，IC/IR/衰减率/换手率/容量 | WorldQuant |
| `quant-bounty-architect.md` | 量化竞赛架构，Kaggle模式驱动社区创新 | Numerai, Kaggle |

### 📊 策略验证
| 文件 | 核心功能 | 对标机构 |
|------|---------|---------|
| `out-of-sample-validator.md` | 样本外测试框架，时序/组合/交叉验证 | Citadel, AQR |
| `stress-test-simulator.md` | 极端市场情境模拟，尾部风险量化 | Bridgewater, PIMCO |
| `strategy-attribution.md` | Brinson归因+因子归因，收益来源拆解 | MSCI Barra |

### ⚡ 执行与套利
| 文件 | 核心功能 | 对标机构 |
|------|---------|---------|
| `smart-order-router.md` | 智能订单路由，VWAP/TWAP/冰山算法 | Citadel Securities, Virtu |
| `multi-market-arbitrage.md` | 跨所/跨品种/跨期限套利 | Jump Trading, Tower Research |
| `a-share-t0.md` | A股融券T+0日内回转策略 | 国内量化私募 |
| `crypto-funding-arb.md` | 永续合约资金费率套利，Delta中性对冲 | Alameda, Wintermute |

### 🤖 Polymarket
| 文件 | 核心功能 |
|------|---------|
| `polymarket-signal-hunter.md` | 预测市场错误定价发现 |
| `polymarket-bot.md` | 实盘执行机器人，集成风控引擎 |

### 📐 仓位管理
| 文件 | 核心功能 |
|------|---------|
| `dynamic-position-sizing.md` | 凯利/Kelly/波动率自适应/风险平价仓位 |

## 技术栈

| 领域 | 技术栈 |
|------|--------|
| **数据** | CCXT (交易所统一接口) + Pandas/NumPy/Polars + 多源数据管道 |
| **回测** | Backtrader / vnpy / Qlib / Zipline / 自研事件驱动引擎 |
| **策略** | Pine Script (TradingView) / Python / C++ (HFT) |
| **因子** | Alphalens / pyfolio / Qlib Alpha360 / 自研因子库 |
| **风控** | CVaR / 压力测试 / 集中度 / 杠杆 / 熔断 |
| **执行** | 智能路由 / VWAP / TWAP / Implementation Shortfall |
| **AI/ML** | XGBoost / LightGBM / CatBoost / LSTM / Transformer / 强化学习 |

## 交叉引用

- `skills/risk/` — CVaR守护者、动态仓位管理（风控版）
- `skills/ccxt-python/` — 交易所行情与交易接口
- `skills/hft-quant-expert/` — HFT量化专家 (社区skill)
- `skills/backtesting-trading-strategies/` — 回测框架 (社区skill)
- `skills/generating-trading-signals/` — 多指标信号生成 (社区skill)
- `skills/tracking-crypto-prices/` — 实时行情 (社区skill)
- `skills/trade-prediction-markets/` — Polymarket交易 (社区skill)
- `skills/stock-research-executor/` — 股票投研 (社区skill)
- `skills/stock-analysis/` — 美股技术分析 (社区skill)
- `skills/crypto-report/` — 加密货币市场报告 (社区skill)
- `skills/pine-backtester/` — Pine Script回测 (社区skill)
- `skills/agent-trading-predictor/` — 时序预测agent (社区skill)
