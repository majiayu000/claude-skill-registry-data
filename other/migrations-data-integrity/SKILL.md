---
name: migrations-data-integrity
description: 'Design safe Django schema/data migrations for HIVMeet backend. Use for model evolution, data backfill, constraints, transactional safety, rollback planning, and deployment-safe migration sequencing.'
argument-hint: 'Describe model changes, expected data transitions, table size/risk, and deployment constraints.'
user-invocable: true
---

# Migrations and Data Integrity

## Purpose
Evolve database schema and data without integrity loss, prolonged downtime, or release instability.

## Use When
- Changing Django models
- Adding/removing constraints/indexes
- Performing data backfills
- Resolving migration conflicts or failed deploy migrations

## Mandatory Workflow

### 1. Change Classification
- Classify migration type: schema-only, data-only, mixed
- Estimate blast radius: row count, lock risk, critical tables
- Identify backward compatibility needs across deploy steps

### 2. Safe Migration Design
- Prefer additive first (new nullable column, backfill, then enforce)
- Split risky operations into small migrations
- Use RunPython for deterministic, idempotent backfill logic

### 3. Transaction and Lock Strategy
- Use atomic operations where feasible
- Avoid long-running locks on hot tables when possible
- Plan phased rollout for large data transitions

### 4. Data Integrity Controls
- Validate unique constraints before enforcing
- Validate foreign-key consistency before tightening relations
- Validate default values and nullability transitions

### 5. Rollback and Recovery Plan
- Define reverse migration behavior when possible
- For irreversible steps, document explicit recovery playbook
- Keep backup/restore and operator instructions clear

### 6. Verification Before and After
- Run makemigrations and inspect generated migration files
- Apply migrations in clean and representative environments
- Verify key queries and application behavior post-migration

### 7. Output Contract
1. Migration type and risk profile
2. Files/migrations created or updated
3. Integrity checks performed
4. Rollback/recovery instructions
5. Validation results and residual risk

## Quality Gates
- No model change merged without migration file
- No high-risk backfill without explicit validation and fallback plan
- No constraint hardening without pre-check on existing data
