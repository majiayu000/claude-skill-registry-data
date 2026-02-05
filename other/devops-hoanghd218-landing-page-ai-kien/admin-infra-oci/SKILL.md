---
name: admin-infra-oci
description: |
  Deploys infrastructure on Oracle Cloud Infrastructure (OCI) with ARM64 instances (Always Free tier eligible).
  Handles compartments, VCNs, subnets, security lists, and compute instances.

  Use when: setting up Oracle Cloud infrastructure, deploying ARM64 instances, troubleshooting OUT_OF_HOST_CAPACITY errors, optimizing for Always Free tier.

  Keywords: oracle cloud, OCI, ARM64, VM.Standard.A1.Flex, Always Free tier, OUT_OF_HOST_CAPACITY, oci compartment, oci vcn
license: MIT
---

# Oracle Cloud Infrastructure (OCI)

**Status**: Production Ready | **Dependencies**: OCI CLI, SSH key pair

---

## Navigation

- Operations, troubleshooting, config, and cleanup: `references/OPERATIONS.md`
- CLI install/config/capacity/networking details: `docs/`

---

## Step 0: Gather Required Information (MANDATORY)

**STOP. Before ANY deployment commands, collect ALL parameters from the user.**

Copy this checklist and confirm each item:

```
Required Parameters:
- [ ] SERVER_NAME       - Unique name for this server
- [ ] OCI_REGION        - Region (us-ashburn-1, us-phoenix-1, ca-toronto-1, etc.)
- [ ] OCI_SHAPE         - Instance shape (see profiles below)
- [ ] OCI_OCPUS         - Number of OCPUs (1-4 for Always Free)
- [ ] OCI_MEMORY_GB     - Memory in GB (1-24 for Always Free)
- [ ] SSH_KEY_PATH      - Path to SSH public key (default: ~/.ssh/id_rsa.pub)

Deployment Purpose (determines recommended profile):
- [ ] Purpose: coolify / kasm / both / custom
      coolify → 2 OCPU, 12GB RAM (Always Free eligible)
      kasm    → 4 OCPU, 24GB RAM (Always Free eligible)
      both    → 4 OCPU, 24GB RAM (Always Free eligible)

Always Free Tier Limits:
- Shape: VM.Standard.A1.Flex (ARM64)
- Max: 4 OCPUs, 24GB RAM total (can split across instances)
```

**Recommended profiles by purpose:**

| Purpose | OCPUs | RAM | Shape | Cost |
|---------|-------|-----|-------|------|
| coolify | 2 | 12GB | VM.Standard.A1.Flex | FREE |
| kasm | 4 | 24GB | VM.Standard.A1.Flex | FREE |
| both | 4 | 24GB | VM.Standard.A1.Flex | FREE |

**DO NOT proceed to Prerequisites until ALL parameters are confirmed.**

---

## Prerequisites

Before using this skill, verify the following:

### 1. OCI CLI Installed

```bash
oci --version
```

**If missing**, install with:
```bash
bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)" -- --accept-all-defaults
source ~/.bashrc  # or restart terminal
```

### 2. OCI CLI Configured

```bash
ls ~/.oci/config
```

**If missing**, configure with:
```bash
oci setup config
```

You'll need:
- Tenancy OCID (OCI Console → Profile → Tenancy)
- User OCID (OCI Console → Profile → My Profile)
- Region (e.g., us-ashburn-1)
- API key pair (wizard generates this)

### 3. SSH Key Pair

```bash
ls ~/.ssh/id_rsa.pub
```

**If missing**, generate with:
```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
```

### 4. SSH Key Permissions

```bash
stat -c %a ~/.ssh/id_rsa  # Should be 600
```

**If wrong**, fix with:
```bash
chmod 600 ~/.ssh/id_rsa
```

### 5. Test Authentication

```bash
oci iam availability-domain list
```

**If this fails**: API key may not be uploaded to OCI Console → Profile → API Keys

---

## Quick Start

### 1. Check Capacity First

OCI Always Free ARM instances are highly demanded. **Always check before deploying:**

```bash
./scripts/check-oci-capacity.sh
```

<details>
<summary><strong>Options and troubleshooting</strong></summary>

```bash
# Check specific region
./scripts/check-oci-capacity.sh us-ashburn-1

# Use different OCI profile
./scripts/check-oci-capacity.sh --profile PRODUCTION

# Check multiple regions
for region in us-ashburn-1 us-phoenix-1 ca-toronto-1; do
  echo "=== $region ==="
  ./scripts/check-oci-capacity.sh "$region"
done
```

**No capacity?** Use automated monitoring:

```bash
./scripts/monitor-and-deploy.sh --stack-id <STACK_OCID>
```

</details>

### 2. Deploy Infrastructure

```bash
# Configure environment
cp scripts/.env.example scripts/.env
# Edit scripts/.env with your values

# Deploy
./scripts/oci-infrastructure-setup.sh
```

---

## Scripts Reference

| Script | Purpose | Usage |
|--------|---------|-------|
| `check-oci-capacity.sh` | Check ARM instance availability | `./scripts/check-oci-capacity.sh [region]` |
| `oci-infrastructure-setup.sh` | Full infrastructure deployment | `./scripts/oci-infrastructure-setup.sh` |
| `monitor-and-deploy.sh` | Auto-deploy when capacity available | `./scripts/monitor-and-deploy.sh --stack-id <ID>` |
| `cleanup-compartment.sh` | Delete all resources | `./scripts/cleanup-compartment.sh <COMPARTMENT_OCID>` |

<details>
<summary><strong>Script details</strong></summary>

### check-oci-capacity.sh

Checks VM.Standard.A1.Flex availability across availability domains.

```bash
./scripts/check-oci-capacity.sh                    # Home region
./scripts/check-oci-capacity.sh us-ashburn-1       # Specific region
./scripts/check-oci-capacity.sh --profile DANIEL   # With profile
```

Tests 4 OCPU / 24GB RAM (full free tier), falls back to 2/12 if unavailable.

### monitor-and-deploy.sh

Continuously monitors and auto-deploys when capacity found.

```bash
./scripts/monitor-and-deploy.sh \
  --stack-id <STACK_OCID> \
  --profile DANIEL \
  --interval 300 \
  --max-attempts 100
```

### oci-infrastructure-setup.sh

Creates complete infrastructure: compartment → VCN → subnet → IGW → security list → instance.

Requires `.env` file with OCI credentials and configuration.

### cleanup-compartment.sh

Safely deletes compartment and all resources (requires confirmation).

```bash
./scripts/cleanup-compartment.sh ocid1.compartment.oc1..xxx
```

</details>

---

## Operations

Common issues, best practices, configuration variables, and cleanup ordering are in `references/OPERATIONS.md`.

---

## Logging Integration

When performing infrastructure operations, log to the centralized system:

```bash
# After provisioning
log_admin "SUCCESS" "operation" "Provisioned OCI instance" "id=$INSTANCE_ID provider=OCI"

# After destroying
log_admin "SUCCESS" "operation" "Terminated OCI instance" "id=$INSTANCE_ID"

# On error
log_admin "ERROR" "operation" "OCI deployment failed" "error=OUT_OF_HOST_CAPACITY"
```

See `admin` skill's `references/logging.md` for full logging documentation.

---

## Additional Documentation

- [Installation Guide](docs/INSTALL.md) - Install OCI CLI on any OS
- [Configuration Guide](docs/CONFIG.md) - Set up OCI credentials
- [Capacity Guide](docs/CAPACITY.md) - Handling capacity issues
- [Networking Guide](docs/NETWORKING.md) - VCN, subnets, security lists
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md) - Common issues and solutions

---

## Official Resources

- [OCI Documentation](https://docs.oracle.com/en-us/iaas/Content/home.htm)
- [OCI CLI Reference](https://docs.oracle.com/en-us/iaas/tools/oci-cli/latest/)
- [Always Free Tier](https://www.oracle.com/cloud/free/)
- [ARM Instances Guide](https://docs.oracle.com/en-us/iaas/Content/Compute/References/arm.htm)
