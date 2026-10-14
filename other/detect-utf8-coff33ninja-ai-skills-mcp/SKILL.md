---
name: detect-utf8
description: Detects whether the terminal, console, or device supports UTF-8 encoding. Checks code page, .NET encoding defaults, environment locale, and verifies with a round-trip test of Unicode characters.
---

# Detect UTF-8

## Problem

Scripts and tools that output or read non-ASCII text (emojis, accented characters, CJK, special symbols) fail silently or produce garbled output when the terminal or device doesn't support UTF-8. This can corrupt logs, break cross-platform file reads, and introduce subtle bugs in text processing.

## Detection triggers

Activate when:
- You're about to write a script that outputs non-ASCII characters
- You see garbled text in terminal output or log files
- Working across Windows and Unix environments with different default encodings
- You need to decide whether to use `-Encoding utf8` or `-Encoding utf8BOM`
- The task involves emoji, Unicode symbols, or internationalized text

## Detection checks

The bundled script checks these in order:

1. **PowerShell output encoding** — `$OutputEncoding` and `[Console]::OutputEncoding`
2. **Windows code page** — via `chcp` (e.g. 65001 = UTF-8, 437 = US-ASCII, 932 = Shift-JIS)
3. **Locale environment** — `LANG`, `LC_ALL`, `LC_CTYPE` on Unix; `$env:VSLANG` on Windows
4. **.NET default encoding** — `[System.Text.Encoding]::Default`
5. **Round-trip test** — writes and reads a Unicode string (✨🔬✅) to verify end-to-end UTF-8 fidelity
6. **UTF-8 BOM awareness** — distinguishes between UTF-8 with BOM and without BOM

## Protocol

1. Run the detection script before creating or modifying files that contain non-ASCII text
2. If UTF-8 is not supported, set the console to UTF-8 mode before proceeding:
   - Windows: `chcp 65001` or `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`
   - Unix: set `LANG=en_US.UTF-8` or `LC_ALL=en_US.UTF-8`
3. If round-trip fails, use ASCII-safe alternatives or explicit byte encoding
4. Apply UTF-8 to all subsequent operations when supported:
   - Set `$PSDefaultParameterValues['*:Encoding'] = 'utf8'` for all file/cmdlet operations
   - Use `-Encoding utf8` explicitly on every `Out-File`, `Set-Content`, `Export-Csv`, and similar cmdlets
   - Pass `[System.Text.UTF8Encoding]::new($false)` to .NET file APIs for BOM-free UTF-8
   - On Unix, ensure `LANG` or `LC_ALL` ends with `.UTF-8` before running scripts
5. For scripts generated in this session, include an explicit encoding declaration:
   - PowerShell: `#Requires -Version 7` + use `-Encoding utf8` on all file writes
   - Python: `# -*- coding: utf-8 -*-` or `sys.stdout.reconfigure(encoding='utf-8')`
   - Node.js: `// encoding: utf-8` or use `fs.writeFileSync(path, data, 'utf8')`
6. Log the encoding state alongside other environment metadata
7. If `-Apply` was used, re-run detection after any shell/code-page reset to confirm UTF-8 is still active

## When NOT to use

- Pure ASCII-only content (no Unicode characters at all)
- Binary file operations where encoding doesn't apply
- The encoding is already known from a prior detection in the same session

## Bundled Script

Copy `check-utf8.ps1` to your project's `.ai_scripts/` directory:

```powershell
# From skill source
cp <skill-path>/detect-utf8/scripts/check-utf8.ps1 .ai_scripts/
```

Run the detection:

```powershell
.ai_scripts\check-utf8.ps1                    # human-readable report
.ai_scripts\check-utf8.ps1 -Json              # JSON for programmatic use
.ai_scripts\check-utf8.ps1 -Quiet             # exit code only (0 = UTF-8 OK)
.ai_scripts\check-utf8.ps1 -Apply             # detect + apply UTF-8 to session
```

## Cross-references

- **os-awareness** — UTF-8 detection is part of OS-aware environment probing; OS type determines which encoding checks apply.
- **portable-self-contained** — Project-local tooling must be encoding-aware; UTF-8 detection ensures scripts produce portable output.
- **audit-project** — Audit can include encoding health as part of environment portability checks.
