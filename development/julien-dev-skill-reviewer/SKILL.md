---
name: julien-dev-skill-reviewer
description: "Review and improve skill quality. Use when: user asks to review skill, check skill quality, improve skill, or after creating a skill with skill-creator-pro."
license: Apache-2.0
metadata:
  author: "Julien"
  version: "2.0.0"
  category: "development"
triggers:
  - "review skill"
  - "check skill"
  - "improve skill"
  - "skill quality"
  - "audit skill"
  - "score skill"
  - "évaluer skill"
  - "vérifier skill"
  - "améliorer skill"
  - "qualité skill"
  - "auditer skill"
  - "revoir skill"
  - "relire skill"
  - "review my skill quality"
  - "check skill score"
  - "évaluer la qualité de la skill"
  - "améliorer ma skill"
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Bash
---

# Skill Reviewer

Systematically evaluate and improve skill quality through scoring, refactoring, and iteration.

## When to Use

- After creating a skill with skill-creator-pro
- When SKILL.md exceeds 500 lines
- Before packaging for distribution
- When quality score is unknown or low
- When skill feels bloated or has duplication

## Review Process

### Step 1: Read and Parse

```bash
# Read main file
Read skills/skill-name/SKILL.md

# Discover all resources
Glob skills/skill-name/**/*

# Check line count
wc -l skills/skill-name/SKILL.md
```

Parse YAML frontmatter: `name`, `description`, `license`, `allowed-tools`.

### Step 2: Score Against Rubric

Evaluate 9 dimensions (1-5 scale). See [references/quality-rubric.md](references/quality-rubric.md) for detailed criteria.

| Dimension | Check |
|-----------|-------|
| Clarity | Clear steps, no ambiguity |
| Completeness | All scenarios covered |
| Discoverability | Good name + description |
| Context Efficiency | **< 500 lines**, refs used |
| Actionability | Concrete, copy-paste ready |
| Resource Organization | Proper scripts/refs/assets |
| Examples | Concrete, realistic |
| Skill Chaining | I/O/Dependencies documented |
| Error Handling | Troubleshooting provided |

### Step 3: Calculate Score

```
Average = Sum of 9 scores / 9
```

| Score | Status |
|-------|--------|
| 1.0-2.4 | Needs major rework |
| 2.5-3.4 | Functional, needs improvement |
| 3.5-4.4 | Good, minor refinements |
| 4.5-5.0 | Excellent, production ready |

**Minimum for production**: 3.5/5, no dimension < 3/5

### Step 4: Identify Issues

For each dimension < 4/5, document with line references.
See [references/refactoring-templates.md](references/refactoring-templates.md) for issue format.

### Step 5: Suggest Refactoring

Create prioritized plan:
- **Priority 1**: Critical (must fix)
- **Priority 2**: High impact
- **Priority 3**: Polish

See [references/dry-patterns.md](references/dry-patterns.md) for common patterns.

### Step 6: Execute (with approval)

Ask user before changes:
```
A) Show detailed plan
B) Execute Priority 1 automatically
C) Walk through one-by-one
D) Focus on specific dimension
```

### Step 7: Re-evaluate

After refactoring:
1. Re-read modified files
2. Re-score all 9 dimensions
3. Compare before/after
4. Report improvement

### Step 8: Iterate if Needed

If score < 3.5/5, continue iterations.
**Safety limit**: Max 5 iterations.

## Key Validation Checks

See [references/validation-checks.md](references/validation-checks.md) for complete list.

| Check | Requirement |
|-------|-------------|
| Line count | SKILL.md < 500 lines |
| Name | ≤ 64 chars, lowercase + hyphens |
| Description | Third person, ≤ 1024 chars |
| Paths | Forward slashes only |
| References | One level deep |
| Long files | TOC if > 100 lines |
| No duplicates | Content in one place only |

## Reference Files

| File | Content |
|------|---------|
| [references/quality-rubric.md](references/quality-rubric.md) | 9-dimension scoring details |
| [references/dry-patterns.md](references/dry-patterns.md) | DRY violations and fixes |
| [references/refactoring-templates.md](references/refactoring-templates.md) | Report and plan templates |
| [references/validation-checks.md](references/validation-checks.md) | Automated and manual checks |

## Quality Assurance Checklist

Before marking production-ready:

- [ ] Average score ≥ 3.5/5
- [ ] No dimension < 3/5
- [ ] SKILL.md ≤ 500 lines
- [ ] Proper progressive disclosure
- [ ] No DRY violations
- [ ] Skill Chaining documented
- [ ] Examples are concrete
- [ ] Error handling documented
- [ ] YAML frontmatter valid
- [ ] All references linked from SKILL.md

## Skill Chaining

### Skills Required Before
- **julien-dev-tools-skill-creator-pro** (optionnel): If reviewing newly created skill

### Input Expected
- Path to skill directory with SKILL.md
- Skill must have valid YAML frontmatter

### Output Produced
- **Format**: Review report in markdown
- **Side effects**:
  - May create `references/` directory
  - May create new .md files
  - May modify SKILL.md (with approval)
  - Creates backup: `SKILL.md.backup-YYYYMMDD-HHMMSS`
- **Duration**: 5-10 minutes (3-5 iterations)

### Compatible Skills After
**Recommandés** (if score ≥ 3.5/5):
- Package script from skill-creator-pro
- **julien-workflow-sync-personal-skills**: Deploy to ~/.claude/skills/

### Called By
- **julien-dev-tools-skill-creator-pro**: After Step 4, before packaging
- Direct invocation: "Review my skill X"

### Tools Used
- `Read` (usage: read SKILL.md, references/)
- `Glob` (usage: discover skill files)
- `Grep` (usage: search patterns, word count)
- `Edit` (usage: refactor SKILL.md)
- `Write` (usage: create references/*.md)
- `Bash` (usage: wc -l, backup files)

### Visual Workflow

```
User: "Review skills/my-skill"
    ↓
[THIS SKILL]
    ├─► Read SKILL.md + refs
    ├─► Score 9 dimensions
    ├─► Identify issues
    └─► Generate report
    ↓
Score < 3.5/5?
    YES → Refactor → Re-evaluate → Iterate
    NO  → Production ready ✅
    ↓
[Next steps]
    ├─► package_skill.py
    └─► sync-personal-skills
```

### Usage Example

**Scenario**: Review deployment skill

**Command**: "Review the skill at skills/deployment-manager/"

**Result**:
- Initial score: 2.8/5
- Issues: DRY violation, bloated SKILL.md (6000 words), missing chaining
- After 3 iterations: 4.3/5
- SKILL.md: 6000 → 2500 words
- Created: references/api-reference.md, references/examples.md
- Status: Production ready
