---
name: cross-agent-skill-publishing
description: "Publish SKILL.md for any agent: skills.sh, CLI-first."
---

# Cross-Agent Skill Publishing

Making a project's capability consumable by ANY AI agent (Claude Code, Cursor,
Codex, Gemini, Hermes, …). Session 2026-08-02, BootKeeper — the user's chosen
standard is skills.sh (Vercel).

## The core problem

Skill formats are NOT cross-agent: Claude SKILL.md, Hermes skill, OpenCode differ
in packaging. But **every agent can run a CLI**. Therefore:

> **A CLI is the truly agent-agnostic base; SKILL.md is just the instruction
> sheet over it.**

MCP can be added later as another thin adapter over the SAME CLI — never bake
the AI interface into the core. This is the pattern the user endorsed for
BootKeeper: stable `bootkeeper` CLI + root SKILL.md; MCP deferred as an adapter.

## skills.sh (Vercel) — the standard

- `vercel-labs/skills` (~28k stars). Format = standard SKILL.md, no special header.
- Install on any supporting agent: `npx skills add <owner>/<repo>`
- Supports 19+ agents incl. **nous-research (Hermes)**, Claude Code, Cursor,
  Codex, GitHub Copilot, Windsurf, Gemini, Cline.
- Badge for README: `[![skills.sh](https://skills.sh/b/owner/repo)](https://skills.sh/owner/repo)`
- Hermes page: `https://skills.sh/agent/nous-research`

## Placement & structure that works

- SKILL.md at **repo root** — that's what `npx skills add` picks up.
- Self-contained: the agent has zero other context. Include:
  - When to use (trigger)
  - Every command with examples
  - Output format (JSON field names)
  - Platform notes (e.g. "must run on Windows, else returns []")
  - Agent rules (never fabricate; risk is authoritative; writes not yet available)

## Worked example (BootKeeper)

`publieople/BootKeeper`: root SKILL.md documents `bootkeeper list/get/analyze/
snapshot` (JSON out). CLI builds cross-platform; SKILL.md documents JSON shapes
an agent parses directly.

## Pitfalls

- **Don't skip the CLI.** A doc-only SKILL.md gives the agent nothing to run —
  it would write its own fragile reimplementation each time.
- **Don't bake MCP into core.** MCP is an adapter; the CLI is the contract.
- **Verify install format**: if `npx skills add` fails frontmatter validation,
  fall back to git clone (see hermes-external-skill-install skill).
