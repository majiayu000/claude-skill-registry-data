---
name: bioresearcher-onboard
description: "Bootstraps a project-local biomcp MCP server runtime in .bioresearcher-runtime/: downloads portable Node.js 22 (if missing), vendors biomcp with fast mirror support (official or npmmirror), configures optional features (R, Biowasm, SQLite), and registers the server in OpenCode, Claude Code, Cursor, ZCode, Pi, CodeBuddy, or WorkBuddy. Use when biomcp is not installed, when biomedical tools are missing, or on requests like setup bioresearcher, install biomcp, or onboard."
license: Apache-2.0
compatibility: "Unix-like shells (Linux, macOS) and Windows (PowerShell, cmd.exe); OpenCode, Claude Code, Cursor, ZCode, Pi Coding Agent, CodeBuddy, WorkBuddy"
metadata:
  version: "1.1.1"
  source: "bioresearcher-skills"
allowed-tools: Bash Read Write Edit
---

# BioMCP Project-Local Onboarding

This skill sets up a self-contained, project-local BioMCP runtime in your
working directory under `.bioresearcher-runtime/`.

## What it does

- Checks if the host has Node.js >= 22.13. If missing, downloads a pinned,
  cryptographically verified portable Node.js LTS binary into
  `.bioresearcher-runtime/node/` (zero global installation, does not touch `~`
  or `/usr/local`).
- Auto-detects network conditions (official distribution vs. fast npmmirror in
  mainland China).
- Installs `biomcp` locally into `.bioresearcher-runtime/node_modules/` with
  sub-100ms startup latency and offline resilience.
- Configures optional features (R analysis, Biowasm genomics, SQLite database)
  and registers the server in your harness configuration (`opencode.json`,
  `.mcp.json`, etc.) without overwriting existing settings.
- Verifies the configuration using the built-in diagnostic doctor.

## Steps

Follow the steps below in order.

### Step 1: Run Stage 0 Bootstrap

Execute the bootstrap script corresponding to your operating system.

**For Unix-like shells (Linux, macOS, Git Bash):**

```bash
bash skills/bioresearcher-onboard/scripts/bootstrap.sh
```

**For Windows (PowerShell):**

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File skills\bioresearcher-onboard\scripts\bootstrap.ps1
```

The script automatically:
1. Reuses your host Node.js if version >= 22.13 is available.
2. If missing, downloads and verifies the official portable Node.js archive into
   `.bioresearcher-runtime/node/`.
3. Installs `biomcp@1.4.0` into `.bioresearcher-runtime/node_modules/`.
4. Updates your harness configuration (`opencode.json` or `.mcp.json`) with
   absolute executable paths.

### Step 2: Configure Optional Features (Optional)

By default, the core biomedical tools (PubMed/literature, clinical trials,
genes, variants, drugs, diseases, patents) and built-in SQLite are installed.

If the user needs specialized capabilities, pass the corresponding flags to the
bootstrap script or set environment variables before running:

- **R / Bioconductor Analysis** (DESeq2, edgeR, limma; requires ~2 GB RAM):
  Pass `--with-r` to install the `webr@0.6` peer dependency and enable R
  analysis in `.biomcp.json`.
- **Biowasm Analysis** (SAM/BAM/BED/BCF genomics tools):
  Pass `--with-biowasm` to enable Biowasm in `.biomcp.json`.
- **Local SQLite Database**:
  Pass `--sqlite-path=<path_to_db>` (e.g. `--sqlite-path=data/research.db`).
- **Client Override**:
  Pass `--client=opencode`, `--client=claude-code`, `--client=cursor`,
  `--client=zcode`, `--client=pi`, `--client=codebuddy`, or
  `--client=workbuddy` if auto-detection should be overridden.

Example with R analysis and SQLite enabled:

```bash
bash skills/bioresearcher-onboard/scripts/bootstrap.sh --with-r --sqlite-path=data/research.db
```

### Step 3: In-Session Feature Reconfiguration

Once BioMCP is registered and running, you do not need to hand-edit
configuration files. Use the built-in `biomcp_configure` tool to inspect or
adjust features dynamically:

- Inspect feature status:
  `biomcp_configure(action="status")`
- Enable or disable features:
  `biomcp_configure(action="set", values={"features.analysis_r.enabled": true})`
- Configure SQLite database:
  `biomcp_configure(action="set", values={"features.database.enabled": true, "features.database.type": "sqlite", "features.database.sqlite_path": "data/research.db"}, confirm_sensitive=true)`

### Step 4: Restart the Harness

MCP servers are spawned at client startup. Instruct the user to restart their
agent session or IDE to activate the newly connected BioMCP tools:

- **OpenCode**: Restart the session or open a new terminal session.
- **Claude Code**: Start a new session (`claude`).
- **Cursor / VS Code**: Reload the window or restart the application.
- **ZCode**: Reload the workspace or start a new ADE session.
- **Pi Coding Agent**: Start a new agent session (`pi`).
- **CodeBuddy**: Reload the window or restart the CLI session.
- **WorkBuddy**: Restart the application or switch workspace.

After restarting, verify connectivity by asking the agent to search for a gene
or article (e.g., `gene_search(query="BRAF")`).
