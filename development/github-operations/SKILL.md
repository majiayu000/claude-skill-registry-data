---
name: github-operations
description: Use when Codex must inspect or update GitHub resources (issues, PRs, workflows) through the official remote GitHub MCP server.
---

# GitHub Operations

## Purpose
Provide actionable steps for reviewing pull requests, triaging issues, syncing branches, and triggering GitHub workflows using the GitHub-hosted MCP server defined in `servers/github`.

## Setup Checklist
1. Ensure `mcp.json` includes the `github` entry pointing to `${GITHUB_MCP_ENDPOINT}` with the `${GITHUB_MCP_TOKEN}` Authorization header.
2. Confirm scopes on `${GITHUB_MCP_TOKEN}` cover `repo`, `workflow`, and `read:org`.
3. Keep repository context synchronized locally so file diffs referenced by the server make sense inside this workspace.

## Core Workflow
1. **Plan** – summarize the GitHub objective (e.g., “merge PR #42 after lint passes”) and list the API actions needed (`pullRequest.get`, `reviews.create`, etc.).
2. **Execute** – call the MCP tools exposed by the server (issue search, PR diff, workflow dispatch). Prefer batched queries to avoid rate limits.
3. **Validate** – re-fetch the entity to confirm the state transition (PR merged, labels applied, workflow run queued).
4. **Document** – record actions inside the user message or repository docs when follow-up by humans is required.

## Operational Notes
- Rate limits from GitHub are enforced at the server; when a call is throttled, wait 5 seconds and retry once.
- Use read-only queries when gathering context for other skills (e.g., fetching PR details before a filesystem refactor) to minimize write noise.
- Treat `${GITHUB_MCP_TOKEN}` as a production credential—store it in `.env.local` and do not log it.
