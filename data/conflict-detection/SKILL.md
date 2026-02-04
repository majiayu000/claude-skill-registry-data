---
name: conflict-detection
description: Use before creating new stories or when user asks "check for conflicts", "find duplicates", "review story overlaps", or "detect story conflicts" - scans story-tree database to identify duplicate stories, scope overlaps, and competing approaches using lightweight text similarity (no external dependencies).
---

# Conflict Detection

Detect duplicate and overlapping stories in the story-tree database.

**Database:** `.claude/data/story-tree.db`

**Critical:** Use Python sqlite3 module, NOT sqlite3 CLI.

## When to Run

1. **Before generating new stories** - prevent creating duplicates
2. **On user request** - audit existing stories for conflicts
3. **Periodically in CI** - catch conflicts early

## Conflict Types

| Type | Description | Confidence |
|------|-------------|------------|
| `duplicate` | Same story, different words | High (65%+ title sim) |
| `scope_overlap` | One subsumes or partially covers another | Medium (60%+ keyword containment) |
| `competing` | Same problem, incompatible approaches | Medium (40%+ want sim, low benefit) |

## Quick Scan

Run the detection script:

```python
python -c "
import subprocess, sys
result = subprocess.run([sys.executable, '.claude/skills/conflict-detection/scripts/detect_conflicts.py'],
                       capture_output=True, text=True)
print(result.stdout)
if result.returncode > 0:
    print(f'Exit code {result.returncode} = {result.returncode} conflicts found')
"
```

## Usage Options

```bash
# Default scan (50% confidence threshold)
python .claude/skills/conflict-detection/scripts/detect_conflicts.py

# JSON output for programmatic use
python .claude/skills/conflict-detection/scripts/detect_conflicts.py --format json

# Lower threshold for more matches
python .claude/skills/conflict-detection/scripts/detect_conflicts.py --min-confidence 0.4

# Custom database path
python .claude/skills/conflict-detection/scripts/detect_conflicts.py --db path/to/story-tree.db
```

## Output Format

**Text (default):**
```
Found N potential conflict(s):

## Conflict 1: DUPLICATE (confidence: 94%)
**Story A**: `1.3.5` - Matter/Client Database Management
**Story B**: `1.8.1` - Matter/Client Database
**Reason**: Near-identical titles: title=85%
```

**JSON:**
```json
[{
  "story_a_id": "1.3.5",
  "story_b_id": "1.8.1",
  "conflict_type": "duplicate",
  "confidence": 0.94,
  "reason": "Near-identical titles: title=85%",
  "want_similarity": 0.45,
  "benefit_similarity": 0.32,
  "title_similarity": 0.85
}]
```

## Handling Conflicts

After detection, resolve conflicts by:

1. **Duplicates**: Merge stories or reject one
2. **Scope overlap**: Clarify boundaries or make one a child of the other
3. **Competing**: Choose an approach and document decision

Update story status to `rejected` for discarded stories with a note explaining the decision.

## Integration with Story Writing

Before generating stories for a node, check for conflicts:

```python
python -c "
import subprocess, sys, json
result = subprocess.run([sys.executable, '.claude/skills/conflict-detection/scripts/detect_conflicts.py',
                        '--format', 'json'], capture_output=True, text=True)
conflicts = json.loads(result.stdout) if result.stdout.strip().startswith('[') else []
if conflicts:
    print(f'WARNING: {len(conflicts)} existing conflicts - resolve before adding stories')
    for c in conflicts[:3]:
        print(f'  - {c[\"conflict_type\"]}: {c[\"story_a_id\"]} vs {c[\"story_b_id\"]}')
else:
    print('No conflicts detected - safe to proceed')
"
```

## Algorithm

1. Load active stories (skip rejected/archived)
2. Extract components: title, want, benefit, acceptance criteria
3. Normalize tokens using domain-specific synonym groups
4. Compare all pairs using:
   - Jaccard + containment similarity on normalized tokens
   - Acceptance criteria comparison (high signal)
   - Keyword containment ratio
5. Classify conflicts based on multi-signal scoring
6. Return sorted by confidence

**Constraints:**
- Python stdlib only (no numpy, sklearn, sentence-transformers)
- Runs in CI without external API calls
- O(n^2) comparison - fast for <500 stories

## Performance Characteristics

Tested against ground truth test cases:

| Category | Detection Rate | Notes |
|----------|---------------|-------|
| Duplicates | 100% (3/3) | High accuracy on title/criteria overlap |
| Scope Overlaps | 40% (2/5) | Limited by lexical similarity |
| False Positives | 0% | No false positives on negative cases |

**Known Limitation:** Stories using very different vocabulary to describe the same functionality may not be detected. This is inherent to lexical similarity without semantic embeddings.

**Tuning:** Lower `--min-confidence` to 0.40 for higher recall (more false positives).
