---
name: cp-writing-style
description: "Expert guidance on writing in Chamath Palihapitiya's communication style across 5 formats (Annual Letters, Customer Briefs, Emails, Policy Ideas Briefs, Learn with Me Presentations). Use when helping with any writing task, document creation, editing, reviewing communications, or answering questions about how to write something. Includes 10 universal principles, format-specific playbooks, internal team email guidance, templates, decision frameworks, and quality control checklists. MODULAR ARCHITECTURE: Optimized for LLM consumption with selective context loading (core + format)."
---

# CP Writing Style Guide v4.1.0

**Version**: 4.1.0
**Last Updated**: 2025-11-14

## Changelog

**v4.1.0 (2025-11-14)**: **REFINEMENT - Persuasion Elements Implicit** - Removed Principle 11 (RIZZ) as explicit principle. Persuasion, energy modulation, and vulnerability remain implicit in existing 10 principles and demonstrated through examples. Deleted advanced-rhetoric.md module. Kept format-internal-team-emails.md with Top of Mind examples but removed explicit persuasion scoring. Total system: ~10.5K words across 8 modules. Closer to original v3.0.0 philosophy with valuable internal email examples retained.

**v4.0.0 (2025-11-14)**: **RIZZ FACTOR INTEGRATION** - Added Principle 11 (Strategic Authenticity - The RIZZ Factor) covering charisma/persuasion layer with 4 components: selective vulnerability, energy modulation, intellectual flex, contrarian positioning. Created 2 new modules: advanced-rhetoric.md (~1.5K words - RIZZ deep dive) and format-internal-team-emails.md (~1.5K words - internal team updates with 5 full Top of Mind examples). Updated format-emails.md to include Type 4 (Internal Team Updates). Enhanced quick-reference.md with comprehensive RIZZ cheatsheet. Total system: ~12K words across 9 files. Enhanced Principle 2 with guidance on qualifying imprecise estimates.

**v3.0.0 (2025-10-30)**: **MAJOR ARCHITECTURAL REDESIGN** - Transformed from monolithic guide to modular system optimized for LLM consumption. Created 7 specialized files (core-principles.md + 5 format modules + quick-reference.md) totaling ~9.3K words. Added MUST/SHOULD/MAY hierarchy to every principle. Added "When to Deviate" guidance. Created decision trees throughout. Token reduction: 85-90% per typical task. Added CRITICAL RULE: Never fabricate data when applying "Data Over Adjectives" principle.

---

This skill provides comprehensive guidance on writing in Chamath Palihapitiya's distinctive communication style using a **modular, LLM-optimized architecture**.

## When to Use This Skill

Claude should invoke this skill when:
- User asks for help writing any type of document
- User requests document review or editing
- User asks "how should I write..." or "what format should I use..."
- User mentions any of the 5 formats: Annual Letters, Customer Briefs, Emails, Policy Ideas Briefs, or Learn with Me Presentations
- User asks about writing style, tone, structure, or formatting
- User needs templates or examples for business communications

## Modular Architecture

### File Structure
```
core-principles.md (~3K words) - ALWAYS LOAD
format-customer-briefs.md (~1.5K words) - Load for customer briefs
format-emails.md (~1K words) - Load for emails (now includes 4 types)
format-internal-team-emails.md (~1.5K words) - Load for internal team updates
format-annual-letters.md (~1K words) - Load for annual letters
format-policy-ideas.md (~1K words) - Load for policy briefs
format-learn-with-me.md (~1K words) - Load for presentations
quick-reference.md (~1K words) - Optional cheatsheet
```

### Key Features
1. **MUST/SHOULD/MAY hierarchy** explicit on all 10 principles
2. **"When to Deviate" guidance** for each principle
3. **Decision trees** throughout (format selection, pattern choice)
4. **At-a-glance specs tables** for every format
5. **Self-contained modules** - each format independently loadable
6. **Internal team email examples** - 5 full "Top of Mind" emails demonstrating CP's natural style
7. **CRITICAL RULE**: Never fabricate data - use bracketed placeholders when data is missing

## How to Use This Skill (v4.1.0)

### CRITICAL: Modular Loading Pattern

**ALWAYS follow this sequence:**

1. **Load core-principles.md first** (REQUIRED for every task)
   - Contains: 10 Universal Principles, format decision tree, banned/golden phrases, meta-rules

2. **Load appropriate format module** based on task:
   - Writing customer brief? → Load `format-customer-briefs.md`
   - Writing email? → Load `format-emails.md` (tactical 50-200 words)
   - Writing internal team update? → Load `format-internal-team-emails.md` (200-600 words)
   - Writing annual letter? → Load `format-annual-letters.md`
   - Writing policy ideas? → Load `format-policy-ideas.md`
   - Creating presentation? → Load `format-learn-with-me.md`

3. **Optionally load quick-reference.md** for spot checks

### Response Format

**IMPORTANT**: When this skill is invoked, ALWAYS begin your response with:
```
Using CP Writing Style Guide v4.1.0 - Modular Architecture
Loaded: core-principles.md + [format-module-name]
```

### MANDATORY: 3-Pass Method

**You have NOT applied CP style unless you complete all 3 passes:**

1. **PASS 1**: Write to think (get ideas out, use placeholders)
2. **PASS 2**: Apply ALL 10 principles (checklist in core-principles.md)
3. **PASS 3**: Cut 30% more (ruthless editing)

**FINAL CHECK**: Word count reduced 50-80% from Pass 1? All MUST principles applied?

**If you skip Pass 2 or Pass 3, you have NOT applied CP style. You've only started.**

### Example Usage

**Task: Help user write a customer brief**
```
Response starts with:
"Using CP Writing Style Guide v4.1.0 - Modular Architecture
Loaded: core-principles.md + format-customer-briefs.md"

[Then provide guidance using the loaded modules]
```

**Task: Help user write an internal team update email**
```
Response starts with:
"Using CP Writing Style Guide v4.1.0 - Modular Architecture
Loaded: core-principles.md + format-internal-team-emails.md"

[Then provide guidance using the loaded modules]
```

## The 10 Universal Principles (Quick Reference)

**🚨 CRITICAL: NEVER FABRICATE DATA 🚨**
When applying Principle 2 (Data Over Adjectives), you can ONLY use data from the original source material. If data is missing, use bracketed placeholders `[Need: description]` or state "data not available." Fabricated numbers are worse than vague language.

1. **Radical Clarity**: Say it simpler [MUST]
2. **Data Over Adjectives**: Show numbers from source, not descriptions [MUST] - NEVER INVENT DATA
3. **Honesty First**: Acknowledge failures upfront [MUST]
4. **First-Principles Thinking**: Explain from fundamentals [SHOULD]
5. **Economy of Language**: Cut every wasted word [MUST]
6. **Active Voice**: People do things [MUST]
7. **Context Provision**: Always explain "why" [MUST]
8. **Attribution**: Credit sources [SHOULD]
9. **Forward-Looking**: Point to next, drive outcomes [MUST]
10. **Format Follows Function**: Structure serves message [SHOULD]

*See `core-principles.md` for detailed explanations, examples, and "When to Deviate" guidance.*

## 5 Complete Format Playbooks

### 1. Annual Letters (2,000-5,000 words)
- **Purpose**: Strategic reflection + performance reporting
- **Audience**: Investors/public
- **Key Feature**: Frontload performance data (no hiding)
- **Load**: `format-annual-letters.md`

### 2. Customer Briefs (500-2,000 words)
- **Purpose**: Progress reporting + stakeholder management
- **Audience**: Business stakeholders (internal or external)
- **Key Feature**: Losses before wins, heavy tables, color-coded status
- **Load**: `format-customer-briefs.md`
- **Patterns**: Pattern 1 (Strategic Hook) vs Pattern 2 (Decision-Driven)

### 3. Emails (50-200 words)
- **Purpose**: Quick tactical communication
- **Audience**: Colleagues, team members
- **Key Feature**: Single purpose only, minimal formatting
- **Load**: `format-emails.md`
- **Types**: Philosophy sharing, Personnel changes, Directives, Internal team updates (200-600 words)

### 3a. Internal Team Emails (200-600 words)
- **Purpose**: Weekly/monthly progress updates, cultural reinforcement
- **Audience**: Internal team
- **Key Feature**: Numbered hierarchy, energy modulation (celebrate/correct/teach)
- **Load**: `format-internal-team-emails.md`
- **Examples**: 5 full "Top of Mind" emails included

### 4. Policy Ideas Briefs (3,000-5,000 words)
- **Purpose**: Policy recommendations + implementation plans
- **Audience**: Policymakers, decision-makers
- **Key Feature**: 70-80% bullets, imperative verbs
- **Load**: `format-policy-ideas.md`

### 5. Learn with Me Presentations (40-80 slides)
- **Purpose**: Educational deep-dives on complex topics
- **Audience**: Learners, curious audience
- **Key Feature**: Visual-first, one idea per slide
- **Load**: `format-learn-with-me.md`

## Key Decision Framework

```
Purpose: Quick tactical → Email (50-200 words)
Purpose: Progress update → Customer Brief (500-2,000 words)
Purpose: Strategic reflection → Annual Letter (2,000-5,000 words)
Purpose: Policy recommendations → Policy Ideas Brief (3,000-5,000 words)
Purpose: Educational deep-dive → Learn with Me (40-80 slides)
```

*See `core-principles.md` for complete decision tree with detailed criteria.*

## File Reference

| File | Purpose | When to Load |
|------|---------|--------------|
| `core-principles.md` | 10 Universal Principles + decision tree | ALWAYS (required) |
| `format-customer-briefs.md` | Customer brief playbook | Writing customer briefs |
| `format-emails.md` | Email playbook (4 types) | Writing tactical emails (50-200 words) |
| `format-internal-team-emails.md` | Internal team update playbook + 5 examples | Writing team updates (200-600 words) |
| `format-annual-letters.md` | Annual letter playbook | Writing annual letters |
| `format-policy-ideas.md` | Policy ideas playbook | Writing policy briefs |
| `format-learn-with-me.md` | Presentation playbook | Creating presentations |
| `quick-reference.md` | Cheatsheet (tables, checklists) | Quick lookups |

---

**For detailed guidance**: Load the appropriate module files based on your task.
**For quick lookups**: See `quick-reference.md`
