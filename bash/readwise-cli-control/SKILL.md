---
name: readwise-cli-control
description: Use when a user wants to search, export, organize, or automate Readwise or Reader data from Codex or another terminal agent, especially when browser auth should be avoided and an access token is available.
---

# Readwise Cli Control

## Overview

This skill wraps the official Readwise CLI for headless use in Codex. Use it when the user wants direct control over Readwise or Reader without browser-based OAuth, or when they provide a Readwise access token.

For terminal agents, prefer the CLI over the remote MCP server. The official Readwise docs say the CLI is usually the simpler option for Codex and supports token auth via `readwise login-with-token <token>`.

## Decision Rule

Use this skill when the user wants any of the following:

- Search Readwise highlights or Reader documents from Codex
- Export or summarize saved articles, PDFs, newsletters, or tweets from Reader
- Organize Reader items by location, tags, shortlist/archive state, or highlights
- Authenticate Readwise with an access token instead of a browser
- Give Codex read-only or read-write control over Readwise/Reader

Do not assume the remote MCP server accepts token-based auth. The official current MCP docs document OAuth for `https://mcp2.readwise.io/mcp`; the official headless/token path is the CLI.

If you need the official rationale or URLs, read [references/official-notes.md](./references/official-notes.md).

## Quick Start

1. Ensure the CLI is installed and authenticated with a token:

```bash
READWISE_ACCESS_TOKEN='<token>'
"$HOME/.codex/skills/readwise-cli-control/scripts/setup-readwise-cli.sh" --readonly false
```

2. Run commands through the JSON wrapper:

```bash
"$HOME/.codex/skills/readwise-cli-control/scripts/readwise-json.sh" reader-search-documents --query "aggregation theory"
```

3. For read-only sessions:

```bash
READWISE_ACCESS_TOKEN='<token>'
"$HOME/.codex/skills/readwise-cli-control/scripts/setup-readwise-cli.sh" --readonly true
```

## Authentication Workflow

- Prefer `READWISE_ACCESS_TOKEN` in the shell environment over passing the token as a literal argument.
- If `readwise` is missing, run the setup script; it installs `@readwise/cli`.
- Use `readwise login-with-token` instead of `readwise login`.
- After changing readonly mode, refresh the CLI tool cache with `readwise --refresh`.

Readonly rules:

- `--readonly true` hides write operations and is safer for analysis-only tasks.
- If you switch readonly off after it was on, the CLI requires re-authentication. The setup script handles this by logging in again with the token.

## Common Commands

Prefer `readwise --json ...` so downstream parsing is reliable.

Reader document tasks:

```bash
readwise --json reader-search-documents --query "topic"
readwise --json reader-list-documents --location new
readwise --json reader-get-document-details --document-id <id>
readwise --json reader-create-document --url "https://example.com/article"
readwise --json reader-move-documents --document-ids <id1>,<id2> --location archive
readwise --json reader-add-tags-to-document --document-id <id> --tags "ai,research"
readwise --json reader-create-highlight --document-id <id> --text "The key insight is..."
readwise --json reader-export-documents
```

Readwise highlight tasks:

```bash
readwise --json readwise-search-highlights --vector-search-term "compounding"
readwise --json readwise-get-daily-review
```

If you need a command not listed here, run:

```bash
readwise --help
```

## Output Discipline

- Use JSON output for command execution.
- Summarize large results instead of pasting raw blobs unless the user explicitly wants the raw output.
- When referencing Reader documents, saved posts, highlights, or content ideas based on Readwise data, always include the original source link.
- For Reader documents, request `source_url` in `--response-fields` and use `source_url` as the link. Do not use `url` when `url` is a `read.readwise.io` Reader link and `source_url` is available.
- For Readwise highlights, request `book_source_url` and use that as the original link. Use the highlight `url` only as a fallback if no original source URL is available.
- If a list/search response does not include the original link, fetch details or export metadata before answering. Do not omit the original link when Readwise has it.
- For write operations, confirm intent if the user has not clearly asked to modify their library.
- If the token is missing, ask the user for it directly instead of falling back to browser auth.

## Scripts

- `scripts/setup-readwise-cli.sh`
  Installs the official CLI if needed, authenticates with `READWISE_ACCESS_TOKEN`, and sets readonly mode.
- `scripts/readwise-json.sh`
  Runs the official CLI with `--json`. If `READWISE_ACCESS_TOKEN` is set, it refreshes auth first.

## Portability Notes

- Specific to the author's current workflow: this prefers the official Readwise CLI and local skill scripts over browser OAuth or remote MCP usage.
- Reusable: token-in-environment authentication, readonly setup for analysis, JSON command output, original-source-link discipline, and confirmation before write operations.
- Adapt before reuse: configure the CLI install path, token storage, readonly default, allowed write operations, and source-link fields for the target Readwise account and CLI version.
