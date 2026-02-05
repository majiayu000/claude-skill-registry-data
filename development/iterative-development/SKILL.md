---
name: iterative-development
description: |
  Load when adding features or analyzing impact on existing framework. Supports progressive development without requiring everything upfront. Used by /add-feature and /analyze-impact commands.
---

# Iterative Development Skill

Supports adding features and analyzing impact without full upfront planning.

## When to Load

Load this skill for:
- `/katachi:add-feature` - Add new feature on-the-go
- `/katachi:analyze-impact` - Analyze change impact

## Philosophy

The framework should support "add as you go" not "define everything upfront":

- Features can be added mid-project
- Dependencies are analyzed dynamically
- Phases recalculate automatically
- Quick-start mode for MVPs

## Add Feature Workflow

### 1. Capture Feature Description

Ask user to describe the feature:
- What does it do?
- Who uses it?
- Any known dependencies?

### 2. Determine Category

Categories follow the pattern: `CATEGORY-NNN`

**Process:**
1. Read existing categories from FEATURES.md
2. Infer category from description
3. Confirm with user

```python
# Example categories
CORE - Core functionality
CLI - Command-line interface
API - API endpoints
UI - User interface
DATA - Data handling
AUTH - Authentication
```

If new category needed, confirm with user before creating.

### 3. Assign ID

Find next available ID in category:

```bash
# Check existing IDs
python scripts/features.py status list --category CORE

# Result: CORE-001, CORE-002, CORE-003
# New ID: CORE-004
```

### 4. Capture Complexity

Ask user for complexity estimate:
- **Easy**: 1-2 hours, straightforward
- **Medium**: Half day, some complexity
- **Hard**: Full day+, significant complexity

### 5. Analyze Dependencies

**Option A: User knows dependencies**
- Ask: "Does this depend on any existing features?"
- Validate dependencies exist

**Option B: Agent analysis**
- Dispatch `katachi:impact-analyzer` with feature description
- Agent identifies likely dependencies based on description
- Present to user for confirmation

### 6. Update FEATURES.md

Add new feature entry:

```markdown
| CORE-004 | New feature description | Medium | ✗ Defined |
```

### 7. Update DEPENDENCIES.md

Add to dependency matrix:

```bash
python scripts/features.py deps add-feature CORE-004
python scripts/features.py deps add-dep CORE-004 CORE-001  # If depends on CORE-001
```

### 8. Recalculate Phases

Phases recalculate based on dependencies:

```bash
python scripts/features.py deps recalculate-phases
```

Show user the new phase assignment:
- "CORE-004 assigned to Phase 2 (depends on CORE-001)"

### 9. Offer Next Step

After adding:
- "CORE-004 added. Create spec now? [Y/N]"
- If yes, transition to `/katachi:spec-feature CORE-004`

## Impact Analysis Workflow

### 1. Capture Change Description

Ask user to describe the proposed change:
- What is being changed?
- Why is this change needed?
- What areas might be affected?

### 2. Dispatch Impact Analyzer

```python
Task(
    subagent_type="katachi:impact-analyzer",
    prompt=f"""
Analyze the impact of this proposed change:

## Change Description
{change_description}

## FEATURES.md
{features_content}

## DEPENDENCIES.md
{dependencies_content}

## Existing Specs
{list_of_spec_paths}

Trace dependencies and report affected features.
"""
)
```

### 3. Present Findings

Show user:
- Directly affected features
- Transitively affected features (dependency chain)
- Documents needing updates
- Risk assessment

### 4. Ask Next Steps

Based on impact level:

**Isolated:**
- "This change is isolated to X. Proceed with implementation?"

**Moderate:**
- "This affects N features. Review affected specs before proceeding?"

**Significant:**
- "This is a significant change. Create an ADR to document this decision?"

**Structural:**
- "This affects core architecture. Recommend detailed analysis before proceeding."

## Quick-Start Mode

For new projects, offer quick-start:

1. **Minimal VISION.md**
   - Problem statement
   - MVP scope (not full scope)
   - Key workflows (top 3)

2. **MVP Features Only**
   - Extract only features needed for MVP
   - Skip nice-to-haves
   - Aim for 5-10 features max

3. **Simple Dependencies**
   - Phase 1 = MVP
   - Linear dependencies where possible
   - Skip complex dependency analysis

4. **First Feature Guidance**
   - Guide through first spec
   - Establish patterns early
   - User learns workflow on real work
