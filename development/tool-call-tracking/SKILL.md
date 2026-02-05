---
name: tool-call-tracking
description: Instrument agent tool executions with proper context and error handling
triggers:
  - "track tool calls"
  - "instrument tools"
  - "tool execution spans"
  - "function call tracing"
priority: 1
---

# Tool Call Tracking

Instrument tool/function executions to understand what agents do and why they fail.

## Core Principle

Tools are where agents interact with the real world. Track:
1. **Which tool** was called
2. **What arguments** were passed (safely)
3. **What result** was returned (safely)
4. **Did it succeed** or fail
5. **How long** it took

## Essential Span Attributes

```python
# Required (P0)
span.set_attribute("tool.name", "web_search")
span.set_attribute("tool.success", True)
span.set_attribute("tool.latency_ms", 450)

# Safe argument summary (P1)
span.set_attribute("tool.args.query", "weather in NYC")  # Safe to log
span.set_attribute("tool.args.count", 3)  # Summarize, don't dump

# Result summary (P1)
span.set_attribute("tool.result.type", "search_results")
span.set_attribute("tool.result.count", 10)
span.set_attribute("tool.result.length", 2500)

# Error context (when applicable)
span.set_attribute("tool.error.type", "timeout")
span.set_attribute("tool.error.message", "Request timed out after 30s")
```

## What NOT to Log

```python
# BAD - Full arguments (PII risk, unbounded size)
span.set_attribute("tool.args", json.dumps(args))
span.set_attribute("tool.result", json.dumps(result))

# BAD - Sensitive tool arguments
span.set_attribute("tool.args.api_key", api_key)
span.set_attribute("tool.args.password", password)

# GOOD - Safe summaries
span.set_attribute("tool.args.has_credentials", True)
span.set_attribute("tool.result.success", True)
```

## Tool Categories

Different tools need different instrumentation:

### Search/Retrieval Tools
```python
span.set_attribute("tool.name", "vector_search")
span.set_attribute("tool.retrieval.query_length", len(query))
span.set_attribute("tool.retrieval.results_count", len(results))
span.set_attribute("tool.retrieval.top_score", results[0].score)
```

### API/HTTP Tools
```python
span.set_attribute("tool.name", "http_request")
span.set_attribute("tool.http.method", "POST")
span.set_attribute("tool.http.url", sanitize_url(url))  # Remove query params
span.set_attribute("tool.http.status", 200)
```

### Database Tools
```python
span.set_attribute("tool.name", "sql_query")
span.set_attribute("tool.db.operation", "SELECT")
span.set_attribute("tool.db.table", "users")
span.set_attribute("tool.db.rows_affected", 5)
```

### File System Tools
```python
span.set_attribute("tool.name", "read_file")
span.set_attribute("tool.file.path", sanitize_path(path))
span.set_attribute("tool.file.size_bytes", 1024)
span.set_attribute("tool.file.type", "text/plain")
```

### Code Execution Tools
```python
span.set_attribute("tool.name", "python_repl")
span.set_attribute("tool.code.lines", 15)
span.set_attribute("tool.code.has_imports", True)
span.set_attribute("tool.execution.exit_code", 0)
```

## Wrapper Pattern

Generic tool wrapper for consistent instrumentation:

```python
from functools import wraps
from langfuse.decorators import observe

def traced_tool(tool_name: str):
    def decorator(func):
        @wraps(func)
        @observe(name=f"tool.{tool_name}")
        def wrapper(*args, **kwargs):
            span = get_current_span()
            span.set_attribute("tool.name", tool_name)

            try:
                result = func(*args, **kwargs)
                span.set_attribute("tool.success", True)
                return result
            except Exception as e:
                span.set_attribute("tool.success", False)
                span.set_attribute("tool.error.type", type(e).__name__)
                span.set_attribute("tool.error.message", str(e)[:500])
                raise
        return wrapper
    return decorator

@traced_tool("web_search")
def search_web(query: str) -> list:
    # Tool implementation
    pass
```

## Framework Integration

### LangChain Tools
```python
from langchain.tools import tool
from langfuse.decorators import observe

@tool
@observe(name="tool.calculator")
def calculator(expression: str) -> float:
    """Evaluate math expression."""
    return eval(expression)
```

### CrewAI Tools
```python
from crewai import Agent
from langfuse.decorators import observe

@observe(name="tool.research")
def research_tool(topic: str) -> str:
    # Implementation
    pass
```

## Error Categories

Track error types for better debugging:
```python
ERROR_CATEGORIES = {
    "timeout": ["TimeoutError", "ReadTimeout"],
    "rate_limit": ["RateLimitError", "TooManyRequests"],
    "auth": ["AuthenticationError", "PermissionDenied"],
    "validation": ["ValidationError", "InvalidInput"],
    "network": ["ConnectionError", "NetworkError"],
    "internal": ["InternalError", "ServerError"],
}
```

## Anti-Patterns

See `references/anti-patterns/tool-tracing.md`:
- Logging full arguments (PII, unbounded)
- Logging credentials
- Missing error categorization
- No latency tracking

## Related Skills
- `error-retry-tracking` - Error handling patterns
- `llm-call-tracing` - LLM-specific instrumentation
