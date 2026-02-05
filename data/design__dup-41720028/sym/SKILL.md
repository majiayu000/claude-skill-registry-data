---
name: sym
description: List Python symbols (classes/functions) quickly via AST to discover real identifiers before using `def`/`ctx`.
---

# sym

## Use this skill when
- You need candidate symbol names fast (avoid guessing / placeholder names).
- You want a compact index of classes/functions in a package.

## Commands

```sh
# List top-level symbols under a directory (fast)
sym .

# Focus on a package / subdir
sym mypkg

# Include class methods (more output)
sym mypkg --include-methods

# Filter by name and kind
sym mypkg --query trainer --kind class

# Filter classes by base class (e.g. nn.Module)
sym mypkg --base nn.Module --kind class

# Filter by decorator (e.g. dataclasses.dataclass / dataclass)
sym mypkg --decorator dataclass --kind class

# Include nested defs (rarely needed)
sym mypkg --include-nested --query inner

# If you filter for methods, methods are automatically included
sym mypkg --query __init__ --kind method

# Output JSON (for tooling)
sym mypkg --json

# (fallback if wrappers are not on PATH)
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
python3 "$CODEX_HOME/skills/sym/scripts/sym.py" mypkg
```

## Notes
- AST-based: precise (low false positives) for Python.
- Bounded: respects `--max-files`, `--max-results`, and `--max-file-bytes`.
