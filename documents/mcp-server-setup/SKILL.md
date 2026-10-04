---
name: mcp-server-setup
description: "Use when adding an stdio MCP server to Hermes Agent."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
---

# MCP Server Setup (Stdio Transport)

When adding an MCP server that uses a stdio command (e.g., `npx -y @automattic/mcp-wordpress-remote@latest`), follow these steps to ensure the server is properly configured and returns its tools.

## Steps

1. **Add the server** using `hermes mcp add` with `--command` and `--args`. Do **not** place environment variables inside the `--args` array.
   ```bash
   hermes mcp add <NAME> \
     --command npx \
     --args -y @automattic/mcp-wordpress-remote@latest \
     --env WP_API_URL=<URL> \
           WP_API_USERNAME=<USER> \
           WP_API_PASSWORD=<PASS>
   ```
   - The `--env` option (or equivalent `env:` block in `config.yaml`) injects the variables into the subprocess environment.
   - Placing `WP_API_URL=...` inside `--args` will be passed as an argument to the wrapped program, which typically ignores it, causing the MCP server to start without credentials and return zero tools.

2. **Enable** the server (if not automatically enabled).
   ```bash
   hermes config set mcp_servers.<NAME>.enabled true
   ```

3. **Test** the connection and verify tools are discovered.
   ```bash
   hermes mcp test <NAME>
   ```
   Expected output includes `✓ Tools discovered: N` where N > 0.

4. **(Optional)** List tools to confirm.
   ```bash
   hermes mcp configure <NAME>
   ```

## Pitfalls

- **Env in args yields zero tools** – If you mistakenly add `--env WP_API_URL=...` inside the `--args` list (e.g., `hermes mcp add ... --args -y @automattic/mcp-wordpress-remote@latest --env WP_API_URL=...`), the underlying wrapper receives it as an argument, does not set the environment variable, and the MCP server cannot authenticate. The connection succeeds but the tool list is empty.
- **Missing credentials** – Ensure the WordPress MCP plugin is active and the sandbox (`wp-content/novamira-sandbox/`) does not contain files that emit output (echo/print) before `<?php`, as this corrupts the JSON‑RPC stream and also results in zero tools.

## Verification

After successful setup, you should see the server listed with a tool count:

```bash
hermes mcp list
# Example output:
#  NAME                    TRANSPORT                      TOOLS        STATUS
#  ────────────────────── ────────────────────────────── ────────── ──────────
#  novamira-leejuan-com    npx -y @automattic/mcp-wordpress-remote@latest   all          ✓ enabled
```

## Related

- `hermes mcp add` – reference for adding MCP servers.
- `hermes config` – for enabling/modifying server settings.
- Novamira WordPress MCP specifics: see the `novamira-smartmillionaire` skill or the Novamira documentation.
