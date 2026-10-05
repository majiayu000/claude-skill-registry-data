---
name: python-quality-review
description: Python-specific code review focusing on idiomatic patterns, type hints, async correctness, and Python best practices. Use for reviewing Python code, ensuring Pythonic patterns, catching Python-specific pitfalls, and maintaining Python code quality.
---

# Python Quality Review

Review Python code for idiomatic patterns, correctness, and best practices.

## Python-Specific Checks

### Type Hints
```python
# Missing type hints
def process(data):
    return data.get('value')

# With type hints
def process(data: dict[str, Any]) -> str | None:
    return data.get('value')
```

### Mutable Default Arguments
```python
# Bug: Mutable default (shared across calls)
def append_to(item, target=[]):
    target.append(item)
    return target

# Fixed: Use None default
def append_to(item, target: list | None = None):
    if target is None:
        target = []
    target.append(item)
    return target
```

### Exception Handling
```python
# Too broad
try:
    result = process(data)
except Exception:
    pass  # Silently swallows all errors

# Better: Specific exceptions
try:
    result = process(data)
except ValidationError as e:
    logger.warning(f"Validation failed: {e}")
    return None
except ConnectionError as e:
    logger.error(f"Connection failed: {e}")
    raise
```

## Pythonic Patterns

### Use Comprehensions
```python
# Non-Pythonic
result = []
for item in items:
    if item.is_valid:
        result.append(item.value)

# Pythonic
result = [item.value for item in items if item.is_valid]
```

### Use Context Managers
```python
# Bad: Manual resource management
f = open('file.txt')
try:
    data = f.read()
finally:
    f.close()

# Good: Context manager
with open('file.txt') as f:
    data = f.read()
```

### Use Unpacking
```python
# Verbose
first = items[0]
second = items[1]
rest = items[2:]

# Pythonic
first, second, *rest = items
```

### Use enumerate/zip
```python
# Index tracking manually
i = 0
for item in items:
    print(f"{i}: {item}")
    i += 1

# Use enumerate
for i, item in enumerate(items):
    print(f"{i}: {item}")
```

## Async/Await Issues

### Blocking in Async
```python
# Bug: Blocking call in async function
async def fetch_data():
    response = requests.get(url)  # Blocks the event loop!
    return response.json()

# Fixed: Use async library
async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

### Missing Await
```python
# Bug: Coroutine never awaited
async def process():
    fetch_data()  # Returns coroutine, doesn't execute!

# Fixed
async def process():
    await fetch_data()
```

### Concurrent Execution
```python
# Sequential (slow)
async def fetch_all(urls):
    results = []
    for url in urls:
        results.append(await fetch(url))
    return results

# Concurrent (fast)
async def fetch_all(urls):
    return await asyncio.gather(*[fetch(url) for url in urls])
```

## Performance Patterns

### String Concatenation
```python
# Slow: String concatenation in loop
result = ""
for item in items:
    result += str(item)

# Fast: Join
result = "".join(str(item) for item in items)
```

### Generator vs List
```python
# Memory heavy: Creates full list
def get_values(items):
    return [expensive_compute(item) for item in items]

# Memory efficient: Generator
def get_values(items):
    return (expensive_compute(item) for item in items)
```

### Dict/Set for Lookups
```python
# Slow: O(n) lookup
if item in large_list:
    ...

# Fast: O(1) lookup
large_set = set(large_list)
if item in large_set:
    ...
```

## Review Checklist

### Correctness
- [ ] No mutable default arguments
- [ ] Exceptions caught specifically (not bare except)
- [ ] Resources properly closed (context managers)
- [ ] Async/await used correctly

### Style
- [ ] Type hints on public functions
- [ ] Docstrings on public functions
- [ ] Comprehensions where appropriate
- [ ] Pythonic idioms used

### Performance
- [ ] No O(n²) operations in loops
- [ ] Generators for large sequences
- [ ] Set/dict for membership testing
- [ ] No blocking calls in async code

## Review Output Format

```markdown
## Python Review: [File Name]

### Type Safety
- [ ] Type hints complete
- [ ] Types are accurate
- [ ] Optional types handled

### Python Issues
- **Line X**: [Issue description]
  ```python
  # Current
  problematic_code()

  # Suggested
  better_code()
  ```

### Async Issues
- [List any async/await problems]

### Performance Concerns
- [List any performance issues]
```
