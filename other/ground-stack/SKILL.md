---
name: ground-stack
description: Ground the right stack philosophy for the current technology context.
---

# Skill: Ground Stack

> "Right philosophy for the right technology."

## Execute

```pseudo
available_skills
    | where name ~ "*:ground-*"
    | where name !~ "kernel:ground-*"
    | where skill's technology context matches current task
    | parallel Skill

-> "Stack grounded: [names]." or "No stack context."
```

Multiple stacks can ground simultaneously (e.g., Pest tests for Laravel).
Skip stacks already grounded this session.
⛔ Do NOT ground all stacks blindly. Match to the task.
