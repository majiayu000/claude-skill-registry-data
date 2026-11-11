---
description: Identify and replace Python code with code in the `helpers` package
model: haiku
---

# Goal
Given Python source files `<FILES>`, find functions that `helpers` can replace.

# Workflow
- The most important packages are:
  - `helpers/hdbg.py`
    - Debugging utilities with specialized assertions, logging, and fatal error
      handling
  - `helpers/hio.py`
    - Filesystem operations, file read/write, and directory management utilities
  - `helpers/hsystem.py`
    - System interaction: shell commands, environment variables, process
      management
- Do not change the behavior of the code

# Verification
- [ ] Confirm replaced calls preserve the original behavior
- [ ] Run the file's unit tests to confirm nothing broke
