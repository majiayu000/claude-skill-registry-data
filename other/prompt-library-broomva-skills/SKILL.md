---
name: prompt-library
category: tooling
description: >
  Manage and retrieve reusable prompts from broomva.tech or any compatible prompt repository.
  Pull prompts by slug, category, or tag; push new prompts or update existing ones; list
  available prompts with filtering. Supports remote push/update/delete via authenticated API
  using OAuth session tokens. Use when: (1) user asks for a prompt, system instruction,
  or agent directive, (2) user wants to save a prompt for reuse, (3) user mentions "prompt
  library", "prompt repo", "save this prompt", "get prompt", "pull prompt", (4) agent needs
  a reusable system prompt for a task like code review, research, or architecture analysis,
  (5) user says "use the X prompt" referring to a named prompt. Default distribution endpoint:
  https://broomva.tech/api/prompts
---

# Prompt Library

Manage versioned, parameterized prompts stored in a database and distributed via a JSON API.

## Quick Start

### Pull a prompt

```bash
python3 scripts/prompt-sync.py pull code-review-agent
```

### List available prompts

```bash
python3 scripts/prompt-sync.py list
```

### Pull with variable substitution

```bash
python3 scripts/prompt-sync.py pull code-review-agent --var language=python --var strictness=strict
```

### Push a prompt remotely (over the air)

```bash
python3 scripts/prompt-sync.py remote-push \
  --title "My Prompt" \
  --category system-prompts \
  --body "You are a helpful assistant..." \
  --tags "tag1,tag2" \
  --token "$BROOMVA_API_TOKEN"
```

## Commands

### Read Commands

| Command | Description |
|---------|-------------|
| `list` | List all prompts (supports `--category`, `--tag`, `--model` filters) |
| `pull <slug>` | Fetch a prompt by slug, print raw content |

### Local Write Commands

| Command | Description |
|---------|-------------|
| `push` | Write a new prompt MDX file to local `content/prompts/` |
| `update <slug>` | Update an existing local prompt, optionally bump version |

### Remote Write Commands (API-based)

| Command | Description |
|---------|-------------|
| `remote-push` | Create a prompt via the remote API (requires auth token) |
| `remote-update <slug>` | Update a prompt remotely (owner or admin only) |
| `remote-delete <slug>` | Soft-delete a prompt remotely (owner or admin only) |

All commands accept `--endpoint URL` to target a different prompt repository. Default: `https://broomva.tech/api/prompts`.

## Authentication

Remote commands require an API token. Get yours by:

1. Log in at [broomva.tech](https://broomva.tech) via OAuth (Google/GitHub)
2. Visit `https://broomva.tech/api/auth/api-token` to get your session token
3. Set it: `export BROOMVA_API_TOKEN="your-token-here"`

Or pass `--token` directly to any remote command.

The token is your OAuth session token — it's user-scoped and auto-expires. No static API keys needed.

### Admin Features

For the admin user (`carlosdavidescobar@gmail.com`), remote pushes and updates also:
- Commit the prompt as an MDX file to the GitHub repo
- Trigger a Vercel redeploy automatically

## Prompt Schema

See `references/prompt-schema.md` for the full frontmatter specification.

Key fields:
- `category`: system-prompts, agent-instructions, templates, chains, evaluators
- `version`: Semver string for tracking prompt evolution
- `variables`: Declared template variables with `{{name}}` syntax and defaults
- `model`: Target model (optional)
- `tags`: Searchable tag array

## Category Taxonomy

See `references/categories.md` for the full taxonomy.

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/api/prompts` | Public | List prompts (DB + MDX fallback) |
| `POST` | `/api/prompts` | Required | Create a new prompt |
| `GET` | `/api/prompts/[slug]` | Public | Get prompt by slug |
| `PUT` | `/api/prompts/[slug]` | Owner/Admin | Update a prompt |
| `DELETE` | `/api/prompts/[slug]` | Owner/Admin | Soft-delete a prompt |
| `GET` | `/api/auth/api-token` | Session | Get your bearer token |

## For Other Repositories

Anyone can host their own prompt library:

1. Create a database table for prompts (or use `content/prompts/` with `.mdx` files)
2. Add the API routes: `GET /api/prompts`, `GET /api/prompts/[slug]`, `POST /api/prompts`
3. Use `--endpoint https://your-site.com/api/prompts` with the sync script

The schema and API contract are the standard. The endpoint is configurable.
