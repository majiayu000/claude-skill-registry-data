---
name: spreadsheet-data-cleaning
description: "Profile, clean, standardize, transform, fill, or deduplicate spreadsheet or delimited data into an authorized new output with traceable rules, before/after statistics, an audit log, and validation of formulas, encoding, dimensions, and key summaries. Do not overwrite source data, guess critical values, or delete plausible records, and degrade to a cleaning plan when execution tools are unavailable. Use excel-data-quality-check-basic instead when the user requests only a read-only data-quality audit or issue report without changes or a cleaned copy. 对电子表格或分隔数据进行画像、清洗、标准化、转换、填补或去重，并在用户授权下生成新结果，提供可追踪规则、前后统计、审计日志及公式、编码、行列数和关键汇总验证。不得覆盖原始数据、猜测关键值或删除可能有效的记录；缺少执行工具时降级为清洗计划。用户只要求只读数据质量审计或问题报告，不要求修改或清洗副本时，应使用 excel-data-quality-check-basic。"
---

# Spreadsheet Data Cleaning（表格数据清洗）

Use the section matching the user's language. 使用与用户输入语言一致的章节。

# Spreadsheet Data Cleaning

Read `references/productivity-evidence-and-file-safety.md`, then read `references/cleaning-rules.md`. Use `assets/cleaning-audit-template.md` for the audit log.

Use this Skill when the user requests cleaning, normalization, transformation, filling, deduplication, repair, or a new cleaned output. Use `excel-data-quality-check-basic` for a read-only quality audit that only reports missing values, duplicates, types, formats, or anomalies. Missing spreadsheet tools make an authorized cleaning request degrade to a cleaning plan; they do not turn it into a basic read-only audit.

1. Confirm the source, new output path and format, key columns, uniqueness rules, protected formulas, valid ranges, and business exceptions. Never overwrite the source; keep cleaning results in a separate output.
2. Verify that a spreadsheet or delimited-file reader is available. Without one, inspect only accessible text/metadata and return a cleaning specification, not a cleaned-file claim.
3. Profile sheets, dimensions, headers, inferred types, missingness, duplicates, whitespace, encoding, formats, formulas, enums, and potential outliers before changing data.
4. Define each rule with target columns, condition, transformation, ambiguity policy, and expected count. Quarantine or flag ambiguous records; do not guess critical identifiers or delete plausible values.
5. Apply rules to a new output. Preserve raw values in the audit trail and keep row-level traceability when practical.
6. Reopen and validate the output: encoding, sheet names, row/column counts, formulas, data types, key uniqueness, missingness, and reconciled summaries. Report unverified checks.
7. Return before/after statistics, applied/skipped rules, exceptions, audit location, output location, and residual risks.

# Output Contract

1. Source profile and assumptions
2. Cleaning rules and ambiguity policy
3. Before/after statistics
4. Output and audit-log locations
5. Validation results, exceptions, and residual risks

---

# 表格数据清洗

先读取 `references/productivity-evidence-and-file-safety.md`，再读取 `references/cleaning-rules.md`。使用 `assets/cleaning-audit-template.md` 记录审计日志。

用户要求清洗、规范化、转换、填补、去重、修复或生成新的清洗结果时使用本 Skill。只要求只读报告缺失、重复、类型、格式或异常的数据质量审计时，使用 `excel-data-quality-check-basic`。缺少表格工具时，已获授权的清洗请求降级为清洗计划，而不是变成 basic 只读审计。

1. 确认来源、新输出路径与格式、关键列、唯一性规则、受保护公式、合法范围和业务例外；绝不覆盖原文件，清洗结果始终写入独立输出。
2. 确认平台具备电子表格或分隔文件读取工具；没有工具时只能基于可访问文本/元数据输出清洗规格，不得声称已生成清洗文件。
3. 修改前画像工作表、行列数、表头、推断类型、缺失、重复、空格、编码、格式、公式、枚举和潜在异常值。
4. 为每条规则定义目标列、条件、转换、歧义处理和预期数量；隔离或标记歧义记录，不猜测关键标识，不删除可能有效的数据。
5. 将规则应用到新输出，审计日志保留原值，并尽量保留行级追踪。
6. 重新打开并验证编码、工作表名、行列数、公式、类型、关键唯一性、缺失和汇总勾稽；报告未验证项目。
7. 输出前后统计、已执行/跳过规则、例外、审计与结果位置及残余风险。

# 输出契约

1. 原始数据画像与假设
2. 清洗规则与歧义策略
3. 前后统计
4. 结果与审计日志位置
5. 验证结果、例外和残余风险
