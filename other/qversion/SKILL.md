---
name: Qversion
user_invocable: true
description: Shows the current QE Framework version. Use when asked 'what version', 'qe version', 'show version', or 'check version'.
invocation_trigger: When the user asks which QE Framework version is currently installed.
recommendedModel: haiku
---

# Qversion — Version Info

## Role
Displays the current QE Framework plugin version.

## Execution Procedure

### Step 1: Read version
Read `.claude-plugin/plugin.json` from the QE Framework plugin directory and extract the `version` field.

### Step 2: Display
Print a single line:

```
QE Framework v{version}
```

## Will
- Read and display the current version from plugin.json

## Will Not
- Modify any files
- Execute any commands beyond reading the version
