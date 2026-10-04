---
name: orbit-wp-playground
description: Thin wrapper around the official `WordPress/agent-skills` repo (Brandon Payton's wp-playground skill, January 2026). When invoked, ensures the WP core agent skill is installed via `npx openskills install WordPress/agent-skills`, and delegates Playground-related work to it. Use when the user says "wp-playground", "WordPress agent skill", "playground for AI", "openskills", or wants the AI agent to spin up WordPress in seconds for code-iteration testing.
---

# 🪐 orbit-wp-playground — Wrapper for WordPress core's official agent skill

> WP core ships `WordPress/agent-skills` (Jan 2026). It's good. We use it; we don't reinvent it.

---

## What is `WordPress/agent-skills`?

WordPress core's official AI agent skills — published by [Brandon Payton](https://profiles.wordpress.org/bpayton/) on January 30, 2026. The flagship skill is `wp-playground`: spins up WordPress via the [Playground CLI](https://github.com/WordPress/wordpress-playground), auto-detects whether your code should mount as plugin or theme, and gives AI agents a tight feedback loop to iterate on plugin code.

**Repo:** https://github.com/WordPress/agent-skills
**Announcement:** https://wordpress.org/news/2026/01/new-ai-agent-skill/

---

## Install

```bash
# Install for current project
npx openskills install WordPress/agent-skills

# Sync (make available to non-Claude agents)
npx openskills sync
```

Orbit's `install.sh` runs this for you on first install (opt-in prompt).

---

## What it does

When an AI agent (Claude Code, Codex, Cursor) detects this skill installed:

1. Starts WordPress in seconds via Playground CLI (much faster than wp-env's Docker)
2. Auto-mounts the current directory as the plugin or theme based on file signatures (plugin header → `wp-content/plugins/`, `style.css` with `Theme Name:` → `wp-content/themes/`)
3. Provides helper scripts so agents don't waste time waiting for "ready"
4. Auto-logs into WP-Admin for easy testing

**Comparison vs Orbit's `/orbit-docker-site`:**

| | `/orbit-docker-site` (wp-env) | wp-playground (this skill) |
|---|---|---|
| Backend | Docker (full WP + MySQL container) | WASM + browser-based PHP |
| Startup | 60-90s on first run | ~5s |
| Best for | Full gauntlet, DB profiling, CI | AI code iteration, smoke tests |
| Persistent state | Yes | Optional (Blueprints) |
| Multi-version matrix | Yes (PHP 7.4 / 8.x × WP 6.x / 7.x) | Limited |
| WP-CLI | Yes (full) | Yes (subset) |

Use both: `/orbit-docker-site` for heavy audits, wp-playground for fast iteration.

---

## Usage from inside Claude Code

After install, the AI agent has new tools available. Examples:

- "Spin up a fresh WP install and try my plugin"
- "Run wp-cli plugin list against my Playground site"
- "Open my plugin's settings page in the Playground site and screenshot"

The agent uses wp-playground's primitives directly — Orbit doesn't need to wrap them more deeply.

---

## How Orbit composes with WordPress/agent-skills

| Concern | Owner |
|---|---|
| Spin up WordPress for testing | **WordPress/agent-skills** (`wp-playground`) |
| Plugin code-quality audit | Orbit (`/orbit-wp-standards`, etc.) |
| UAT flows | Orbit (`/orbit-uat-agent`) |
| Live security feeds | Orbit (`/orbit-cve-check`) |
| Multi-version matrix testing | Orbit (`/orbit-compat-matrix`, full Docker) |
| AI orchestration of plugin code | WordPress/agent-skills + AI agent client |

WP core's skills handle the "spin up + iterate" loop. Orbit handles the "ship-readiness audit" loop. They compose — both installed, both used.

---

## Future additions WP core is considering

Per the announcement, WP core's roadmap for `agent-skills`:

- Persistent Playground sites based on the current directory
- Running commands against an existing Playground instance (incl. wp-cli)
- Blueprint generation for repeatable test scenarios

When those ship, `npx openskills install WordPress/agent-skills` picks them up automatically — Orbit benefits without any code change.

---

## Smoke test

Input: a vanilla "Hello Dolly" plugin in a fresh directory.
Expected:
- `npx openskills install WordPress/agent-skills` succeeds
- Agent can issue "spin up Playground for this plugin" command
- WordPress is reachable + plugin auto-activated within ~10 seconds
- WP-Admin opens with admin already logged in

---

## Pair with

- `/orbit-docker-site` — when you need full Docker isolation (CI, multi-version)
- `/orbit-uat-agent` — natural-language UAT runs against the Playground site
- `/orbit-do-it` — orchestrator picks Playground for fast iteration, Docker for release-gate

---

## Sources & Evergreen References

### Live sources (fetched on every run)
- [WordPress/agent-skills repo](https://github.com/WordPress/agent-skills) — the actual skills
- [Announcement — WordPress.org news](https://wordpress.org/news/2026/01/new-ai-agent-skill/) — context + roadmap
- [WordPress Playground](https://github.com/WordPress/wordpress-playground) — underlying Playground CLI
- [openskills CLI](https://www.npmjs.com/package/openskills) — install / sync runtime

### Embedded fallback rules (offline)
- Install command: `npx openskills install WordPress/agent-skills`
- Sync after install: `npx openskills sync`
- Skill name in agent's catalog: `wp-playground`

### Last reviewed
2026-04-30 — wrap, don't reinvent. WP core's roadmap is the source of truth here.
