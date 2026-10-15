---
name: mcp-mastery
description: "MCP server catalog, advisor, and task router. Use when the user asks 'which MCP do I need for X', 'set up MCP for [service]', 'install MCP server', 'what MCP servers exist', or describes a task needing external system access (databases, GitHub, Slack, browsers, cloud, payments). Maps workflow needs to the right server from a curated 30-server catalog. Pairs with `mcp-builder` (for creating new servers) and GAPS.md (gap analysis vs. current stack)."
---

# MCP Mastery — Server Catalog, Advisor, Task Router

## The mental model

**Skills** teach Claude HOW to think — workflows, patterns, playbooks.
**MCP servers** give Claude WHERE things live — real connections to systems and data.

You need both. Skills without MCP = brilliant employee with no tools. MCP without skills = employee with every key but no playbook.

MCP = Model Context Protocol. An open standard that lets Claude connect to external tools, databases, APIs, SaaS platforms, files, browsers, and cloud infra through a universal plug-and-play interface. Without it, the human is the middleware: copy-paste in, copy-paste out. With it, Claude reads the DB directly, opens the PR, sends the Slack message — the human describes intent.

## Where to find servers (search these first, don't build from scratch)

| Source | URL | When to use |
|--------|-----|-------------|
| Reference implementations | github.com/modelcontextprotocol/servers | Start here. Filesystem, git, memory, fetch, sequential-thinking — official + free. |
| Official registry | registry.modelcontextprotocol.io | 500+ indexed servers. The "app store". Anthropic + GitHub + Microsoft + PulseMCP-backed. |
| Awesome list | github.com/wong2/awesome-mcp-servers | Community catalog, organized by category, fastest to skim. |
| Sandbox runner | mcp.run | Try a server without local install. |

## Install a server (Claude Code, user scope)

```bash
# Stdio server via npx
claude mcp add --scope user <name> -- npx -y <package>@latest

# Stdio with env vars
claude mcp add --scope user -e API_KEY=xxx <name> -- npx -y <package>

# HTTP transport (remote)
claude mcp add --scope user --transport http <name> https://server.example.com/mcp

# Verify
claude mcp list                    # should show ✓ Connected
```

Scope options:
- `--scope user` — global, across all projects (recommended for tools you use everywhere)
- `--scope project` — shared in `.mcp.json`, committed to repo
- `--scope local` — this project, your machine only (default)

Config files:
- User: `~/.claude.json` under `mcpServers`
- Project: `.mcp.json` at repo root
- Local: `~/.claude.json` under `projects[<cwd>].mcpServers`

**Before installing**, ask: does the user actually use this service? Most MCPs past the foundation tier need paid accounts or API keys. Don't install speculatively.

## The 30-server catalog (priority order)

### Tier 1: Foundation (install first — free, official, make everything else better)

| # | Server | Purpose | Install |
|---|--------|---------|---------|
| 1 | filesystem | Direct fs read/write/search beyond cwd | `claude mcp add --scope user filesystem -- npx -y @modelcontextprotocol/server-filesystem <allowed-path>` |
| 2 | git | Git operations via MCP (diff, log, blame) | `claude mcp add --scope user git -- uvx mcp-server-git` |
| 3 | memory | Knowledge-graph persistent memory | `claude mcp add --scope user memory -- npx -y @modelcontextprotocol/server-memory` |
| 4 | sequential-thinking | Multi-step structured reasoning | `claude mcp add --scope user sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking` |

### Tier 2: Development & code

| # | Server | Auth | Use for |
|---|--------|------|---------|
| 5 | **GitHub** (github.com/github/github-mcp-server) | GITHUB_PAT | #1 most popular. PRs, issues, code search, workflows. |
| 6 | Playwright (github.com/microsoft/playwright-mcp) | none | Browser automation, UI tests, screenshots. |
| 7 | Sentry (github.com/getsentry/sentry-mcp) | Sentry auth | Read crash reports, stack traces. |
| 8 | Semgrep (github.com/semgrep/mcp) | free tier | SAST, security scanning. |
| 9 | CircleCI (github.com/circleci/mcp-server-circleci) | CCI token | Debug pipelines. |

### Tier 3: Databases & data

| # | Server | Auth |
|---|--------|------|
| 10 | PostgreSQL / Neon (github.com/neondatabase/mcp-server-neon) | DB URL / Neon acct |
| 11 | Supabase (github.com/supabase-community/supabase-mcp) | Supabase project |
| 12 | Neo4j (github.com/neo4j/neo4j-mcp) | local desktop ok |
| 13 | Qdrant (github.com/qdrant/mcp-server-qdrant) — vector DB | local ok |
| 14 | ClickHouse / Tinybird (github.com/tinybirdco/mcp-tinybird) | paid |

### Tier 4: Cloud & infrastructure

| # | Server | Auth |
|---|--------|------|
| 15 | AWS suite (github.com/awslabs/mcp) | AWS creds |
| 16 | Cloudflare (github.com/cloudflare/mcp-server-cloudflare) — 16 specialized servers | CF acct |
| 17 | Grafana (github.com/grafana/mcp-grafana) | Grafana instance |
| 18 | Railway (github.com/nichochar/railway-mcp) | Railway token |
| 19 | Render (github.com/render-oss/render-mcp-server) | Render token |

### Tier 5: Productivity & business

| # | Server | Auth |
|---|--------|------|
| 20 | Notion (github.com/makenotion/notion-mcp-server) | Notion integration token |
| 21 | Slack (github.com/anthropics/slack-mcp) | Slack bot token |
| 22 | Gmail | OAuth (claude.ai provides this) |
| 23 | Jira / Asana | workspace auth |
| 24 | Stripe (github.com/stripe/agent-toolkit) | Stripe secret key |
| 25 | HubSpot | HubSpot auth |

### Tier 6: Web scraping & extraction

| # | Server | Auth |
|---|--------|------|
| 26 | Firecrawl (github.com/mendableai/firecrawl) | free tier |
| 27 | Browserbase (github.com/browserbase/mcp-server-browserbase) | paid |
| 28 | Bright Data | paid |
| 29 | Apify (github.com/apify/actors-mcp-server) | free tier |

### Tier 7: Media & design

| # | Server | Auth |
|---|--------|------|
| 30 | Figma (github.com/nichochar/figma-mcp) | Figma PAT (free) |
| + | ElevenLabs (github.com/elevenlabs/elevenlabs-mcp) | API key |
| + | Context7 (github.com/upstash/context7) — library docs | free |

## Recommended install order (tell the user this every time)

1. **Foundation** — filesystem, git, memory, sequential-thinking (always).
2. **Personal stack** — whichever 2-3 match the user's actual daily tools (GitHub + Postgres + AWS, or GitHub + Supabase + Cloudflare, etc.).
3. **Productivity** — Notion, Slack, Gmail if they live in those tools.
4. **Extraction/scraping** — only when a specific task needs it (don't speculatively install Firecrawl).

## Task → MCP routing

When the user describes a task, map to the minimum set of MCPs needed.

| Task signal | Primary MCP | Supporting |
|-------------|-------------|------------|
| "Review this PR" | github | git (local diff) |
| "Query my database" | postgres / supabase | — |
| "Summarize Slack thread" | slack | — |
| "Find me current info about X" | tavily / brave-search | — |
| "Extract brand tokens from URL" | chrome-devtools | playwright, puppeteer |
| "Lookup this library's API" | context7 | — |
| "Read / edit my notes" | obsidian | filesystem |
| "Check error rate in production" | sentry + grafana | — |
| "Deploy the infra change" | terraform / kubernetes | github |
| "Design / extract from Figma" | figma | — |
| "Scrape a SaaS page without an API" | firecrawl / browserbase | playwright |
| "Process a payment / refund" | stripe | — |
| "Ticket triage" | jira / asana / github issues | slack |

## Your current stack (ground truth, 2026-04-16)

Run `claude mcp list` for the live authoritative view.

**Actually connected (8)**:
- `filesystem` (user, stdio) — foundation, fs read/write beyond cwd
- `memory` (user, stdio) — foundation, knowledge-graph memory
- `sequential-thinking` (user, stdio) — foundation, multi-step reasoning
- `git` (user, stdio, via uvx) — foundation, git ops via MCP
- `chrome-devtools` (user, stdio) — brand design-token extraction via Hue
- `gmail` via claude.ai OAuth ✓
- `supabase` (~/.mcp.json, HTTP) — project_ref: pzpaebzlwwmyhgwcjsge
- `code-review-graph` (~/.mcp.json, stdio)

**Auth-pending (2)**: `google-calendar`, `google-drive` (claude.ai OAuth, need refresh).

**Aspirational (19 — documented in CLAUDE.md as targets, not yet installed)**: github, context7, postgres, playwright, puppeteer, docker, kubernetes, terraform, slack, notion, stripe, brave-search, tavily, google-maps, obsidian, aster, sim-studio, hermes, penpot, aidesigner.

See `GAPS.md` in this skill's directory for a structured matrix and install recommendations.

## Relationship to other skills in this setup

- `mcp-builder` — when the user needs to **build** a new MCP server from scratch, not look up an existing one.
- `paperclip` — governance/authority-aware MCP dispatch in the broader org pipeline.
- `coremind-core` — 10-stage CoreMind pipeline; Stage 4 (Planner) routes task domains to MCP servers using the table above.
- `governance-gate` — policy layer; MCP security gate auto-validates tool calls against whitelist.

## Rules for Claude

1. When the user says "set up MCP for X", give them: repo link + exact install command + verify command. Don't paraphrase.
2. When the user describes a task, name the minimum MCP set needed from the routing table. Don't recommend an MCP the user doesn't have without flagging it.
3. Before suggesting an install, check `claude mcp list` and `~/.claude.json` + `~/.mcp.json` for what's already there.
4. Always remind: MCP = access. Skills = playbook. Need both.
5. If a task can be done with built-in tools (Read, Write, Bash, WebFetch), don't invent an MCP for it.
6. Never install a paid-auth MCP without explicit user authorization.
