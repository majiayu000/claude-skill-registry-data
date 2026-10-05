---
name: example-skill
description: Example skill demonstrating the skill system
version: 1.0.0
author: PonyBunny Team
tags: [example, demo]
phases: [execution, verification]
requiresApproval: false
userInvocable: true
disableModelInvocation: false
---

# Example Skill

This is an example skill that demonstrates the PonyBunny skill system.

## Purpose

This skill shows how to:
- Structure a skill with frontmatter metadata
- Define which phases can use this skill
- Make skills user-invocable
- Include skills in model prompts

## Usage

When the agent is in the **execution** or **verification** phase, this skill becomes available.

### Steps

1. **Identify the task**: Check if this skill applies to the current work item
2. **Read this file**: The agent should use the `read` tool to load this SKILL.md
3. **Follow instructions**: Execute the steps defined below

### Example Task Flow

```bash
# Step 1: Analyze the requirement
echo "Analyzing task requirements..."

# Step 2: Execute the work
npm test

# Step 3: Verify results
echo "Verification complete"
```

## Constraints

- Only use this skill when explicitly needed
- Always verify results before marking complete
- Escalate if requirements are unclear

## Success Criteria

- [ ] Task requirements understood
- [ ] Work executed successfully
- [ ] Results verified
- [ ] Documentation updated
