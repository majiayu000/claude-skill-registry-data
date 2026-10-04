---
name: thrunt-resume-work
description: Resume project or hunt work from the previous session with full context restoration
allowed-tools: Read, Bash, Write, AskUserQuestion, SlashCommand
---


<objective>
Restore complete hunt context and resume the active workflow seamlessly from the previous session.

Routes to the resume-program workflow which handles:

- STATE.md loading (or reconstruction if missing)
- Checkpoint detection (.continue-here files)
- Incomplete work detection (PLAN without SUMMARY)
- Active planning doc detection (`MISSION.md`, `HUNTMAP.md`)
- Status presentation
- Context-aware next action routing into `/hunt:*` or `/thrunt:*`
  </objective>

<execution_context>
@.github/thrunt-god/workflows/resume-program.md
</execution_context>

<process>
**Follow the resume-program workflow** from `@.github/thrunt-god/workflows/resume-program.md`.

The workflow handles all resumption logic including:

1. Hunt existence check
2. STATE.md loading or reconstruction
3. Detection of the active mission and huntmap
4. Checkpoint and incomplete work detection
5. Visual status presentation
6. Context-aware option offering
7. Routing to the appropriate next command
8. Session continuity updates
   </process>
