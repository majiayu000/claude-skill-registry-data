---
name: setup-tradeblazer
description: Use after installing tradeblazer_skills to collect user preferences for TBQ3/TB language work, including task focus, strategy type, document output location, and review expectations.
---

# TradeBlazer Skills 初始化

首次安装后运行本 skill，用几个问题收集用户偏好，并给出后续使用建议。不要修改项目文件，除非用户明确要求保存配置或模板。

## 初始化流程

按顺序询问用户，每次只问一个问题：

1. 主要用途：写策略、审查策略、查函数/语法文档，还是组合使用。
2. 常用任务类型：Bar 策略、事件驱动、指标/Plot、多品种/跨周期、函数查询。
3. 默认输出位置：是否要把策略说明、审查记录或参考文档保存到某个目录。
4. 风控偏好：是否要求默认包含手续费、滑点、保证金、止盈止损、反手规则说明。

## 使用建议

根据用户回答，给出简短配置摘要和下一步建议：

- 写或改 TB 策略：建议使用 `tb-core`，并明确周期、品种、开平仓规则和风控假设。
- 审查 TB 策略：建议使用 `tb-review`，优先检查交易方向、持仓状态、重复发单、回测真实性。
- 查函数或语法：建议使用 `tb-core` 按需检索 `docs/`，不要一次性加载全部文档。

## 输出格式

初始化完成后输出：

```text
TradeBlazer skills 已准备好。

默认用途：...
常用任务：...
默认输出位置：...
风控/审查偏好：...

下一步：把 TB 代码或策略想法发给我，我会从 tb-core 开始处理。
```

## 注意事项

- 对用户没有回答的项目，写“未设置”，不要猜测。
- 如果用户要求保存偏好，先确认目标文件路径。
- 本仓库文档较多，后续处理任务时应使用 `rg` 精确检索相关文档。
