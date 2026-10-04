---
name: broomva-cli
category: tooling
description: >
  CLI for broomva.tech — manage prompts, skills, and context from the terminal.
  Pull/push prompts, browse the skills roster, and query project conventions.
triggers:
  - broomva cli
  - broomva prompts
  - push prompt
  - pull prompt
  - broomva skills
  - broomva context
---

# @broomva/cli

CLI for broomva.tech — prompts, skills, and context from the terminal.

## Installation

```bash
bunx @broomva/cli            # one-shot
bun add -g @broomva/cli      # global install
```

## Authentication

```bash
broomva auth login    # Guided login: sign in → get token → paste
broomva auth status   # Check auth state
broomva auth token    # Print current token
broomva auth logout   # Remove stored token
```

### How it works

1. **Sign in** at [broomva.tech](https://broomva.tech) using email/password, Google, or GitHub.
   Accounts with the same email are automatically linked — you can sign up with email
   and later log in with Google (or vice versa) and it resolves to the same user.
2. **Get your token** at `https://broomva.tech/api/auth/api-token` (requires active session).
3. **Paste it** when `broomva auth login` prompts you, or set `BROOMVA_API_TOKEN` env var.

Token is stored in `~/.broomva/config.json` (0o600). Resolution order: `--token` flag > `BROOMVA_API_TOKEN` env > config file. Tokens are session-scoped and auto-expire.

## Commands

### Prompts

```bash
broomva prompts list                        # List all public prompts
broomva prompts list --mine                 # List your prompts (auth required)
broomva prompts list --category agents      # Filter by category
broomva prompts list --tag research --json  # JSON output

broomva prompts get <slug>                  # Show prompt with metadata
broomva prompts get <slug> --raw            # Content only (pipe-friendly)
broomva prompts get <slug> --json           # Full JSON

broomva prompts create --title "My Prompt" --content @prompt.md
broomva prompts update <slug> --content @updated.md --tags "agent,research"
broomva prompts delete <slug>

broomva prompts pull <slug>                 # Download to <slug>.md
broomva prompts pull <slug> -o custom.md    # Custom output path
broomva prompts push prompt.md              # Update from local file
broomva prompts push prompt.md --create     # Create new from local file
```

### Skills

```bash
broomva skills list                    # Browse all layers
broomva skills list --layer foundation # Filter by layer
broomva skills get <slug>              # Skill details
broomva skills install <slug>          # Runs npx skills add broomva/<slug>
```

### Context

```bash
broomva context show          # Full project context
broomva context conventions   # Conventions only
broomva context stack         # Tech stack only
```

### Config

```bash
broomva config get                    # Show all config
broomva config get apiBase            # Show single value
broomva config set apiBase http://localhost:3000  # Override API base
broomva config set defaultFormat json # Default output format
broomva config reset                  # Reset to defaults
```

### Global Options

```
--json          Output as JSON
--api-base URL  Override API base URL
--token TOKEN   Override auth token
--no-color      Disable colored output
```

## API Base

Default: `https://broomva.tech`. Override with `--api-base`, `broomva config set apiBase`, or for local dev: `--api-base http://localhost:3000`.

## File Format for Push/Pull

Prompts use markdown with YAML frontmatter:

```markdown
---
title: "My Prompt"
slug: "my-prompt"
category: "agents"
tags: ["research", "coding"]
visibility: "public"
---

Your prompt content here...
```
