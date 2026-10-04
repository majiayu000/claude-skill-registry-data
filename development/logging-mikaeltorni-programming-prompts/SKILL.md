---
name: logging
description: >-
  v1.0.6 — Trace every authored function, including tests and fixtures: print its
  incoming parameters at entry and return value just before returning.
  Keep it to plain print() — no logging modules or log files.
---

# Function entry/exit print logging

**Every** `def` / `async def` / method you write or edit gets an entry print
and an exit print. No function is exempt — not private `_helpers`, not
one-line functions, not the thin public entrypoint, not constructors or other
special methods, not functions with no parameters. Only `lambda` expressions
are exempt.

**A constructor receives `self` even when called with no explicit arguments.**
Write its entry trace before initializing fields and its exit trace after them:

```python
class Store:
    def __init__(self):
        """Create an empty store.

        Parameters: self - the instance being initialized.

        Returns: None.
        """
        print(f"self={object.__repr__(self)}")
        self.items = []
        print(None)
```

`print("parameters=none")` is invalid in this constructor. Determine parameter
names from the `def` signature, never from the call site or a docstring that
says "Parameters: none". An uninitialized instance still has an identity;
`object.__repr__(self)` prints it without reading fields or invoking a custom
representation.

1. **Entry print — the first statement in the body.** `print` **every**
   incoming parameter's **actual name** and value, including optional
   parameters whose value is `None` and method receivers `self` / `cls`;
   one print listing every real name is enough. "First statement" is literal:
   no parse call, validation, `global`, or dispatch runs before it. Python
   permits a `global` declaration after a parameter-only entry print; put
   the declaration there, before reading or assigning that global. Keep a
   docstring first when present, with the print directly after it.

   ```python
   def update(value):
       """Replace stored state.

       Parameters: value - the new state.

       Returns: the stored state.
       """
       print(f"value={value}")        # first statement after the docstring
       global stored_state           # declaration comes after the print
       stored_state = value
       print(stored_state)
       return stored_state
   ```

   Failures: printing only after `parsed = _parse_command(command)`; omitting
   a named parameter because it is unused or `None`; a generic label
   (`input=`, `args=`, `params=`) or one unlabeled tuple standing in for the
   real names. A helper that prints `command=` does not cover the entrypoint —
   every function prints its own parameters. Only a signature with **zero
   parameters**, such as `def ready()`, permits `print("entry")` or
   `print("parameters=none")`. `def size(self)` has one parameter and must
   print `self=`; `def update(self, value)` must print both `self=` and
   `value=`. Class methods likewise print `cls=`. Use `object.__repr__(self)`
   when tracing the receiver could call a traced `__repr__` / `__str__`
   recursively.
2. **Exit print — just before each `return`** (or before falling off the end
   with an implicit `None`), `print` the value about to leave the function.
   `print(result)` is enough; a `return=` label is not required. Print
   **everything** the `return` hands back: for `return result, []` the value
   is the whole tuple, so write `print(result, [])`. Every `return` gets its
   own exit print, including an early or empty-input branch.
   This includes constructors (`__init__`) and validation helpers: if they
   finish normally without a return statement, end with `print(None)`.
   A path ending in an explicit return has no additional implicit exit.
   A helper's exit print does not cover its caller: before `return helper()`,
   assign the helper result, print that result in the caller, and return it.
   Check every dispatch branch, including branches with direct helper returns.

Apply this rule to agent-authored tests as well as application code. Test methods,
fixtures, setup/teardown methods, and assertion helpers have their own entries
and normal exits. An assertion-only test method still receives `self` and
normally returns `None`: print `self=` first and `None` after its final assertion.
Calling a traced application function does not trace the test method itself.
Redirecting stdout inside a test does not waive its first-statement entry print;
place that print before opening the redirect. Review every changed Python file,
including tests, before each commit.

Before committing, inspect source order in every function: the first
non-docstring statement must be its parameter print. A successful runtime
trace does not excuse a preceding `global` declaration. Compare each
signature with that first print and inspect every normal exit, including
early returns. Check object construction in a smoke run so the constructor's
`self=` and final `None` are observed.

Nothing is required before a `raise` / exception exit — only normal return
paths. Use the built-in `print(...)` only: no log files, no `logging` import,
no custom logger helper.
