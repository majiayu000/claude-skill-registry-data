---
name: jisu-gold
description: 使用极速数据黄金价格 API，查询上海黄金交易所、上海期货交易所、香港金银业贸易场、银行账户黄金、伦敦金银及金店金价等行情数据。
metadata: { "openclaw": { "emoji": "🥇", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据黄金价格（Jisu Gold）

基于 [黄金价格 API](https://www.jisuapi.com/api/gold/) 的 OpenClaw 技能，支持：

- **上海黄金交易所价格**（`/gold/shgold`）
- **上海期货交易所价格**（`/gold/shfutures`）
- **香港金银业贸易场价格**（`/gold/hkgold`）
- **银行账户黄金价格**（`/gold/bank`）
- **伦敦金、银价格**（`/gold/london`）
- **金店金价**（`/gold/storegold`）

使用技能前需要申请数据，申请地址：https://www.jisuapi.com/api/gold/

## 环境变量配置

```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/gold/gold.py`

## 使用方式

### 1. 上海黄金交易所价格（/gold/shgold）

```bash
python3 skills/gold/gold.py shgold
```

### 2. 上海期货交易所价格（/gold/shfutures）

```bash
python3 skills/gold/gold.py shfutures
```

### 3. 香港金银业贸易场价格（/gold/hkgold）

```bash
python3 skills/gold/gold.py hkgold
```

### 4. 银行账户黄金价格（/gold/bank）

```bash
python3 skills/gold/gold.py bank
```

### 5. 伦敦金、银价格（/gold/london）

```bash
python3 skills/gold/gold.py london
```

### 6. 金店金价（/gold/storegold）

```bash
# 不指定日期：默认当天（仅支持最近 7 天）
python3 skills/gold/gold.py storegold

# 指定日期：
python3 skills/gold/gold.py storegold '{"date":"2023-09-20"}'
```

请求 JSON（仅 `storegold` 支持）：

```json
{
  "date": "2023-09-20"
}
```

## 返回结果示例（节选）

### 上海黄金交易所价格

```json
[
  {
    "type": "Au(T+D)",
    "typename": "黄金延期",
    "price": "238.05",
    "openingprice": "241.00",
    "maxprice": "241.50",
    "minprice": "237.50",
    "changepercent": "-0.90%",
    "lastclosingprice": "240.22",
    "tradeamount": "45998.0000",
    "updatetime": "2015-10-26 15:29:13"
  }
]
```

### 上海期货交易所价格

```json
[
  {
    "type": "AU1512",
    "typename": "黄金1512",
    "price": "238.7",
    "changequantity": "-0.949",
    "buyprice": "238.7",
    "buyamount": "5",
    "sellprice": "238.75",
    "sellamount": "100",
    "tradeamount": "210274",
    "openingprice": "241.5",
    "lastclosingprice": "239.649",
    "maxprice": "241.5",
    "minprice": "237.799",
    "holdamount": "188302",
    "increaseamount": "-6086"
  }
]
```

### 银行账户黄金价格

```json
[
  {
    "typename": "人民币黄金",
    "midprice": "408.92",
    "buyprice": "408.67",
    "sellprice": "409.17",
    "maxprice": "409.16",
    "minprice": "407.58",
    "updatetime": "2020-07-21 12:19:54"
  }
]
```

### 伦敦金、银价格

```json
[
  {
    "type": "伦敦金",
    "price": "1818.6899",
    "changepercent": "+0.05%",
    "changequantity": "+0.9199",
    "openingprice": "1817.95",
    "maxprice": "1820.29",
    "minprice": "1815.8199",
    "lastclosingprice": "1817.77",
    "updatetime": "2020-07-21 12:23:35"
  }
]
```

### 金店金价

```json
{
  "list": [
    {
      "store_name": "周大福",
      "date": "2023-09-20",
      "gold": "612.00",
      "platinum": "387.00",
      "goldbar": "602.00",
      "jewelry": "612.00",
      "solid_gold": null
    }
  ]
}
```

当无数据时，脚本会输出：

```json
{
  "error": "api_error",
  "code": 201,
  "message": "没有信息"
}
```

## 常见错误码

来源于 [极速数据黄金文档](https://www.jisuapi.com/api/gold/)：

| 代号 | 说明     |
|------|----------|
| 201  | 没有信息 |

系统错误码：

| 代号 | 说明                 |
|------|----------------------|
| 101  | APPKEY 为空或不存在  |
| 102  | APPKEY 已过期        |
| 103  | APPKEY 无请求权限    |
| 104  | 请求超过次数限制     |
| 105  | IP 被禁止            |

## 在 OpenClaw 中的推荐用法

1. 用户提问：「现在黄金价格大概是多少？帮我看看上海黄金交易所和金店价格。」  
2. 代理依次调用：  
   - `python3 skills/gold/gold.py shgold`  
   - `python3 skills/gold/gold.py storegold`  
3. 从返回结果中选取常见品种（如 AU9999、黄金延期）以及主流金店（周大福、老凤祥等）的金价，为用户总结当前克价与最近涨跌情况。  

---
name: jisu-gold
description: 使用极速数据黄金价格 API，查询上海黄金交易所、上海期货交易所、香港金银业贸易场、银行账户黄金、伦敦金银及金店金价等行情数据。
metadata: { "openclaw": { "emoji": "🥇", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据黄金价格（Jisu Gold）

基于 [黄金价格 API](https://www.jisuapi.com/api/gold/) 的 OpenClaw 技能，支持：

- **上海黄金交易所价格**（`/gold/shgold`）
- **上海期货交易所价格**（`/gold/shfutures`）
- **香港金银业贸易场价格**（`/gold/hkgold`）
- **银行账户黄金价格**（`/gold/bank`）
- **伦敦金、银价格**（`/gold/london`）
- **金店金价**（`/gold/storegold`）

使用技能前需要申请数据，申请地址：https://www.jisuapi.com/api/gold/

## 环境变量配置

```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/gold/gold.py`

## 使用方式

### 1. 上海黄金交易所价格（/gold/shgold）

```bash
python3 skills/gold/gold.py shgold
```

### 2. 上海期货交易所价格（/gold/shfutures）

```bash
python3 skills/gold/gold.py shfutures
```

### 3. 香港金银业贸易场价格（/gold/hkgold）

```bash
python3 skills/gold/gold.py hkgold
```

### 4. 银行账户黄金价格（/gold/bank）

```bash
python3 skills/gold/gold.py bank
```

### 5. 伦敦金、银价格（/gold/london）

```bash
python3 skills/gold/gold.py london
```

### 6. 金店金价（/gold/storegold）

```bash
# 不指定日期：默认当天（仅支持最近 7 天）
python3 skills/gold/gold.py storegold

# 指定日期：
python3 skills/gold/gold.py storegold '{"date":"2023-09-20"}'
```

请求 JSON（仅 `storegold` 支持）：

```json
{
  "date": "2023-09-20"
}
```

## 返回结果示例（节选）

### 上海黄金交易所价格

```json
[
  {
    "type": "Au(T+D)",
    "typename": "黄金延期",
    "price": "238.05",
    "openingprice": "241.00",
    "maxprice": "241.50",
    "minprice": "237.50",
    "changepercent": "-0.90%",
    "lastclosingprice": "240.22",
    "tradeamount": "45998.0000",
    "updatetime": "2015-10-26 15:29:13"
  }
]
```

### 上海期货交易所价格

```json
[
  {
    "type": "AU1512",
    "typename": "黄金1512",
    "price": "238.7",
    "changequantity": "-0.949",
    "buyprice": "238.7",
    "buyamount": "5",
    "sellprice": "238.75",
    "sellamount": "100",
    "tradeamount": "210274",
    "openingprice": "241.5",
    "lastclosingprice": "239.649",
    "maxprice": "241.5",
    "minprice": "237.799",
    "holdamount": "188302",
    "increaseamount": "-6086"
  }
]
```

### 银行账户黄金价格

```json
[
  {
    "typename": "人民币黄金",
    "midprice": "408.92",
    "buyprice": "408.67",
    "sellprice": "409.17",
    "maxprice": "409.16",
    "minprice": "407.58",
    "updatetime": "2020-07-21 12:19:54"
  }
]
```

### 伦敦金、银价格

```json
[
  {
    "type": "伦敦金",
    "price": "1818.6899",
    "changepercent": "+0.05%",
    "changequantity": "+0.9199",
    "openingprice": "1817.95",
    "maxprice": "1820.29",
    "minprice": "1815.8199",
    "lastclosingprice": "1817.77",
    "updatetime": "2020-07-21 12:23:35"
  }
]
```

### 金店金价

```json
{
  "list": [
    {
      "store_name": "周大福",
      "date": "2023-09-20",
      "gold": "612.00",
      "platinum": "387.00",
      "goldbar": "602.00",
      "jewelry": "612.00",
      "solid_gold": null
    }
  ]
}
```

当无数据时，脚本会输出：

```json
{
  "error": "api_error",
  "code": 201,
  "message": "没有信息"
}
```

## 常见错误码

来源于 [极速数据黄金文档](https://www.jisuapi.com/api/gold/)：

| 代号 | 说明     |
|------|----------|
| 201  | 没有信息 |

系统错误码：

| 代号 | 说明                 |
|------|----------------------|
| 101  | APPKEY 为空或不存在  |
| 102  | APPKEY 已过期        |
| 103  | APPKEY 无请求权限    |
| 104  | 请求超过次数限制     |
| 105  | IP 被禁止            |

## 在 OpenClaw 中的推荐用法

1. 用户提问：「现在黄金价格大概是多少？帮我看看上海黄金交易所和金店价格。」  
2. 代理依次调用：  
   - `python3 skills/gold/gold.py shgold`  
   - `python3 skills/gold/gold.py storegold`  
3. 从返回结果中选取常见品种（如 AU9999、黄金延期）以及主流金店（周大福、老凤祥等）的金价，为用户总结当前克价与最近涨跌情况。  

