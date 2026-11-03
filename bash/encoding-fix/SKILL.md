---
name: encoding-fix
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Mojibake-Reparatur für doppelt/dreifach kodiertes UTF-8. Behebt Windows-cp1252/Latin-1-Fehlinterpretationen. Ohne Abhängigkeiten.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [encoding, utf-8, mojibake, windows, cp1252, text-repair]
language: de
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "bach"
  origin_path: "system/tools/encoding_fix.py"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false
---
<img src="banner.png" width="100%" alt="encoding-fix banner">

# Encoding Fix

Repariert Mojibake (doppelt/dreifach kodiertes UTF-8) das durch Windows cp1252/Latin-1
Fehlinterpretation entsteht. Zero Dependencies — nur Python stdlib.

## Typisches Problem

```
"ue" (U+00FC) → UTF-8 \xc3\xbc → als cp1252 gelesen → "Ã¼"
```

## Nutzung

### Als Library
```python
from encoding_fix import sanitize_outbound

clean = sanitize_outbound("WÃ¼rge")  # → "Würge"
```

### Subprocess-Output
```python
from encoding_fix import sanitize_subprocess_output

text = sanitize_subprocess_output(process.stdout)
```

### CLI
```bash
python encoding_fix.py "WÃ¼rge"    # Einzelnen String prüfen
python encoding_fix.py              # Selbst-Test
```

## Features

- **Idempotent:** Korrekt kodierter Text wird nicht veraendert
- **Bis zu 3 Runden:** Repariert auch dreifach-kodierte Strings
- **Subprocess-Dekoder:** UTF-8/cp1252 Fallback fuer Prozess-Output
- **Zero Dependencies:** Nur Python stdlib

## Changelog

### 1.0.0 (2026-03-12)
- Portiert aus BACH system/tools/encoding_fix.py
