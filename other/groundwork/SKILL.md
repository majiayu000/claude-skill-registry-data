---
name: groundwork
description: >-
  Sets up or audits a project for AI work: CLAUDE.md contract, docs layout, agents. Use when starting a new project, there is no CLAUDE.md, or the user asks to set up or audit the repo. Writes only after your ok.
license: Apache-2.0
metadata:
  level: "setup"
  uses: ""
  agents: ""
  tokens: "865"
---

Sets up or audits the project layout and the CLAUDE.md contract the other foma-skills read. Explore, present, confirm, write.

Hand-offs (by message, never called): rule content (stale, duplicate, contradicting rules) to `/foma-skills:learning`; junk files, stray `*.md`, unarchived plans to `/foma-skills:tidying`.

## Steps
1. Explore, read-only. Read with Read (HTML comments are invisible in context): root and nested `CLAUDE.md`, `AGENTS.md`, `.claude/` (settings, rules, agents, skills), `.gitignore`, `docs/`, manifests. Mode: no CLAUDE.md and no AGENTS.md, or an empty repo, is setup; otherwise audit. `$ARGUMENTS` is only a hint of the mode.
2. Safety first, both modes: list hooks, `env` (esp. `ANTHROPIC_BASE_URL`), `enableAllProjectMcpServers` and `.mcp.json` servers from `.claude/settings*.json`, and tell the user before anything else. Change none of them.
3. Setup: if the repo is empty, ask what the project is for first. Ask the choices in rounds of 4 or fewer, recommended answer first.
4. Branch per mode (below).
5. Present findings and the exact proposed diffs, grouped (contract, docs skeleton, agents, `.gitignore`, optional lines). Write a group only after the user's ok on that group.
6. Write. Own content goes in one block, `<!-- foma-skills:start -->` ... `<!-- foma-skills:end -->`. On rerun, Read the file and replace the text between the markers; never append a second block. If the markers are missing but the headings exist, edit those sections in place.
7. Agents: copy each of `${CLAUDE_SKILL_DIR}/assets/agents/{implementer,reviewer,explorer}.md` to `.claude/agents/` only if the user chose them. If the target file exists, skip it and say so. Say that a newly created `.claude/agents/` needs a Claude Code restart.
8. Re-Read every written file; check that referenced paths exist and the markers appear once.

## Rules
- Never overwrite CLAUDE.md or AGENTS.md wholesale; edit sections in place, keep the user's wording.
- If AGENTS.md exists, it stays the source: CLAUDE.md imports it with `@AGENTS.md` and holds Claude-only lines. Do not create CLAUDE.local.md next to it.
- Root CLAUDE.md holds only what the agent cannot infer: no trees, dependency lists, overviews, README duplicates. Over 200 lines is a finding.
- The contract keys are fixed (`## Commands`, `## Where things live`: Docs, Decisions, Specs, Plans, Design, Rules, Scratch, Trash). Fill only keys that exist in the project; consumers fall back to defaults for missing ones.
- No secrets under `.claude/`; no symlinks for instruction files.
- Hooks, settings, `.gitignore` and agent files are side effects: each needs its own ok.
- The one-line rules block is offered only as an opt-in or on request, never by default: strong models follow these rules without it, weaker ones (Haiku) benefit.
- Session-start cost: estimate tokens of root CLAUDE.md, unscoped rules, MEMORY.md, MCP servers and plugins (chars / 4) and name what to disable or move to a lazy layer.

## Branches
If the mode is setup, read `references/setup.md`.
If the mode is audit, read `references/audit.md`.
If the user asks for the one-line rules block or accepts it as a choice, read `references/lines.md`.

## Report
- Mode, findings count (safety / contract / structure / cost), files written, agents skipped.
- Not checked: <what was not read or run>

Next: `/foma-skills:learning` for rule content, `/foma-skills:tidying` for junk; restart Claude Code if `.claude/agents/` is new.
