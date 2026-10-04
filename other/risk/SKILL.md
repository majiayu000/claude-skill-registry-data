---
name: risk-management
description: "风险管理核心skill套件 — CVaR实时风控、动态仓位管理（风控版）。对标Bridgewater全天候策略、PIMCO风控体系的工程化实现。"
---

# 风险管理 Skill Suite

> 烛龙风控中台 — 对标全球顶级资管机构的风险控制体系

## 定位

与 `skills/quant/` 联动，提供所有交易策略在实盘前的风控审查和实盘中的实时风控。

## 目录索引

| 文件 | 核心功能 | 对标机构 |
|------|---------|---------|
| `cvar-guardian.md` | CVaR驱动的实时风控系统，逐笔监控+分级熔断 | Bridgewater, PIMCO |
| `dynamic-position-sizing.md` | 风控视角的仓位分配，集中度/杠杆/相关性限制 | AQR, BlackRock |

## 风控流程图

```
策略信号 → position-sizing审核 → cvar-guardian实时监控 → 预警/熔断/强制平仓
    ↑               ↓                     ↓                    ↓
    └── 归因分析 ←── 动态调仓 ←──── 压力测试循环 ──── 对冲执行
```

## 风控指标体系

| 指标 | 适用场景 | 触发阈值（例） |
|------|---------|--------------|
| VaR (95%/99%) | 组合风险敞口 | 日VaR > 3% 预警 |
| CVaR/Expected Shortfall | 尾部风险 | CVaR > 5% 熔断 |
| 最大回撤 (MDD) | 策略健康度 | MDD > 20% 暂停 |
| Sharpe Ratio | 风险调整收益 | < 0.5 需优化 |
| Calmar Ratio | 回撤收益比 | < 1.0 降仓 |
| 杠杆倍数 | 总敞口控制 | > 3x 自动降杠杆 |
| 集中度 | 单一标的敞口 | > 20% 强制再平衡 |
| 相关性 | 策略间对冲效果 | > 0.7 减少重复敞口 |

## 交叉引用

- `skills/quant/` — 因子挖掘、策略归因、压力测试、仓位管理（量化版）
- `skills/risk-metrics-calculation/` — VaR/CVaR计算 (社区skill)
- `skills/risk-assessment/` — 风险评估 (社区skill)
- `skills/risk-management-playbook/` — 风险管理手册 (社区skill)
- `skills/risk-matrix/` — 风险矩阵 (社区skill)
