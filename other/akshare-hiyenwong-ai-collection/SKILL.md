---
name: akshare
description: "Access Chinese financial market data via AkShare Python library. Use when user needs to fetch stock market data (A-shares, Hong Kong stocks, US stocks), futures data, fund data, macro economic indicators, bond data, foreign exchange, cryptocurrency, and other financial data from China. Trigger keywords: 股票数据, 期货数据, 基金数据, 宏观经济, 股票行情, 行情查询, 金融数据, A股, 港股, 美股, akshare."
---

# AkShare - Chinese Financial Data Interface

AkShare is an elegant and simple financial data interface library for Python, built for human beings! It provides free access to a wide range of Chinese financial market data.

## Installation

```bash
# General
pip install akshare --upgrade

# China mirrors
pip install akshare -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com --upgrade
```

## Quick Start

```python
import akshare as ak

# Example: Fetch A-share historical data
stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20170301", end_date="20231022", adjust="")
print(stock_zh_a_hist_df)
```

## Data Categories

### Stock Market Data (股票市场数据)

**A-Shares (A股数据)**
- `stock_zh_a_hist()` - A-share historical data (daily)
- `stock_zh_a_hist_em()` - A-share historical data from East Money
- `stock_zh_a_spot()` - Real-time A-share quotes from Sina
- `stock_zh_a_spot_em()` - Real-time A-share quotes from East Money
- `stock_zh_a_minute()` - Intraday minute data
- `stock_zh_a_hist_min_em()` - Minute historical data from East Money
- `stock_zh_ah_spot()` - A+H stock real-time quotes
- `stock_zh_ah_daily()` - A+H stock historical data

**Hong Kong Stocks (港股数据)**
- `stock_hk_spot()` - Hong Kong stock historical data
- `stock_hk_daily()` - Hong Kong stock real-time quotes
- `stock_hk_spot_em()` - Hong Kong stock real-time quotes from East Money
- `stock_hk_hist_min_em()` - Hong Kong stock minute data

**US Stocks (美股数据)**
- `stock_us_daily()` - US stock historical data
- `stock_us_spot()` - US stock quotes
- `get_us_stock_name()` - Get all US stock symbols
- `stock_us_hist_min_em()` - US stock minute data

**Stock Indices (股票指数)**
- `stock_zh_index_daily()` - Stock index historical data
- `stock_zh_index_spot_em()` - Stock index real-time quotes
- `stock_zh_index_daily_em()` - Stock index historical data from East Money

### Futures Data (期货数据)

**Exchange Futures Data**
- `get_cffex_daily()` - CFFEX (China Financial Futures Exchange) daily data
- `get_czce_daily()` - CZCE (Zhengzhou Commodity Exchange) daily data
- `get_dce_daily()` - DCE (Dalian Commodity Exchange) daily data
- `get_shfe_daily()` - SHFE (Shanghai Futures Exchange) daily data
- `get_ine_daily()` - INE (Shanghai International Energy Exchange) daily data
- `get_gfex_daily()` - GFEX (Guangzhou Futures Exchange) daily data

**Futures Quotes**
- `futures_zh_realtime()` - Domestic futures real-time quotes
- `futures_zh_spot()` - Domestic futures spot quotes
- `futures_foreign_realtime()` - Foreign futures real-time quotes
- `futures_foreign_hist()` - Foreign futures historical data
- `futures_hist_em()` - Futures historical data from East Money

**Futures Options**
- `option_hist_dce()` - DCE commodity options data
- `option_hist_czce()` - CZCE commodity options data
- `option_hist_shfe()` - SHFE commodity options data

**Roll Yield**
- `get_roll_yield_bar()` - Futures roll yield data
- `get_roll_yield()` - Roll yield for specific contract

### Fund Data (基金数据)

**Open-end Funds**
- `fund_open_fund_daily_em()` - Open-end fund real-time data
- `fund_open_fund_info_em()` - Open-end fund historical data
- `fund_name_em()` - Fund basic information

**ETF Funds**
- `fund_etf_fund_daily_em()` - ETF real-time data
- `fund_etf_fund_info_em()` - ETF historical data
- `fund_etf_spot_em()` - ETF real-time quotes
- `fund_etf_hist_em()` - ETF historical data

**Fund Rankings**
- `fund_open_fund_rank_em()` - Open-end fund rankings
- `fund_em_exchange_rank()` - Exchange-traded fund rankings

### Macro Economic Data (宏观经济数据)

**China Macro Data**
- `macro_china_gdp_yearly()` - China GDP yearly
- `macro_china_cpi_yearly()` - China CPI yearly
- `macro_china_ppi_yearly()` - China PPI yearly
- `macro_china_pmi_yearly()` - China official manufacturing PMI
- `macro_china_cx_pmi_yearly()` - China Caixin manufacturing PMI
- `macro_china_m2_yearly()` - China M2 money supply
- `macro_china_fx_reserves_yearly()` - China foreign exchange reserves

**US Macro Data**
- `macro_usa_gdp_monthly()` - US GDP
- `macro_usa_cpi_monthly()` - US CPI
- `macro_usa_core_cpi_monthly()` - US Core CPI
- `macro_usa_unemployment_rate()` - US unemployment rate
- `macro_usa_non_farm()` - US non-farm payrolls

**Central Bank Rates**
- `macro_bank_usa_interest_rate()` - Fed interest rate decisions
- `macro_bank_euro_interest_rate()` - ECB interest rate decisions
- `macro_bank_japan_interest_rate()` - Bank of Japan interest rate

### Bond Data (债券数据)

- `bond_zh_hs_daily()` - Bond market historical data
- `bond_zh_hs_spot()` - Bond market real-time quotes
- `bond_zh_hs_cov_daily()` - Convertible bond historical data
- `bond_cb_jsl()` - Convertible bond real-time data from Jisilu

### Foreign Exchange (外汇数据)

- `get_fx_spot_quote()` - RMB foreign exchange spot quotes
- `get_fx_swap_quote()` - RMB foreign exchange forward quotes
- `get_fx_pair_quote()` - Foreign currency pair spot quotes
- `currency_latest()` - Latest currency quotes
- `currency_convert()` - Currency conversion

### Cryptocurrency (加密货币)

- `crypto_js_spot()` - Mainstream cryptocurrency quotes
- `crypto_name_url_table()` - Cryptocurrency names and URLs
- `crypto_bitcoin_hold_report()` - Bitcoin holdings report

### Other Data (其他数据)

**Movie Box Office**
- `movie_boxoffice_realtime()` - Movie real-time box office
- `movie_boxoffice_daily()` - Movie daily box office

**News Data**
- `news_cctv()` - CCTV news transcript
- `stock_news_em()` - Individual stock news

## Common Patterns

### Fetch Stock Historical Data

```python
import akshare as ak

# A-share historical data
df = ak.stock_zh_a_hist(
    symbol="000001",           # Stock code
    period="daily",            # Period: daily, weekly, monthly
    start_date="20240101",     # Start date: YYYYMMDD
    end_date="20241231",       # End date: YYYYMMDD
    adjust=""                   # Adjustment: "" (no adjust), "qfq" (forward), "hfq" (backward)
)
```

### Fetch Real-time Quotes

```python
# A-share real-time quotes
df = ak.stock_zh_a_spot_em()

# Hong Kong stocks real-time
df = ak.stock_hk_spot_em()

# US stocks real-time
df = ak.stock_us_spot(symbol="AAPL")
```

### Fetch Fund Data

```python
# ETF fund list
df = ak.fund_etf_spot_em()

# Fund historical data
df = ak.fund_etf_hist_em(symbol="510050", period="daily", start_date="20240101", end_date="20241231")
```

### Fetch Macro Economic Indicators

```python
# China GDP
df = ak.macro_china_gdp_yearly()

# US CPI
df = ak.macro_usa_cpi_monthly()

# Central bank interest rate
df = ak.macro_bank_usa_interest_rate()
```

## Data Format

All AkShare functions return pandas DataFrame objects with standardized column names:

- Stock data: date, open, close, high, low, volume, amount, etc.
- Index data: date, open, close, high, low, volume, etc.
- Fund data: date, net_value, accumulated_value, etc.
- Macro data: date, value, etc.

## Advanced Features

### Plotting with mplfinance

```python
import akshare as ak
import mplfinance as mpf

# Fetch data
df = ak.stock_us_daily(symbol="AAPL", adjust="qfq")
df = df.set_index(["date"])
df = df["2024-01-01": "2024-01-31"]

# Plot candlestick chart
mpf.plot(df, type="candle", mav=(5, 10, 20), volume=True)
```

### Futures Roll Yield Analysis

```python
# Calculate roll yield for a specific futures contract
df = ak.get_roll_yield_bar(
    type_method="date",  # "date" for date-based, "symbol" for symbol-based
    var="RB",           # Contract symbol (e.g., RB for rebar)
    start_day="20240101",
    end_day="20241231"
)
```

## Important Notes

1. **Data Purpose**: All data provided by AkShare is for academic research only and does not constitute any investment advice.

2. **Rate Limiting**: Some data sources may have rate limiting. If you encounter errors, wait a moment before retrying.

3. **Data Availability**: Not all data interfaces provide historical data. Some only provide real-time or recent data.

4. **Data Quality**: Always validate data from multiple sources before using it for important decisions.

5. **Network Dependencies**: AkShare relies on various data sources. Network issues may affect data fetching.

## When to Use References

For a comprehensive list of all available interfaces and detailed parameter documentation, consult:
- [references/interfaces.md](references/interfaces.md) - Complete interface catalog
- [references/examples.md](references/examples.md) - Code examples for common use cases

## Troubleshooting

**Installation Issues**: Use China mirrors if pip install fails:
```bash
pip install akshare -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com --upgrade
```

**Data Fetching Errors**:
- Check network connectivity
- Verify the data source is available (some sources may be temporarily unavailable)
- Check if the function parameters are correct
- Try reducing the date range for large queries

**Empty Results**:
- Check if the stock symbol exists
- Verify the date format is correct (YYYYMMDD)
- Some stocks may be suspended or delisted



## Activation Keywords
- stock data
- 股票数据
- akshare
- 期货数据
- 基金数据
- 宏观经济
- 行情查询
- A股
- 港股
- 美股

## Tools Used
- exec: Run Python scripts using the akshare library to fetch financial data
- read: Read fetched data files and output results
- write: Save analysis results and fetched data to files

## Instructions for Agents

When a user asks for Chinese financial market data, use the AkShare Python library.

### Step 1: Identify Data Type
Determine which data category the user needs: stock, futures, fund, macro economics, etc.

### Step 2: Select Correct Function
Choose the appropriate AkShare function from the Data Categories section.

### Step 3: Execute Python Code
Run the AkShare function via exec tool to fetch the data.

### Step 4: Present Results
Format and present the data clearly as a table or summary.

## Examples

### Example 1: Fetch A-share Stock Data
```
User: "帮我查询000001平安银行最近30天的股价数据"

Agent:
1. Identify: A-share historical stock data
2. Use ak.stock_zh_a_hist() function
3. Execute Python script to fetch data
4. Present as a table

Agent: "以下是平安银行(000001)近30天的股价数据..."
```
