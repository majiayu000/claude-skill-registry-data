---
name: cross-layer-check
description: Verify that a symbol (field, enum, status code) exists across all layers of a monorepo. Use after adding new fields, enums, or codes to catch cross-layer gaps.
allowed-tools: Bash(bash *) Bash(grep *) Bash(find *)
argument-hint: "<symbol> [--exact]"
---

# Cross-Layer Consistency Check

Verify that a symbol (field name, enum value, status code) exists across all layers of the monorepo.

## Usage

Run the bundled script:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/cross-layer-check.sh $ARGUMENTS
```

### Examples

```bash
# Check a field name (substring match)
bash ${CLAUDE_SKILL_DIR}/scripts/cross-layer-check.sh invoiceNumber

# Check an enum value (exact word match)
bash ${CLAUDE_SKILL_DIR}/scripts/cross-layer-check.sh PAYMENT_SENT --exact

# Check a new DTO field
bash ${CLAUDE_SKILL_DIR}/scripts/cross-layer-check.sh paymentDueDate
```

## What It Checks

The script searches across all source directories in order, reporting hits per layer:
- Backend / API source code
- Frontend source code
- Shared packages / libraries
- Test files
- Migrations / database schemas
- Configuration and documentation

## Interpreting Results

- **✅ Layer: N hits** — Symbol found in this layer
- **❌ Layer: no hits** — Symbol NOT found — possible gap
- **⚠️ WARNING** (< 3 layers) — Likely incomplete implementation

## When to Use

- After adding a new field to a DTO
- After adding a new status code or enum value
- During MR review (Review Protocol point #2: cross-layer consistency)
- When the `/review` command flags potential cross-layer gaps

