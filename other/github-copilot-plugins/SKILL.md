---
name: github-copilot-plugins
description: >-
  Use for designing, creating, reviewing, or packaging GitHub Copilot and Agent Plugins for Visual Studio Code, including plugin.json, portable skills, MCP components, client-specific agents, commands, and hooks. Do not use for a single standalone skill, ordinary VS Code extensions, or installing an unreviewed plugin.
argument-hint: "[plugin capability, components, portability, distribution, and trust]"
---

# GitHub Copilot plugins

Plugins are preview functionality in VS Code and can bundle executable hooks
or MCP servers. Inspect the installed version and active plugin schema first.
Package only components that genuinely share installation,
versioning, trust, and lifecycle.

## Workflow

1. Define the bundle's user job, component graph, portability target, license,
   publisher, update path, executable behavior, and uninstall contract.
2. Prefer Agent Plugins 1.0 for portable skills and MCP servers: root
   `plugin.json`, `skills/`, and `mcp.json`.
3. Use a host-specific Copilot/Claude compatibility format only when agents,
   hooks, or slash commands are required and document the lost portability.
4. Validate every embedded skill, MCP server, hook, agent, command, reference,
   root token, version, and license independently before packaging.
5. Keep writable state under the format's data location; never write into the
   installed package or embed credentials.
6. Inspect the full package before separately authorized local installation.
   Test enable, disable, update, and uninstall without assuming trust persists.

## Rules

- Do not create a plugin merely to distribute one skill; a skill repository is simpler.
- Agent Plugins 1.0 portable components are skills and MCP servers. Treat
  agents, hooks, and slash commands as client-specific unless the active spec says otherwise.
- Plugin MCP servers can be trusted as part of installation; make that expansion visible.
- Never claim Microsoft/GitHub endorsement or copy vendor documentation/examples.
- Pin versions and retain third-party notices for any bundled material.

Read [plugin contracts](references/artifact-contracts.md), use [bundle patterns](references/patterns.md), and apply [verification](references/verification.md).

## Completion

The manifest and every component validate; portability claims match the chosen
format; executable trust and licenses are visible; no secrets/private authoring
material are bundled; and an approved VS Code smoke proves install, discovery,
disable, update behavior, and clean uninstall.
