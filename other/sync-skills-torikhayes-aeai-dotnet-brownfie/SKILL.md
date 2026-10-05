---
name: "sync-skills"
description: "Audit and sync skill/prompt parity between Claude and GitHub Copilot. Creates bridging files so neither toolset is left behind. Trigger phrases: sync skills, skill parity, missing prompt, copilot claude sync, check skill coverage."
argument-hint: "Optional: 'report' to only report gaps, 'copilot-only' to create only Copilot prompts, 'claude-only' to create only Claude skills."
user-invocable: true
---

Read the shared agent definition at `.github/agents/sync-skills.agent.md` for full instructions, then execute the workflow from Step 1.

`.github/agents/sync-skills.agent.md` is the single source of truth for the sync logic and is shared with GitHub Copilot. Do not duplicate its content here.

## What This Skill Does

1. Lists all Claude skills (`.claude/skills/`), Copilot agents (`.github/agents/`), and Copilot prompts (`.github/prompts/`)
2. Identifies capabilities present in one tool but absent from the other
3. Creates **bridging files** — thin wrappers that delegate to the canonical definition — so both tools can invoke every capability
4. Flags near-matches (same concept, different name) for human review without auto-bridging them
5. Reports the full parity table

## User Input

```text
$ARGUMENTS
```
