---
name: claude-code-patterns
description: Use when deciding whether to create a skill, command, or agent. Provides decision framework, templates, and best practices for Claude Code abstractions.
version: "2.1.0"
---

# Claude Code Abstraction Patterns

Guide for deciding when and how to create skills, commands, and agents.

## Official Documentation

- **Skills Overview**: https://docs.claude.com/en/docs/claude-code/skills
- **Skills Repository**: https://github.com/anthropics/skills
- **Best Practices**: https://www.anthropic.com/engineering/claude-code-best-practices

## The Three Abstractions

| Type | Purpose | Trigger | Scope |
|------|---------|---------|-------|
| **Skill** | Domain knowledge & best practices | Working in a domain | Loaded on demand |
| **Command** | Specific action or workflow | User invokes `/command` | Single task |
| **Agent** | Autonomous complex task | Delegation needed | Multi-step work |

## Decision Framework

### When to Create a SKILL

Create a skill when you have **reusable domain knowledge** that should influence how code is written.

**Signals:**
- You're explaining the same best practices repeatedly
- A technology/framework has specific patterns to follow
- There are "always do X" or "never do Y" rules
- Knowledge applies across multiple files/features

**Examples:**
- `astro` — Astro framework best practices
- `tailwind` — Tailwind CSS patterns
- `gsap` — Animation guidelines
- `plans` — Project planning context

**File Structure (Recommended):**
```
.claude/skills/
└── skill-name/
    ├── SKILL.md          # Required: Main skill file
    ├── reference.md      # Optional: Extended documentation
    ├── examples.md       # Optional: Additional examples
    ├── scripts/          # Optional: Helper scripts
    │   └── helper.py
    └── templates/        # Optional: Template files
        └── template.txt
```

**Frontmatter Schema:**
| Field | Required | Max Length | Notes |
|-------|----------|------------|-------|
| `name` | Yes | 64 chars | Lowercase, hyphens only, must match folder name |
| `description` | Yes | 1024 chars | Critical for discovery—be specific about when to use |
| `version` | Recommended | — | Semantic versioning (e.g., "1.0.0") |

**Description Pattern:**
```
Use when [specific context/trigger]. Applies [topic] best practices for [focus areas].
```

**Template:**
```markdown
---
name: skill-name
description: Use when [specific context]. Applies [topic] best practices for [focus areas].
version: "1.0.0"
---

# Skill Name

Brief overview of what this skill covers.

## Core Principles

1. First principle
2. Second principle

## Patterns

### Pattern Name
\`\`\`code
example
\`\`\`

## Common Patterns

Document recurring patterns with examples.

## Avoid

- Anti-pattern 1 (explain why)
- Anti-pattern 2 (explain why)
```

**Skill Content Guidelines:**
- Keep instructions clear and actionable
- Provide concrete code examples
- Include "Avoid" section with anti-patterns
- Link to official documentation where applicable
- Focus on domain-specific knowledge, not general programming
- Make skills standalone and reusable across projects

**For Language/Framework Skills, Also Include:**
- **File Organization** — Directory structure patterns, where to put what
- **Naming Conventions** — Files, functions, classes, variables
- **Import Organization** — Ordering and grouping of imports
- **Module Patterns** — When to split, how to structure exports

Not all skills need these sections. Only include when:
- The technology has established conventions (TypeScript, Astro, React)
- File structure decisions impact maintainability
- There are common organizational anti-patterns to avoid

Skills like `gsap` (animation library) or `lenis` (smooth scroll) don't need file structure guidance—they're used within existing structures, not defining them.

### When to Create a COMMAND

Create a command when you have a **specific workflow** that users will invoke explicitly.

**Signals:**
- User will type `/something` to trigger it
- It's a discrete action with clear start/end
- Takes optional arguments
- Repeatable process

**Examples:**
- `/commit` — Create git commit
- `/plan-status` — Show phase statuses
- `/idea` — Capture to backlog
- `/review` — Code review

**File Structure:**
```
.claude/commands/
└── command-name.md    # Single markdown file
```

**Frontmatter Schema:**
| Field | Required | Notes |
|-------|----------|-------|
| `description` | Yes | One-line description of what command does |
| `allowed-tools` | Recommended | Comma-separated list of tools |
| `argument-hint` | Optional | Show argument placeholders |
| `aliases` | Optional | Alternative command names |

**Template:**
```markdown
---
description: What this command does (one line)
allowed-tools: Tool1, Tool2
argument-hint: [arg1] [arg2]
---

# Command Name

What this command accomplishes.

## Usage

\`\`\`
/command arg1 arg2
\`\`\`

## Instructions

1. Step one
2. Step two

## Output Format

Expected output structure.
```

**Command Content Guidelines:**
- Be explicit about steps and expected behavior
- Define clear output format
- Handle both with-arguments and no-arguments cases
- Include examples of typical usage

### When to Create an AGENT

Create an agent when you need **autonomous execution** of complex, multi-step tasks.

**Signals:**
- Task requires many tool calls
- Could run without human intervention
- Benefits from focused context
- Too complex for a command
- Delegation would be helpful

**Examples:**
- `plan-executor` — Implement entire phases
- `code-reviewer` — Comprehensive review
- `test-writer` — Generate test suites
- `doc-writer` — Create documentation

**File Structure:**
```
.claude/agents/
└── agent-name.md    # Single markdown file
```

**Frontmatter Schema:**
| Field | Required | Notes |
|-------|----------|-------|
| `name` | Yes | Lowercase, hyphenated identifier |
| `description` | Yes | What agent does and when to use it |
| `tools` | Yes | Comma-separated list of allowed tools |
| `model` | Optional | Model to use (sonnet, opus, haiku) |

**Template:**
```markdown
---
name: agent-name
description: What this agent does (one line). Use for [use cases].
tools: Tool1, Tool2, Tool3
model: sonnet
---

# Agent Name

You are an agent that [purpose].

## Your Role

- What you do
- What you're responsible for

## Process

1. How you approach tasks
2. Steps you follow

## Guidelines

- Important rules
- Quality standards

## Output

What you return when done.
```

**Agent Content Guidelines:**
- Write in second person ("You are an agent that...")
- Define clear process steps
- Specify expected output format
- Include what NOT to do
- Provide example invocations

## Decision Tree

```
Is it reusable knowledge/best practices?
├── Yes → SKILL
└── No
    ├── Is it a user-invoked action?
    │   ├── Yes → COMMAND
    │   └── No
    │       └── Is it autonomous multi-step work?
    │           ├── Yes → AGENT
    │           └── No → Maybe not needed
```

## Combination Patterns

Often abstractions work together:

### Skill + Command
- Skill provides context
- Command triggers action that uses skill knowledge
- Example: `plans` skill + `/plan-start` command

### Command + Agent
- Command initiates
- Agent executes
- Example: `/plan-start` could invoke `plan-executor`

### Skill + Agent
- Skill loaded into agent context
- Agent applies knowledge autonomously
- Example: `code-reviewer` agent uses `software-engineering` skill

## Naming Conventions

**Skills:**
- Lowercase, hyphenated
- Technology or domain name
- Examples: `astro`, `gsap`, `software-engineering`

**Commands:**
- Lowercase, hyphenated
- Verb or action-oriented
- Examples: `/commit`, `/plan-status`, `/idea`

**Agents:**
- Lowercase, hyphenated
- Role or actor name
- Examples: `code-reviewer`, `plan-executor`, `test-writer`

## Anti-Patterns

### Over-Abstraction
Don't create abstractions for:
- One-time tasks
- Simple operations
- Things that change frequently
- Highly project-specific logic

### Under-Abstraction
Do create abstractions when:
- You've repeated something 3+ times
- Others would benefit from the pattern
- Consistency matters

### Wrong Type
- Don't use a command when you need autonomous work (use agent)
- Don't use an agent for simple actions (use command)
- Don't use a skill for workflows (use command)

## Evaluation Checklist

Before creating an abstraction, ask:

1. [ ] Is this reusable beyond this specific case?
2. [ ] Will this be used more than 2-3 times?
3. [ ] Does it reduce cognitive load?
4. [ ] Is it clear which type it should be?
5. [ ] Does a similar abstraction already exist?
6. [ ] Is it named clearly and consistently?

## Related Commands

- `/codify` (alias: `/formalize`) — Analyze if a pattern should be codified
- `/patterns` — List all skills, commands, and agents in the project
