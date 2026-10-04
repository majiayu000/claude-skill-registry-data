---
name: tb-core
description: Use when working with TBQ3 or TB language code, including strategy generation, syntax questions, trading functions, Bar strategies, event-driven trading, Plot drawing, examples, or TB-specific code review.
---

# TBQ3 总控入口

本 skill 负责把 TBQ3 任务路由到合适的专家 skill 和本仓库文档。不要把全部文档加载进上下文；先判断任务类型，再按需读取少量 references 或 `docs` 原文。

首次安装本仓库 skills 后，建议先运行 `setup-tradeblazer`，用于设置常用任务类型、默认输出位置和风控/审查偏好。

## 路由规则

- 写或改 Bar 交易策略：先使用 `tb-bar-strategy`，必要时再使用 `tb-syntax` 和 `tb-doc-index`。
- 审查 TB 策略代码：先使用 `tb-review`，涉及 Bar 交易细节时读取 `tb-bar-strategy`。
- 解释 TB 基础语法、类型、变量、参数、控制结构：使用 `tb-syntax`。
- 查函数签名、案例、专题文档：使用 `tb-doc-index`，优先 `rg` 搜索 `docs`。
- 事件驱动、高频、订阅、委托、持仓回报：一期只做文档路由，优先查 `tb-doc-index` 的事件驱动索引。
- Plot、画板、线型、颜色、表格、ICON：一期只做文档路由，使用 `rg "Plot|画板|线型|ICON|颜色|表格" docs`。

## 工作流

1. 判定用户是在生成、修改、解释还是审查 TB 代码。
2. 选择最小专家 skill 集合；不要同时加载无关领域。
3. 对不确定的函数名或运行机制，用 `tb-doc-index` 定位原始文档后再回答。
4. 生成 TB 代码时，优先保证交易语义正确：持仓状态、开平仓方向、重复发单、成本设置、历史/实时差异。
5. 输出时说明关键假设，尤其是周期、品种、是否允许反手、资金手数计算和止盈止损优先级。

## 一期边界

一期重点是 Bar 策略生成和审查。事件驱动、Plot、多品种、跨周期、换月复权可以检索文档并给出保守实现，但复杂任务应先提示需要查证相关专题文档。
