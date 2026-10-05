---
name: python
description: Apply when writing Python code. Type hints, error handling, mutable defaults, async patterns, and packaging conventions.
license: MIT
version: 1.1.0
tokens_target: 2900
triggers:
  - python code
  - type hints
  - python packaging
loads_after:
  - code-quality
supersedes: []
---

# Sub-Skill: Python Best Practices
<!-- target: ~2200 tokens (real tiktoken count) | 20 rules with severity classification -->

**Purpose:** Prevents the Python-specific mistakes LLMs make on autopilot — mutable defaults, bare excepts, missing guards, and subtle performance traps that pass review but break in production.

## Rule classification

- **MUST** — load-bearing. Violating causes bugs, security issues, or invisible failures. Never break.
- **SHOULD** — default behavior. Deviation needs a documented reason in the code or PR.
- **AVOID** — usually wrong; documented exception inline where needed.

**Where these rules don't strictly apply:** test fixtures, generated code, throwaway scripts, REPL exploration, and tutorial snippets may legitimately differ. The rules below apply to **production code paths and reusable libraries**.

---

## Rules

### Type Hints

1. **SHOULD: Annotate function signatures with types.** `def process(data)` tells callers nothing. Use `def process(data: list[str]) -> dict[str, int]:`. Return type `None` should be explicit too. *Exception: lambdas and short generator helpers in private scope.*

2. **SHOULD: Use built-in lowercase generics for Python 3.9+.** `list[str]`, `dict[str, int]`, `tuple[int, ...]` rather than `List`, `Dict`, `Tuple` from `typing`.

3. **MUST: Use `Optional[X]` or `X | None` for nullable parameters, never a bare default of `None` without a type annotation.** `def find(id: int) -> User | None:` not `def find(id):`.

4. **AVOID: `Any` as a shortcut.** If the type is genuinely unknown, document why with a comment. `Any` silences the type checker and hides bugs. *Exception: third-party libraries without stubs and explicit dynamic-data boundaries (e.g. JSON decode at the API edge).*

---

### Error Handling

5. **MUST: Never use bare `except:`.** It catches `SystemExit`, `KeyboardInterrupt`, and `GeneratorExit`. Always catch `except Exception:` at minimum, or a specific exception class.

   ```python
   # Wrong
   try:
       risky()
   except:
       pass

   # Correct
   try:
       risky()
   except ValueError as e:
       logger.warning("Invalid value: %s", e)
   ```

6. **MUST: Never silently swallow exceptions with `pass`.** At minimum log the error. Silent failures produce ghost bugs that are impossible to trace.

7. **SHOULD: Raise with context when re-raising.** Use `raise NewError("msg") from original_error` to preserve the traceback chain, not `raise NewError("msg")` alone.

---

### Common Pitfalls

8. **MUST: Never use mutable default arguments.** Python evaluates defaults once at function definition, not per call. The list or dict is shared across all calls.

   ```python
   # Wrong — items accumulates across calls
   def append_item(val, items=[]):
       items.append(val)
       return items

   # Correct
   def append_item(val, items=None):
       if items is None:
           items = []
       items.append(val)
       return items
   ```

9. **MUST: Guard script entry points with `if __name__ == "__main__":`.** Without it, importing the module executes top-level code, breaking tests and imports.

10. **MUST: Use `with` for file handles, sockets, and locks.** Never open a file without a context manager. `f = open(...)` without `with` leaks handles on exceptions.

    ```python
    # Wrong
    f = open("data.txt")
    data = f.read()
    f.close()

    # Correct
    with open("data.txt") as f:
        data = f.read()
    ```

11. **AVOID: String concatenation in loops.** Each `+=` on a string creates a new object. Collect into a list and call `"".join(parts)` at the end.

    ```python
    # Wrong — O(n^2) memory
    result = ""
    for word in words:
        result += word + " "

    # Correct
    result = " ".join(words)
    ```

12. **SHOULD: Use f-strings for string interpolation in Python 3.6+.** Avoid `%` formatting or `"Hello " + name`. F-strings are faster, safer, and readable.

    ```python
    # Avoid
    msg = "User %s has %d items" % (name, count)

    # Prefer
    msg = f"User {name} has {count} items"
    ```

13. **AVOID: `dict()` constructor when a literal suffices.** `{}` is faster and more idiomatic. `dict(key=value)` is only justified when keys are dynamic or come from variables.

---

### Performance

14. **SHOULD: Use list comprehensions or generator expressions instead of `map`/`filter` with `lambda`.** Comprehensions are more readable and equally fast. Use generators when the full list is not needed at once.

    ```python
    # Avoid
    result = list(map(lambda x: x * 2, items))

    # Prefer
    result = [x * 2 for x in items]

    # For large data, use a generator
    total = sum(x * 2 for x in items)
    ```

15. **SHOULD: Use a `set` for membership lookups, not a `list`.** `x in list` is O(n). `x in set` is O(1). Convert once, query many times.

    ```python
    # Wrong for repeated lookups
    valid_ids = [1, 2, 3, ...]
    if user_id in valid_ids:  # O(n) every call

    # Correct
    valid_ids = {1, 2, 3, ...}
    if user_id in valid_ids:  # O(1)
    ```

---

### Testing

16. **SHOULD: Name test functions to describe the scenario, not just the function under test.** `test_process_returns_empty_dict_on_empty_input` not `test_process`.

17. **MUST: Never use `assert` statements in production code for validation.** `assert` is stripped with `python -O`. Use explicit `if` checks with `raise ValueError(...)` for runtime validation.

18. **MUST: Use `pytest.raises` as a context manager to assert exceptions, never wrap in try/except inside a test.** A bare try/except can mask a missing exception.

    ```python
    # Wrong
    def test_bad_input():
        try:
            process(None)
        except ValueError:
            pass  # test passes even if no exception is raised

    # Correct
    def test_bad_input():
        with pytest.raises(ValueError, match="input cannot be None"):
            process(None)
    ```

19. **SHOULD: Use `@pytest.mark.parametrize` to test the same logic with multiple inputs.** Write one parameterized test instead of duplicating test functions for each case.

20. **SHOULD: Place shared fixtures in `conftest.py` at the nearest common ancestor directory.** Do not scatter fixtures across individual test files. Pytest auto-discovers `conftest.py` at every level.

21. **MUST: Never return mutable objects directly from a pytest fixture.** Each test must receive a fresh instance. Use factory fixtures that return a callable creating fresh objects. Reference: ERR-2026-014.

22. **AVOID: Fixtures with side effects (network, DB) without explicit scope.** Use `scope="session"` or `scope="module"` for expensive shared resources with proper teardown via `yield`.

23. **SHOULD: Use the `tmp_path` fixture for filesystem tests instead of manual temporary directories.** It auto-cleans and is process-safe.

---

### Packaging

24. **SHOULD: Include `__init__.py` in every package directory.** Without it, Python 3 treats the directory as a namespace package, which breaks relative imports and tool discovery in many environments. *Exception: explicit namespace packages (PEP 420) where the omission is documented intent.*

25. **AVOID: Imports from `__init__.py` inside the same package's submodules.** This creates circular imports. Keep `__init__.py` as a re-export surface only, not a logic file.

26. **SHOULD: Use `pyproject.toml` as the single source of project metadata.** Avoid `setup.py` and `setup.cfg` for new projects. Modern tooling (pip, build, hatch, uv) all read `pyproject.toml` natively.

27. **MUST: Pin exact versions in lock files but use ranges in `pyproject.toml` dependencies.** Lock files (`uv.lock`, `poetry.lock`) ensure reproducibility; flexible ranges in project metadata allow resolver to find compatible versions.

28. **SHOULD: Define CLI entry points in `[project.scripts]` instead of relying on `python -m` patterns.** Entry points generate proper executables and integrate with system PATH.

---

## Why This Sub-Skill Earns Stars

These rules target the exact failure modes that appear in LLM-generated Python:

- Mutable defaults and missing `__main__` guards are invisible bugs that only surface at runtime.
- Bare `except:` and silent `pass` blocks make debugging take 10x longer.
- String concatenation in loops and list membership checks are performance traps that scale badly.
- Missing type annotations and `Any` shortcuts defeat the entire value of static analysis.
- Skipping `with` for file handles causes resource leaks under load.

None of these are caught by syntax checkers. All of them appear in production incidents. The MUST/SHOULD/AVOID classification means the security/correctness rules are strict and the stylistic rules respect context.
