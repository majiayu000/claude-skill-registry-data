---
name: mx-data
description: |
  投资分析数据层——invest-cli 的统一封装。
  不直接调用 API，不管理授权，直接复用 invest-cli 的数据源体系。
  由 invest 系列方法论层调用，不直接面向用户。
triggers:
  - mx-data
---

# mx-data：invest-cli 数据封装层

## 定位

**in-process 封装层**。不直接调用 API，不管理授权，直接复用 invest-cli 的数据源体系。

invest-cli 已经有的数据源、授权、路由、降级逻辑，全部复用。mx-data 只加一层"场景→取数"的映射。

## 统一接口

所有查询通过 `scripts/get_data.py` 入口（in-process 调 `route.fetch`，与 `invest-cli stock/fund/us` 同源同缓存；import 失败才降级 subprocess）：

```bash
# 自然语言查询（自动路由到 invest-cli 命令）
python3 scripts/get_data.py --query "茅台的ROE和毛利率"

# 指定标的和指标
python3 scripts/get_data.py --type stock --code 600519 --metrics ["ROE","PE","revenue"]
```

## 场景→invest-cli 命令映射

| 场景 | 命令 | 说明 |
|---|---|---|
| A 股基本面 | `invest-cli stock <代码>` | 同花顺优先，东财/天天补充 |
| 港股 | `invest-cli stock <代码>` | 东财优先 |
| 美股 | `invest-cli us <代码>` | yfinance 优先，Tiingo/FMP 补充 |
| 基金 | `invest-cli fund <代码>` | 天天基金优先，同花顺/东财补充 |
| 债券 | `invest-cli intent deep bond <代码>` | Wind 优先 |
| 行业 | `invest-cli stock <代码>` + `invest-cli cn report <代码>` | 同花顺+研报 |
| 资讯 | `invest-cli info <查询词>` | argo |
| 宏观 | `invest-cli intent macro` | FRED/argo |

## 与 invest-cli 的关系

- mx-data **不重复造轮子**，直接调用 invest-cli 命令
- invest-cli 管理授权、路由、降级，mx-data 不关心
- mx-data 只负责把"方法论层的需求"翻译成"invest-cli 命令"

## 脚本

| 脚本 | 用途 |
|---|---|
| `scripts/query_router.py` | 场景→invest-cli 命令映射 |
| `scripts/get_data.py` | 统一入口，调用 invest-cli |

## 与 invest 系列的关系

- invest-* 调用 mx-data 获取数据
- mx-data 调用 invest-cli 命令
- invest-cli 管理数据源和授权
