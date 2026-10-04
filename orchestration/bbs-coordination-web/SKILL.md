---
name: bbs-coordination-web
description: >
  Shared Bulletin Board System (BBS) coordination protocol for web-research
  swarm subagents. Covers posting and reading from BBS, channel descriptions,
  structured data requirements, and idle review behavior.
  Load this skill before using the post_to_bbs tool.
---

# BBS Coordination Skill (Web Research)

## Bulletin Board System (BBS)

You communicate with the orchestrator and other subagents through a
shared Bulletin Board System (BBS).

### Tools

- **post_to_bbs**: Post discoveries, results, or discussion to the BBS.
  Always include `structured_data` for machine-readable payloads.
- **read_bbs**: Read recent posts from the BBS, optionally filtered by
  channel or tags.

### BBS Channels

- `discoveries`: Web findings, key data points, source URLs, extracted facts.
- `key-findings`: Critical information, candidate answers, important facts.
- `consensus`: Resolved decisions — post here when you agree or disagree
  with another agent's findings.
- `discussion`: Challenge or build on findings from other agents.

### Posting Guidelines

- Always post findings to the BBS so other agents can see them.
- Read the BBS before starting work to see what others have already found.
- Be specific in posts — include data, evidence, and source URLs.

## When Idle

When there are no tasks to claim, you will see BBS updates from other
agents. Review them critically:

- If you spot a potential issue with a specific agent's work, use **#discussion**.
- If you realize your own completed task's findings were wrong,
  call `update_task_summary` to record the correction directly.
- Keep verification lightweight (1-2 quick checks max).
- Do NOT duplicate work or repeat others' exact analysis.
- If everything looks correct, just say "Nothing to flag."
