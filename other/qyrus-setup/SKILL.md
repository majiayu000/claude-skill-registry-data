---
name: qyrus-setup
description: Set up Qyrus access and verify the available tools before testing.
---

# qyrus-setup

On the first Qyrus request, check which Qyrus MCP tools Claude can see. If available, use the guide and a read-only team lookup to confirm the connection and the user's access. On a host with terminal access, check the existing Qyrion client with `qyrion capabilities --json`. Confirm CLI credentials separately with `qyrion auth teams`. A capability listing alone only verifies the local client.

If Qyrus MCP is missing, first check whether the organization already offers an approved Qyrus connector. If available, help the user enable it and sign in to the correct tenant. If the organization wants the bundled local Qyrus MCP bridge for Cowork or Claude Code, give its Claude admin these steps:

1. Open [Qyrion Releases](https://github.com/QQyrus/qyrion/releases) and find the newest published Qyrion release, including prereleases. Under **Assets**, download `qyrusai-assure-<version>-claude.zip` matching that release. If that asset is missing, report the missing filename.
2. In Claude, open **Organization settings → Plugins & skills → Add → Upload a plugin**. Select the organization marketplace (or create one), choose the ZIP, and click **Upload**.
3. Make QyrusAI Assure available to the intended members. Have the user enable the organization plugin in Cowork or Claude Code and complete its setup. Recheck for the Qyrus tools and verify access with the read-only team lookup. For Claude web chat, use an approved remote connector.

If Qyrion is needed and missing, guide them through the [official Qyrion downloads](https://github.com/QQyrus/qyrion/releases). For an unconfigured CLI, have the user run `qyrion configure` in their own terminal and enter the tenant and credentials privately. Never ask for a key in chat or read a credential file. Recheck the missing capability and resume the original request. If the current host has no terminal, use available connector tools or explain which step needs a CLI-capable host.

Confirm the selected tenant and team before starting a test. Report which capability checks succeeded.
