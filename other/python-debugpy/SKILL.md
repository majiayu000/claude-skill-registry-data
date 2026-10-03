---
name: python-debugpy
description: "Debug Python: pdb REPL + debugpy remote (DAP)."
allowed-tools:
  - bash
  - read_file
enabled: true
related-skills: [systematic-debugging, node-inspect-debugger]
license: MIT
author: Adapted from hermes-agent (Nous Research, MIT)
---

# Python Debugger (pdb + debugpy)

## Overview

Three tools, picked by situation:

| Tool | When |
|---|---|
| **`breakpoint()` + pdb** | Local, interactive, simplest. Add `breakpoint()` in source, run, get REPL. |
| **`python -m pdb`** | Launch script under pdb with no source edits. |
| **`debugpy`** | Remote / headless / attach to running process. DAP, scriptable. |

**Start with `breakpoint()`.** It's the cheapest thing that works.

## When to Use

- A test fails and the traceback doesn't reveal why a value is wrong
- You need to step through a function and watch a collection mutate
- A long-running process misbehaves and you can't restart it
- Post-mortem: an exception fired and you want to inspect locals at crash site
- A subprocess is the actual bug site

**Don't use for:** things `print()` / `logging.debug` solve in under a minute,
or things `pytest -vv --tb=long --showlocals` already reveals.

## pdb Quick Reference

Inside any pdb prompt (`(Pdb)`):

| Command | Action |
|---|---|
| `h` / `h cmd` | help |
| `n` | next line (step over) |
| `s` | step into |
| `r` | return from current function |
| `c` | continue |
| `unt N` | continue until line N |
| `j N` | jump to line N (same function only) |
| `b N` | set breakpoint at line N |
| `b file:N` | set breakpoint in another file |
| `b func` | set breakpoint at function |
| `cl N` | clear breakpoint N |
| `l` | list 11 lines around current |
| `ll` | list whole function |
| `w` / `where` | show call stack |
| `u` / `d` | move up/down stack frame |
| `p expr` | print expression |
| `pp expr` | pretty-print expression |
| `a` | print args of current function |
| `args` | same as `a` |
| `display expr` | watch expression (re-eval each step) |
| `interact` | drop into interactive Python REPL |

## Using `breakpoint()`

```python
def process(data):
    result = transform(data)
    breakpoint()  # Execution pauses here, pdb REPL opens
    return result
```

Run normally:
```bash
python script.py
# Pauses at breakpoint(), (Pdb) prompt appears
```

## Using `python -m pdb` (no source edits)

```bash
python -m pdb script.py
# Starts paused at first line
```

## Post-mortem debugging

Drop into pdb at the exact exception site:

```python
import pdb, traceback
try:
    main()
except Exception:
    traceback.print_exc()
    pdb.post_mortem()
```

Or:
```bash
python -m pdb -c continue script.py
# Runs until exception, then drops to pdb at the crash
```

## debugpy (remote attach)

For long-running processes or headless debugging:

```bash
# Install
pip install debugpy

# Option 1: Launch with debugpy
python -m debugpy --listen 5678 --wait-for-client script.py

# Option 2: Inject into running code
import debugpy
debugpy.listen(5678)
print("Waiting for debugger on port 5678...")
debugpy.wait_for_client()
```

Attach from another terminal (DAP client):
```bash
# Using debugpy's CLI to set breakpoints + continue
python -m debugpy --connect localhost:5678 --set-breakpoint script.py:42
```

Or use any DAP-compatible editor (VS Code, Neovim) to attach to port 5678.

## Common Debugging Patterns

### Watch a variable change

```python
# In pdb
(Pdb) display my_list
# Each step, pdb re-evaluates and shows the value if changed
```

### Conditional breakpoint

```python
# In source
breakpoint() if condition else None

# Or in pdb
(Pdb) b 42, x > 100  # Break at line 42 only when x > 100
```

### Inspect a running subprocess

```python
import debugpy
# In the subprocess code:
debugpy.listen(5679)
debugpy.wait_for_client()
# Parent can attach to port 5679
```

## Pitfalls

- **breakpoint() in production**: remove before commit. Use `breakpoint()` only
  for local debugging.
- **pdb + multiprocessing**: child processes don't inherit the pdb prompt.
  Use `debugpy` for multi-process debugging.
- **pdb + asyncio**: pdb works but async stack traces can be confusing. Use
  `w` (where) to see the full async call stack.
- **Windows + pdb**: some pdb features work differently on Windows. `python -m
  pdb` is more reliable than `breakpoint()` in some Windows terminals.
- **debugpy port conflicts**: default port 5678 may be taken. Use
  `--listen 5679`.
