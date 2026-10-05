---
name: ut-chain
description: Compose and execute a chain of UltraThink skills for a task
disable-model-invocation: true
allowed-tools: Read, Bash, Grep, Glob, Edit, Write
argument-hint: "skill1 + skill2 + skill3 — task description"
---

# UltraThink Skill Chain

Compose multiple skills into a sequential pipeline. Each skill's output feeds into the next.

## Usage

```
/ut-chain plan + scout + react + test — Build a settings page
/ut-chain debug + fix + test — Fix the auth bug
/ut-chain research + api-designer + nextjs — Design the API
```

## How to parse $ARGUMENTS

Split on `—` (em dash) or `--`:
- **Left side**: skill names separated by `+`
- **Right side**: the task description

## Execution

For each skill in the chain:

1. Read `~/.claude/skills/<skill-name>/SKILL.md`
2. Extract the key patterns, best practices, and pitfalls
3. Apply them to the task in sequence
4. After each skill completes its phase, summarize what was done before moving to the next

## Example chain: `plan + react + test`

**Step 1 — Plan**: Read the `plan` skill. Create a phased implementation plan for the task. Present the plan for user approval before continuing.

**Step 2 — React**: Read the `react` skill. Implement the solution following React patterns, hooks best practices, and performance guidelines from the skill.

**Step 3 — Test**: Read the `test` skill. Generate tests following the testing patterns, verify the implementation works.

## Validation

Before executing, verify each skill exists:

```bash
for skill in $(echo "SKILLS_LIST" | tr '+' '\n' | tr -d ' '); do
  if [ ! -f "$HOME/.claude/skills/$skill/SKILL.md" ]; then
    echo "Skill not found: $skill"
    echo "Available skills: /ut-skills"
    exit 1
  fi
done
```

Show the execution plan (which skills in what order) and ask for confirmation before starting.

## Chain Templates

If no arguments, show common chain templates:

```
Common chains:
  /ut-chain plan + scout + code-review     — Research & plan
  /ut-chain debug + fix + test             — Debug workflow
  /ut-chain plan + react + tailwindcss     — Frontend feature
  /ut-chain plan + nextjs + postgresql     — Full-stack feature
  /ut-chain scout + refactor + test        — Refactor safely
  /ut-chain api-designer + nodejs + test   — API development
  /ut-chain security-scanner + owasp + fix — Security audit
```
