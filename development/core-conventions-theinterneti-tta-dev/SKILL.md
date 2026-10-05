---
name: core-conventions
description: 'Use this skill when writing or reviewing Python code in TTA.dev. Covers the package manager (uv), type hint standards, primitives usage, anti-patterns to avoid, state management, and LLM provider strategy. Invoke when the user says "write code", "review code", "add a feature", or asks about conventions or standards.'
---

### Core Conventions (TTA.dev)

Non-negotiable standards for all code in the TTA.dev repository.

#### Package Manager

**Always use `uv`, never `pip` or `poetry`.**

```bash
uv add package-name        # Add dependency
uv sync --all-extras       # Sync all dependencies
uv run pytest -v           # Run via uv
```

#### Python Version & Types

- Python 3.12+ required
- `str | None` not `Optional[str]`
- `dict[str, Any]` not `Dict[str, Any]`
- Google-style docstrings on all public functions

#### Primitives — Always Use Them

```python
# ✅ Use primitives
workflow = RetryPrimitive(primitive=api_call, max_retries=3)

# ❌ Never write manual retry/timeout loops
for attempt in range(3):  # WRONG
    try: ...
```

#### Anti-Patterns

| ❌ Don't | ✅ Do |
|---------|------|
| `try/except` retry loops | `RetryPrimitive` |
| `asyncio.wait_for()` | `TimeoutPrimitive` |
| Manual caching dicts | `CachePrimitive` |
| Global variables for state | `WorkflowContext` |
| `pip install` | `uv add` |
| `Optional[str]` | `str | None` |
| `from primitives.X` | `from ttadev.primitives.X` |

#### State Management

Pass state via `WorkflowContext`, never global variables:

```python
context = WorkflowContext(workflow_id="demo")
result = await workflow.execute(input_data, context)
```

#### LLM Provider Strategy

**Always use `get_llm_client()` — never hardcode a model or base URL.**

```python
from ttadev.workflows.llm_provider import get_llm_client

cfg = get_llm_client()
# cfg.base_url, cfg.model, cfg.api_key, cfg.provider
```

Provider hierarchy for TTA.dev apps (automatic, zero config required):
1. **Ollama** — default, always available, no API key needed (`qwen2.5:7b`)
2. **OpenRouter `:free`** — if `OPENROUTER_API_KEY` is set
3. **Paid models** — if a paid key is configured

**Never use** `nvidia/nemotron-3-super-120b-a12b:free` — it is a reasoning-only
model that returns `content: null`. Any code reading `response.content` will crash.

#### Deep Reference

- Primitives API & patterns: [`docs/agent-guides/primitives-patterns.md`](../../docs/agent-guides/primitives-patterns.md)
- Python standards: [`docs/agent-guides/python-standards.md`](../../docs/agent-guides/python-standards.md)
- LLM provider strategy: [`docs/agent-guides/llm-provider-strategy.md`](../../docs/agent-guides/llm-provider-strategy.md)
- TODO management: [`docs/agent-guides/todo-management.md`](../../docs/agent-guides/todo-management.md)
