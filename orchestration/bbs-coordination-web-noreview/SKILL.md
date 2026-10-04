---
name: bbs-coordination-web-noreview
description: >
  Ablation variant of bbs-coordination-web with the idle peer-review protocol
  ("When Idle") removed (GATE 2 OFF — no board review). Posting and reading of
  findings is retained. Used by the R1 and R0 arms of the review-gate ablation;
  do not use for production runs. Load this skill before using the post_to_bbs
  tool.
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
