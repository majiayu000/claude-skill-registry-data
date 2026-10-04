---
name: qa-argus-setup
section: pipeline
description: "Argus QA first-run setup wizard; configures MCP, app settings, and Azure DevOps credentials"
model: haiku
---

# Argus QA Setup Wizard

Initialize Argus QA for your project. Run once per project:

```
/qa-argus-setup
```

---

## Setup Phases

### Phase 1: Playwright MCP Configuration (CRITICAL — AUTO-INSTALL)

**Goal:** Enable fast browser operations via Playwright MCP instead of slow Bash fallback.

**Policy (updated 2026-06-03):** AUTO-INSTALL without asking the user. Match `qa-preflight` behavior. Playwright MCP is a known-required dependency; asking Y/N adds friction for zero benefit. The only acceptable user prompt for install is when the install itself fails (permission, network, disk).

1. Check if `@playwright/mcp` is installed globally:
   ```bash
   npm list -g @playwright/mcp
   ```

2. If NOT found, AUTO-INSTALL silently (no Y/N prompt). Log and run:
   ```
   ⚠ Playwright MCP not detected — auto-installing (one-time, ~90 seconds)...
   ```
   ```bash
   npm install -g @playwright/mcp@latest               # ~30s
   npx playwright install chromium firefox webkit      # ~60s, browser binaries
   ```
   On failure: log the exact stderr and HARD STOP with a clear fix-it message ("Run as Administrator on Windows" / "Use sudo on Linux/Mac" / "Check disk space").

3. **Check if MCP is configured in Claude Code settings:**
   - Prefer `~/.claude/settings.local.json` (local override, better)
   - Fallback to `~/.claude/settings.json` (global)
   - Look for `mcpServers.playwright` entry
   
4. **If NOT configured, auto-register it (no prompt):**
   
   Run:
   ```bash
   claude mcp add playwright -- npx "@playwright/mcp@latest"
   ```
   
   Or write directly to `~/.claude/settings.local.json` if the CLI is unavailable:
   ```json
   {
     "mcpServers": {
       "playwright": {
         "command": "npx",
         "args": ["@playwright/mcp@latest", "--isolated"]
       }
     }
   }
   ```
   
   Then print:
   ```
   ✓ Playwright MCP installed and registered
   ⏸ Restart Claude Code to load the MCP server, then re-run your audit.
   ```
   
   This is a friendly HARD STOP — Claude Code only picks up MCP servers at startup. The user understands they're 60 seconds away from a working audit.

5. **If already configured:**
   ```
   ✓ Playwright MCP already configured — skipping install
   ```

---

### Phase 2: Application Configuration

Ask the user for their app details:

```
What is your app's base URL?
  (e.g., https://ui-dev.undertakings.dobusiness.dev)
  URL: _______

What is your app's login route?
  (e.g., /auth/login or /login)
  Route: _______

Public-only audit, or include auth-gated routes?
  (1) Public pages only
  (2) Public + authenticated routes
  Choice: _
```

Write to `{project-root}/.claude/automation.config.json`:

```json
{
  "apps": [
    {
      "name": "undertakings",
      "baseUrl": "https://ui-dev.undertakings.dobusiness.dev",
      "auth": {
        "loginRoute": "/auth/login",
        "requiresAuth": false
      }
    }
  ],
  "ado": {
    "org": "https://dev.azure.com/YOUR_ORG",
    "project": "YOUR_PROJECT",
    "areaPath": "YOUR_AREA_PATH"
  },
  "responsiveness": {
    "headless": false,
    "viewports": [
      { "name": "iPhone 12", "width": 390, "height": 844, "class": "mobile" },
      { "name": "iPad Air", "width": 820, "height": 1180, "class": "tablet" },
      { "name": "Desktop 1440", "width": 1440, "height": 900, "class": "desktop" }
    ]
  },
  "crossBrowser": {
    "enabled": true
  }
}
```

---

### Phase 3: Azure DevOps Configuration (Optional)

Ask if user wants to file real ADO bugs:

```
File bugs to Azure DevOps? (Y/N default=N)
  Y = file real tickets (requires PAT + ADO org configured)
  N = dry-run mode (detect issues, no tickets filed)
```

If Y, collect:
```
Azure DevOps organization:
  (URL format: https://dev.azure.com/YOUR_ORG)
  Organization: _______

Azure DevOps project:
  (e.g., DoWeb, MyProject)
  Project: _______

Area Path:
  (e.g., DoWeb\QA, Team\QA)
  Path: _______

Personal Access Token (PAT):
  (will be stored in .claude/secrets.json, gitignored)
  PAT: _______
```

Write to `{project-root}/.claude/secrets.json` (gitignored):
```json
{
  "AZURE_DEVOPS_PAT": "YOUR_PAT_HERE"
}
```

---

### Phase 4: Preflight Validation

Run preflight checks:
```bash
node --version
npx playwright --version
curl -sf {BASE_URL}
```

Print summary:
```
═══════════════════════════════════════
 ✓ Setup Complete
═══════════════════════════════════════
 ✓ Playwright MCP:        configured
 ✓ App:                   undertakings
 ✓ Base URL:              reachable (200)
 ✓ Azure DevOps:          dry-run mode (change in customize.toml)
 
 Ready to audit!
 
 Next: /qa-argus
         or: /qa-argus audit undertaking
```

---

## Safety Rules

- Never auto-install without explicit confirmation
- Never write PATs to `automation.config.json`
- Store secrets only in `.claude/secrets.json`
- Always gitignore `.claude/secrets.json`
- Preserve existing config when re-running setup
