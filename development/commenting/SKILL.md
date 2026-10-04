---
name: commenting
description: >-
  v1.0.4 — Use whenever writing or editing Python (or other) functions: every
  function, including authored tests and fixtures, needs a description and
  same-line Parameters and Returns labels. Apply on every coding task.
---

# Function docstrings

Write the complete docstring when creating each function, including the first
regression test. A framework-generated or copied one-line test description
must be expanded before saving it. Passing tests or adding logging does not
complete this separate docstring obligation.

Give every `def`, `async def`, and method a docstring with:

1. A short description.
2. `Parameters:` followed on that line by every parameter and its meaning.
   For a function with no parameters, write `Parameters: none` or
   `Parameters: None`. A trailing period is fine.
3. `Returns:` followed on that line by the return meaning. Use
   `Returns: None` when there is no meaningful return.

A long parameter list may continue on later lines once the `Parameters:`
line has content. Do not use `Args:` or leave either label on a line alone.
`lambda` expressions do not need docstrings.

The same contract applies to agent-authored test code: test methods, fixtures,
setup/teardown methods, and assertion helpers are functions too. A test's short
description alone is insufficient. Include `self` / `cls` in the parameter
meanings when present, and use `Returns: None` for an assertion-only method.
Inspect every changed Python file, including tests, before committing; reviewing
only the program file leaves the test functions unchecked.

Before each code commit, inspect every `def` and method in the changed source,
including helpers added for the latest command. Add all three required
docstring parts in that Feature's commit; recheck after later edits rather than
relying on a previous Feature's docstring review. The README documentation
phase does not replace this code-level check.

Example:

```text
"""Return the updated count.

Parameters: value - amount to add; count - current count.

Returns: the updated count.
"""
```

For an assertion-only instance test, the docstring itself has this shape even
when no logging companion is selected. The uppercase names below are placeholders
for the requested public call and an independently expected result:

```python
def test_requested_behavior(self):
    """Check the requested public behavior.

    Parameters: self - the test instance.
    Returns: None.
    """
    self.assertEqual(PUBLIC_ENTRYPOINT(REQUESTED_INPUT), EXPECTED_RESULT)
```

At the commit gate, enumerate the functions in every changed application and
test file. Check description, parameter meanings and return meaning separately
for each function; a description-only test method is unfinished even when its
assertions and entry/exit prints are correct.
