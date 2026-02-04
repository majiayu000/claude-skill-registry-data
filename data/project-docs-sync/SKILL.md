---
name: project-docs-sync
description: Automatically synchronize project documentation when major changes occur (new tech, architecture changes, requirements shifts). Detects significant updates and propagates changes across TECH-STACK.md, ARCHITECTURE.md, and SPECIFICATIONS.md.
---

# Project Documentation Sync Skill

**Purpose**: Keep project documentation consistent without manual syncing overhead.

**Trigger**: Auto-invoked by PostToolUse hook when files in `project-management/` are edited.

---

## Decision Logic: Should We Sync?

```python
def should_sync(change: dict) -> tuple[bool, str]:
    """Conservative sync decision - only on big changes."""

    # Track last sync state
    last_sync = load_last_sync()  # from .meta/last-sync.json

    significant_changes = {
        # Technology changes
        "added_technology": True,      # New language, framework, library
        "removed_technology": True,    # Deprecated/removed tech
        "upgraded_major_version": True, # React 17 → 18, Python 3.10 → 3.11

        # Architecture changes
        "added_service": True,         # New microservice, component
        "removed_service": True,       # Deprecated service
        "changed_data_flow": True,     # New integration pattern
        "added_integration": True,     # New third-party API

        # Requirements changes
        "new_security_requirement": True,
        "new_performance_requirement": True,
        "changed_api_contract": True,
        "added_compliance_need": True,
    }

    # Skip minor changes
    minor_changes = {
        "typo_fix": False,
        "formatting": False,
        "comment_update": False,
        "example_clarification": False,
    }

    change_type = classify_change(change, last_sync)
    return significant_changes.get(change_type, False), change_type
```

---

## What Gets Synced (Conservative Strategy)

### 1. TECH-STACK.md Changed → Update ARCHITECTURE.md

**Triggers:**
- Added new language/framework (e.g., added Redis)
- Removed technology (e.g., removed MongoDB)
- Major version upgrade (e.g., React 17 → 18)

**Sync Actions:**
```markdown
TECH-STACK.md shows:
+ Redis 7.x (added for caching)

→ Update ARCHITECTURE.md:
  - Add Redis component to architecture diagram
  - Add caching layer to data flow
  - Document Redis connection pattern
```

**Example Output:**
```
✓ Synced TECH-STACK.md → ARCHITECTURE.md
  - Added: Redis caching layer
  - Updated: Data flow diagram (added cache lookup)
  - Reason: New technology requires architectural integration
```

---

### 2. ARCHITECTURE.md Changed → Update SPECIFICATIONS.md

**Triggers:**
- New service/component added
- API gateway pattern introduced
- Data model changed
- Integration pattern modified

**Sync Actions:**
```markdown
ARCHITECTURE.md shows:
+ API Gateway (Kong) added between clients and services

→ Update SPECIFICATIONS.md:
  - Add API Gateway endpoints
  - Update authentication flow
  - Add rate limiting specs
  - Update API contract examples
```

**Example Output:**
```
✓ Synced ARCHITECTURE.md → SPECIFICATIONS.md
  - Added: API Gateway endpoint specs
  - Updated: Authentication flow (now via gateway)
  - Reason: Architectural change affects API contracts
```

---

### 3. PROJECT-OVERVIEW.md Changed → Validate Consistency

**Triggers:**
- Project scope changed
- New requirement category added
- Compliance requirement added
- Target users changed

**Sync Actions:**
```markdown
PROJECT-OVERVIEW.md shows:
+ Compliance: GDPR data privacy required

→ Validate across all docs:
  - Check TECH-STACK.md has encryption libraries
  - Check ARCHITECTURE.md has data privacy layer
  - Check SPECIFICATIONS.md has GDPR endpoints (data export, deletion)
  - Flag missing pieces
```

**Example Output:**
```
⚠ Validation: PROJECT-OVERVIEW.md → ALL DOCS
  - Missing in TECH-STACK.md: No encryption library listed
  - Missing in SPECIFICATIONS.md: No GDPR data export endpoint
  - Recommendation: Add encryption lib + GDPR API specs
```

---

## Change Detection Algorithm

```python
def classify_change(file_path: str, diff: str, last_sync: dict) -> str:
    """Classify change significance using diff analysis."""

    # Parse diff
    added_lines = [line for line in diff.split('\n') if line.startswith('+')]
    removed_lines = [line for line in diff.split('\n') if line.startswith('-')]

    # Check for technology changes
    tech_keywords = ['framework', 'library', 'language', 'database', 'cache']
    if any(kw in line.lower() for line in added_lines for kw in tech_keywords):
        if any(removed_lines):  # Replacement
            return "upgraded_major_version"
        return "added_technology"

    # Check for architecture changes
    arch_keywords = ['service', 'component', 'layer', 'gateway', 'microservice']
    if any(kw in line.lower() for line in added_lines for kw in arch_keywords):
        return "added_service"

    # Check for requirement changes
    req_keywords = ['security', 'performance', 'compliance', 'GDPR', 'HIPAA']
    if any(kw in line.lower() for line in added_lines for kw in req_keywords):
        return "new_security_requirement"

    # Check for API contract changes
    if 'endpoint' in diff.lower() or 'route' in diff.lower():
        return "changed_api_contract"

    # Default: minor change (skip sync)
    if len(added_lines) < 3 and not removed_lines:
        return "typo_fix"

    return "unknown_change"
```

---

## Sync State Tracking

**Storage**: `.meta/last-sync.json`

```json
{
  "last_sync_timestamp": "2025-10-30T14:30:00Z",
  "synced_files": {
    "project-management/TECH-STACK.md": {
      "hash": "abc123",
      "last_modified": "2025-10-30T14:00:00Z",
      "change_type": "added_technology"
    },
    "project-management/ARCHITECTURE.md": {
      "hash": "def456",
      "last_modified": "2025-10-30T14:30:00Z",
      "synced_from": "TECH-STACK.md"
    }
  },
  "pending_syncs": []
}
```

**Update Logic**:
1. After Write/Edit to `project-management/*.md`
2. Calculate file hash (md5 of content)
3. Compare with last sync state
4. If different + significant change → Trigger sync
5. Update `.meta/last-sync.json`

---

## Sync Execution Flow

```
PostToolUse Hook Fires
      ↓
File edited: project-management/TECH-STACK.md
      ↓
Load .meta/last-sync.json
      ↓
Calculate diff from last sync
      ↓
Classify change: "added_technology" (Redis)
      ↓
Decision: should_sync() → TRUE
      ↓
┌────────────────────────────────────┐
│ Sync: TECH-STACK → ARCHITECTURE    │
│ - Read TECH-STACK.md additions     │
│ - Identify: Redis 7.x (cache)      │
│ - Update ARCHITECTURE.md:          │
│   + Add Redis component            │
│   + Update data flow               │
└────────────────────────────────────┘
      ↓
Write updated ARCHITECTURE.md
      ↓
Update .meta/last-sync.json
      ↓
Log sync action
      ↓
Output brief sync report
```

---

## Sync Report Format

```markdown
## Documentation Sync Report

**Trigger**: TECH-STACK.md modified (added Redis)
**Timestamp**: 2025-10-30T14:30:00Z

---

### Changes Detected: 1

1. **[SIGNIFICANT] Added technology: Redis 7.x**
   - **Source**: project-management/TECH-STACK.md:45
   - **Purpose**: Caching layer for API responses

---

### Syncs Applied: 2

1. **TECH-STACK.md → ARCHITECTURE.md**
   - ✓ Added: Redis component to architecture diagram
   - ✓ Updated: Data flow (added cache lookup step)
   - ✓ File: project-management/ARCHITECTURE.md:120-135

2. **TECH-STACK.md → SPECIFICATIONS.md**
   - ✓ Added: Cache invalidation API endpoint
   - ✓ Updated: Response time expectations (now <100ms with cache)
   - ✓ File: project-management/SPECIFICATIONS.md:78-82

---

### Validation Checks: 2

✓ TECH-STACK.md consistency: OK
✓ ARCHITECTURE.md alignment: OK

---

**Result**: Documentation synchronized successfully.
**Next Action**: Review changes in next commit.
```

---

## Integration with PostToolUse Hook

**Hook Location**: `.claude/hooks/post_tool_use_format.py`

**Trigger Condition**:
```python
def should_trigger_docs_sync(file_path: str, tool_name: str) -> bool:
    """Only trigger on project-management doc edits."""

    if tool_name not in ["Write", "Edit"]:
        return False

    project_docs = [
        "project-management/TECH-STACK.md",
        "project-management/ARCHITECTURE.md",
        "project-management/PROJECT-OVERVIEW.md",
        "project-management/SPECIFICATIONS.md",
    ]

    return any(doc in file_path for doc in project_docs)
```

**Invocation**:
```python
# In PostToolUse hook
if should_trigger_docs_sync(file_path, tool_name):
    # Load skill
    skill_result = invoke_skill("project-docs-sync", {
        "file_path": file_path,
        "change_type": classify_change(file_path, diff),
        "last_sync_state": load_last_sync()
    })

    # Log sync action
    log_sync_action(skill_result)
```

---

## Sync Strategies by File Type

### TECH-STACK.md → ARCHITECTURE.md
**What to sync:**
- New databases → Add data layer component
- New frameworks → Add to tech stack diagram
- New APIs → Add integration points
- Version upgrades → Update compatibility notes

### ARCHITECTURE.md → SPECIFICATIONS.md
**What to sync:**
- New services → Add service endpoints
- New integrations → Add API contracts
- Data model changes → Update request/response schemas
- Security layers → Add authentication specs

### PROJECT-OVERVIEW.md → ALL DOCS
**What to validate:**
- Compliance requirements → Check encryption in TECH-STACK
- Performance goals → Check caching in ARCHITECTURE
- Target users → Check API design in SPECIFICATIONS
- Scope changes → Validate alignment across all docs

---

## Conservative Sync Rules

**DO Sync When:**
- ✅ New technology added (database, framework, library)
- ✅ Service/component added or removed
- ✅ API contract changed (new endpoint, schema change)
- ✅ Compliance requirement added (GDPR, HIPAA)
- ✅ Major version upgrade (breaking changes possible)

**DO NOT Sync When:**
- ❌ Typo fixes (1-2 character changes)
- ❌ Formatting changes (whitespace, markdown)
- ❌ Comment/example clarifications
- ❌ Documentation of existing features (no new info)
- ❌ Minor version bumps (patch releases)

---

## Error Handling

**If sync fails:**
1. Log error to `.meta/sync-errors.log`
2. Add to pending syncs in `.meta/last-sync.json`
3. Report to user with clear action items
4. Do NOT block the write operation (non-blocking)

**Example Error Report:**
```
⚠ Documentation Sync Failed

**File**: project-management/TECH-STACK.md
**Error**: Could not parse ARCHITECTURE.md (syntax error)
**Action Required**:
  1. Fix ARCHITECTURE.md syntax error (line 45)
  2. Re-run: /lazy docs-sync

**Pending Syncs**: 1 (tracked in .meta/last-sync.json)
```

---

## Configuration

```bash
# Disable auto-sync (manual /lazy docs-sync only)
export LAZYDEV_DISABLE_DOCS_SYNC=1

# Sync everything (even minor changes)
export LAZYDEV_DOCS_SYNC_AGGRESSIVE=1

# Sync specific files only
export LAZYDEV_DOCS_SYNC_FILES="TECH-STACK.md,ARCHITECTURE.md"
```

---

## What This Skill Does NOT Do

❌ Sync code files (only project-management docs)
❌ Generate docs from scratch (use `/lazy docs`)
❌ Fix documentation errors (use `/lazy fix`)
❌ Create missing docs (use `/lazy plan`)

✅ **DOES**: Automatically propagate significant changes across project documentation with conservative triggers.

---

**Version**: 1.0.0
**Non-blocking**: Syncs in background, logs errors
**Speed**: <2 seconds for typical sync
