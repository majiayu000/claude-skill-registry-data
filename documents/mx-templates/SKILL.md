---
name: mx-templates
description: |
  投资分析报告模板库——纯呈现层，不绑定数据源。
  用 {{变量}} 占位，由 mx-data 填充数据。
  由 invest 系列方法论层调用。
triggers:
  - mx-templates
---

# mx-templates：投资分析报告模板库

## 定位

纯呈现层。只定义报告结构和输出格式，不关心数据从哪来。

被 invest-* 方法论层调用，将分析结果渲染为最终报告。

## 模板清单

| 模板 | 用途 | 适用场景 |
|---|---|---|
| `company_onepager.md` | 公司一页纸（9 章节） | 个股深度研究 |
| `fund_deep_report.md` | 基金深度报告（八步流程） | 基金全面分析 |
| `fund_diagnosis.md` | 基金综合诊断报告 | 基金泛化问题 |
| `fund_manager_report.md` | 基金经理研究报告 | 基金经理研究 |
| `bond_onepager.md` | 债券一页纸 | 信用债/地方债分析 |
| `credit_spread.md` | 信用利差分析报告 | 利差分析 |
| `earnings_review.md` | 业绩点评报告 | 财报/业绩解读 |
| `ic_report.md` | 首次覆盖报告 | 首次覆盖/深度研究 |
| `enterprise_15.md` | 企业深度分析（15 板块） | 企业分析 |
| `industry_report.md` | 行业研究报告 | 行业分析 |

## 使用方式

invest-* 方法论层调用模板时：

1. 方法论层完成分析，得到结构化结论
2. 将结论填入模板的 `{{变量}}` 占位符
3. 输出最终报告（Markdown/HTML/PDF）

## 模板变量约定

- `{{company_name}}` — 公司名称
- `{{code}}` — 证券代码
- `{{date}}` — 报告日期
- `{{metrics_table}}` — 关键指标表
- `{{analysis_text}}` — 分析正文
- `{{risk_warning}}` — 风险提示
- `{{disclaimer}}` — 免责声明

## 与 invest 系列、mx-data 的关系

- **mx-data** 提供数据 → invest-* 方法论层分析 → **mx-templates** 渲染输出
- 模板不关心数据来自东财/ttskill/其他源
- 方法论层不关心报告用什么模板渲染
