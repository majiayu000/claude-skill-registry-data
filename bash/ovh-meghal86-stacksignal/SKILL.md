---
name: ovh
version: 1.0.0
description: Manage OVHcloud services via API. Use when user asks about OVH domains, DNS records, VPS, cloud instances, dedicated servers, email, SSL certificates, or any OVH service management. Supports listing, creating, updating, and deleting resources.
---

# OVH

Manage OVHcloud services via the bundled `ovh-cli.py` script.

## Setup

Store credentials in environment:

```bash
export OVH_ENDPOINT="ovh-ca"  # or ovh-eu, ovh-us, etc.
export OVH_APP_KEY="your-app-key"
export OVH_APP_SECRET="your-app-secret"
export OVH_CONSUMER_KEY="your-consumer-key"
```

**Get credentials:**
1. Go to https://ca.api.ovh.com/createToken/ (or eu/us variant)
2. Create application with desired permissions
3. Validate the consumer key via the provided URL

**Endpoints:** `ovh-eu`, `ovh-ca`, `ovh-us`, `soyoustart-eu`, `soyoustart-ca`, `kimsufi-eu`, `kimsufi-ca`

## Usage

The script is at `scripts/ovh-cli.py`. Commands:

```bash
# Account info
ovh-cli.py me

# Domains
ovh-cli.py domains                      # List all domains
ovh-cli.py domain <domain>              # Get domain info
ovh-cli.py domain <domain> renew        # Check renewal info

# DNS (OVH-managed zones, not Cloudflare)
ovh-cli.py dns <domain>                 # List DNS records
ovh-cli.py dns <domain> get <id>        # Get specific record
ovh-cli.py dns <domain> create --type A --subdomain www --target 1.2.3.4 [--ttl 300]
ovh-cli.py dns <domain> update <id> --target 5.6.7.8
ovh-cli.py dns <domain> delete <id>
ovh-cli.py dns <domain> refresh         # Refresh zone (apply changes)

# VPS
ovh-cli.py vps                          # List all VPS
ovh-cli.py vps <name>                   # VPS details
ovh-cli.py vps <name> status            # Current state
ovh-cli.py vps <name> reboot            # Reboot VPS
ovh-cli.py vps <name> start             # Start VPS
ovh-cli.py vps <name> stop              # Stop VPS
ovh-cli.py vps <name> ips               # List IPs

# Cloud Projects
ovh-cli.py cloud                        # List projects
ovh-cli.py cloud <project> instances    # List instances
ovh-cli.py cloud <project> instance <id> # Instance details

# Dedicated Servers
ovh-cli.py dedicated                    # List servers
ovh-cli.py dedicated <name>             # Server details
ovh-cli.py dedicated <name> reboot      # Reboot server

# SSL Certificates
ovh-cli.py ssl                          # List certificates
ovh-cli.py ssl <id>                     # Certificate details

# Bills & Orders
ovh-cli.py bills [--limit N]            # Recent bills
ovh-cli.py orders [--limit N]           # Recent orders
```

## Common Patterns

**Check domain expiry:**
```bash
ovh-cli.py domain pushp.ovh renew
```

**Add DNS record:**
```bash
ovh-cli.py dns pushp.ovh create --type A --subdomain api --target 203.0.113.50
ovh-cli.py dns pushp.ovh refresh
```

**Manage VPS:**
```bash
ovh-cli.py vps myvps status
ovh-cli.py vps myvps reboot
```

## Notes

- DNS changes require `refresh` to apply
- Use `--json` flag for machine-readable output
- Some operations are async; check status with subsequent calls
