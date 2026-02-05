---
name: sub-agent-design
description: Interpretive guidance for designing Claude Code sub-agents. Helps apply official documentation effectively and avoid common pitfalls. ALWAYS use when creating or reviewing sub-agents (aka agents or subagents).
---

# Sub-agent Design

This skill provides interpretive guidance for creating Claude Code sub-agents (aka Subagents aka Agents). It helps you understand what the docs mean and how to create excellent sub-agents.

## Fundamentals

**Everything in this skill is built on top of the box-factory-architecture skill. Load that first!**

This skill adds sub-agent-specific guidance on top of that foundation.

## Workflow Selection

| If you need to...                      | Go to...                                                                   |
| -------------------------------------- | -------------------------------------------------------------------------- |
| Understand sub-agent isolation model   | `box-factory-architecture` skill (load first)                              |
| Decide sub-agent vs command vs skill   | `box-factory-architecture` skill (component selection)                     |
| Decide what goes in sub-agent vs skill | [Sub-agent-Skill Relationship](#sub-agent-skill-relationship)              |
| Structure the agent body               | [Agent Body Structure](#agent-body-structure)                              |
| Auto-load skills in a sub-agent        | [The `skills` Field](#the-skills-field-best-practice)                      |
| Write Skill Usage section              | [Skill Usage Section Pattern](#skill-usage-section-pattern)                |
| Inline validation checklist            | [Inlining Quality Checklists](#inlining-quality-checklists)                |
| Pick tools for a sub-agent             | [Tool Selection Philosophy](#tool-selection-philosophy)                    |
| Know which tool is forbidden           | [Never Include AskUserQuestion](#never-include-askuserquestion)            |
| Understand why creators need Bash      | [Bash is Foundational for Creators](#bash-is-foundational-for-creators)    |
| Pair WebFetch with skills              | [WebFetch Pairs with Skills](#webfetch-pairs-with-skills-for-verification) |
| Determine file path for new sub-agent  | `box-factory-architecture` skill (component-paths)                         |
| Write the description field            | [Description Field Design](#description-field-design)                      |
| Avoid common mistakes                  | [Common Gotchas](gotchas.md)                                               |
| Check color for status line            | [Color Selection](#color-selection)                                        |
| Validate before completing             | [Quality Checklist](#quality-checklist)                                    |

## Quick Start

Sub-agent file structure:

```markdown
---
name: my-agent
description: Does X when Y. ALWAYS use when Z.
tools: Read, Grep, Glob, Skill
skills: my-plugin:my-design-skill
color: green
---

# My Agent

This sub-agent [purpose].

## Process

1. [Step one]
2. [Step two]

## Constraints

- Never include "ask the user" phrases (sub-agents can't interact with users)
```

**Critical:** Sub-agents operate in isolated context and return results. They cannot ask users questions.

## Agent Body Structure

The body of a sub-agent (everything after YAML frontmatter) defines its system prompt.

**Required:**

| Section  | Purpose                           |
| -------- | --------------------------------- |
| H1 Title | Agent identity. Single H1 only.   |
| Process  | Numbered steps the agent follows. |

**Optional:**

| Section        | When to Include                                            |
| -------------- | ---------------------------------------------------------- |
| Opening line   | Brief statement of purpose (one sentence after H1)         |
| Prerequisites  | Skills or conditions required before starting              |
| Skill Usage    | **When agent loads skills via `skills` field** (see below) |
| Constraints    | Behavioral rules during execution                          |
| Error Handling | Table of edge cases and responses                          |

**Section naming:**

- "Prerequisites" = things that must be true before starting (skill availability, environment)
- "Skill Usage" = navigation pointers for loaded skills (what to consult each for)
- "Constraints" = behavioral limitations during execution
- "Error Handling" = edge case responses (typically a table)

**Minimal agent:**

```markdown
# Agent Name

## Process

1. **Step one**
2. **Step two**
```

**Full agent (with skills):**

```markdown
# Agent Name

This sub-agent [purpose].

## Prerequisites

The following skills must be available. If they are not, report failure and stop:

- skill-one
- skill-two

## Skill Usage

Follow the **Workflow Selection** table in each loaded skill to navigate to the right guidance.

**skill-one** - Consult for:

- [Aspect A] (Section Name)
- [Aspect B] (Section Name)

**skill-two** - Consult for:

- [Aspect C] (Section Name)
- [Aspect D] (Section Name)

## Process

1. **Understand requirements** from the caller
2. **Design** by navigating loaded skills:
   - Follow skill-one for [specific decisions]
   - Consult skill-two for [other decisions]
3. **Execute** the task
4. **Validate** - ALL items must pass before completing:
   - [ ] Checklist item one
   - [ ] Checklist item two
   - [ ] Checklist item three
   **If ANY item fails:** Fix before reporting results.
5. **Report results**

## Error Handling

| Situation | Action |
| --- | --- |
| Required skills not loaded | Report failure, do not attempt task |
| Unclear requirements | Make reasonable assumptions, document them |
```

**Why this structure works:**

- **Skill Usage** tells the agent WHERE to look (navigation pointers, not duplicated content)
- **Process step 2** references specific skills for specific decisions
- **Process step 4** inlines the checklist so it can't be skipped

## The `skills` Field (Best Practice)

The `skills` YAML field auto-loads skills when the sub-agent starts. This is especially valuable for Box Factory sub-agents that need design skills.

```yaml
---
name: agent-writer
description: Creates sub-agents. ALWAYS use when creating sub-agents.
tools: Read, Write, Edit, Glob, Grep, Skill, WebFetch
skills: box-factory:sub-agent-design
---
```

**When to use:**

| Pattern            | Choose When                                     | Avoid When                                    |
| ------------------ | ----------------------------------------------- | --------------------------------------------- |
| `skills` field     | Domain is fixed; always needs same skill        | Different skills needed based on context      |
| Skill tool in body | Domain varies; skill depends on runtime context | Same skill always needed (use `skills` field) |
| No skill           | No relevant skill exists                        | A skill exists with guidance Claude needs     |

**Box Factory pattern:** Writer sub-agents should declare their design skill dependency:

- `agent-writer` → `skills: box-factory:sub-agent-design`
- `skill-writer` → `skills: box-factory:skill-design`
- `command-writer` → `skills: box-factory:slash-command-design`

**Note:** Still include `Skill` in your `tools` list - the sub-agent may need to load additional skills during execution.

**Example of conditional skill loading** (Skill tool in body pattern):

```markdown
---
name: component-validator
description: Validates Claude Code components. MUST BE USED when validating plugins or components.
tools: Read, Grep, Glob, Skill, WebFetch
---

# Component Validator

## Process

1. **Identify component type** from file structure
2. **Load relevant design skill:**
   - Plugin → `Skill box-factory:plugin-design`
   - Sub-agent → `Skill box-factory:sub-agent-design`
   - Skill → `Skill box-factory:skill-design`
   - Command → `Skill box-factory:slash-command-design`
3. **Validate** against loaded skill's patterns
```

This sub-agent can't declare a single skill upfront because which skill it needs depends on what component type it discovers at runtime.

## Skill Usage Section Pattern

**When an agent loads skills via the `skills` field, include a Skill Usage section.** This teaches the agent HOW to traverse the loaded skills, not just THAT they're loaded.

**Problem it solves:** Skills auto-load content, but the agent might not know which parts to consult for which decisions. Generic instructions like "use the skill" don't guide navigation.

**Structure:**

```markdown
## Skill Usage

Follow the **Workflow Selection** table in each loaded skill to navigate to the right guidance.

**skill-name** - Consult for:

- [What to look up] (Section Name in skill)
- [Another aspect] (Another Section)
```

**Key principles:**

| Principle                         | Why It Matters                                                      |
| --------------------------------- | ------------------------------------------------------------------- |
| Navigation pointers, not content  | Avoids duplication; skill remains single source of truth            |
| Reference section names           | Stable pointers; section names change rarely                        |
| Specific aspects per skill        | Agent knows which skill answers which question                      |
| **No cross-component file paths** | Skill internals are implementation details from agent's perspective |

**Critical prohibition:** When an agent references a skill it loads, use **indirect references** (section names, concept names) NOT the skill's internal file paths. A skill's internal file structure is an implementation detail from the agent's perspective.

- ✅ `(Quick Start)` - section name in skill
- ✅ `(Tool Selection Philosophy)` - section name in skill
- ✅ `(the skill's guidance on X)` - indirect reference
- ❌ `(gotchas.md)` - skill's internal file (agent shouldn't know this)
- ❌ `(skill-structure.md)` - skill's internal file

**Example (concrete):**

```markdown
## Skill Usage

Follow the **Workflow Selection** table in each loaded skill.

**box-factory-architecture** - Consult for:

- Component paths (where to put files)
- Isolation model (why agents can't ask questions)
- Communication patterns (CAN/CANNOT matrix)

**sub-agent-design** - Consult for:

- YAML frontmatter structure (Quick Start)
- Tool selection (Tool Selection Philosophy)
- Color selection (Color Selection)
```

**When to skip:** If agent loads no skills or loads them conditionally via Skill tool (runtime decision), Skill Usage section is not needed.

## Inlining Quality Checklists

**For critical validation, inline the checklist in the Process section.** Don't just reference a skill's checklist—agents may skip the reference.

**Problem it solves:** "Validate against the skill's checklist" is easy to skip or satisfy superficially. Inlined checklists force explicit verification.

**Pattern:**

```markdown
4. **Validate** - ALL items must pass before completing:

   - [ ] Item one
   - [ ] Item two
   - [ ] Item three

   **If ANY item fails:** Fix before reporting results.
```

**What to inline:**

| Inline                            | Reference (don't inline)                |
| --------------------------------- | --------------------------------------- |
| Validation checklists (blocking)  | Guidance and context (informational)    |
| Required checks before completion | Decision frameworks (for understanding) |
| Items that MUST NOT be skipped    | Examples and patterns (for learning)    |

**Balance:** Inline only the checklist items themselves (1-2 lines each). Keep explanations and rationale in the skill. This maintains single source of truth while ensuring validation happens.

**Example (from sub-agent creation):**

```markdown
7. **Validate** - ALL items must pass before completing:

   - [ ] Fetched official docs (or noted why skipped)
   - [ ] Valid YAML frontmatter with required fields
   - [ ] No forbidden language ("ask the user", "confirm with")
   - [ ] Tools match autonomous responsibilities
   - [ ] Description has specific triggering conditions
   - [ ] Color set with semantic meaning

   **If ANY item fails:** Fix before reporting results.
```

## Official Documentation

**Claude Code changes rapidly and is post-training knowledge.** Fetch these docs when creating sub-agents to ensure current syntax:

- **<https://code.claude.com/docs/en/sub-agents.md>** - Core specification and examples
- **<https://code.claude.com/docs/en/settings#tools-available-to-claude>** - Verify tool names
- **<https://code.claude.com/docs/en/model-config.md>** - Current model options

## Sub-agent-Skill Relationship

**Core principle:** When a sub-agent loads a skill, knowledge lives in the skill; the sub-agent focuses on process.

**Decision logic:**

| Sub-agent has backing skill? | Where knowledge goes            | Sub-agent contains                   |
| ---------------------------- | ------------------------------- | ------------------------------------ |
| Yes, loads a skill           | Skill contains domain knowledge | Process, mechanics, validation steps |
| No backing skill             | Sub-agent contains it           | Both process AND knowledge           |

**Why this matters:**

- Avoids duplication (same knowledge in sub-agent AND skill)
- Single source of truth (update skill, all sub-agents benefit)
- Smaller sub-agent prompts (less context consumed)
- Skills are reusable across multiple sub-agents

**Pattern for skill-backed sub-agents:**

Prefer the `skills` YAML field (see [The `skills` Field](#the-skills-field-best-practice)) to auto-load skills at startup. The sub-agent body then focuses on process, with a **Skill Usage section** providing navigation:

```markdown
## Skill Usage

Follow the **Workflow Selection** table in each loaded skill.

**my-skill** - Consult for:

- [Aspect A] (Section Name)
- [Aspect B] (Section Name)

## Process

1. **Design** by navigating loaded skills:
   - Consult my-skill for [specific decisions]
2. **Execute task**
3. **Validate** - ALL items must pass:
   - [ ] Checklist item from skill
   - [ ] Another item
   **If ANY fails:** Fix before reporting.
```

See [Skill Usage Section Pattern](#skill-usage-section-pattern) and [Inlining Quality Checklists](#inlining-quality-checklists) for detailed guidance.

**Pattern for standalone sub-agents (no skill):**

```markdown
## Process

1. **Understand requirements** [process step]

2. **Apply domain knowledge** [embedded in sub-agent]:
   - Guideline one
   - Guideline two
   - Decision framework here

3. **Execute task** [process step]
```

**Anti-pattern:** Sub-agent loads skill but also embeds same knowledge inline. This causes:

- Maintenance burden (update two places)
- Context waste (duplicate content loaded)
- Potential conflicts (sub-agent and skill disagree)

## Tool Selection Philosophy

**General principle:** Match tools to the sub-agent's job. Reviewers should be read-only; builders need write access.

### Never Include AskUserQuestion

Sub-agents operate in isolation and cannot interact with users. The AskUserQuestion tool will fail silently or cause unexpected behavior. If your sub-agent needs clarification, it must infer from context or make reasonable assumptions.

### Bash is Foundational for Creators

Any sub-agent with creative responsibilities needs Bash, regardless of output type. Even a sub-agent that only produces markdown files needs shell operations:

| Operation             | Why Bash                                                        |
| --------------------- | --------------------------------------------------------------- |
| Directory scaffolding | `mkdir -p` for nested structures (Write doesn't create parents) |
| File organization     | `mv`, `cp` for restructuring                                    |
| Post-write formatting | `mdformat`, linters, formatters                                 |
| Structure inspection  | `ls` to understand existing layout                              |
| Git operations        | `git mv` for tracked renames                                    |

**Rule of thumb:** If a sub-agent creates files, include Bash. The Write tool handles file content; Bash handles the filesystem orchestration around it.

### WebFetch Pairs with Skills for Verification

When a sub-agent loads skills via the `skills` field (especially for specifications or rapidly-changing domains), also include WebFetch:

```yaml
tools: Read, Write, Edit, Glob, Grep, Skill, WebFetch
skills: box-factory:sub-agent-design
```

**Why:** Skills encode knowledge delta (interpretive guidance beyond docs), but the underlying specifications change. Sub-agents should verify current official docs against skill guidance when uncertain.

**Pattern:** The sub-agent's process should include a step like:

> "If uncertain about current spec, fetch official documentation to verify"

This maintains the low-maintenance-first philosophy—skills provide stable interpretive guidance while WebFetch catches spec drift.

## Color Selection

The `color` field sets visual distinction for sub-agents in the status line.

- **Official spec:** Optional
- **Box Factory requirement:** Required for all sub-agents

**Note:** Color support is not documented officially. The following was verified through testing—Claude often guesses wrong colors that don't render.

**Supported colors (7 total):** `red`, `green`, `blue`, `yellow`, `cyan`, `purple`, `orange`

**Not supported:** `magenta`, `white`, `black`, `gray`, `grey`, `*Bright` variants

**Semantic mapping:**

| Color    | Category   | Use For                                               |
| -------- | ---------- | ----------------------------------------------------- |
| `blue`   | Creators   | Sub-agents that create/write files, components, code  |
| `green`  | Quality    | Validators, reviewers, checkers, analyzers            |
| `yellow` | Operations | Git, deployment, CI/CD, system tasks                  |
| `purple` | Meta       | Sub-agents that create other sub-agents               |
| `cyan`   | Research   | Exploration, documentation, research sub-agents       |
| `red`    | Safety     | Security checks, destructive operations, warnings     |
| `orange` | Other      | Sub-agents that don't fit other categories (reserved) |

**Example:**

```yaml
---
name: code-reviewer
color: green
---
```

**Guidelines:**

- Match color to primary function, not secondary features
- Be consistent within a plugin (all quality sub-agents green)
- Reserve `orange` for sub-agents that don't fit established categories

## Description Field Design

The `description` field determines when Main Claude delegates to your sub-agent. This is critical for autonomous invocation.

**Official requirement:** "Natural language explanation of when to invoke the subagent"

**Quality test:** Would Main Claude invoke this sub-agent based on context alone, or only when explicitly asked?

**Guidelines:**

- State WHEN to use (triggering conditions), not just WHAT it does
- Be specific about context and use cases
- Test empirically - if your sub-agent isn't being invoked automatically, revise the description
- Avoid overly generic descriptions that match too many scenarios

## Quality Checklist

Before finalizing a sub-agent:

1. **Fetch official docs** - Verify against current specification
2. **Check structure** - Valid YAML frontmatter, required fields present
3. **Scan for forbidden language** - No user interaction phrases
4. **Validate tools** - Match autonomous responsibilities, no AskUserQuestion
5. **Test description** - Specific triggering conditions, not generic
6. **Review system prompt** - Single H1, clear structure, actionable instructions
7. **Verify no hardcoding** - No version-specific details that will become outdated
8. **Set color** - Choose semantic color matching sub-agent's primary function (creator=blue, quality=green, ops=yellow, meta=purple, research=cyan, safety=red, other=orange)
9. **If agent loads skills via `skills` field:**
   - Skill Usage section present with navigation pointers
   - Navigation pointers use indirect references (section names), NOT skill's internal file paths
   - Process steps reference specific skill sections
   - Quality checklist inlined in validation step (not just referenced)
