---
name: writing-skills
description: Use when creating new skill files, editing existing SKILL.md files, or reviewing skills before deployment — covers structure, CSO (discoverability), and quality standards
user-invocable: true
disable-model-invocation: true
---

# Writing Skills

## Overview

A **skill** is a reference guide for proven techniques, patterns, or tools. Skills help future Claude instances find and apply effective approaches.

**Skills are:** Reusable techniques, patterns, tools, reference guides  
**Skills are NOT:** Narratives about how you solved a problem once, project-specific conventions (those go in CLAUDE.md)

## SKILL.md Structure

**Frontmatter (YAML):**

- Required fields: `name`, `description`
- Max 1024 characters total
- `name`: Letters, numbers, hyphens only — no parentheses or special chars
- `description`: Third-person, describes ONLY when to use (NOT what it does) — see CSO section

```markdown
---
name: skill-name
description: Use when [specific triggering conditions and symptoms]
user-invocable: true # only if user should invoke with /skill-name
---

# Skill Name

## Overview

Core principle in 1-2 sentences.

## When to Use

Bullet list with symptoms and use cases. When NOT to use.

## Core Pattern

Before/after comparison or workflow steps.

## Quick Reference

Table or bullets for scanning.

## Common Mistakes

What goes wrong + fixes.
```

## Claude Search Optimization (CSO)

**The description field is the discovery mechanism.** Claude reads it to decide which skills to load.

### Description = Triggering Conditions ONLY

**NEVER summarize the skill's workflow in the description.**

**Why this matters:** Testing revealed that when a description summarizes the workflow, Claude follows the description instead of reading the full skill body. A description saying "code review between tasks" caused Claude to do ONE review, even though the skill's flowchart showed TWO reviews. Changing the description to triggering conditions only fixed it.

**The trap:** Descriptions that summarize workflow create a shortcut Claude will take. The skill body becomes documentation Claude skips.

```yaml
# BAD: Summarizes workflow — Claude may follow this instead of reading skill
description: Use when executing plans - dispatches subagent per task with code review between tasks

# GOOD: Just triggering conditions
description: Use when executing implementation plans with independent tasks in the current session
```

**Content rules:**

- Start with "Use when..."
- Include specific symptoms, situations, contexts
- Technology-agnostic unless skill is technology-specific
- Third person (injected into system prompt)
- Keep under 500 characters

### Keyword Coverage

Include words Claude would search for:

- Error messages: "race condition", "ENOTEMPTY", "hook timed out"
- Symptoms: "flaky", "hanging", "zombie"
- Tools: actual command names, library names

### Token Efficiency

Skills that load frequently must be concise.

| Skill type                  | Target word count |
| --------------------------- | ----------------- |
| Frequently-loaded workflows | < 200 words       |
| Other skills                | < 500 words       |

Techniques:

- Reference `--help` instead of documenting all flags inline
- Cross-reference other skills instead of repeating their content
- One excellent code example beats five mediocre ones

## Skill Types

| Type      | Description                    | Examples                                |
| --------- | ------------------------------ | --------------------------------------- |
| Technique | Concrete method with steps     | `root-cause-trace`, `cross-layer-check` |
| Pattern   | Way of thinking about problems | `careful`, `tdd`                        |
| Reference | API docs, tool documentation   | `playwright`, `cocoindex-code`          |

## Directory Structure

```
.claude/skills/
  skill-name/
    SKILL.md              # Main reference (required)
    supporting-file.*     # Only if needed for heavy reference or reusable tools
```

Keep inline: principles, concepts, code patterns < 50 lines.  
Separate file for: heavy reference (100+ lines), reusable scripts/templates.

## Quality Checklist

Before deploying any skill:

- [ ] `name` uses only letters, numbers, hyphens
- [ ] `description` starts with "Use when..." — no workflow summary
- [ ] Description is under 500 characters
- [ ] Keywords throughout for discoverability
- [ ] Clear overview with core principle
- [ ] No narrative storytelling ("in session 2025-10-03 we found...")
- [ ] One excellent example (not multi-language)
- [ ] Entry added to `claude/README.md` skills table (required by self-maintenance rule)

## Common Mistakes

| Mistake                           | Fix                                               |
| --------------------------------- | ------------------------------------------------- |
| Description summarizes workflow   | Rewrite as triggering conditions only             |
| Multiple language examples        | Pick the most relevant language, one good example |
| Narrative storytelling            | Convert to reusable technique/pattern             |
| Project-specific rules in skill   | Move to CLAUDE.md                                 |
| Generic labels (step1, helper2)   | Use semantic names                                |
| Flowchart for linear instructions | Use numbered list instead                         |
| No entry in README                | Add to skills table immediately                   |

## When to Create a Skill

**Create when:**

- Technique wasn't intuitively obvious
- You'd reference this again across projects
- Pattern applies broadly (not project-specific)

**Don't create for:**

- One-off solutions
- Standard practices well-documented elsewhere
- Project-specific conventions → CLAUDE.md instead
- Mechanical constraints enforceable with automation
