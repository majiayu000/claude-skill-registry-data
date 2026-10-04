---
name: python-code-documentation-guidelines
description: Apply Google-style docstrings and inline comments to Python .py files. Use when documenting new functions/classes/modules, incrementally documenting touched code, or flagging rename opportunities as TODOs.
license: MIT
compatibility: claude cursor opencode
metadata:
  version: "1.0.0"
  languages: python
  audience: developers
  workflow: docs
  since: "2026-03-04"
---

# Doc Code Inline

Apply consistent Python documentation conventions: docstrings, class-level docs, and inline comments so code stays clear and maintainable.

## When to run this skill

- You are adding or updating docstrings for new or existing Python functions, classes, or modules in .py files.
- You are touching existing Python code and want to document it step-by-step (incremental docs).
- You spot function, class, or variable names that would benefit from renames and need to record a tracked task in the code.

## Steps

1. **Docstring format (Python only)**
   - Use **Google-style** docstrings in .py files.
   - Include a summary line, then `Args:`, `Returns:`, and `Raises:` with types in parentheses where relevant.
   - Example:

   ```python
   def fetch_user(user_id: str) -> User:
       """Load a user by ID from the backing store.

       Args:
           user_id (str): Unique identifier for the user.

       Returns:
           User: The user instance, if found.

       Raises:
           NotFoundError: When no user exists for the given ID.
       """
   ```

   For modules, add a top-of-file docstring describing the module's purpose:

   ```python
   """Utilities for loading and caching user records."""
   ```

2. **Class docstrings**
   - In .py files, add a class-level docstring that describes the **class’s responsibility** (what it does), not just the class name.
   - Avoid docstrings that only repeat the class name.

3. **Comments and single-line docstrings**
   - Prefer self-documenting names; avoid superfluous comments when names make the code clear.
   - When a docstring is needed, a single-line docstring is fine as long as it adds information—not one that mostly repeats the function name.

4. **Renames and TODOs**
   - When you spot function/class/variable renames that would make code clearer, add a `# TODO` in the .py file and reference ticket **UN-17829** (e.g. `# TODO(UN-17829): rename to get_active_sessions`).
   - No mandate to flag every possible rename — use judgment for names that genuinely mislead.

## Checklist

- [ ] New or updated docstrings in .py files use Google-style (summary, Args/Returns/Raises with types in parentheses).
- [ ] Class docstrings in .py files describe the class’s responsibility, not just the name.
- [ ] Comments and docstrings add information; avoid repeating names or obvious behavior.
- [ ] Misleading names are flagged as `# TODO(UN-17829): rename to …` where appropriate.
- [ ] New Python code is documented; existing .py code gets incremental docs when you touch it.
