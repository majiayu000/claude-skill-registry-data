---
name: "financial-analyst"
description: "执行财务比率分析、DCF valuation、预算差异分析和滚动预测，为经营与战略决策提供依据。适用于分析 financial statements、建立估值模型、检查 cash flow、评估预算差异、构建财务预测或处理 spreadsheet 财务数据。"
license: MIT
metadata:
  source: "alirezarezvani/claude-skills"
  language: "zh-CN"
---

# 财务分析师

用于企业财务分析、预测与预算、管理报告、经营绩效分析和估值。核心原则：先验证数据和口径，再计算；所有估值都必须展示假设、敏感性和合理性检查。

## 五阶段工作流

### 1. 界定范围

- 明确分析目标、使用者和要支持的决策。
- 确认数据来源、期间、币种、单位以及合并/单体口径。
- 设定重要性阈值、准确性要求和适用框架。

### 2. 数据分析与建模

- 收集并核验利润表、资产负债表和现金流量表。
- 计算前检查必需字段、空值、符号、量纲和明显不合理值。
- 分析盈利、流动性、杠杆、效率和估值五类比率。
- 构建包含 WACC 与终值的 DCF，并用可比倍数和合理区间做交叉检查。
- 分析实际值、预算值和上年同期差异，区分有利/不利差异。
- 建立驱动因素预测以及基准、乐观、悲观情景。

### 3. 形成洞察

- 解读趋势，并与公司历史和行业基准比较。
- 找出重大差异、驱动因素和根因。
- 用敏感性分析表达估值区间，而不是伪精确单点。
- 比较不同预测情景对决策的影响。

### 4. 报告

- 先给管理层摘要和关键结论。
- 对重大预算差异按部门、类别和驱动因素展开。
- DCF 报告必须包含假设、WACC、终值和敏感性表。
- 滚动预测必须展示趋势、现金缺口和关键风险。

### 5. 跟踪

- 跟踪预测准确率；参考目标为收入 ±5%、费用 ±3%，但应按业务波动调整。
- 用实际结果更新模型并复盘偏差。
- 修订假设时保留版本和理由。

## 内置工具

### 财务比率：`scripts/ratio_calculator.py`

覆盖：

- 盈利：ROE、ROA、毛利率、营业利润率、净利率。
- 流动性：流动比率、速动比率、现金比率。
- 杠杆：负债权益比、利息保障倍数、DSCR。
- 效率：资产、存货、应收账款周转率和 DSO。
- 估值：P/E、P/B、P/S、EV/EBITDA、PEG。

```bash
python scripts/ratio_calculator.py assets/sample_financial_data.json
python scripts/ratio_calculator.py assets/sample_financial_data.json --format json
python scripts/ratio_calculator.py assets/sample_financial_data.json --category profitability
```

### DCF：`scripts/dcf_valuation.py`

功能包括 CAPM/WACC、收入与自由现金流预测、永续增长和退出倍数终值、企业价值/股权价值，以及折现率×增长率双向敏感性分析。

```bash
python scripts/dcf_valuation.py assets/sample_financial_data.json
python scripts/dcf_valuation.py assets/sample_financial_data.json --format json
python scripts/dcf_valuation.py assets/sample_financial_data.json --projection-years 7
```

### 预算差异：`scripts/budget_variance_analyzer.py`

计算金额和百分比差异，默认重大性门槛为 10% 或 50,000 美元，并按收入/费用逻辑判断有利或不利。

```bash
python scripts/budget_variance_analyzer.py assets/sample_financial_data.json
python scripts/budget_variance_analyzer.py assets/sample_financial_data.json --format json
python scripts/budget_variance_analyzer.py assets/sample_financial_data.json --threshold-pct 5 --threshold-amt 25000
```

### 预测：`scripts/forecast_builder.py`

支持驱动因素收入预测、13 周滚动现金流、基准/乐观/悲观情景和简单线性趋势分析。

```bash
python scripts/forecast_builder.py assets/sample_financial_data.json
python scripts/forecast_builder.py assets/sample_financial_data.json --format json
python scripts/forecast_builder.py assets/sample_financial_data.json --scenarios base,bull,bear
```

## 按需参考资料

只读取当前问题需要的文件：

| 文件 | 用途 |
|---|---|
| `references/financial-ratios-guide.md` | 比率公式、解释和行业基准 |
| `references/valuation-methodology.md` | DCF、WACC、终值和可比估值 |
| `references/forecasting-best-practices.md` | 驱动预测、滚动预测和准确率 |
| `references/industry-adaptations.md` | SaaS、零售、制造、金融和医疗行业适配 |
| `references/SKILL.en.md` | 上游英文原文，仅在核对遗漏或升级差异时读取 |

## 模板

| 文件 | 用途 |
|---|---|
| `assets/variance_report_template.md` | 预算差异报告 |
| `assets/dcf_analysis_template.md` | DCF 估值报告 |
| `assets/forecast_report_template.md` | 收入预测报告 |

## 输入格式

脚本接受两种 JSON：

1. **扁平结构**：工具所需字段位于顶层。
2. **组合结构**：四类输入分别放在 `ratio_analysis`、`dcf_valuation`、`budget_variance`、`forecast` 下。

完整示例见 `assets/sample_financial_data.json`。脚本会自动识别结构；缺少可用字段时应以非零状态退出并给出明确错误，不得用臆测数据填补。

## 依赖与边界

所有脚本只使用 Python 标准库，无需 numpy、pandas 或 scipy。计算结果仍须经过口径核对、行业比较和合理性审查；脚本不能替代专业判断。
