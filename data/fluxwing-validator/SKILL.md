---
name: fluxwing-validator
description: Validate uxscii components and screens against schema with interactive menu or direct script calls
version: 1.0.0
author: Fluxwing Team
allowed-tools: Read, Bash, AskUserQuestion, TodoWrite
---

# Fluxwing Validator

Validate uxscii components and screens against JSON Schema with interactive workflows.

## Overview

This skill provides two modes of operation:

1. **Interactive Mode**: User invocation with menu and minimal output
2. **Direct Mode**: Script calls from other skills with verbose output

## When to Use This Skill

**User says:**
- "Validate my components"
- "Check if everything is valid"
- "Run validation on my screens"
- "Validate the project"

**Other skills:** Call validator scripts directly (see Technical Reference below)

## Interactive Validation Workflow

### Step 1: Present Validation Options

Use AskUserQuestion to present menu:

```
What would you like to validate?
```

**Options:**
1. **Everything in this project** - Validates all components and screens
2. **Just components** - Validates `./fluxwing/components/*.uxm`
3. **Just screens** - Validates `./fluxwing/screens/*.uxm`
4. **Let me specify a file or pattern** - Custom path/glob pattern

### Step 2: Check What Exists

Before running validation, check if directories exist:

```bash
# Check for components
test -d ./fluxwing/components

# Check for screens
test -d ./fluxwing/screens
```

**If neither exists:**
- Inform user: "No components or screens found. Create some first!"
- Exit cleanly

**If option 4 (custom) selected:**
- Ask user for the pattern/file path
- Validate it's not empty
- Proceed with user-provided pattern

### Step 3: Run Validation

Based on user selection:

**Option 1: Everything**
```bash
# Validate components
node {SKILL_ROOT}/validate-batch.js \
  "./fluxwing/components/*.uxm" \
  "{SKILL_ROOT}/../fluxwing-component-creator/schemas/uxm-component.schema.json" \
  --json

# Validate screens
node {SKILL_ROOT}/validate-batch.js \
  "./fluxwing/screens/*.uxm" \
  "{SKILL_ROOT}/../fluxwing-component-creator/schemas/uxm-component.schema.json" \
  --screens \
  --json
```

**Option 2: Just components**
```bash
node {SKILL_ROOT}/validate-batch.js \
  "./fluxwing/components/*.uxm" \
  "{SKILL_ROOT}/../fluxwing-component-creator/schemas/uxm-component.schema.json" \
  --json
```

**Option 3: Just screens**
```bash
node {SKILL_ROOT}/validate-batch.js \
  "./fluxwing/screens/*.uxm" \
  "{SKILL_ROOT}/../fluxwing-component-creator/schemas/uxm-component.schema.json" \
  --screens \
  --json
```

**Option 4: Custom pattern**
```bash
# Use user-provided pattern
node {SKILL_ROOT}/validate-batch.js \
  "${userPattern}" \
  "{SKILL_ROOT}/../fluxwing-component-creator/schemas/uxm-component.schema.json" \
  --json
```

### Step 4: Parse Results and Show Minimal Summary

Parse JSON output from validator to extract:
- `total`: Total files validated
- `passed`: Number of valid files
- `failed`: Number of failed files
- `warnings`: Total warning count

**Display minimal summary:**

```
✓ 12/14 components valid
✗ 2/14 components failed
⚠ 3 warnings total
```

**If all passed:**
```
✓ All 14 components valid
⚠ 3 warnings
```

**If everything failed:**
```
✗ All 14 components failed
```

**If nothing to validate:**
```
No files found matching pattern
```

### Step 5: Ask About Details

Use AskUserQuestion to ask:

```
Show error details?
```

**Options:**
1. **Yes** - Display full validation output
2. **No** - Clean exit

### Step 6: Display Details (if requested)

If user selects "Yes", show full validation output including:

**Failed files section:**
```
Failed Files:

  ✗ broken-button (./fluxwing/components/broken-button.uxm)
    Errors: 2
      1. must have required property 'fidelity'
      2. ASCII template file not found

  ✗ old-card (./fluxwing/components/old-card.uxm)
    Errors: 1
      1. invalid version format
```

**Passed with warnings section:**
```
Passed with Warnings:

  ✓ login-screen (2 warnings)
  ✓ dashboard (1 warning)
```

**Fully passed section (optional, only if not too many):**
```
Fully Passed:

  ✓ primary-button
  ✓ secondary-button
  ✓ email-input
  ...
```

## Edge Cases

### No fluxwing directory exists
```
No components or screens found. Create some first!
```

### Empty directories
```
✓ 0/0 components valid
```

### Invalid glob pattern (option 4)
```
No files found matching pattern: ${pattern}
```

### Validation script fails to execute
```
Error: Cannot execute validator. Node.js required.
```

## Technical Reference (For Other Skills)

### Direct Script Calls

Other skills (component-creator, screen-scaffolder) call validator scripts directly:

**Validate single component:**
```bash
node {SKILL_ROOT}/../fluxwing-validator/validate-component.js \
  ./fluxwing/components/button.uxm \
  {SKILL_ROOT}/schemas/uxm-component.schema.json
```

**Validate single screen:**
```bash
node {SKILL_ROOT}/../fluxwing-validator/validate-screen.js \
  ./fluxwing/screens/login-screen.uxm \
  {SKILL_ROOT}/schemas/uxm-component.schema.json
```

**Batch validate:**
```bash
node {SKILL_ROOT}/../fluxwing-validator/validate-batch.js \
  "./fluxwing/components/*.uxm" \
  {SKILL_ROOT}/schemas/uxm-component.schema.json
```

**Output modes:**
- Default: Human-readable (verbose, full errors/warnings)
- `--json`: Machine-readable JSON

**Exit codes:**
- `0`: All files valid
- `1`: One or more files invalid
- `2`: Missing dependencies or invalid arguments

### Validator Scripts

**Available scripts:**
- `validate-component.js` - Validate single component file
- `validate-screen.js` - Validate single screen file (with screen-specific checks)
- `validate-batch.js` - Validate multiple files with glob patterns
- `test-validator.js` - Test component templates
- `test-screen-validator.js` - Test screen templates

### npm Scripts (for testing)

```bash
cd {SKILL_ROOT}

# Run tests
npm test                    # Test component templates
npm run test:screens       # Test screen templates

# Batch validation
npm run validate:components  # Validate all components
npm run validate:screens     # Validate all screens
npm run validate:all         # Validate everything
```

## Example Interactions

### Example 1: Validate Everything

**User:** "Validate my components"

**Skill:**
```
What would you like to validate?

1. Everything in this project
2. Just components
3. Just screens
4. Let me specify a file or pattern
```

**User selects:** Option 1

**Skill runs validation and shows:**
```
✓ 12/14 components valid
✗ 2/14 components failed
⚠ 3 warnings total

✓ 2/2 screens valid
⚠ 1 warning

Show error details?
```

**User:** "yes"

**Skill shows full error details for failed files**

### Example 2: Validate Specific Pattern

**User:** "Validate my components"

**Skill:** (presents menu)

**User selects:** Option 4 (custom pattern)

**Skill:** "What file or pattern would you like to validate?"

**User:** "./fluxwing/components/*-button.uxm"

**Skill validates and shows:**
```
✓ 3/3 files valid

Show error details?
```

## Implementation Notes

**Parse JSON output:**
```javascript
const result = JSON.parse(bashOutput);
const total = result.total;
const passed = result.passed;
const failed = result.failed;
const warnings = result.warnings;
```

**Summary formatting:**
- Show passed/failed ratio for quick scan
- Highlight failures prominently
- Warnings shown but not intrusive
- Clean, minimal output by default

**Error detail formatting:**
- Group by status (failed, warnings, passed)
- Show file path and error count
- Display first 2-3 errors per file
- Indicate if more errors exist

---

**Skill Status:** Ready for use
**Version:** 1.0.0
