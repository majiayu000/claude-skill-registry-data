---
name: uv-script-deps
description: Run Python scripts with inline dependencies using uv and PEP 723.
---

# uv Script Dependencies

Declare dependencies inside single-file scripts. No requirements.txt, no manual venv.

## Pattern

```python
# /// script
# dependencies = ["requests", "pandas>=2.0"]
# requires-python = ">=3.11"
# ///

import requests
import pandas as pd
```

```bash
uv run script.py
```

uv creates an ephemeral venv, installs deps, runs the script, caches for next time.

## Options

```bash
uv run script.py                      # use inline deps
uv run --python 3.12 script.py        # specific interpreter
uv run --with httpx script.py         # add dep at runtime
```

