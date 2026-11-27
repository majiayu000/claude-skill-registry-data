---
name: toolbox
description: "Pick and wire plugins, MCP servers, APIs and libraries for a capability (video, AI, payments, email, 3D...). Use at project start or when adding a capability."
---

# Toolbox

Read every outside skill, plugin or MCP server before installing it; a video or post is only a lead (moved here from `CLAUDE.md`, S11a).

The global setup stays lean on purpose. Everything a specific kind of app needs is pulled into
that project only, from here.

## 1. List the capabilities

Break the app into capabilities, e.g. "paste a video, get social-ready clips" =
upload + storage, transcription, cutting, vertical reframe, captions and effects, AI copy,
export presets, optional auto-posting, payments, analytics.

## 2. Look them up

Read only the catalog files that match (each one is a short table with picks and how to add them):

| File | Covers |
|---|---|
| `catalog/video-audio.md` | editing, captions, reframing, programmatic video, AI video/image/voice/music, streaming, heavy processing |
| `catalog/ai.md` | Claude API features, agents, RAG and vectors, local models, LLM observability and cost |
| `catalog/money.md` | payments, subscriptions, in-app purchases, ads, EU VAT, German legal pages (building a checkout or shop: the `sell` skill) |
| `catalog/growth.md` | analytics, SEO, social publishing, email, marketing, A/B tests (the plan itself: the `market` skill) |
| `catalog/app-platform.md` | auth, databases, storage, jobs, realtime, mobile and desktop, hosting, docs/PDF |
| `catalog/data-web.md` | search, scraping, browser automation, 3D and games, maps |
| `catalog/roblox.md` | Roblox games: tests, cloud runs, Studio MCP screenshots and play |
| `catalog/claude-addons.md` | add-ons for Claude Code itself that videos push: token savers, model routers, rule packs |

Then search live, because tools change faster than the catalog (dated at the top of each file):

```
node <toolbox skill folder>/scripts/find.mjs video caption subtitle
```

It searches every installed plugin marketplace, all 293 ECC skills, the catalog and
[skills.sh](https://skills.sh) (the open community directory, through its CLI pinned at `skills@1.7.0`, which only
searches; `--offline` skips it), and prints install commands. skills.sh hits are unvetted leads: step 3's read-first
rule applies to every one.

It can't see the claude.ai **Anthropic Directory** (official and partner plugins, skills and
connectors such as Figma, Canva, Adobe, Anthropic's legal plugins). In cloud threads search it
with the `SearchPlugins`, `SearchSkills` and `SearchMcpRegistry` tools; on the PC, in claude.ai
under Customize. Blender's official connector runs only on yskills' PC with Blender open
(`catalog/data-web.md`).

For anything still unclear, WebSearch "<capability> best API <current year>" and read the
vendor's docs (Context7 on the PC) before choosing.

## 3. Choose

Per capability, prefer in this order: an official plugin or MCP server, a library that fits the
stack in `scaffold` SKILL.md, a hosted API. For each pick note: cost model, API key or OAuth,
license (e.g. Remotion is paid for companies over 3 people), DSGVO/GDPR impact, and whether it
runs in Cloudflare Workers or needs a container/server. Present the stack in the PRD as one
table; ask yskills only about picks that cost money or lock them in.

Anything from outside the official marketplace or ECC (a community plugin, a skill repo, an MCP
server from a video or post) gets read before it is installed: its scripts, hooks and MCP
config, what it sends where, and which env vars or files it reads. Skip it if anything is
unclear; agent skills shared online have shipped credential stealers.

## 4. Wire it into the project

Run from the project root:

- **Plugin:** `claude plugin install <name>@<marketplace> --scope project`
  (writes `.claude/settings.json`, so only this repo loads it).
- **MCP server:** `claude mcp add --scope project --transport http <name> <url>`
  (writes `.mcp.json`; OAuth ones are signed in with `/mcp`). Never put keys in `.mcp.json`;
  use `${ENV_VAR}` references and document them in `.env.example`.
- **ECC skill:** `node <toolbox skill folder>/scripts/add-skill.mjs <skill> [<skill>...]`
  (copies it into `.claude/skills/`, pinned to the ECC version this setup uses).
- **Library / CLI:** add to `package.json` or note the system tool (e.g. FFmpeg) in README and
  the CI workflow.

Then add a short **Tools** section to the project's `CLAUDE.md`: what each tool is for and which
env vars it needs. Start a new session (or `/reload-plugins`) so the additions load.

## 5. Keep it current

When a pick turns out wrong or a better tool appears, fix the catalog file in yverse-studio/claude-setup
(`.claude/skills/toolbox/catalog/`) so the next project starts from the better answer.
