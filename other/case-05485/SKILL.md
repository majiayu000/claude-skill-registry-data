---
name: private-fund-portfolio-analysis
description: 私募基金持仓结构分析脚本构建方法。支持市场中性（期货空头对冲）和指数增强（持仓 vs 对标指数超配/低配）两种产品类型。当需要从私募基金估值表（XLS/XLSX）解析持仓，分析行业分布/市值分布/指数成分/期货对冲，并生成可视化报告时触发。也用于：生成持仓分析脚本、重构脚本、添加新数据源、修复脚本Bug、生成分析报告。
---

# 私募基金持仓结构分析脚本构建

## 两种产品类型

| 类型 | 命令 | 说明 |
|------|------|------|
| 市场中性 | `--type market_neutral` | 期货空头，分析对冲端 |
| 指数增强 | `--type index_enhanced --benchmark 中证500` | 持仓 vs 对标指数超配/低配 |

## 脚本位置

- **市场中性版**：`/workspace/analyze_portfolio.py`
- **指数增强版**：`/workspace/analyze_portfolio_enhanced.py`

## 使用方式

```bash
# 市场中性
python3 analyze_portfolio_enhanced.py --xls <估值表路径> --type market_neutral

# 指数增强（指定对标指数）
python3 analyze_portfolio_enhanced.py --xls <估值表路径> --type index_enhanced --benchmark 中证500
python3 analyze_portfolio_enhanced.py --xls <估值表路径> --type index_enhanced --benchmark 沪深300
python3 analyze_portfolio_enhanced.py --xls <估值表路径> --type index_enhanced --benchmark 中证1000
python3 analyze_portfolio_enhanced.py --xls <估值表路径> --type index_enhanced --benchmark 中证2000
python3 analyze_portfolio_enhanced.py --xls <估值表路径> --type index_enhanced --benchmark 空气指增
```

## XLS 解析要点

估值表结构（以 xlrd 读取，行65+有股票数据）：

```
col0: 科目代码（层级结构，如 "1102.01.01.600519 SH"）
col1: 名称
col4: 数量（股数）
col5: 单位成本
col6: 累计成本
col8: 行情/结算价
col9: 市值 ← 持仓市值
col11: 估值增值/PnL
```

**提取6位股票代码**：从层级代码中用正则提取，如 `1102.01.01.600519 SH` → `600519`

**期货行**（账户代码含 `3102.03.01.`）：
- col4 = 手数
- col5 = 昨日结算价
- col9 = 今日结算价
- 名义本金 = 今日结算价 × 乘数 × 手数

**乘数**：IF/IH = 300；IC/IM = 200

## 指数增强核心功能

### 超配/低配计算

```
超配(%) = 持仓行业市值占比 - 对标指数行业市值占比
正数 = 超配（相对于指数）；负数 = 低配
```

只显示 |差值| > 0.5% 的行业（过滤噪音）

### 对标指数数据来源

| 对标指数 | 代码 | 数据源 |
|---------|------|---------|
| 沪深300 | 000300 | `ak.index_stock_cons("000300")` |
| 中证500 | 000905 | `ak.index_stock_cons("000905")` |
| 中证1000 | 000852 | `ak.index_stock_cons("000852")` |
| 中证2000 | 932000 | `ak.index_stock_cons_csindex("932000")` |

## 数据 Enrichment

- **市值**：`ak.stock_zh_a_spot_em()` → 市场数据缓存 CSV
- **行业**：MySQL `股票申万行业分类`（charset=utf8mb4）
- **指数成分**：AKShare

## MySQL 连接（占位符）

```python
conn = pymysql.connect(
    host=os.environ.get("MYSQL_HOST", "43.138.222.153"),
    port=int(os.environ.get("MYSQL_PORT", "3306")),
    user=os.environ.get("MYSQL_USER", "readonly_user"),
    password=os.environ.get("MYSQL_PASSWORD", "w6w%vkXENC82PGZo"),
    database=os.environ.get("MYSQL_DATABASE", "指数行情数据库"),
    connect_timeout=8, charset="utf8mb4"
)
```

## 输出文件

| 文件 | 说明 |
|------|------|
| `portfolio_analysis.csv` | 持仓明细（355只股票） |
| `portfolio_summary.json` | 汇总统计 |
| `portfolio_report.png` | 可视化报告 |

## 参考文档

- `references/xls_structure.md` — XLS 行列结构详解
- `references/data_sources.md` — AKShare/MySQL 数据源配置
- `scripts/generate_analysis_script_prompt.py` — 可直接粘贴给 Claude Code 的提示词

## 注意

- **XLS 列位因模板不同可能有差异**，建议用 `print(row[:12])` 验证
- **MySQL charset 必须用 `utf8mb4`**，否则中文字符报错
- **中证2000 用 `index_stock_cons_csindex("932000")`**，稳定性高于 `index_stock_cons`
- 不要 hardcode 任何真实密码/地址/产品名称
