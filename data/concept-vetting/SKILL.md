---
name: concept-vetting
description: Use when orchestrator generates new concepts or user says "vet concepts", "check conflicts", "find duplicates", "scan for overlaps" - scans story-tree database to detect duplicate, overlapping, or competing concepts. Returns conflict pairs with types and confidence scores for human review.
disable-model-invocation: true
---

# Concept Vetting - Automated Concept Conflict Resolution

Detect and resolve conflicting concepts in the story-tree database. This skill **vets concepts** before presenting them to humans - most conflicts are resolved automatically.

**Database:** `.claude/data/story-tree.db`

**Critical:** Use Python sqlite3 module, NOT sqlite3 CLI.

**Platform Note:** All Python commands use `python` (not `python3`) for cross-platform compatibility.

## Architecture Overview

```
Phase 1: Candidate Detection (Python script)
├── Run keyword/similarity heuristics
├── Output CANDIDATE pairs (potential conflicts)
└── No classification — just "these might conflict"

Phase 2: Classification & Resolution (Main Agent)
├── For each candidate pair:
│   ├── Read both story descriptions
│   ├── Classify: duplicate / scope_overlap / competing / incompatible / false_positive
│   ├── Look up action (deterministic based on classification + effective status)
│   └── Execute action (LLM for merges, Python for deletes/three-field updates)
└── Present only HUMAN REVIEW cases interactively
```

## Decision Matrix

The skill vets **concepts only** — deciding what ideas to present to the human.

### Conflict Types

| Type | Description |
|------|-------------|
| `duplicate` | Essentially the same story |
| `scope_overlap` | One subsumes or partially covers another |
| `competing` | Same problem, different/incompatible approaches |
| `incompatible` | Mutually exclusive approaches that cannot be merged |
| `false_positive` | Flagged by heuristics but not actually conflicting |

### Automated Actions

| Conflict Type | Concept vs... | Action |
|---------------|---------------|--------|
| **DUPLICATE** | `wishlist`, `refine` | TRUE MERGE → keep stage |
| **DUPLICATE** | `concept` | TRUE MERGE → concept |
| **DUPLICATE** | everything else | DELETE concept |
| **SCOPE_OVERLAP** | `concept` | TRUE MERGE → concept |
| **SCOPE_OVERLAP** | any other | HUMAN REVIEW |
| **COMPETING** | `concept`, `wishlist`, `refine` | TRUE MERGE |
| **COMPETING** | `rejected`, `infeasible`, `duplicative`, `broken`, `queued`, `pending`, `blocked`, `conflict` | BLOCK concept with note |
| **COMPETING** | everything else | AUTO-DUPLICATIVE with note (not a goal signal) |
| **INCOMPATIBLE** | `concept` | Claude picks better, DELETE other |
| **FALSE_POSITIVE** | — | SKIP (no action) |
| **Non-concept vs non-concept** | — | IGNORE |

### Effective Status Reference

Effective status is computed as `COALESCE(terminus, hold_reason, stage)`.

**Mergeable with concepts:**
- `stage = 'concept'`
- `hold_reason = 'wishlisted'`
- `hold_reason = 'polish'`
- `hold_reason = 'refine'`

**Block against:**
- `terminus IN ('rejected', 'infeasible', 'duplicative')`
- `hold_reason IN ('broken', 'queued', 'escalated', 'blocked', 'conflicted')`

**Auto-duplicative against:**
- `stage IN ('planning', 'implementing', 'reviewing', 'implemented', 'ready', 'polish', 'released')`
- `terminus IN ('legacy', 'deprecated', 'archived')`

### Three-Field System Internals

The vetting system computes a pseudo-status field using:
```sql
COALESCE(terminus, hold_reason, stage) AS status
```

Priority: terminus (terminal) > hold_reason (paused) > stage (position)

This means:
- Story with `terminus='rejected'` shows status='rejected' regardless of stage
- Story with `hold_reason='escalated'` shows status='escalated' (stage preserved for resume)
- Story with only stage set shows that stage value

---

## CI Mode

When running in CI (non-interactive environment), HUMAN_REVIEW cases cannot prompt for input. Instead:

- **HUMAN_REVIEW → DEFER_PENDING**: Set concept `hold_reason = 'refine'` with note listing conflicting story-node IDs (e.g., "Scope overlap detected with story-node IDs: 3.2.1, 4.1.1.3")
- All other automated actions work the same

**Detection**: CI mode is active when running in GitHub Actions or when explicitly specified.

**Purpose of refine status**: Stories set to `refine` should be reworked to eliminate scope overlaps before proceeding to approval.

---

## Decision Cache

The vetting system uses a persistent cache to avoid re-classifying the same story pairs on each run. This is especially important when running vetting daily, as most pairs will be false positives that don't need repeated LLM analysis.

### How It Works

1. **Version Tracking**: Each `story_nodes` record has a `version` column (INTEGER, default 1)
2. **Cache Storage**: Classification decisions are stored in `vetting_decisions` table with:
   - Canonical pair key (smaller ID first, e.g., `1.1|1.8.4`)
   - Version numbers at time of decision
   - Classification and action taken
3. **Invalidation**: When a story's `title`, `description`, `stage`, `hold_reason`, or `terminus` changes, increment its `version`. All cached pairs involving that story become stale.

### Cache Behavior

- **First run (cold cache)**: All 238 candidates processed by LLM, decisions stored
- **Subsequent runs (warm cache)**: ~150-180 false_positives skipped, only stale/new pairs classified
- **After story edit**: Pairs involving edited story re-enter Phase 2

### Reporting Cache Operations

When reporting cache activity, use specific language:

| Avoid | Use Instead |
|-------|-------------|
| "Stored 3 decisions" | "Cached 3 new conflict classifications (will skip on future runs)" |
| "Cache: stored..." | "Decision cache: recorded 3 pair classifications to avoid re-analysis" |
| "Cached for future runs" | "Cached to skip LLM re-classification on next run" |

**Why clear language matters**: "Stored" is ambiguous - it could mean written to database, saved to file, or something else. Explicit language helps users understand that cached decisions let future vetting runs skip pairs that have already been classified.

### CLI Commands

```bash
# Run schema migration (safe to run multiple times)
python .claude/skills/concept-vetting/vetting_cache.py migrate

# View cache statistics
python .claude/skills/concept-vetting/vetting_cache.py stats

# Clear all cached decisions
python .claude/skills/concept-vetting/vetting_cache.py clear
```

---

## Phase 1: Candidate Detection

Run the detector script to find candidate conflict pairs:

```bash
python .claude/skills/concept-vetting/candidate_detector.py
```

**What it does:** Scans all stories, applies keyword/similarity heuristics, filters cached false_positives, outputs candidate pairs as JSON.

**Output format:**
```json
{
  "total_stories": N,
  "candidates_before_cache": N,
  "candidates_after_cache": N,
  "cache_hits": {"false_positive": N, "other_cached": N, "uncached": N},
  "candidates": [
    {
      "story_a": {"id": "...", "title": "...", "status": "...", "description": "..."},
      "story_b": {"id": "...", "title": "...", "status": "...", "description": "..."},
      "signals": {"shared_keywords": [...], "title_similarity": 0.XX, ...}
    }
  ]
}
```
*Note: The `status` field is computed as `COALESCE(terminus, hold_reason, stage)` from the three-field system.*

**Detection thresholds:** Pairs flagged if any: shared implementation keywords ≥1, title Jaccard >0.15, title overlap >0.4, description Jaccard >0.10.

---

## Phase 2: Classification & Resolution

For each candidate pair from Phase 1, the main agent must:

### Step 1: Classify the Conflict

Read both story descriptions and determine the conflict type:

- **duplicate**: Stories describe essentially the same feature/requirement
- **scope_overlap**: One story's scope partially overlaps with another (but they're distinct)
- **competing**: Same problem, but different/incompatible solution approaches
- **incompatible**: Two concepts with mutually exclusive approaches (cannot merge)
- **false_positive**: Heuristics flagged it, but stories are actually unrelated

### Step 2: Determine Action

Use this lookup based on classification and effective statuses (computed from three-field system):

```python
# Effective status = COALESCE(terminus, hold_reason, stage)
# Note: concept=stage, wishlisted/polish/refine=hold_reason
MERGEABLE_STATUSES = {'concept', 'wishlisted', 'polish', 'refine'}
BLOCK_STATUSES = {'rejected', 'infeasible', 'duplicative', 'broken', 'queued', 'escalated', 'blocked', 'conflicted'}

def get_action(conflict_type, eff_status_a, eff_status_b, ci_mode=False):
    # Ensure concept is always story_a for consistent logic
    if eff_status_b == 'concept' and eff_status_a != 'concept':
        eff_status_a, eff_status_b = eff_status_b, eff_status_a

    if conflict_type == 'false_positive':
        return 'SKIP'

    if conflict_type == 'duplicate':
        if eff_status_b in MERGEABLE_STATUSES:
            return 'TRUE_MERGE'
        else:
            return 'DELETE_CONCEPT'

    if conflict_type == 'scope_overlap':
        if eff_status_a == 'concept' and eff_status_b == 'concept':
            return 'TRUE_MERGE'
        else:
            # In CI mode, defer to pending instead of blocking for human input
            return 'DEFER_PENDING' if ci_mode else 'HUMAN_REVIEW'

    if conflict_type == 'competing':
        if eff_status_b in MERGEABLE_STATUSES:
            return 'TRUE_MERGE'
        elif eff_status_b in BLOCK_STATUSES:
            return 'BLOCK_CONCEPT'
        else:
            return 'DUPLICATIVE_CONCEPT'

    if conflict_type == 'incompatible':
        # Claude picks the better concept, deletes the other
        return 'PICK_BETTER'

    return 'SKIP'
```

### Step 3: Execute Action

Use the actions script: `python .claude/skills/concept-vetting/vetting_actions.py <action> <args...>`

| Action | Command | Description |
|--------|---------|-------------|
| DELETE_CONCEPT | `python ...vetting_actions.py delete <concept_id>` | Remove concept from database |
| DUPLICATIVE_CONCEPT | `python ...vetting_actions.py duplicative <concept_id> <duplicate_of_id>` | Set terminus=duplicative (not a goal signal) |
| BLOCK_CONCEPT | `python ...vetting_actions.py block <concept_id> <blocking_id>` | Set hold_reason=blocked with note |
| DEFER_PENDING | `python ...vetting_actions.py defer <concept_id> <conflicting_id>` | Set hold_reason=pending (CI mode) |
| TRUE_MERGE | `python ...vetting_actions.py merge <keep_id> <delete_id> "<title>" "<desc>"` | Combine stories, delete one |
| CACHE | `python ...vetting_actions.py cache <id_a> <id_b> <classification> <action>` | Store decision in cache |

#### TRUE_MERGE Process

Before calling merge, Claude must:
1. Read both descriptions carefully
2. Create merged title (concise, captures both scopes)
3. Create merged description combining best "As a user..." statement, deduplicated acceptance criteria, unique details
4. Keep the story with lower/earlier ID (more established in hierarchy)

#### PICK_BETTER

For incompatible concepts, Claude evaluates which is better based on clarity, feasibility, project alignment, technical soundness. Then use DELETE on the worse concept.

#### HUMAN_REVIEW

Present stories side-by-side, offer options: [A] Reject A, [B] Reject B, [M] Merge, [S] Skip. Execute chosen action.

---

## Workflow Summary

1. **Run Phase 1** - Execute candidate detection Python script
2. **Parse results** - Load candidate pairs from JSON output
3. **For each candidate:**
   - Read both story descriptions
   - Classify conflict type (duplicate/scope_overlap/competing/incompatible/false_positive)
   - Look up action from decision matrix (pass `ci_mode=True` in CI environment)
   - Execute action (auto for most, DEFER_PENDING for scope overlaps in CI)
4. **Report summary** - Show counts of actions taken

### Expected Output (Interactive)

```
STORY VETTING COMPLETE
======================

Candidates scanned: 45
Actions taken:
  - Deleted: 8 duplicate concepts
  - Merged: 12 concept pairs
  - Duplicative: 3 competing concepts
  - Blocked: 2 concepts
  - Skipped: 15 false positives
  - Human review: 5 scope overlaps

Human review required for 5 conflicts (see above).
```

### Expected Output (CI Mode)

```
STORY VETTING COMPLETE (CI MODE)
================================

Candidates scanned: 45
Actions taken:
  - Deleted: 8 duplicate concepts
  - Merged: 12 concept pairs
  - Duplicative: 3 competing concepts
  - Blocked: 2 concepts
  - Skipped: 15 false positives
  - Needs refinement: 5 scope overlaps

5 concepts set to hold_reason='refine' for scope overlap resolution.
```

---

## References

- **Database:** `.claude/data/story-tree.db`
- **Schema:** `.claude/skills/story-tree/references/schema.sql`
- **SQL Queries:** `.claude/skills/story-tree/references/sql-queries.md`
- **Three-Field System:** `.claude/skills/story-tree/SKILL.md` (stage + hold_reason + terminus)
- **Shared Utilities:** `.claude/skills/story-tree/utility/story_db_common.py` (DB_PATH, delete_story, reject_concept, etc.)
