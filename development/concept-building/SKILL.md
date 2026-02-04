---
name: concept-building
description: Use when user says "build concepts", "generate stories", "create stories", "brainstorm stories", "brainstorm features", "create stories for [node]", or asks for new story ideas. Complete story lifecycle - generates evidence-based stories from git commits and gap analysis, validates quality, vets for conflicts, and retries up to 10 times if duplicates detected. Polishes stories with hold_reason='polish' FIRST before generating new ones. Supports multi-node batching. Does NOT commit - leaves that to caller.
disable-model-invocation: true
---

# Concept Building - Evidence-Based Generation with Vetting

Generate user stories grounded in git commits and gap analysis, with built-in duplicate detection.

**Database:** `.claude/data/story-tree.db`

**Critical:** Use Python sqlite3 module, NOT sqlite3 CLI.

---

## Critical Rules

> **A story is NOT complete until vetted.**
>
> This applies to ALL stories—AI-generated or user-provided.
> Never commit after insertion alone.

---

## Priority Order

1. **FIRST:** Polish any stories with `hold_reason='polish'`
2. **THEN:** Generate new stories for target node

```python
python -c "
import sqlite3, json
conn = sqlite3.connect('.claude/data/story-tree.db')
conn.row_factory = sqlite3.Row
stories = [dict(row) for row in conn.execute('''
    SELECT s.id, s.title, s.description, s.stage, s.hold_reason, s.notes,
           (SELECT ancestor_id FROM story_paths WHERE descendant_id = s.id AND depth = 1) as parent_id
    FROM story_nodes s WHERE s.hold_reason = 'polish' ORDER BY s.created_at
''').fetchall()]
print(json.dumps({'count': len(stories), 'stories': stories}, indent=2))
conn.close()
"
```

---

## Multi-Node Batching

When given multiple node IDs (e.g., "Generate stories for nodes: 1.2, 1.3"):

- Perform goals check and git analysis ONCE (shared context)
- Loop through nodes for context/gap/generation
- Max 1 story per node when batching, total max 2 stories
- Single combined output

**Token savings:** ~2,800 tokens per additional node.

---

## Select Workflow

| Context | Workflow |
|---------|----------|
| GitHub Actions / Automation | `references/ci-workflow.md` |
| User conversation / Interactive | `references/interactive-workflow.md` |

### How to Identify Context

**CI Context:**
- Running in GitHub Actions
- No user available for prompts
- Batch processing mode

**Interactive Context:**
- User is present in conversation
- User may provide story directly
- User may ask for story to be generated
- Can ask user for conflict resolution

---

## Shared Requirements

Both workflows share these requirements:

### Database Access

Use Python sqlite3 module (sqlite3 CLI unavailable):

```python
python -c "
import sqlite3
conn = sqlite3.connect('.claude/data/story-tree.db')
cursor = conn.cursor()
cursor.execute('YOUR SQL HERE')
print(cursor.fetchall())
conn.close()
"
```

### Story Format

```markdown
**As a** [specific user role]
**I want** [specific capability]
**So that** [specific benefit]

**Acceptance Criteria:**
- [ ] [Specific, testable criterion]
- [ ] [Specific, testable criterion]
- [ ] [Specific, testable criterion]

**Related context:** [Evidence from commits or gaps]
```

**Quality Requirements:**
- Specific user role (not generic "user")
- Concrete, measurable capability
- Testable acceptance criteria
- Evidence from commits or clear functional gap
- Stories decompose parent scope (don't expand it)

### Conflict Classification

| Type | Description |
|------|-------------|
| `duplicate` | Same capability, same scope |
| `scope_overlap` | Partial overlap in functionality |
| `competing` | Mutually exclusive approaches |
| `incompatible` | Cannot coexist in codebase |
| `false_positive` | Flagged but actually unrelated |

### Three-Field System

```
Stage:       concept → approved → planned → active → implemented → ready → released

Hold:        polish | wishlist (pauses progress, clears on resume)

Disposition: rejected | infeasible | deprecated | archived | legacy (terminal)
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Find capacity | `python .claude/scripts/story_workflow.py --ci` |
| Vet concept | `python .claude/skills/concept-vetting/candidate_detector.py --story-id ID` |
| View tree | `python .claude/skills/story-tree/scripts/tree-view.py` |

---

## References

### Workflows
- **CI Workflow:** `references/ci-workflow.md`
- **Interactive Workflow:** `references/interactive-workflow.md`

### Generation
- **Gap Analysis:** `references/gap-analysis.md` - Evidence-based story discovery
- **ID Generation:** `references/id-generation.md` - ID format rules and assignment
- **Validation:** `references/validation.md` - Pre-insertion quality checks

### External
- **Concept Vetting:** `.claude/skills/concept-vetting/SKILL.md`
- **Story Tree:** `.claude/skills/story-tree/SKILL.md`
- **Goals:** `.claude/data/goals/goals.md`, `.claude/data/goals/non-goals.md`
