---
name: python-file-splitter
description: Split large Python files into multiple files organized as a package. Use when user says "split this file", "this file is too big", "break this into multiple files", or similar requests for Python (.py) files.
---

# Python File Splitter

Requires `ast-grep`: `npm install -g @ast-grep/cli`

## Full Workflow

### Phase 1: Parse & Plan

0. If you have not yet read the file in question DO NOT READ IT YET. IT MIGHT BE TOO BIG, WAIT AFTER YOU RUN parse.
1. Copy `scripts/split_module.py` to working directory (using cp)
2. Run parse:
   ```bash
   python split_module.py parse path/to/module.py
   ```
3. Analyze output, apply grouping heuristics (see below)
4. Create `groupings.json`
5. Present proposed structure to user, wait for confirmation
   - **(Mode 1 stops here if user just wants to see the plan)**

### Phase 2: Split & Iterate

6. Run split:
   ```bash
   python split_module.py split path/to/module.py groupings.json package.module Class1 Class2
   ```
7. If imports succeed → done!
8. **If imports fail → rollback happens automatically**, then:
   - **Fix `groupings.json`** (add missing items to `base`, adjust groups)
   - **Re-run step 6**
   - Repeat until imports pass

### The Retry Loop

```
split → test fails → rollback → fix groupings.json → repeat
```

**NEVER edit generated files.** They get deleted on rollback. Only `groupings.json` survives - that's your source of truth.

## CLI Reference

```bash
# Parse: print definitions JSON
python split_module.py parse <file.py>

# Split: write files, test imports, rollback on failure
python split_module.py split <file.py> <groupings.json> <module> <Name1> [Name2 ...]
```

## Groupings JSON format

```json
{
  "base": ["BaseClass", "helper_func"],
  "groups": {
    "group_name": ["ClassA", "ClassAVariant"],
    "other": ["ClassB"]
  },
  "init_extras": ["get_instance", "create_thing"]
}
```

## Grouping heuristics

Apply in order:

1. **Base classes** → `base`: parent is `ABC`/`Protocol`/`BaseModel`, or name contains `Base`/`Mixin`
2. **Inheritance chains** → same group: class + all subclasses that inherit from it
3. **Naming patterns** → same group: `FooRenderer`, `FooVLRenderer`, `FooDisableThinkingRenderer`
4. **Helper functions** → with related class if name matches, else `base`
5. **Factory functions** → `init_extras`: `get_*`, `create_*`, `make_*`, `build_*`

## Output structure

```
module.py      → re-export stub (backwards compat)
module/
├── __init__.py   # re-exports + factory functions
├── base.py       # imports + base classes + shared utils
└── <group>.py    # from .base import * + group members
```

## FAQ

**Q: Imports failed. Can I just edit base.py to fix it?**
A: No. Rollback deletes generated files. Edit `groupings.json` instead, then re-run. That's the whole point of the retry loop.

**Q: Why does rollback exist?**
A: It protects you. Failed state = broken code in the repo. Rollback restores clean state so you can iterate on `groupings.json` safely.

**Q: cmd_parse didn't capture something (type aliases, constants, etc). What do I do?**
A: This will happen. When imports fail, read the error, figure out what's missing, and either add it to `base` in groupings.json or fix the script's `parse_definitions()` if it's a pattern you'll hit often.

**Q: What if I need to edit split_module.py to capture new patterns?**
A: Prefer using `ast-grep` patterns over regex. The script already uses `run_ast_grep()` for classes and functions. Add new patterns following the existing style (see `parse_definitions()`).