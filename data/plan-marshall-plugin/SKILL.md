---
name: plan-marshall-plugin
description: Documentation domain manifest for plan-marshall workflow integration
user-invocable: false
allowed-tools: Read
---

# Plan Marshall Plugin - Documentation Domain

Domain manifest skill providing documentation capabilities to plan-marshall workflows.

## Purpose

Declares the documentation domain configuration including:
- Domain identity (key: documentation)
- Profile-based skill organization (core, quality)

## Configuration

All configuration is in `extension.py` which implements the Extension API:
- `get_skill_domains()` - Domain metadata with profiles
- `provides_triage()` - Triage skill reference or None
- `provides_outline()` - Outline skill reference or None

### Capabilities

Domain capabilities for `${domain}` placeholder resolution:

```json
"capabilities": {
  "triage": "pm-documents:ext-triage-docs"
}
```

Only triage capability is provided. Verification steps requiring `quality-gate` or `build-verify` are skipped for this domain.

## Detection

This domain is applicable when a `doc/` directory exists in the project root, indicating AsciiDoc documentation.

## Integration

This manifest is read by:
- `skill-domains get-available` - Lists available domains
- `skill-domains configure` - Applies domain configuration to marshal.json
- `marshall-steward` wizard - Domain selection during project setup
