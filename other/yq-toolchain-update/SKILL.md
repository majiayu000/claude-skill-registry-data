---
name: yq-toolchain-update
description: Audit or update this Windows computer's fixed third-party Codex helper toolchain when the user requests local helper-tool maintenance. Always show the complete registered list and obtain confirmation for each update group; exclude Codex itself and general runtimes unless explicitly added.
---

# YQ Toolchain Update

Maintain the fixed local helper-tool list in [tool-registry.json](references/tool-registry.json). This Skill manages ordinary third-party command-line tools; use `skill-lifecycle-manager` separately for Skills' own sources, installs, and upgrades.

## Required first response

Run `scripts/toolchain-audit.ps1 -Mode Inventory` before any update. Show the user the complete table of every selected tool, not only a count. Include its group, installed/not-installed state, observed version output, update source, and a short plain-language reason for the recommended order.

The registry is the single source of truth for the fixed list and its three groups: collaboration and cloud; browser, MCP, and search; content platforms. Show exact tool names only from the inventory output, so the entrypoint does not become a stale second copy.

Do not add Codex, Node, Python, Git, Docker, Bun, pnpm, uv, or other general runtimes unless the user explicitly asks.

## Confirmation gates

1. After showing the complete list and current state, get explicit approval for group 1.
2. Before a group, show the full list for that group, available stable updates, and likely effect in non-technical language.
3. Update one tool at a time with its source-native method from the registry. Verify its version and basic command before starting the next tool.
4. At the end of a group, show a complete result table: updated, already current, skipped, or blocked. Stop and get explicit approval before the next group.
5. Stop immediately for interactive login, authorization, configuration migration, or a failed validation. State exactly what needs the user's decision; never silently skip it or continue to another group.

Use stable releases only. Never run unbounded bulk updates such as a bare `npm update -g` or `winget upgrade --all`.

## Safe update rules

- Verify the official source and current stable version immediately before an update. Record the old and new version.
- Preserve existing credentials, cookies, profiles, and user configuration. Do not print their contents.
- Use package-manager readback plus a non-authenticated `--version` or `--help` check after each change.
- If a PowerShell function or alias has the same name as a registry executable, report the conflict and use the verified application path for the probe. Do not run a shadowing function as if it were the registered tool.
- For Playwright, update only the browser engines already installed unless the user asks for another browser. Do not alter the user's Chrome profile or login state.
- Agent Reach can route to other tools but does not own their installations. Update its integrations as separate registry entries.
- For LinkedIn, first search active Codex/Claude MCP configuration paths without printing secrets. Only replace a legacy server command after finding a real reference and receiving confirmation. If none is active, install and validate `mcp-server-linkedin`, leave the legacy command as a rollback path, and do not create a new MCP configuration.

## Reporting

Keep reports simple. List every requested tool by name, including ones already current. Separate observed facts from unverified account health. End a completed three-group run by asking whether the user wants the registry or this Skill changed; do not change either automatically.
