---
name: admin-unix
description: |
  Native macOS and Linux administration (non-WSL). Profile-aware - reads preferences
  from ~/.admin/profiles/{hostname}.json.

  Use when: macOS/Linux system admin, Homebrew (macOS), apt (Linux), services.
  NOT for WSL - use admin-wsl instead.
license: MIT
---

# Unix Administration (macOS + Linux)

**Requires**: macOS or native Linux (NOT WSL)

---

## Profile-First Approach

Profile location:

```bash
ADMIN_ROOT="${HOME}/.admin"
PROFILE_PATH="${ADMIN_ROOT}/profiles/$(hostname).json"
```

**Load profile:**

```bash
source /path/to/admin/scripts/load-profile.sh
load_admin_profile
show_admin_summary
```

---

## Platform Detection

```bash
OS=$(uname -s)
case "$OS" in
    Darwin) echo "macOS" ;;
    Linux)  
        if grep -qi microsoft /proc/version 2>/dev/null; then
            echo "WSL - use admin-wsl instead"
        else
            echo "Native Linux"
        fi
        ;;
esac
```

---

## Package Management (Profile-Aware)

### Check Preference

```bash
PKG_MGR=$(jq -r '.preferences.packages.manager' "$PROFILE_PATH")
```

### macOS (Homebrew)

```bash
# Install
brew install $package

# Update
brew upgrade $package

# List
brew list

# Search
brew search $package
```

### Linux (apt)

```bash
# Update index
sudo apt update

# Install
sudo apt install -y $package

# Upgrade all
sudo apt upgrade -y

# Search
apt search $package
```

---

## Python Commands (Profile-Aware)

```bash
PY_MGR=$(get_preferred_manager python)

case "$PY_MGR" in
    uv)     uv pip install "$package" ;;
    pip)    pip3 install "$package" ;;
    conda)  conda install "$package" ;;
esac
```

---

## Node Commands (Profile-Aware)

```bash
NODE_MGR=$(get_preferred_manager node)

case "$NODE_MGR" in
    npm)    npm install "$package" ;;
    pnpm)   pnpm add "$package" ;;
    yarn)   yarn add "$package" ;;
    bun)    bun add "$package" ;;
esac
```

---

## Services

### Linux (systemd)

```bash
# Status
sudo systemctl status $service

# Start/Stop/Restart
sudo systemctl start $service
sudo systemctl stop $service
sudo systemctl restart $service

# Enable/Disable on boot
sudo systemctl enable $service
sudo systemctl disable $service

# View logs
journalctl -u $service -f
```

### macOS (Homebrew services)

```bash
# List
brew services list

# Start/Stop
brew services start $service
brew services stop $service
brew services restart $service
```

---

## SSH to Servers

Use profile server data:

```bash
ssh_to_server "cool-two"  # Helper from load-profile.sh
```

Or manually:

```bash
SERVER=$(jq '.servers[] | select(.id == "cool-two")' "$PROFILE_PATH")
HOST=$(echo "$SERVER" | jq -r '.host')
USER=$(echo "$SERVER" | jq -r '.username')
KEY=$(echo "$SERVER" | jq -r '.keyPath')

ssh -i "$KEY" "$USER@$HOST"
```

---

## Update Profile

After installing a tool:

```bash
PROFILE=$(cat "$PROFILE_PATH")
PROFILE=$(echo "$PROFILE" | jq --arg ver "$(python3 --version | cut -d' ' -f2)" \
    '.tools.python.version = $ver | .tools.python.present = true')
echo "$PROFILE" | jq . > "$PROFILE_PATH"
```

---

## Capabilities Check

```bash
has_capability "hasDocker" && docker info
has_capability "hasGit" && git --version
```

---

## Scope Boundaries

| Task | Handle Here | Route To |
|------|-------------|----------|
| Homebrew (macOS) | ✅ | - |
| apt (Linux) | ✅ | - |
| systemd services | ✅ | - |
| Python/Node | ✅ | - |
| WSL operations | ❌ | admin-wsl |
| Windows operations | ❌ | admin-windows |
| Server provisioning | ❌ | admin-devops |

---

## References

- `references/OPERATIONS.md` - Common operations, troubleshooting
