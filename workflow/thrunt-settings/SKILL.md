---
name: thrunt-settings
description: Configure THRUNT workflow toggles and model profile
allowed-tools: Read, Write, Bash, AskUserQuestion
---


<objective>
Interactive configuration of THRUNT workflow agents and model profile via multi-question prompt.

Routes to the settings workflow which handles:
- Config existence ensuring
- Current settings reading and parsing
- Interactive settings prompt (model profile, research, plan checker, findings validator, branching, and workflow toggles)
- Config merging and writing
- Confirmation display with quick command references
</objective>

<execution_context>
@.github/thrunt-god/workflows/settings.md
</execution_context>

<process>
**Follow the settings workflow** from `@.github/thrunt-god/workflows/settings.md`.

The workflow handles all logic including:
1. Config file creation with defaults if missing
2. Current config reading
3. Interactive settings presentation with pre-selection
4. Answer parsing and config merging
5. File writing
6. Confirmation display
</process>
