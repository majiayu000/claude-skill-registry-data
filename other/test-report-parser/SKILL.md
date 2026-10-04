---
name: test-report-parser
description: Parse and analyze test results from various formats
activation_keywords: [test, report, parse, junit, coverage, result, xml, json]
execution_mode: server
---

# Test Report Parser Skill

Parse test results from various formats:

- **JUnit XML**: Parse JUnit test reports
- **JSON**: Parse JSON test output
- **Cobertura**: Parse coverage reports
- **JaCoCo**: Parse Java coverage reports
- **Istanbul**: Parse JavaScript coverage

Use `builtin_test_report_parser` tool with fields:
- `operation`: "parse" | "summary" | "failures"
- `format`: "junit" | "json" | "cobertura" | "jacoco" | "istanbul"
- `path`: Path to test report file
- `filters`: (optional) Filter by status: "passed" | "failed" | "skipped"

Returns:
- Total tests, passed, failed, skipped count
- Test duration
- Failure details with stack traces
- Coverage percentage (if available)