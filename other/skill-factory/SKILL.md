---
name: skill-factory
description: >-
  Meta-skill for creating complete, production-ready Claude skills from scratch or by migrating existing prompts/GPTs.
  Generates full skill packages including SKILL.md, references, scripts, and triggering tests.
  Use when creating a new skill, converting a prompt to a skill, migrating a GPT, or improving an existing skill.
  Provides interactive workflow with analysis, design, validation, and generation phases.
  Not for simple one-time prompts or highly volatile procedures.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Skill Factory

## Overview

Meta-skill that generates complete, standards-compliant Claude skills through an interactive workflow. Produces production-ready packages with SKILL.md, references, scripts, and automated triggering tests.

## Quick Decision Tree

```
┌─────────────────────────────────────────────────────────────┐
│                    What do you need?                        │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ NEW SKILL     │   │ MIGRATION     │   │ IMPROVEMENT   │
│ from scratch  │   │ prompt → skill│   │ existing skill│
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
        ▼                   ▼                   ▼
   Phase 1-6            Phase 2-6            Audit + 
   (full flow)       (skip analysis)      suggestions
```

## Interactive Workflow (6 Phases)

### Phase 1: Pre-Creation Analysis
**Goal**: Validate skill necessity and define scope

**Questions to answer**:
1. What problem does this skill solve? (1 sentence)
2. How often is this task performed? (≥5 past, ≥10 future = good candidate)
3. Who is the target persona? (dev backend, data analyst, PM...)
4. What trigger words will users employ?
5. What are the success criteria? (measurable output)
6. What is explicitly OUT of scope?

**Output**: Completed analysis using [pre-analysis.md](templates/pre-analysis.md)

**Decision gate**: 
- ✅ Proceed if: recurring task, stable procedures, clear scope
- ❌ Stop if: one-time task, volatile procedures, duplicates existing capability

---

### Phase 2: Skill Architecture Design
**Goal**: Define structure and file organization

**Decisions**:
1. **Skill name**: kebab-case, ≤64 chars, descriptive
2. **Target platforms**: Claude.ai / Claude Code / Both
3. **Complexity level**:
   - Simple: SKILL.md only
   - Standard: SKILL.md + references/
   - Advanced: Full package with scripts + templates
4. **Multi-workflow?**: If yes → design decision tree

**Output**: Structure diagram + file list

**Reference**: [skill-structure.md](templates/skill-structure.md)

---

### Phase 3: Description Engineering (Triggering)
**Goal**: Craft optimal description for semantic matching

**Formula**:
```
[CAPABILITIES] + [USE CASES] + [TRIGGERS] + [BOUNDARIES]
```

**Checklist**:
- [ ] Action verbs (extract, analyze, create, validate...)
- [ ] File types / data types concerned
- [ ] "Use when..." with 2-3 contexts
- [ ] "Not for..." with explicit exclusions
- [ ] No overlap with existing skills

**Reference**: [description-formulas.md](references/description-formulas.md)

**Validation**: Description must be ≤1024 chars

---

### Phase 4: Workflow & Instructions Design
**Goal**: Define the operational workflow

**Structure**:
1. Overview (2-3 sentences)
2. Quick Start / Decision Tree (if multi-workflow)
3. Numbered workflow steps
4. Critical rules (mandatory filters, validations)
5. Examples (input → output)
6. Links to references
7. Explicit limitations

**Guidelines**:
- Instructions < 5000 tokens
- Progressive disclosure: details in references/
- Every referenced file must have explicit link

---

### Phase 5: Validation (Dry-Run)
**Goal**: Verify before generation

**Preview includes**:
- [ ] Final structure diagram
- [ ] Complete SKILL.md preview
- [ ] Generated test cases
- [ ] Checklist compliance report

**Checklist verification** (12 points):
→ See [checklist-validation.md](references/checklist-validation.md)

**User approval required before Phase 6**

---

### Phase 6: Generation
**Goal**: Produce complete skill package

**Outputs generated**:
1. `skill-name/SKILL.md` - Main skill file
2. `skill-name/references/*.md` - Reference documentation
3. `skill-name/scripts/test_triggering.py` - Automated tests
4. `skill-name/templates/*` - Output templates (if needed)

**Post-generation**:
- Compliance report
- Deployment instructions
- Suggested test queries

---

## Critical Cheatsheet (Inline)

### YAML Frontmatter Rules
```yaml
---
name: kebab-case-max-64-chars      # REQUIRED
description: >-                    # REQUIRED, max 1024 chars
  Action verbs + file types + "Use when..." + "Not for..."
allowed-tools: Read, Grep, Glob    # OPTIONAL (Claude Code only)
---
```

### Description Formula
```
[WHAT it does] + [WHAT files/data] + [WHEN to use] + [WHEN NOT to use]
```

### Structure Limits
| Element | Limit |
|---------|-------|
| `name` | ≤64 chars, kebab-case |
| `description` | ≤1024 chars |
| SKILL.md body | <5000 tokens |
| Folder depth | Max 2 levels |

### Token Budget
| Level | Content | Tokens |
|-------|---------|--------|
| L1 | Frontmatter | ~100 (always loaded) |
| L2 | SKILL.md body | <5000 (on trigger) |
| L3 | References | Variable (on demand) |

### Anti-Patterns to Avoid
- ❌ Vague descriptions → random triggering
- ❌ Everything in SKILL.md → context overflow
- ❌ Unlinked reference files → never loaded
- ❌ Multi-purpose skills → split into focused skills
- ❌ Tabs in YAML → use spaces only

---

## Knowledge Base

### References
- [Best Practices Guide](references/best-practices-guide.md) - Complete methodology
- [Description Formulas](references/description-formulas.md) - Triggering patterns
- [YAML Rules](references/yaml-rules.md) - Syntax validation
- [Validation Checklist](references/checklist-validation.md) - 12-point verification
- [Domain Templates](references/domain-templates.md) - Pre-configured templates

### Templates
- [Pre-Analysis Template](templates/pre-analysis.md)
- [Skill Structure Template](templates/skill-structure.md)

### Scripts
- [Triggering Test Template](scripts/test_triggering_template.py)

---

## Supported Domains (Templates Available)

| Domain | Typical Use Cases |
|--------|-------------------|
| **SQL/Data** | Data warehouse queries, KPI analysis, reporting |
| **Code Review** | Security audit, best practices, refactoring |
| **Documentation** | Technical docs, API reference, guides |
| **File Processing** | PDF, Excel, CSV manipulation |
| **Workflow Automation** | Multi-step business processes |

---

## Limitations

This skill does NOT:
- Generate skills for highly volatile procedures
- Create skills duplicating Claude's native capabilities
- Build skills requiring external API integrations (use MCP instead)
- Generate skills in languages other than English (skill content only)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-10 | Initial release |

## Current: v1.0.0
