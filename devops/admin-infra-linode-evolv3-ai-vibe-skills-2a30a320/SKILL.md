---
name: admin-infra-linode
description: |
  Deploys infrastructure on Linode (Akamai Cloud) with Linodes, Firewalls, and VLANs.
  Strong Kubernetes support with Cluster Autoscaler and Akamai edge network integration.

  Use when: setting up Linode/Akamai infrastructure, deploying Linodes, configuring firewalls, needing Kubernetes autoscaling, wanting Akamai CDN integration.

  Keywords: linode, akamai, linode-cli, VPS, dedicated CPU, firewall, VLAN, kubernetes autoscale, infrastructure
license: MIT
---

# Linode Infrastructure

**Status**: Production Ready | **Dependencies**: linode-cli, SSH key pair

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
- [ ] LINODE_REGION    - Region (us-east, us-central, us-west, eu-west, ap-south, etc.)
- [ ] LINODE_TYPE      - Linode type (see profiles below)
- [ ] SSH_KEY_LABEL    - Label of SSH key in Linode
- [ ] SSH_KEY_PATH     - Path to local SSH private key (default: ~/.ssh/id_rsa)

Deployment Purpose (determines recommended profile):
- [ ] Purpose: coolify / kasm / both / custom
      coolify → g6-standard-2 ($36/mo)
      kasm    → g6-standard-4 ($72/mo)
      both    → g6-standard-8 ($144/mo)
      custom  → Ask for specific type
```

**Recommended profiles by purpose:**

| Purpose | Type | vCPU | RAM | Monthly |
|---------|------|------|-----|---------|
| coolify | g6-standard-2 | 2 | 4GB | $36 |
| kasm | g6-standard-4 | 4 | 8GB | $72 |
| both | g6-standard-8 | 8 | 16GB | $144 |

**DO NOT proceed to Prerequisites until ALL parameters are confirmed.**

---

## Prerequisites

Before using this skill, verify the following:

### 1. Linode CLI Installed

```bash
linode-cli --version
```

**If missing**, install with:

```bash
# Python (pip) - Recommended
pip3 install linode-cli

# macOS (Homebrew)
brew install linode-cli

# Linux (pipx)
pipx install linode-cli
```

### 2. Linode Account & API Token

**If you don't have a Linode account**:

Sign up at: https://www.linode.com/?r=YOUR_REFERRAL_CODE

> *Disclosure: This is a referral link. You'll receive $100 in credit for 60 days, and the skill author receives $25 account credit after you spend $25. Using this link helps support the development of these skills.*

**Get API Token**: https://cloud.linode.com/profile/tokens

Create a Personal Access Token with **Read/Write** access for Linodes, Firewalls, NodeBalancers, etc.

### 3. linode-cli Configured

```bash
linode-cli account view
```

**If it shows an error**, configure with:

```bash
# Interactive setup
linode-cli configure

# Or via environment variable
export LINODE_CLI_TOKEN="your_token_here"
linode-cli account view
```

### 4. SSH Key Pair

```bash
ls ~/.ssh/id_rsa.pub
```

**If missing**, generate with:

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
```

### 5. SSH Key Uploaded to Linode

```bash
linode-cli sshkeys list
```

**If empty**, upload with:

```bash
linode-cli sshkeys create --label "my-key" --ssh_key "$(cat ~/.ssh/id_rsa.pub)"
```

### 6. Test Authentication

```bash
linode-cli regions list
```

**If this fails**: Token may be invalid or expired. Create a new one.

---

## Server Profiles

### Coolify/Kasm Deployments

| Profile | Linode Type | vCPU | RAM | Disk | Monthly Cost |
|---------|-------------|------|-----|------|--------------|
| `coolify` | g6-standard-2 | 2 | 4GB | 80GB | $36 |
| `kasm` | g6-standard-4 | 4 | 8GB | 160GB | $72 |
| `both` | g6-standard-8 | 8 | 16GB | 320GB | $144 |

### Dedicated CPU (Best Performance)

| Profile | Linode Type | vCPU | RAM | Disk | Monthly Cost |
|---------|-------------|------|-----|------|--------------|
| `dedicated-small` | g6-dedicated-2 | 2 | 4GB | 80GB | $36 |
| `dedicated-medium` | g6-dedicated-4 | 4 | 8GB | 160GB | $72 |
| `dedicated-large` | g6-dedicated-8 | 8 | 16GB | 320GB | $144 |

<details>
<summary><strong>Premium Plans (Higher Performance)</strong></summary>

| Linode Type | vCPU | RAM | Disk | Monthly Cost |
|-------------|------|-----|------|--------------|
| g7-premium-2 | 2 | 4GB | 100GB | $43 |
| g7-premium-4 | 4 | 8GB | 200GB | $86 |
| g7-premium-8 | 8 | 16GB | 400GB | $172 |

</details>

---

## Deployment Steps

### Step 1: Set Environment Variables

```bash
export LINODE_REGION="us-east"             # See regions below
export LINODE_TYPE="g6-standard-2"         # See profiles above
export LINODE_IMAGE="linode/ubuntu22.04"
export SERVER_NAME="my-server"
export SSH_KEY_LABEL="my-key"
```

<details>
<summary><strong>Region options</strong></summary>

| Code | Location | Region |
|------|----------|--------|
| `us-east` | Newark, NJ | US East |
| `us-central` | Dallas, TX | US Central |
| `us-west` | Fremont, CA | US West |
| `us-southeast` | Atlanta, GA | US Southeast |
| `us-ord` | Chicago, IL | US Central |
| `us-lax` | Los Angeles, CA | US West |
| `us-mia` | Miami, FL | US Southeast |
| `us-sea` | Seattle, WA | US Northwest |
| `ca-central` | Toronto, Canada | Canada |
| `eu-west` | London, UK | UK |
| `eu-central` | Frankfurt, Germany | Germany |
| `ap-south` | Singapore | Asia |
| `ap-northeast` | Tokyo, Japan | Japan |
| `ap-west` | Mumbai, India | India |
| `ap-southeast` | Sydney, Australia | Australia |

Run `linode-cli regions list` for full list.

</details>

### Step 2: Get SSH Key ID

```bash
SSH_KEY_ID=$(linode-cli sshkeys list --label "$SSH_KEY_LABEL" --format id --text --no-headers)
echo "SSH Key ID: $SSH_KEY_ID"

# Verify
if [ -z "$SSH_KEY_ID" ]; then
  echo "ERROR: SSH key '$SSH_KEY_LABEL' not found. Upload it first."
  exit 1
fi
```

### Step 3: Create Firewall

```bash
# Create firewall
FIREWALL_ID=$(linode-cli firewalls create \
  --label "my-firewall" \
  --rules.inbound_policy DROP \
  --rules.outbound_policy ACCEPT \
  --format id --text --no-headers)

echo "Firewall ID: $FIREWALL_ID"

# Allow SSH
linode-cli firewalls rules-update "$FIREWALL_ID" \
  --inbound '[
    {"protocol":"TCP","ports":"22","addresses":{"ipv4":["0.0.0.0/0"],"ipv6":["::/0"]},"action":"ACCEPT"},
    {"protocol":"TCP","ports":"80","addresses":{"ipv4":["0.0.0.0/0"],"ipv6":["::/0"]},"action":"ACCEPT"},
    {"protocol":"TCP","ports":"443","addresses":{"ipv4":["0.0.0.0/0"],"ipv6":["::/0"]},"action":"ACCEPT"},
    {"protocol":"TCP","ports":"8000","addresses":{"ipv4":["0.0.0.0/0"],"ipv6":["::/0"]},"action":"ACCEPT"},
    {"protocol":"TCP","ports":"6001-6002","addresses":{"ipv4":["0.0.0.0/0"],"ipv6":["::/0"]},"action":"ACCEPT"},
    {"protocol":"TCP","ports":"8443","addresses":{"ipv4":["0.0.0.0/0"],"ipv6":["::/0"]},"action":"ACCEPT"},
    {"protocol":"TCP","ports":"3389","addresses":{"ipv4":["0.0.0.0/0"],"ipv6":["::/0"]},"action":"ACCEPT"},
    {"protocol":"TCP","ports":"3000-4000","addresses":{"ipv4":["0.0.0.0/0"],"ipv6":["::/0"]},"action":"ACCEPT"}
  ]' \
  --inbound_policy DROP \
  --outbound_policy ACCEPT
```

### Step 4: Create Linode

```bash
LINODE_ID=$(linode-cli linodes create \
  --region "$LINODE_REGION" \
  --type "$LINODE_TYPE" \
  --image "$LINODE_IMAGE" \
  --label "$SERVER_NAME" \
  --authorized_keys "$(cat ~/.ssh/id_rsa.pub)" \
  --root_pass "$(openssl rand -base64 32)" \
  --format id --text --no-headers)

echo "Linode ID: $LINODE_ID"
```

### Step 5: Apply Firewall to Linode

```bash
linode-cli firewalls device-create "$FIREWALL_ID" \
  --type linode \
  --id "$LINODE_ID"
```

### Step 6: Wait and Get Linode IP

```bash
# Wait for Linode to be running
echo "Waiting for Linode to be running..."
while [ "$(linode-cli linodes view "$LINODE_ID" --format status --text --no-headers)" != "running" ]; do
  sleep 5
done

# Get IP address
SERVER_IP=$(linode-cli linodes view "$LINODE_ID" --format ipv4 --text --no-headers | head -1)
echo "SERVER_IP=$SERVER_IP"
```

### Step 7: Wait for Server Ready

```bash
# Wait for SSH to be available (typically 60-90 seconds)
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
# Linode only offers x86 architecture
SERVER_ARCH="amd64"

# Save to .env.local for downstream skills
echo "SERVER_IP=$SERVER_IP" >> .env.local
echo "SSH_USER=root" >> .env.local
echo "SSH_KEY_PATH=~/.ssh/id_rsa" >> .env.local
echo "SERVER_ARCH=$SERVER_ARCH" >> .env.local
echo "COOLIFY_SERVER_IP=$SERVER_IP" >> .env.local
echo "KASM_SERVER_IP=$SERVER_IP" >> .env.local

echo ""
echo "Linode deployed successfully!"
echo "  IP: $SERVER_IP"
echo "  Arch: $SERVER_ARCH"
echo "  SSH: ssh root@$SERVER_IP"
```

---

## Verify Deployment

```bash
ssh root@$SERVER_IP "echo 'Linode connected successfully'"
```

---

## Kubernetes Auto-Scaling

Linode Kubernetes Engine (LKE) supports Cluster Autoscaler for automatic node scaling.

### Create LKE Cluster

```bash
# Create cluster (via API - CLI doesn't support all options)
linode-cli lke cluster-create \
  --label "my-lke" \
  --region "$LINODE_REGION" \
  --k8s_version "1.28"
```

### Enable Cluster Autoscaler

The Cluster Autoscaler runs in the management cluster and scales based on workload:

1. Install Cluster Autoscaler add-on in your cluster
2. Configure with Linode API token
3. Set min/max nodes per pool

See: https://linode.github.io/cluster-api-provider-linode/topics/autoscaling.html

---

## Cleanup

**Warning**: This is destructive and cannot be undone.

```bash
# Delete Linode
linode-cli linodes delete "$LINODE_ID"

# Delete firewall
linode-cli firewalls delete "$FIREWALL_ID"

# Optionally delete SSH key
# linode-cli sshkeys delete "$SSH_KEY_ID"
```

---

## Operations

Troubleshooting, best practices, configuration variables, and cost snapshots are in `references/OPERATIONS.md`.

---

## Logging Integration

When performing infrastructure operations, log to the centralized system:

```bash
# After provisioning
log_admin "SUCCESS" "operation" "Provisioned Linode" "id=$LINODE_ID provider=Linode"

# After destroying
log_admin "SUCCESS" "operation" "Deleted Linode" "id=$LINODE_ID"

# On error
log_admin "ERROR" "operation" "Linode deployment failed" "error=$ERROR_MSG"
```

See `admin` skill's `references/logging.md` for full logging documentation.

---

## References

- [Linode Cloud Manager](https://cloud.linode.com/)
- [linode-cli Documentation](https://www.linode.com/docs/products/tools/cli/get-started/)
- [Pricing](https://www.linode.com/pricing/)
- [API Documentation](https://www.linode.com/docs/api/)
- [LKE Documentation](https://www.linode.com/docs/products/compute/kubernetes/)
- [Cluster Autoscaler](https://linode.github.io/cluster-api-provider-linode/topics/autoscaling.html)
