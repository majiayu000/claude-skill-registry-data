---
name: add-error-handling
description: Implement comprehensive error handling for Python code paths to keep services resilient and user-friendly. Use when failures are currently silent or exceptions leak through.
license: MIT
compatibility: claude cursor opencode
metadata:
  version: "1.0.0"
  languages: python
  audience: developers
  workflow: maintenance
  since: "2026-02-25"
---

# Add Error Handling

Strengthen resilience by catching and recovering from predictable failures.

## Steps

1. **Error detection**
   - Identify failure points (network calls, file I/O, external APIs)
   - Find unhandled exceptions, missing validations, and async errors
   - Ensure coroutine boundaries (`async def`) wrap awaited calls with exception handling

2. **Handling strategy**
   - Use specific exception types (`ValueError`, `RuntimeError`, custom errors) instead of bare `except`
   - Raise from lower-level exceptions (`raise MyError(...) from exc`) to preserve context
   - Validate inputs early (pydantic models, schema checks, `assert` statements for invariants)
   - Log structured errors with correlation IDs or context-specific metadata

3. **Recovery mechanisms**
   - Retry transient failures with exponential backoff (`tenacity`, `async_retry`)
   - Provide fallbacks (cached data, defaults) when external services fail
   - Use context managers (`with` statements) to guarantee cleanup
   - Propagate user-friendly errors to callers while logging detailed internals

4. **User experience**
   - Return clear API responses (HTTP 4xx/5xx) with actionable messages
   - Add loading states or retries for UI/integration components when backend requests fail
   - Suggest remediation steps in logs/docs if manual intervention is required

## Checklist
- [ ] Identified every potential failure point in the changed code
- [ ] Added validation and sanitization for external inputs
- [ ] Logged meaningful error details without leaking secrets
- [ ] Wrapped async calls with appropriate `try/except` or `asyncio.wait_for`
- [ ] Added retries or fallbacks for transient dependencies
- [ ] Raised custom exceptions with `from` chains for traceability
- [ ] Provided clear user-facing messages or HTTP status codes
