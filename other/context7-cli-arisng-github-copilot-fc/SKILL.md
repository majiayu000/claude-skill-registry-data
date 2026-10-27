---
name: context7-cli
description: CLI tool for managing AI coding skills across different AI assistants like Claude, Cursor, and others. Use when you need to search, install, generate, or manage AI coding skills using the Context7 registry. Supports authentication, skill discovery, installation, and generation workflows.
version: 1.0.0
---

# Context7 CLI

This skill provides guidance for using the Context7 CLI (`ctx7`) to manage AI coding skills across different AI assistants.

## Installation

The Context7 CLI can be installed globally or run directly with npx:

```bash
# Install globally
npm install -g ctx7

# Or run directly (no installation needed)
npx ctx7
```

## Authentication

Before using authenticated features like skill generation, you need to log in:

```bash
# Log in (opens browser for OAuth)
ctx7 login

# Check login status
ctx7 whoami

# Log out
ctx7 logout
```

## Core Workflows

### Searching for Skills

Search the Context7 registry for skills by topic or technology:

```bash
# Search for skills
ctx7 skills search pdf
ctx7 skills search typescript
ctx7 skills search "react testing"
```

### Installing Skills

Install skills from the registry to your AI assistant:

```bash
# Install a specific skill
ctx7 skills install /anthropics/skills pdf

# Install multiple skills
ctx7 skills install /anthropics/skills pdf commit

# Install to specific AI assistant
ctx7 skills install /anthropics/skills pdf --claude
ctx7 skills install /anthropics/skills pdf --cursor

# Install globally (home directory)
ctx7 skills install /anthropics/skills pdf --global
```

### Generating Custom Skills

Create new skills tailored to your needs using AI:

```bash
# Generate a skill (requires login)
ctx7 skills generate

# Generate for specific assistant
ctx7 skills generate --claude
ctx7 skills generate --cursor

# Short aliases
ctx7 skills gen
ctx7 skills g
```

The generation process:
1. Describe the expertise you want (e.g., "OAuth authentication with NextAuth.js")
2. Select relevant libraries from search results
3. Answer clarifying questions
4. Review and install the generated skill

### Managing Installed Skills

```bash
# List installed skills
ctx7 skills list
ctx7 skills list --claude
ctx7 skills list --global

# Get info about available skills in a project
ctx7 skills info /anthropics/skills

# Remove a skill
ctx7 skills remove pdf
ctx7 skills remove pdf --claude
```

## Supported AI Assistants

The CLI automatically detects and supports:

- Claude Code (`.claude/skills/`)
- Cursor (`.cursor/skills/`)
- Codex (`.codex/skills/`)
- OpenCode (`.opencode/skills/`)
- Amp (`.agents/skills/`)
- Antigravity (`.agent/skills/`)

## Common Use Cases

### Finding Skills for Specific Tasks

When a user needs skills for a particular technology or framework:

1. Search the registry: `ctx7 skills search <topic>`
2. Review results and install relevant skills
3. Verify installation with `ctx7 skills list`

### Setting Up a New Project

For new projects, install commonly needed skills:

```bash
# Install essential skills for web development
ctx7 skills install /anthropics/skills typescript react testing --claude
```

### Creating Custom Skills

When existing skills don't cover specific needs:

1. Use `ctx7 skills generate` for AI-assisted creation
2. Provide detailed description of required expertise
3. Review and refine the generated skill
4. Install to your preferred AI assistant

## Tips

- Use short aliases for faster workflow: `ctx7 si` (install), `ctx7 ss` (search)
- Skills are installed to project-specific directories by default
- Use `--global` flag for skills available across all projects
- Generation has weekly limits (6 free, 10 pro accounts)
- Visit [context7.com](https://context7.com) to browse the registry manually