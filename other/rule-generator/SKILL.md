---
name: rule-generator
description: "Creates new Antigravity rules when a behavioral pattern, user preference, or project convention needs to be enforced permanently. Triggers when the evolution observer detects a preference, or when the user explicitly asks for a new rule."
---

# Rule Generator (Meta-Skill)

## Goal

Create properly formatted Antigravity rules that are clear, actionable, and do not conflict with existing rules.

## Instructions

### Step 1: Define the Rule

Before creating the file, clarify:
- **What behavior to enforce**: What should the agent always do (or never do)?
- **Why it matters**: What goes wrong if this rule is not followed?
- **Source**: Where did this rule come from? (user preference, error prevention, project convention)

### Step 2: Check for Conflicts

Read all existing rules in `.agent/rules/`:
- Does any existing rule contradict this new one?
- Does any existing rule already cover this? (in which case, update it instead of creating a new one)
- If there is a conflict, present both rules to the orchestrator and ask which takes priority

### Step 3: Write the Rule File

Create a new file in `.agent/rules/` with the naming convention:
- Core rules (00-06): NEVER modify these
- Project-specific rules: start numbering from `10-` onwards (e.g., `10-python-style.md`, `11-api-conventions.md`)
- This leaves room for future core rules (07-09)

Use the template in `resources/rule-template.md`.

### Step 4: Log and Inform

- Append to `.agent/knowledge/evolution-log.md`
- Tell the orchestrator:
  - What the new rule does (plain English)
  - Why it was created
  - That it is now active in all future interactions
  - Where to find it (`.agent/rules/<filename>`)

## Constraints

- NEVER modify rules 00 through 06 — these are the Ground Zero core
- NEVER create rules that weaken safety (e.g., "skip quality checks," "ignore errors")
- ALWAYS get orchestrator approval before creating a rule
- Rules must be phrased as clear imperatives ("Always do X," "Never do Y," "When X happens, do Y")
- Avoid vague rules ("Try to be clean" — what does "clean" mean? Be specific.)
