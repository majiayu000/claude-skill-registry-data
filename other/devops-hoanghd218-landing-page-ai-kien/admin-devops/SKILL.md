---
name: admin-devops
description: |
  Infrastructure management using the device profile. Servers are stored in profile.servers[],
  deployments reference .env.local files via profile.deployments{}.

  Use when: managing server inventory, provisioning infrastructure, deploying to cloud providers.
license: MIT
---

# DevOps Administration

**Purpose**: Coordinate server provisioning and deployment across `admin-infra-*` and `admin-app-*` skills using the unified profile.

---

## Profile-First Approach

**Servers are in the profile, not a separate inventory file.**

```powershell
# PowerShell
. scripts/Load-Profile.ps1
Load-AdminProfile -Export
$AdminProfile.servers | Format-Table id, name, host, role, provider, status
```

```bash
# Bash
source scripts/load-profile.sh
load_admin_profile
jq '.servers[] | {id, name, host, role, provider, status}' "$ADMIN_PROFILE_PATH"
```

---

## Server Operations

### List All Servers

```powershell
Get-AdminServer | Format-Table
```

```bash
get_admin_server all ""
```

### Filter by Role

```powershell
Get-AdminServer -Role "coolify"
```

```bash
get_admin_server role "coolify"
```

### Filter by Provider

```powershell
Get-AdminServer -Provider "contabo"
```

```bash
get_admin_server provider "contabo"
```

### Get Specific Server

```powershell
Get-AdminServer -Id "cool-two"
```

```bash
get_admin_server id "cool-two"
```

---

## SSH to Server

Profile contains all SSH details:

```powershell
$server = Get-AdminServer -Id "cool-two"
ssh -i $server.keyPath -p $server.port "$($server.username)@$($server.host)"
```

```bash
ssh_to_server "cool-two"  # Helper from load-profile.sh
```

---

## Add New Server

### After Provisioning

```powershell
$AdminProfile.servers += @{
    id = "new-server"
    name = "NEW_SERVER"
    host = "192.168.1.100"
    port = 22
    username = "root"
    authMethod = "key"
    keyPath = "C:/Users/Owner/.ssh/id_rsa"
    provider = "hetzner"
    role = "coolify"
    domain = "example.com"
    status = "active"
    addedAt = (Get-Date).ToString("o")
    lastConnected = $null
    notes = "Provisioned via admin-infra-hetzner"
}

# Save
$AdminProfile | ConvertTo-Json -Depth 10 | Set-Content $AdminProfile.paths.deviceProfile
```

---

## Deployments

Deployments reference `.env.local` files containing provider credentials and config.

### List Deployments

```powershell
$AdminProfile.deployments.PSObject.Properties | ForEach-Object {
    [PSCustomObject]@{
        Name = $_.Name
        Type = $_.Value.type
        Provider = $_.Value.provider
        Status = $_.Value.status
        HasEnvFile = [bool]$_.Value.envFile
    }
}
```

### Load Deployment Config

```powershell
Load-AdminProfile -Deployment "vibeskills-oci" -Export
$DeploymentEnv  # Contains .env.local variables
```

```bash
load_admin_profile
load_deployment "vibeskills-oci"
# Variables exported to environment
```

### Add New Deployment

```powershell
$AdminProfile.deployments["my-new-deploy"] = @{
    envFile = "D:/projects/my-deploy/.env.local"
    type = "coolify"
    provider = "hetzner"
    status = "pending"
    serverIds = @("new-server")
    lastDeployed = $null
    notes = $null
}
```

---

## Provisioning Workflow

### Step 1: Choose Provider

| Provider | Skill | Notes |
|----------|-------|-------|
| OCI | `admin-infra-oci` | Free tier ARM |
| Hetzner | `admin-infra-hetzner` | Best price/perf |
| Contabo | `admin-infra-contabo` | Budget VPS |
| DigitalOcean | `admin-infra-digitalocean` | Simple |
| Vultr | `admin-infra-vultr` | Global |
| Linode | `admin-infra-linode` | Akamai |

### Step 2: Create .env.local

Copy template and fill provider section:

```bash
cp templates/env-template.env ./my-deploy/.env.local
# Edit with provider credentials
```

### Step 3: Register Deployment

```powershell
$AdminProfile.deployments["my-deploy"] = @{
    envFile = "D:/projects/my-deploy/.env.local"
    type = "coolify"
    provider = "hetzner"
    status = "pending"
    serverIds = @()
}
```

### Step 4: Run Infrastructure Skill

```
# Route to appropriate skill
admin-infra-hetzner → Provisions server
# Returns server details
```

### Step 5: Update Profile

```powershell
# Add server
$AdminProfile.servers += @{ ... }

# Link to deployment
$AdminProfile.deployments["my-deploy"].serverIds += "new-server-id"
$AdminProfile.deployments["my-deploy"].status = "active"

# Save
$AdminProfile | ConvertTo-Json -Depth 10 | Set-Content $AdminProfile.paths.deviceProfile
```

---

## Application Deployment

### After Infrastructure Ready

| App | Skill | Prerequisites |
|-----|-------|---------------|
| Coolify | `admin-app-coolify` | Server with Docker |
| KASM | `admin-app-kasm` | Server with Docker |

### Workflow

1. Load deployment: `Load-AdminProfile -Deployment "my-deploy" -Export`
2. Get server: `$server = Get-AdminServer -Id $DeploymentEnv.SERVER_ID`
3. SSH and deploy via `admin-app-*` skill

---

## Status Updates

```powershell
# Find server
$idx = $AdminProfile.servers.FindIndex({ param($s) $s.id -eq "cool-two" })

# Update status
$AdminProfile.servers[$idx].status = "stopped"
$AdminProfile.servers[$idx].lastConnected = (Get-Date).ToString("o")

# Save
$AdminProfile | ConvertTo-Json -Depth 10 | Set-Content $AdminProfile.paths.deviceProfile
```

---

## Routing Summary

| Task | Route To |
|------|----------|
| Provision OCI | `admin-infra-oci` |
| Provision Hetzner | `admin-infra-hetzner` |
| Provision others | `admin-infra-{provider}` |
| Install Coolify | `admin-app-coolify` |
| Install KASM | `admin-app-kasm` |
| Windows tasks | `admin-windows` |
| WSL tasks | `admin-wsl` |

---

## References

- `references/DEPLOYMENT_WORKFLOWS.md` - Detailed deployment steps
- `references/TROUBLESHOOTING.md` - Common issues
