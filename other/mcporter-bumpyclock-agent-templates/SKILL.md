---
name: mcporter
description: "Call configured MCP servers through mcporter, including Chrome, web search, design tools, Microsoft 365, and Higgsfield media, brand, website, app, and game workflows."
---

# mcporter

Use mcporter to call configured MCP tools from the terminal. Read only the relevant server reference below.
Use its known calls for documented servers directly. Discover schemas only for undocumented tools, missing arguments, or a schema mismatch. Update the relevant server reference when updated tools are discovered (add or remove).

## Common paths

```bash
# Find configured aliases without connecting to every server.
mcporter config list

# Inspect one unfamiliar tool, or one server when the tool is unknown.
mcporter list SERVER.TOOL --schema --no-oauth
mcporter list SERVER --brief --no-oauth

# Call a tool. JSON preserves nested objects, arrays, booleans, and string IDs.
mcporter call SERVER.TOOL --args '{"key":"value"}' --output json
mcporter call SERVER.TOOL key=value --output text
```

Replace uppercase placeholders and example IDs with actual values. Alias and argument names are case-sensitive.
Use `--output text` for readable content and `--output json` for structured processing.
Inspect the result for tool errors; a completed CLI process does not prove the requested action succeeded.
For writes, verify the resulting state before reporting completion. Do not blindly replay a write after a timeout.

Use `mcporter --help` and `mcporter <command> --help` for less common commands and flags.
Do not load every server schema or copy the CLI manual into context.

## Server references

These aliases reflect the configuration inspected on 2026-09-28. If needed tool unavailable or needs auth let user know.
Examples use discovered schemas, not executed account operations. Read the matching reference before calling its tools.

| Task | Alias and reference |
| --- | --- |
| Browser use for Automate or inspect existing Chrome tabs | [chrome-devtools](references/browser-use.md) |
| Web Search or fetch public web content | [exa-search](references/exa-search.md) |
| Inspect Figma designs, components, or variables | [figma](references/figma.md) |
| Read or edit Craft documents and tasks | [craft](references/craft.md) |
| Find meetings or work with calendar events | [MicrosoftCalendar](references/microsoft-calendar.md) |
| Search mail, read messages, or prepare drafts | [MicrosoftEmail](references/microsoft-email.md) |
| Retrieve evidence across enterprise sources | [Workiq](references/workiq.md) |
| Resolve people and organization details | [m365-user](references/m365-user.md) |
| Ask Copilot about cross-workload internal content | [m365-copilot](references/m365-copilot.md) |
| Search Viva Engage conversations | [engage](references/engage.md) |
| Search Microsoft documentation and code samples | [msft-learn](references/msft-learn.md) |
| Find and read OneDrive files | [onedrive](references/onedrive.md) |
| Find Planner plans, tasks, and goals | [planner](references/planner.md) |
| Query Power BI semantic models and reports | [powerbi](references/powerbi.md) |
| Find Teams chats, channels, and messages | [teams](references/teams.md) |
| Read Word documents and comments | [word](references/word.md) |
| Find Azure DevOps work items, pull requests, builds, and logs | [ado](references/ado.md) |
| Generate or edit media, create brand assets, or build websites, apps, and games | [higgsfield](references/higgsfield.md) |

## Higgsfield workflows

For Higgsfield tasks, read [Higgsfield](references/higgsfield.md), then only the matching workflow guide.
The guides, supporting references, and bundled scripts live under `references/higgsfield/`; they are not separate skills.
Use the documented `higgsfield` CLI for CLI workflows. Use `mcporter call higgsfield.TOOL` for MCP operations.

## Connection and authorization

For a missing alias, authentication failure, or configuration problem, read [Configuration and recovery](references/configuration.md).
Use configured aliases instead of reconstructing endpoints or copying credentials into commands.
Keep internal content out of public search queries. Never print tokens, passwords, cookies, or authorization headers.
Tool availability does not authorize sending messages, changing permissions, deleting data, or other account writes.

When maintaining a reference, record verified tool names, common arguments, pagination, and non-obvious constraints.
Exclude credentials, private endpoints, account data, and machine-specific paths. Mark unavailable schemas rather than guessing their tools.
