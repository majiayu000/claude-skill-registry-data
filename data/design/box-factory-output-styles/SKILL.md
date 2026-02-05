---
name: box-factory-output-styles
description: Interpretive guidance for Claude Code output styles - when they add value, when they don't, and how they relate to agents. Use when considering output styles or wondering if your workflow would benefit from them.
---

# Output Styles Skill

This skill helps you understand when output styles actually add value. **The key insight most people miss:** output styles affect the main Claude Code conversation, not your agents. If you're already using agents for specialized tasks, output styles might not add anything.

## Fundamentals

**Prerequisites:** Load the box-factory-architecture skill for component selection context.

**Core insight:** Output styles modify the main Claude Code session prompt. They do NOT affect agents, which have their own isolated prompts. Most confusion about output styles stems from misunderstanding this separation.

## Required Reading

Fetch official documentation with WebFetch:

- **<https://code.claude.com/docs/en/output-styles>** - Official specification and built-in styles

## Workflow Selection

| If you need to...                  | Go to...                                                                    |
| ---------------------------------- | --------------------------------------------------------------------------- |
| Understand output styles vs agents | [Critical Architecture Understanding](#critical-architecture-understanding) |
| Decide if you need an output style | [Decision Framework](#decision-framework)                                   |
| See when output styles help        | [When Output Styles Actually Help](#when-output-styles-actually-help)       |
| See when they don't help           | [When Output Styles Don't Help](#when-output-styles-dont-help)              |
| Create a custom output style       | [Custom Style Design](#custom-style-design)                                 |
| Identify common mistakes           | [Common Pitfalls](#common-pitfalls)                                         |

## Critical Architecture Understanding

### Output Styles vs Agents: They're Orthogonal

**This is the most important thing to understand:**

```text
Output styles → Affect main Claude Code session (where you type)
Agents        → Have their own isolated prompts (defined in agent files)
```

**What this means practically:**

- Your agents **don't inherit** output styles
- Your agents **already have** focused system prompts in their definitions
- Output styles change **your interactive session**, not delegated work

**Common misconception:** "Should I use an output style for my code review agent?"

**Reality:** Your agent already has a prompt that defines its behavior. Output styles are irrelevant to agents.

### Where Output Styles Actually Live

Output styles modify the system prompt for the **main conversation**. When you delegate to an agent via the Task tool, that agent:

- Gets its own isolated context
- Uses its own system prompt (from the agent file)
- Returns results to main conversation
- Is completely unaffected by your output style

## When Output Styles Actually Help

### 1. Learning/Onboarding (Explanatory Mode)

**Scenario:** You're exploring an unfamiliar codebase and want Claude to explain what it finds.

**What it does:** Adds "Insights" sections explaining:

- Why code is structured this way
- Architectural patterns discovered
- Tradeoffs in implementation choices

**When to use:**

- First week on a new project
- Reviewing code you didn't write
- Understanding legacy systems

**Switch:** `/output-style explanatory`

### 2. Deliberate Practice (Learning Mode)

**Scenario:** You want to build skills by doing, not just watching Claude work.

**What it does:**

- Assigns you small coding tasks with `TODO(human)` markers
- Provides feedback on your implementations
- Explains concepts while you practice

**When to use:**

- Learning a new language or framework
- Junior developers wanting guided practice
- Deliberately building muscle memory

**Switch:** `/output-style learning`

### 3. Non-Engineering Domains

**Scenario:** You're using Claude Code's file system capabilities for non-coding work.

**What it does:** Removes software engineering assumptions entirely.

**Example domains:**

- Technical writing and documentation analysis
- Content strategy and reorganization
- Research synthesis across documents
- UX research analysis

**Critical:** For these, `keep-coding-instructions: false` (the default) is correct.

### 4. Session-Wide Persona Shift

**Scenario:** You want a consistent personality across an entire work session.

**What it does:** Changes interaction patterns for everything, not just specific tasks.

**Examples:**

- Socratic mentor (asks questions instead of giving answers)
- Verbose explainer (detailed reasoning on every decision)
- Terse executor (minimal explanation, maximum action)

**Key distinction:** This affects ALL interactions in the session, not isolated tasks.

## When Output Styles Don't Help

### Already Using Agents for Specialized Work

**Scenario:** You have agents for code review, writing, testing, etc.

**Why styles don't help:** Your agents already have focused prompts. The main conversation just delegates and integrates results.

**Example:** Box Factory plugins - the skill-writer, sub-agent-writer, validation-agent all have their own prompts. Adding an output style to the main session doesn't change how those agents behave.

### Project Conventions and Context

**Scenario:** You want Claude to follow team coding standards, understand project structure, use specific tools.

**Better alternative:** CLAUDE.md

**Why:** CLAUDE.md is always loaded, team-shareable via git, and adds context without changing personality. It works WITH the default software engineering mode, not against it.

### Enforcement and Automation

**Scenario:** You want to ensure tests run before commits, linting passes, certain files aren't modified.

**Better alternative:** Hooks

**Why:** Hooks can actually block operations (exit code 2). Output styles are just personality suggestions that can be overridden. You can't enforce with personality.

### Standard Software Engineering Work

**Scenario:** Writing code, fixing bugs, refactoring, typical development.

**Why default is optimal:** The default output style IS the software engineering system prompt. It's already optimized for this. Adding a coding-focused output style is redundant.

## Decision Framework

Ask these questions:

**1. Am I doing software engineering?**

- Yes → Default style is optimal
- No → Consider custom style without coding instructions

**2. Do I need personality change or just context?**

- Personality (how Claude thinks/responds) → Output style
- Context (what Claude knows about project) → CLAUDE.md

**3. Is this for the whole session or specific tasks?**

- Whole session → Output style makes sense
- Specific tasks → Use agents with focused prompts

**4. Do I need enforcement or just guidance?**

- Enforcement → Hooks
- Guidance → Output style or CLAUDE.md

**5. Am I already delegating to agents?**

- Yes → Output styles probably don't add value
- No → Consider if an agent would be better first

## Built-in Styles (Official Specification)

| Style           | Purpose              | Use When                          |
| --------------- | -------------------- | --------------------------------- |
| **Default**     | Software engineering | Normal development work           |
| **Explanatory** | Educational insights | Learning codebases, onboarding    |
| **Learning**    | Deliberate practice  | Building skills, pair programming |

## Custom Style Design

### When Custom Styles Make Sense

- Non-engineering domains (content, research, analysis)
- Specific interaction patterns (Socratic, verbose, terse)
- Session-wide persona that built-in styles don't cover

### File Structure

```markdown
---
name: Style Display Name
description: Brief description for /output-style menu
keep-coding-instructions: false
---

# Persona

[Specific personality, expertise, approach]

## Interaction Patterns

[How to communicate, what to emphasize]

## Constraints

[Boundaries of the role]
```

### Storage Locations

- User level: `~/.claude/output-styles/[style-name].md`
- Project level: `.claude/output-styles/[style-name].md`

### The `keep-coding-instructions` Toggle

- `true` = Coding specialist variant (TDD expert, debugging coach)
- `false` = Non-engineering domain (content, research, analysis)

**Default is false** - meaning engineering assumptions are removed.

## Common Pitfalls

### Pitfall: Style for What Should Be an Agent

**Problem:** Creating output style for specialized task

```markdown
---
name: Security Reviewer
---
Focus on security vulnerabilities, OWASP top 10...
```

**Why it fails:** This is a task, not a personality. It pollutes your main session with security focus even when doing other work.

**Better:** Create a security-reviewer agent with Read-only tools.

### Pitfall: Style for What Should Be CLAUDE.md

**Problem:** Using output style for project context

```markdown
---
name: Our Project
---
Use React 18, follow ESLint config, run tests before commits.
```

**Why it fails:** This is context, not personality. It replaces the engineering system prompt when you want to augment it.

**Better:** Put in CLAUDE.md, keep default style.

### Pitfall: Style for What Should Be Hooks

**Problem:** Trying to enforce with personality

```markdown
---
name: Safe Mode
---
NEVER modify production files. ALWAYS run tests first.
```

**Why it fails:** Claude can still be convinced to override. No actual enforcement.

**Better:** Use PreToolUse hooks that exit 2 on violations.

### Pitfall: Output Style for Agents

**Problem:** Thinking agents need output styles

**Reality:** Agents have their own prompts. They don't use or inherit output styles. If you want different agent behavior, modify the agent's system prompt, not the session's output style.

## Practical Example: Box Factory Analysis

**Question:** Would any Box Factory agents benefit from output styles?

**Answer:** No, and here's why:

- `skill-writer` has its own prompt about skill design
- `sub-agent-writer` has its own prompt about agent patterns
- `validation-agent` has its own prompt about validation rules
- `component-reviewer` has its own prompt about review criteria

These agents operate in isolated contexts with focused instructions. The main conversation delegates to them and integrates results. Output styles only affect the main conversation, which is doing software engineering work (writing/managing Claude Code components) - exactly what the default style is optimized for.

**When output styles WOULD help for Box Factory work:**

- **Explanatory mode** if you're learning how the plugin system works
- **Learning mode** if you want to practice writing agents/skills yourself
- **Custom "plugin architect" style** if you want opinionated design feedback in every interaction (but a reviewer agent is probably better)

## Summary

**Output styles are for session-level personality transformation.**

They're most valuable when:

- You're not doing standard software engineering
- You want educational/learning mode
- You need consistent personality across all interactions
- Built-in styles (explanatory, learning) match your goal

They're NOT valuable when:

- You're doing normal development (default is optimal)
- You're using agents for specialized work (they have their own prompts)
- You need project context (use CLAUDE.md)
- You need enforcement (use hooks)

**The honest assessment:** Most developers doing software engineering get the most value from the default style + CLAUDE.md + agents. Output styles shine for learning, onboarding, and non-engineering domains.

## Quality Checklist

Before creating or using output styles:

**Need Assessment:**

- [ ] Doing software engineering? (If yes, default style is optimal)
- [ ] Need personality change vs context? (Context → CLAUDE.md)
- [ ] Whole session vs specific tasks? (Specific → agents)
- [ ] Need enforcement vs guidance? (Enforcement → hooks)
- [ ] Already delegating to agents? (If yes, styles probably don't help)

**Custom Style Design (if creating):**

- [ ] Fetched official documentation
- [ ] `keep-coding-instructions` set appropriately (true for coding variants, false for non-engineering)
- [ ] Description field included (improves discoverability)
- [ ] Focused on personality/interaction patterns, not project context
- [ ] Saved in correct location (user vs project level)

## Documentation References

- <https://code.claude.com/docs/en/output-styles> - Official specification
- <https://code.claude.com/docs/en/sub-agents.md> - Agent architecture
- <https://code.claude.com/docs/en/hooks> - Enforcement via hooks
- <https://code.claude.com/docs/en/memory#claudemd> - Project context
