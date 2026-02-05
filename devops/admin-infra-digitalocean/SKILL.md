---
name: admin-infra-digitalocean
description: |
  Deploys infrastructure on DigitalOcean with Droplets (VMs), Firewalls, and VPCs.
  Includes Kasm Workspaces auto-scaling integration for dynamic agent provisioning.

  Use when: setting up DigitalOcean infrastructure, deploying Droplets, configuring firewalls, integrating with Kasm auto-scaling, looking for US/global cloud with good API.

  Keywords: digitalocean, doctl, droplet, VPS, firewall, VPC, kasm autoscale, cloud infrastructure
license: MIT
---

# DigitalOcean Infrastructure

**Status**: Production Ready | **Dependencies**: doctl CLI, SSH key pair

---

## Navigation

- Operations, troubleshooting, config, and cost snapshot: `references/OPERATIONS.md`

---

## Step 0: Gather Required Information (MANDATORY)

**STOP. Before ANY deployment commands, collect ALL parameters from the user.**

Copy this checklist and confirm each item:

```
Required Parameters:
- [ ] SERVER_NAME      - Unique name for this server
- [ ] DO_REGION        - Region (nyc1, sfo3, lon1, fra1, sgp1, etc.)
- [ ] DO_SIZE          - Droplet size (see profiles below)
- [ ] SSH_KEY_NAME     - Name of SSH key in DigitalOcean
- [ ] SSH_KEY_PATH     - Path to local SSH private key (default: ~/.ssh/id_rsa)

Deployment Purpose (determines recommended profile):
- [ ] Purpose: coolify / kasm / both / custom
      coolify → s-2vcpu-4gb ($24/mo)
      kasm    → s-4vcpu-8gb ($48/mo)
      both    → s-8vcpu-16gb ($96/mo)
      custom  → Ask for specific size
```

**Recommended profiles by purpose:**

| Purpose | Size | vCPU | RAM | Monthly |
|---------|------|------|-----|---------|
| coolify | s-2vcpu-4gb | 2 | 4GB | $24 |
| kasm | s-4vcpu-8gb | 4 | 8GB | $48 |
| both | s-8vcpu-16gb | 8 | 16GB | $96 |

**DO NOT proceed to Prerequisites until ALL parameters are confirmed.**

---

## Prerequisites

Before using this skill, verify the following:

### 1. DigitalOcean CLI Installed

```bash
doctl version
```

**If missing**, install with:

```bash
# macOS
brew install doctl

# Linux (snap)
sudo snap install doctl

# Linux (download binary)
cd ~
wget https://github.com/digitalocean/doctl/releases/download/v1.104.0/doctl-1.104.0-linux-amd64.tar.gz
tar xf doctl-1.104.0-linux-amd64.tar.gz
sudo mv doctl /usr/local/bin

# Windows (scoop)
scoop install doctl
```

### 2. DigitalOcean Account & API Token

**If you don't have a DigitalOcean account**:

Sign up at: https://m.do.co/c/YOUR_REFERRAL_CODE

> *Disclosure: This is a referral link. You'll receive $200 in credit for 60 days, and the skill author receives account credit. Using this link helps support the development of these skills.*

**Get API token**: https://cloud.digitalocean.com/account/api/tokens

Create a token with **Read & Write** scope.

### 3. doctl CLI Configured

```bash
doctl account get
```

**If it shows an error**, authenticate with:

```bash
doctl auth init
# Paste your API token when prompted
```

Or set via environment variable:
```bash
export DIGITALOCEAN_ACCESS_TOKEN="your_token_here"
doctl account get
```

### 4. SSH Key Pair

```bash
ls ~/.ssh/id_rsa.pub
```

**If missing**, generate with:

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
```

### 5. SSH Key Uploaded to DigitalOcean

```bash
doctl compute ssh-key list
```

**If empty**, upload with:

```bash
doctl compute ssh-key import my-key --public-key-file ~/.ssh/id_rsa.pub
```

### 6. Test Authentication

```bash
doctl compute region list
```

**If this fails**: Token may be invalid or expired. Create a new one.

---

## Server Profiles

### Coolify/Kasm Deployments

| Profile | Droplet Type | vCPU | RAM | Disk | Monthly Cost |
|---------|--------------|------|-----|------|--------------|
| `coolify` | s-2vcpu-4gb | 2 | 4GB | 80GB | $24 |
| `kasm` | s-4vcpu-8gb | 4 | 8GB | 160GB | $48 |
| `both` | s-8vcpu-16gb | 8 | 16GB | 320GB | $96 |

### Premium CPU (Higher Performance)

| Profile | Droplet Type | vCPU | RAM | Disk | Monthly Cost |
|---------|--------------|------|-----|------|--------------|
| `premium-small` | c-4-8gib | 4 | 8GB | 50GB | $84 |
| `premium-medium` | c-8-16gib | 8 | 16GB | 100GB | $168 |
| `premium-large` | c-16-32gib | 16 | 32GB | 200GB | $336 |

<details>
<summary><strong>General Purpose (Best for mixed workloads)</strong></summary>

| Droplet Type | vCPU | RAM | Disk | Monthly Cost |
|--------------|------|-----|------|--------------|
| g-2vcpu-8gb | 2 | 8GB | 25GB | $63 |
| g-4vcpu-16gb | 4 | 16GB | 50GB | $126 |
| g-8vcpu-32gb | 8 | 32GB | 100GB | $252 |

</details>

---

## Deployment Steps

### Step 1: Set Environment Variables

```bash
export DO_REGION="nyc1"                    # See regions below
export DO_SIZE="s-2vcpu-4gb"               # See profiles above
export DO_IMAGE="ubuntu-22-04-x64"
export SERVER_NAME="my-server"
export SSH_KEY_NAME="my-key"
```

<details>
<summary><strong>Region options</strong></summary>

| Code | Location | Region |
|------|----------|--------|
| `nyc1` | New York 1 | US East |
| `nyc3` | New York 3 | US East |
| `sfo2` | San Francisco 2 | US West |
| `sfo3` | San Francisco 3 | US West |
| `tor1` | Toronto | Canada |
| `lon1` | London | UK |
| `ams3` | Amsterdam | Netherlands |
| `fra1` | Frankfurt | Germany |
| `blr1` | Bangalore | India |
| `sgp1` | Singapore | Asia |
| `syd1` | Sydney | Australia |

</details>

### Step 2: Get SSH Key ID

```bash
SSH_KEY_ID=$(doctl compute ssh-key list --format ID,Name --no-header | grep "$SSH_KEY_NAME" | awk '{print $1}')
echo "SSH Key ID: $SSH_KEY_ID"

# Verify
if [ -z "$SSH_KEY_ID" ]; then
  echo "ERROR: SSH key '$SSH_KEY_NAME' not found. Upload it first."
  exit 1
fi
```

### Step 3: Create Firewall

```bash
# Create firewall
doctl compute firewall create \
  --name my-firewall \
  --inbound-rules "protocol:tcp,ports:22,address:0.0.0.0/0,address:::/0" \
  --inbound-rules "protocol:tcp,ports:80,address:0.0.0.0/0,address:::/0" \
  --inbound-rules "protocol:tcp,ports:443,address:0.0.0.0/0,address:::/0" \
  --inbound-rules "protocol:tcp,ports:8000,address:0.0.0.0/0,address:::/0" \
  --inbound-rules "protocol:tcp,ports:6001-6002,address:0.0.0.0/0,address:::/0" \
  --inbound-rules "protocol:tcp,ports:8443,address:0.0.0.0/0,address:::/0" \
  --inbound-rules "protocol:tcp,ports:3389,address:0.0.0.0/0,address:::/0" \
  --inbound-rules "protocol:tcp,ports:3000-4000,address:0.0.0.0/0,address:::/0" \
  --outbound-rules "protocol:tcp,ports:all,address:0.0.0.0/0,address:::/0" \
  --outbound-rules "protocol:udp,ports:all,address:0.0.0.0/0,address:::/0" \
  --outbound-rules "protocol:icmp,address:0.0.0.0/0,address:::/0"
```

### Step 4: Create Droplet

```bash
doctl compute droplet create "$SERVER_NAME" \
  --region "$DO_REGION" \
  --size "$DO_SIZE" \
  --image "$DO_IMAGE" \
  --ssh-keys "$SSH_KEY_ID" \
  --tag-names "myproject" \
  --wait
```

### Step 5: Get Droplet IP

```bash
SERVER_IP=$(doctl compute droplet get "$SERVER_NAME" --format PublicIPv4 --no-header)
echo "SERVER_IP=$SERVER_IP"
```

### Step 6: Apply Firewall to Droplet

```bash
FIREWALL_ID=$(doctl compute firewall list --format ID,Name --no-header | grep "my-firewall" | awk '{print $1}')
DROPLET_ID=$(doctl compute droplet get "$SERVER_NAME" --format ID --no-header)

doctl compute firewall add-droplets "$FIREWALL_ID" --droplet-ids "$DROPLET_ID"
```

### Step 7: Wait for Server Ready

```bash
# Wait for SSH to be available (typically 30-60 seconds)
echo "Waiting for server to be ready..."
until ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no root@$SERVER_IP "echo connected" 2>/dev/null; do
  sleep 5
done
echo "Server is ready!"
```

### Step 8: Verify Connection

```bash
ssh root@$SERVER_IP "uname -a && free -h && df -h /"
```

### Step 9: Output for Downstream Skills

```bash
# DigitalOcean only offers x86 architecture
SERVER_ARCH="amd64"

# Save to .env.local for downstream skills
echo "SERVER_IP=$SERVER_IP" >> .env.local
echo "SSH_USER=root" >> .env.local
echo "SSH_KEY_PATH=~/.ssh/id_rsa" >> .env.local
echo "SERVER_ARCH=$SERVER_ARCH" >> .env.local
echo "COOLIFY_SERVER_IP=$SERVER_IP" >> .env.local
echo "KASM_SERVER_IP=$SERVER_IP" >> .env.local

echo ""
echo "Droplet deployed successfully!"
echo "  IP: $SERVER_IP"
echo "  Arch: $SERVER_ARCH"
echo "  SSH: ssh root@$SERVER_IP"
```

---

## Verify Deployment

```bash
ssh root@$SERVER_IP "echo 'DigitalOcean Droplet connected successfully'"
```

---

## Kasm Workspaces Auto-Scaling

DigitalOcean has native integration with Kasm Workspaces for automatic agent provisioning.

### Enable in Kasm Admin

1. Go to **Infrastructure** → **Pools** → **Edit Pool**
2. Enable **Digital Ocean Scaling Enabled**
3. Configure:
   - **DO API Key**: Your DigitalOcean API token
   - **DO Region**: Region for new agents
   - **DO Droplet Size**: Size for auto-provisioned droplets
   - **DO SSH Key ID**: Your SSH key ID

### How It Works

- Kasm automatically provisions new Droplets when user demand increases
- Droplets are destroyed when no longer needed
- Ensures resource utilization and cost efficiency

---

## Cleanup

**Warning**: This is destructive and cannot be undone.

```bash
# Delete droplet
doctl compute droplet delete "$SERVER_NAME" --force

# Delete firewall
FIREWALL_ID=$(doctl compute firewall list --format ID,Name --no-header | grep "my-firewall" | awk '{print $1}')
doctl compute firewall delete "$FIREWALL_ID" --force

# Optionally delete SSH key
# doctl compute ssh-key delete "$SSH_KEY_ID" --force
```

---

## Operations

Troubleshooting, best practices, configuration variables, and cost snapshots are in `references/OPERATIONS.md`.

---

## Logging Integration

When performing infrastructure operations, log to the centralized system:

```bash
# After provisioning
log_admin "SUCCESS" "operation" "Provisioned DigitalOcean droplet" "id=$DROPLET_ID provider=DigitalOcean"

# After destroying
log_admin "SUCCESS" "operation" "Deleted DigitalOcean droplet" "id=$DROPLET_ID"

# On error
log_admin "ERROR" "operation" "DigitalOcean deployment failed" "error=$ERROR_MSG"
```

See `admin` skill's `references/logging.md` for full logging documentation.

---

## References

- [DigitalOcean Console](https://cloud.digitalocean.com/)
- [doctl CLI Documentation](https://docs.digitalocean.com/reference/doctl/)
- [Droplet Pricing](https://www.digitalocean.com/pricing/droplets)
- [API Documentation](https://docs.digitalocean.com/reference/api/)
- [Kasm Auto-Scaling Docs](https://www.kasmweb.com/docs/latest/guide/zones/aws_autoscaling.html)
