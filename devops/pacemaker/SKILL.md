---
name: pacemaker
description: Manages Pacemaker HA clusters with pcs and crmsh for resource provisioning, constraints, STONITH fencing, quorum configuration, and cluster lifecycle operations on two-node and multi-node setups.
license: MIT
compatibility: opencode
metadata:
  version: "1.0.0"
  domain: linux
  role: implementation
  scope: infrastructure
  output-format: code
  content-types: [code, guidance, config, do-dont]
  triggers: pacemaker, pcs command, crmsh, cluster resource, STONITH fencing, CIB configuration, quorum management, promotable clone
  archetypes:
    - tactical
    - diagnostic
  anti_triggers:
    - brainstorming
    - vague ideation
  response_profile:
    verbosity: low
    directive_strength: high
    abstraction_level: operational
  related-skills: corosync, linux-services, storage-architecture
  maturity: stable
  completeness: 95
  exampleCount: 4
---

# Pacemaker HA Cluster Management

Senior Linux infrastructure engineer managing Pacemaker 3.x HA clusters with PCS and crmsh for resource provisioning, constraints, STONITH fencing, quorum configuration, and cluster lifecycle operations.

## TL;DR Checklist

- [ ] Verify node connectivity and corosync membership before creating any resources
- [ ] Configure STONITH (fencing) devices on every cluster — never disable in production
- [ ] Set up quorum strategy (qdevice for two-node clusters) before adding workloads
- [ ] Create resources with explicit monitor operations and appropriate intervals
- [ ] Define colocation AND ordering constraints — they are independent, not interchangeable
- [ ] Use `pcs resource cleanup` after node recovery to clear stale failcounts

---

## When to Use

Use this skill when:

- **Building HA clusters** — You're provisioning a two-node or multi-node Pacemaker cluster with Corosync and need end-to-end setup guidance
- **Managing cluster resources** — You need to create, migrate, stop, start, or troubleshoot OCF resource agents (VirtualIP, Apache, database, etc.)
- **Configuring fencing** — You must set up STONITH/fence devices (IPMI, iLO, DRAC, WTI) for a production cluster
- **Fixing split-brain risk** — A two-node cluster needs qdevice or corosync `two_node` quorum configuration
- **Troubleshooting clusters** — Resources won't start, nodes show uncertain state, or CIB conflicts need resolution
- **Implementing master/slave patterns** — You're deploying promotable clones for databases (PostgreSQL, MySQL), DRBD, or other active/passive workloads
- **Running cluster diagnostics** — You need to generate reports with `crm_report` or analyze CIB state

---

## When NOT to Use

Avoid this skill for:

- **Kubernetes clustering** — Use Kubernetes native HA patterns instead; Pacemaker is not a container orchestrator
- **Load balancing** — Use HAProxy, Nginx, or cloud load balancers; Pacemaker manages node failover, not traffic distribution
- **Single-node high availability** — If only one server exists, you need backups/replication, not a cluster
- **Application-level redundancy** — Design your application to be stateless and multi-instance; Pacemaker is infrastructure-level failover

Use `linux-services` for systemd unit configuration that complements OCF resource agents. Use `corosync` for network-layer membership and token configuration.

---

## Core Workflow

### 1. Cluster Initialization and Node Setup

Create the cluster from scratch with Corosync as the messaging layer.

```bash
# On BOTH nodes — install packages (RHEL/Rocky/Alma)
sudo dnf install -y pcs pacemaker corosync

# Enable and start PCS daemon on both nodes
sudo systemctl enable --now pcsd

# Set identical hacluster password on every node
echo 'changeme' | sudo passwd hacluster --stdin

# Authenticate PCS between nodes from the first node
sudo pcs cluster auth node1 node2 -u hacluster -p 'changeme' --force

# Create and start the cluster
sudo pcs cluster setup --name mycluster node1 node2 --start --enable
```

**Checkpoint:** Run `pcs status` — all nodes should show as "Online" and the cluster state should be "Active." If any node is "Offline," check corosync logs: `journalctl -u corosync --since "5 minutes ago"`.

### 2. Configure STONITH (Fencing) Devices

Every production cluster MUST have fencing configured before adding workloads.

```bash
# Example: IPMI fence device for each node
sudo pcs stonith create fence-node1-ipmi \
  stonith:fence_ipmilan \
  ipaddr="192.168.1.100" \
  login="admin" \
  passwd="secret" \
  pcmk_host_list="node1" \
  power_wait="5" \
  op monitor interval="60s"

sudo pcs stonith create fence-node2-ipmi \
  stonith:fence_ipmilan \
  ipaddr="192.168.1.101" \
  login="admin" \
  passwd="secret" \
  pcmk_host_list="node2" \
  power_wait="5" \
  op monitor interval="60s"

# Enable fencing on the cluster
sudo pcs property set stonith-enabled=true

# Set fencing delay to prevent race conditions during multi-node outages
sudo pcs property set pcmk_delay_base=30
sudo pcs property set pcmk_delay_max=60

# Test each fence device BEFORE declaring production readiness
sudo pcs stonith fence node1 --force
sudo pcs stonith fence node2 --force
```

**Checkpoint:** Both fence devices show as "Started" in `pcs status resources`. Each test fence action successfully powers cycles the target node (or reports success from the management interface).

### 3. Configure Quorum Strategy

Two-node clusters without qdevice are susceptible to split-brain. Choose a strategy:

```bash
# OPTION A — Recommended for two-node clusters: qdevice (RHEL 9+)
sudo pcs qdevice setup alibi --init --nodes node1,node2

# OPTION B — Corosync-level two_node mode (works without qdevice)
# Edit corosync.conf on BOTH nodes:
# quorum { expected_votes: 2; two_node: 1 }

# For multi-node clusters (3+), the default majority-quorum policy works fine
# sudo pcs property set no-quorum-policy=stop   # default — stops all resources

# Set safe no-quorum policy for qdevice-enabled clusters
sudo pcs property set no-quorum-policy=ignore
```

**Checkpoint:** `pcs status corosync` shows correct membership count. `pcs status quorum` confirms expected votes match and the node count provides adequate quorum.

### 4. Create Resources with Constraints

Define virtual IP, application, and storage resources with proper ordering.

```bash
# Create a managed VirtualIP resource
sudo pcs resource create VirtualIP ocf:heartbeat:IPaddr2 \
  ip="192.168.1.200" \
  cidr_netmask="24" \
  op monitor interval="30s"

# Create an Apache resource (runs on the same node as VirtualIP)
sudo pcs resource create Apache ocf:heartbeat:apache \
  configfile="/etc/httpd/conf/httpd.conf" \
  statusurl="http://localhost/server-status" \
  op monitor interval="60s" \
  op start timeout="60s" \
  op stop timeout="60s"

# Create a web application resource (managed by Apache)
sudo pcs resource create WebSite ocf:heartbeat:apache \
  configfile="/etc/httpd/conf.d/webapp.conf" \
  op monitor interval="30s"

# Colocation: VirtualIP and Apache must be on the same node
sudo pcs constraint colocation add apache-with-vip VirtualIP Apache INFINITY

# Ordering: VirtualIP starts before Apache
sudo pcs constraint order VirtualIP then Apache kind=Mandatory

# Resource group alternative (bundles both colocation AND ordering)
# sudo pcs resource group add web-stack VirtualIP Apache WebSite
```

**Checkpoint:** `pcs status resources` shows all three resources running on the same node. Verify with `crm_simulate -s` that the constraint graph is consistent.

### 5. Implement Promotable Clones (Master/Slave)

For databases and shared-storage workloads requiring active/passive failover.

```bash
# Create a DRBD resource with promote operation
sudo pcs resource create db-storage ocf:linbit:drbd \
  drbd_resource=db0 \
  op monitor interval="30s" role=Slave \
  op promote interval="0s" role=Master

# Promote it to master/slave clone
sudo pcs resource master db-master db-storage \
  master-max=1 \
  master-node-max=1 \
  clone-max=2 \
  clone-node-max=1 \
  notify=true

# Ensure application runs only on the current master
sudo pcs constraint colocation add db-app-with-db-master WebSite with db-master INFINITY
sudo pcs constraint order db-master then WebSite kind=Mandatory
```

**Checkpoint:** `pcs status resources` shows one node as Master and the other as Slave for `db-master`. Failover test: `pcs cluster standby node1` — verify that the database promotes on node2 within the expected window.

---

## Implementation Patterns

### Pattern 1: Complete Cluster Build Script (BAD vs. GOOD)

**BAD — Manual step-by-step without error handling, skipping fencing, no idempotency**

```bash
# ❌ BAD: No error handling, skips critical security steps, not repeatable
sudo systemctl enable pcsd
sudo systemctl start pcsd
echo "changeme" | passwd hacluster --stdin
pcs cluster setup mycluster node1 node2
pcs property set stonith-enabled=false   # ← NEVER DISABLE STONITH
pcs resource create VIP ocf:heartbeat:IPaddr2 ip=10.0.0.50 op monitor interval=30s
```

**Problems:**
- No `set -euo pipefail` — failures are silently ignored
- Disables STONITH — Red Hat does NOT support unfenced clusters; split-brain data corruption risk
- Hardcoded passwords in plain text without secure handling
- No authentication between nodes (pcs cluster auth missing)
- No quorum configuration for the cluster type
- No start/stop timeout definitions on resources
- Not idempotent — re-running will create duplicate resources or fail

**GOOD — Idempotent, secure, production-ready with fencing and quorum**

```bash
#!/usr/bin/env bash
# Production-ready Pacemaker cluster setup script
# Usage: ./setup-cluster.sh <cluster_name> node1 node2 [node3...] [--qdevice-node <third_node>]
set -euo pipefail

readonly CLUSTER_NAME="${1:?Usage: $0 <cluster_name> node1 node2 ...}"
readonly NODES=("${@:2}")
readonly QDEVICE_NODE="${4:-}"  # Optional third node for qdevice

# ─── Validation ──────────────────────────────────────────────
if [[ ${#NODES[@]} -lt 2 ]]; then
    echo "ERROR: At least 2 nodes required" >&2
    exit 1
fi

echo "=== Pacemaker Cluster Setup: ${CLUSTER_NAME} ==="
echo "Nodes: ${NODES[*]}"

# ─── Step 1: Package Installation (idempotent) ──────────────
echo "[1/6] Installing packages..."
for node in "${NODES[@]}"; do
    echo "  → Ensuring packages on ${node}..."
    ssh -o StrictHostKeyChecking=no root@"${node}" \
        dnf install -y --setopt=install_weak_deps=false \
            pcs pacemaker corosync || {
            echo "ERROR: Failed to install packages on ${node}" >&2
            exit 1
        }
    ssh root@"${node}" systemctl enable --now pcsd
done

# ─── Step 2: Authentication ─────────────────────────────────
echo "[2/6] Configuring node authentication..."
for node in "${NODES[@]}"; do
    # Check if already authenticated by attempting a no-op command
    if ! ssh root@"${node}" pcs cluster auth >/dev/null 2>&1; then
        echo "  → Authenticating with ${node}..."
        ssh root@"${node}" passwd hacluster --stdin <<< "${HA_CLUSTER_PASSWORD:-changeme}"
    fi
done

# ─── Step 3: Cluster Creation ───────────────────────────────
echo "[3/6] Creating cluster: ${CLUSTER_NAME}..."
if ! pcs cluster auth --with-force "${NODES[@]}" -u hacluster \
        -p "${HA_CLUSTER_PASSWORD:-changeme}" >/dev/null 2>&1; then
    echo "ERROR: Node authentication failed. Verify hacluster password matches." >&2
    exit 1
fi

if ! pcs cluster setup --name "${CLUSTER_NAME}" "${NODES[@]}" \
        --start --enable --with-force; then
    echo "ERROR: Cluster setup failed" >&2
    exit 1
fi

# ─── Step 4: STONITH Configuration ──────────────────────────
echo "[4/6] Configuring fencing..."
for i in "${!NODES[@]}"; do
    local node="${NODES[$i]}"
    local ipmi_addr="${IPMI_ADDRESSES[$i]:-}"
    
    if [[ -n "${ipmi_addr}" ]]; then
        echo "  → Creating fence device for ${node} (IPMI: ${ipmi_addr})"
        pcs stonith create "fence-${node}" \
            stonith:fence_ipmilan \
            ipaddr="${ipmi_addr}" \
            login="${IPMI_LOGIN:-admin}" \
            passwd="${IPMI_PASS:-changeme}" \
            pcmk_host_list="${node}" \
            power_wait="5" \
            op monitor interval="60s" || true
    fi
done

pcs property set stonith-enabled=true 2>/dev/null || true
pcs property set pcmk_delay_base=30 2>/dev/null || true
pcs property set pcmk_delay_max=60 2>/dev/null || true

# ─── Step 5: Quorum Configuration ───────────────────────────
echo "[5/6] Configuring quorum..."
if [[ ${#NODES[@]} -eq 2 ]] && [[ -z "${QDEVICE_NODE}" ]]; then
    echo "  WARNING: Two-node cluster without qdevice — split-brain risk"
    echo "  Apply corosync two_node=1 in quorum configuration."
    pcs property set no-quorum-policy=stop 2>/dev/null || true
elif [[ -n "${QDEVICE_NODE}" ]]; then
    echo "  → Setting up qdevice on ${QDEVICE_NODE}"
    pcs qdevice setup alibi --init --nodes "${NODES[*]}" 2>/dev/null || true
    pcs property set no-quorum-policy=ignore 2>/dev/null || true
fi

# ─── Step 6: Verification ───────────────────────────────────
echo "[6/6] Verifying cluster state..."
sleep 5

if ! pcs cluster status >/dev/null 2>&1; then
    echo "ERROR: Cluster is not responding. Check corosync and pacemaker logs." >&2
    exit 1
fi

echo ""
echo "=== Cluster ${CLUSTER_NAME} Ready ==="
pcs status nodes || true
pcs stonith list || true
pcs property show stonith-enabled no-quorum-policy || true
```

### Pattern 2: Constraint Configuration (BAD vs. GOOD)

**BAD — Using resource groups when specific control is needed, missing ordering**

```bash
# ❌ BAD: Resource group forces implicit ordering you may not want,
#          and makes per-resource meta-options harder to manage
sudo pcs resource group add web-stack VirtualIP Apache WebSite
# Problem: You cannot set different monitor intervals or failure actions
#         for individual resources within a group. The group acts as one unit.

# ❌ BAD: Colocation without ordering — resources run together but may start in wrong order
sudo pcs constraint colocation add apache-with-vip VirtualIP Apache INFINITY
# Problem: Apache might attempt to start before the VIP exists,
#          causing bind failures even though they end up on the same node.
```

**GOOD — Explicit colocation AND ordering with resource-level options**

```bash
# ✅ GOOD: Separate resources with explicit constraints gives full control
#          over per-resource monitor intervals, failure actions, and meta-options

# Create resources independently with tuned operations
sudo pcs resource create VirtualIP ocf:heartbeat:IPaddr2 \
    ip="192.168.1.200" \
    cidr_netmask="24" \
    op monitor interval="30s" \
    meta failure-timeout="90s"

sudo pcs resource create Apache ocf:heartbeat:apache \
    configfile="/etc/httpd/conf/httpd.conf" \
    op monitor interval="60s" timeout="60s" \
    op start timeout="60s" \
    op stop timeout="60s" \
    meta failure-timeout="90s"

# Colocation constraint: run together on the same node
sudo pcs constraint colocation add apache-with-vip \
    VirtualIP Apache INFINITY

# Ordering constraint: define startup sequence explicitly
sudo pcs constraint order VirtualIP then Apache \
    kind=Mandatory score=INFINITY

# Location preference: prefer this node for VIP (for controlled failover)
sudo pcs constraint location VirtualIP prefers node1 INFINITY

# Verify the full constraint graph
pcs constraint list --full
crm_simulate -s  # Simulate to verify no conflicts
```

### Pattern 3: Cluster Diagnostic and Recovery Script

**Bash — Automated cluster diagnostics with safe recovery**

```bash
#!/usr/bin/env bash
# Pacemaker cluster diagnostic and recovery script
# Generates comprehensive diagnostics and offers safe recovery actions.
set -euo pipefail

readonly REPORT_DIR="/var/tmp/pacemaker-diagnostics"
readonly TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
mkdir -p "${REPORT_DIR}/${TIMESTAMP}"

echo "=== Pacemaker Cluster Diagnostics ==="
echo "Timestamp: ${TIMESTAMP}"

# ─── Collect diagnostic data ────────────────────────────────
collect() {
    local label="$1"; shift
    echo "[+] Collecting: ${label}"
    "$@" > "${REPORT_DIR}/${TIMESTAMP}/${label}.log" 2>&1 || true
}

collect "nodes_status"      pcs status nodes
collect "full_status"       pcs status
collect "resources_status"  pcs status resources
collect "corosync_status"   pcs status corosync
collect "quorum_status"     pcs status quorum
collect "stonith_list"      pcs stonith list
collect "stonith_config"    pcs stonith config 2>/dev/null || true
collect "constraints"       pcs constraint list --full
collect "properties"        pcs property show
collect "cib_dump"          pcs cluster cib 2>/dev/null || true

# ─── Generate crm_report (if available) ─────────────────────
if command -v crm_report &>/dev/null; then
    echo "[+] Generating crm_report..."
    crm_report -f "${REPORT_DIR}/${TIMESTAMP}/crm_report.tar.gz" 2>/dev/null || true
else
    echo "[-] crm_report not available — install pacemaker-cluster-libs"
fi

# ─── Collect logs ──────────────────────────────────────────
collect "corosync_log"   journalctl -u corosync --no-pager -n 500
collect "pacemaker_log"  journalctl -u pacemaker --no-pager -n 500
collect "pengine_log"    journalctl -u pacemaker-ngd --no-pager -n 500 2>/dev/null || \
                         journalctl -u pacemaker-schedulerd --no-pager -n 500

# ─── Analyze common issues ──────────────────────────────────
echo ""
echo "=== Analysis ==="

# Check for STONITH status
STONITH_ENABLED=$(pcs property show stonith-enabled 2>/dev/null | grep -o 'stonith-enabled=[a-z]*' || echo "unknown")
echo "STONITH: ${STONITH_ENABLED}"

if [[ "${STONITH_ENABLED}" == "stonith-enabled=false" ]]; then
    echo "  WARNING: STONITH is DISABLED — production clusters require fencing!"
fi

# Check for fenced nodes (nodes in uncertain state)
FENCED_COUNT=$(pcs status | grep -c 'fencing' || true)
if [[ ${FENCED_COUNT} -gt 0 ]]; then
    echo "  WARNING: Nodes have been or are being fenced"
fi

# Check resource failures
echo ""
echo "Resource fail counts:"
crm_failcount show -r 2>/dev/null || echo "  (crm_failcount not available)"

# ─── Offer safe recovery ──────────────────────────────────
echo ""
echo "=== Recovery Options ==="
echo "1. Cleanup all resource failures:    pcs resource cleanup"
echo "2. Cleanup specific resource:        pcs resource cleanup <resource_name>"
echo "3. Clear failcount for a resource:   crm_failcount delete -r <resource> [node]"
echo "4. Force stop/start of a resource:   pcs resource manage <name>"
echo ""
echo "Diagnostic report saved to: ${REPORT_DIR}/${TIMESTAMP}/"

# Compress the report
tar czf "${REPORT_DIR}/cluster-diagnostic-${TIMESTAMP}.tar.gz" \
    -C "${REPORT_DIR}" "${TIMESTAMP}" 2>/dev/null || true
rm -rf "${REPORT_DIR}/${TIMESTAMP}"

echo "Compressed: ${REPORT_DIR}/cluster-diagnostic-${TIMESTAMP}.tar.gz"
```

### Pattern 4: Promotable Clone Master/Slave Configuration (BAD vs. GOOD)

**BAD — Missing notify and proper clone parameters causes failed failover**

```bash
# ❌ BAD: Missing notify=true means the application doesn't know when
#         promotion status changes, causing it to read from a degraded replica
sudo pcs resource create db-storage ocf:linbit:drbd \
    drbd_resource=db0 \
    op monitor interval="30s" role=Slave

sudo pcs resource master db-master db-storage \
    master-max=1 clone-max=2
# Problems:
# - No role-specific monitor operations (Slave vs. Master)
# - Missing notify=true — dependents won't track promotion changes
# - No clone-node-max limit — could allow multiple masters

# ❌ BAD: Application resource has no dependency tracking
sudo pcs resource create db-app ocf:heartbeat:lsb:postgresql \
    op monitor interval="30s"
# Problem: db-app might start on a node where the DB is still Slave
```

**GOOD — Properly configured with all required parameters**

```bash
# ✅ GOOD: Full DRBD + PostgreSQL master/slave pattern
# Step 1: DRBD with explicit role-based monitor operations
sudo pcs resource create db-storage ocf:linbit:drbd \
    drbd_resource=db0 \
    op monitor interval="30s" role=Slave \
    op monitor interval="20s" role=Master \
    op promote interval="0s" role=Master \
    op demote interval="0s" role=Slave

# Step 2: Promotable clone with correct parameters and notify
sudo pcs resource master db-master db-storage \
    master-max=1 \
    master-node-max=1 \
    clone-max=2 \
    clone-node-max=1 \
    notify=true

# Step 3: Database service tied to the master role
sudo pcs resource create PostgreSQL ocf:heartbeat:pgsql \
    pghost="/var/run/postgresql" \
    pguser="postgres" \
    repmode="sync" \
    sync_level="1" \
    op monitor interval="30s" timeout="60s" \
    op start timeout="120s" \
    op stop timeout="60s"

# Step 4: Colocation enforces PostgreSQL runs only on master
sudo pcs constraint colocation add pg-with-db-master \
    PostgreSQL with db-master INFINITY

# Step 5: Ordering ensures DB starts after DRBD promotes
sudo pcs constraint order db-master then PostgreSQL kind=Mandatory

# Step 6: VirtualIP follows the database (not the storage layer)
sudo pcs resource create DatabaseVIP ocf:heartbeat:IPaddr2 \
    ip="192.168.1.50" cidr_netmask="24" \
    op monitor interval="30s"

sudo pcs constraint colocation add vip-with-pg \
    DatabaseVIP with PostgreSQL INFINITY
sudo pcs constraint order PostgreSQL then DatabaseVIP kind=Mandatory
```

---

## Constraints

### MUST DO

- **MUST** configure STONITH (fencing) on every production cluster — never run Pacemaker without fencing in production; Red Hat certification requires it
- **MUST** set `pcmk_delay_base` and `pcmk_delay_max` properties for clusters with multiple simultaneous fence targets to prevent race conditions
- **MUST** define both colocation AND ordering constraints when resources must share a node — colocation alone does NOT guarantee startup sequence
- **MUST** use `pcs resource cleanup` after recovering a node to clear stale failcounts and let the scheduler re-evaluate placements
- **MUST** test all fence devices with `pcs stonith fence <node> --force` before declaring the cluster production-ready
- **MUST** configure quorum strategy appropriate to cluster size — two-node clusters need qdevice or corosync `two_node` mode
- **MUST** use `pcs resource describe <type>` and `pcs stonith describe <type>` to discover valid parameters before creating resources
- **MUST** use `crm_report -f report.tar.gz` for diagnostics when troubleshooting unexpected behavior; include the report when seeking external support
- **MUST** enable monitor operations on every resource with appropriate intervals — unmonitored resources will not be recovered after failures

### MUST NOT DO

- **MUST NOT** disable STONITH in production (`pcs property set stonith-enabled=false`) — unfenced clusters risk data corruption from split-brain scenarios
- **MUST NOT** edit the CIB directly with `cibadmin` for configuration changes — use `pcs`, `crm_shadow`, or `cib-push --diff-against` instead
- **MUST NOT** assume colocation implies ordering — they are separate constraint types; define both explicitly
- **MUST NOT** skip quorum planning for two-node clusters — without qdevice or `two_node: 1`, split-brain will cause data corruption on shared storage
- **MUST NOT** use resource groups (`pcs resource group add`) when you need per-resource control over monitor intervals, failure actions, or meta-options
- **MUST NOT** run `pcs cluster destroy` on a node that is actively fencing — ensure resources have already migrated before destroying the cluster
- **MUST NOT** set `no-quorum-policy=fence` as a default policy — this will fence ALL nodes if quorum is lost, causing cascading outages
- **MUST NOT** create promotable clones without `notify=true` — dependent resources won't track promotion changes and may start on Slave nodes

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `corosync` | Configure Corosync messaging layer, membership, quorum, and network settings that Pacemaker depends on |
| `linux-services` | Define systemd unit files that can be used as LSB or systemd OCF resource agents within Pacemaker |
| `storage-architecture` | Design shared storage layouts (DRBD, LVM, multipath) for HA cluster workloads |
| `observability` | Set up monitoring and alerting for cluster state, fencing events, and resource transitions |

---

## Live References

> Authoritative documentation links for Pacemaker HA clustering. The model follows markdown links at load time to resolve external references and inline content.

- [Pacemaker Documentation Index](https://www.clusterlabs.org/pacemaker/doc/) — Official doc index with all versions
- [Clusters from Scratch (Corosync + Pacemaker)](https://clusterlabs.org/projects/pacemaker/doc/2.1/Clusters_from_Scratch/singlehtml/) — Step-by-step cluster building guide
- [Pacemaker Administration Guide](https://clusterlabs.org/projects/pacemaker/doc/2.1/Pacemaker_Administration/singlehtml/) — Full administration reference including pcs and crmsh
- [Pacemaker Explained (CIB/XML Reference)](https://www.clusterlabs.org/pacemaker/doc/2.1/Pacemaker_Explained/singlehtml/) — CIB schema, resource agent conventions, constraint model
- [PCS Source Repository](https://github.com/ClusterLabs/pcs) — pcs command source code and issues tracker
- [PCS ↔ crmsh Feature Comparison](https://clusterlabs.org/projects/pacemaker/doc/2.1/Pacemaker_Administration/epub/pcs-crmsh.xhtml) — Side-by-side command mapping between pcs and crmsh
- [RHEL 9 High Availability Cluster Documentation](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/configuring_and_managing_high_availability_clusters/index) — Red Hat's official HA cluster guide with production best practices
