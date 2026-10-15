---
name: migrate
description: Plan and execute data or schema migrations -- ledger format, bus format, config changes, database.
version: 0.1.0
execution-mode: side_effecting
argument-hint: "\"MIGRATION DESCRIPTION\" (e.g., \"add links field to ledger entries\")"
category: fleet-ops
status: candidate
---
# Migrate

Plan and execute data or schema migrations safely with rollback capability.

## Execution

### 0. Emit SKILL_INVOKE
Post SKILL_INVOKE to the bus before any stateful action.
```
Type: SKILL_INVOKE
To: all
Message: [skill=migrate] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

### 1. Assess the migration

| Question | Answer |
|----------|--------|
| What's changing? | <schema, format, location, structure> |
| Who's affected? | <which services, agents, consumers> |
| Is it backward-compatible? | <yes: minor version, no: major version> |
| Can it be done incrementally? | <yes: phased, no: big-bang> |
| What's the rollback plan? | <how to undo if it fails> |

### 2. Design the migration

**Preferred: Expand-Migrate-Contract (backward-compatible)**
1. **Expand**: Add new field/format alongside old (both work)
2. **Migrate**: Update all consumers to use new format
3. **Contract**: Remove old field/format after all consumers updated

**If breaking change is unavoidable:**
1. Freeze writes (kill switch or feature flag)
2. Run migration script
3. Update all consumers
4. Verify
5. Resume writes

### 3. Write the migration script
```python
#!/usr/bin/env python3
"""Migration: <description>

Run: python -m your_project.migrations.<name>
Rollback: python -m your_project.migrations.<name> --rollback
"""

def migrate():
    # Read current data
    # Transform
    # Write to new location/format
    # Verify
    pass

def rollback():
    # Restore from backup
    pass

def verify():
    # Check migration succeeded
    # Count records before/after
    # Spot-check data integrity
    pass
```

### 4. Execute

```bash
# Backup
cp _state/cognition/ledger.jsonl _state/cognition/ledger.jsonl.pre-migration-$(date +%Y%m%d)

# Dry run
python -m your_project.migrations.<name> --dry-run

# Execute
python -m your_project.migrations.<name>

# Verify
python -m your_project.migrations.<name> --verify
```

### 5. Post migration record
```bash
python -m your_project.cognition post \
  --vendor "${AGENT_VENDOR:?set AGENT_VENDOR to the provider actually running}" --model "${AGENT_MODEL:?set AGENT_MODEL to the model actually running}" \
  --type decision --scope project \
  --content "MIGRATION: <description>. Records: <count>. Rollback: <available/not>." \
  --tags "migration"
# The skill invocation runtime injects the caller's canonical identity as agent.
```

## Output Format
```
Migration Plan | <description>
═══════════════════════════════

## What's Changing
<before -> after>

## Impact
<who/what is affected>

## Strategy: [EXPAND-MIGRATE-CONTRACT | BIG-BANG]
<rationale>

## Steps
1. <step with command>
2. <step>
3. <verify step>

## Rollback
<how to undo>

## Verification
<how to confirm success>
```

## Skill Chains

### Mandatory

- `[migration-check]` MUST pass before execution — pre-migration validation ensures schema compatibility, rollback feasibility, and data integrity before any destructive write.

### Advisory

- After `[migrate]` → `[test-run]` to verify migrated data integrity
- After `[migrate]` → `[decision-log]` to record the migration as an ADR
- Before `[migrate]` → `[schema-migrate]` if the migration is driven by a contract schema change

## Authority

- **T1 (TRUSTED)**: May run with `[migration-check]` passed
- **T2 (Active/High)**: Operator approval required + `[migration-check]` passed
- **T3 (Medium)**: Operator approval required + `[migration-check]` passed
- **T4 (Probationary)**: BLOCKED
- **Operator**: Override any restriction
