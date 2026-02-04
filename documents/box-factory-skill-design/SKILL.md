---
name: box-factory-skill-design
description: Meta-skill that teaches how to design Claude Code skills following the Box Factory philosophy. Helps you understand when to create skills, how to structure them for low maintenance, and how to add value beyond documentation. Use when creating or reviewing skills.
---

# Skill Design Skill

This meta-skill teaches you how to design excellent Claude Code skills. **Skills are unique among Claude Code components** - they provide progressive knowledge disclosure and guidance that loads when relevant.

## Fundamentals

**Everything in this skill is built on top of the box-factory-architecture skill. Load that first!**

## Workflow Selection

| If you need to...                 | Go to...                                                     |
| --------------------------------- | ------------------------------------------------------------ |
| Get folder structure              | [skill-structure.md](skill-structure.md)                     |
| Write SKILL.md file               | [skill-md.md](skill-md.md)                                   |
| Decide what to include vs exclude | [knowledge-delta.md](knowledge-delta.md)                     |
| Write decision-making content     | box-factory-architecture skill (decision frameworks section) |
| Look up a specific anti-pattern   | [common-pitfalls.md](common-pitfalls.md)                     |
| Validate before completing        | [skill-md.md](skill-md.md) (Quality Checklist)               |

> **Creating a skill?** Start with [skill-md.md](skill-md.md) for the template and quality checklist. **Traverse when:** writing any SKILL.md file, validating before completion.

## Official Documentation

Fetch the official skills documentation for current syntax and features:

- **<https://code.claude.com/docs/en/skills>** - Official skills documentation

## Core Understanding

### Skills Are Progressive Knowledge Disclosure

**Key insight:** Skills solve the "you can't put everything in the system prompt" problem.

```text
Base Prompt (always loaded)
    ↓
Topic becomes relevant
    ↓
Skill loads automatically
    ↓
Provides specialized knowledge
```

- **Without skills:** Important knowledge buried in long prompts or forgotten
- **With skills:** Knowledge loads automatically when topics become relevant
- **Value proposition:** Right information at the right time, without token bloat

**Decision test:** Does this information need to be available across multiple contexts, but not always?

### Skills vs System Prompts vs Memory (eg CLAUDE.md)

| Component          | Use For                                                                                                     |
| ------------------ | ----------------------------------------------------------------------------------------------------------- |
| **Skills**         | Substantial procedural expertise (20+ lines), domain knowledge needed sporadically, interpretive frameworks |
| **System prompts** | Always-relevant instructions, core behavior, universal constraints                                          |
| **Memory**         | Project-specific context, repository structure, team conventions, always-loaded information                 |

### The Knowledge Delta Principle

**Critical:** Skills should only document what Claude doesn't already know.

Claude's training includes common tools, standard workflows, and general best practices. Skills that duplicate this waste tokens.

**Deep dive:** [knowledge-delta.md](knowledge-delta.md) - Full include/exclude criteria with decision test. **Traverse when:** deciding what content to include, reviewing for bloat. **Skip when:** clear user-specific content, already understand delta principle.

**Quick test:** Would Claude get this wrong without the skill? If no, don't include it.

## The Box Factory Philosophy

### 1. Low-Maintenance by Design

**Point to official documentation for details Claude might not know:**

```markdown
## Official Documentation

For syntax details or recent changes, fetch:

- **https://code.claude.com/docs/en/skills** - Skills documentation
```

**Why:** Documentation changes; skills that defer stay valid.

**Critical nuance - doc fetching depends on knowledge reliability:**

| Topic Type                                           | Claude's Knowledge | Guidance                  |
| ---------------------------------------------------- | ------------------ | ------------------------- |
| **Post-training tech** (Claude Code, new frameworks) | Unreliable         | Fetch when creating/using |
| **Established tools** (git, ruff, black, pytest)     | Reliable           | Fetch only for edge cases |

**Don't hardcode:**

- Model names, tool lists, version-specific syntax

**Do reference:**

- Official docs via WebFetch instructions

### 2. Two-Layer Approach

**Layer 1: Official Specification**

- What the docs explicitly say
- Required fields and syntax
- Mark accordingly: `(Official Specification)`

**Layer 2: Best Practices or User Preference**

- What the docs don't emphasize
- Common gotchas and anti-patterns
- Mark accordingly: `## X (Best Practices)`

**Example:**

```markdown
<!-- Official specification lists the `description` field is optional and defaults to first line. -->
## Description Field Design (Best Practices)

Always include `description` even though it's optional - improves discoverability.
```

### 3. Evidence-Based Recommendations

All claims must be:

- Grounded in official documentation, **OR**
- Clearly marked as opinionated best practices, **OR**
- Based on documented common pitfalls

**Avoid:** Presenting opinions as official requirements.

**Deep dive:** [common-pitfalls.md](common-pitfalls.md) - Catalog of anti-patterns with symptoms and fixes. **Traverse when:** reviewing skills, debugging why a skill isn't working, checking for common mistakes. **Skip when:** creating new skill from scratch, following patterns above.

## When to Create Skills

### Skill vs Other Components

For the full decision framework on choosing between Skills, Agents, Commands, Hooks, and Memory, load the `box-factory-architecture` skill.

**Quick test:** Is this knowledge that shapes behavior, or work to be done?

- Knowledge → Skill
- Work → Agent

### Scope Guidelines

**Good skill scope:**

- Focused on single domain
- Self-contained knowledge
- Clear boundaries
- Composable with other skills

**Bad skill scope:**

- "Everything about development" (too broad)
- Just 3-4 bullet points (put in CLAUDE.md)
- Project-specific details (put in CLAUDE.md)

## File Structure

Skills live in subdirectories within `skills/`:

```text
plugin-name/
├── skills/
│   ├── skill-one/
│   │   ├── SKILL.md          # Required (uppercase)
│   │   ├── some-topic.md     # Optional subfiles (any name)
│   │   └── another-topic.md
│   └── skill-two/
│       └── SKILL.md
```

Only `SKILL.md` has a required name. Subfiles can use any descriptive names.

**Deep dive:** [skill-structure.md](skill-structure.md) - Complete folder layouts, splitting guidance, navigation table patterns. **Traverse when:** structuring complex skills, deciding subfile organization, adding scripts or assets. **Skip when:** simple single-file skill, basic structure questions answered above.

## Documentation References

**Official documentation:**

- https://code.claude.com/docs/en/skills - Official skills documentation

This skill demonstrates its own patterns: routes to subfiles for reference content, keeps the main file focused on philosophy, and defers to official docs.
