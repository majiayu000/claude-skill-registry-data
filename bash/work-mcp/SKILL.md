---
name: work-mcp
description: Use native Pi MCP tools for work services through code mode; keep queries narrow and confirm writes.
---

# Work MCP

Work default and web profiles connect directly to Pi's MCP servers.
Use `codemode` with `searchTools(query, { namespace: "<server>" })` and `describeTool(name)` to find the exact tool and arguments before calling `tools.<name>(args)`.
Reduce large results inside the script before returning them.
Use `/mcp` to inspect connections or sign in to an OAuth server; `pi mcp list` checks connection health from a shell.
Do not use MCPorter wrappers for these profiles.

- For Sourcegraph, scope searches to a repository, symbol, path, or revision and cite repository, revision, and path. Prefer local search for the current checkout.
- For Linear, start with exact issue identifiers, team, project, or a narrow query. Treat create, update, delete, comments, and attachments as mutations.
- For Slack, scope by channel, participant, topic, or time. Return only relevant private-message content. Treat send, reaction, marking, and workflow saves as mutations.
- For Granola, constrain discovery by date, participant, or folder. Use transcripts only when exact wording is needed; minimize private excerpts.
- For Grafana, start with a service, a short time window, and one signal. Separate evidence from hypotheses; treat alert changes as mutations.
- For Hubble, resolve the entity or DAG first; bound lineage depth and execution windows. Report identifiers, timestamps, and environment.
- For Lunar Skills, search or list the relevant practice, then read it before changing affected work code. Local repository instructions take precedence on conflict.
- For 1Password, access it only when explicitly requested. Return names and references unless the user needs a value, and never include secrets in summaries or logs.

The approval gate prompts for non-read-only MCP calls, including calls from code mode; it blocks them without an interactive UI. Obtain the user's approval for the exact mutation before requesting the gate confirmation.
