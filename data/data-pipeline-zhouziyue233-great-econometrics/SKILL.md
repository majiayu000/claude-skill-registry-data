---
name: data-pipeline
description: "End-to-end data pipeline for empirical research: fetch economic data from APIs (FRED, World Bank, IMF, BLS, OECD, Yahoo Finance), clean and transform raw data, construct strategy-specific variables, and validate panel structure. Use when asked to fetch data, download data, clean data, merge datasets, prepare analysis-ready data."
---

# Data-Pipeline

## Purpose

本 skill 是一体化数据管道，由 `/data` 命令调用，负责完整的数据工作流：

1. **数据获取**（Part 1）— 从多个 API 自动下载原始数据
2. **数据清洗与转换**（Part 2）— 合并、去重、缺失值处理、异常值检测、变量构建
3. **质量保证**（Part 3）— 验证面板结构、进行质量审计、输出分析就绪的数据集

产出：`data/clean/[project_name]_clean.[dta|parquet|csv]` + `data/clean/cleaning_log.md`

---

## When to Use

- 由 `/data` 命令自动调用（主要场景，分别在 Step 1 和 Step 2 调用）
- 独立触发：用户需要获取 + 清洗数据的完整流程

---

## Part 1: Data Acquisition（数据获取）

### Step 0: API Key Setup Check

**执行任何代码前必须先检查所需 API Key。**

1. 读取 `[plugin_root]/.env` 文件（与 `CLAUDE.md` 同目录，即插件根目录）
2. 检查 `FRED_API_KEY` 和 `BLS_API_KEY`

**若 `FRED_API_KEY` 缺失或为空：**
- 告知用户：*"需要免费的 FRED API Key。请访问 https://fred.stlouisfed.org/docs/api/api_key.html（约 1 分钟）。粘贴 Key 后我会保存。"*
- 等待输入，然后将 `FRED_API_KEY=<value>` 追加到 `.env`

**若 `BLS_API_KEY` 缺失：**
- 告知用户这是可选但可提升速率限制的 Key，地址 https://www.bls.gov/developers/

**若 `.env` 已存在且 Key 已设置：**
- 静默加载，通过 `python-dotenv` 注入所有代码中

```python
from dotenv import load_dotenv
load_dotenv()  # 自动从 CWD 及父目录搜索 .env
```

> **⚠️ `.env` 格式要求：** 标准 `KEY=VALUE` 格式（每行一个），**非 JSON**。若为 JSON 格式，需先转换。

---

### Step 1: 接收调用上下文

**本 skill 由 `/data` 传入结构化上下文，无需重新询问用户。**

接收参数：

| 参数 | 说明 | 示例 |
|------|------|------|
| `target_datasets` | 目标数据集名称列表 | `["FRED宏观", "World Bank"]` |
| `variables` | 变量清单 | `Y=gdp_growth, Z=tariff_rate` |
| `time_range` | 起止年份与频率 | `2000–2023, 年度` |
| `geo_scope` | 地理范围 | `中国31省` / `美国全国` |
| `identification_strategy` | 识别策略 | `DiD` / `RDD` / `IV` / `Panel FE` |
| `output_format` | 输出格式 | `csv`（默认）/ `dta` / `parquet` |

---

### Step 2: 选择合适的数据源

根据传入的数据集名称和地理范围，选择对应 API：

| 数据类型 | 最佳数据源 | 方式 |
|---------|----------|------|
| 美国宏观时间序列 | FRED | `fredapi` |
| 全球发展指标 | World Bank | `wbdata` |
| 美国劳动力市场 | BLS API v2 | `requests`（需分块） |
| 跨国宏观/金融 | IMF WEO | `imf-reader` |
| 金融资产价格 | Yahoo Finance | `yfinance` |

> **无法自动获取的数据源（需用户手动下载）：**
> - **OECD**：数据端点受 Cloudflare 防护，沙箱不可访问。优先用 IMF WEO 替代。
> - **国家统计局（NBS）**：API 限制中国大陆 IP。请前往 https://data.stats.gov.cn 下载后走手动上传流程。

---

### Step 3: 生成并执行获取代码

生成的脚本必须包含：

**① 基础要素**
- API Key 通过环境变量注入（`python-dotenv`），不硬编码
- API 请求失败的错误处理（捕获异常、打印错误信息）
- 系列 ID 的中英文注释说明

**② 输出路径规范**

```python
from datetime import date
filename = f"data/raw/{source_name}_{date.today().strftime('%Y%m%d')}.csv"
df.to_csv(filename, index=False)
```

**③ 写入 `data/raw/data_log.md`**

```python
log_entry = f"""
## {dataset_name} 获取记录
- 获取日期：{date.today()}
- 数据来源：{source_name}
- 原始文件路径：{filename}
- 变量数：{df.shape[1]}，观测数：{df.shape[0]}
- 频率：{frequency}
- 合并键：{merge_key}
"""
os.makedirs("data/raw", exist_ok=True)
with open("data/raw/data_log.md", "a", encoding="utf-8") as f:
    f.write(log_entry)
```

**④ 关键变量验证**

```python
required_vars = [Y_var, D_var, Z_var] + control_vars
available = df.columns.tolist()
found    = [v for v in required_vars if v in available]
missing  = [v for v in required_vars if v not in available]

print("=== 变量到位检查 ===")
for v in found:
    print(f"✅ {v}")
for v in missing:
    print(f"⚠️  {v} — 需在清洗阶段处理")
```

---

## Part 2: Data Cleaning & Transformation（数据清洗与转换）

### Step 0: 接收调用上下文

接收参数（来自 `identification-memo.md`）：

| 参数 | 说明 | 示例 |
|------|------|------|
| `identification_strategy` | 识别策略 | `DiD` / `RDD` / `IV` |
| `Y_var` | 结果变量 | `log_gdp_growth` |
| `D_var` | 处理变量 | `policy_dummy` |
| `Z_var` | 识别变量 | `tariff_rate_1990` |
| `control_vars` | 协变量列表 | `["log_gdp", "population"]` |
| `id_var` | 面板个体标识 | `province_code` |
| `time_var` | 时间变量 | `year` |
| `input_files` | 原始数据文件路径 | `["data/raw/fred_*.csv"]` |
| `merge_plan` | 多源合并方案 | 主文件 + 辅助文件 |

---

### Step 1: 多源数据合并（条件触发）

**触发条件：** `input_files` 包含 ≥2 个文件且 `merge_plan` 已确认

#### 1.1 执行合并

```python
import pandas as pd

df = pd.read_csv("data/raw/[主文件]")
n_before = len(df)

for aux_file, merge_key, how in merge_plan:
    aux = pd.read_csv(f"data/raw/{aux_file}")
    df = df.merge(aux, on=merge_key, how=how, suffixes=("", "_aux"))
    print(f"合并 {aux_file}：{len(df):,} 行（{how} join on {merge_key}）")
```

#### 1.2 合并质量报告

```python
n_after = len(df)
match_rate = n_after / n_before * 100
print(f"匹配率：{match_rate:.1f}%")

dups = df.duplicated(subset=merge_key).sum()
if dups > 0:
    print(f"⚠️  发现 {dups} 行重复")

for v in [Y_var, D_var, Z_var]:
    miss_rate = df[v].isna().mean() * 100
    print(f"{v} 缺失率：{miss_rate:.1f}%")
```

若匹配率低于 70%，需向用户报告并说明原因。

---

### Step 2: 通用清洗流水线

按以下顺序执行，**每步都在 `cleaning_log.md` 中记录样本量和关键指标变化**。

#### 2.1 重复观测检测与处理

```python
dup_mask = df.duplicated(subset=[id_var, time_var], keep=False)
n_dups = dup_mask.sum()
print(f"重复观测：{n_dups} 行")

if n_dups > 0:
    df_dups = df[dup_mask]
    df_dups.to_csv("data/clean/duplicates_removed.csv", index=False)
    df = df.drop_duplicates(subset=[id_var, time_var], keep="first")
```

#### 2.2 缺失值编码识别与处理

```python
MISSING_CODES = [-99, -88, -77, -9, 9999, 99999, -9999]
df.replace(MISSING_CODES, pd.NA, inplace=True)

miss_report = df.isnull().mean().sort_values(ascending=False)
miss_high = miss_report[miss_report > 0.05]

print("缺失率 > 5% 的变量：")
for var, rate in miss_high.items():
    print(f"  {var}: {rate:.1%}")
```

**缺失值处理决策**：

| 情形 | 推荐处理 |
|------|---------|
| Y / D 缺失 | 明确报告，删除；不得插补 |
| Z 缺失 | 明确报告；可能非随机 |
| 协变量 < 5% | 可考虑均值/中位数插补 |
| 协变量 5–20% | 建议多重插补或敏感性分析 |
| 协变量 > 20% | 寻找替代变量 |

#### 2.3 变量类型修正与命名规范化

```python
# 列名统一为 snake_case
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(r"\s+", "_", regex=True)
    .str.replace(r"[^a-z0-9_]", "", regex=True)
)

# 关键变量类型修正
df[time_var] = pd.to_numeric(df[time_var], errors="coerce").astype("Int64")
df[id_var]   = df[id_var].astype(str).str.strip()

for col in numeric_vars:
    df[col] = pd.to_numeric(df[col], errors="coerce")
```

#### 2.4 异常值检测与处理

```python
def winsorize(series, lo=0.01, hi=0.99):
    """将连续变量在 lo/hi 分位数处缩尾"""
    lo_val = series.quantile(lo)
    hi_val = series.quantile(hi)
    return series.clip(lo_val, hi_val)

# 仅对连续型协变量缩尾，不对 Y / D / Z 自动缩尾
for col in continuous_controls:
    n_outliers = ((df[col] < df[col].quantile(0.01)) |
                  (df[col] > df[col].quantile(0.99))).sum()
    print(f"{col}: {n_outliers} 个观测超出 [p1, p99]")
    df[f"{col}_w"] = winsorize(df[col])  # 保留原始变量
```

> ⚠️ **经济学提醒**：Winsorize 需要经济学判断，不是默认必须步骤。

#### 2.5 变量标签（Stata 输出时）

```stata
label variable `Y_var'     "结果变量：[描述]"
label variable `D_var'     "处理变量：[描述]"
label variable `Z_var'     "识别变量：[描述]"
```

---

### Step 3: 识别策略专属变量构建

根据传入的 `identification_strategy`，**自动触发**对应的变量构建模块。

---

#### 策略 A: 双重差分（DiD / Event Study）

```stata
* DiD 核心变量构建
gen treated = (group_var == "treated_group")
gen post = (year >= policy_year)
gen treated_post = treated * post
gen event_time = year - policy_year

* 交错处理时点
bysort id: egen first_treated_year = min(cond(treated_post == 1, year, .))
gen relative_time = year - first_treated_year
```

**Python 版本：**

```python
df["treated"]      = (df["group_var"] == "treated_group").astype(int)
df["post"]         = (df[time_var] >= policy_year).astype(int)
df["treated_post"] = df["treated"] * df["post"]
df["event_time"]   = df[time_var] - policy_year

first_treated = (df[df["treated_post"] == 1]
                 .groupby(id_var)[time_var].min()
                 .rename("first_treated_year"))
df = df.merge(first_treated, on=id_var, how="left")
df["relative_time"] = df[time_var] - df["first_treated_year"]
```

---

#### 策略 B: 断点回归（RDD）

```stata
gen running_centered = running_var - cutoff_value
gen above_cutoff = (running_var >= cutoff_value)
gen running_above = running_centered * above_cutoff
```

**Python 版本：**

```python
df["running_centered"] = df["running_var"] - cutoff_value
df["above_cutoff"]     = (df["running_var"] >= cutoff_value).astype(int)
df["running_above"]    = df["running_centered"] * df["above_cutoff"]

print(f"阈值以上样本：{df['above_cutoff'].sum()}")
```

---

#### 策略 C: 工具变量（IV）

```python
# 范式 1：历史值作工具变量
df["Z_historical"] = df["D_var_baseyear"]

# 范式 2：Bartik 工具
df["Z_bartik"] = (df["industry_share_base"] * df["national_growth"]).groupby(id_var).transform("sum")

# 范式 3：政策 × 时间外生变动
df["Z_policy_interact"] = df["policy_var"] * df["exogenous_shock"]

# 初步检查：Z 与 D 的相关性
corr = df[[Z_var, D_var]].corr().iloc[0, 1]
print(f"Z-D 相关系数：{corr:.3f}")
if abs(corr) < 0.1:
    print("⚠️  相关性较弱，一阶段 F 可能 < 10")
```

---

#### 策略 D: 面板固定效应（Panel FE）

```python
# 唯一标识符验证
assert not df.duplicated(subset=[id_var, time_var]).any()

# 面板平衡性检查
counts = df.groupby(id_var)[time_var].count()
is_balanced = (counts == counts.max()).all()
print(f"面板平衡性：{'强平衡' if is_balanced else '弱平衡'}")

# Within / Between 方差分解
df["Y_mean_i"]    = df.groupby(id_var)[Y_var].transform("mean")
df["Y_within"]    = df[Y_var] - df["Y_mean_i"]
var_within    = df["Y_within"].var()
var_between   = df["Y_mean_i"].var()
print(f"Within 方差占比：{var_within / (var_within + var_between):.1%}")
```

---

#### 策略 E: 合成控制（Synthetic Control）

```python
assert id_var in df.columns and time_var in df.columns

df["is_treated_unit"] = (df[id_var] == treated_unit_id).astype(int)
df["is_donor"]        = (1 - df["is_treated_unit"])
df["pre_treatment"]   = (df[time_var] < treatment_year).astype(int)
df["post_treatment"]  = (df[time_var] >= treatment_year).astype(int)

n_donors = df[df["is_donor"] == 1][id_var].nunique()
T_pre    = df[df["pre_treatment"] == 1][time_var].nunique()
print(f"控制池规模：{n_donors}，预处理期：{T_pre}")

if T_pre < 5:
    print("⚠️  预处理期较短，匹配质量可能受限")
```

---

### Step 4: 面板结构验证（条件触发）

**触发条件：** `identification_strategy` 为 DiD、Panel FE 或 Synthetic Control

```python
print("=== 面板结构验证 ===")
print(f"观测总数：{len(df):,}")
print(f"个体数：{df[id_var].nunique()}")
print(f"时间期数：{df[time_var].nunique()}")
print(f"时间范围：{df[time_var].min()} – {df[time_var].max()}")

obs_per_unit = df.groupby(id_var).size()
print(f"每个体观测数：min={obs_per_unit.min()}, max={obs_per_unit.max()}")

if obs_per_unit.min() == obs_per_unit.max():
    print("✅ 强平衡面板")
else:
    print(f"⚠️  不平衡面板")
```

---

## Part 3: Quality Assurance（质量保证）

### Step 1: 关键变量最终审计

```python
print("\n=== 关键变量最终状态 ===")
audit_vars = [Y_var, D_var, Z_var] + control_vars
for v in audit_vars:
    if v not in df.columns:
        print(f"❌ {v}：不存在！")
        continue
    miss = df[v].isna().mean()
    mean = df[v].mean() if df[v].dtype != object else "N/A"
    std  = df[v].std()  if df[v].dtype != object else "N/A"
    print(f"{'✅' if miss < 0.05 else '⚠️ '} {v}: 缺失={miss:.1%}, 均值={mean:.4g}, 标准差={std:.4g}")
```

---

### Step 2: 保存清洗后数据集

```python
import os
from datetime import date

os.makedirs("data/clean", exist_ok=True)

output_path_parquet = f"data/clean/{project_name}_clean.parquet"
df.to_parquet(output_path_parquet, index=False)
print(f"✅ 已保存：{output_path_parquet}（{len(df):,} 行 × {df.shape[1]} 列）")

# 如需 Stata 格式
try:
    import pyreadstat
    output_path_dta = f"data/clean/{project_name}_clean.dta"
    pyreadstat.write_dta(df, output_path_dta)
    print(f"✅ 已保存：{output_path_dta}")
except ImportError:
    print("（如需 .dta 格式，请安装 pyreadstat）")
```

---

### Step 3: 写入 `cleaning_log.md`

每次清洗完成后自动追加：

```python
log = f"""
## 数据清洗记录 — {project_name}
- 清洗日期：{date.today()}
- 识别策略：{identification_strategy}
- 输入文件：{input_files}
- 输出文件：data/clean/{project_name}_clean.parquet

### 样本量变化
| 步骤 | 操作 | 样本量 |
|------|------|--------|
| 原始数据（合并后） | — | {n_raw:,} |
| 删除重复观测 | ({id_var}, {time_var}) | {n_after_dedup:,} |
| 删除 Y/D 缺失 | 结果/处理变量 | {n_after_ymiss:,} |
| 最终样本 | — | {len(df):,} |

### 关键变量缺失率（清洗后）
| 变量 | 角色 | 缺失率 |
|------|------|--------|
{chr(10).join(f"| {v} | {role} | {df[v].isna().mean():.1%} |" for v, role in zip([Y_var, D_var, Z_var], ["Y", "D", "Z"]))}

### 识别策略专属变量
{chr(10).join(f"- `{v}`：已构建" for v in strategy_vars_built)}

### 数据质量问题记录
{quality_notes}
"""

os.makedirs("data/clean", exist_ok=True)
with open("data/clean/cleaning_log.md", "a", encoding="utf-8") as f:
    f.write(log)
print("✅ 已写入 data/clean/cleaning_log.md")
```

---

## Common Pitfalls

| ❌ 常见错误 | ✅ 正确做法 |
|------------|------------|
| 合并前不检查合并键唯一性 | `assert df[key].is_unique` |
| 对 Y / D 自动 Winsorize | 缩尾前须有经济学判断 |
| 用全局均值填充 Y / D 缺失 | Y/D 应删除，不应插补 |
| DiD 用全局政策年份，忽视交错处理 | 用个体自身 `first_treated_year` |
| 覆盖原始数据 | `data/raw/` 仅读，`data/clean/` 用于保存 |
| 未记录样本量变化 | 每步都在 `cleaning_log.md` 记录 |
| 合并后不检查匹配率 | 低于 70% 需向用户报告 |
| 对 RDD 忘记密度检验 | McCrary 检验在 EDA 阶段执行 |

---

## Requirements

```bash
pip install pandas pyreadstat python-dotenv fredapi wbdata requests yfinance imf-reader
```

## Related Skills & Commands

- **`/data`**：调用本 skill 的上级命令
- **`results-analysis`**：接收本 skill 的输出，生成描述性统计与探索性分析
- **`did-analysis` / `rdd-analysis` / `iv-estimation` / `panel-data`**：应用本 skill 构建的变量
