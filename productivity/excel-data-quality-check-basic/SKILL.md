---
name: excel-data-quality-check-basic
description: "Perform a read-only spreadsheet data-quality audit that reports missing values, duplicates, types, formats, anomalies, and source-traceability issues without cleaning, standardizing, filling, deduplicating, overwriting, or generating a modified copy. Use for requests to check, audit, or list data-quality problems; use spreadsheet-data-cleaning when the user requests transformations, fixes, or a cleaned output. 对表格执行只读数据质量审计，报告缺失、重复、类型、格式、异常和来源可追溯性问题，不清洗、标准化、填补、去重、覆盖或生成修改后的副本。用于检查、审计或列出数据质量问题；用户要求转换、修复或输出清洗结果时使用 spreadsheet-data-cleaning。"
---

# English

# Basic Excel Data Quality Check

Perform a read-only spreadsheet data-quality audit using generic public-safe rules.

## Safety Boundary

- Do not include finance or investment advice.
- Do not infer business meaning without source evidence.
- Do not clean, standardize, fill, deduplicate, overwrite, or generate a modified spreadsheet copy.
- Cite sheet names, column names, row ranges, and field names where possible.

## Routing Boundary

- Use this Skill for requests to check, audit, or list missing values, duplicates, types, formats, and anomalies without changing data.
- Use `spreadsheet-data-cleaning` when the user asks to clean, normalize, transform, repair, fill, deduplicate, or create a cleaned output.
- If a request starts as an audit but asks for changes, do not apply them; hand the modification task to `spreadsheet-data-cleaning`.
- When spreadsheet tools are unavailable, report what cannot be inspected and do not claim that a data-quality check was completed.

## Workflow

1. Identify workbook structure: sheets, tables, headers, dimensions, and data types.
2. Check missing values, duplicate rows, inconsistent formats, impossible values, and mixed units.
3. Check whether key fields and source fields are present.
4. Summarize data quality risks and manual confirmation items.
5. Suggest safe next steps without applying changes or generating a modified file.

# Output Format

1. Workbook overview
2. Sheet and field inventory
3. Data quality findings
4. Evidence references
5. Suggested next steps not applied
6. Manual confirmation items

# 简体中文

# Excel 数据质量基础检查

使用通用、公开安全的规则执行只读表格数据质量审计。

## 安全边界

- 不包含财务或投资建议。
- 没有来源证据时不推断业务含义。
- 不清洗、标准化、填补、去重、覆盖或生成修改后的表格副本。
- 尽量引用工作表名称、列名、行范围和字段名。

## 路由边界

- 用户要求在不改变数据的前提下检查、审计或列出缺失、重复、类型、格式和异常时使用本 Skill。
- 用户要求清洗、规范化、转换、修复、填补、去重或生成清洗结果时使用 `spreadsheet-data-cleaning`。
- 如果请求先要求审计又要求修改，不在本 Skill 中执行修改；把修改任务转交 `spreadsheet-data-cleaning`。
- 表格工具不可用时报告无法检查的内容，不得声称已完成数据质量检查。

## 工作流程

1. 识别工作簿结构：工作表、表格、表头、维度和数据类型。
2. 检查缺失值、重复行、格式不一致、不可能值和单位混用。
3. 检查关键字段和来源字段是否存在。
4. 总结数据质量风险和人工确认项。
5. 建议安全后续步骤，但不应用修改或生成修改后的文件。

# 输出格式

1. 工作簿概览
2. 工作表和字段清单
3. 数据质量问题
4. 证据来源
5. 未执行的建议后续步骤
6. 人工确认项
