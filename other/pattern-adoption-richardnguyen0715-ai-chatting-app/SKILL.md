---
name: pattern-adoption
description: Adapt and integrate a specific pattern from your references into your current codebase. Use when you've identified a pattern worth adopting and need a structured plan to integrate it with minimal disruption.
---

# Pattern Adoption

## Overview

You've found a pattern in your references that you want to use. This skill guides the systematic process of adapting it — not copy-pasting it — into your current codebase. The key challenge is respecting your existing conventions while capturing the essence of what made the reference pattern good.

## When to Use

- You've done a `reference-lookup` and found a clear pattern to adopt
- You want to restructure part of your code based on a reference implementation
- You're replacing an existing approach with something better from your references
- A team member asks "can we use the pattern from that repo we analyzed?"

---

## Adoption Workflow

### Step 1 — Pattern Brief

Before writing any code, answer:

```
Pattern Name:    {what you're adopting, e.g. "Repository pattern for Delta table access"}
Source:          ~/references/{repo}/analysis.md §{section} or ~/.copilot/context/{file}.md
Core Idea:       What makes this pattern good (one sentence)
Current State:   What you have now in your codebase
Target State:    What it looks like after adoption
Scope:           What files/modules are touched
```

### Step 2 — Gap Analysis

Compare the reference pattern to your current implementation:

| Dimension | Reference Pattern | Current Code | Gap |
|-----------|------------------|--------------|-----|
| Structure | | | |
| Abstractions | | | |
| Dependencies | | | |
| Tests | | | |
| Error handling | | | |

### Step 3 — Adaptation Design

The reference pattern may not drop in directly. Plan your adaptation:

**What stays the same:**
- Core mechanism / algorithm

**What must change:**
- Language/framework specifics (e.g., they used Django ORM, you use PySpark)
- Naming conventions (match your project's style)
- Error handling (match your project's patterns)
- Configuration approach (use your secret scopes, not their env vars)

**What you intentionally leave out:**
- Features you don't need
- Complexity that doesn't apply to your scale

### Step 4 — Integration Plan

Break the adoption into atomic steps:

```
□ Step A: Create new module/class shell (no behavior yet)
□ Step B: Implement core method from pattern
□ Step C: Write unit test for core method
□ Step D: Wire into existing code (feature flag if needed)
□ Step E: Remove old implementation
□ Step F: Update docs/AGENTS.md if architectural change
```

### Step 5 — Implementation

Follow `incremental-implementation` skill:
- One step at a time
- Test at each step
- Don't refactor and adopt simultaneously

**Databricks/PySpark-specific notes:**
- Validate PySpark transformations produce correct output with `.show()` / `.count()` before wiring in
- Wrap in a feature flag via Databricks job parameter if the old path must stay available during rollout
- Update `databricks.yml` if the adoption introduces new dependencies or cluster requirements

### Step 6 — Validate

```bash
# Run tests
pytest tests/ -v -k "{relevant test scope}"

# If Databricks: validate bundle
databricks bundle validate
```

### Step 7 — Document

Update `~/.copilot/context/{domain}/{pattern}.md`:
- Add "Implemented in: {my-project}/{path}" note
- Document any adaptations made from the original

---

## Adoption Checklist

- [ ] Pattern brief written — core idea understood
- [ ] Gap analysis complete — differences from current code mapped
- [ ] Adaptation design done — what changes, what's kept, what's skipped
- [ ] Integration steps are atomic and ordered
- [ ] Tests written alongside implementation
- [ ] Old implementation removed (not just hidden)
- [ ] Context KB updated with "implemented in" reference
- [ ] No copy-paste from reference — adapted to your conventions

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails |
|-------------|-------------|
| Copy-paste the whole file | Brings in assumptions and style that clash with your codebase |
| Adopt pattern AND refactor simultaneously | Hard to debug when something breaks |
| Adopt before understanding WHY it's good | You'll implement it wrong |
| Skip the gap analysis | Discover mid-implementation the pattern doesn't fit |
| No tests during adoption | You break existing behavior without knowing |

## Tips

- **Adopt the idea, not the code** — rewrite from scratch in your style
- If the gap is too large, consider a **thin wrapper** first (adopt interface, keep your implementation)
- Use `code-reviewer` agent after implementation to catch style drift from your conventions
