---
name: Documenting Debugging Workflows
description: Create symptom-based debugging documentation that matches how developers actually search for solutions
when_to_use: when creating debugging guides, documenting common bugs, building troubleshooting documentation, or organizing FIX/ sections
version: 1.0.0
---

# Documenting Debugging Workflows

## Overview

Create debugging documentation organized by observable symptoms, not root causes. Developers search by what they see, not by what's wrong.

**Announce at start:** "I'm using the documenting-debugging-workflows skill to create symptom-based debugging docs."

## When to Use

- Creating debugging documentation for a project
- Documenting common bugs and their fixes
- Building troubleshooting guides
- Organizing FIX/ section content
- Recurring issues need documentation

## Core Principle

**Wrong:** Organize by root cause (memory-leaks/, type-errors/)
**Right:** Organize by observable symptom (visual-bugs/, slow-startup/)

Developers don't know the root cause when they start debugging - they know what they observe.

## The Process

### Step 1: Collect Symptoms

Gather observable symptoms from:
- Bug reports and issues
- Support tickets
- Slack/team chat questions
- Your own debugging sessions
- Code review comments

For each symptom, note:
- What exactly does the developer see?
- How do they describe it?
- What words do they use to search?

### Step 2: Create Symptom Categories

Group symptoms by observable category:

```
FIX/
├── symptoms/
│   ├── visual-bugs/       # "Rendering looks wrong"
│   ├── performance/       # "It's slow"
│   ├── test-failures/     # "Tests fail"
│   ├── build-errors/      # "Won't compile"
│   └── data-issues/       # "Data is wrong"
├── investigation/
│   └── systematic-debugging.md
└── solutions/
    └── common-fixes.md
```

Choose categories based on YOUR project's common issues.

### Step 3: Build Quick Diagnosis Table

Create the entry point with a scannable table:

```markdown
# [Category] Debugging Guide

## Quick Diagnosis

| Symptom | Likely Cause | Investigation | Priority |
|---------|--------------|---------------|----------|
| [What you see] | [Root cause] | [Link] | ⚠️ High |
| [What you see] | [Root cause] | [Link] | ☠️ Critical |
```

Priority icons:
- ☠️ Critical (production impact)
- ⚠️ High (blocking work)
- 🎯 Medium (should fix soon)
- ✅ Low (minor annoyance)

### Step 4: Document Each Symptom

For each symptom, create structured documentation:

1. **What You See** - Exact observable behavior
2. **Likely Causes** - Ordered by probability
3. **Investigation Steps** - With commands to run
4. **Solutions** - Fixes for each cause
5. **Prevention** - How to avoid in future

**Use template:** `${CLAUDE_PLUGIN_ROOT}templates/symptom-debugging-template.md`

### Step 5: Create Investigation Strategies

Document systematic approaches in `investigation/`:

- How to reproduce consistently
- How to isolate the problem
- Gathering evidence (logs, metrics)
- Forming and testing hypotheses
- Binary search for breaking changes

### Step 6: Build Solutions Catalog

Document known fixes in `solutions/`:

- Common error codes and fixes
- Proven workarounds
- Configuration fixes
- Code patterns that prevent issues

### Step 7: Add Escalation Guidance

Document when to escalate:
- Time thresholds (stuck > X hours)
- Impact thresholds (production, data, security)
- Who to contact
- What information to gather first

### Step 8: Verify and Maintain

- Test documentation with someone unfamiliar
- Update when new symptoms discovered
- Archive outdated fixes (don't delete - mark as historical)
- Track which docs get used most

## Checklist

- [ ] Symptoms collected from real sources
- [ ] Categories match project's common issues
- [ ] Quick diagnosis table created
- [ ] Each symptom has structured documentation
- [ ] Investigation strategies documented
- [ ] Solutions catalog started
- [ ] Escalation guidance clear
- [ ] Tested with fresh eyes

## Anti-Patterns

**Don't:**
- Organize by root cause (developers don't know it yet)
- Skip the quick diagnosis table
- Write investigation steps without commands
- Forget escalation guidance
- Let docs become stale

**Do:**
- Use exact symptom descriptions
- Include runnable commands
- Link to related docs liberally
- Update when fixes are found
- Track which docs help most

## Example: Visual Bug Entry

```markdown
## Rendering Artifacts on Screen

### What You See
Flickering textures, z-fighting, or objects appearing through walls.

### Likely Causes
1. **Floating point precision** (most common)
   - Objects far from origin
   - Verify: Check object world coordinates

2. **Z-buffer precision**
   - Near/far plane ratio too large
   - Verify: Check camera settings

### Investigation Steps
1. [ ] Log object world coordinates
   ```rust
   info!("Position: {:?}", transform.translation);
   ```
   If > 10000 units from origin → floating point issue

2. [ ] Check camera near/far planes
   ```rust
   info!("Near: {}, Far: {}", camera.near, camera.far);
   ```
   If ratio > 10000 → z-buffer issue

### Solutions
**If floating point:** Implement floating origin
**If z-buffer:** Adjust camera planes

### Prevention
- Use floating origin for large worlds
- Keep near plane as far as acceptable
```

## Related Skills

- **Organizing documentation:** `${CLAUDE_PLUGIN_ROOT}skills/organizing-documentation/SKILL.md`
- **Creating research packages:** `${CLAUDE_PLUGIN_ROOT}skills/creating-research-packages/SKILL.md`
- **Creating quality gates:** `${CLAUDE_PLUGIN_ROOT}skills/creating-quality-gates/SKILL.md`

## References

- Standards: `${CLAUDE_PLUGIN_ROOT}standards/documentation-structure.md`
- Template: `${CLAUDE_PLUGIN_ROOT}templates/symptom-debugging-template.md`
