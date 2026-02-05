---
name: mmd-debugging
description: Troubleshoot and debug MIDI Markdown (MMD) files including validation errors, timing issues, value ranges, syntax problems, and compilation failures. Use when the user encounters MMD errors, validation failures, unexpected behavior, or needs help diagnosing MMD issues.
---

# MMD Debugging Skill

## Overview

This skill specializes in troubleshooting and debugging MIDI Markdown files. It provides systematic approaches to identify and fix errors, validation issues, and unexpected behavior.

## Quick Diagnosis

When encountering an MMD error, follow this diagnostic sequence:

### 1. Check Syntax First

```bash
# Fast syntax check
mmdc check file.mmd

# Or use validation script
python .claude/skills/mmd-writing/scripts/validate_syntax.py file.mmd
```

**Common syntax issues**:
- Missing frontmatter (`---`)
- Missing timing markers before commands
- Invalid timing format
- Missing `- ` before commands
- Missing `@end` after loops/aliases

### 2. Full Validation

```bash
# Complete validation with details
mmdc validate file.mmd --verbose
```

**Common validation issues**:
- Values out of range (>127)
- Channels outside 1-16
- Timing going backwards
- Invalid note names
- Missing required frontmatter fields

### 3. Inspect Events

```bash
# See what events are generated
mmdc inspect file.mmd

# Filter specific types
mmdc inspect file.mmd --type note_on
mmdc inspect file.mmd --type cc
```

**Look for**:
- Missing events
- Incorrect timing
- Wrong channels or values
- Unexpected event sequences

## Error Categories

### Timing Errors

**Symptom**: "Time X is before previous event at time Y"

**Causes**:
1. Timing markers not monotonically increasing
2. Loop timing overlaps
3. Using absolute timing after musical timing

**Debug approach**:
```bash
# Extract all timing markers
mmdc inspect file.mmd | awk '{print $1}' | sort -c

# Check if times are sequential
mmdc inspect file.mmd | head -20
```

**Solutions**:
- Use relative timing `[+duration]` to avoid conflicts
- Ensure absolute times increase: `[00:05.000]` → `[00:10.000]`
- Use musical timing consistently: `[1.1.0]` → `[2.1.0]`

---

### Value Range Errors

**Symptom**: "Value X exceeds maximum allowed (Y)"

**MIDI value ranges**:
- Most values: 0-127
- Channels: 1-16
- Notes: 0-127 (C-1 to G9)
- Pitch bend: -8192 to +8191 or 0 to 16383

**Debug approach**:
```bash
# Export to CSV and check values
mmdc compile file.mmd --format csv -o debug.csv

# Find values > 127
awk -F',' '$5 > 127 {print}' debug.csv
```

**Quick fixes**:
```mmd
# Wrong
- cc 1.7.255        # Max is 127

# Correct
- cc 1.7.127        # Use max value
```

---

### Syntax Errors

**Symptom**: "Unexpected token at line X"

**Common causes**:

1. **Missing dash**:
   ```mmd
   # Wrong
   [00:00.000]
   note_on 1.C4 100 1b

   # Correct
   [00:00.000]
   - note_on 1.C4 100 1b
   ```

2. **Invalid timing format**:
   ```mmd
   # Wrong
   [1:30]         # Missing milliseconds
   [1-1-0]        # Wrong separator

   # Correct
   [00:01.500]    # mm:ss.ms
   [1.1.0]        # bar.beat.tick
   ```

3. **Missing @end**:
   ```mmd
   # Wrong
   @loop 4 times at [1.1.0] every 1b
     - note_on 1.C4 100 1b
   # Missing @end!

   # Correct
   @loop 4 times at [1.1.0] every 1b
     - note_on 1.C4 100 1b
   @end
   ```

---

### Import/Alias Errors

**Symptom**: "Import file not found" or "Undefined alias"

**Debug approach**:
```bash
# Check if device library exists
ls devices/quad_cortex.mmd

# Verify import syntax
grep "@import" file.mmd
```

**Common issues**:
1. **Missing quotes**: `@import devices/...` → `@import "devices/..."`
2. **Wrong path**: `@import "quad_cortex.mmd"` → `@import "devices/quad_cortex.mmd"`
3. **Alias before import**: Move `@import` statements before alias usage

---

### Random Values Issues

**Symptom**: "random() not supported in this context"

**NOT allowed**:
```mmd
[00:08.random(-10,10)]              # Timing
@define VEL random(40,60)           # Variables
- note_on 10.42.random(80,100) 1b   # Numeric note IDs
```

**Allowed**:
```mmd
- note_on 1.C4 random(70,100) 0.5b  # Velocity ✓
- note_on 1.random(C3,C5) 80 0.5b   # Note range ✓
- cc 1.74.random(50,90)             # CC value ✓
```

---

### Variable Errors

**Symptom**: "Variable not defined" or "Invalid variable name"

**Requirements**:
- Names must be UPPERCASE_WITH_UNDERSCORES
- Define before use
- Use `${}` syntax for references

**Debug approach**:
```bash
# List all variable definitions
grep "@define" file.mmd

# List all variable uses
grep "\${" file.mmd
```

**Example**:
```mmd
# Define first
@define MAIN_TEMPO 120
@define VERSE_PRESET 5

# Use later
[00:00.000]
- tempo ${MAIN_TEMPO}
- pc 1.${VERSE_PRESET}
```

## Debugging Techniques

### Binary Search for Errors

When error location is unclear:

1. **Comment out half the file**:
   ```mmd
   /*
   [00:10.000]
   - note_on 1.C4 100 1b
   ...
   */
   ```

2. **Test validation**: `mmdc validate file.mmd`

3. **If error persists**: Problem is in uncommented half
   **If error gone**: Problem is in commented half

4. **Repeat** until error isolated

### Minimal Reproduction

Create smallest file that reproduces error:

```mmd
---
ppq: 480
tempo: 120
---

[00:00.000]
# Add problematic command here
```

This helps isolate the issue from surrounding code.

### Event Inspection

**Check event count**:
```bash
mmdc inspect file.mmd | wc -l
```

**Check timing distribution**:
```bash
mmdc inspect file.mmd | awk '{print $1}' | sort | uniq -c
```

**Check channels used**:
```bash
mmdc inspect file.mmd | grep -o "ch:[0-9]*" | sort | uniq -c
```

**Find specific commands**:
```bash
mmdc inspect file.mmd | grep "note_on"
mmdc inspect file.mmd | grep "cc"
```

### Comparison with Working Examples

Compare your code with similar working examples:

```bash
# Find relevant example
ls examples/

# Compare structure
diff -u examples/00_basics/01_hello_world.mmd your_file.mmd
```

### Export and Analyze

Export to different formats for analysis:

```bash
# JSON for detailed inspection
mmdc compile file.mmd --format json -o debug.json
cat debug.json | jq '.events[] | select(.type == "note_on")'

# CSV for spreadsheet analysis
mmdc compile file.mmd --format csv -o debug.csv
# Open in spreadsheet or analyze with awk/grep

# Table for visual inspection
mmdc compile file.mmd --format table | less
```

## Common Scenarios

### Scenario 1: "No MIDI output"

**Checklist**:
1. ✓ Frontmatter present?
2. ✓ Timing markers before commands?
3. ✓ Commands start with `- `?
4. ✓ Loops have `@end`?
5. ✓ File validates without errors?

**Debug**:
```bash
mmdc inspect file.mmd
# If no output: commands not being parsed

mmdc validate file.mmd --verbose
# Check for validation failures
```

---

### Scenario 2: "Timing is wrong"

**Checklist**:
1. Mixing timing paradigms? (absolute vs musical)
2. Tempo/time_signature defined for musical timing?
3. Relative timing referencing correct previous event?
4. Loop timing makes sense?

**Debug**:
```bash
# Check first 20 events
mmdc inspect file.mmd | head -20

# Look for time jumps
mmdc inspect file.mmd | awk '{print $1}'
```

---

### Scenario 3: "Loop doesn't work"

**Common issues**:
1. Missing `@end`
2. Invalid loop syntax
3. Timing conflicts

**Test**:
```mmd
# Minimal loop test
@loop 4 times at [00:00.000] every 1b
  - note_on 1.C4 100 0.5b
@end
```

**Debug**:
```bash
# Count events (should be 4)
mmdc inspect file.mmd | grep "note_on" | wc -l
```

---

### Scenario 4: "Device alias not working"

**Checklist**:
1. ✓ Import statement present?
2. ✓ Import before usage?
3. ✓ Correct device library name?
4. ✓ Correct parameter count?

**Debug**:
```bash
# Check imports
grep "@import" file.mmd

# Check available aliases
cat devices/quad_cortex.mmd | grep "@alias"

# Test without alias (use raw MIDI)
- cc 1.32.2  # Instead of cortex_load...
```

---

### Scenario 5: "Validation passes but output wrong"

**Possible causes**:
1. Logic error (correct syntax, wrong intent)
2. Timing calculation issue
3. Device not responding as expected

**Debug**:
```bash
# Inspect exact events generated
mmdc inspect file.mmd

# Export to MIDI and test in DAW
mmdc compile file.mmd -o test.mid

# Play back to verify
mmdc play file.mmd --port 0
```

## Systematic Debug Workflow

### Step 1: Identify Error Type

Run validation and note error category:
- Syntax error (E1xx)
- Validation error (E2xx)
- Import/alias error (E3xx)
- Compilation error (E4xx)

### Step 2: Locate Exact Line

Error messages include line numbers:
```
Error: Line 45: Value 255 exceeds maximum allowed (127)
```

### Step 3: Check Context

Look at surrounding lines:
- Previous timing marker
- Related commands
- Variable definitions
- Loop/alias boundaries

### Step 4: Apply Fix

Use troubleshooting guide or examples for solution.

### Step 5: Verify Fix

```bash
# Validate
mmdc validate file.mmd

# Inspect events
mmdc inspect file.mmd

# Test playback
mmdc play file.mmd --port 0
```

## Quick Fixes

### Fix: Missing Frontmatter
```mmd
---
ppq: 480
tempo: 120
---
```

### Fix: Timing Going Backwards
```mmd
# Use relative timing
[00:05.000]
- note_on 1.C4 100 1b

[+5s]          # Instead of absolute time
- note_on 1.D4 100 1b
```

### Fix: Value Out of Range
```mmd
# Clamp to valid range
- cc 1.7.127   # Instead of 255
```

### Fix: Missing Timing Marker
```mmd
[00:00.000]    # Add timing marker
- note_on 1.C4 100 1b
```

### Fix: Invalid Variable Name
```mmd
@define MAIN_TEMPO 120  # UPPERCASE_SNAKE_CASE
```

### Fix: Missing Import
```mmd
@import "devices/quad_cortex.mmd"

[00:00.000]
- cortex_load 1.1.0.5
```

## Diagnostic Tools

### Built-in Tools

1. **mmdc check** - Syntax only (fastest)
2. **mmdc validate** - Full validation
3. **mmdc inspect** - Event inspection
4. **mmdc compile --format json** - Detailed output

### Custom Scripts

1. **validate_syntax.py** - Quick syntax validation
   ```bash
   python .claude/skills/mmd-writing/scripts/validate_syntax.py file.mmd
   ```

2. **generate_template.py** - Create working templates
   ```bash
   python .claude/skills/mmd-writing/scripts/generate_template.py --type basic
   ```

## When to Ask for Help

If after following this guide you're still stuck:

1. **Create minimal reproduction**
2. **Gather diagnostic info**:
   - Error message (full text)
   - Output of `mmdc validate --verbose`
   - Minimal MMD file that reproduces issue
3. **Check related resources** (see below)
4. **File GitHub issue** with reproduction case

## Related Skills and Resources

**Skills**:
- **mmd-writing** - MMD syntax reference
- **mmd-cli** - CLI tools and options
- **mmd-device-library** - Creating device libraries

**Resources**:
- **TROUBLESHOOTING.md** - Detailed error reference (in mmd-writing skill)
- **examples/** - 49 working example files
- **spec.md** - Complete language specification
- **docs/dev-guides/anti-patterns.md** - Common mistakes to avoid

## Quick Reference

### Error to Solution Mapping

| Error | Quick Fix |
|-------|-----------|
| Missing frontmatter | Add `---\nppq: 480\n---` at top |
| No timing marker | Add `[00:00.000]` before first command |
| Timing backwards | Use relative timing `[+duration]` |
| Value > 127 | Clamp to 127 |
| Invalid channel | Use 1-16 range |
| Undefined alias | Add `@import` statement |
| Missing @end | Add `@end` after loop/alias |
| Invalid variable | Use UPPERCASE_SNAKE_CASE |
| random() not allowed | Move to velocity/note/CC value |

### Validation Command Matrix

| Need | Command |
|------|---------|
| Quick syntax check | `mmdc check file.mmd` |
| Full validation | `mmdc validate file.mmd` |
| Detailed errors | `mmdc validate file.mmd --verbose` |
| Event inspection | `mmdc inspect file.mmd` |
| JSON export | `mmdc compile file.mmd --format json` |
| CSV export | `mmdc compile file.mmd --format csv` |

For comprehensive troubleshooting reference, see TROUBLESHOOTING.md in the mmd-writing skill directory.
