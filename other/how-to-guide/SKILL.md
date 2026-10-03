---
name: how-to-guide
description: Write a task-oriented how-to guide for an already oriented user, focusing on prerequisites, direct steps, variants, verification, and recovery without turning the page into a tutorial or conceptual essay.
---
# How-To Guide

Use when users know the product but need reliable instructions for one specific task.

## Procedure
1. Define the task, intended user, supported versions or environments, prerequisites, and what successful completion looks like.
2. Verify the task on the current supported implementation before documenting it.
3. Put prerequisites and important consequences before the first mutating action.
4. Give the shortest complete sequence using exact UI labels, commands, arguments, or paths where needed.
5. Add alternatives only when they represent common supported variants, and clearly separate them from the main path.
6. Include verification steps that prove the task succeeded rather than assuming command exit or a saved setting is enough.
7. Put likely error recovery and rollback close to the relevant operation, especially for configuration or destructive tasks.
8. Link to concepts, reference, or troubleshooting material instead of duplicating them extensively.

## Decision rules
- A how-to solves one task; it does not need to teach the entire system.
- Do not omit prerequisites because an experienced author finds them obvious.
- Verify exact commands and product labels.
- Alternatives should not obscure the default supported path.

## Quality gate
The guide is ready when a qualified user can complete the task from a known starting state, exact actions are current and reproducible, success can be verified, common recovery is available, and unrelated conceptual material does not bury the procedure.