---
name: plugin-audit
description: Diff the Anthropic `claude-plugins-official` marketplace against installed plugins and surface the delta, filtering known-unwanted entries (language LSPs you don't use, SaaS integrations you don't use, sample/demo plugins).
triggers:
  - "audit plugins"
  - "what plugins am I missing"
  - "check anthropic marketplace"
  - "plugin delta"
---

# plugin-audit

Keeps the gap between Anthropic's official marketplace and your installed plugin set visible and actionable, without reinstalling things you already have or surfacing language LSPs you'll never use.

## When to run

- Monthly hygiene check.
- After a fresh clone / machine setup, before deep work.
- When a new feature lands in claude-plugins-official (watch its README for changelog hints).

## One-liner

```bash
bash ~/.claude/skills/plugin-audit/audit.sh
```

Returns:
- A ranked list of plugins present in the marketplace but not installed, with reason to install / skip.
- A short install plan (exact `claude plugin install <name>@claude-plugins-official` commands for the recommended set).

## Exclusions (tune per user)

Edit `audit.sh` to maintain the user's skip list. Defaults:

- **Language LSPs** not in use: `clangd-lsp`, `csharp-lsp`, `gopls-lsp`, `jdtls-lsp`, `kotlin-lsp`, `lua-lsp`, `php-lsp`, `ruby-lsp`, `rust-analyzer-lsp`, `swift-lsp`, `typescript-lsp` (TS LSP often skipped if you already have editor-integrated TS tooling).
- **SaaS integrations** not in use: `asana`, `imessage`, `telegram`, `greptile`, `firebase`, `gitlab`, `discord` (plugin — you may run Discord via MCP), `laravel-boost`, `terraform` (unless running IaC).
- **Samples**: `example-plugin`, `fakechat`, `math-olympiad`, `playground`.

Everything else is surfaced with a `(candidate)` tag.

## Output format

```
Installed: 30  |  Available (post-filter): 8  |  Delta: 3

Candidates to install:
  - session-report    — structured end-of-session report
  - hookify           — hook authoring assistant
  - mcp-server-dev    — MCP server build patterns

Install plan:
  claude plugin install session-report@claude-plugins-official
  claude plugin install hookify@claude-plugins-official
  claude plugin install mcp-server-dev@claude-plugins-official
```

## Why this exists

Claude's `find-skills` skill searches the full ecosystem (90k+ skills) and is great for discovery. `plugin-audit` is narrower and opinionated: it answers *"what should I install from the one marketplace I trust, and skip everything else"*. The two complement each other.

## Related

- `find-skills` — community-wide discovery
- `skill-creator` — authoring new skills once installed
- `skill-maintainer` — auditing installed skills (not plugins)
