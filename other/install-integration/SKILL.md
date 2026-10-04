---
name: install-integration
description: Install a new MCP server, Claude Code skill, or plugin — either from a GitHub URL (auto-detect its shape from the README/manifest) or by name only (look it up in the plugin marketplace first, then ask the user to verify if it isn't found). Use whenever asked to add/install an integration.
---

# Install Integration — MCP Server / Skill / Plugin

Three different things can live at a GitHub URL someone hands you, and
each installs a different way. Never assume which one it is from the repo
name alone — check the actual repo contents.

| Kind | What it is | Where it installs |
|---|---|---|
| **MCP server** | A process/endpoint exposing tools over the Model Context Protocol | This repo's `.mcp.json` (shared) + each dev's `enabledMcpjsonServers` |
| **Plugin** | A bundle of skills/commands/agents, distributed via a marketplace | Globally, per-developer (`claude plugin install`) — not git-tracked |
| **Skill** (bare, no plugin manifest) | A single `SKILL.md` (+ assets) | `.claude/skills/<name>/` in this repo (team-shared) or the user's personal `~/.claude/skills/` |

## Path A — given a GitHub URL

1. **Inspect the repo structure** before reading prose — it's the reliable
   signal, the README's wording isn't. For a GitHub URL `<owner>/<repo>`:
   ```bash
   gh api repos/<owner>/<repo>/git/trees/HEAD?recursive=1 --jq '.tree[].path'
   ```
   Look for:
   - `.claude-plugin/marketplace.json` at root → this repo **is a
     marketplace** (a catalog of plugins, possibly just one).
   - `.claude-plugin/plugin.json` (with or without a marketplace.json) →
     this repo **is a plugin**.
   - `SKILL.md` at root or under `skills/*/SKILL.md`, no plugin manifest →
     **bare skill(s)**.
   - No `.claude-plugin/`, but README/code shows a `command`+`args` (or
     `mcpServers` JSON) meant for an MCP client config, or the package
     name/description says "MCP server" → **MCP server**.
   - A repo can only be one of the above at the root — if it looks like
     more than one, or none, read the README
     (`gh api repos/<owner>/<repo>/readme -H "Accept: application/vnd.github.raw"`)
     before guessing.

2. **Install by kind:**

   - **MCP server** — read the README's config example for the exact
     `command`/`args`/`env` (or `url`, for an `http`/`sse` server). Add an
     entry to this repo's `.mcp.json` matching the existing shape (see the
     `chrome-devtools`/`TalkToFigma`/`stitch` entries). This file is
     committed and shared — confirm the entry with the user before
     writing it, since it's team-wide config, and note that enabling it
     locally (`enabledMcpjsonServers` in each developer's own
     `.claude/settings.local.json`, gitignored) is a separate per-developer
     step everyone has to do themselves. If the server needs auth/setup
     (API key, OAuth, gcloud), document the one-time steps in a
     `.claude/rules/<name>.md` the way `.claude/rules/stitch-design.md`
     does — don't assume the next session/teammate will rediscover them.

   - **Plugin** — add its marketplace and install it:
     ```bash
     claude plugin marketplace add <owner>/<repo>
     claude plugin install <plugin-name>@<marketplace-name>
     ```
     (`<marketplace-name>` and `<plugin-name>` come from the repo's
     `.claude-plugin/marketplace.json` — read it, don't assume it matches
     the repo name.) This is a **global, per-developer install** — it does
     NOT get vendored into this repo or inherited by teammates. Write a
     short note in a relevant rule file (pattern: `.claude/rules/stitch-design.md`'s
     "Skill plugin" section) so the team knows the plugin exists and how
     to install it themselves.

   - **Bare skill (no plugin manifest)** — ask the user whether this
     should be team-shared or personal-only if it's not obvious from
     context:
     - Team-shared → copy the skill's directory (SKILL.md + assets) into
       `.claude/skills/<name>/` in this repo, matching this repo's other
       vendored skills (e.g. `brainstorming/` already vendored this way).
     - Personal-only → point the user at copying it into their own
       `~/.claude/skills/<name>/` instead — that's outside this repo's git
       history, same category as the TalkToFigma bridge
       (`.claude/rules/figma-design.md`).

3. Decide, per `claude-code-conventions` skill's decision guide, whether
   the new integration also needs a short rule file (so future sessions
   know it exists and when to reach for it) — most nontrivial integrations
   do; a one-off personal convenience plugin usually doesn't.

## Path B — given only a name, no link

1. Check marketplaces already added: `claude plugin marketplace list`.
2. If not found there, add Anthropic's official marketplace (if not
   already added) and check it:
   ```bash
   claude plugin marketplace add anthropics/claude-plugins-official
   gh api repos/anthropics/claude-plugins-official/contents/.claude-plugin/marketplace.json -H "Accept: application/vnd.github.raw"
   ```
   Search the returned JSON for the requested name.
3. **Still not found** — stop. Do not guess a plausible GitHub repo for
   the name (this violates the "never generate/guess URLs" rule and the
   no-fallbacks principle — a wrong guess could install someone else's
   unrelated or malicious package). Tell the user it isn't in the known
   marketplaces and ask them to confirm the exact source (GitHub URL or
   correct package/plugin name) before proceeding to Path A.

## Load this skill when

- Asked to install/add a new MCP server, skill, or plugin — with or
  without a link.
- The `install-integration` rule fires.

## Skip when

- Just explaining what an existing integration does (no install action).
