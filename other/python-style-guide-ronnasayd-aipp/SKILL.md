---
name: python-style-guide
description: "Coding conventions and best practices for Python based on the Google Python Style Guide, emphasizing readability, explicitness, consistent naming, clear docstrings, safe exception handling, small focused functions, and static typing for writing maintainable production-quality Python code."
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Skill: Python (Google Style Guide)

## Overview

This skill implements conventions from the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html). The primary goal is to produce Python code that is readable, maintainable, and consistent across large codebases by following established patterns and avoiding common pitfalls.

---

# 1. Language Rules

### Linting

- **Mandatory Tooling:** Use `pylint` to catch errors and style issues.
- **Suppression:** Suppress warnings only when necessary and justified (e.g., `pylint: disable=no-member`).

### Imports

- **Packages & Modules:** Prefer `import x` for packages and modules.
- **Specific Items:** Use `from x import y` only when `y` is a module, or for items from `typing` and similar core libraries.
- **No Wildcards:** Never use `from module import *`.
- **Order:**
  1. Standard library imports.
  2. Third-party library imports.
  3. Local application imports.

### Exceptions

- **Specific Catch:** Never use catch-all `except:` or `except Exception:`. Catch specific exceptions.
- **Try Block Size:** Minimize the amount of code inside a `try` block.
- **Custom Exceptions:** Inherit from `Exception` (or a more specific built-in) and end the name with `Error`.

### Global State

- **Avoid Mutability:** Avoid mutable global variables.
- **Internal Only:** If global state is necessary, prefix with an underscore (`_`) and access via public functions.

### Functions & Power Features

- **Length:** Prefer small, focused functions. Reconsider logic if a function exceeds ~40 lines.
- **Complexity:** Avoid complex "power" features like metaclasses, bytecode access, or dynamic inheritance unless absolutely necessary for infrastructure.
- **Lambda:** Use only for simple, one-line expressions. Use named functions for anything complex.

### Default Arguments

- **No Mutable Defaults:** Never use mutable objects (e.g., `[]`, `{}`) as default values.
- **Correct Pattern:** Use `None` as the default and initialize inside the function.
  ```python
  def process_items(items=None):
      if items is None:
          items = []
  ```

---

# 2. Style Rules

### Layout & Formatting

- **Line Length:** Maximum of **80 characters**. Use implicit line joining (parentheses) instead of backslashes.
- **Indentation:** Use **4 spaces** per level. No tabs.
- **Blank Lines:**
  - Two blank lines between top-level definitions (classes, functions).
  - One blank line between method definitions within a class.

### Whitespace

- **Operators:** Surround binary operators (`=`, `==`, `<`, `+`, `-`, etc.) with a single space.
- **Keyword Args:** No spaces around `=` for keyword arguments or default values, _unless_ there is a type hint.
  ```python
  def func(param: int = 5):  # Space allowed with type hint
  def func(param=5):        # No spaces without type hint
  ```
- **Grouping:** No whitespace inside parentheses, brackets, or braces.

### Naming Conventions

| Entity                  | Style                 | Example             |
| :---------------------- | :-------------------- | :------------------ |
| **Modules / Packages**  | `lower_with_under`    | `user_service.py`   |
| **Classes**             | `CapWords`            | `UserManager`       |
| **Exceptions**          | `CapWords`            | `ValidationError`   |
| **Functions / Methods** | `lower_with_under`    | `fetch_data()`      |
| **Variables / Params**  | `lower_with_under`    | `user_id`           |
| **Constants**           | `CAPS_WITH_UNDER`     | `MAX_RETRIES`       |
| **Internal Members**    | `_leading_underscore` | `_private_helper()` |

### Docstrings

Mandatory for public APIs, classes, and non-trivial functions. Use `"""triple double quotes"""`.

```python
def function(arg1: int, arg2: str) -> bool:
    """Summary line of the function.

    Detailed explanation if necessary.

    Args:
        arg1: Description of arg1.
        arg2: Description of arg2.

    Returns:
        Description of the return value.

    Raises:
        ValueError: When arg1 is negative.
    """
```

---

# 3. Modern Python & Typing

### Type Annotations

- **Public APIs:** Strongly encouraged for all public function signatures.
- **Readability:** Use type hints to improve clarity and enable static analysis with tools like `mypy`.

  ```python
  from typing import List, Optional

  def get_users(query: str) -> List[User]:
      ...
  ```

---

# 4. Main Entry Point

Executable modules must always use a `main()` function and the `if __name__ == '__main__':` guard.

```python
def main():
    # Application logic here
    pass

if __name__ == '__main__':
    main()
```

---

# Key Principles

1. **Readability First:** If the rule makes the code less readable, follow common sense.
2. **Explicitness:** Be explicit in imports and behavior.
3. **Consistency:** Match the style of the existing file/project if it differs slightly but is consistent.
4. **Defensive Programming:** Use static typing and robust error handling.
