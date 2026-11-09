---
name: headcount-report
description: The standard DataStream Corp headcount report. Use when asked for headcount, employee counts per department or a staffing overview.
---
# Headcount report

1. Count only employees with `status = 'active'`.
2. One row per department (`employees.department_id = departments.id`); keep departments with no active employees
   (LEFT JOIN, count 0).
3. Columns, in this order: Department | Active employees | Share of company (%, one decimal). Compute the share
   in the SQL query (`ROUND(100.0 * count / total, 1)`), never by hand.
4. Sort by active employees, largest first, then add a final **Total** row.
5. Answer with the markdown table, then exactly one line: `Source: datastream_corp.db, active employees only.`
