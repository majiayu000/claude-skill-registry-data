---
name: rqdata
description: |
  RiceQuant (米筐) rqdatac Python金融数据库查询工具。通过rqdatac SDK从米筐RQData服务端获取中国金融市场全品种数据。
  覆盖品种：A股(行情/财务/因子/分红/行业)、港股、期货(主力合约/仓单/升贴水)、期权(Greeks/衍生指标)、
  指数与ETF(成分/权重)、公募基金(净值/持仓/经理)、可转债(转股/强赎/衍生指标)、风险因子(暴露度/协方差)、
  现货、货币市场(SHIBOR/国债回购)、宏观经济、另类数据(一致预期/ESG)。
  当用户要求"通过ricequant/米筐/rqdata获取数据"、"查询A股行情"、"获取期货主力合约"、"查基金净值"、
  "获取收益率曲线"、"查转债数据"、"获取SHIBOR"、"rqdatac查询"等金融数据查询任务时触发。
  支持日线/分钟线/tick/周线多频率，支持实时行情推送。
  **重要：直接运行查询并返回数据结果，不仅仅生成代码。自动校验和修正代码格式。**
---

# RQData Python 金融数据查询

## 工作流程

**当用户请求查询数据时，必须按以下步骤执行：**

1. **代码格式校验与修正** - 自动识别并修正合约代码格式
2. **执行查询** - 使用Bash工具运行Python代码获取实际数据
3. **返回结果** - 以结构化格式展示查询结果

**禁止行为：**
- ❌ 仅生成代码而不执行
- ❌ 返回代码片段让用户自己运行
- ❌ 不验证代码格式直接查询

**必须行为：**
- ✅ 自动修正代码格式（如基金代码去除.OF后缀）
- ✅ 运行Python代码获取真实数据
- ✅ 格式化展示查询结果

## 初始化连接

每次使用前必须初始化。使用 license 方式：

```python
import rqdatac

# 主 License（支持分钟数据，有效期30天）
licence = "gEicDQz-O2ni5lVb8G7-j2ccCypIK3sXSQ-vtZP4BxAxr7XF_6zIT27KZgORkFifbY_trFV7LAdqSQPH6V0U-YmUoKWEquE5olX5QMvoZBZ4dOgc9Er17252ezz251rlb3JBVE2ub9G7zqYqzVaykp_BBTDzUnzrDFWNSUlZ9Ng=E_E9MdSRJ6o9lYblVWiV1qM2n2iAShbCL1gdbgORObm2Kt8CQn-N2kBTyEE7UFKXKSFq6phLdfgRQ4_KZuolY7a9cV_C-A3ip8xbGCaCG60BhW3VTCkpI_nRcAtTMH3ArmXVxp0kqLR2L8Vw6EUxmkUJnhwSB0ug4sG9_iVWEyo="

# 备用 License（不支持分钟数据）
# licence = "SXF4jz91bGBpFOPY5BIycxRQHOML4u4k069mhLmeDvlZN6Nv0oqEJ_kGoejOnkaFMTOEQAAaRvu5-Xk4v9Mf8_lnKktX5vJqqaSWsHjU9D1mSi1mxcTL3sqfWgX-vCzIxeCCukipK37UB8OjzyJdoPbAZB6Gn5Pw8iuK7t5HRjU=MOeqFY1Yyo1jYyc-hOqYxN-4uzHkfbcDyzzWQMQj4QDKUZMa5O26rHgk8VnMnFBMlPe0JsfWjKrxwBTvOSXNB9sJNisO3zSd87Otq9-i0OWZFvgnnnMFvFbm9Ird8Tqe6iHMPQf7ddqmqan675ccRyeZ5NmFNQL2WUx4_vH9gQE="

rqdatac.init('license', licence)
```

检查连接状态：`rqdatac.info()`，查看配额：`rqdatac.user.get_quota()`

## 合约代码规则与自动修正

### 标准格式

| 品种 | 格式 | 示例 | 常见错误格式 |
|------|------|------|-------------|
| 沪市股票/ETF/指数 | XXXXXX.XSHG | 600000.XSHG | 600000.SH |
| 深市股票/ETF/指数 | XXXXXX.XSHE | 000001.XSHE | 000001.SZ |
| 港股 | XXXXX.XHKG | 00001.XHKG | 00001.HK |
| **基金** | **XXXXXX (纯数字)** | **090007** | **090007.OF** ❌ |
| 期货 | 品种代码+合约月份 | IF2403, RB2501 | - |
| 期货主力连续 | 品种+88 | IF88 | - |
| 期货指数连续 | 品种+99 | IF99 | - |
| 期权 | 数字代码 | 10000615 | - |
| 可转债(沪) | 11XXXX.XSHG | 113002.XSHG | 113002.SH |
| 可转债(深) | 12XXXX.XSHE | 128052.XSHE | 128052.SZ |
| 现货(上金所) | AUXXXX.SGEX | AU9999.SGEX | - |

### 自动修正规则

查询前必须自动修正代码格式：

```python
# 基金代码修正（最重要！）
'090007.OF' → '090007'  # 去除.OF后缀
'110022.OF' → '110022'  # 去除.OF后缀

# 股票/ETF代码修正
'600000.SH' → '600000.XSHG'
'000001.SZ' → '000001.XSHE'

# 可转债代码修正
'113002.SH' → '113002.XSHG'
'128052.SZ' → '128052.XSHE'
```

**实现方式**：查询前先用 `rqdatac.fund.all_instruments()` 或 `rqdatac.all_instruments()` 验证代码，如果无效则自动修正。

## 日期格式

所有API支持：`20150101`, `"2015-01-01"`, `datetime.date(2015,1,1)`, `pd.Timestamp('20150101')`

## 核心API速查

### 通用行情 (所有品种通用)

```python
# 获取历史行情 (日/分钟/周/tick)
rqdatac.get_price(order_book_ids, start_date, end_date, frequency='1d', fields=None, adjust_type='pre')
# frequency: '1d','1w','1m','5m','15m','30m','60m','tick'
# adjust_type: 'pre'前复权, 'post'后复权, 'none'不复权

# 获取实时快照
rqdatac.current_snapshot(order_book_ids)

# 获取最新分钟线
rqdatac.current_minute(order_book_ids)

# 合约信息
rqdatac.all_instruments(type='CS', date=None)  # 获取所有某类型合约
rqdatac.instruments(order_book_ids)  # 获取合约详情

# 交易日历
rqdatac.get_trading_dates(start_date, end_date)
rqdatac.get_previous_trading_date(date, n=1)
rqdatac.get_next_trading_date(date, n=1)
rqdatac.get_latest_trading_date()

# 收益率曲线 (中债国债)
rqdatac.get_yield_curve(start_date, end_date, tenor=None)
# tenor: '0S','1M','2M','3M','6M','9M','1Y','2Y',...,'30Y','50Y'

# 涨跌幅 / VWAP
rqdatac.get_price_change_rate(order_book_ids, start_date, end_date)
rqdatac.get_vwap(order_book_ids, start_date, end_date, frequency='1d')
```

### 分品种API索引

根据需要查阅对应的详细参考文档：

- **A股**: 财务/因子/分红/行业/融资融券/资金流 -> 见 [references/stock-api.md](references/stock-api.md)
- **港股**: 行情/复权/财务/行业 -> 见 [references/hk-stock-api.md](references/hk-stock-api.md)
- **期货**: 主力合约/仓单/升贴水/交易参数 -> 见 [references/futures-api.md](references/futures-api.md)
- **期权**: Greeks/主力月份/衍生指标 -> 见 [references/options-api.md](references/options-api.md)
- **指数与ETF**: 成分股/权重/估值指标 -> 见 [references/index-etf-api.md](references/index-etf-api.md)
- **基金**: 净值/持仓/份额/经理/分类 -> 见 [references/fund-api.md](references/fund-api.md)
- **可转债**: 转股/强赎/回售/衍生指标 -> 见 [references/convertible-api.md](references/convertible-api.md)
- **风险因子/现货/货币市场/宏观**: -> 见 [references/other-api.md](references/other-api.md)

## 使用注意事项

1. 所有API调用前必须先执行 `rqdatac.init()`
2. 大量获取分钟或tick数据时，建议单只合约+长时段以提高效率
3. 返回数据绝大部分为 pandas DataFrame，可直接 `.to_csv()` 导出
4. 试用账户每日流量限制1G，通过 `rqdatac.user.get_quota()` 查看用量
5. `get_price` 的 `time_slice` 参数是先获取全部数据再切分，注意流量
6. 实时行情推送使用 `LiveMarketDataClient`，支持阻塞和非阻塞模式
