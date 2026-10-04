---
name: jlceda-mcp-automation
description: Use when installing, activating, launching, documenting, or wiring JLCEDA/LCEDA Pro with MCP bridge automation for PCB design agents, including local Electron CDP launch, private activation handling, jlc-bridge extension setup, gateway checks, and MCP tools/list or pcb_ping validation.
---

# JLCEDA MCP Automation

Use this skill when an agent needs to prepare JLCEDA/LCEDA Pro for PCB automation through MCP. Keep EDA activation files, license text, browser state, and user project data out of git.

For JLC/JLCEDA website browsing and downloads on Lachlan's workstation, reuse
the shared Chrome profile `$HOME/.cache/xyq-chrome` through noVNC `6099`
(display `:98`, VNC `5908`, CDP `9344`). This is also the Xiaoyunque and general
download browser. Do not confuse it with LCEDA Pro's separate Electron
application profile or replace it with a newly created Chrome profile.

## Safety Rules

- Never print, summarize, or commit activation file contents. Only report path, size, hash prefix if useful, and success/failure.
- Keep downloaded LCEDA archives, extracted apps, cloned MCP repos, `node_modules`, and app profiles outside project git unless the user explicitly asks to vendor them.
- Treat MCP PCB edits as live design changes. Run a read-only smoke test before edit tools, and confirm the active project/document before moving components or routing.
- Document dependency audit warnings from third-party MCP repos instead of silently ignoring them.

## AgenticApp Tooling

When working in AgenticApp, prefer the maintained local tool:

```bash
agentic_tools/jlceda_mcp_agent/scripts/install_lceda_pro_local.sh \
  ~/Downloads/lceda-pro-linux-x64-3.2.149.zip
agentic_tools/jlceda_mcp_agent/scripts/launch_lceda_pro.sh --restart --port 51370
python3 agentic_tools/jlceda_mcp_agent/scripts/lceda_cdp.py status --port 51370
```

If the user supplies an activation file, apply it without exposing content:

```bash
python3 -m pip install -r agentic_tools/jlceda_mcp_agent/requirements.txt
python3 agentic_tools/jlceda_mcp_agent/scripts/lceda_cdp.py activate \
  --port 51370 --file ~/Downloads/lceda-pro-activation.txt
```

Install the preferred MCP server and LCEDA bridge package:

```bash
agentic_tools/jlceda_mcp_agent/scripts/install_jlcmcp.sh
```

This clones `hyl64/jlcmcp` to `~/.local/share/appautoaction/mcp/jlcmcp`, builds
`dist/index.js`, builds `jlc-bridge/build/jlc-bridge.eext`, and writes a
`tools/list` smoke output to `/tmp/jlcmcp-tools-list.jsonl`.

## MCP Choice

- Prefer `hyl64/jlcmcp` for direct PCB manipulation: state, screenshots, DRC, component moves, routing, vias, copper, keepouts, silkscreen, differential pairs, equal-length groups, schematic reads, and calculators.
- Consider `sengbin/JLCEDA-MCP` when the workflow is VS Code/Cursor centered.
- Treat `Spectoda/easyeda-mcp` as an architecture reference unless it has matured for the target task.

## Bridge Wiring

Add an MCP entry like:

```json
{
  "mcpServers": {
    "jlceda": {
      "command": "node",
      "args": ["$HOME/.local/share/appautoaction/mcp/jlcmcp/dist/index.js"],
      "env": {
        "GATEWAY_WS_URL": "ws://127.0.0.1:18800/ws/bridge"
      }
    }
  }
}
```

Real editing requires two more live pieces: install `jlc-bridge.eext` in LCEDA
Pro's extension manager, and run the gateway that accepts bridge WebSocket
connections on port `18800`. `tools/list` only proves the MCP server works;
`pcb_ping` proves the LCEDA bridge path works.

## Validation

Report these before claiming completion:

- LCEDA app version and CDP target title/URL.
- MCP repository and commit used.
- `npm run build` results for server and bridge.
- `tools/list` smoke-test result and tool count.
- Bridge status: not installed, installed but gateway missing, or `pcb_ping` OK.
- Any unresolved audit warnings or manual extension-manager steps.
