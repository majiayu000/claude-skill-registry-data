---
name: admin-mcp
description: |
  MCP server management for Claude Desktop. Profile-aware - reads MCP server inventory
  from profile.mcp.servers{} and config path from profile.paths.claudeConfig.

  Use when: installing MCP servers, configuring Claude Desktop, troubleshooting MCP issues.
license: MIT
---

# MCP Server Management

**Requires**: Node.js 18+, Claude Desktop

---

## Profile-First Approach

MCP config and servers tracked in profile:

```powershell
# Config file location
$AdminProfile.mcp.configFile
# "C:/Users/Owner/AppData/Roaming/Claude/claude_desktop_config.json"

# Installed servers
$AdminProfile.mcp.servers | Format-Table
```

```bash
jq '.mcp' "$ADMIN_PROFILE_PATH"
```

---

## List MCP Servers

```powershell
$AdminProfile.mcp.servers.PSObject.Properties | ForEach-Object {
    [PSCustomObject]@{
        Name = $_.Name
        Package = $_.Value.package
        Status = $_.Value.status
        Tools = $_.Value.toolCount
    }
}
```

Example output:
```
Name      Package                     Status   Tools
----      -------                     ------   -----
win-cli   D:/mcp/win-cli-mcp-server   working  12
coolify   @pashvc/mcp-server-coolify  working  50
```

---

## Config File Location

From profile:

```powershell
$configPath = $AdminProfile.mcp.configFile
# Or
$configPath = $AdminProfile.paths.claudeConfig

# Read current config
$config = Get-Content $configPath | ConvertFrom-Json
$config.mcpServers
```

---

## Install New MCP Server

### Step 1: Backup Config

```powershell
$configPath = $AdminProfile.mcp.configFile
$backup = "$configPath.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
Copy-Item $configPath $backup
```

### Step 2: Add Server Entry

```powershell
$config = Get-Content $configPath | ConvertFrom-Json

# NPX pattern (most common)
$config.mcpServers | Add-Member -NotePropertyName "new-server" -NotePropertyValue @{
    command = "npx"
    args = @("-y", "@some/mcp-server")
}

# Save
$config | ConvertTo-Json -Depth 10 | Set-Content $configPath
```

### Step 3: Update Profile

```powershell
$AdminProfile.mcp.servers["new-server"] = @{
    name = "new-server"
    package = "@some/mcp-server"
    version = "1.0.0"
    command = "npx -y @some/mcp-server"
    configFile = $null
    environment = @{}
    status = "pending"
    toolCount = 0
    notes = "Just installed"
}

$AdminProfile | ConvertTo-Json -Depth 10 | Set-Content $AdminProfile.paths.deviceProfile
```

### Step 4: Restart Claude Desktop

Close and reopen Claude Desktop, then verify tools appear.

### Step 5: Update Status

```powershell
$AdminProfile.mcp.servers["new-server"].status = "working"
$AdminProfile.mcp.servers["new-server"].toolCount = 15  # Count from Claude
$AdminProfile | ConvertTo-Json -Depth 10 | Set-Content $AdminProfile.paths.deviceProfile
```

---

## Installation Patterns

### NPX (Recommended)

```json
{
  "command": "npx",
  "args": ["-y", "@package/mcp-server"]
}
```

### Global npm

```json
{
  "command": "mcp-server-name"
}
```
Requires: `npm install -g @package/mcp-server`

### Local Clone

```json
{
  "command": "node",
  "args": ["D:/mcp/server-name/dist/index.js"]
}
```

### With Environment Variables

```json
{
  "command": "npx",
  "args": ["-y", "@package/mcp-server"],
  "env": {
    "API_KEY": "your-key",
    "BASE_URL": "https://api.example.com"
  }
}
```

---

## Troubleshooting

### Check Profile for Issues

```powershell
# Known MCP issues
$AdminProfile.issues.current | Where-Object { $_.tool -like "*mcp*" }
```

### Common Problems

| Error | Cause | Fix |
|-------|-------|-----|
| `spawn ENOENT` | Command not found | Check path, install globally |
| `Server not starting` | Config syntax | Validate JSON |
| `Tools not appearing` | Didn't restart | Close/reopen Claude |
| `Permission denied` | Path issue | Use absolute Windows paths |

### Diagnostics

```powershell
# Check Node
node --version

# Check npm global
npm list -g --depth=0

# Validate config JSON
$configPath = $AdminProfile.mcp.configFile
try {
    Get-Content $configPath | ConvertFrom-Json | Out-Null
    Write-Host "Config JSON valid"
} catch {
    Write-Host "Config JSON invalid: $_"
}
```

---

## Track MCP Issue

```powershell
$AdminProfile.issues.current += @{
    id = "mcp-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    tool = "mcp-server-name"
    issue = "Server fails to start - spawn ENOENT"
    priority = "high"
    status = "pending"
    created = (Get-Date).ToString("o")
}

$AdminProfile | ConvertTo-Json -Depth 10 | Set-Content $AdminProfile.paths.deviceProfile
```

---

## Remove MCP Server

### From Claude Config

```powershell
$config = Get-Content $AdminProfile.mcp.configFile | ConvertFrom-Json
$config.mcpServers.PSObject.Properties.Remove("server-to-remove")
$config | ConvertTo-Json -Depth 10 | Set-Content $AdminProfile.mcp.configFile
```

### From Profile

```powershell
$AdminProfile.mcp.servers.PSObject.Properties.Remove("server-to-remove")
$AdminProfile | ConvertTo-Json -Depth 10 | Set-Content $AdminProfile.paths.deviceProfile
```

---

## References

- `references/INSTALLATION.md` - Detailed install patterns
- `references/CONFIGURATION.md` - Config file structure
- `references/TROUBLESHOOTING.md` - Common fixes
