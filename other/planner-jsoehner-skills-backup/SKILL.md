---
name: planner
description: A built-in agent for decomposing high-level objectives into actionable steps, milestones, and execution plans.
---

# Planner

## When to Use
Use the planner agent for tasks requiring its specific core functionality. This is a built-in pi agent.

## Procedure
1. Call the planner agent directly or via a chain/parallel task.
2. Provide the necessary requirements or context.
3. The planner will perform its specialized role (e.g., planning, research, review, or orchestration).

## Pitfalls
- Ensure you provide clear instructions; built-in agents are powerful but require well-defined goals.
- For multi-step tasks, consider using a chain to pass information between different agents.

## Verification
- The planner agent returns the expected output in the requested format.
- The logic follows the expected behavior for its specific role.
