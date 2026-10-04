---
name: qmt
description: QMT迅投量化交易终端 - 内置Python策略开发、回测引擎和实盘交易，支持中国证券市场全品种。
version: 1.2.0
homepage: http://dict.thinktrader.net/freshman/rookie.html
metadata: {"clawdbot":{"emoji":"🖥️","requires":{"bins":["python3"]}}}
---

# QMT（迅投量化交易终端）

[QMT](http://www.thinktrader.net)（Quant Market Trading）是迅投科技开发的专业量化交易平台。提供完整的桌面客户端，内置Python策略开发、回测引擎和实盘交易功能，支持中国证券市场全品种。

> ⚠️ **需要通过券商开通QMT权限**。QMT仅在Windows上运行。可通过国金、华鑫、中泰、东方财富等券商获取。

## 两种运行模式

| 模式 | 说明 |
|---|---|
| **QMT（完整版）** | 完整桌面GUI，内置Python编辑器、图表和回测引擎 |
| **miniQMT** | 极简模式 — 通过外部Python使用xtquant SDK（参见 `miniqmt` skill） |

## 内置Python策略框架

QMT提供事件驱动策略框架，内置Python运行时（类似聚宽/米筐）。

### 策略生命周期

```python
def init(ContextInfo):
    """初始化函数 - 策略启动时调用一次，用于设置股票池和参数"""
    ContextInfo.set_universe(['000001.SZ', '600519.SH'])

def handlebar(ContextInfo):
    """K线处理函数 - 每根K线触发一次（tick/1m/5m/1d等），在此编写交易逻辑"""
    close = ContextInfo.get_market_data(['close'], stock_code='000001.SZ', period='1d', count=20)
    # 在此编写交易逻辑

def stop(ContextInfo):
    """停止函数 - 策略停止时调用"""
    pass
```

### 获取行情数据（内置）

```python
def handlebar(ContextInfo):
    # 获取最近20根K线的收盘价
    data = ContextInfo.get_market_data(
        ['open', 'high', 'low', 'close', 'volume'],
        stock_code='000001.SZ',
        period='1d',
        count=20
    )

    # 获取历史数据
    history = ContextInfo.get_history_data(
        20, '1d', 'close', stock_code='000001.SZ'
    )

    # 获取板块股票列表
    stocks = ContextInfo.get_stock_list_in_sector('沪深A股')

    # 获取财务数据
    fin = ContextInfo.get_financial_data('000001.SZ')
```

### 下单（内置）

```python
def handlebar(ContextInfo):
    # 限价买入100股，价格11.50
    order_shares('000001.SZ', 100, 'fix', 11.50, ContextInfo)

    # 限价卖出100股，价格12.00
    order_shares('000001.SZ', -100, 'fix', 12.00, ContextInfo)

    # 按目标金额买入（10万元）
    order_target_value('000001.SZ', 100000, 'fix', 11.50, ContextInfo)

    # 撤单
    cancel('order_id', ContextInfo)
```

### 查询持仓与账户

```python
def handlebar(ContextInfo):
    # 获取持仓信息
    positions = get_trade_detail_data('your_account', 'stock', 'position')
    for pos in positions:
        print(pos.m_strInstrumentID, pos.m_nVolume, pos.m_dMarketValue)

    # 获取委托信息
    orders = get_trade_detail_data('your_account', 'stock', 'order')

    # 获取账户资产信息
    account = get_trade_detail_data('your_account', 'stock', 'account')
```

## 回测

QMT内置回测引擎：

1. 在内置Python编辑器中编写策略
2. 设置回测参数（日期范围、初始资金、手续费、滑点）
3. 点击"运行回测"
4. 查看结果：资金曲线、最大回撤、夏普比率、交易记录

### 回测参数设置

```python
def init(ContextInfo):
    ContextInfo.capital = 1000000          # 初始资金
    ContextInfo.set_commission(0.0003)     # 手续费率
    ContextInfo.set_slippage(0.01)         # 滑点
    ContextInfo.set_benchmark('000300.SH') # 基准指数
```

## 完整示例：双均线策略

```python
import numpy as np

def init(ContextInfo):
    ContextInfo.stock = '000001.SZ'
    ContextInfo.set_universe([ContextInfo.stock])
    ContextInfo.fast = 5    # 快速均线周期
    ContextInfo.slow = 20   # 慢速均线周期

def handlebar(ContextInfo):
    stock = ContextInfo.stock
    # 获取最近slow+1根K线的收盘价
    closes = ContextInfo.get_history_data(ContextInfo.slow + 1, '1d', 'close', stock_code=stock)

    if len(closes) < ContextInfo.slow:
        return  # 数据不足，跳过

    # 计算当前和前一根K线的快慢均线值
    ma_fast = np.mean(closes[-ContextInfo.fast:])
    ma_slow = np.mean(closes[-ContextInfo.slow:])
    prev_fast = np.mean(closes[-ContextInfo.fast-1:-1])
    prev_slow = np.mean(closes[-ContextInfo.slow-1:-1])

    # 查询当前持仓
    positions = get_trade_detail_data(ContextInfo.accID, 'stock', 'position')
    holding = any(p.m_strInstrumentID == stock and p.m_nVolume > 0 for p in positions)

    # 金叉信号：快速均线上穿慢速均线，买入
    if prev_fast <= prev_slow and ma_fast > ma_slow and not holding:
        order_shares(stock, 1000, 'fix', closes[-1], ContextInfo)

    # 死叉信号：快速均线下穿慢速均线，卖出
    elif prev_fast >= prev_slow and ma_fast < ma_slow and holding:
        order_shares(stock, -1000, 'fix', closes[-1], ContextInfo)
```


## 数据覆盖范围

| 类别 | 内容 |
|---|---|
| **股票** | A股（沪、深、北交所）、港股通 |
| **指数** | 所有主要指数 |
| **期货** | 中金所、上期所、大商所、郑商所、能源中心、广期所 |
| **期权** | ETF期权、股票期权、商品期权 |
| **ETF** | 所有交易所交易基金 |
| **债券** | 可转债、国债 |
| **周期** | Tick、1分钟、5分钟、15分钟、30分钟、1小时、日、周、月 |
| **Level 2** | 逐笔委托、逐笔成交（取决于券商权限） |
| **财务** | 资产负债表、利润表、现金流量表、关键指标 |

## QMT vs miniQMT vs Ptrade 对比

| 特性 | QMT | miniQMT | Ptrade |
|---|---|---|---|
| **厂商** | 迅投科技 | 迅投科技 | 恒生电子 |
| **Python** | 内置（版本受限） | 外部（任意版本） | 内置（版本受限） |
| **界面** | 完整GUI | 极简 | 完整（网页端） |
| **回测** | 内置 | 需自行实现 | 内置 |
| **部署** | 本地 | 本地 | 券商服务器（云端） |
| **外网访问** | 支持 | 支持 | 不支持（仅内网） |

## 使用技巧

- QMT仅在**Windows**上运行。
- 内置Python版本由QMT固定，无法安装任意pip包。
- 如需不受限的Python环境，使用**miniQMT**模式配合`xtquant` SDK。
- 策略文件存储在QMT安装目录中。
- 文档：http://dict.thinktrader.net/freshman/rookie.html
- 也支持VBA接口用于Excel集成。

---

## 进阶示例

### 多股票轮动策略

```python
import numpy as np

def init(ContextInfo):
    # 设置股票池：银行龙头股
    ContextInfo.stock_pool = ['601398.SH', '601939.SH', '601288.SH', '600036.SH', '601166.SH']
    ContextInfo.set_universe(ContextInfo.stock_pool)
    ContextInfo.hold_num = 2  # 最多持有2只股票

def handlebar(ContextInfo):
    # 计算每只股票的20日收益率
    momentum = {}
    for stock in ContextInfo.stock_pool:
        closes = ContextInfo.get_history_data(21, '1d', 'close', stock_code=stock)
        if len(closes) >= 21:
            ret = (closes[-1] - closes[0]) / closes[0]  # 20日收益率
            momentum[stock] = ret

    # 按动量排序，选择前N只股票
    sorted_stocks = sorted(momentum.items(), key=lambda x: x[1], reverse=True)
    target_stocks = [s[0] for s in sorted_stocks[:ContextInfo.hold_num]]

    # 获取当前持仓
    positions = get_trade_detail_data(ContextInfo.accID, 'stock', 'position')
    holding = {p.m_strInstrumentID: p.m_nVolume for p in positions if p.m_nVolume > 0}

    # 卖出不在目标列表中的股票
    for stock, vol in holding.items():
        if stock not in target_stocks:
            closes = ContextInfo.get_history_data(1, '1d', 'close', stock_code=stock)
            if len(closes) > 0:
                order_shares(stock, -vol, 'fix', closes[-1], ContextInfo)

    # 买入目标股票
    account = get_trade_detail_data(ContextInfo.accID, 'stock', 'account')
    if account:
        cash = account[0].m_dAvailable
        per_stock_cash = cash / ContextInfo.hold_num  # 等权分配
        for stock in target_stocks:
            if stock not in holding:
                closes = ContextInfo.get_history_data(1, '1d', 'close', stock_code=stock)
                if len(closes) > 0 and closes[-1] > 0:
                    vol = int(per_stock_cash / closes[-1] / 100) * 100  # 向下取整到整手
                    if vol >= 100:
                        order_shares(stock, vol, 'fix', closes[-1], ContextInfo)
```


### RSI策略

```python
import numpy as np

def init(ContextInfo):
    ContextInfo.stock = '000001.SZ'
    ContextInfo.set_universe([ContextInfo.stock])
    ContextInfo.rsi_period = 14     # RSI周期
    ContextInfo.oversold = 30       # 超卖阈值
    ContextInfo.overbought = 70     # 超买阈值

def handlebar(ContextInfo):
    stock = ContextInfo.stock
    closes = ContextInfo.get_history_data(ContextInfo.rsi_period + 2, '1d', 'close', stock_code=stock)

    if len(closes) < ContextInfo.rsi_period + 1:
        return

    # 计算RSI
    deltas = np.diff(closes)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gains[-ContextInfo.rsi_period:])
    avg_loss = np.mean(losses[-ContextInfo.rsi_period:])

    if avg_loss == 0:
        rsi = 100
    else:
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

    # 查询持仓
    positions = get_trade_detail_data(ContextInfo.accID, 'stock', 'position')
    holding = any(p.m_strInstrumentID == stock and p.m_nVolume > 0 for p in positions)

    # RSI超卖 — 买入
    if rsi < ContextInfo.oversold and not holding:
        order_shares(stock, 1000, 'fix', closes[-1], ContextInfo)

    # RSI超买 — 卖出
    elif rsi > ContextInfo.overbought and holding:
        order_shares(stock, -1000, 'fix', closes[-1], ContextInfo)
```

### 布林带策略

```python
import numpy as np

def init(ContextInfo):
    ContextInfo.stock = '600519.SH'
    ContextInfo.set_universe([ContextInfo.stock])
    ContextInfo.boll_period = 20    # 布林带周期
    ContextInfo.boll_std = 2        # 标准差倍数

def handlebar(ContextInfo):
    stock = ContextInfo.stock
    closes = ContextInfo.get_history_data(ContextInfo.boll_period + 1, '1d', 'close', stock_code=stock)

    if len(closes) < ContextInfo.boll_period:
        return

    # 计算布林带
    recent = closes[-ContextInfo.boll_period:]
    mid = np.mean(recent)                          # 中轨
    std = np.std(recent)                           # 标准差
    upper = mid + ContextInfo.boll_std * std       # 上轨
    lower = mid - ContextInfo.boll_std * std       # 下轨
    price = closes[-1]                             # 当前价格

    positions = get_trade_detail_data(ContextInfo.accID, 'stock', 'position')
    holding = any(p.m_strInstrumentID == stock and p.m_nVolume > 0 for p in positions)

    # 价格触及下轨 — 买入
    if price <= lower and not holding:
        order_shares(stock, 1000, 'fix', price, ContextInfo)

    # 价格触及上轨 — 卖出
    elif price >= upper and holding:
        order_shares(stock, -1000, 'fix', price, ContextInfo)
```

## 定时任务

```python
def init(ContextInfo):
    ContextInfo.stock = '000001.SZ'
    ContextInfo.set_universe([ContextInfo.stock])

def handlebar(ContextInfo):
    import datetime
    now = ContextInfo.get_bar_timetag(ContextInfo.barpos)
    dt = datetime.datetime.fromtimestamp(now / 1000)
    # 仅在每変14:50执行调仓逻辑
    if dt.hour == 14 and dt.minute == 50:
        pass  # 执行调仓
```

## 常见错误处理

| 错误 | 原因 | 解决方法 |
|------|------|----------|
| 账户未登录 | QMT未连接券商 | 检查QMT登录状态，确认券商账户已连接 |
| 委托失败 | 资金不足或超出涨跌停 | 检查可用资金和委托价格 |
| 数据为空 | 股票代码错误或停牌 | 校验代码格式（如`000001.SZ`），检查是否停牌 |
| Python版本不兼容 | 内置Python版本受限 | 改用miniQMT模式 |
| 策略运行缓慢 | 数据量过大 | 减少`get_history_data`的count参数 |

## 内置函数参考

### 行情数据函数

| 函数 | 说明 | 返回值 |
|------|------|--------|
| `ContextInfo.get_market_data(fields, stock_code, period, count)` | 获取K线数据 | dict/DataFrame |
| `ContextInfo.get_history_data(count, period, field, stock_code)` | 获取历史数据序列 | list |
| `ContextInfo.get_stock_list_in_sector(sector)` | 获取板块成分股 | list |
| `ContextInfo.get_financial_data(stock_code)` | 获取财务数据 | dict |
| `ContextInfo.get_instrument_detail(stock_code)` | 获取合约详情 | dict |
| `ContextInfo.get_full_tick(stock_list)` | 获取全推行情快照 | dict |

### 交易函数

| 函数 | 说明 |
|------|------|
| `order_shares(code, volume, style, price, ContextInfo)` | 按股数下单（正买负卖） |
| `order_target_value(code, value, style, price, ContextInfo)` | 按目标市值下单 |
| `order_lots(code, lots, style, price, ContextInfo)` | 按手数下单 |
| `order_percent(code, percent, style, price, ContextInfo)` | 按组合比例下单 |
| `cancel(order_id, ContextInfo)` | 撤单 |
| `get_trade_detail_data(account, market, data_type)` | 查询交易数据 |

### 交易数据类型

| data_type | 说明 | 常用字段 |
|-----------|------|----------|
| `'position'` | 持仓 | `m_strInstrumentID`（代码）, `m_nVolume`（数量）, `m_dMarketValue`（市值） |
| `'order'` | 委托 | `m_strOrderSysID`（委托号）, `m_nVolumeTraded`（成交量）, `m_dLimitPrice`（委托价） |
| `'deal'` | 成交 | `m_strTradeID`（成交号）, `m_dPrice`（成交价）, `m_nVolume`（成交量） |
| `'account'` | 账户 | `m_dAvailable`（可用资金）, `m_dBalance`（总资产）, `m_dMarketValue`（持仓市值） |

## 进阶示例：MACD策略

```python
import numpy as np

def init(ContextInfo):
    ContextInfo.stock = '600519.SH'
    ContextInfo.set_universe([ContextInfo.stock])

def handlebar(ContextInfo):
    stock = ContextInfo.stock
    closes = ContextInfo.get_history_data(60, '1d', 'close', stock_code=stock)
    if len(closes) < 35:
        return
    closes = np.array(closes, dtype=float)

    def ema(data, period):
        result = np.zeros_like(data)
        result[0] = data[0]
        k = 2 / (period + 1)
        for i in range(1, len(data)):
            result[i] = data[i] * k + result[i-1] * (1 - k)
        return result

    ema12 = ema(closes, 12)
    ema26 = ema(closes, 26)
    dif = ema12 - ema26
    dea = ema(dif, 9)

    positions = get_trade_detail_data(ContextInfo.accID, 'stock', 'position')
    holding = any(p.m_strInstrumentID == stock and p.m_nVolume > 0 for p in positions)

    # 金叉：DIF上穿DEA
    if dif[-2] <= dea[-2] and dif[-1] > dea[-1] and not holding:
        order_shares(stock, 1000, 'fix', closes[-1], ContextInfo)
    # 死叉：DIF下穿DEA
    elif dif[-2] >= dea[-2] and dif[-1] < dea[-1] and holding:
        order_shares(stock, -1000, 'fix', closes[-1], ContextInfo)
```

## 进阶示例：止盈止损策略

```python
import numpy as np

def init(ContextInfo):
    ContextInfo.stock = '000001.SZ'
    ContextInfo.set_universe([ContextInfo.stock])
    ContextInfo.entry_price = 0
    ContextInfo.stop_loss = 0.05      # 止损5%
    ContextInfo.take_profit = 0.10    # 止盈10%

def handlebar(ContextInfo):
    stock = ContextInfo.stock
    closes = ContextInfo.get_history_data(21, '1d', 'close', stock_code=stock)
    if len(closes) < 21:
        return
    price = closes[-1]
    ma20 = np.mean(closes[-20:])

    positions = get_trade_detail_data(ContextInfo.accID, 'stock', 'position')
    pos = None
    for p in positions:
        if p.m_strInstrumentID == stock and p.m_nVolume > 0:
            pos = p
            break

    if pos is None:
        if price > ma20:
            order_shares(stock, 1000, 'fix', price, ContextInfo)
            ContextInfo.entry_price = price
    else:
        if ContextInfo.entry_price > 0:
            pnl = (price - ContextInfo.entry_price) / ContextInfo.entry_price
            if pnl <= -ContextInfo.stop_loss:
                order_shares(stock, -pos.m_nVolume, 'fix', price, ContextInfo)
                ContextInfo.entry_price = 0
            elif pnl >= ContextInfo.take_profit:
                order_shares(stock, -pos.m_nVolume, 'fix', price, ContextInfo)
                ContextInfo.entry_price = 0
```

---

---

## 🤖 AI Agent 高阶使用指南

对于 AI Agent，在使用该量化/数据工具时应遵循以下高阶策略和最佳实践，以确保任务的高效完成：

### 1. 数据校验与错误处理
在获取数据或执行操作后，AI 应当主动检查返回的结果格式是否符合预期，以及是否存在缺失值（NaN）或空数据。
* **示例策略**：在通过 API 获取数据框（DataFrame）后，使用 `if df.empty:` 进行校验；捕获 `Exception` 以防网络或接口错误导致进程崩溃。

### 2. 多步组合分析
AI 经常需要进行宏观经济分析或跨市场对比。应善于将当前接口与其他数据源或工具组合使用。
* **示例策略**：先获取板块或指数的宏观数据，再筛选成分股，最后对具体标的进行深入的财务或技术面分析，形成完整的决策链条。

### 3. 构建动态监控与日志
对于交易和策略类任务，AI 可以定期拉取数据并建立监控机制。
* **示例策略**：使用循环或定时任务检查特定标的的异动（如涨跌停、放量），并在发现满足条件的信号时输出结构化日志或触发预警。

---

## 社区与支持

由 **大佬量化** 维护 — 量化交易教学与策略研发团队。

微信客服: **bossquant1** · [Bilibili](https://space.bilibili.com/48693330) · 搜索 **大佬量化** — 微信公众号 / Bilibili / 抖音
