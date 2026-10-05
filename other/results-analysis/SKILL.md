---
name: results-analysis
description: "Comprehensive results analysis for empirical research: generate publication-quality descriptive statistics and balance tables, interpret regression coefficients with economic magnitude and effect sizes, assess identification assumption diagnostics, and produce structured results memos. Use when asked to create summary statistics, Table 1, balance tests, interpret results, assess economic significance, or write results narratives."
---

# Results-Analysis

## Purpose

本 skill 是一体化结果分析工具，支持从原始数据探索（EDA）到回归结果解读的完整流程：

1. **描述性统计与 EDA**（Part 1）— 生成 Table 1、Table 2、诊断图、缺失值报告
2. **结果解读与经济学意义**（Part 2）— 系数量级换算、效应量计算、文献对比、识别可信度评估
3. **输出生成**（Part 3）— `results-memo.md` 和所有表格的 .tex/.csv 双格式输出

---

## When to Use

- Phase 4 EDA 阶段（由 `/data` Step 3 调用）
- Phase 7 结果解读（由 `/code` Phase 6 执行完成后调用）
- 独立触发：用户持有数据或回归结果，需要快速生成统计表或结果解读

---

## Part 1: Descriptive Statistics & EDA（描述统计与探索性分析）

### Step 0: 环境初始化

**本 skill 通常由 `/data` 或 `/code` 传入结构化上下文。**

接收参数：

| 参数 | 说明 | 示例 |
|------|------|------|
| `clean_data_path` | 清洗后数据路径 | `data/clean/china_trade_*.parquet` |
| `identification_strategy` | 识别策略 | `DiD` / `RDD` / `IV` / `Panel FE` |
| `Y_var` | 结果变量 | `log_gdp_growth` |
| `D_var` | 处理变量 | `policy_dummy` |
| `Z_var` | 识别变量（如适用） | `tariff_rate_1990` |
| `control_vars` | 协变量列表 | `["log_gdp", "population"]` |
| `id_var` | 面板个体标识 | `province_code` |
| `time_var` | 时间变量 | `year` |
| `treatment_timing` | 政策实施时点（DiD 用） | `2003` |
| `cutoff_value` | 断点阈值（RDD 用） | `50.0` |

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

os.makedirs("tables",  exist_ok=True)
os.makedirs("figures", exist_ok=True)

mpl.rcParams.update({
    "figure.dpi": 300,
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
})

df = pd.read_parquet(clean_data_path)
print(f"样本：{len(df):,} 行 × {df.shape[1]} 列")
```

---

### Step 1: Table 1 — 描述性统计

生成全样本描述性统计，**双格式输出**（`.tex` 用于论文，`.csv` 用于核查）。

```python
# ─────────────────────────────────────────────
# Table 1 — 描述性统计
# ─────────────────────────────────────────────
analysis_vars = [Y_var, D_var] + ([Z_var] if Z_var else []) + control_vars
analysis_vars = [v for v in analysis_vars if v in df.columns]

stats_dict = {}
for v in analysis_vars:
    s = df[v].dropna()
    stats_dict[v] = {
        "N":      len(s),
        "Mean":   s.mean(),
        "SD":     s.std(),
        "P25":    s.quantile(0.25),
        "Median": s.median(),
        "P75":    s.quantile(0.75),
        "Min":    s.min(),
        "Max":    s.max(),
    }

table1 = pd.DataFrame(stats_dict).T.round(3)
table1.to_csv("tables/table1_descriptive.csv")
print("✅ Table 1 数据已保存（.csv）")
# LaTeX 格式化由 `table` skill 统一负责（在 /plot 阶段调用）
```

---

### Step 2: Table 2 — 平衡性检验

**触发条件：** 存在处理变量 `D_var`

**关键原则：平衡性检验必须限定在预处理期样本上，不得使用全样本。**

```python
# ─────────────────────────────────────────────
# Table 2 — 处理组/控制组平衡性检验
# ─────────────────────────────────────────────
from scipy import stats as scipy_stats

# 筛选预处理期样本
if treatment_timing:
    df_pre = df[df[time_var] < treatment_timing].copy()
    print(f"预处理期样本：{len(df_pre):,} 行")
else:
    df_pre = df.copy()

treated_group  = df_pre[df_pre[D_var] == 1]
control_group  = df_pre[df_pre[D_var] == 0]

balance_rows = {}
for v in control_vars:
    if v not in df_pre.columns:
        continue
    t_vals = treated_group[v].dropna()
    c_vals = control_group[v].dropna()

    mean_t = t_vals.mean()
    mean_c = c_vals.mean()
    diff   = mean_t - mean_c
    t_stat, p_val = scipy_stats.ttest_ind(t_vals, c_vals, equal_var=False)
    norm_diff = diff / np.sqrt((t_vals.var() + c_vals.var()))

    balance_rows[v] = {
        "Treatment Mean": round(mean_t, 3),
        "Control Mean":   round(mean_c, 3),
        "Difference":     round(diff, 3),
        "t-stat":         round(t_stat, 2),
        "p-value":        round(p_val, 3),
        "Norm. Diff.":    round(norm_diff, 3),
        "Balanced":       "✅" if abs(norm_diff) < 0.25 else "⚠️",
    }

table2 = pd.DataFrame(balance_rows).T
table2.to_csv("tables/table2_balance.csv")
print("✅ Table 2 数据已保存（.csv）")
# LaTeX 格式化由 `table` skill 统一负责（在 /plot 阶段调用）

unbalanced = table2[table2["Balanced"] == "⚠️"].index.tolist()
if unbalanced:
    print(f"⚠️  标准化差异 > 0.25 的变量：{unbalanced}")
```

---

### Step 3: 识别变量分布诊断图

根据 `identification_strategy`，**自动触发**对应的诊断图。

#### 策略 A: DiD — 处理组 vs 控制组年均趋势

```python
# ─────────────────────────────────────────────
# DiD：预处理期平行趋势目测
# ─────────────────────────────────────────────
trend = (df.groupby([time_var, D_var])[Y_var]
           .mean()
           .reset_index()
           .rename(columns={D_var: "group"}))

fig, ax = plt.subplots(figsize=(8, 4.5))

for g, label, color, ls in [(1, "Treatment", "#C0392B", "-"),
                              (0, "Control",   "#2C3E50", "--")]:
    sub = trend[trend["group"] == g]
    ax.plot(sub[time_var], sub[Y_var], color=color, ls=ls,
            lw=2, marker="o", ms=4, label=label)

if treatment_timing:
    ax.axvline(treatment_timing, color="gray", ls=":", lw=1.5,
               label=f"Policy ({treatment_timing})")

ax.set_xlabel("Year")
ax.set_ylabel(f"Mean {Y_var}")
ax.set_title("Treatment vs Control: Pre-treatment Trend")
ax.legend()
plt.tight_layout()
plt.savefig("figures/eda_did_trend.png", dpi=300)
plt.close()

# 预处理期趋势斜率对比
pre = df[df[time_var] < treatment_timing] if treatment_timing else df
for g, label in [(1, "Treatment"), (0, "Control")]:
    sub = pre[pre[D_var] == g].groupby(time_var)[Y_var].mean()
    if len(sub) >= 2:
        slope = np.polyfit(sub.index, sub.values, 1)[0]
        print(f"  {label}：年均趋势斜率 = {slope:.4f}")
```

#### 策略 B: RDD — 分配变量分布 + 阈值附近散点图

```python
# ─────────────────────────────────────────────
# RDD：分配变量分布 + 阈值附近密度目测
# ─────────────────────────────────────────────
running_centered = df["running_centered"]

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

bandwidth_plot = running_centered.std() * 3
mask = running_centered.abs() <= bandwidth_plot

# 左图：直方图
ax = axes[0]
ax.hist(running_centered[mask & (running_centered < 0)],
        bins=30, color="#2C3E50", alpha=0.7, label="Below cutoff")
ax.hist(running_centered[mask & (running_centered >= 0)],
        bins=30, color="#C0392B", alpha=0.7, label="Above cutoff")
ax.axvline(0, color="black", lw=1.5, ls="--")
ax.set_xlabel("Running Variable (centered)")
ax.set_ylabel("Frequency")
ax.set_title("Distribution of Running Variable")
ax.legend()

# 右图：Y 关于分配变量的散点 + 分段拟合
ax = axes[1]
x = running_centered[mask]
y = df.loc[mask, Y_var]
ax.scatter(x, y, alpha=0.2, s=8, color="steelblue")

for side_mask, color in [(x < 0, "#2C3E50"), (x >= 0, "#C0392B")]:
    if side_mask.sum() > 5:
        coef = np.polyfit(x[side_mask], y[side_mask], 1)
        x_line = np.linspace(x[side_mask].min(), x[side_mask].max(), 100)
        ax.plot(x_line, np.polyval(coef, x_line), color=color, lw=2)
ax.axvline(0, color="black", lw=1.5, ls="--")
ax.set_xlabel("Running Variable (centered)")
ax.set_ylabel(Y_var)
ax.set_title(f"Y vs Running Variable Near Cutoff")

plt.suptitle("RDD Diagnostic Plots", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("figures/eda_rdd.png", dpi=300)
plt.close()

n_above = (df["above_cutoff"] == 1).sum()
n_below = (df["above_cutoff"] == 0).sum()
print(f"阈值以上：{n_above}，以下：{n_below}（比值 {n_above/n_below:.2f}）")
```

#### 策略 C: IV — 工具变量与处理变量相关性

```python
# ─────────────────────────────────────────────
# IV：Z 与 D 的散点图 + 一阶段初步检验
# ─────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

ax = axes[0]
ax.scatter(df[Z_var], df[D_var], alpha=0.3, s=10, color="steelblue")
coef = np.polyfit(df[Z_var].dropna(), df[D_var].dropna(), 1)
x_line = np.linspace(df[Z_var].min(), df[Z_var].max(), 100)
ax.plot(x_line, np.polyval(coef, x_line), color="#C0392B", lw=2)
ax.set_xlabel(f"Instrument: {Z_var}")
ax.set_ylabel(f"Treatment: {D_var}")
ax.set_title("First Stage: Z vs D")

corr = df[[Z_var, D_var]].corr().iloc[0, 1]
ax.text(0.05, 0.92, f"ρ = {corr:.3f}", transform=ax.transAxes,
        fontsize=11, color="#C0392B")

ax = axes[1]
ax.scatter(df[Z_var], df[Y_var], alpha=0.3, s=10, color="#2C3E50")
corr_zy = df[[Z_var, Y_var]].corr().iloc[0, 1]
ax.set_xlabel(f"Instrument: {Z_var}")
ax.set_ylabel(f"Outcome: {Y_var}")
ax.set_title("Reduced Form: Z vs Y")
ax.text(0.05, 0.92, f"ρ = {corr_zy:.3f}", transform=ax.transAxes,
        fontsize=11, color="#2C3E50")

plt.suptitle("IV Diagnostic Plots", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("figures/eda_iv.png", dpi=300)
plt.close()

if abs(corr) < 0.1:
    print(f"⚠️  Z-D 相关系数仅 {corr:.3f}，一阶段 F < 10 风险")
```

#### 策略 D: Panel FE — Within / Between 方差分解

```python
# ─────────────────────────────────────────────
# Panel FE：方差分解
# ─────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

for ax, var, title in [(axes[0], Y_var, "Outcome Y"),
                        (axes[1], D_var, "Treatment D")]:
    unit_means = df.groupby(id_var)[var].mean()
    df_temp = df.copy()
    df_temp["unit_mean"] = df_temp.groupby(id_var)[var].transform("mean")
    df_temp["within"]    = df_temp[var] - df_temp["unit_mean"]

    var_between = unit_means.var()
    var_within  = df_temp["within"].var()
    total       = var_between + var_within

    bars = ax.bar(["Between", "Within"],
                  [var_between / total * 100, var_within / total * 100],
                  color=["#2C3E50", "#C0392B"], alpha=0.8, width=0.5)
    ax.bar_label(bars, fmt="%.1f%%", padding=3)
    ax.set_ylabel("Share of Total Variance (%)")
    ax.set_title(f"Variance Decomposition: {title}")
    ax.set_ylim(0, 110)

    if var_within / total < 0.1:
        ax.text(0.5, 0.6, "⚠️ Low within\nFE weak",
                transform=ax.transAxes, ha="center", color="#C0392B", fontsize=9)

plt.suptitle(f"Panel FE: Within vs Between Variance", fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig("figures/eda_panel_fe.png", dpi=300)
plt.close()
```

---

### Step 4: 缺失值报告

```python
miss = df.isnull().mean().sort_values(ascending=False)
miss = miss[miss > 0]

miss_report = pd.DataFrame({
    "N_Missing":   df.isnull().sum()[miss.index],
    "Pct_Missing": (miss * 100).round(2),
})
miss_report.to_csv("tables/missing_report.csv")

if not miss_report.empty:
    print("=== 缺失值报告 ===")
    print(miss_report.to_string())

    key_vars = [v for v in [Y_var, D_var, Z_var] if v and v in miss_report.index]
    if key_vars:
        print("\n⚠️  关键变量缺失：")
        for v in key_vars:
            pct = miss_report.loc[v, "Pct_Missing"]
            print(f"  {v}: {pct:.1f}%")
```

---

## Part 2: Results Interpretation（结果解读与经济学意义）

### Step 0: 读取输入文件

依次读取：

```
model-spec.md              # 主方程、识别假设状态
tables/table_main.csv      # 主回归结果
tables/table1_descriptive.csv  # 描述统计
data-report.md             # 样本信息
literature-review-report.md    # 先行文献估计值（可选）
```

---

### Step 1: 提取点估计与置信区间

```python
results = pd.read_csv("tables/table_main.csv", index_col=0)

beta    = results.loc[D_var, "coef"]        # 点估计
se      = results.loc[D_var, "se"]          # 标准误
p_value = results.loc[D_var, "pvalue"]      # p 值
ci_lo   = results.loc[D_var, "ci_low"]      # 95% CI 下界
ci_hi   = results.loc[D_var, "ci_high"]     # 95% CI 上界
n_obs   = results.loc["N", "coef"]

print(f"β̂ = {beta:.4f}（SE = {se:.4f}, p = {p_value:.3f}）")
print(f"95% CI：[{ci_lo:.4f}, {ci_hi:.4f}]")

# 读取描述统计用于量级换算
desc = pd.read_csv("tables/table1_descriptive.csv", index_col=0)
Y_mean = desc.loc[Y_var, "Mean"]
Y_sd   = desc.loc[Y_var, "SD"]
D_mean = desc.loc[D_var, "Mean"]
```

---

### Step 2: 系数量级解读

**量级解读是结果分析最核心的环节。**

根据变量变换类型，自动选择对应的解读框架：

| Y 变换 | D 变换 | 系数含义 | 推荐表达 |
|--------|--------|---------|---------|
| 水平值 | 虚拟变量 | D=1 时 Y 绝对变化量 | "[处理]使 Y 增加 β 个单位" |
| log Y | 虚拟变量 | D=1 时 Y 百分比变化 | "[处理]使 Y 增加约 100β%" |
| log Y | log D | 弹性 | "D 增加 1%，Y 变化 β%" |
| 标准化 z-score | 任意 | 以 Y 的标准差为单位 | "效应量 = β SD" |

#### 效应量计算

```python
# 效应量（Cohen's d 等价）
effect_size_sd = abs(beta) / Y_sd
print(f"效应量：{effect_size_sd:.3f} σ_Y")

if effect_size_sd < 0.1:
    magnitude = "极小（< 0.1σ）"
elif effect_size_sd < 0.3:
    magnitude = "小（0.1–0.3σ）"
elif effect_size_sd < 0.5:
    magnitude = "中等（0.3–0.5σ）"
else:
    magnitude = "较大（> 0.5σ）"
print(f"等级：{magnitude}")

# 相对于均值的百分比
pct_of_mean = beta / Y_mean * 100
print(f"相对于 Y 均值的效应：{pct_of_mean:.1f}%")
```

---

### Step 3: 统计显著性 vs. 经济显著性

**两者必须同时讨论，不可仅凭 p 值下结论。**

```python
def sig_stars(p):
    if p < 0.01: return "***"
    if p < 0.05: return "**"
    if p < 0.10: return "*"
    return "(不显著)"

stars = sig_stars(p_value)
print(f"β̂ = {beta:.4f}{stars}，p = {p_value:.3f}")
print(f"95% CI：[{ci_lo:.4f}, {ci_hi:.4f}]")

# 诊断信息
if p_value < 0.05 and effect_size_sd < 0.05:
    print("⚠️  统计显著但经济上微不足道（大样本效应）")
elif p_value >= 0.05 and (ci_hi - ci_lo) > 0.2:
    print("⚠️  精度不足，无法排除实质效应")
elif p_value >= 0.05 and (ci_hi - ci_lo) <= 0.1:
    print("✅ 精度充分，可合理排除大效应")
```

**经济显著性判断框架：**

```
经济显著性 ⟺
1. 效应量 ≥ 0.1σ_Y
2. 相对于均值 ≥ 5%
3. 置信区间全同号
4. 与 IV/OLS 估计一致
```

---

### Step 4: 与先行文献对比

从 `literature-review-report.md` 提取同类研究的估计值：

```python
# 文献估计汇总表
literature_comparison = {
    "[作者, 年份]": {
        "strategy": "[识别策略]",
        "sample": "[地区/时期]",
        "beta": "[估计值]",
        "comment": "本文高/低/一致"
    }
}

# 差异来源检查
print("""
差异来源检查清单
□ 识别策略不同（OLS vs. IV/DiD）→ 衰减偏误方向
□ 样本差异（国家/时期）→ 异质性
□ 变量定义不同 → 测量误差衰减
□ LATE vs. ATE 差异
□ 短期 vs. 长期效应
□ 政策强度差异
""")

print(f"""
边际贡献定位：
与 [文献] 相比，本文采用 [更可信的识别策略]，
估计值为 {beta:.4f}，[高于/低于/类似于] 文献中位数估计。
差异主要来自 [原因]。
""")
```

---

### Step 5: 识别可信度评估

将 `model-spec.md` 中每条识别假设的状态纳入结果解读：

```python
credibility_assessment = """
识别可信度评估
══════════════════════════════════════════
策略：[策略名称]
目标参数：[ATE / ATT / LATE]

假设状态：
  ✅ [假设1]：[诊断通过的依据]
  ⚠️ [假设2]：[存疑的表现及应对]
  ❌ [假设3]：[未满足的含义]

综合可信度：高 / 中 / 低
══════════════════════════════════════════
"""

# 可信度等级定义
credibility_levels = {
    "高": "所有核心假设 ✅ → 可使用因果语言",
    "中": "核心假设含 ⚠️ 但无 ❌ → 审慎语言",
    "低": "存在 ❌ 假设 → 明确声明局限性，降级为相关性"
}

# 按策略的核心假设快速诊断
core_assumptions = {
    "DiD": "平行趋势假设",
    "RDD": "分配变量无操纵",
    "IV": "排他性限制",
    "Panel FE": "严格外生性",
    "Synthetic Control": "预处理期拟合良好"
}
```

---

### Step 6: 外部有效性与局限性

#### LATE 的适用边界（IV / Fuzzy RDD 用）

```python
late_interpretation = """
LATE 解读
────────────────────────────────────────
本文估计的是 Compliers 的处理效应，即：
"因 [工具变量/阈值] 改变而改变处理状态的个体"

Compliers 可能不代表：
□ Always-takers
□ Never-takers
□ 样本外的其他群体

政策含义：结果直接适用于 [可能受政策影响的边际群体]
────────────────────────────────────────
"""
```

#### 样本代表性

```python
representativeness_check = """
样本代表性检查
- 地理范围：结果是否仅适用于特定国家/地区？
- 时间范围：特定政治经济环境下的效应可推广吗？
- 行业/群体：是否存在选择性进入样本？
- 数据局限：测量误差的影响方向
"""
```

#### 残余内生性风险

```python
residual_endogeneity = """
残余内生性检查
□ 同期发生的其他政策/事件（Confounders）
□ 样本选择
□ 测量误差
□ SUTVA 违反（处理单元间溢出）
□ 一般均衡效应（大规模政策的反馈）
"""
```

---

## Part 3: Output Generation（输出生成）

### Step 1: 生成 `results-memo.md`

整合 Part 2 的所有分析，写入工作目录：

```markdown
# Results Memo
**项目：** [研究问题一句话]
**版本：** v1.0
**日期：** [YYYY-MM-DD]
**对应方程：** model-spec.md，方程 [eq:label]

---

## 1. 核心估计结果

| | 主规格 | 加控制变量 | 全样本 |
|--|--------|-----------|--------|
| β̂ (D_var) | [值]*** | [值]*** | [值]** |
| SE | ([值]) | ([值]) | ([值]) |
| N | [N] | [N] | [N] |

**主系数解读：**
[按 Step 2 格式，含绝对量级、效应量、相对均值百分比]

## 2. 统计显著性 vs. 经济显著性

- **统计显著性：** [显著/边缘显著/不显著]，p = [值]
- **95% CI：** [[lo], [hi]]
- **效应量：** [值] σ_Y（[极小/小/中/大]）
- **相对于均值：** Y 均值的 [值]%
- **经济显著性：** [一句话结论]

## 3. 与先行文献对比

[表格 + 2–3 句话说明差异来源和贡献]

## 4. 识别可信度评估

综合可信度：**[高/中/低]**

[逐条列出假设及状态]

结论语言建议：[因果语言 / 审慎语言 / 相关性语言]

## 5. 外部有效性与局限性

[LATE 边界 + 样本代表性 + 残余内生性威胁]

## 6. Phase 8 稳健性检验优先级

1. **[最高优先级]**：[检验名称]——原因：[...]
2. **[次优先级]**：[检验名称]——原因：[...]
3. **[可选]**：[检验名称]——原因：[...]

## 7. 论文写作建议

- **Results 节核心句**：[直接可用于论文的表达，含系数值和置信区间]
- **语言强度：** [因果 / 审慎因果 / 相关性]
- **Discussion 必须提及的注意事项**：[识别局限性]
```

---

## Common Pitfalls

| ❌ 常见错误 | ✅ 正确做法 |
|------------|------------|
| 平衡性检验用全样本 | **仅用预处理期样本** |
| 只报告 p 值 | 同时报告标准化差异和效应量 |
| EDA 图不标注政策时点 | DiD 趋势图必须标注 `treatment_timing` |
| 表格只保存 .tex | 双格式输出：.tex + .csv |
| 主系数不显著就说"无效应" | CI 窄 = 零效应本身是重要发现 |
| 系数方向与理论预期相反，直接回避 | 排查编码方向、中介变量、样本选择，如实记录 |
| 缺失值报告仅列数量 | 对关键变量给出 MCAR/MAR/MNAR 初步判断 |

---

## Requirements

```bash
pip install pandas numpy matplotlib scipy
```

## Related Skills & Commands

- **`/data`**：调用本 skill 的上级命令（Phase 4 Step 3）
- **`data-pipeline`**：上一阶段，提供本 skill 的输入数据
- **`/model` & `/code`**：Phase 5–6，执行回归并产出 `table_main.csv`
- **`/robustness`**：Phase 8，使用本 skill 生成的 `results-memo.md` 指导稳健性检验
- **`/write`**：Phase 9，直接使用本 skill 生成的结果表格和 results-memo.md
