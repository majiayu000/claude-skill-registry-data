---
name: hcloud
description: Manage Hetzner Cloud infrastructure using the hcloud CLI. Use when working with Hetzner servers, firewalls, networks, volumes, load balancers, or any Hetzner Cloud resources. Supports server management (create/delete/start/stop), firewall configuration, SSH key management, volume operations, and infrastructure monitoring.
---

# Hetzner Cloud CLI (hcloud)

Manage Hetzner Cloud infrastructure with the official CLI tool.

## Prerequisites

**Installation** (if not already installed):
```bash
# Detect architecture
ARCH=$(uname -m)
if [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
  URL="https://github.com/hetznercloud/cli/releases/latest/download/hcloud-linux-arm64.tar.gz"
else
  URL="https://github.com/hetznercloud/cli/releases/latest/download/hcloud-linux-amd64.tar.gz"
fi

# Install
cd /tmp
wget -q "$URL"
tar xzf hcloud-linux-*.tar.gz
sudo mv hcloud /usr/local/bin/
chmod +x /usr/local/bin/hcloud
```

**Configuration** (first time):
```bash
mkdir -p ~/.config/hcloud
cat > ~/.config/hcloud/cli.toml <<EOF
active_context = "default"

[[contexts]]
name = "default"
token = "YOUR_HETZNER_API_TOKEN"
EOF
chmod 600 ~/.config/hcloud/cli.toml
```

**Verify**:
```bash
hcloud version
hcloud server list
```

## Common Commands

### Servers

```bash
# List servers
hcloud server list

# Get server details
hcloud server describe <name-or-id>

# Create server
hcloud server create \
  --name my-server \
  --type cx11 \
  --image ubuntu-24.04 \
  --ssh-key <key-id-or-name> \
  --location nbg1

# Start/stop/reboot
hcloud server start <name-or-id>
hcloud server stop <name-or-id>
hcloud server reboot <name-or-id>

# Delete server
hcloud server delete <name-or-id>

# SSH into server
hcloud server ssh <name-or-id>

# Run command on server
hcloud server ssh <name-or-id> -- 'uname -a'
```

### Firewalls

```bash
# List firewalls
hcloud firewall list

# Get firewall details
hcloud firewall describe <name-or-id>

# Create firewall
hcloud firewall create \
  --name my-firewall \
  --rules-file rules.json

# Add rule to firewall
hcloud firewall add-rule <name-or-id> \
  --direction in \
  --port 22 \
  --protocol tcp \
  --source-ips 0.0.0.0/0 \
  --source-ips ::/0 \
  --description "SSH"

# Apply firewall to server
hcloud firewall apply-to-resource <firewall-name> \
  --type server \
  --server <server-name-or-id>

# Remove firewall from server
hcloud firewall remove-from-resource <firewall-name> \
  --type server \
  --server <server-name-or-id>

# Delete firewall
hcloud firewall delete <name-or-id>
```

### SSH Keys

```bash
# List SSH keys
hcloud ssh-key list

# Add SSH key
hcloud ssh-key create \
  --name my-key \
  --public-key-from-file ~/.ssh/id_ed25519.pub

# Delete SSH key
hcloud ssh-key delete <name-or-id>
```

### Server Types & Images

```bash
# List available server types
hcloud server-type list

# List available images
hcloud image list
hcloud image list --type system  # Only system images

# List locations
hcloud location list
```

### Volumes

```bash
# List volumes
hcloud volume list

# Create volume
hcloud volume create \
  --name my-volume \
  --size 10 \
  --location nbg1

# Attach volume to server
hcloud volume attach <volume-name> <server-name>

# Detach volume
hcloud volume detach <volume-name>

# Delete volume
hcloud volume delete <volume-name>
```

### Networks

```bash
# List networks
hcloud network list

# Create network
hcloud network create \
  --name my-network \
  --ip-range 10.0.0.0/16

# Add subnet
hcloud network add-subnet <network-name> \
  --type cloud \
  --network-zone eu-central \
  --ip-range 10.0.1.0/24

# Attach server to network
hcloud server attach-to-network <server-name> \
  --network <network-name>
```

### Load Balancers

```bash
# List load balancers
hcloud load-balancer list

# Create load balancer
hcloud load-balancer create \
  --name my-lb \
  --type lb11 \
  --location nbg1

# Add target (server)
hcloud load-balancer add-target <lb-name> \
  --server <server-name>

# Add service
hcloud load-balancer add-service <lb-name> \
  --protocol http \
  --listen-port 80 \
  --destination-port 80
```

## Firewall Rules Format

For complex firewall rules, use JSON:

```json
[
  {
    "direction": "in",
    "port": "22",
    "protocol": "tcp",
    "source_ips": ["0.0.0.0/0", "::/0"],
    "description": "SSH"
  },
  {
    "direction": "in",
    "port": "80",
    "protocol": "tcp",
    "source_ips": ["0.0.0.0/0", "::/0"],
    "description": "HTTP"
  },
  {
    "direction": "in",
    "port": "443",
    "protocol": "tcp",
    "source_ips": ["0.0.0.0/0", "::/0"],
    "description": "HTTPS"
  },
  {
    "direction": "in",
    "protocol": "icmp",
    "source_ips": ["0.0.0.0/0", "::/0"],
    "description": "ICMP (ping)"
  }
]
```

## Common Server Types

| Type  | vCPU | RAM   | Disk   | Price/mo (approx) |
|-------|------|-------|--------|-------------------|
| cx11  | 1    | 2 GB  | 20 GB  | €4                |
| cx21  | 2    | 4 GB  | 40 GB  | €6                |
| cx22  | 2    | 4 GB  | 40 GB  | €6 (deprecated)   |
| cx23  | 2    | 4 GB  | 40 GB  | €3                |
| cx31  | 2    | 8 GB  | 80 GB  | €10               |
| cx33  | 4    | 8 GB  | 80 GB  | €5                |
| cpx11 | 2    | 2 GB  | 40 GB  | €5                |
| cpx21 | 3    | 4 GB  | 80 GB  | €10               |
| cpx31 | 4    | 8 GB  | 160 GB | €18               |

**cx series**: Shared vCPU (cost-optimized)  
**cpx series**: Dedicated vCPU (performance-optimized)

## Tips

- **Use `--output json`** for parsing: `hcloud server list --output json | jq`
- **Context switching**: Create multiple contexts in `~/.config/hcloud/cli.toml` for different projects/accounts
- **Server labels**: Use labels for organization: `--labels environment=production,project=web`
- **Default location**: Set default location to avoid specifying: `hcloud context config default-location nbg1`
- **Dry run**: Many commands support `--dry-run` or `--validate` flags

## Documentation

Official docs: https://docs.hetzner.cloud/
GitHub: https://github.com/hetznercloud/cli
