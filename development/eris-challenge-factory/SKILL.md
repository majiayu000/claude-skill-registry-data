---
name: eris-challenge-factory
description: Scout, pilot, build, revise, and audit Project Eris benchmark challenges in Claude Code using the bot's canonical factory policy and local evidence gates.
---

# Eris Challenge Factory for Claude Code

Read `${CLAUDE_PROJECT_DIR}/.codex/skills/eris-challenge-factory/SKILL.md`
completely and follow every selected reference, script, gate, and evidence
requirement from that bundled skill.

This adapter changes only runtime nouns:

- a dedicated Codex task becomes a Claude project subagent or current session;
- Codex browser work becomes the project Playwright MCP browser;
- every durable result remains under `Working/`, `Workspace/output/`, the
  registry, and the controller ledger.

Do not promote Pilot, Hold, or Reject to Proceed because a browser draft exists
or the user wants a fixed count. Search for a replacement candidate in the same
slot while preserving all source, license, truth, scale, novelty, leakage,
shortcut, metric, stability, and runtime gates.
