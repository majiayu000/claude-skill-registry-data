---
name: my-skill
description: "One-sentence description shown in the Claude Code slash command picker."
pass-full-context: true
pass-conversation-history: true
agent: my-orchestrator-agent
argument-hint: "[argument]"
---

# /my-skill

One-sentence description of what this slash command does.

Invoke the agent with: $ARGUMENTS

## Usage

- `/my-skill DEF0123456` — describe what happens with a specific argument
- `/my-skill` — describe what happens with no argument (e.g. will prompt for input)

## Notes

- This skill is a thin entry point. All logic lives in the `my-orchestrator-agent` agent.
- The `$ARGUMENTS` placeholder forwards everything the user types after `/my-skill` directly to the agent.
- Keep this file short — if you find yourself adding logic here, move it to the agent instead.
