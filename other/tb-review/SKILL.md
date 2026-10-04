---
name: tb-review
description: Use when reviewing, debugging, or improving TBQ3/TB language code for trading correctness, Bar strategy behavior, order direction, position state, sizing, costs, backtest realism, event timing, multi-symbol logic, or function documentation consistency.
---

# TBQ3 代码审查

以交易正确性优先审查 TB 代码。不要只检查格式或通用语法；重点找会导致实盘错误、回测失真或信号异常的问题。

## 审查流程

1. 判断代码类型：Bar 策略、事件驱动、Plot、指标公式、账户委托。
2. Bar 策略优先结合 `tb-bar-strategy` 的规则检查。
3. 函数语义不确定时，使用 `tb-doc-index` 查原始文档。
4. 输出 findings 时按严重程度排序，先说风险，再说修复方向。
5. 如果没有发现问题，说明剩余风险，例如未运行 TB 平台验证或函数签名未完全查证。

## 高优先级问题

- 开平仓方向错误：`Buy`、`Sell`、`SellShort`、`BuyToCover` 混用。
- 没有持仓状态限制，导致连续信号重复开仓或反复加仓。
- 同一根 Bar 同时平仓和开仓但没有明确反手规则。
- 止盈止损处理开仓 Bar，造成无法判断价格先后。
- 止盈止损没有处理开盘跳空。
- 固定资金或保证金手数计算可能为 0，或错误使用 `MarginRatio`。
- 回测使用复权/连续价格，实盘下单没有处理真实价格或委托映射。
- 多品种/跨周期代码没有处理数据源索引、对齐或每个品种的交易设置。

## 中优先级问题

- 未设置或未说明初始资金、手续费、滑点、保证金。
- 当前 Bar 条件在实时 Tick 更新时可能产生盘中信号漂移。
- `BarStatus`、`CurrentBar`、`BarsSinceEntry`、`AvgEntryPrice` 等函数使用未查证。
- 参数命名或注释不清楚，导致策略意图难以维护。

## 审查输出

- 先列具体问题和风险。
- 给出最小修复方向或代码片段。
- 引用相关文档路径，尤其是交易函数、止盈止损、运行机制。
- 对不确定项明确写“需要在 TB 文档或平台中确认”，不要伪造确定结论。
