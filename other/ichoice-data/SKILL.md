---
name: ichoice-data
description: "iChoice/EMQuantAPI 金融市场数据查询工具。通过东方财富Choice量化接口(EMQuantAPI Python SDK)获取中国及全球市场数据，包括：(1)宏观经济数据(GDP/CPI/PMI/社融/M2等)，(2)债券收益率曲线(国债/国开/中票/城投/银行债各期限各评级)，(3)股票指数行情(A股/海外/申万行业)及估值(PE)，(4)资金利率(DR/SHIBOR/IRS)，(5)外汇汇率，(6)商品期货价格，(7)可转债指数，(8)指数成分股，(9)交易日历。当用户需要获取市场数据、宏观数据、利率数据、汇率数据、指数行情、债券收益率、商品价格等金融数据时自动触发。触发关键词：市场数据、宏观数据、债券收益率、利率、汇率、股票行情、指数数据、PMI、GDP、CPI、国债、国开债、信用利差、收益率曲线、SHIBOR、DR007、iChoice、Choice数据、EMQuant。"
---

# iChoice Data Query

通过 EMQuantAPI (Choice量化接口) 获取金融市场数据。

## Environment

- 账号: `xylczh0181` / 密码: `ef465509`
- 指标映射表: `/Users/fanshengxia/Desktop/ichoice_data/ichoice/数据指标.xlsx`

### SDK 路径（按优先级搜索）

| 机器 | 路径 |
|------|------|
| 主机 (fanshengxia) | `/Users/fanshengxia/Desktop/ichoice_data/ichoice/EMQuantAPI_Python/python3` |
| 备用路径 | `~/Desktop/ichoice_data/ichoice/EMQuantAPI_Python/python3` |
| 通用搜索 | 见下方 `setup_emquant()` 自动检测函数 |

### 首次使用新机器：安装 SDK

```bash
# 在 SDK python3 目录下运行一次，创建 .pth 文件使 Python 能找到 EmQuantAPI
cd /path/to/EMQuantAPI_Python/python3
python3 installEmQuantAPI.py
# 成功输出: "Success: EmQuantAPI installed."
```

安装原理：`installEmQuantAPI.py` 在 `site-packages` 下写入 `EmQuantAPI.pth`，内容为 SDK 绝对路径。之后无需手动添加 `sys.path`。

## Critical: Execution Requirements

**iChoice API 登录和数据获取耗时较长，必须遵循以下规则：**

1. **Bash timeout 必须设置 `timeout=300000`（5分钟）或更长**。首次登录需下载配置文件（ChoiceToHQ.xml等），总耗时可达2-3分钟。
2. **将所有逻辑写在单个 Python 脚本中运行**，使用 `python3 << 'EOF' ... EOF` 格式。不要分步调用。
3. **多代码长周期数据分开获取**：对多个证券代码获取长时间序列时（如10年），逐个代码调用 `c.csd()`，避免单次请求过大。
4. **始终使用 `Ispandas=1`** 返回 DataFrame，便于处理。
5. **始终在 finally 块中调用 `c.stop()`** 确保退出。

## Portable Setup Function（跨机器通用）

**每个脚本开头必须调用此函数**，它会自动检测并注册 SDK，在新机器上也能工作：

```python
import sys, os, subprocess

def setup_emquant():
    """自动检测并注册 EmQuantAPI SDK，跨机器可移植。"""
    # 1. 已安装则直接返回
    try:
        import EmQuantAPI
        return True
    except ImportError:
        pass

    # 2. 搜索候选路径
    home = os.path.expanduser("~")
    candidates = [
        # 主机已知路径
        f"{home}/Desktop/ichoice_data/ichoice/EMQuantAPI_Python/python3",
        # 其他常见位置
        f"{home}/Desktop/ichoice/EMQuantAPI_Python/python3",
        f"{home}/ichoice/EMQuantAPI_Python/python3",
        f"{home}/Documents/ichoice/EMQuantAPI_Python/python3",
        f"{home}/Downloads/EMQuantAPI_Python/python3",
    ]
    # 也搜索 Desktop 子目录（深度2）
    desktop = os.path.join(home, "Desktop")
    if os.path.isdir(desktop):
        for d1 in os.listdir(desktop):
            p = os.path.join(desktop, d1, "ichoice", "EMQuantAPI_Python", "python3")
            if os.path.isdir(p):
                candidates.insert(0, p)  # 优先尝试

    sdk_dir = None
    for path in candidates:
        if os.path.isfile(os.path.join(path, "EmQuantAPI.py")):
            sdk_dir = path
            break

    if sdk_dir is None:
        print("ERROR: EmQuantAPI SDK not found. Please place SDK at:")
        print("  ~/Desktop/ichoice_data/ichoice/EMQuantAPI_Python/python3/")
        print("Then run: cd <sdk_dir> && python3 installEmQuantAPI.py")
        return False

    # 3. 注册路径
    if sdk_dir not in sys.path:
        sys.path.insert(0, sdk_dir)

    # 4. 自动安装 .pth（让以后无需 sys.path）
    try:
        pth_installed = any(
            os.path.isfile(os.path.join(p, "EmQuantAPI.pth"))
            for p in sys.path if "site-packages" in p
        )
        if not pth_installed:
            subprocess.run(
                [sys.executable, "installEmQuantAPI.py"],
                cwd=sdk_dir, capture_output=True
            )
            print(f"SDK auto-installed from: {sdk_dir}")
    except Exception:
        pass  # 安装失败不影响本次运行

    return True
```

## Standard Script Template

```python
import sys, os, subprocess
import pandas as pd

# ── 环境初始化（必须在 import EmQuantAPI 之前） ──
def setup_emquant():
    try:
        import EmQuantAPI; return True
    except ImportError:
        pass
    home = os.path.expanduser("~")
    desktop = os.path.join(home, "Desktop")
    candidates = [
        f"{home}/Desktop/ichoice_data/ichoice/EMQuantAPI_Python/python3",
        f"{home}/Desktop/ichoice/EMQuantAPI_Python/python3",
        f"{home}/ichoice/EMQuantAPI_Python/python3",
    ]
    if os.path.isdir(desktop):
        for d in os.listdir(desktop):
            p = os.path.join(desktop, d, "ichoice", "EMQuantAPI_Python", "python3")
            if os.path.isdir(p): candidates.insert(0, p)
    sdk_dir = next((p for p in candidates if os.path.isfile(os.path.join(p, "EmQuantAPI.py"))), None)
    if not sdk_dir:
        print("ERROR: EmQuantAPI SDK not found."); return False
    sys.path.insert(0, sdk_dir)
    try:
        if not any(os.path.isfile(os.path.join(p, "EmQuantAPI.pth")) for p in sys.path if "site-packages" in p):
            subprocess.run([sys.executable, "installEmQuantAPI.py"], cwd=sdk_dir, capture_output=True)
    except Exception: pass
    return True

if not setup_emquant():
    exit(1)

from EmQuantAPI import c

# ── 登录 ──
result = c.start("UserName=xylczh0181,Password=ef465509,ForceLogin=1")
if result.ErrorCode != 0:
    print(f"Login failed: {result.ErrorMsg}"); exit()
print("Login OK")

try:
    # === Fetch data here ===
    data = c.csd("000300.SH", "CLOSE", "2025-01-01", "2025-01-31", "Ispandas=1")
    if isinstance(data, pd.DataFrame):
        print(data)
    else:
        print(f"Error: {data.ErrorCode}, {data.ErrorMsg}")
finally:
    c.stop()
    print("Logout done")
```

## Data Query Patterns

### Pattern 1: EDB (宏观/债券收益率/EDB指标)

用于 EMM/EMG/EMI/E 开头的指标代码。覆盖宏观经济、债券收益率曲线、部分资金利率。

```python
# 单指标
data = c.edb("EMM00087117", "Ispandas=1")

# 多指标+日期范围
data = c.edb("EMM00072301,EMM00073348", "StartDate=2024-01-01,EndDate=2025-01-31,Ispandas=1")

# 仅最新值
data = c.edb("E1000180", "IsLatest=1,Ispandas=1")
```

#### ⚠️ EDB 返回 DataFrame 的格式（必读）

`c.edb(..., "Ispandas=1")` 返回的 DataFrame **不是**以日期为索引，而是以指标代码为索引：

```
              DATES   RESULT
CODES
E1000180  2026/01/04  1.8427   ← 索引是指标码，不是日期！
E1000180  2026/01/05  1.8584
```

**正确的解析方式（必须按此操作，否则报错）：**

```python
data = c.edb("E1000180", "StartDate=2023-01-01,EndDate=2026-02-26,Ispandas=1")
df = data[['DATES', 'RESULT']].copy()
df['DATES'] = pd.to_datetime(df['DATES'], format='%Y/%m/%d')   # 格式固定为 YYYY/MM/DD
df['RESULT'] = pd.to_numeric(df['RESULT'], errors='coerce')     # 必须转 float，否则 idxmax/min 报错
df = df.set_index('DATES').rename(columns={'RESULT': 'value'})
df = df.dropna().sort_index()
```

**常见错误：**
- ❌ `pd.to_datetime(df.index)` → 报错，index 是指标代码字符串
- ❌ `df['RESULT'].idxmax()` 不转 numeric → `TypeError: reduction operation 'argmax' not allowed`
- ❌ `df.columns = ['yield']` → 先要 `data[['DATES','RESULT']]` 提取，不能直接改列名

### Pattern 2: CSD Time Series (行情序列)

用于带交易所后缀的证券代码（.SH/.SZ/.GI/.FX/.IB/.SWI等）。

```python
# 单代码
data = c.csd("000300.SH", "CLOSE", "2025-01-01", "2025-01-31", "Ispandas=1")

# 多代码短周期可以合并
data = c.csd("000300.SH,000905.SH", "CLOSE", "2025-01-01", "2025-01-31", "Ispandas=1")

# 多代码长周期（>1年）：逐个获取，避免超时
for code in ["000300.SH", "000905.SH"]:
    data = c.csd(code, "CLOSE", "2016-01-01", "2026-01-31", "Ispandas=1")
```

常用字段: CLOSE, OPEN, HIGH, LOW, VOLUME, AMOUNT, PETTM

### Pattern 3: CSS Cross-Section (截面数据)

```python
data = c.css("000001.SZ,600519.SH", "CLOSE,VOLUME", "TradeDate=2025-01-20,Ispandas=1")
```

### Pattern 4: Sector Components (指数成分)

```python
data = c.sector("000300.SH", "2025-01-20", "Ispandas=1")
```

### Pattern 5: Trading Calendar

```python
dates = c.tradedates("2025-01-01", "2025-01-31", "")
# dates.Data 返回交易日列表

offset = c.getdate("20250120", -3, "Market=CNSESH")
# 往前推3个交易日
```

### Pattern 6: 债券估值数据 (中债/中证估值)

获取单只债券的估值指标，包括全价、净价、修正久期、收益率等。

```python
# 债券估值字段说明:
# DIRTYCNBD  - 估价全价(中债估值中心)
# NETCNBD    - 估价净价(中债估值中心)
# MODIDURACNBD - 估价修正久期(中债估值中心)
# YIELDCNBD  - 估价收益率(%)(中债估值中心)
# DIRTYCSI   - 估价全价(中证指数有限公司)
# NETCSI     - 估价净价(中证指数有限公司)
# YIELDCSI   - 估价收益率(%)(中证指数有限公司)
# MODIDURACSI - 估价修正久期(中证指数有限公司)

# ⚠️ 重要: CredType=1 是必须的参数，不要添加 Ispandas=1

# 获取单只债券估值
data = c.css("102480862.IB", "MODIDURACNBD,YIELDCNBD", "EndDate=2026-02-12,CredType=1")
# 返回格式: data.Data = {'102480862.IB': [1.0342, 1.7781]}

# 获取多只债券久期和收益率
data = c.css("102480862.IB,102481397.IB", "MODIDURACNBD,YIELDCNBD", "EndDate=2026-02-12,CredType=1")
# 返回格式: data.Data = {'102480862.IB': [1.0342, 1.7781], '102481397.IB': [1.1102, 1.7903]}

# 获取完整估值字段
data = c.css("102480862.IB", "DIRTYCNBD,NETCNBD,MODIDURACNBD,YIELDCNBD", "EndDate=2026-02-12,CredType=1")
```

**重要提示**: 
- `CredType=1` 是必须的参数
- 不要添加 `Ispandas=1` 参数（会导致返回None）
- 返回数据格式: `{债券代码: [字段1值, 字段2值, ...]}`
- 建议使用前一个交易日的日期(EndDate)，当天数据可能尚未更新

## Indicator Code Lookup

| Data Type | Function | Code Format | Example |
|-----------|----------|-------------|---------|
| 宏观经济 | `c.edb()` | EMM/EMG/EMI+number | EMM00087117 (GDP) |
| 债券收益率 | `c.edb()` | E/EMM+number | E1000180 (国债10Y) |
| A股指数行情 | `c.csd()` | code.SH/SZ | 000300.SH (沪深300) |
| 海外指数 | `c.csd()` | code.GI | SPX.GI (标普500) |
| 申万行业 | `c.csd()` | code.SWI | 801780.SWI (银行) |
| 外汇汇率 | `c.csd()` | code.FX/IB | USDCNY.IB |
| 资金利率(市场) | `c.csd()` | code.IB/IR | DR007.IB, Shibor3M.IR |
| 资金利率(EDB) | `c.edb()` | E/EMM+number | E1715081 (7天逆回购) |
| 商品期货 | `c.csd()` | code.SHF/DCE/INE | AU0.SHF (沪金) |
| 商品(EDB) | `c.edb()` | EMI/EMM+number | EMI01618427 (原油) |
| 国债期货 | `c.csd()` | TSM/TFM/TM.CFE | TM.CFE (10Y国债期货) |
| 债券指数 | `c.csd()` | code.CS/CSI/EI | CBA00121.CS |
| 债券估值 | `c.css()` | code.IB/SH/SZ | MODIDURACNBD (久期), YIELDCNBD (收益率) |
| 指数成分 | `c.sector()` | code.SH | 000300.SH |

### Quick Reference: Common Indicators

**宏观:**
- GDP同比: EMM01526652 (现价), EMM00000012 (不变价)
- CPI同比: EMM00072301 | PPI同比: EMM00073348
- PMI: EMM00121996 | 工业增加值同比: EMM00008445
- M2同比: EMM00087086 | 社融当月: EMM00088684
- MLF1年: EMM00650875

**债券收益率(EDB):**
- 国债30Y: E1000183 | 国债10Y: E1000180 | 国债5Y: EMM00166462 | 国债1Y: E1000172
- 国开10Y: E1701714 | 国开5Y: E1701710 | 国开3Y: E1701708
- 中票AAA 3Y: E1000590 | 中票AA+ 3Y: E1000621
- 城投AAA 3Y: E1702579 | 城投AA 3Y: E1702615
- 同业存单AAA 1Y: E1706149
- 二级资本债AAA- 3Y: E1705908

**指数行情(CSD, CLOSE):**
- 沪深300: 000300.SH | 中证500: 000905.SH | 中证1000: 000852.SH
- 上证50: 000016.SH | 创业板指: 399006.SZ | 万得全A: 800000.EI
- 标普500: SPX.GI | 纳斯达克: IXIC.GI | 日经225: N225.GI

**资金利率(CSD, CLOSE):**
- DR001: DR001.IB | DR007: DR007.IB
- SHIBOR3M: Shibor3M.IR | FR007 IRS 1Y: FR007_1Y.IB

**外汇(CSD, CLOSE):**
- 美元指数: USDX.FX | 美元兑人民币: USDCNY.IB | 离岸人民币: USDCNH.FX

**商品(CSD, CLOSE):**
- 沪金: AU0.SHF | 原油: scm.INE | 螺纹钢: RB0.SHF | 豆粕: M0.DCE

**⚠️ 查询指标代码的首选方式：先读取 `references/indicator_codes.md`**

使用规则：
- 遇到任何债券收益率（国债/国开/城投/信用债）、利率、宏观指标代码需求时，**必须先 Read `references/indicator_codes.md`** 获取准确代码，禁止凭记忆猜测
- Quick Reference 仅为常用指标的便捷索引，不代表全量指标

**For full 453 indicator code mappings:** Read [references/indicator_codes.md](references/indicator_codes.md)

**For complete API function reference:** Read [references/api_reference.md](references/api_reference.md)

## Chart Generation Notes

生成中文图表时设置字体：
```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti TC', 'STHeiti']
plt.rcParams['axes.unicode_minus'] = False
```

## Key Notes

- Wind `.SI` → Choice `.SWI` (申万行业)
- Wind `881001.WI` (万得全A) → Choice `800000.EI`
- 部分指标无Choice对应码：南华指数, USDCNYM.IB, 螺纹钢期货Wind码
- `Ispandas=1` 返回 DataFrame，否则返回 EmQuantData 对象
- Rate limits: css/csd 700次/分钟, edb 单次最多100个指标
- 务必在脚本结束时调用 `c.stop()` 释放连接

### DataFrame 列格式速查

| 函数 | 索引 | 列名 | DATES 格式 | 数值列 |
|------|------|------|-----------|--------|
| `c.edb()` | 指标代码（如 E1000180） | `DATES`, `RESULT` | `"YYYY/MM/DD"` 字符串 | `RESULT`（需 `pd.to_numeric()`） |
| `c.csd()` | 证券代码（如 000300.SH） | `DATES`, `CLOSE` 等 | `"YYYY/MM/DD"` 字符串 | 直接可用 |

两者的 `DATES` 列都是字符串，统一用：
```python
df['DATES'] = pd.to_datetime(df['DATES'], format='%Y/%m/%d')
```

`edb()` 的 `RESULT` 列必须转 numeric 才能做数值运算：
```python
df['RESULT'] = pd.to_numeric(df['RESULT'], errors='coerce')
```

### 环境问题排查

| 错误 | 原因 | 解决 |
|------|------|------|
| `ModuleNotFoundError: EmQuantAPI` | SDK 未注册 | 运行 `installEmQuantAPI.py` 或用 `setup_emquant()` |
| `OSError: dlopen ... no such file` | `.pth` 指向旧路径 | 重新运行 `installEmQuantAPI.py` |
| `DateParseError: E1000180` | 对 `edb` 结果错误使用 `pd.to_datetime(df.index)` | 改用 `pd.to_datetime(df['DATES'])` |
| `TypeError: argmax not allowed` | `RESULT` 列未转 numeric | 加 `pd.to_numeric(df['RESULT'])` |
