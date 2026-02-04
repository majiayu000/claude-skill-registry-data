---
name: using-braintrust
description: |
  Enables AI agents to use Braintrust for LLM evaluation, logging, and observability.
  Includes scripts for querying logs with SQL, running evals, and logging data.
version: 1.0.0
---

# Using Braintrust

Braintrust is a platform for evaluating, logging, and monitoring LLM applications.

## Listing projects

Use `scripts/list_projects.py` to see all available projects:

```bash
uv run /path/to/scripts/list_projects.py
```

## Querying logs with SQL

Use the `query_logs.py` script to run SQL queries against Braintrust logs.

**Always share the SQL query you used** when reporting results, so the user understands what was executed.

**Script location:** `scripts/query_logs.py` (relative to this file)

**Run from the user's project directory** (where `.env` with `BRAINTRUST_API_KEY` exists):

```bash
uv run /path/to/scripts/query_logs.py --project "Project Name" --query "SQL_QUERY"
```

### Common queries

**Count logs from last 24 hours:**
```sql
SELECT count(*) as count FROM logs WHERE created > now() - interval 1 day
```

**Get recent logs:**
```sql
SELECT input, output, created FROM logs ORDER BY created DESC LIMIT 10
```

**Filter by metadata:**
```sql
SELECT input, output FROM logs WHERE metadata.user_id = 'user123' LIMIT 20
```

**Filter by time range:**
```sql
SELECT * FROM logs WHERE created > now() - interval 7 day LIMIT 50
```

**Aggregate by field:**
```sql
SELECT metadata.model, count(*) as count FROM logs GROUP BY metadata.model
```

**Group by hour:**
```sql
SELECT hour(created) as hr, count(*) as count FROM logs GROUP BY hour(created)
```

### SQL quirks in Braintrust

- **Time functions**: Use `hour()`, `day()`, `month()`, `year()` instead of `date_trunc()`
  - ✅ `hour(created)`
  - ❌ `date_trunc('hour', created)`
- **Intervals**: Use `interval 1 day`, `interval 7 day`, `interval 1 hour` (no quotes, singular unit)
- **Nested fields**: Use dot notation: `metadata.user_id`, `scores.Factuality`, `metrics.duration`
- **Table name**: Always use `FROM logs` (the script handles project scoping)

### SQL reference

**Operators:**
- `=`, `!=`, `>`, `<`, `>=`, `<=`
- `IS NULL`, `IS NOT NULL`
- `LIKE 'pattern%'`
- `AND`, `OR`, `NOT`

**Aggregations:**
- `count(*)`, `count(field)`
- `avg(field)`, `sum(field)`
- `min(field)`, `max(field)`

**Time filters:**
- `created > now() - interval 1 day`
- `created > now() - interval 7 day`
- `created > now() - interval 1 hour`

## Logging data

Use `scripts/log_data.py` to log data to a project:

```bash
uv run /path/to/scripts/log_data.py --project "Project Name" --input "query" --output "response"
```

With metadata:
```bash
--input "query" --output "response" --metadata '{"user_id": "123"}'
```

Batch from JSON:
```bash
--data '[{"input": "a", "output": "b"}, {"input": "c", "output": "d"}]'
```

## Running evaluations

Use `scripts/run_eval.py` to run evaluations:

```bash
uv run /path/to/scripts/run_eval.py --project "Project Name" --data '[{"input": "test", "expected": "test"}]'
```

From file:
```bash
--data-file test_cases.json --scorer factuality
```

## Setup

Create a `.env` file in your project directory:

```
BRAINTRUST_API_KEY=your-api-key-here
```

## Writing evaluation code (SDK)

For custom evaluation logic, use the SDK directly.

**IMPORTANT**: First argument to `Eval()` is the project name (positional).

```python
import braintrust
from autoevals import Factuality

braintrust.Eval(
    "My Project",  # Project name (required, positional)
    data=lambda: [{"input": "What is 2+2?", "expected": "4"}],
    task=lambda input: my_llm_call(input),
    scores=[Factuality],
)
```

**Common mistakes:**
- ❌ `Eval(project_name="My Project", ...)` - Wrong!
- ❌ `Eval(name="My Project", ...)` - Wrong!
- ✅ `Eval("My Project", data=..., task=..., scores=...)` - Correct!

## Writing logging code (SDK)

```python
import braintrust

logger = braintrust.init_logger(project="My Project")
logger.log(input="query", output="response", metadata={"user_id": "123"})
logger.flush()  # Always flush!
```

## Common issues

- **"Eval() got an unexpected keyword argument 'project_name'"**: Use positional argument
- **Logs not appearing**: Call `logger.flush()` after logging
- **Authentication errors**: Create `.env` file with `BRAINTRUST_API_KEY=your-key`
