---
name: stock-market-pro-zh
description: >-
  基于 Yahoo Finance (yfinance) 的股票分析技能：实时报价、基本面分析、ASCII 趋势图、高分辨率技术图表（RSI/MACD/BB/VWAP/ATR），以及可选的新闻搜索和期权/资金流向分析。
---

# Stock Market Pro 专业股市分析

**Stock Market Pro** 是一个快速、本地优先的市场研究工具包。
获取清晰的价格和基本面数据，生成可发布的高质量图表（带技术指标面板：RSI/MACD/BB/VWAP/ATR），运行一键报告同时输出摘要和高分辨率 PNG 图表。
可选扩展功能：快速新闻链接搜索（DDG）+ 浏览器优先的期权/资金流向分析（Unusual Whales）。

## 功能特点
- 获取 **实时报价**（价格 + 涨跌幅）
- 汇总 **基本面数据**（市值、前瞻市盈率、每股收益、净资产收益率）
- 打印 **ASCII 趋势图**（终端友好）
- 生成 **高分辨率 PNG 图表**，支持叠加指标面板：
  - RSI / MACD / 布林带 / VWAP / ATR
- 运行 **一键报告**，输出紧凑摘要并生成图表路径
- 通过 DuckDuckGo 搜索 **新闻链接**
- 打开 **期权/资金流向页面**（浏览器优先，Unusual Whales）

---

## 命令（本地）

> 本技能使用 `uv run --script` 处理依赖。
> 如果没有安装 `uv`：从 https://github.com/astral-sh/uv 安装

### 1) 报价查询
```bash
uv run --script scripts/yf.py price TSLA
# 简写形式
uv run --script scripts/yf.py TSLA
```

### 2) 基本面分析
```bash
uv run --script scripts/yf.py fundamentals NVDA
```

### 3) ASCII 趋势图
```bash
uv run --script scripts/yf.py history AAPL 6mo
```

### 4) 专业图表（PNG）
```bash
# K 线图（默认）
uv run --script scripts/yf.py pro 000660.KS 6mo

# 折线图
uv run --script scripts/yf.py pro 000660.KS 6mo line
```

#### 技术指标（可选）
```bash
uv run --script scripts/yf.py pro TSLA 6mo --rsi --macd --bb
uv run --script scripts/yf.py pro TSLA 6mo --vwap --atr
```

- `--rsi` : RSI(14) 相对强弱指标
- `--macd`: MACD(12,26,9) 指数平滑异同移动平均线
- `--bb`  : 布林带(20,2)
- `--vwap`: VWAP 成交量加权平均价（选定范围内的累计值）
- `--atr` : ATR(14) 平均真实波幅

### 5) 一键报告
打印紧凑的文本摘要并生成图表 PNG。

```bash
uv run --script scripts/yf.py report 000660.KS 6mo
# 输出包含: CHART_PATH:/tmp/<...>.png
```

> 可选的网络扩展（新闻/期权）可由智能体工作流附加。

---

## 网络扩展（可选）

### A) 新闻搜索（通过 `ddgs` 使用 DuckDuckGo）
本技能内置辅助脚本（`scripts/ddg_search.py`）。

依赖：
```bash
pip3 install -U ddgs
```

运行：
```bash
python3 scripts/news.py NVDA --max 8
# 或
python3 scripts/ddg_search.py "NVDA 财报 业绩指引" --kind news --max 8 --out md
```

### B) 期权/资金流向（浏览器优先）
Unusual Whales 经常阻止爬虫/无头浏览器访问。
因此推荐的方式是：**在浏览器中打开页面并总结可见内容**。

快速链接辅助：
```bash
python3 scripts/options_links.py NVDA
```

常用 URL：
- `https://unusualwhales.com/stock/{股票代码}/overview`
- `https://unusualwhales.com/live-options-flow?ticker_symbol={股票代码}`
- `https://unusualwhales.com/stock/{股票代码}/options-flow-history`

---

## 子命令（yf.py）
`yf.py` 支持：
- `price` - 价格查询
- `fundamentals` - 基本面
- `history` - 历史走势
- `pro` - 专业图表
- `chart` - 简单图表（别名）
- `report` - 综合报告
- `option` - 期权数据（尽力获取；建议浏览器回退）

查看帮助：
```bash
python3 scripts/yf.py --help
```

## 股票代码示例
- 美股: `AAPL`, `NVDA`, `TSLA`
- 韩股: `005930.KS`, `000660.KS`
- 加密货币: `BTC-USD`, `ETH-KRW`
- 外汇: `USDKRW=X`
