---
name: def
description: Locate symbol definitions quickly (precise for Python via AST; conservative candidates for other languages) and print a bounded context packet.
---

# def

## Use this skill when
- You need definition locations for a symbol without opening files manually.
- You want minimal, high-signal context for review or refactor work.

## Commands

```sh
# Auto (tries Python-precise, then other languages as candidates)
def MyClass .

# Prefer Python precision and include a small snippet
def MyClass . --lang py -C 2

# Methods / dotted qualnames (Python): find `Class.method`
def MyClass.__init__ mypkg --lang py -C 1

# Bias path ranking if you know where code likely lives
def MyClass . --prefer torch --prefer aten
```

## Notes
- Python results are AST-validated (low false positives).
- Non-Python results are heuristic candidates; use `ctx` to confirm if ambiguous.
