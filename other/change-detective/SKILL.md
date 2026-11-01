---
name: change-detective
description: Change Detective — Institutional capability and runbook for change-detective.
---

# SKILL: Change Detective
## Domain: Autonomous Change Detection, Auto-Documentation, Drift Analysis

**Activation triggers:** change detection, detect changes, what changed, diff
analysis, auto-document, schema drift, API drift, type drift, undocumented change,
changelog, audit trail, memory update, codebase drift.

---

## What the Change Detective Does

The Change Detective is an **autonomous observer** that:
1. Detects all code changes since a reference point (last commit, last deploy, merge-base)
2. Classifies changes by impact (breaking / non-breaking / cosmetic)
3. Auto-documents changes into `software-factory/memory/`
4. Flags schema, API, and type-level regressions before they reach production

---

## Running the Change Detector

```bash
# Detect changes since last commit
python3 software-factory/context-engine/change_detector.py --since HEAD~1

# Detect changes since branching from main
python3 software-factory/context-engine/change_detector.py \
  --since $(git merge-base HEAD main)

# Detect and auto-document (writes to memory/)
python3 software-factory/context-engine/change_detector.py \
  --since HEAD~1 --document

# Watch mode — re-run on every file save (during active dev)
python3 software-factory/context-engine/change_detector.py --watch

# Specific scope
python3 software-factory/context-engine/change_detector.py \
  --since HEAD~1 --scope integral-expert-backend/
```

---

## Change Classification Matrix

```
Category            | Examples                        | Action Required
────────────────────|─────────────────────────────────|─────────────────────────
BREAKING API        | route removed, field removed,   | Update TypeScript types,
                    | response schema changed          | version route (/v2/)
BREAKING SCHEMA     | column removed, type changed,   | Write migration, test
                    | FK constraint added              | rollback
NEW API             | new endpoint, new field added   | Update TS types, add test
NEW SCHEMA          | new table/column                | Migration already exists?
SECURITY            | auth removed, CORS changed,     | Run security-audit skill
                    | new plaintext credential        | immediately
PERFORMANCE         | new N+1 query, missing index,   | Run explain analyze
                    | cache removed                   | before merging
COSMETIC            | rename, comment, formatting     | No action needed
```

---

## Autonomous Documentation Pattern

After detecting changes, the detective writes structured memory entries:

```python
# change_detector.py output format (written to memory/):

## 2026-05-25 — Auto-detected changes on branch feature/copy-trading-risk

### API Changes (integral-expert-backend)
- ADDED:   POST /api/v1/copy-trading/subscriptions/{id}/pause
- MODIFIED: GET /api/v1/journal/trades — added `symbol` filter param

### Schema Changes
- ADDED column: copy_trading.subscriptions.paused_at (TIMESTAMP, nullable)
- MIGRATION: alembic/versions/012_add_subscription_pause.py ✅

### Type Changes (frontend)
- MODIFIED: CopySubscription — added paused_at?: string | null

### Files Changed
- integral-expert-backend/app/models/copy_trading/__init__.py
- integral-expert-backend/app/api/v1/endpoints/copy_trading/subscriptions.py
- app/src/shared/api/types/copyTrading.ts
```

---

## Manual Change Investigation (Agent Protocol)

When a bug or unexpected behavior is found:

```bash
# Step 1: Find when the behavior changed
git log --oneline --all -- <affected-file>

# Step 2: Diff the relevant period
git diff HEAD~5 HEAD -- integral-expert-backend/app/api/v1/endpoints/auth.py

# Step 3: Use CodeGraph to find all callers of changed function
codegraph_callers("changed_function_name")

# Step 4: Check if TypeScript types are still in sync
grep -r "interface.*Response\|type.*Response" app/src/shared/api/types/ | \
  grep -i "<changed-field>"

# Step 5: Check DB schema matches model
cd integral-expert-backend && source venv/bin/activate && alembic check

# Step 6: Document the finding
python3 software-factory/context-engine/change_detector.py \
  --since <commit-before-bug> --document
```

---

## Schema Drift Detection

```bash
# Detect if DB schema has drifted from SQLAlchemy models
cd integral-expert-backend && source venv/bin/activate
alembic check        # exits non-zero if drift detected
alembic revision --autogenerate -m "detect_drift"
# Then inspect the generated file — if non-empty, drift exists

# For quick visual diff:
python3 -c "
from app.db.session import engine
from sqlalchemy import inspect
inspector = inspect(engine)
schemas = inspector.get_schema_names()
for schema in schemas:
    tables = inspector.get_table_names(schema=schema)
    print(f'{schema}: {tables}')
"
```

---

## API Contract Drift Detection

```bash
# Compare current OpenAPI schema against last known-good
curl -s http://localhost:8002/openapi.json > /tmp/current-openapi.json
diff <(cat software-factory/memory/api-snapshots/expert-latest.json | python3 -m json.tool) \
     <(cat /tmp/current-openapi.json | python3 -m json.tool)

# Save current snapshot (do this after every release)
cp /tmp/current-openapi.json \
   software-factory/memory/api-snapshots/expert-$(date +%Y%m%d).json
ln -sf expert-$(date +%Y%m%d).json \
   software-factory/memory/api-snapshots/expert-latest.json
```

---

## Autonomous Memory Update (Post-Implementation)

```bash
# After every feature ship — run this to auto-update memory:
python3 software-factory/context-engine/change_detector.py \
  --since $(git merge-base HEAD main) \
  --document \
  --output software-factory/memory/decisions/$(date +%Y-%m).md

# This writes a structured changelog entry with:
# - All files modified
# - API changes detected
# - Schema changes detected
# - Classification (breaking/non-breaking)
```

---

## Anti-Patterns

```
✗ Merging without running change_detector (silent breaking changes ship)
✗ Treating all changes as equal (breaking schema change ≠ comment edit)
✗ Memory entries written manually without change_detector (inconsistent format)
✗ Only detecting Python changes (TypeScript types drift silently too)
✗ Not saving OpenAPI snapshots (can't diff API changes later)
✗ Running change_detector AFTER a bug appears (run it in CI, not reactively)
```
