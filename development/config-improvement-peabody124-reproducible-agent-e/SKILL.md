---
name: config-improvement
description: Propose improvements to upstream RAE repository
---

## Overview

When you discover a better pattern, configuration, or guideline during work, this skill guides you through proposing it upstream to the Reproducible Agent Environment repository.

## Parameters

- **improvement_type** (optional): "guideline", "skill", "sop", "config", or "template"
- **description** (required): Brief description of the improvement

## Steps

### 1. Evaluate Scope

Determine if the improvement is universal or project-specific.

**Constraints:**
- You MUST verify the improvement works in the current project
- You MUST check if a similar pattern already exists upstream
- You SHOULD consider if the improvement applies broadly or only to specific domains

**Decision:**
- IF universal → Proceed to step 2
- IF project-specific → Add to local overrides with comment explaining why, then STOP

### 2. Document the Improvement

Prepare a clear description of the change.

**Constraints:**
- You MUST include before/after examples
- You MUST explain the rationale (why is this better?)
- You SHOULD reference any research or sources that informed the improvement
- You MUST specify which file(s) would be modified

### 3. Create Upstream PR

**Constraints:**
- You MUST create a branch with descriptive name (e.g., `improve/ruff-config`, `guideline/async-patterns`)
- You MUST write a clear commit message explaining the improvement
- You SHOULD include test cases or examples if applicable
- You MUST open PR with the documented rationale

### 4. Update Local

After PR is merged:
- Run `scripts/sync.sh` to pull the improvement
- Verify it works correctly in your project

## Examples

**User:** "I found a better ruff configuration for catching common issues"
**Agent:** Evaluates if it's universal (yes), documents the change with before/after examples, creates PR to update templates/pyproject.toml.

**User:** "/config-improvement guideline 'Add guidance on async/await patterns'"
**Agent:** Checks if async guidance exists (no), drafts new section for python-standards.md, creates PR with examples.
