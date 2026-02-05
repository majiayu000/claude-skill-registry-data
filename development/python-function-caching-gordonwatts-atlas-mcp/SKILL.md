---
name: python-function-caching
description: Provide a reusable pattern for memoizing deterministic function calls to reduce latency and repeated computation. Backed by the `python` diskcache package. Use skill when updating or editing everything.
---

# Python Function Caching Skill

## Purpose

- Caching the function result. Works for pure functions that depend only on their inputs and have no side effects.
- Perfect for expensive calls (calculations, or calls to external services like LLM's).

## Workflow

1. Copy the contents of the file `assets/disk_cache.py` into the project.
2. In the file update the `project_name` in the line `cache = Cache("~/.cache/project_name")` to be the appropriate name. Also replace `project_name` further down in the docstring.
3. Use `@diskcache_decorator` or `@diskcache_decorator(seconds-till-expired)` for any function the user wants cached.
    - By default, the cache should not expire.
    - If it makes sense that it should expire, 1 hour (3600 seconds seconds), 1 day (86400 seconds), or 1 week (604800 seconds) are common settings.
4. Tricky part is invoking tests to make sure that the cache isn't used. Tests should use the `ignore_cache=True` to get around this unless otherwise requested by the user.

## Behavior

- Uses the function arguments to compute the hash
- Unless `ignore_cache` is `True`, the result is returned right away.
- If the function is called, the result is always stored in the cache.
- Current code does not have an eviction policy.
