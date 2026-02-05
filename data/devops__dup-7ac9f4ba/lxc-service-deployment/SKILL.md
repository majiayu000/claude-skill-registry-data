---
name: lxc-service-deployment
description: Standardized deployment procedure for services in LXC containers on the Proxmox HA cluster. Use when deploying a new service, creating LXC containers, configuring DHCP reservations (Kea), DNS rewrites (AdGuard), reverse proxy routes (Traefik), or integrating with monitoring (Uptime Kuma) and dashboard (Homepage). Triggers on phrases like "deploy a new service", "create container for", "set up DHCP", "add Traefik route", "configure DNS rewrite", or any homelab infrastructure deployment.
---

# LXC Service Deployment Skill

Deploy services to the Proxmox HA cluster with full infrastructure integration.

## Infrastructure Inventory

Update these values if infrastructure changes. IPs are used for core infrastructure (DNS may be unavailable during configuration). DNS names are used for validation and service access.

```bash
# === CORE INFRASTRUCTURE (use IPs - DNS may not be available) ===
PROXMOX_NODES=("192.168.1.137" "192.168.1.125" "192.168.1.126")
KEA_PRIMARY="192.168.1.133"
KEA_SECONDARY="192.168.1.134"
ADGUARD_PRIMARY="192.168.1.253"
ADGUARD_SECONDARY="192.168.1.224"
TRAEFIK_IP="192.168.1.110"
HOMEPAGE_IP="192.168.1.45"

# === SERVICE ACCESS (use DNS after deployment) ===
TRAEFIK_DASHBOARD="https://traefik.internal.lakehouse.wtf"
UPTIME_KUMA="https://uptime.internal.lakehouse.wtf"
DOMAIN_SUFFIX="internal.lakehouse.wtf"

# === CONFIGURATION PATHS ===
KEA_CONFIG="/etc/kea/kea-dhcp4.conf"
ADGUARD_CONFIG="/opt/AdGuardHome/AdGuardHome.yaml"
TRAEFIK_ROUTERS="/etc/traefik/dynamic/routers.yml"
TRAEFIK_SERVICES="/etc/traefik/dynamic/services.yml"
HOMEPAGE_CONFIG="/home/homepage/homepage/config/services.yaml"
```

## Quick Reference

| Component | Primary | Secondary | Config Path |
|-----------|---------|-----------|-------------|
| **Proxmox** | .137 | .125, .126 | - |
| **Kea DHCP** | .133 | .134 | `/etc/kea/kea-dhcp4.conf` |
| **AdGuard DNS** | .253 | .224 | `/opt/AdGuardHome/AdGuardHome.yaml` |
| **Traefik** | .110 | - | `/etc/traefik/dynamic/*.yml` |
| **Uptime Kuma** | .132 | - | Web UI |
| **Homepage** | .45 | - | `/home/homepage/homepage/config/services.yaml` |

**Domain Pattern:** `<service>.internal.lakehouse.wtf` → Traefik → Backend

## DNS Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ External DNS (Cloudflare)                                   │
│   *.lakehouse.wtf → Cloudflare (tunnel/proxy)              │
│   *.internal.lakehouse.wtf → Cloudflare (needs override!)  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Internal DNS (AdGuard Rewrite) - OVERRIDES Cloudflare       │
│   service.internal.lakehouse.wtf → Traefik IP              │
│   (Per-service rewrites for flexibility with standalone HW) │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Traefik Reverse Proxy                                       │
│   Routes by Host header → Backend service IP:PORT           │
│   TLS termination with Cloudflare wildcard cert            │
└─────────────────────────────────────────────────────────────┘
```

**Why per-service DNS rewrites (not wildcard):**
- Allows pointing some services directly to standalone hardware, bypassing Traefik
- More explicit control over what resolves internally
- Flexibility for non-HTTP services or services with their own TLS

## Deployment Workflow

### Phase 1: Planning

Gather this information before starting:

| Field | Value | Notes |
|-------|-------|-------|
| Service name | | Lowercase, hyphenated (e.g., `my-service`) |
| LXC ID | | Check availability across cluster |
| Target IP | | Verify not in use |
| Service port | | Check app documentation |
| Health check path | | Usually `/`, `/health`, or `/api/health` |
| CPU cores | | Default: 2 |
| RAM (MB) | | Default: 2048 |
| Disk (GB) | | Default: 20 |

**Verify availability:**
```bash
SERVICE="my-service"
IP="192.168.1.XXX"
LXC_ID="XXX"

# Check IP not in use
ping -c 2 $IP

# Check LXC ID available across cluster
for node in "${PROXMOX_NODES[@]}"; do
  ssh root@$node "pct list | grep -w $LXC_ID" && echo "⚠️  ID $LXC_ID in use on $node"
done
```

### Phase 2: Container Creation

```bash
NODE="${PROXMOX_NODES[0]}"  # Or select based on resource availability
LXC_ID="XXX"
HOSTNAME="service-name"
IP="192.168.1.XXX"

# Create container (Debian 12)
ssh root@$NODE "pct create $LXC_ID local:vztmpl/debian-12-standard_12.7-1_amd64.tar.zst \
  --hostname $HOSTNAME \
  --memory 2048 --cores 2 --rootfs local-lvm:20 \
  --net0 name=eth0,bridge=vmbr0,ip=$IP/24,gw=192.168.1.1 \
  --onboot 1 --unprivileged 1"

ssh root@$NODE "pct start $LXC_ID"

# Get MAC address (needed for DHCP)
MAC=$(ssh root@$NODE "pct config $LXC_ID | grep hwaddr | awk '{print \$2}'")
echo "MAC Address: $MAC"
```

### Phase 3: DHCP Reservation (Kea)

**⚠️ Both servers must be updated for HA failover:**

```bash
SERVICE="service-name"
IP="192.168.1.XXX"
MAC="XX:XX:XX:XX:XX:XX"

# Backup configs on both servers
ssh root@$KEA_PRIMARY "cp $KEA_CONFIG ${KEA_CONFIG}.backup-$(date +%Y%m%d)"
ssh root@$KEA_SECONDARY "cp $KEA_CONFIG ${KEA_CONFIG}.backup-$(date +%Y%m%d)"

# Add reservation to primary (edit the 192.168.1.0/24 subnet's reservations array)
# Format: {"hw-address": "$MAC", "ip-address": "$IP", "hostname": "$SERVICE"}

# Copy config to secondary
scp root@$KEA_PRIMARY:$KEA_CONFIG /tmp/kea-dhcp4.conf
scp /tmp/kea-dhcp4.conf root@$KEA_SECONDARY:$KEA_CONFIG

# Reload both servers
ssh root@$KEA_PRIMARY "systemctl reload isc-kea-dhcp4-server"
ssh root@$KEA_SECONDARY "systemctl reload isc-kea-dhcp4-server"

# Verify
ssh root@$KEA_PRIMARY "grep -A2 '$MAC' $KEA_CONFIG"
```

### Phase 4: DNS Rewrite (AdGuard)

**⚠️ Both servers must be updated for HA failover:**

```bash
SERVICE="service-name"
DOMAIN="${SERVICE}.${DOMAIN_SUFFIX}"

# Backup and add rewrite to BOTH AdGuard servers
for AG in $ADGUARD_PRIMARY $ADGUARD_SECONDARY; do
  ssh root@$AG "cp $ADGUARD_CONFIG ${ADGUARD_CONFIG}.backup-$(date +%Y%m%d)"
  
  # Add rewrite entry (append to rewrites section)
  ssh root@$AG "cat >> $ADGUARD_CONFIG << EOF
  - domain: $DOMAIN
    answer: $TRAEFIK_IP
EOF"
  
  ssh root@$AG "systemctl restart AdGuardHome"
done

# Verify DNS resolution (should return Traefik IP)
echo "Testing DNS resolution..."
dig +short $DOMAIN @$ADGUARD_PRIMARY
dig +short $DOMAIN @$ADGUARD_SECONDARY
```

**Note on standalone hardware:** If deploying to hardware outside Proxmox that should bypass Traefik, point the DNS rewrite directly to the hardware IP instead of Traefik.

### Phase 5: Traefik Configuration

**Add router to `$TRAEFIK_ROUTERS`:**

```yaml
    service-name-router:
      rule: "Host(`service-name.internal.lakehouse.wtf`)"
      entryPoints:
        - websecure
      service: service-name-service
      tls:
        certResolver: cloudflare
```

**Add service to `$TRAEFIK_SERVICES`:**

```yaml
    service-name-service:
      loadBalancer:
        servers:
          - url: "http://192.168.1.XXX:PORT"
        healthCheck:
          path: /health
          interval: 30s
          timeout: 5s
```

```bash
# Apply changes
ssh root@$TRAEFIK_IP "systemctl reload traefik"

# Verify via API (uses DNS - confirms full chain works)
curl -sk "$TRAEFIK_DASHBOARD/api/http/routers" | grep -q "service-name" && echo "✅ Router configured"
curl -sk "$TRAEFIK_DASHBOARD/api/http/services" | grep -q "service-name" && echo "✅ Service configured"
```

### Phase 6: Monitoring & Dashboard

**Uptime Kuma** (access via $UPTIME_KUMA):
1. Add New Monitor
2. Type: HTTP(s)
3. URL: `https://service-name.internal.lakehouse.wtf`
4. Interval: 60s
5. Expected status: 200 (or 302 if redirects)

**Homepage** (edit on $HOMEPAGE_IP):
```bash
ssh root@$HOMEPAGE_IP "cat >> $HOMEPAGE_CONFIG << 'EOF'
- Service Name:
    icon: service-icon
    href: https://service-name.internal.lakehouse.wtf
    description: Service description
EOF"
```

### Phase 7: Validation Checklist

Run all checks - all should pass before marking deployment complete:

```bash
SERVICE="service-name"
IP="192.168.1.XXX"
PORT="XXXX"
MAC="XX:XX:XX:XX:XX:XX"
DOMAIN="${SERVICE}.${DOMAIN_SUFFIX}"

echo "=== Deployment Validation ==="

# 1. Container accessible
ssh root@$IP "hostname" &>/dev/null && echo "✅ Container accessible via SSH" || echo "❌ Container SSH failed"

# 2. Service listening on expected port
ssh root@$IP "ss -tlnp | grep -q ':$PORT'" && echo "✅ Service listening on port $PORT" || echo "❌ Service not listening"

# 3. DNS resolving to Traefik
dig +short $DOMAIN | grep -q "$TRAEFIK_IP" && echo "✅ DNS resolves to Traefik" || echo "❌ DNS misconfigured"

# 4. HTTPS accessible through Traefik
curl -skI "https://$DOMAIN" | grep -qE "HTTP/[12]" && echo "✅ HTTPS working via Traefik" || echo "❌ HTTPS failed"

# 5. DHCP reservation exists
ssh root@$KEA_PRIMARY "grep -q '$MAC' $KEA_CONFIG" && echo "✅ DHCP reservation on primary" || echo "❌ DHCP missing on primary"
ssh root@$KEA_SECONDARY "grep -q '$MAC' $KEA_CONFIG" && echo "✅ DHCP reservation on secondary" || echo "❌ DHCP missing on secondary"

# 6. Traefik health check passing
curl -sk "$TRAEFIK_DASHBOARD/api/http/services" | grep -A5 "$SERVICE" | grep -q '"status":"UP"' && echo "✅ Traefik health check passing" || echo "⚠️  Check Traefik health status"

echo "=== Validation Complete ==="
```

## Standalone Hardware Deployment

For services running on dedicated hardware (not LXC), skip Phase 2 (container creation) and adjust:

- **Phase 3 (DHCP):** Use the hardware's actual MAC address
- **Phase 4 (DNS):** 
  - Point to Traefik IP if proxying through Traefik (recommended)
  - Point directly to hardware IP if bypassing Traefik
- **Phase 5 (Traefik):** Backend URL points to hardware IP

## Common Issues

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| **502 Bad Gateway** | `curl -I http://$IP:$PORT` fails | Service not running or wrong port in Traefik |
| **DNS returns Cloudflare IP** | `dig +short $DOMAIN` shows 104.x.x.x | AdGuard rewrite missing - add to both servers |
| **IP Conflict** | `ping $IP` responds before container created | Choose different IP |
| **DHCP not assigning IP** | Container gets random IP | Check MAC in reservation matches `pct config` |
| **Traefik 404** | Route exists but 404 | Check Host() rule matches exactly |

## Rollback Procedure

```bash
# 1. Stop and destroy container
ssh root@$NODE "pct stop $LXC_ID && pct destroy $LXC_ID"

# 2. Remove DHCP reservation (restore backup or edit manually)
ssh root@$KEA_PRIMARY "cp ${KEA_CONFIG}.backup-* $KEA_CONFIG && systemctl reload isc-kea-dhcp4-server"
ssh root@$KEA_SECONDARY "cp ${KEA_CONFIG}.backup-* $KEA_CONFIG && systemctl reload isc-kea-dhcp4-server"

# 3. Remove Traefik config (edit files to remove router/service entries)
ssh root@$TRAEFIK_IP "systemctl reload traefik"

# 4. Remove DNS rewrite (restore backup or edit manually)
ssh root@$ADGUARD_PRIMARY "cp ${ADGUARD_CONFIG}.backup-* $ADGUARD_CONFIG && systemctl restart AdGuardHome"
ssh root@$ADGUARD_SECONDARY "cp ${ADGUARD_CONFIG}.backup-* $ADGUARD_CONFIG && systemctl restart AdGuardHome"

# 5. Remove from Uptime Kuma (manual via web UI)
# 6. Remove from Homepage (edit $HOMEPAGE_CONFIG)
```

## References

- [references/infrastructure.md](references/infrastructure.md) - Full inventory with all IPs and paths
- [references/traefik-templates.md](references/traefik-templates.md) - Router/service YAML templates and middleware examples
