---
name: access-module-encoding
description: Check encoding consistency and mojibake risks for Access/VBA exported modules (.bas/.cls) and related files, and fix common mojibake. Use when asked to review codificacion/encoding issues, to verify UTF-8 vs ANSI, to fix mojibake, or to detect BOM/UTF-16 problems before importing into Access.
---

# Access Module Encoding

## Quick use

Check encodings:
```bash
python scripts/check_access_module_encoding.py --root C:\Proyectos\gestion-proyectos --extensions .bas .cls
python scripts/check_access_module_encoding.py path\to\File.bas path\to\File.cls
python scripts/check_access_module_encoding.py --strict
```

Fix mojibake (dry-run by default):
```bash
python scripts/fix_access_mojibake.py --root C:\Proyectos\gestion-proyectos --extensions .bas .cls
python scripts/fix_access_mojibake.py path\to\File.bas --apply --backup
```

Fix mojibake with built-in Spanish defaults:
```bash
python scripts/fix_access_mojibake.py --root C:\Proyectos\gestion-proyectos --extensions .bas .cls --spanish-defaults --apply --backup
```

Fix mojibake with explicit replacements for \ufffd (lossy):
```bash
python scripts/fix_access_mojibake.py --root C:\Proyectos\gestion-proyectos --extensions .bas .cls --map path\to\mojibake_map.json --fix-map --apply --backup
```

Normalize to UTF-8 no BOM:
```bash
python scripts/normalize_access_module_encoding.py --root C:\Proyectos\gestion-proyectos --extensions .bas .cls
python scripts/normalize_access_module_encoding.py path\to\File.bas --dry-run
python scripts/normalize_access_module_encoding.py --root C:\Proyectos\gestion-proyectos --extensions .bas .cls --backup
```

## Interpret results

- ascii-only: safe everywhere.
- utf8: UTF-8 without BOM.
- utf8-bom: UTF-8 with BOM (risky for Access import).
- ansi-cp1252: typical Access export.
- utf16-le/utf16-be/binary: treat as problems.

## Normalize notes

- Writes in place; use --dry-run to preview or --backup to keep .bak copies.
- Use --strict to return exit code 1 if a file cannot be converted.

## Mojibake notes

- The utf8-in-cp1252 repair is reversible and safe when sequences like \u00c3 or \u00c2 appear.
- Use --spanish-defaults for common Spanish words and EnumSiNo.S\u00ed patterns.
- The replacement character \ufffd is lossy; use --map with explicit replacements if you want to fix it.
