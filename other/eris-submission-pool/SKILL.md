---
name: eris-submission-pool
description: Finish a verified build-ready Shipd Eris dataset/challenge pair in Claude Code through rebuild, zero-warning checks, Mark as Ready, challenge preparation, and the requested stopping point.
---

# Eris Submission Pool for Claude Code

Read `${CLAUDE_PROJECT_DIR}/.codex/skills/eris-submission-pool/SKILL.md`
completely, including its selected workflow reference and state template. Also
read `../eris-challenge-automation/references/claude-runtime.md`.

Use the project Playwright MCP browser for authenticated Shipd work. Verify the
exact linked dataset and challenge IDs before the first write. All local package
and admission gates still apply; this adapter never invents missing artifacts in
the browser.

Resolve every yellow and red result genuinely. Default to stopping with all
checks green and Run Agents visibly available. Launch only when the current
request explicitly says `through Run Agents`, then verify the launch and stop.
