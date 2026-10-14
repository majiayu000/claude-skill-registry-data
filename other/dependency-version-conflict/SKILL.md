---
name: dependency-version-conflict
description: Debug cascading version incompatibilities across package dependency chains.
---

# Dependency Version Conflict Skill

## Problem it solves

Package managers report metadata-level compatibility, but the real conflict is inside the wheel/jar/artifact. A package declares `protobuf>=3.20` but its generated `_pb2.py` imports `google.protobuf.internal.builder` which may not exist in older versions. Pip says "all satisfied" while the runtime crashes with `ImportError`. These cascading chains are the hardest dependency bugs to diagnose because each package looks fine in isolation.

## Detection triggers

Activate when:
- `ImportError` or `ModuleNotFoundError` for a submodule that should exist in the installed version
- Package A works alone but breaks when package B is also installed
- Version pins conflict: A requires `<3.21` but B requires `>=4.0`
- "Works on my machine" but fails in CI or a different Python/Node/Go version
- Downgrading one package fixes another but breaks a third

## Protocol

### 1. Download and inspect the actual artifact

Do not trust package metadata. Download the wheel/zip and check its contents:
```bash
# Python — list wheel contents
pip download <package>==<version> --no-deps -d ./tmp-wheel
unzip -l ./tmp-wheel/<package>-<version>-*.whl | grep <path-you-expect>

# Node — check what a package actually ships
npm pack <package>@<version> --dry-run

# Go — verify module contents
go list -m -json <module>@<version>
```

Look for the specific file/submodule the error mentions. If it's missing from the wheel, the pin is wrong regardless of what metadata says.

### 2. Map the full conflict chain

Draw the dependency graph for the conflicting packages:
```
mediapipe 0.10.9 → protobuf >=3.20, <4
tensorflow 2.10  → protobuf >=3.20, <3.21  (declared <3.20 but works with 3.20.3)
streamlit 1.22   → protobuf >=3.20
```

Find the intersection of all constraints. If no version satisfies all of them, the combo is incompatible.

### 3. Pin the combo as a unit

Never pin packages individually when they form a conflict chain. Pin the working combination:
```
# BAD
mediapipe==0.10.9
protobuf>=3.20

# GOOD — this exact combo works on py3.10-win
mediapipe==0.10.9
protobuf==3.20.3
tensorflow==2.10.0
```

Document why the pin exists. Future-you will thank present-you.

### 4. Verify the pin in a clean environment

```bash
python -m venv .test-env
.test-env\Scripts\activate
pip install mediapipe==0.10.9 protobuf==3.20.3 tensorflow==2.10.0
python -c "import mediapipe; import google.protobuf.internal.builder; print('OK')"
```

If the clean install fails, the chain has a hidden dependency you missed.

### 5. Check for submodule double-wrapping

When a helper returns a submodule, don't re-apply the parent name:
```python
# BAD — mp.solutions is already mediapipe.python.solutions
from mediapipe.python import solutions
mp.solutions.pose  # → mediapipe.python.solutions.solutions.pose → AttributeError

# GOOD
solutions = mediapipe.python.solutions
solutions.Pose()  # correct
```

## When NOT to use

- Fabricated packages (use `anti-library-hallucination` instead)
- Single-package version bumps with no chain effects
- Lock file conflicts that are just stale locks (delete and reinstall)

## Cross-references

- **anti-library-hallucination** — Prevents suggesting non-existent packages. Use this skill for real packages with real but incompatible versions.
- **anti-global-install** — Install into project-local environments to isolate version conflicts.
- **uv** — Use `uv` for deterministic Python environment management.

## Lessons learned

Real bugs caught by this skill:
1. mediapipe 0.10.9 + protobuf 3.20.3 + TF 2.10 is the only working combo on py3.10-win — each component looks fine alone but breaks in other combos
2. `pip install` says "all satisfied" while runtime crashes — metadata compatibility ≠ runtime compatibility
3. mediapipe 0.10.31 cp310 wheel ships only the tasks API, no `mp.solutions` — verify wheel contents, not package name
