---
name: ruleset-optimization
description: Guidelines for optimizing Claude rulesets and instruction files (CLAUDE.md, settings.json) using context efficiency principles. Includes strategies for skill extraction, progressive disclosure, token savings calculation, and deduplication. Manually invoke when optimizing rulesets, reducing context size, extracting content to skills, or improving ruleset organization.
---

# Ruleset Optimization Guidelines

**Auto-activate when:** Working with `CLAUDE.md`, `settings.json`, `SKILL.md` files, `.claude/` directory, or when user mentions ruleset optimization, context efficiency, skill extraction, token savings, or improving Claude Code configuration.

This skill provides comprehensive guidelines for optimizing Claude rulesets to minimize context usage while maximizing effectiveness.

## Context Efficiency Philosophy

**PRIMARY GOAL**: Minimize baseline context, maximize signal-to-noise ratio.

**Core Strategy:**
- **Skills for domain-specific rules** (git, python, web, containers): auto-load when relevant, 30-70% context reduction when inactive
- **CLAUDE.md minimal**: project overview, quick start, project-specific patterns, skill references only
- **Progressive disclosure**: baseline=always-needed (~20%), details=on-demand via skills (~80%)

## Decision Framework

### Extraction Decision Tree
```
Is content >200 tokens?
├─ No → Keep in CLAUDE.md
└─ Yes → Is it procedural?
    ├─ No → Keep in CLAUDE.md (policy)
    └─ Yes → Is it used <70% of sessions?
        ├─ No → Keep in CLAUDE.md (always needed)
        └─ Yes → Extract to skill (saves tokens)
```

### Move to Skills (Procedural "How-To")
- Step-by-step procedures, domain workflows, tool patterns, decision trees
- Language/framework-specific rules, optional best practices

### Keep in CLAUDE.md (Policy "What/Why")
- Core values, always-applicable preferences, security requirements
- File operation policies, communication style, project overview

### Token Savings Calculation
**Formula:** tokens × (1 - usage_frequency)

**Priority thresholds:**
- High: 500+ tokens, used <50% of time
- Medium: 200-500 tokens, used <30% of time
- Low: <200 tokens or used >70% of time

**Report format:**
- Before: X tokens baseline
- After: Y tokens baseline, Z with skills (when needed)
- Savings: (X - Y) tokens baseline (N% reduction)

## Deduplication Strategy

**Personal vs Project Rulesets:**
- Personal (~/.claude/CLAUDE.md): universal defaults
- Project (.claude/CLAUDE.md): project-specific overrides, takes precedence
- Never duplicate between them

**Across Skills:**
- Clear, non-overlapping scope per skill
- Reference other skills vs duplicating content

## Creating Effective Skills

### Structure Template
```markdown
---
name: skill-name
description: Clear description of when to activate and what it contains.
---

# Skill Title

Brief introduction and purpose.

## Core Content
[Domain-specific guidance]
```

### Activation Patterns
**Auto-activation triggers:**
- File patterns: .py, package.json, Dockerfile
- Git operations: commit, push, version control
- Project structure: directories, files present

**Manual invocation:**
- Slash commands: /optimize-prompt, /commit
- Explicit requests: "optimize this ruleset"

### Anti-Patterns
- Over-extraction: No skills for <100 tokens
- Under-referencing: Always add reference when removing content
- Duplication: Never duplicate between personal/project or across skills
- Poor organization: Don't mix domains in one skill

## Optimization Impact Examples

**Before:** 6,000 tokens baseline (all loaded)
**After:** 4,000 tokens baseline + 1,500 tokens in skills (selective)
**Result:** 33% baseline reduction, 25-33% typical session savings

**Compound benefits:**
- Optimization helps ALL projects using shared skills
- Clearer organization improves maintainability
- Faster context loading and better reasoning
- More room for project-specific context

## Maintenance Guidelines

### Regular Review
- Quarterly token usage review
- Check for new extraction opportunities
- Verify skill activation patterns
- Remove stale or unused skills

### Skill Evolution
- Update content as practices evolve
- Merge overlapping skills
- Split skills >1000 tokens
- Archive deprecated skills with notes

---

**This skill is manually invoked when optimizing rulesets or organizing Claude instructions.**

For command usage, see:
- `/optimize-ruleset` - Analyze and optimize current ruleset
- `/analyze-permissions` - Review permission patterns