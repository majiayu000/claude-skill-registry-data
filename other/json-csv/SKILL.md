---
name: json-csv
description: Convert between JSON and CSV. A JSON array of objects becomes a CSV, and a CSV becomes a JSON array of objects. Direction follows the file extensions.
---

# json-csv

Convert tabular data between formats. Direction is chosen automatically from the
input and output extensions.

## How to run

```
python3 <skill_dir>/run.py <input.json> <output.csv>   # JSON array of objects -> CSV
python3 <skill_dir>/run.py <input.csv>  <output.json>  # CSV -> JSON array of objects
```

- Both paths must be in an allowed folder or the **out-box** (write to the out-box).
- JSON input must be an array of objects (a single object is also accepted).

Standard library only. After running, tell the user the saved path.
