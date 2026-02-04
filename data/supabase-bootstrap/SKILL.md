---
name: supabase-bootstrap
description: "Bootstrap toolkit for new Supabase projects. Use when: (1) Setting up a new Supabase project, (2) Configuring sqlfluff for SQL formatting, (3) Setting up mise task runner, (4) Configuring MCP server for schema access, (5) Initializing project structure"
license: Proprietary. LICENSE.txt has complete terms
---

# Supabase Project Bootstrap

Toolkit for setting up new Supabase projects with proper tooling.

## Quick Start

Copy template files to your Supabase project:

```bash
cp assets/mise.toml assets/.sqlfluff assets/.mcp.json /path/to/supabase/
```

Then configure `.mcp.json` with your project reference.

## Template Files

| File | Purpose |
|------|---------|
| `assets/mise.toml` | Task runner (lint, format, psql install) |
| `assets/.sqlfluff` | SQL formatting config |
| `assets/.mcp.json` | MCP server for schema access |

## Setup Steps

### 1. Copy Templates

```bash
cd your-project/supabase
cp /path/to/skill/assets/* .
```

### 2. Configure MCP

Edit `.mcp.json` and replace `PROJECT_REF_PLACEHOLDER` with your Supabase project reference:

```json
{
  "mcpServers": {
    "supabase": {
      "type": "http",
      "url": "https://mcp.supabase.com/mcp?project_ref=YOUR_PROJECT_REF?read_only=true"
    }
  }
}
```

Find your project ref in Supabase Dashboard → Project Settings → General.

### 3. Install Tools

```bash
# Install mise if not already installed
curl https://mise.run | sh

# Install project tools (sqlfluff, psql)
mise install
```

### 4. Verify Setup

```bash
# Check sqlfluff
mise run lint

# Check MCP connection (requires Claude Code)
# MCP will auto-connect when querying schema
```

## Directory Structure

After bootstrap, your project should have:

```
supabase/
├── .mcp.json           # MCP server config
├── .sqlfluff           # SQL formatter config
├── mise.toml           # Task runner
├── migrations/         # Schema migrations
└── seed/               # Seed data files
```

## Available Tasks

After setup, use mise to run tasks:

```bash
mise run lint           # Lint SQL files
mise run format         # Format SQL files
mise run fix            # Lint and auto-fix
mise run install-psql   # Install PostgreSQL client
```
