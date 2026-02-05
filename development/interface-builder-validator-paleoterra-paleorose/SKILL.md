---
name: interface-builder-validator
description: Parse and validate XIB/Storyboard files for broken outlets, warnings, accessibility
type: skill
language: python
---

# Interface Builder Validator

Validate XIB and Storyboard files for common issues.

## Capabilities
- Parse XIB/Storyboard XML
- Find broken IBOutlet connections
- Detect missing IBAction connections
- Check Auto Layout warnings
- Validate accessibility labels
- Find ambiguous constraints
- Detect missing localization
- Check for deprecated UI elements
- Validate color/image references

## Tools
`ib_validator.py` - Parse and validate IB files

## Commands
```bash
# Validate all XIBs
./ib_validator.py validate --path "PaleoRose/**/*.xib"

# Check specific file
./ib_validator.py check XRoseDocument.xib

# Find broken outlets
./ib_validator.py broken-outlets

# Accessibility audit
./ib_validator.py accessibility
```

## Issues Detected
- Outlets connected to deleted properties
- IBActions with wrong signatures
- Missing accessibility identifiers
- Ambiguous Auto Layout
- Missing localization keys
- Invalid color/image names
- Deprecated UI classes

## Output
```
Interface Builder Validation
============================

XRoseDocument.xib:
  ✓ All outlets connected
  ⚠ Missing accessibility label (3 views)
  ⚠ Ambiguous width for view at line 234

MainMenu.xib:
  ✓ No issues found

Total: 2 warnings, 0 errors
```
