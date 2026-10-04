---
name: tb-bar-strategy
description: Use when generating, modifying, explaining, or reviewing TBQ3 Bar-based trading strategies with OnBar, OnInit, OnReady, entries, exits, MarketPosition, stop profit/loss, sizing, slippage, commission, multi-symbol, or cross-period logic.
---

# TB Bar 策略

使用本 skill 写 TBQ3 Bar 策略。目标是生成能被交易语义约束的 TB 代码，而不是只拼接指标条件。

## 必查时机

- 用户要求写交易策略、开平仓、反手、止盈止损、资金管理、手续费滑点。
- 代码包含 `OnBar`、`Buy`、`Sell`、`SellShort`、`BuyToCover`、`MarketPosition`。
- 用户问“为什么重复开仓/信号太多/回测不对/止损不触发”。

## 生成流程

1. 先确认策略是 Bar 驱动，默认代码结构为 `Params`、`Vars`、`Events`。
2. 初始化交易环境放在 `OnInit` 或 `OnReady`：初始资金、保证金、手续费、滑点、委托偏移、委托映射。
3. 在 `OnBar(ArrayRef<Integer> indexs)` 中计算信号和交易动作。
4. 开仓必须用持仓状态约束，常用 `MarketPosition<>1` 或 `MarketPosition<>-1` 避免连续条件重复发单。
5. 平仓逻辑必须与方向匹配：多仓用 `Sell`，空仓用 `BuyToCover`。
6. 止盈止损默认跳过开仓 Bar：使用 `BarsSinceEntry >= 1`，并处理开盘跳空价格。
7. 若涉及复杂模板，读取 `references/bar-patterns.md`；若涉及失败模式，读取 `references/bar-pitfalls.md`。
8. 函数语义不确定时，使用 `tb-doc-index` 查 `references/function-index.md` 或 `docs/TB语言函数文档` 原文。

## 默认代码骨架

```cpp
Params
    Numeric initCapital(100);
Vars
    Numeric lots(1);
Events
OnInit()
{
    // 设置交易环境
    SetInitCapital(initCapital * 10000);
}

OnBar(ArrayRef<Integer> indexs)
{
    // 计算信号并执行交易
}
```

## 内置审查清单

- 是否有 `MarketPosition` 或等价状态限制，避免信号连续满足时重复开仓。
- 多空两侧是否对称，开仓和平仓函数是否匹配。
- 止盈止损是否使用 `AvgEntryPrice` 或明确入场价，且避免处理开仓 Bar。
- 手数计算是否避免为 0，是否说明固定手数、固定市值或固定保证金。
- 是否设置或说明初始资金、保证金、手续费、滑点。
- 跨周期、多品种、换月复权是否查证专题文档，而不是凭猜测实现。

## 关键文档

- Bar 策略说明：`docs/TB语言编程技巧/236-策略代码说明.md`
- 止盈止损：`docs/TB语言编程技巧/2842-止盈止损.md`
- 加仓减仓：`docs/TB语言编程技巧/2844-加仓减仓.md`
- 平仓延迟反手：`docs/TB语言编程技巧/2847-平仓延迟反手.md`
- 多品种交易：`docs/TB语言编程技巧/2845-多品种交易.md`
- 跨周期：`docs/TB语言编程技巧/2846-跨周期.md`
