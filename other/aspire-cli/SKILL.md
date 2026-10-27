---
name: aspire-cli
description: "Guidance for using the .NET Aspire CLI and agent integration to create, adopt, run, inspect, debug, update, publish, deploy, and automate Aspire AppHosts. Use when choosing or explaining Aspire commands and workflows such as aspire new, init, restore, run, start, ps, stop, wait, resource, describe, logs, otel, add, update, publish, deploy, do, doctor, docs list, docs search, docs get, or agent; when setting up AI coding agents with aspire agent init or aspire agent mcp; when browsing official Aspire guidance before editing unfamiliar integrations, custom commands, or AppHost APIs; when troubleshooting distributed apps with resource status, logs, traces, endpoints, or MCP docs tools such as list_docs, search_docs, and get_doc; or when running multiple AppHost instances in parallel with --isolated."
metadata:
   version: 0.11.0
   author: arisng
---

# Aspire CLI

Use this skill to choose the right Aspire workflow, keep long-running processes under Aspire's control, and combine AppHost source, official docs lookup, CLI inspection, MCP tools, and browser automation into a tight agent loop.

## Fast path

1. Identify the goal: scaffold, adopt, configure agents, browse official docs, start attached or detached, inspect, debug, manage resources, update, or publish/deploy.
2. Confirm context: AppHost path, single vs multiple AppHosts, human-interactive vs automation, single instance vs parallel worktrees.
3. Prefer the smallest reliable surface:
   - `aspire doctor` for environment issues.
   - `aspire agent init` for agent setup.
   - `aspire docs list`, `aspire docs search`, and `aspire docs get` before unfamiliar integrations, custom dashboard or resource commands, or AppHost APIs.
   - MCP `list_docs`, `search_docs`, and `get_doc` when the Aspire MCP server already exposes docs tools in the current agent session.
   - `aspire run` for attached interactive sessions.
   - `aspire start` for background or delegated sessions.
   - `aspire run --isolated` or `aspire start --isolated` for parallel worktrees, background agents, or side-by-side validation.
   - `aspire describe`, `aspire logs`, `aspire otel`, `aspire wait`, and `aspire resource` for CLI-first inspection and control.
   - MCP tools when the Aspire MCP server is already configured and runtime access is needed from the agent.
4. Read the AppHost source before changing orchestration. The AppHost is the topology source of truth.
5. Load only the reference files that match the task.

## Load this reference when...

| Need | Use |
| --- | --- |
| Command selection, flags, and automation-friendly patterns | [CLI commands overview](references/cli-commands.md) |
| Official docs lookup, docs-first edits, and CLI/MCP docs parity | [Docs lookup workflows](references/docs-lookup.md) |
| Current 13.2 command surface, renames, and migration notes | [Aspire 13.2 CLI notes](references/aspire-13.2-cli.md) |
| AppHost-first agent loop, docs-first editing, telemetry guidance, and Playwright pairing | [Agentic development with Aspire](references/agentic-development.md) |
| Adding Aspire to an existing solution | [App adoption patterns](references/app-adoption.md) |
| CLI and MCP runtime access, resource discovery, and agent wiring | [Aspire agent integration and resource access](references/mcp-server-and-resource-access.md) |
| Parallel worktrees, multi-instance AppHosts, or isolated mode | [Aspire isolation](references/aspire-isolation.md) |
| HTTPS certificate cleanup or trust issues | [HTTPS certificate management](references/https-cert-management.md) |
| Choosing Aspire testing vs browser-driven testing | [Aspire testing vs Playwright CLI](references/aspire-vs-playwright-testing.md) |

## Decision guide

| Goal | Default workflow |
| --- | --- |
| Create a new Aspire solution | `aspire new` |
| Add Aspire to an existing solution | `aspire init` -> wire AppHost -> `aspire run` |
| Set up AI coding agents | `aspire agent init` |
| Browse available Aspire docs | `aspire docs list` |
| Find official guidance for a feature or API | `aspire docs search <topic>` |
| Read the selected page or section | `aspire docs get <slug>` or `aspire docs get <slug> --section "<heading>"` |
| Look up docs through MCP when already connected | `list_docs`, `search_docs`, `get_doc` |
| Add an integration after confirming the supported pattern | `aspire add <name-or-id>` |
| Start in foreground | `aspire run` |
| Start in background | `aspire start` |
| Run multiple copies safely | `aspire run --isolated` or `aspire start --isolated` |
| Inspect resources and endpoints | `aspire describe` or MCP `list_resources` |
| Read logs and telemetry | `aspire logs`, `aspire otel`, or MCP log/trace tools |
| Wait for readiness in automation | `aspire wait <resource>` |
| Restart a single resource | `aspire resource <resource> restart` |
| Restore integrations or generated SDKs | `aspire restore` |
| Publish or deploy | `aspire publish`, `aspire deploy`, `aspire do ...` |

## Agentic development workflow

1. Run `aspire doctor` when the environment, certificates, container runtime, or SDK look suspect.
2. Read the AppHost source to understand resources, references, parameters, and startup order.
3. Run `aspire agent init` if the repo does not already have Aspire agent configuration.
4. Before editing the AppHost for an unfamiliar integration, custom command, or API:
   - use `aspire docs list` when the right page or slug is unclear
   - use `aspire docs search <topic>` and then `aspire docs get <slug>` to confirm the documented pattern
   - if Aspire MCP docs tools are already available, `list_docs`, `search_docs`, and `get_doc` are equivalent entry points to the same official docs
5. Start the app:
   - `aspire run` for an attached local debugging loop.
   - `aspire start --format Json` for background or delegated sessions.
   - Add `--isolated` when another worktree, agent, or test run may start the same AppHost.
6. Inspect runtime state with `aspire describe`, `aspire logs`, `aspire otel`, `aspire wait`, or MCP tools.
7. Apply code changes. For integrations or custom commands, use `aspire add <name-or-id>` or edit the AppHost only after docs confirm the supported pattern, then restart only the affected resource with `aspire resource <name> restart` when possible.
8. For UI validation, discover the live endpoint via Aspire, then load the `playwright-cli` skill to drive the browser.
9. Use telemetry to close the loop: build -> start -> inspect -> browser-check -> fix -> restart -> retest.

## Guardrails

- Do not guess topology from ad hoc scripts if an AppHost exists; read the AppHost source.
- Do not guess integration names, custom resource command shapes, or unfamiliar AppHost APIs; use `aspire docs search` and `aspire docs get` first.
- Use `aspire docs list` when the right page or slug is unclear.
- Prefer official `aspire.dev` docs surfaced through Aspire CLI or MCP over memory or third-party pages.
- If Aspire MCP docs tools are already available, treat `list_docs`, `search_docs`, and `get_doc` as first-class entry points to the same official docs.
- Do not hardcode ports; use `aspire describe` or MCP `list_resources`.
- Do not scrape the dashboard when CLI or MCP already exposes structured output.
- Do not make the agent babysit several long-running dev servers when Aspire can manage them as one AppHost.
- Use `--isolated` whenever two copies of the same AppHost may run at once.
- Use `--format Json` and `--non-interactive` for automation and agent-driven flows, and use `--section` when one part of a doc page is enough.
- Prefer AppHost parameters and Aspire user secrets over committing secrets to repo `.env` files.
- `aspire exec` is for running a new command in a resource context; it is not a log reader.
- If multiple AppHosts are running, pass `--apphost <path>` or work from the intended AppHost folder to avoid ambiguity.

## Version focus

Target the Aspire 13.2 command surface first.

- `aspire agent init` and `aspire agent mcp` replace the older `aspire mcp ...` naming.
- `aspire start` is the detached-friendly shorthand; `aspire run --detach` remains valid.
- `aspire docs list`, `aspire docs search`, and `aspire docs get` are the preferred docs lookup commands before unfamiliar AppHost edits.
- `list_docs`, `search_docs`, and `get_doc` expose the same official docs through Aspire MCP when configured.
- `aspire.config.json` is the preferred rooted config file; older `.aspire\settings.json` files may still appear during migration.
