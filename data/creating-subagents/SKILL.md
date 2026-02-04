---
name: creating-subagents
description:
  Use when need to create specialized subagent for recurring tasks,
  domain-specific work, or pipeline automation
---

# Creating Subagents

Subagents are specialized AI instances with focused expertise, isolated context,
and scoped tool access.

## When to Create

- Task repeats across projects (code review, security audit)
- Domain expertise needed (data science, API design)
- Pipeline step requires isolation (PM → Architect → Implementer)
- Tool access must be restricted

Skip if: one-off task, no specialization needed.

## Quick Reference

| Field             | Required | Purpose                                |
| ----------------- | -------- | -------------------------------------- |
| `name`            | Yes      | Lowercase, hyphens only                |
| `description`     | Yes      | When to delegate (triggers)            |
| `tools`           | No       | Allowlist; omit = inherit all          |
| `disallowedTools` | No       | Denylist; removed from inherited       |
| `permissionMode`  | No       | `default`, `acceptEdits`, `plan`, etc. |
| `skills`          | No       | Preload skill content into context     |
| `hooks`           | No       | Lifecycle hooks (`PreToolUse`, `Stop`) |
| `color`           | No       | Background color for UI identification |

## Design Process

### 1. Define the Problem

Before writing code, answer:

- What task does this agent solve?
- What does success look like?
- What tools are absolutely required?
- What should the agent NOT do?

### 2. Write Description First

Description determines when agent is invoked. Write it before the prompt.

**Pattern:** `[Role]. [Trigger condition]. Use proactively [when].`

```yaml
# ❌ BAD: Vague, no trigger
description: Helps with code

# ❌ BAD: Describes process, not trigger
description: Reviews code and provides feedback

# ✅ GOOD: Clear role + trigger + proactive hint
description: Code quality reviewer. Use proactively after code changes.
```

### 3. Minimal Viable Prompt

Start with the smallest prompt that works:

```markdown
---
name: code-reviewer
description: Code quality reviewer. Use proactively after code changes.
tools: Read, Glob, Grep, Bash
color: blue
---

You are a code reviewer. When invoked:

1. Run git diff to see changes
2. Review modified files
3. Report: Critical → Warnings → Suggestions

Include fix examples.
```

### 4. Test Before Deploy

Run the agent on real tasks. Document:

- Did it activate when expected?
- Did it have the right tools?
- Was output useful and structured?
- Did it stay in scope?

### 5. Iterate Based on Failures

When agent fails, identify the gap:

| Symptom             | Fix                            |
| ------------------- | ------------------------------ |
| Doesn't activate    | Improve description triggers   |
| Wrong scope         | Add constraints to prompt      |
| Missing context     | Add required tools or skills   |
| Unstructured output | Define output format in prompt |
| Does too much       | Split into focused agents      |

## Tool Access by Role

| Role              | Tools                                 |
| ----------------- | ------------------------------------- |
| Read-only         | Read, Grep, Glob                      |
| Research          | Read, Grep, Glob, WebFetch, WebSearch |
| Code modification | Read, Write, Edit, Bash, Glob, Grep   |
| Full access       | (omit field — inherits all)           |

## Common Mistakes

| Mistake                     | Fix                                     |
| --------------------------- | --------------------------------------- |
| Vague description           | Specific triggers: "after code changes" |
| Tool inheritance by default | Explicit `tools` field for security     |
| No structured output        | Define format in prompt                 |
| Monolithic mega-agent       | Split into single-purpose agents        |
| Missing "Use proactively"   | Add to description for auto-delegation  |
| Prompt before description   | Write description first — it's the API  |

## Creation Checklist

- [ ] Problem clearly defined (what, success criteria, non-goals)
- [ ] Description written first with trigger conditions
- [ ] Tools explicitly listed (not inherited)
- [ ] Prompt is minimal and focused
- [ ] Output format defined
- [ ] Tested on real task
- [ ] Iterated based on failures

## Pipeline Pattern

Chain agents for multi-stage workflows:

```
pm-spec → architect-review → implementer-tester
```

Each agent:

- Has single responsibility
- Updates status on completion
- Hooks trigger next stage
