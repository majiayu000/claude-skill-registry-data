---
name: python
description: Python engineering guidance for type hints, pydantic validation, httpx usage, pytest conventions, pyproject structure, async patterns, and lightweight dependency injection. Use when building or reviewing Python services and libraries.
---

# Python

Prefer typed, explicit Python with validation at boundaries, modern async I/O, and simple seams over framework-heavy indirection.

## When to Activate

- Add or refactor Python modules
- Choose a model type for request or domain data
- Write an outbound HTTP integration
- Add async handlers or background jobs
- Configure pytest, typing, or packaging
- Replace hidden globals with explicit dependencies
- Review Python code for type and validation drift

## Typing and Modeling

| Pattern | Preferred | Avoid |
| --- | --- | --- |
| Public functions | Full parameter and return annotations | Unannotated signatures |
| Collections | `list[str]`, `dict[str, int]` | `List`, `Dict` unless compatibility requires it |
| Optional values | `str | None` | Implicit `None` returns |

| Need | Use |
| --- | --- |
| External input validation | `pydantic.BaseModel` |
| Internal immutable value object | `@dataclass(frozen=True)` |
| Loosely structured mapping shape | `TypedDict` |

## HTTP and Async

BAD

```python
import requests

response = requests.get(url, timeout=30)
```

GOOD

```python
import httpx

async with httpx.AsyncClient(timeout=10.0) as client:
    response = await client.get(url)
```

| Rule | Why |
| --- | --- |
| Use `async` only for real I/O boundaries | Avoid fake async complexity |
| Do not call blocking I/O inside async handlers | Prevent event loop stalls |
| Batch concurrent I/O with `asyncio.TaskGroup` or `gather` where safe | Improve latency deterministically |

## Project Layout and DI

| Section | Purpose |
| --- | --- |
| `[project]` | Metadata and dependencies |
| `[tool.pytest.ini_options]` | Test discovery and markers |
| `[tool.ruff]` or `[tool.black]` | Lint and format configuration |
| `[tool.mypy]` | Type checking configuration |

| Preferred | Avoid |
| --- | --- |
| Pass collaborators through constructors or function parameters | Global singletons hidden inside modules |
| Build objects in a wiring layer | Import-time side effects creating clients |

BAD

```python
def create_user(data):
    return User(**data)
```

GOOD

```python
class CreateUserInput(BaseModel):
    email: EmailStr
    name: str


def create_user(data: CreateUserInput) -> User:
    return User(email=data.email, name=data.name)
```

## Checklist

- [ ] Public functions and methods have type hints
- [ ] Boundary inputs are validated with pydantic where appropriate
- [ ] `httpx` is used for outbound HTTP unless a project standard overrides it
- [ ] Async code avoids blocking calls
- [ ] `pyproject.toml` centralizes tool configuration
- [ ] Data models use `BaseModel`, `dataclass`, or `TypedDict` intentionally
- [ ] Dependencies are injected explicitly
