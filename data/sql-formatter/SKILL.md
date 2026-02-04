---
name: sql-formatter
description: This skill should be used when the user asks to format SQL code, polish SQL queries, improve SQL readability, or work with .sql files. Use when queries mention SQL formatting, code beautification, Oracle SQL, or database query polishing.
---

# SQL Code Formatter

Format, polish, and document SQL code following Oracle Database 19 best practices with consistent style and readability.

## Purpose

This skill provides comprehensive SQL code formatting rules and guidelines for Oracle Database 19. It enforces consistent code style, improves readability, and applies industry-standard formatting conventions to SQL queries, DDL statements, and DML operations.

## When to Use This Skill

Use this skill when:

- Formatting or beautifying SQL code
- Working with .sql files that need polishing
- Improving SQL query readability
- Standardizing SQL code style across projects
- Documenting complex SQL queries
- Reviewing or refactoring existing SQL code
- Converting unformatted SQL to well-structured queries

## Core Formatting Principles

### 1. Case Conventions

- **SQL Keywords**: UPPERCASE (SELECT, FROM, WHERE, JOIN, etc.)
- **Identifiers**: lowercase (column names, table names, aliases)
- **Consistency**: Maintain consistent casing throughout queries

Example:
```sql
SELECT employee_id,
       first_name,
       last_name
  FROM employees
 WHERE department_id = 10;
```

### 2. Indentation and Alignment

- Use **4 spaces** for indentation (no tabs)
- Align subsequent columns/conditions vertically with the first item
- Indent sub-queries one level deeper than parent query
- Align clause keywords (SELECT, FROM, WHERE) at consistent positions

### 3. Line Breaks and Structure

- **First item on same line**: Start first column/condition on the same line as the clause keyword
- **New line for each item**: Each subsequent column, condition, or table goes on a new line
- **New line for clauses**: Start each major clause (SELECT, FROM, WHERE, JOIN, GROUP BY, ORDER BY, HAVING) on a new line
- **Vertical alignment**: Align continuation items vertically

Example:
```sql
SELECT first_column,
       second_column,
       third_column
  FROM table_name
 WHERE first_condition
   AND second_condition
   AND third_condition;
```

### 4. Operators and Spacing

- Single space on either side of operators (=, <, >, <=, >=, !=, ||, +, -, *, /)
- Single space after commas
- Single space around AS keyword for aliases

### 5. Common Table Expressions (CTEs)

- Begin with WITH keyword followed by CTE name
- Place AS ( on the same line as CTE name
- Close with ) on new line, aligned with WITH
- Separate multiple CTEs with comma and line break

Example:
```sql
WITH active_employees AS (
    SELECT employee_id,
           first_name,
           last_name
      FROM employees
     WHERE status = 'ACTIVE'
),
department_summary AS (
    SELECT department_id,
           COUNT(*) AS employee_count
      FROM active_employees
     GROUP BY department_id
)
SELECT *
  FROM department_summary;
```

### 6. JOIN Clauses

- Explicitly specify JOIN type (INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN)
- Place JOIN and first ON condition on same line
- Indent JOIN to align with FROM clause
- Additional ON conditions go on new lines with AND keyword

Example:
```sql
SELECT e.employee_id,
       e.first_name,
       d.department_name
  FROM employees e
 INNER JOIN departments d ON e.department_id = d.department_id
        AND e.status = 'ACTIVE'
        AND d.status = 'ACTIVE';
```

### 7. CASE Expressions

- Start CASE with first WHEN on same line
- Each subsequent WHEN, all THEN, and ELSE on separate lines
- Align WHEN, THEN, and ELSE vertically
- Place END aligned with CASE
- Column alias on same line as END

Example:
```sql
SELECT CASE WHEN salary < 50000
            THEN 'Low'
            WHEN salary BETWEEN 50000 AND 100000
            THEN 'Medium'
            ELSE 'High'
       END AS salary_category
  FROM employees;
```

### 8. INSERT Statements

- List columns in parentheses, one per line (except first)
- Align columns vertically
- VALUES clause follows same pattern

Example:
```sql
INSERT INTO employees (
            employee_id,
            first_name,
            last_name,
            department_id
) VALUES (
            1001,
            'Jane',
            'Smith',
            20
);
```

### 9. UPDATE Statements

- Place table name on same line or new line after UPDATE
- SET clause on new line
- Each column assignment on new line (except first)
- WHERE clause on new line

Example:
```sql
UPDATE employees
   SET first_name = 'John',
       last_name = 'Doe',
       salary = 75000
 WHERE employee_id = 1001;
```

### 10. Comments

- Use `--` for single-line comments
- Use `/* comment */` for multi-line comments
- Add comments to explain complex logic only when explicitly requested
- Place comments above the code they describe

## Bundled Resources

### References (`references/`)

- `references/sql-formatting-rules.md` - Complete formatting specification with all 13 rules and detailed examples

Load this reference when working with complex SQL formatting scenarios or when users need detailed rule explanations.

## How to Use This Skill

### Basic SQL Formatting

When user provides unformatted SQL code:

1. Identify SQL statement type (SELECT, INSERT, UPDATE, DELETE, CREATE, etc.)
2. Apply core formatting principles from this skill
3. Ensure keywords are UPPERCASE and identifiers are lowercase
4. Apply proper indentation (4 spaces)
5. Align columns, conditions, and clauses vertically
6. Return formatted SQL code

### Advanced Formatting

For complex queries with CTEs, joins, subqueries, and CASE expressions:

1. Read `references/sql-formatting-rules.md` for detailed specifications
2. Apply all 13 formatting rules in sequence
3. Pay special attention to vertical alignment
4. Ensure consistent indentation at all nesting levels
5. Validate that all examples in the reference are followed

### Working with .sql Files

When user requests formatting of .sql files:

1. Read the SQL file content
2. Apply formatting rules to each statement
3. Preserve existing comments unless reformatting is requested
4. Write back formatted SQL to the file or display for review
5. Ensure file encoding is preserved (UTF-8 recommended)

## Key Information

- **Database:** Oracle Database 19
- **Indentation:** 4 spaces (no tabs)
- **Keywords:** UPPERCASE
- **Identifiers:** lowercase
- **Line Length:** No strict limit, but prefer readability
- **File Extension:** .sql

## Best Practices

- Apply formatting consistently across all SQL files in a project
- Format SQL before committing to version control
- Use vertical alignment to improve readability
- Keep related conditions grouped with parentheses
- Add comments sparingly, only for complex logic
- Test formatted SQL to ensure functionality is preserved
- Preserve the logical structure and query optimization

## Troubleshooting

**Issue: Query becomes too long horizontally**
- Break long expressions across multiple lines
- Use CTEs to simplify complex subqueries
- Split long CASE expressions into multiple lines

**Issue: Unclear which columns belong to which clause**
- Ensure consistent vertical alignment
- Use proper indentation (4 spaces per level)
- Verify first column/condition is on same line as clause keyword

**Issue: Complex joins are hard to read**
- Place each JOIN on its own line
- Align all JOINs with FROM clause
- Put additional ON conditions on separate lines with AND

**Issue: Formatted SQL doesn't execute**
- Verify formatting didn't introduce syntax errors
- Check that all parentheses are balanced
- Ensure string literals are properly quoted
- Test the query after formatting

## Examples

See the `examples/` directory for sample SQL files showing:

- `examples/unformatted.sql` - Before formatting
- `examples/formatted.sql` - After applying formatting rules
- `examples/complex-query.sql` - Complex query with CTEs and joins

## Additional Notes

- This skill focuses on formatting and style, not query optimization
- The formatting rules preserve Oracle SQL syntax and semantics
- For very large SQL files (>1000 lines), consider formatting sections separately
- Formatted SQL is easier to review, debug, and maintain
- Consistent formatting improves team collaboration and code reviews
