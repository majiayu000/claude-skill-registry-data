---
name: gate-routing
description: Use when a heartbeat needs to check if a story can progress through a gate. Checks prerequisites, dependencies, 3rd-party deps, and child story completion. Called by heartbeat workflows to determine hold_reason transitions.
---

# Gate Routing - Story Progression Gates

Check whether a story can progress through various gates, and update hold_reason accordingly.

**Database:** `.claude/data/story-tree.db`

**Critical:** Use Python sqlite3 module, NOT sqlite3 CLI.

## Usage

```
/gate-routing <story_id> <gate_type>
```

**Gate Types:**
- `readiness` - Planning→Implementing: Check 3rd-party deps + prerequisite stories
- `prerequisites` - Implementing (queued): Check if prerequisites are implemented
- `dependencies` - Implementing (blocked): Check if dependency children are planned
- `children` - Releasing (queued): Check if all children are at releasing+

## Gate Definitions

### 1. Readiness Gate (planning-queued → implementing)

Checks two conditions before a story can start implementing:

**A. 3rd-Party Dependencies** (from `dependencies` JSON field)
- External libraries, APIs, services that must be available
- Example: `["redis", "stripe-api", "aws-s3"]`
- **Check:** Verify each dependency is installed/accessible
- **If blocked:** Set `hold_reason = 'blocked'` with note listing missing deps

**B. Prerequisite Stories** (from `prerequisites` JSON field)
- Other story IDs that must complete first
- Example: `["1.2", "3.1.4"]`
- **Check:** Each prerequisite must have `stage IN ('implementing', 'testing', 'releasing') OR terminus = 'shipped'`
- **If blocked:** Set `hold_reason = 'queued'` with note listing pending prerequisites

**If all clear:** Set `hold_reason = NULL` (ready for implementing-nohold)

### 2. Prerequisites Gate (implementing-queued)

Rechecks prerequisite stories only:

```sql
SELECT id FROM story_nodes
WHERE id IN (SELECT value FROM json_each(
    (SELECT prerequisites FROM story_nodes WHERE id = '<story_id>')
))
AND stage NOT IN ('implementing', 'testing', 'releasing')
AND (terminus IS NULL OR terminus != 'shipped')
```

- **If any pending:** Stay `hold_reason = 'queued'`
- **If all complete:** Set `hold_reason = NULL`

### 3. Dependencies Gate (implementing-blocked)

Check if dependency child stories have progressed enough:

A story enters `blocked` when it has children that represent dependencies (plan decomposition created them). These children must reach `planning` stage before the parent can proceed.

```sql
SELECT id FROM story_nodes
WHERE parent_id = '<story_id>'
AND stage = 'concept'
AND terminus IS NULL
```

- **If any children still at concept:** Stay `hold_reason = 'blocked'`
- **If all children at planning+:** Set `hold_reason = 'queued'` (now check prerequisites)

### 4. Children Gate (releasing-queued)

For parent stories to release, all children must be at releasing stage or shipped:

```sql
SELECT id FROM story_nodes
WHERE parent_id = '<story_id>'
AND stage NOT IN ('releasing')
AND (terminus IS NULL OR terminus != 'shipped')
```

- **If any children not at releasing+:** Stay `hold_reason = 'queued'`
- **If all children at releasing+ or shipped:** Set `hold_reason = NULL`

## Implementation

### Step 1: Load Story and Parse Fields

```python
import sqlite3
import json

conn = sqlite3.connect('.claude/data/story-tree.db')
conn.row_factory = sqlite3.Row

story = conn.execute('''
    SELECT id, stage, hold_reason, dependencies, prerequisites
    FROM story_nodes WHERE id = ?
''', (story_id,)).fetchone()

deps = json.loads(story['dependencies']) if story['dependencies'] else []
prereqs = json.loads(story['prerequisites']) if story['prerequisites'] else []
```

### Step 2: Run Gate Check

Based on gate_type argument, run the appropriate check:

```python
def check_readiness_gate(conn, story_id, deps, prereqs):
    """Check both 3rd-party deps and prerequisite stories."""
    issues = []

    # Check 3rd-party dependencies (simplified - just note them)
    if deps:
        # In practice, you'd check if these are actually available
        # For now, assume they're available unless explicitly blocked
        pass

    # Check prerequisite stories
    if prereqs:
        pending = conn.execute('''
            SELECT id, stage, terminus FROM story_nodes
            WHERE id IN ({})
            AND stage NOT IN ('implementing', 'testing', 'releasing')
            AND (terminus IS NULL OR terminus != 'shipped')
        '''.format(','.join('?' * len(prereqs))), prereqs).fetchall()

        if pending:
            issues.extend([f"Prerequisite {p['id']} at {p['stage']}" for p in pending])

    return issues

def check_prerequisites_gate(conn, story_id, prereqs):
    """Check only prerequisite stories."""
    if not prereqs:
        return []

    pending = conn.execute('''
        SELECT id, stage FROM story_nodes
        WHERE id IN ({})
        AND stage NOT IN ('implementing', 'testing', 'releasing')
        AND (terminus IS NULL OR terminus != 'shipped')
    '''.format(','.join('?' * len(prereqs))), prereqs).fetchall()

    return [f"Prerequisite {p['id']} at {p['stage']}" for p in pending]

def check_dependencies_gate(conn, story_id):
    """Check if child dependency stories have reached planning."""
    children_at_concept = conn.execute('''
        SELECT id FROM story_nodes
        WHERE parent_id = ?
        AND stage = 'concept'
        AND terminus IS NULL
    ''', (story_id,)).fetchall()

    return [f"Child {c['id']} still at concept" for c in children_at_concept]

def check_children_gate(conn, story_id):
    """Check if all children are at releasing+ or shipped."""
    pending_children = conn.execute('''
        SELECT id, stage FROM story_nodes
        WHERE parent_id = ?
        AND stage NOT IN ('releasing')
        AND (terminus IS NULL OR terminus != 'shipped')
    ''', (story_id,)).fetchall()

    return [f"Child {c['id']} at {c['stage']}" for c in pending_children]
```

### Step 3: Update Story Based on Result

```python
def update_hold_reason(conn, story_id, new_hold, note=None):
    """Update hold_reason and optionally append to notes."""
    if note:
        conn.execute('''
            UPDATE story_nodes
            SET hold_reason = ?,
                notes = COALESCE(notes, '') || ? || char(10),
                updated_at = datetime('now')
            WHERE id = ?
        ''', (new_hold, f"[gate-routing] {note}", story_id))
    else:
        conn.execute('''
            UPDATE story_nodes
            SET hold_reason = ?,
                updated_at = datetime('now')
            WHERE id = ?
        ''', (new_hold, story_id))
    conn.commit()
```

## Decision Logic

| Gate | Issues Found | Action |
|------|--------------|--------|
| `readiness` | 3rd-party deps missing | `hold_reason = 'blocked'` |
| `readiness` | Prerequisites pending | `hold_reason = 'queued'` |
| `readiness` | All clear | `hold_reason = NULL` |
| `prerequisites` | Any pending | Stay `hold_reason = 'queued'` |
| `prerequisites` | All complete | `hold_reason = NULL` |
| `dependencies` | Children at concept | Stay `hold_reason = 'blocked'` |
| `dependencies` | All children planned+ | `hold_reason = 'queued'` |
| `children` | Children not releasing | Stay `hold_reason = 'queued'` |
| `children` | All at releasing+ | `hold_reason = NULL` |

## Output Format

Report the gate check result:

```
GATE CHECK: {gate_type}
Story: {story_id}
Current hold: {hold_reason}

Checks:
- [PASS/FAIL] {check_description}
- [PASS/FAIL] {check_description}

Result: {CLEAR | BLOCKED | QUEUED}
New hold_reason: {new_value or NULL}
```

## References

- **Database:** `.claude/data/story-tree.db`
- **Schema:** `.claude/skills/story-tree/references/schema.sql`
- **Heartbeat workflows:** `.github/workflows/heartbeat-*.yml`
