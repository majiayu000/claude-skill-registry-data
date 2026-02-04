---
name: stock-data-fetcher
description: 获取A股数据(baostock)并缓存到本地CSV文件，避免MCP返回大量数据占用上下文。触发场景：(1)获取超过100条的K线数据 (2)需要多次查询同一股票数据 (3)需要用grep/awk分析数据 (4)用户提到"保存数据"或"缓存数据"
---

# Stock Data Fetcher

获取A股数据并保存到本地CSV，通过grep/read按需查看，避免上下文膨胀。

## 快速开始

```bash
# 获取K线数据（默认1年，前复权，保存到 ./data/cache）
uv run python .claude/skills/stock-data-fetcher/scripts/fetch_stock_data.py sh.601138

# 获取近2年数据
uv run python .claude/skills/stock-data-fetcher/scripts/fetch_stock_data.py sh.601138 --days 730

# 指定日期范围
uv run python .claude/skills/stock-data-fetcher/scripts/fetch_stock_data.py sh.600000 --start 2024-01-01 --end 2024-12-31

# 获取财务数据
uv run python .claude/skills/stock-data-fetcher/scripts/fetch_stock_data.py sh.601138 --type profit --year 2024 --quarter 3

# 指定缓存目录
uv run python .claude/skills/stock-data-fetcher/scripts/fetch_stock_data.py sh.601138 --cache-dir ./my_data

# 或通过环境变量设置缓存目录
STOCK_CACHE_DIR=./my_data uv run python .claude/skills/stock-data-fetcher/scripts/fetch_stock_data.py sh.601138
```

## 缓存目录

优先级: `--cache-dir` > `STOCK_CACHE_DIR` 环境变量 > `./data/cache`

```
{cache_dir}/
  sh_601138/
    daily_2024-01-01_2024-12-31.csv    # K线
    profit_2024Q3.csv                   # 盈利
    growth_2024Q3.csv                   # 成长
```

## 数据类型

| 类型 | 参数 | 说明 |
|------|------|------|
| kline | `--freq d/w/m` | K线，支持日/周/月/分钟 |
| profit | `--year --quarter` | 盈利能力(ROE/净利率等) |
| growth | `--year --quarter` | 成长能力(YOY增长率) |
| balance | `--year --quarter` | 偿债能力(资产负债率等) |
| cashflow | `--year --quarter` | 现金流 |
| dupont | `--year --quarter` | 杜邦分析 |
| dividend | `--year` | 分红数据 |

## 查看缓存数据

```bash
# 列出所有缓存
uv run python .claude/skills/stock-data-fetcher/scripts/fetch_stock_data.py --list

# 列出指定股票缓存
uv run python .claude/skills/stock-data-fetcher/scripts/fetch_stock_data.py sh.601138 --list

# 查看最近10条
tail -10 data/cache/sh_601138/daily_*.csv

# 搜索特定月份
grep "2024-09" data/cache/sh_601138/daily_*.csv

# 筛选涨幅>5%的日期
awk -F',' 'NR==1 || $13>5' data/cache/sh_601138/daily_*.csv
```

## K线字段

| 字段 | 说明 |
|------|------|
| date | 日期 |
| open/high/low/close | 开高低收 |
| volume | 成交量(股) |
| amount | 成交额(元) |
| turn | 换手率(%) |
| pctChg | 涨跌幅(%) |
| peTTM | 滚动市盈率 |
| pbMRQ | 市净率 |

## 依赖

首次使用需安装: `uv add baostock pandas`
