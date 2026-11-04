---
name: affine
description: Search, read, and manage personal AFFiNE documents and workspaces. Available only in Pi's home browser profile.
---

# AFFiNE

Use the generated CLI through the shared bounded runner:

```sh
bash "$PI_CODING_AGENT_DIR/skills/affine/scripts/run.sh" <command> [flags]
```

Use `<command> --help` for a command's schema.
Prefer focused searches and reads rather than dumping entire workspaces.
The endpoint requires Tailscale connectivity to nixos-ry6a.
The runner decrypts the existing SOPS token in memory when needed; a YubiKey touch may be required.
Never print the token or write it to configuration.

Obtain confirmation for the exact mutation before creating, editing, or deleting documents.
After confirmation, set `MCP_WRITE_CONFIRMED=1` only for that runner process.
See `home-mcp` for shared output limits and mutation controls.

Refresh the generated wrapper from the repository:

```sh
nix run .#update-home-mcp-skills -- affine
nix run .#sync-agents
```
