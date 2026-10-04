---
name: plan
description: "Create a detailed implementation plan for a feature or task. Explores codebase first, then produces phased steps."
argument-hint: "[feature-description]"
allowed-tools: Read Grep Glob Bash
model: gpt-5.4
---

# /plan — Implementation Planning

Create a comprehensive plan for: **$ARGUMENTS**

1. **Explore** — `agents/code-explorer.md` approach: existing patterns, related files, dependencies
2. **Architect** — `agents/architect.md` thinking: trade-offs, patterns, scalability
3. **Plan** — `agents/planner.md` format: phases (MVP → Core → Edge Cases → Optimization), each step with file path, action, why, dependencies, risk level, testing strategy, success criteria
