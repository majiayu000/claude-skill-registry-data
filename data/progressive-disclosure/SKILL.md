---
name: progressive-disclosure
description: Use when creating new skills or refactoring existing skills - teaches the progressive disclosure architecture pattern to optimize context window usage by organizing skills into 3 tiers (metadata, entry point, references) and avoiding documentation dumps. Essential before any skill creation or modification work.
version: 1.0.0
license: MIT
---

# Progressive Disclosure Architecture for Claude Skills

## Overview

Progressive disclosure is an architectural pattern that optimizes context window usage by loading information incrementally. Instead of front-loading all documentation, skills reveal details only when needed.

**Core principle**: SKILL.md is a table of contents, not an encyclopedia. Claude reads the overview, then selectively loads reference files only when the task requires them.

## When to Use

**Always use this skill before**:
- Creating a new skill
- Refactoring an existing skill
- Reviewing skill performance
- Debugging context bloat issues

**Symptoms that indicate you need this**:
- Skills over 500 lines
- Multiple related skills activating together
- Documentation copied from official sources
- Slow skill activation times
- Context window filling up quickly

**When NOT to use**:
- Simple workflow skills under 200 lines that are already well-structured
- Quick skill updates (typo fixes, minor edits)

## The 3-Tier Architecture

| Tier | Always Loaded? | Size Limit | Purpose |
|------|----------------|------------|---------|
| **Tier 1**: Metadata | ✓ Yes | 1024 chars | Skill discovery/triggering |
| **Tier 2**: SKILL.md | On activation | ~500 lines | Overview, navigation, quick ref |
| **Tier 3**: References | On-demand | 200-300 lines each | Deep docs, examples, APIs |

### Tier 1: Metadata (YAML Frontmatter)

```yaml
---
name: skill-name-with-hyphens
description: Use when [specific triggers/symptoms] - [what it does in third person]
version: 1.0.0
license: MIT
---
```

**Critical requirements**:
- Start with "Use when..."
- Include specific symptoms/triggers
- Written in third person (injected into system prompt)
- No parentheses in name (use hyphens only)

### Tier 2: SKILL.md Entry Point (~200-500 lines)

**Structure template**:

```markdown
# Skill Name

## Overview
Core principle in 1-2 sentences.

## When to Use
- Bullet symptoms
- Specific use cases
- When NOT to use

## Quick Reference
[Table or bullets for common operations]

## Workflows
[Step-by-step processes with checklists]

## Detailed Documentation
- [Topic 1](references/topic-1.md)
- [Topic 2](references/topic-2.md)
```

### Tier 3: Reference Files (200-300 lines each)

```
skill-name/
├── SKILL.md              (~200-500 lines)
├── references/
│   ├── api-reference.md
│   ├── examples.md
│   └── advanced.md
└── scripts/
    └── helper.py
```

**CRITICAL**: Keep references **one level deep** from SKILL.md (no nested references like A→B→C)

## Quick Reference: Key Rules

| Rule | Limit | Why |
|------|-------|-----|
| SKILL.md body | <500 lines | Optimal scanning speed |
| Frequently-loaded content | <200 words | Token efficiency |
| Reference files | 200-300 lines | Focused topics |
| Reference depth | 1 level from SKILL.md | Prevent partial reads |
| Description length | <500 chars (ideally) | Quick matching |

## Skills as Documentation vs Capabilities

### Documentation Skills
**Purpose**: Provide reference information (APIs, syntax, schemas)

**Characteristics**:
- Heavy reference material
- Progressive disclosure CRITICAL
- Organize by domain/topic
- Token efficiency essential

**Example**: API reference, database guides, framework docs

### Capability Skills
**Purpose**: Teach workflows, techniques, patterns

**Characteristics**:
- Process-focused (TDD, debugging, brainstorming)
- Workflow often fits in ~200 lines
- Includes checklists and step-by-step guides
- May reference other skills

**Example**: systematic-debugging, test-driven-development, brainstorming

## Workflow-Based vs Tool-Based Organization

### ✓ Workflow-Based (Recommended)
Organize by **user's journey**, not technical features.

```markdown
## PDF Form Filling Workflow

Task Progress:
- [ ] Step 1: Analyze form (run analyze_form.py)
- [ ] Step 2: Create field mapping
- [ ] Step 3: Validate mapping
- [ ] Step 4: Fill form
- [ ] Step 5: Verify output
```

### ✗ Tool-Based (Anti-Pattern)
Organize by **technical features** alphabetically with no workflow guidance.

**Fix**: Add "Common Workflows" section at top, then tool reference below.

## Refactoring Checklist

### Phase 1: Audit
- [ ] Count lines in SKILL.md (target: <500)
- [ ] Count words in frequently-loaded sections (target: <200)
- [ ] Identify content types (overview, reference, workflows, examples)
- [ ] Check reference depth (all should be 1 level from SKILL.md)
- [ ] Verify description has "Use when..." triggers

### Phase 2: Identify Extraction Candidates
- [ ] Mark sections >100 lines for extraction
- [ ] Find domain-specific content (not always needed)
- [ ] Locate heavy API documentation
- [ ] Find long examples
- [ ] Identify embedded executable scripts

### Phase 3: Plan Structure
- [ ] Design file structure
- [ ] Ensure references are 1 level deep
- [ ] Add TOC to files >100 lines
- [ ] Choose workflow vs tool-based organization

### Phase 4: Extract Content
- [ ] Create reference files
- [ ] Move heavy reference material
- [ ] Extract domain-specific content
- [ ] Move scripts to scripts/ directory
- [ ] Keep core workflow in SKILL.md

### Phase 5: Update SKILL.md
- [ ] Reduce to <500 lines
- [ ] Keep overview and principles
- [ ] Add clear navigation to references
- [ ] Add workflow checklist (if complex)
- [ ] Front-load critical information

### Phase 6: Test Progressive Disclosure
- [ ] Test basic usage without loading references
- [ ] Verify Claude can find and load references when needed
- [ ] Test domain-specific loading
- [ ] Confirm workflow makes sense without reading all references

## Common Mistakes

### Mistake 1: Front-Loading Everything
**Problem**: All reference material in SKILL.md

**Fix**: Split by domain, link from overview

### Mistake 2: Too Much Nesting
**Problem**: References that reference other references (A→B→C)

**Fix**: All references link directly from SKILL.md

### Mistake 3: No Navigation in Long Files
**Problem**: Reference file is 300 lines with no TOC

**Fix**: Add table of contents at top

### Mistake 4: Unclear Script Intent
**Problem**: Not clear whether to execute or read scripts

**Fix**: Be explicit - "Run `script.py` to..." or "See `script.py` for the algorithm"

## Consolidation Opportunities

**Red flags indicating consolidation needed**:
- Related skills always activate together
- Shared authentication/setup patterns
- Overlapping workflows
- Combined context >30K tokens

**Example consolidation**:

**Before** (6 separate skills, ~30K tokens when all activate):
```
gemini-audio/
gemini-vision/
gemini-image-gen/
gemini-document-processing/
gemini-video-understanding/
google-adk-python/
```

**After** (unified structure, ~8K tokens for typical usage):
```
gemini-api/
├── SKILL.md (unified auth + routing)
├── audio/SKILL.md
├── vision/SKILL.md
├── generation/SKILL.md
└── documents/SKILL.md
```

## Integration with Other Skills

**Required background**:
- [skill-creator](../skill-creator/SKILL.md) - How to create skills
- [writing-skills](../writing-skills/SKILL.md) - Skill writing best practices

**Use together with**:
- Always use this skill BEFORE creating/refactoring skills
- Reference during skill review processes

## Detailed Documentation

For comprehensive guides and examples, see:
- [refactoring-examples.md](references/refactoring-examples.md) - Before/after examples from real skills
- [context-optimization.md](references/context-optimization.md) - Token efficiency techniques
- [consolidation-strategies.md](references/consolidation-strategies.md) - When and how to merge skills

## Key Takeaways

1. **SKILL.md = Table of contents**, not encyclopedia
2. **<500 lines for SKILL.md** - extract the rest to references
3. **Keep references 1 level deep** - avoid A→B→C chains
4. **Organize by workflow**, not tools
5. **Documentation skills need progressive disclosure** most
6. **Capability skills** can often fit in single SKILL.md
7. **Consolidate related skills** that always activate together
8. **Test without loading references** - core workflow should work
9. **Front-load critical info** - most important content first
10. **Use checklists** for complex multi-step workflows
