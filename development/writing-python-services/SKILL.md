---
name: Writing python services
description: Writing a class with encapsulated logic that interfaces with an external system. Logging, APIs, etc.
---

- Use python 3.12+ syntax for types
  - e.g. `|` for unions, ` | None` for optional

- No side effects in constructor
  - Use `@cached_property` and lazily evaluate properties needing IO

- Methods use `dataclasses` for arguments and responses

