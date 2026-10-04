---
name: greyscript-linter
description: Static-Analyse für GreyScript-Quellen VOR greybel-Build. Erkennt fehlende //command-Marker, nicht-erlaubte Builtins (run, is_folder, str_repeat u.a.) und gibt klare Fehler/Warnings aus. Trigger bei jedem neuen Build und als Pre-Commit-Hook.
version: 1.0.0
author: OpenClaw Agent (MaxClaw Skill-Set)
license: MIT
platforms:
  - linux
  - macos
  - windows
triggers:
  - pre-build: vor jedem `greybel build`
  - pre-commit: vor `git commit` mit .src-Änderungen
  - manual: "lint-greyscript.py file.src"
metadata:
  openclaw:
    tags:
      - code
      - greyscript
      - static-analysis
      - greyhack
---

# greyscript-linter

GreyScript hat kein offizielles Lint-Tool — `greybel build` gibt erst nach
kompletter Transpilierung Fehler aus, oft kryptisch ("Line 0"). Dieser Linter
fängt die **typischen Footguns** vorher ab.

## When to use

- Vor jedem `greybel build` aus GreyHack-Tool-Workflows.
- Als Pre-Commit-Hook in Tool-Repos.
- Beim Übernahme alter Scripts in den Sandbox-Build (`scan-greyscript.sh`).

## Disallowed Builtins (greybel-js Whitelist-Gap)

Diese Builtins existieren in GreyScript-Specs, aber `greybel-js` lehnt sie
zur Build-Zeit ab → Build-Fehler ohne klare Position:

| Builtin        | Workaround                                        |
|----------------|---------------------------------------------------|
| `run`          | `Shell.launch("/bin/bash", "-c", cmd)`            |
| `is_folder`    | `file.is_folder` (object method)                  |
| `str_repeat`   | `str` * n oder Schleife                           |
| `chr` / `ord`  | `str(code)` bzw. ASCII-Loop                       |
| `md5`          | `crypto.md5(str)`                                 |

## Pattern

### 1. Linter (`scripts/lint-greyscript.py`)

```python
#!/usr/bin/env python3
"""lint-greyscript.py — Static-Lint für GreyScript (.src)"""
import re, sys
from pathlib import Path

DISALLOWED = {
    "run":        "Shell.launch(...)",
    "is_folder":  "file.is_folder(...)",
    "str_repeat": "str * n",
    "chr":        "str(code)",
    "ord":        "byte via chr+ord-Loop",
    "md5":        "crypto.md5(...)",
    "include":    "Import via greybel require",
}

issues = []
for path in map(Path, sys.argv[1:]):
    src = path.read_text(encoding="utf-8")
    lines = src.splitlines()

    # Regel 1: erste nicht-leere Zeile MUSS mit //command: ... anfangen
    first = next((l for l in lines if l.strip()), "")
    if not first.startswith("//command:"):
        issues.append(f"{path}:1 [ERROR]  Erste Zeile fehlt '//command: <name>'")

    # Regel 2: jede Funktion mit "command " MUSS //command: Marker haben
    if re.search(r"^\s*\w+\s+command\s*=\s*function", src, re.M):
        if "//command:" not in src:
            issues.append(f"{path} [ERROR]  command=function ohne //command-Marker")

    # Regel 3: Token-basierter Builtin-Scan
    for i, line in enumerate(lines, 1):
        stripped = line.split("//", 1)[0]  # Kommentare ignorieren
        for tok in re.findall(r"\b([A-Za-z_]\w*)\s*\(", stripped):
            if tok in DISALLOWED:
                issues.append(
                    f"{path}:{i} [ERROR]  Verbotenes Builtin '{tok}' — "
                    f"Workaround: {DISALLOWED[tok]}"
                )

    # Regel 4: Warnung — split() ohne max=-1 (greybel-js safe-default)
    for i, line in enumerate(lines, 1):
        if re.search(r"\.split\(\s*[\"'](?!\s*\")", line):
            issues.append(
                f"{path}:{i} [WARN]   str.split() ohne Limit kann leer liefern"
            )

if issues:
    print("\n".join(issues))
    sys.exit(1 if any("[ERROR]" in i for i in issues) else 0)

print(f"OK: {len(sys.argv)-1} Datei(en) sauber.")
```

### 2. Pre-Build-Wrapper (`scripts/build-safe.sh`)

```bash
#!/usr/bin/env bash
# build-safe.sh — lintet vor jedem greybel build
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LINT="$SCRIPT_DIR/../greyscript-linter/scripts/lint-greyscript.py"

# 1) Lint
python3 "$LINT" "$@"

# 2) nur bei OK wirklich bauen
greybel build "$@"
```

### 3. Pre-Commit-Hook

```bash
# .git/hooks/pre-commit (in Tool-Repo)
#!/usr/bin/env bash
git diff --cached --name-only -- '*.src' | \
  xargs -r python3 ~/.openclaw/skills/greyscript-linter/scripts/lint-greyscript.py
```

## Pitfalls

- ❌ **`run`** ist der häufigste Build-Killer — `Shell.launch` stattdessen.
- ❌ **Kommentare mit Beispiel-Code** triggern den Linter genauso; Token-Scan
  ignoriert aber `//`-Kommentare (siehe `split("//", 1)[0]`).
- ❌ `str.split("a")` ohne `max` ist erlaubt, kann aber in Edge-Cases leer
  sein — Linter warnt nur, blockiert nicht.
- ✅ Linter **nicht** in GreyHack-Spielscripts ausführen (anderer Scope) — nur
  auf `*.src` für greybel-Builds.
- ✅ Eigene `DISALLOWED`-Liste pflegen statt blind updaten — neue greybel-Versionen
  können Builtins nachpflegen.

## Cron-Beispiel

```cron
# Täglich 03:00 — alle Tool-Repos linten
0 3 * * * find /home/bratan/maxclaw-tools -name '*.src' | \
  xargs python3 ~/.openclaw/skills/greyscript-linter/scripts/lint-greyscript.py
```