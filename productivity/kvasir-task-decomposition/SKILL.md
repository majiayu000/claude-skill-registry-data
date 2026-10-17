---
name: kvasir-task-decomposition
description: Break complex objectives into well-scoped subtasks with explicit dependencies and execution order.
---

# Task Decomposition

## Purpose

Transform complex objectives into well-defined, independently executable subtasks with clear dependencies, inputs, and outputs. Ensure each subtask maps to exactly one owner with one well-defined output.

## When to Use

- When a task spans multiple workstreams or requires multi-step execution.
- When dependencies between subtasks are non-trivial.
- When the execution order matters and blocking relationships exist.
- When a task is large enough that decomposition reduces risk and improves clarity.

## Workflow

1. **Analyze the objective.**
   - Clarify the end goal and what a successful outcome looks like.
   - Identify constraints such as time, tooling, and architecture.
   - Note which capabilities the requesting agent has made available.

2. **Identify atomic subtasks.**
    - Break the objective into the smallest meaningful units of work.
    - Ensure each unit produces a single, well-defined output.
    - Confirm no subtask bundles unrelated concerns together.

3. **Map dependencies.**
   - Determine which subtasks depend on the outputs of others.
   - Distinguish hard blocking relationships from soft ordering preferences.
   - Identify work that can proceed in parallel.

4. **Assign ownership.**
   - Match each subtask to the required capability based on task type.
   - Verify the required capabilities are available.
   - Ensure every subtask has exactly one responsible owner.

5. **Define execution order.**
   - Sequence subtasks so dependencies are satisfied before dependents run.
   - Group parallelizable subtasks to shorten the critical path.
   - Highlight blocking points where downstream work must wait.

6. **Document the plan.**
   - Assign each subtask a stable ID and a clear description.
   - Record ownership assignments, dependencies, and expected outputs.
   - Present the decomposition so it can be executed without ambiguity.

## Quality Criteria

- Every subtask has a single output and a single responsible owner.
- All dependencies are explicitly stated, not implied.
- Parallelizable subtasks are identified.
- The plan covers the full objective with no gaps.
- Each subtask is small enough to be unambiguous.

## Anti-Patterns

- **Mixed outputs**: A subtask that bundles research and implementation into one unit.
- **Implicit dependencies**: Assuming a subtask can start without checking its inputs are ready.
- **Over-decomposition**: Splitting work so finely that coordination overhead exceeds the work itself.
- **Missing ownership**: A subtask without a clear owner or required capability.
