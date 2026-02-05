---
name: plantuml-manipulator
description: Structured manipulation of PlantUML sequence diagrams - insert blocks after groups, add participants, and validate diagram structures across multiple files simultaneously
---

# PlantUML Manipulator Skill

## When to Use This Skill

Use this skill for:
- **Repetitive changes** to multiple PlantUML files (e.g., insert block into 10+ files)
- **Structural validation** of diagrams (checking for missing groups/participants)
- **Batch operations** like adding participants to multiple files
- **Reporting** on existing structures (which groups/participants exist where)

**Do not use for:**
- Single, one-time changes to 1-2 files (use normal Edit tools)
- Complex semantic changes requiring contextual understanding
- Non-sequence PlantUML diagrams

## Tool Availability

The tool is located at: `./tool/plantuml-manipulator/`

First check if the tool is implemented:
```bash
python -m plantuml_manipulator --help
```

If not available, inform the user that implementation is pending.

## Main Commands

### 1. Insert Block After Group

Most common scenario: Insert a code block after a specific group in multiple files.

**Workflow:**
1. Create a snippet file with the block to insert
2. Run with `--dry-run` to preview changes
3. If OK, run without `--dry-run`

**Example:**
```bash
# 1. Create snippet (you do this with Write tool)
# snippets/validation.puml contains the block to insert

# 2. Dry-run
python -m plantuml_manipulator insert-after \
  --pattern "diagrams/**/*.puml" \
  --after-group "Process Request" \
  --block-file snippets/validation.puml \
  --dry-run \
  --verbose

# 3. Execute if OK
python -m plantuml_manipulator insert-after \
  --pattern "diagrams/**/*.puml" \
  --after-group "Process Request" \
  --block-file snippets/validation.puml \
  --verbose
```

**Important flags:**
- `--skip-if-exists "TEXT"`: Skip files already containing "TEXT"
- `--only-if-has-participant "NAME"`: Only files with participant NAME
- `--backup`: Create .bak files before changes

### 2. Add Participant

Adds a participant to multiple files at the correct position.

**Example:**
```bash
python -m plantuml_manipulator add-participant \
  --pattern "diagrams/**/*.puml" \
  --participant 'participant "API" as API #orange' \
  --after-participant "Frontend" \
  --skip-if-exists "API" \
  --verbose
```

### 3. Validation

Checks if all files contain required structures.

**Example:**
```bash
python -m plantuml_manipulator validate \
  --pattern "diagrams/**/*.puml" \
  --require-group "Perform Validation" \
  --require-participant "API" \
  --report-format table
```

### 4. Reporting

Creates overviews of existing structures.

**Examples:**
```bash
# List all groups
python -m plantuml_manipulator report groups \
  --pattern "diagrams/**/*.puml" \
  --format table

# List all participants
python -m plantuml_manipulator report participants \
  --pattern "diagrams/**/*.puml" \
  --format json

# Show structure of a single file
python -m plantuml_manipulator report structure \
  --file "diagrams/user_login.puml"
```

## Best Practices

### 1. Always Dry-Run First

**IMPORTANT:** Always run with `--dry-run` first to see what would happen.

```bash
# ✓ Correct
python -m plantuml_manipulator insert-after ... --dry-run
# Review output
python -m plantuml_manipulator insert-after ...

# ✗ Wrong
python -m plantuml_manipulator insert-after ...  # Without prior dry-run
```

### 2. Use --skip-if-exists

Prevent duplicate insertions:

```bash
python -m plantuml_manipulator insert-after \
  --after-group "Process Request" \
  --block-file snippets/validation.puml \
  --skip-if-exists "Perform Validation"  # ✓ Prevents duplicates
```

### 3. Use Filters for Targeted Operations

Instead of modifying all files, filter specifically:

```bash
# Only files with specific participant
--only-if-has-participant "PaymentService"

# Only files with specific group
--only-if-has-group "Process Data"
```

### 4. Backup for Large Changes

Always create backups when modifying many files:

```bash
python -m plantuml_manipulator insert-after \
  ... \
  --backup  # Creates .bak files
```

### 5. Validate After Changes

Check if changes were successful:

```bash
# After block insertion
python -m plantuml_manipulator validate \
  --pattern "..." \
  --require-group "New Group Name"
```

## Integration with Normal Tools

This tool is a **supplement**, not a replacement for normal Edit/Read tools:

**Use PlantUML Manipulator:**
- For 5+ similar changes
- When exact structural patterns exist
- For validation/reporting

**Use Normal Edit Tools:**
- For individual, context-dependent changes
- For complex logic changes
- For 1-3 files

## Communicating with the User

When using this skill, inform the user:

**Before execution:**
```
I'm now using the PlantUML Manipulator tool to insert the validation
into 8 files.

First, I'll run a dry-run to check what would happen...
```

**After dry-run:**
```
The dry-run shows that 8 files would be modified:
- user_login.puml
- payment_process.puml
- ...

Shall I proceed?
```

**After successful execution:**
```
✓ Successfully completed:
  - 8 files modified
  - API participant added to 7 files
  - Validation group inserted into 8 files
  - Backup files created (.bak)
```

## Further Information

For detailed API reference see: ../../api-reference.md
For full specification see: ../../specification.md
