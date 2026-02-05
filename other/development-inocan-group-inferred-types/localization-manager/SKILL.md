---
name: localization-manager
description: Manage localization strings, find missing translations, validate .strings files
type: skill
language: python
---

# Localization Manager

Manage app localization and translation files.

## Capabilities
- Extract localizable strings from Swift/ObjC code
- Parse .strings and .stringsdict files
- Find missing translations
- Detect unused localization keys
- Validate string format specifiers
- Generate translation reports
- Export for translators (CSV/XLIFF)
- Import translations

## Tools
`localization_manager.py` - Parse and validate localization files

## Commands
```bash
# Find missing translations
./localization_manager.py find-missing --base-lang en

# Extract strings from code
./localization_manager.py extract-strings --source-dir PaleoRose

# Validate .strings files
./localization_manager.py validate

# Generate report
./localization_manager.py report --output translations.html
```
