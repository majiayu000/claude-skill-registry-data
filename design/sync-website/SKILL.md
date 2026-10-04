---
name: sync-website
description: "Sync the yaah marketing website (website/index.html) with the current project state — features, CLI commands, skills, agents, hooks, and installation instructions. Use this skill whenever the user adds, removes, or changes a feature, CLI command, hook, skill, agent, MCP server, or LSP provider AND the website should reflect that change. Also use when the user explicitly asks to update, sync, or refresh the website, or says things like 'update the site', 'keep the website current', 'reflect this on the website', or 'the website is out of date'."
---

# Sync Website

Keep `website/index.html` in sync with the yaah project's actual capabilities.

## Why this matters

The website is a static single-page site in `website/`. It auto-deploys to GitHub Pages on push to `main` (via `.github/workflows/deploy-pages.yaml`). When features change in the Go code but the website isn't updated, users see stale information.

## Data sources and website sections

Each website section has a canonical source of truth. Read the source first, then update the HTML.

| Website section | HTML landmark | Source of truth |
|---|---|---|
| Hero stats (4 numbers) | `.hero-stats` `.stat-number` | Count from registries below |
| Features grid | `#features .features-grid` | `README.md` features + `pkg/` packages |
| How It Works | `#how-it-works` | `README.md` quick-start |
| Multi-Agent table | `#agents .table-wrapper` | `pkg/generator/` — one file per agent |
| Install methods | `#install .install-grid` | `README.md` install section |
| CLI Reference | `#cli .cli-grid` | `cmd/yaah/main.go` + `internal/cli/` cobra commands |

### How to count for hero stats

| Stat | How to count |
|---|---|
| Agents | Number of generators in `pkg/generator/` (claude, opencode, codex, copilot) |
| Skills | `ls .claude/skills/` — count directories that contain a SKILL.md |
| Hooks | Count distinct handler types in `pkg/hooks/handlers/` |
| Sub-Agents | `ls .claude/agents/` — count `.md` files |

## How to sync

1. **Audit** — Read the source of truth for the section that changed. Read `website/index.html` to see what's currently shown.

2. **Diff** — Identify what's new, removed, or changed.

3. **Edit** — Update `website/index.html` with the Edit tool. Match existing HTML patterns exactly:
   - Feature cards: `<div class="feature-card">` with `<h3>` and `<p>`
   - CLI items: `<div class="cli-item">` with `<code>` for command, `<p>` for description
   - Stats: `<div class="stat">` with `<span class="stat-number">` and `<span class="stat-label">`
   - Install cards: `<div class="install-card">` with code blocks

4. **Verify** — Count items in the edited HTML to confirm they match the codebase.

## Rules

- Only update sections where data actually changed.
- Preserve existing CSS classes, HTML structure, and visual design.
- Keep copy concise — one sentence per feature card, short CLI descriptions.
- Every claim on the website must be backed by code that exists right now.
- If a feature was removed from the code, remove it from the website.
- After editing, remind the user that the deploy triggers automatically on push (workflow watches `website/**`).
