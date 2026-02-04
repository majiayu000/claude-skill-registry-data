---
name: error-doctor
description: Systematic error diagnosis and debugging framework
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: debugging
---

## What I do

- Diagnose errors systematically using stack trace analysis
- Classify error types (SyntaxError, ImportError, TypeError, etc.)
- Identify root causes and suggest fixes
- Provide actionable remediation steps

## When to use me

Use this when you encounter:
- Unexpected exceptions or crashes
- Error messages you don't understand
- Debugging complex failure scenarios
- Need systematic approach to error fixing

## MCP-First Workflow

Always use MCP servers in this order:

1. **codebase** - Search for error handling patterns
   ```python
   search_codebase("error handling patterns Python exception", top_k=10)
   ```

2. **sequential-thinking** - Analyze the error
   ```python
   think_step_by_step("Analyze the error stack trace and identify root cause...")
   ```

3. **filesystem** - view_file the error source
   ```python
   read_file("src/module.py", offset=100, limit=50)
   ```

4. **git** - Check recent changes
   ```python
   git_diff("HEAD~5..HEAD", path="src/")
   ```

## Error Diagnosis Framework

| Error Type | Indicator | Action |
|------------|-----------|--------|
| SyntaxError | "SyntaxError" | Fix code syntax |
| ImportError | "ModuleNotFoundError" | Check imports, install deps |
| TypeError | "expected X got Y" | Fix type mismatch |
| ValueError | "invalid value" | Validate input |
| RuntimeError | Generic runtime | Debug logic flow |
| NetworkError | Connection/timeout | Check service, increase timeout |

## Common Fixes

| Error Pattern | Fix |
|---------------|-----|
| `NoneType has no attribute` | Add null checks with `get()` or `or` |
| `list index out of range` | Validate index bounds |
| `division by zero` | Check denominator before division |
| `connection refused` | Verify service is running |
| `timeout expired` | Increase timeout or implement retry |

## Example Usage

```
Error: KeyError: 'key' in src/module.py:120

Diagnosis:
1. The code tries to access data["key"] but 'key' doesn't exist
2. Check if the key exists with data.get("key", default_value)
3. Verify the data source provides the expected key
```
