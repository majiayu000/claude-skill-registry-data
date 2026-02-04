---
name: Creating Research Packages
description: Document complex domain knowledge as self-contained packages with multiple reading paths
when_to_use: when documenting complex research topics, domain knowledge requiring multiple reading paths, technical deep dives that need verification tracking
version: 1.0.0
---

# Creating Research Packages

## Overview

Bundle complex domain knowledge into self-contained modules with multiple entry points for different time budgets and reader roles.

**Announce at start:** "I'm using the creating-research-packages skill to document this domain knowledge."

## When to Use

- Documenting complex research findings
- Creating domain knowledge packages (physics, algorithms, APIs)
- Building self-contained documentation that can be shared independently
- Topics requiring multiple reading paths (quick overview vs deep dive)
- Knowledge that needs verification tracking

## The Process

### Step 1: Identify the Package Scope

Determine what knowledge should be packaged:

- What is the core topic?
- What are the sub-topics?
- Who are the readers? (roles, time budgets)
- What verification is needed?

### Step 2: Create Directory Structure

```bash
mkdir -p docs/[topic]
```

Standard package structure:

```
[topic]/
├── 00-START-HERE.md           # Entry point + verification status
├── README.md                   # Package overview + TL;DR
├── how-to-use-this.md         # Detailed navigation guide
├── [core-topic-1].md          # Main research content
├── [core-topic-2].md          # Additional research
├── design-decisions.md        # Why decisions were made
├── QUICK-REFERENCE.md         # One-page summary
├── VERIFICATION-REVIEW.md     # Accuracy audit
└── examples/                  # Working examples (if applicable)
```

### Step 3: Write Entry Point (00-START-HERE.md)

Include:
- Verification status with visual indicators
- Time budget options (5 min, 20 min, 2 hours)
- Quick navigation to key documents
- Prerequisites if any

```markdown
# [Topic]: Start Here

**Status:** ✅ Verified | **Last Updated:** YYYY-MM-DD

## Choose Your Path

| Time | Goal | Start With |
|------|------|------------|
| 5 min | Quick overview | [TL;DR section in README] |
| 20 min | Understand context | [README + design-decisions] |
| 2 hours | Full understanding | [All documents in sequence] |
```

### Step 4: Write README with TL;DR

The README is the package overview:

- TL;DR section (2-3 sentences, the essential insight)
- Reading paths by time budget
- Role-based paths
- Package contents overview
- Key concepts with links to details

**Use template:** `${CLAUDE_PLUGIN_ROOT}templates/research-package-template.md`

### Step 5: Write Navigation Guide (how-to-use-this.md)

Detailed guide for different readers:

- Role-based paths with reading orders
- Time estimates for each path
- Key takeaways for each role
- Cross-references between documents

### Step 6: Write Core Content

For each topic document:

- Clear scope statement
- Structured content with headers
- Visual aids where helpful (diagrams, tables)
- Cross-references to related docs
- Verification notes if applicable

### Step 7: Create Quick Reference

One-page summary for rapid lookup:

- Key formulas/constants
- Common commands
- Quick diagnosis table
- Status icons legend

**Use template:** `${CLAUDE_PLUGIN_ROOT}templates/quick-reference-template.md`

### Step 8: Add Verification Tracking

If accuracy is critical:

- Create VERIFICATION-REVIEW.md
- Track what was verified and when
- Note discrepancies found
- Link to authoritative sources
- Include recommended updates

### Step 9: Verify Package Completeness

Checklist:
- [ ] 00-START-HERE.md has clear navigation
- [ ] README has TL;DR that captures essence
- [ ] Reading paths cover different time budgets
- [ ] Role-based paths for different readers
- [ ] QUICK-REFERENCE is truly one page
- [ ] All cross-references work
- [ ] Verification status current

## Checklist

- [ ] Package scope clearly defined
- [ ] Directory structure created
- [ ] Entry point (00-START-HERE) written
- [ ] README with TL;DR written
- [ ] Navigation guide written
- [ ] Core content documents written
- [ ] Quick reference created
- [ ] Verification tracking if needed
- [ ] All internal links verified

## Anti-Patterns

**Don't:**
- Create packages for simple topics (overkill)
- Skip the TL;DR (readers need quick overview)
- Omit time estimates (readers can't plan)
- Ignore verification for critical knowledge
- Make QUICK-REFERENCE more than one page

**Do:**
- Keep TL;DR to 2-3 sentences
- Provide multiple entry points
- Track verification for technical accuracy
- Cross-reference liberally
- Test navigation with fresh eyes

## Related Skills

- **Organizing documentation:** `${CLAUDE_PLUGIN_ROOT}skills/organizing-documentation/SKILL.md`
- **Documenting debugging workflows:** `${CLAUDE_PLUGIN_ROOT}skills/documenting-debugging-workflows/SKILL.md`
- **Creating quality gates:** `${CLAUDE_PLUGIN_ROOT}skills/creating-quality-gates/SKILL.md`

## References

- Standards: `${CLAUDE_PLUGIN_ROOT}standards/documentation-structure.md`
- Template: `${CLAUDE_PLUGIN_ROOT}templates/research-package-template.md`
- Quick Reference Template: `${CLAUDE_PLUGIN_ROOT}templates/quick-reference-template.md`
