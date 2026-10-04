---
name: stock-analysis
description: Comprehensive stock technical analysis system for fetching data, calculating indicators (KDJ, MACD, RSI, BOLL), generating visualizations and reports. Use when user asks about stock analysis, 股票分析, technical analysis, 技术分析, k-line, or stock scoring.
---

# Stock Analysis

## Description
Comprehensive stock technical analysis system that fetches stock data, calculates technical indicators, performs model-based scoring, generates visualizations, and produces Markdown analysis reports. Supports single stock analysis, multi-stock comparison, and technical indicator queries.

## Activation Keywords
- stock analysis
- 股票分析
- technical analysis
- 技术分析
- stock indicators
- stock chart
- k-line
- k线图
- kdj, macd, rsi, boll
- 布林带, 移动平均, 均线
- 股票评分
- stock score
- 股票模型
- stock model
- 趋势分析
- momentum
- 成交量
- 换手率
- 退市风险
- 退市
- delisting risk
- 会不会退市
- 退市风险分析

## Tools Used
- exec: Run Python scripts for data processing and indicator calculation
- read: Read stock data files and configuration
- write: Save analysis reports and generate outputs

## Installation

### Prerequisites
```bash
# Python 3.8+
python3 --version

# Install required packages
pip install akshare pandas numpy matplotlib plotly
```

### Optional Dependencies (Enhanced Features)
```bash
# For faster technical indicators
pip install TA-Lib

# For professional K-line charts
pip install mplfinance

# For machine learning models
pip install scikit-learn
```

### Verify Installation
```bash
python3 -c "import akshare; print('AkShare:', akshare.__version__)"
python3 -c "import pandas; print('Pandas:', pandas.__version__)"
python3 -c "import mplfinance; print('mplfinance installed')"
```

## Usage Patterns

### Single Stock Analysis
```
分析一下贵州茅台 (600519) 最近 60 天的走势，并给出操作建议
```

### Multi-Stock Comparison
```
对比分析 贵州茅台、五粮液、泸州老窖最近 90 天的表现
```

### Technical Indicator Query
```
查看 600519 的 MACD 和 KDJ 当前状态是什么？
```

### Scoring and Recommendation
```
给 600547 山东黄金进行技术评分，并给出买入/持有/卖出建议
```

### Delisting Risk Analysis
```
万科A有没有退市风险?
光明乳业会退市吗?
分析一下600519的退市风险
```

## Instructions for Agents

When user requests stock analysis:

### Step 1: Parse Request
Identify:
- Stock code(s): e.g., "600519" for Guizhou Moutai
- Time period: default 60 days (can be 30/60/90/180)
- Analysis type: single/multi/scoring/indicators
- Specific indicators: if requested

### Step 2: Fetch Data
Use AkShare to fetch stock data:

```python
import akshare as ak

# Fetch daily data
df = ak.stock_zh_a_hist(
    symbol="600519",           # Stock code
    period="daily",            # Daily data
    start_date="20241201",     # YYYYMMDD format
    end_date="20260204",       # YYYYMMDD format
    adjust="qfq"              # Forward-adjusted price
)
```

**⚠️ macOS 系统代理注意:** 如果设置了系统代理（如 127.0.0.1:7890），akshare 会因 macOS 系统代理拦截而失败。见下方「Error Handling > macOS 系统代理阻塞」使用 curl 直连方案。

### Step 3: Calculate Technical Indicators

Use scripts in `scripts/` directory to calculate comprehensive indicators:

**Trend Indicators:**
- MA: Moving Averages (5, 10, 20, 30, 60, 120 days)
- EMA: Exponential Moving Averages
- BOLL: Bollinger Bands (20, 2)
- MACD: (12, 26, 9)
- SAR: Parabolic SAR

**Oscillators:**
- RSI: Relative Strength Index (6, 12, 24 periods)
- KDJ: Stochastic Oscillator (9, 3, 3)
- CCI: Commodity Channel Index (14)
- BIAS: Deviation Rate
- WR: Williams %R

**Volume Indicators:**
- VOL: Volume
- OBV: On-Balance Volume
- VR: Volume Ratio
- EMV: Ease of Movement

**Momentum Indicators:**
- MOM: Momentum
- ROC: Rate of Change
- ARBR: Altitude Ratio
- CR: Capability Ratio

**Custom Indicators:**
- Price Momentum: Price change over N periods
- Volume Momentum: Volume change over N periods
- Composite Score: Weighted combination of indicators

### Step 4: Calculate Model Scores

Use scoring algorithm from `scripts/scoring.py`:

**Score Components:**
1. **Trend Score (40% weight)**
   - MA alignment (bullish/bearish)
   - MACD signal (golden cross/death cross)
   - BOLL position (upper/middle/lower band)
   - Price trend (uptrend/downtrend/sideways)

2. **Momentum Score (30% weight)**
   - RSI level (overbought/oversold)
   - KDJ J-value (momentum strength)
   - MOM trend
   - ROC trend

3. **Money Flow Score (20% weight)**
   - OBV trend (inflow/outflow)
   - Volume change
   - Main fund flow estimation
   - Turnover rate

4. **Sentiment Score (10% weight)**
   - Consecutive up/down days
   - Amplitude (volatility)
   - Recent performance
   - Market sentiment estimate

**Scoring Scale:**
- 90-100: Strong Buy 🟢🟢
- 80-90: Buy 🟢
- 60-80: Hold 🟡
- 40-60: Watch 🟡
- 0-40: Sell 🔴

### Step 5: Generate Visualization

Create charts using `scripts/visualize.py`:

**Chart Types:**
1. **K-line with MA:** Candlestick + moving averages
2. **K-line with BOLL:** Candlestick + Bollinger bands
3. **MACD:** MACD, DIF, DEA, histogram
4. **KDJ:** K, D, J lines
5. **RSI:** RSI with overbought/oversold zones
6. **Volume:** Volume bar chart
7. **Composite:** Multi-panel dashboard

**Save charts to:**
- `assets/charts/` directory
- PNG format for static charts
- Interactive HTML for Plotly (optional)

### Step 6: Generate Report

Create Markdown report using template from `examples/`:

**Report Sections:**
1. Basic Information (stock code, name, date, period)
2. Composite Score Summary
3. Technical Indicator Analysis (by category)
4. Trading Recommendations (short/medium/long term)
5. Risk Warnings
6. Charts (embed images or links)

### Step 7: Output Results

- Save report to workspace: `stock_analysis_<code>_<date>.md`
- Display summary in chat
- Provide chart paths
- Offer further analysis options

## Context Files

The skill uses these context files:

### STOCK_SETTINGS.md
```markdown
# Stock Analysis Settings

## Default Period
60 days

## Indicator Preferences
# Primary indicators to show

## Scoring Weights
trend: 0.4
momentum: 0.3
money_flow: 0.2
sentiment: 0.1

## Chart Style
theme: light
width: 1200
height: 600
```

### STOCK_PREFERENCES.md
```markdown
# User Preferences

## Favorite Stocks
# List frequently analyzed stocks

## Default Output Format
markdown

## Notification Threshold
score: 80  # Alert when score > 80
```

## Technical Indicators Reference

### Complete Indicator List

**Trend Indicators (趋势指标):**
- **MA (Moving Average):** 5, 10, 20, 30, 60, 120日
- **EMA (Exponential MA):** 12, 26日
- **BOLL (Bollinger Bands):** 20日, 2倍标准差
- **MACD (12, 26, 9):** DIF, DEA, MACD柱
- **SAR (Parabolic SAR):** 抛物线转向

**Oscillators (震荡指标):**
- **RSI (Relative Strength Index):** 6, 12, 24日
- **KDJ (9, 3, 3):** K, D, J值
- **CCI (Commodity Channel Index):** 14日
- **BIAS (乖离率):** 6, 12, 24日
- **WR (Williams %R):** 14日
- **OSC (Oscillator):** 10日

**Volume Indicators (量能指标):**
- **VOL (Volume):** 成交量
- **OBV (On-Balance Volume):** 能量潮
- **VR (Volume Ratio):** 成交量比率
- **EMV (Ease of Movement):** 简易波动指标
- **Turnover:** 换手率

**Momentum Indicators (动量指标):**
- **MOM (Momentum):** 动量
- **ROC (Rate of Change):** 变化率
- **ARBR (Altitude Ratio):** 人气意愿指标
- **CR (Capability Ratio):** 能力指标

**Pattern Recognition (形态识别):**
- Golden Cross (金叉): MA上穿
- Death Cross (死叉): MA下穿
- MACD Golden Cross: DIF上穿DEA
- MACD Death Cross: DIF下穿DEA
- BOLL Breakout: 股价突破布林带

## Scripts Usage

### scripts/fetch_data.py
Fetch stock data from AkShare:

```bash
python3 scripts/fetch_data.py --code 600519 --period 60 --adjust qfq
```

### scripts/indicators.py
Calculate all technical indicators:

```bash
python3 scripts/indicators.py --input data.csv --output indicators.csv
```

### scripts/scoring.py
Calculate composite score:

```bash
python3 scripts/scoring.py --input indicators.csv
```

### scripts/visualize.py
Generate charts:

```bash
python3 scripts/visualize.py --input data.csv --charts kline,macd,kdj --output charts/
```

## Report Template

```markdown
# 股票分析报告

## 基本信息
- **股票代码:** 600519
- **股票名称:** 贵州茅台
- **分析日期:** 2026-02-04
- **分析周期:** 近 60 个交易日
- **当前价格:** 1780.50元

## 综合评分

| 维度 | 分数 | 权重 | 状态 | 等级 |
|------|------|------|------|------|
| 趋势 | 85/100 | 40% | 🟢 偏强 | 买入 |
| 动量 | 72/100 | 30% | 🟡 中性 | 观望 |
| 资金面 | 90/100 | 20% | 🟢 流入 | 买入 |
| 情绪 | 65/100 | 10% | 🟡 中性 | 观望 |
| **综合** | **79/100** | **-** | **🟡 持有** | **观望** |

## 技术指标分析

### 趋势指标

#### 移动平均线 (MA)
| MA | 价格 | 趋势 | 信号 |
|----|------|------|------|
| MA5 | 1785.30 | ↑ | 短期偏强 |
| MA10 | 1778.50 | ↑ | 短期偏强 |
| MA20 | 1765.20 | ↑ | 中期偏强 |
| MA60 | 1740.80 | ↑ | 中期偏强 |

**分析:** 呈多头排列，短期均线向上突破长期均线，趋势偏强。

#### MACD (12, 26, 9)
- **DIF:** 12.50
- **DEA:** 10.20
- **MACD:** 2.30
- **信号:** 🟢 金叉

**分析:** DIF上穿DEA形成金叉，偏多头信号。

#### 布林带 (BOLL 20, 2)
- **中轨:** 1768.50
- **上轨:** 1820.30
- **下轨:** 1716.70
- **当前价:** 1780.50
- **位置:** 🟡 接近上轨

**分析:** 股价在中轨和上轨之间，偏强势，但接近上轨需注意回调风险。

### 震荡指标

#### RSI (相对强弱指标)
| RSI6 | RSI12 | RSI24 | 状态 |
|------|-------|-------|------|
| 68 | 62 | 58 | 🟡 中性偏强 |

**分析:** RSI值在50-70之间，属于正常偏强区域，未进入超买。

#### KDJ (9, 3, 3)
- **K值:** 75
- **D值:** 70
- **J值:** 85
- **状态:** 🟢 偏强

**分析:** J值>80，短期动量较强，但需注意超买风险。

### 量能指标

#### 成交量 & 换手率
- **最近5日均量:** 5.2万手
- **今日成交量:** 6.8万手
- **换手率:** 0.68%
- **趋势:** 🟢 放量

**分析:** 今日放量上涨，资金关注度较高。

#### OBV (能量潮)
- **OBV趋势:** 🟢 上升
- **变化:** +120万
- **分析:** 资金持续流入。

## 操作建议

### 短期 (1-5天)
**建议:** 🟡 **观望**
- 技术指标偏强但接近短期高点
- 可等待回调至MA10附近择机介入

### 中期 (5-20天)
**建议:** 🟢 **逢低买入**
- 中期趋势向上
- 支撑位在MA20(1765元)附近
- 可在回调时分批建仓

### 长期 (20天以上)
**建议:** 🟢 **持有可能**
- 中长期趋势完好
- 基本面稳健
- 适合长期持有

## 风险提示

1. ⚠️ 近期涨幅较大，短期面临回调压力
2. ⚠️ RSI和KDJ显示短期超买风险
3. ⚠️ 接近布林带上轨，需注意阻力位
4. ⚠️ 关注成交量变化，缩量上涨需谨慎

## 关键点位
- **支撑位:** 1765元(MA20), 1740元(MA60)
- **阻力位:** 1820元(BOLL上轨), 1850元(前期高点)
- **止损位:** 1740元(MA60)
- **止盈位:** 1850元(前期高点)

## 图表

### K线图 + MA
![K线图](charts/kline_ma_600519.png)

### MACD
![MACD](charts/macd_600519.png)

### KDJ
![KDJ](charts/kdj_600519.png)

### RSI
![RSI](charts/rsi_600519.png)

### 布林带
![布林带](charts/boll_600519.png)

---

*分析生成时间: 2026-02-04 21:30*
*数据来源: AkShare*
```

## Error Handling

### AkShare API Errors
```
If API call fails:
  1. Check network connection
  2. Wait 3 seconds and retry
  3. Try alternative data source if available
  4. Inform user of the issue
```

### ⚠️ macOS 系统代理阻塞 (Common Pitfall)
当 macOS 设置了系统代理（如 127.0.0.1:7890），Python 的 urllib3 会读取系统代理设置，导致 akshare 无法直连东方财富 API，出现 `ProxyError`。

**症状:** `Unable to connect to proxy`, `Remote end closed connection without response`
**根因:** macOS 系统代理 > 环境变量 `http_proxy` — urllib3 从 macOS System Configuration 读取代理，即使取消环境变量也无效。

**解决方案: 使用 `curl --noproxy "*"` 直连东方财富 API**

```python
import subprocess, json

def fetch_quote(code):
    """curl bypass for macOS proxy — fetches real-time quote"""
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    ref = "https://quote.eastmoney.com/"
    url = f"https://push2.eastmoney.com/api/qt/stock/get?secid=0.{code}&fields=f43,f44,f45,f46,f48,f50,f60,f116,f117,f162,f163,f167,f168,f169,f170"
    r = subprocess.run(["curl", "-s", "--noproxy", "*", "-H", f"User-Agent: {ua}", "-H", f"Referer: {ref}", url],
        capture_output=True, text=True, timeout=15)
    d = json.loads(r.stdout).get('data', {}) or {}
    return {
        'price': d.get('f43', 0)/100,
        'change_pct': d.get('f170', 0)/100,
        'change_amt': d.get('f169', 0)/100,
        'high': d.get('f44', 0)/100,
        'low': d.get('f45', 0)/100,
        'open': d.get('f46', 0)/100,
        'pre_close': d.get('f60', 0)/100,
        'volume': d.get('f48', 0),
        'pe': d.get('f162', 0)/100,
        'total_mv': d.get('f116', 0)/1e8,
    }

def fetch_klines(code, start_date, end_date):
    """curl bypass for macOS proxy — fetches K-line data (save to file, no pipe)"""
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    url = f"https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=0.{code}&fields1=f1,f2,f3&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60&klt=101&fqt=1&beg={start_date}&end={end_date}"
    tmp = "/tmp/kline_raw.json"
    subprocess.run(["curl", "-s", "--noproxy", "*", "-H", "User-Agent: Mozilla/5.0", "-H", "Referer: https://quote.eastmoney.com/", url, "-o", tmp], timeout=15)
    with open(tmp) as f:
        data = json.load(f)
    klines = data.get('data', {}).get('klines', [])
    records = []
    for line in klines:
        p = line.split(',')
        records.append({
            'date': p[0], 'open': float(p[1]), 'close': float(p[2]),
            'high': float(p[3]), 'low': float(p[4]),
            'volume': float(p[5]), 'amount': float(p[6]),
            'amplitude': float(p[7]), 'pct': float(p[8]), 'change': float(p[9])
        })
    return records
```

**注意事项:**
- `--noproxy "*"` 必须加，否则 curl 也走代理
- 必须设置 `User-Agent` 请求头，否则 K-line API 返回空
- K-line API 响应不能管道传输到 Python stdin（触发安全扫描），必须 `-o file` 保存
- 实时行情 API (`push2.eastmoney.com`) 和 K-line API (`push2his.eastmoney.com`) 是不同的域名
- 东方财富 API 字段值需要按单位转换：价格/100, PE/100, 成交量=股
- 详细 API 字段参考见 `references/eastmoney-api.md`

### Data Quality Issues
```
If data has missing values:
  1. Fill or interpolate missing data
  2. Verify sufficient data for indicators (need at least 60 days)
  3. Flag questionable data points
  4. Proceed with available data
```

### Indicator Calculation Errors
```
If indicator calculation fails:
  1. Check input data format
  2. Verify required parameters
  3. Use fallback calculation method
  4. Skip problematic indicator and continue
```

## Configuration

### Environment Variables (Optional)
```bash
export AKSHARE_DEFAULT_PERIOD="60"
export AKSHARE_DEFAULT_ADJUST="qfq"
export AKSHARE_CHART_THEME="light"
export AKSAVE_CHARTS="true"
```

### Config File (Optional)
`config.json` in skill directory:
```json
{
  "default_period": 60,
  "default_adjust": "qfq",
  "chart_theme": "light",
  "chart_width": 1200,
  "chart_height": 600,
  "save_charts": true,
  "chart_dir": "assets/charts/"
}
```

## Advanced Features

### Custom Indicator Weights
Users can customize scoring weights:

```python
weights = {
    'trend': 0.5,      # Increase trend weight
    'momentum': 0.3,
    'money_flow': 0.15,  # Decrease money flow weight
    'sentiment': 0.05   # Decrease sentiment weight
}
```

### Multi-Stock Comparison
Compare multiple stocks side-by-side:

```bash
python3 scripts/compare.py --codes 600519,000858,000568 --period 60
```

### Backtesting
Test trading strategies:

```bash
python3 scripts/backtest.py --code 600519 --strategy golden_cross --period 180
```

## Best Practices

1. **Use Adjusted Prices:** Always use forward-adjusted prices (qfq) for accuracy
2. **Validate Data:** Check for anomalies and missing values before analysis
3. **Multiple Timeframes:** Analyze different periods (short/medium/long term)
4. **Combine Indicators:** Don't rely on a single indicator
5. **Context Matters:** Consider market conditions and news
6. **Risk Management:** Always set stop-loss levels

## Examples

### Example 1: Single Stock Analysis
```
User: "分析一下 600547 山东黄金最近 60 天的走势"

Agent Process:
1. Fetch data: Get 600547 data for 60 days
2. Calculate indicators: MA, MACD, KDJ, RSI, BOLL, OBV, etc.
3. Calculate scores: Trend 85, Momentum 72, Money Flow 90, Sentiment 65
4. Generate charts: K-line, MACD, KDJ, RSI, BOLL
5. Create report: Comprehensive Markdown report
6. Output: Display summary and save report

Result:
- Comprehensive score: 79/100 (Hold)
- Short-term: Watch
- Medium-term: Buy on dips
- Long-term: Hold
```

### Example 2: Multi-Stock Comparison
```
User: "对比分析 贵州茅台、五粮液、泸州老窖"

Agent Process:
1. Fetch data for all 3 stocks
2. Calculate indicators and scores for each
3. Generate comparison table
4. Create comparison charts
5. Output comparison report

Result:
| 股票 | 综合评分 | 趋势 | 动量 | 资金 | 建议 |
|------|----------|------|------|------|------|
| 贵州茅台 | 79 | 85 | 72 | 90 | 🟡 观望 |
| 五粮液 | 72 | 78 | 65 | 68 | 🟡 观望 |
| 泸州老窖 | 85 | 88 | 82 | 85 | 🟢 买入 |
```

### Example 3: Indicator Query
```
User: "600519 的 MACD 和 KDJ 是什么状态？"

Agent:
1. Fetch 600519 data
2. Calculate MACD and KDJ
3. Interpret signals
4. Provide concise analysis

Result:
- MACD: DIF(12.50) > DEA(10.20), 金叉信号 🟢
- KDJ: K(75) > D(70), J(85) > 80, 偏强 🟢
- 建议: 短期偏强，但需注意超买风险
```

## Limitations

- Historical data only, no real-time tick data
- Technical analysis doesn't guarantee future performance
- Requires at least 60 days of data for reliable indicators
- Depends on AkShare API availability
- Doesn't include fundamental analysis

## Resources

- **AkShare Docs:** https://akshare.akfamily.xyz/
- **Technical Analysis Guide:** See references/technical-analysis.md
- **Indicator Reference:** See references/indicators-guide.md
- **A股退市风险分析:** See references/delisting-risk-analysis.md — 系统评估面值/市值/财务退市风险
- **EastMoney API Reference:** See references/eastmoney-api.md (proxy bypass, field mappings)

## Related Skills
- **akshare:** Chinese financial data interface
- **coding-agent:** For Python script development
- **obsidian:** For storing analysis reports

## Notes

- All indicators use standard calculation methods
- Back-adjusted prices (qfq) ensure accuracy
- Scoring model is based on widely-used technical analysis principles
- Charts are saved to assets/charts/ directory
- Reports are saved in Markdown format for easy viewing
