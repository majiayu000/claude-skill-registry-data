---
name: corosync
description: Configures Corosync Cluster Engine v3.x messaging layer including totem protocol, quorum models, nodelist management, knet/udpu transports, and security for Pacemaker HA clusters.
license: MIT
compatibility: opencode
metadata:
  version: "1.0.0"
  domain: linux
  role: implementation
  scope: infrastructure
  output-format: code
  content-types: [code, guidance, config, do-dont]
  triggers: corosync, totem protocol, quorum management, cluster messaging, knet transport, udpu unicast, nodelist configuration, qdevice
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
  related-skills: pacemaker, linux-services, networking
  maturity: stable
  completeness: 95
  exampleCount: 4
---

# Corosync Cluster Engine Configuration

Senior Linux infrastructure engineer configuring Corosync v3.x as the cluster messaging layer for Pacemaker HA clusters. Covers totem protocol setup, transport selection (knet/udpu/mcast), quorum models with qdevice, nodelist management, security hardening, logging, and cluster diagnostics.

## TL;DR Checklist

- [ ] Choose transport (knet default, udpu for multicast-blocked networks) before writing corosync.conf
- [ ] Assign unique nodeid to every node in the nodelist — no gaps, no duplicates
- [ ] Configure crypto_cipher + crypto_hash for production clusters on untrusted networks
- [ ] Set quorum strategy appropriate to cluster size (two_node: 1 for two-node, qdevice recommended)
- [ ] Enable logging with timestamp and rotate logfile_max_lines for operational visibility
- [ ] Verify membership with `corosync-cfgtool -s` and quorum with `corosync-quorumtool -s` after every change

---

## When to Use

Use this skill when:

- **Configuring Corosync from scratch** — You're building the cluster messaging layer that Pacemaker depends on, and need transport, nodelist, quorum, and security settings
- **Migrating transports** — Your existing mcast-based cluster needs switching to knet or udpu due to multicast being blocked by firewalls or switches
- **Resolving membership issues** — Nodes are not joining the membership ring; you need to diagnose transport failures, ring timeouts, or network partitions
- **Hardening cluster security** — You must enable encrypted transport (crypto_cipher + crypto_hash) and generate/distribute authkeys across all nodes
- **Configuring quorum for two-node clusters** — You need qdevice setup or `two_node` mode to prevent split-brain scenarios
- **Troubleshooting runtime state** — Membership count is wrong, expected_votes is stale, or CPG groups are not forming correctly
- **Setting up logging and monitoring** — You need proper corosync logging configuration with syslog integration, debug toggles, and log rotation
- **Reading runtime configuration** — You need to inspect the in-memory config database (cmap) for ring addresses, transport status, or node counts

---

## When NOT to Use

Avoid this skill for:

- **Pacemaker resource management** — Use `pacemaker` instead; Corosync handles messaging only, not resources or constraints
- **Kubernetes clustering** — Use Kubernetes native control-plane HA (etcd) instead of Corosync
- **Application-level replication** — Corosync provides cluster membership and message passing, not data replication between databases or filesystems
- **Load balancing** — Use HAProxy, Nginx, or cloud load balancers; Corosync manages node membership, not traffic routing

Use `pacemaker` for configuring resources, constraints, and fencing on top of the Corosync messaging layer. Use `networking` for switch/firewall rules that may affect multicast transport.

---

## Core Workflow

### 1. Choose Transport Layer

The transport determines how cluster members communicate. Choose based on your network capabilities.

```bash
# knet — Modern default (recommended for all new clusters)
# Supports multiple redundant links, IPv6, TCP fallback, and UDP multicast replacement

# udpu — Unicast UDP (use when multicast is blocked by firewalls or switches)
# Every node explicitly lists every other node's ring address

# mcast — Legacy traditional multicast (only available with kmod-based corosync)
# Deprecated; use knet unless you have a specific legacy requirement
```

**Checkpoint:** Confirm multicast works on your network before choosing mcast/knet:
```bash
# Test multicast connectivity from one node to another
ping -M do -s 1472 <mcastaddr> -I <bindnetaddr>  # MTU test with DF bit set
# Or use mtrace for multicast route verification
mtrace <source_ip> <mcastaddr>
```

### 2. Generate Corosync Configuration

Write the complete `corosync.conf` with totem, transport, nodelist, quorum, and logging sections.

```toml
totem {
    version: 2
    cluster_name: MyCluster
    transport: knet              # or 'udpu' or omit for default (knet)

    crypto_cipher: aes256        # Enable for encrypted transport on untrusted networks
    crypto_hash: sha256          # HMAC for message integrity authentication

    interface {
        ringnumber: 0
        mcastaddr: 226.94.1.1
        mcastport: 5405
        ttl: 1
    }
}

quorum {
    provider: corosync_votequorum
    expected_votes: 1            # Usually left at 1 — corosync auto-calculates from nodelist
    two_node: 1                  # For two-node clusters; reduces split-brain risk
}

nodelist {
    node {
        name: cluster-node-1
        nodeid: 1
        ring0_addr: 192.168.1.11
    }
    node {
        name: cluster-node-2
        nodeid: 2
        ring0_addr: 192.168.1.12
    }
}

logging {
    to_stderr: yes
    to_logfile: yes
    logfile: /var/log/cluster/corosync.log
    logfile_max_lines: 100000    # Rotate after N lines
    logfile_ensure_dir: yes      # Create log directory automatically
    to_syslog: yes
    debug: off                   # Enable for troubleshooting only — extremely verbose!
    timestamp: on
    logger_subsys {
        subsys: AMF
        debug: off
    }
}
```

**Checkpoint:** Validate syntax with `corosync-cmaptool` or by starting corosync in dry-run mode. Verify the nodelist has unique nodeids with no gaps, and the cluster_name is consistent across all nodes.

### 3. Generate Authentication Key

If crypto_cipher is set, every node must have the same authkey.

```bash
# Generate a new key on the first node (or wherever you manage configs)
sudo corosync-keygen

# This produces /etc/corosync/authkey with binary content
# Set restrictive permissions immediately
sudo chmod 600 /etc/corosync/authkey
sudo chown root:root /etc/corosync/authkey

# Distribute the key to all other cluster nodes using a secure method
for node in cluster-node-2 cluster-node-3; do
    scp /etc/corosync/authkey "root@${node}:/etc/corosync/authkey"
    ssh root@"${node}" chmod 600 /etc/corosync/authkey
done
```

**Checkpoint:** Verify the authkey is identical on all nodes:
```bash
# On each node, compare the md5sum — they must match exactly
md5sum /etc/corosync/authkey
```

### 4. Deploy Configuration and Start Cluster

Apply the configuration to every node and start the cluster.

```bash
# Copy config to all nodes (must be identical on every node)
for node in cluster-node-1 cluster-node-2; do
    scp /etc/corosync/corosync.conf "root@${node}:/etc/corosync/corosync.conf"
    scp /etc/corosync/authkey "root@${node}:/etc/corosync/authkey"
done

# Start corosync on every node
for node in cluster-node-1 cluster-node-2; do
    ssh root@"${node}" systemctl enable --now corosync
done

# Verify membership has formed
corosync-cfgtool -s           # Show current membership status
corosync-quorumtool -s        # Show quorum state and vote counts
```

**Checkpoint:** `corosync-cfgtool -s` shows all nodes as members with the expected node count. `corosync-quorumtool -s` shows quorum is active (green). If membership is incomplete, check `/var/log/cluster/corosync.log` on both nodes for transport-level errors.

### 5. Configure Quorum Strategy

Two-node clusters need special handling to prevent split-brain. Multi-node clusters rely on majority quorum by default.

```bash
# OPTION A — Two-node cluster: enable two_node mode in corosync.conf
# Add 'two_node: 1' to the quorum section — this changes expected_votes behavior
# so the cluster can remain operational even with one node down

# OPTION B — Two-node cluster: deploy qdevice (recommended for production)
# qdevice acts as a third-party arbiter that breaks ties during network partitions
sudo pcs qdevice setup alibi --init --nodes cluster-node-1,cluster-node-2

# OPTION C — Multi-node cluster (3+ nodes): default majority quorum is sufficient
# No extra configuration needed; corosync votes automatically from nodelist count

# After qdevice setup, set the no-quorum-policy to allow continued operation
sudo pcs property set no-quorum-policy=ignore
```

**Checkpoint:** `corosync-quorumtool -s` shows the correct expected_votes and current node_count. For qdevice clusters, verify the qdevice node appears in the quorum output with its voting status.

---

## Implementation Patterns

### Pattern 1: Complete Corosync Configuration Generator (BAD vs. GOOD)

**BAD — Minimal config with hardcoded values, no transport choice, no logging rotation, missing security**

```toml
# ❌ BAD: No transport specified, no encryption, no log rotation,
#          incomplete nodelist, no quorum strategy

totem {
    version: 2
    cluster_name: MyCluster
    interface {
        ringnumber: 0
        bindnetaddr: 192.168.1.0
        mcastaddr: 226.94.1.1
        mcastport: 5405
    }
}

nodelist {
    node {
        name: cluster-node-1
        nodeid: 1
        ring0_addr: 192.168.1.11
    }
}

# Problems:
# - No transport specified (defaults to knet but should be explicit)
# - No crypto settings — unencrypted cluster messages on production network
# - Only one node in nodelist — no quorum possible
# - No logging section at all — no operational visibility
# - No quorum section — uses defaults that may not be appropriate
# - Missing logfile_ensure_dir, logfile_max_lines for log management
```

**GOOD — Complete, production-ready with explicit transport, encryption, logging, and quorum**

```bash
#!/usr/bin/env bash
# Production Corosync configuration generator
# Generates a complete corosync.conf with best practices applied.
# Usage: ./gen-corosync-conf.sh <cluster_name> <bindnetaddr> <mcastaddr> <mcastport> node1_addr node2_addr [node3_addr...] [--encrypt]
set -euo pipefail

readonly CLUSTER_NAME="${1:?Usage: $0 <cluster_name> <bindnet> <mcastaddr> <mcastport> node_addrs... [--encrypt]}"
readonly BINDNETADDR="$2"
readonly MCASTADDR="$3"
readonly MCASTPORT="${4:-5405}"
readonly ENCRYPT_FLAG="${6:-no}"

# Collect nodes from remaining positional arguments (skip --encrypt flag)
NODE_ADDRS=()
for arg in "$@"; do
    case "$arg" in
        --encrypt|"$1"|"$2"|"$3"|"$4") continue ;;
        *) NODE_ADDRS+=("$arg") ;;
    esac
done

if [[ ${#NODE_ADDRS[@]} -lt 2 ]]; then
    echo "ERROR: At least 2 node addresses required" >&2
    exit 1
fi

readonly NUM_NODES=${#NODE_ADDRS[@]}

# Determine transport based on environment
TRANSPORT="knet"
if grep -qE 'multicast.*(no|disabled|false)' /etc/sysconfig/iptables 2>/dev/null || \
   ! ip maddr show >/dev/null 2>&1; then
    TRANSPORT="udpu"
    echo "WARNING: Multicast appears unavailable, using udpu transport" >&2
fi

# Generate config
CONF_FILE="/etc/corosync/corosync.conf"
mkdir -p "$(dirname "$CONF_FILE")"

cat > "${CONF_FILE}" <<EOF
totem {
    version: 2
    cluster_name: "${CLUSTER_NAME}"
    transport: ${TRANSPORT}

${[[ "${ENCRYPT_FLAG}" == "--encrypt" ]] && echo '    crypto_cipher: aes256' || echo '    crypto_cipher: none'}
${[[ "${ENCRYPT_FLAG}" == "--encrypt" ]] && echo '    crypto_hash: sha256'   || echo '    crypto_hash: none'}

    interface {
        ringnumber: 0
EOF

if [[ "${TRANSPORT}" != "udpu" ]]; then
    cat >> "${CONF_FILE}" <<EOF
        mcastaddr: ${MCASTADDR}
        mcastport: ${MCASTPORT}
        ttl: 1
EOF
else
    echo '        # udpu mode: no multicast — node addresses are in nodelist below' >> "${CONF_FILE}"
fi

cat >> "${CONF_FILE}" <<EOF
    }
}

quorum {
    provider: corosync_votequorum
    expected_votes: 1
    two_node: $([[ ${NUM_NODES} -eq 2 ]] && echo '1' || echo '0')
}

nodelist {
EOF

NODEID=1
for addr in "${NODE_ADDRS[@]}"; do
    cat >> "${CONF_FILE}" <<EOF
    node {
        name: node-${NODEID}
        nodeid: ${NODEID}
        ring0_addr: ${addr}
    }
EOF
    NODEID=$((NODEID + 1))
done

cat >> "${CONF_FILE}" <<EOF
}

logging {
    to_stderr: yes
    to_logfile: yes
    logfile: /var/log/cluster/corosync.log
    logfile_max_lines: 100000
    logfile_ensure_dir: yes
    to_syslog: yes
    debug: off
    timestamp: on
}
EOF

chmod 644 "${CONF_FILE}"
echo "Generated ${CONF_FILE} (${NUM_NODES} nodes, transport: ${TRANSPORT})"
echo "Apply to all cluster nodes and generate authkey with: corosync-keygen"
```

### Pattern 2: Knet Multi-Link Configuration (BAD vs. GOOD)

**BAD — Single-link knet config that does not leverage redundancy**

```toml
# ❌ BAD: No redundant links configured — a single NIC failure breaks the cluster
totem {
    version: 2
    cluster_name: MyCluster
    transport: knet

    interface {
        ringnumber: 0
        mcastaddr: 226.94.1.1
        mcastport: 5405
        ttl: 1
    }
}
# Problems:
# - Single link means single point of failure for cluster communication
# - No knet.link configuration for redundant paths over different NICs
# - Does not utilize multi-homed network infrastructure available on most servers
```

**GOOD — Dual-link knet with independent paths over separate NICs**

```toml
# ✅ GOOD: Dual redundant links using knet, each on a different physical network
totem {
    version: 2
    cluster_name: MyCluster
    transport: knet

    interface {
        ringnumber: 0
        mcastaddr: 226.94.1.1
        mcastport: 5405
        ttl: 1
    }

    link {
        number: 0
        interface {
            bindnetaddr: 192.168.1.0      # Primary management network
            mcastaddr: 226.94.1.1
            mcastport: 5405
            ttl: 1
        }
    }

    link {
        number: 1
        interface {
            bindnetaddr: 192.168.2.0      # Secondary replication network
            mcastaddr: 226.94.2.1
            mcastport: 5406
            ttl: 1
        }
    }
}

nodelist {
    node {
        name: cluster-node-1
        nodeid: 1
        ring0_addr: 192.168.1.11          # Primary address (management)
    }
    node {
        name: cluster-node-2
        nodeid: 2
        ring0_addr: 192.168.1.12
    }
}
```

### Pattern 3: UDPU Transport for Multicast-Blocked Networks (BAD vs. GOOD)

**BAD — Trying to use multicast transport when switches block multicast**

```toml
# ❌ BAD: Multicast transport in an environment where switches drop multicast packets
#          or firewalls block IGMP/UDP multicast ports — cluster will never form
totem {
    version: 2
    cluster_name: MyCluster
    # transport omitted, defaults to knet with mcast

    interface {
        ringnumber: 0
        bindnetaddr: 192.168.1.0
        mcastaddr: 226.94.1.1           # This will fail if multicast is blocked
        mcastport: 5405
    }
}
# Problems:
# - Multicast packets silently dropped → nodes never see each other's membership messages
# - Symptoms: corosync.log shows "totem: Unable to initialize membership" on all nodes
# - No explicit transport declared, so the default knet/mcast fails in silence
```

**GOOD — Explicit udpu transport with every node listed by unicast address**

```toml
# ✅ GOOD: UDPU (Unicast UDP) explicitly configured for multicast-blocked environments
totem {
    version: 2
    cluster_name: MyCluster
    transport: udpu                   # Explicitly declare unicast UDP transport

    interface {
        ringnumber: 0
        bindnetaddr: 192.168.1.0      # Network range for binding
        mcastport: 5405               # Port used for all inter-node communication
    }
}

quorum {
    provider: corosync_votequorum
    expected_votes: 1
    two_node: 1                       # Two-node udpu cluster needs this flag
}

nodelist {
    node {
        name: cluster-node-1
        nodeid: 1
        ring0_addr: 192.168.1.11      # Every node MUST list every other node
    }                             # by unicast address — no multicast discovery
    node {
        name: cluster-node-2
        nodeid: 2
        ring0_addr: 192.168.1.12
    }
}
```

### Pattern 4: Cluster Diagnostics and Troubleshooting Script

**Bash — Automated diagnostics for membership, quorum, and transport health**

```bash
#!/usr/bin/env bash
# Corosync cluster diagnostics script
# Collects membership status, quorum state, runtime config, and log analysis.
set -euo pipefail

readonly REPORT_DIR="/var/tmp/corosync-diagnostics"
readonly TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
mkdir -p "${REPORT_DIR}/${TIMESTAMP}"

echo "=== Corosync Cluster Diagnostics ==="
echo "Timestamp: ${TIMESTAMP}"
echo "Hostname:  $(hostname)"
echo ""

# ─── Collect diagnostics data ──────────────────────────────
collect() {
    local label="$1"; shift
    echo "[+] Collecting: ${label}"
    "$@" > "${REPORT_DIR}/${TIMESTAMP}/${label}.log" 2>&1 || true
}

collect "cfgtool_status"       corosync-cfgtool -s
collect "cmap_full"            corosync-cmaptool dump
collect "quorum_status"        corosync-quorumtool -s
collect "cpgtool"              corosync-cpgtool || true
collect "corosync_config"      cat /etc/corosync/corosync.conf
collect "authkey_present"      [[ -f /etc/corosync/authkey ]] && echo "authkey exists" || echo "authkey MISSING"

# Runtime cmap queries for specific fields
echo "--- Runtime CMap Queries ---" > "${REPORT_DIR}/${TIMESTAMP}/cmap_key_fields.log"
for key in \
    "totem.interface.0.mcastaddr" \
    "totem.interface.0.mcastport" \
    "totem.protocol_id" \
    "runtime.quorum.current_expected_votes" \
    "runtime.nodelist.node_count" \
    "runtime.membership.membership_count" \
    "runtime.config.config_version"; do
    result=$(corosync-cmaptool get "${key}" 2>/dev/null || echo "KEY_NOT_FOUND")
    echo "${key} = ${result}" >> "${REPORT_DIR}/${TIMESTAMP}/cmap_key_fields.log"
done

# ─── Collect logs ──────────────────────────────────────────
collect "corosync_log_recent"   tail -n 500 /var/log/cluster/corosync.log 2>/dev/null || true
collect "corosync_log_errors"   grep -iE 'error|fail|warn|critical' /var/log/cluster/corosync.log 2>/dev/null | tail -n 100 || echo "No errors found in recent log" > "${REPORT_DIR}/${TIMESTAMP}/corosync_log_errors.log"

# ─── Analysis ──────────────────────────────────────────────
echo ""
echo "=== Analysis ==="

# Check membership
MEM_COUNT=$(grep -c 'Number of ring members' "${REPORT_DIR}/${TIMESTAMP}/cfgtool_status.log" 2>/dev/null || echo "0")
if [[ "${MEM_COUNT}" -gt 0 ]]; then
    ACTUAL_MEMBERS=$(grep 'Number of ring members' "${REPORT_DIR}/${TIMESTAMP}/cfgtool_status.log" | awk '{print $NF}')
    CONFIG_NODES=$(grep -c 'nodeid:' /etc/corosync/corosync.conf)
    echo "Membership: ${ACTUAL_MEMBERS} nodes active out of ${CONFIG_NODES} configured"
    if [[ "${ACTUAL_MEMBERS}" -lt "${CONFIG_NODES}" ]]; then
        echo "  WARNING: Membership count (${ACTUAL_MEMBERS}) is less than configured nodes (${CONFIG_NODES})"
        echo "  Possible causes: transport failure, firewall blocking multicast, authkey mismatch"
    fi
else
    echo "  ERROR: Unable to read membership status"
fi

# Check quorum
if command -v corosync-quorumtool &>/dev/null; then
    QUORUM_STATUS=$(corosync-quorumtool -s 2>/dev/null | grep 'Quorum' || echo "Unknown")
    echo "Quorum: ${QUORUM_STATUS}"
fi

# Check for common log errors
ERRORS=0
if [[ -f "${REPORT_DIR}/${TIMESTAMP}/corosync_log_errors.log" ]]; then
    ERRORS=$(wc -l < "${REPORT_DIR}/${TIMESTAMP}/corosync_log_errors.log")
fi
echo "Recent error/warning count in logs: ${ERRORS}"

# ─── Common troubleshooting checklist ──────────────────────
echo ""
echo "=== Troubleshooting Checklist ==="

if [[ -f /etc/corosync/authkey ]]; then
    AUTHKEY_PERMS=$(stat -c '%a' /etc/corosync/authkey 2>/dev/null || echo "unknown")
    if [[ "${AUTHKEY_PERMS}" != "600" ]]; then
        echo "[!] authkey permissions are ${AUTHKEY_PERMS}, should be 600"
    else
        echo "[✓] authkey has correct permissions (600)"
    fi
else
    echo "[✗] authkey file is missing — cluster cannot authenticate if encryption is enabled"
fi

# Check for config_version issues
if grep -q 'config_version' /etc/corosync/corosync.conf 2>/dev/null; then
    echo "[✓] config_version found in totem section"
else
    echo "[!] No config_version in totem — corosync may refuse to apply runtime changes"
fi

# Compress and output report path
tar czf "${REPORT_DIR}/corosync-diagnostics-${TIMESTAMP}.tar.gz" \
    -C "${REPORT_DIR}" "${TIMESTAMP}" 2>/dev/null || true
rm -rf "${REPORT_DIR}/${TIMESTAMP}"
echo ""
echo "Report saved to: ${REPORT_DIR}/corosync-diagnostics-${TIMESTAMP}.tar.gz"
```

---

## Constraints

### MUST DO

- **MUST** explicitly declare the transport in the totem section (`transport: knet | udpu`) rather than relying on the default — explicit configuration prevents silent failures when network capabilities differ between environments
- **MUST** assign a unique `nodeid` to every node in the nodelist with no gaps (1, 2, 3...) and no duplicates — duplicate nodeids cause membership chaos
- **MUST** ensure the authkey file (`/etc/corosync/authkey`) is identical on all cluster nodes when crypto_cipher is enabled — mismatched keys cause authentication failures during membership formation
- **MUST** set `chmod 600 /etc/corosync/authkey` immediately after generation — the key contains cryptographic material and must not be readable by other users
- **MUST** configure quorum strategy appropriate to cluster size — two-node clusters require either `two_node: 1` or qdevice; multi-node clusters use default majority quorum
- **MUST** enable logging with `logfile_ensure_dir: yes` and `logfile_max_lines` for log rotation so cluster state is always observable after a crash
- **MUST** verify membership formation with `corosync-cfgtool -s` and quorum with `corosync-quorumtool -s` before introducing Pacemaker resources on the cluster
- **MUST** use `pcs` to manage corosync configuration changes (handles config_version auto-increment) — never edit corosync.conf manually at runtime without incrementing config_version
- **MUST** enable `timestamp: on` in the logging section so log messages are time-synchronized and debuggable across nodes

### MUST NOT DO

- **MUST NOT** use mcast transport unless you have verified multicast works end-to-end on your physical network infrastructure — switches often drop IGMP or UDP multicast packets silently
- **MUST NOT** edit corosync.conf directly during runtime without incrementing `config_version` in the totem section — corosync will refuse to apply the change and log an error
- **MUST NOT** run Corosync as root on production systems where a dedicated service user is available through systemd's User= directive (though Corosync requires root for network socket creation)
- **MUST NOT** rely on default `expected_votes` without reviewing whether `two_node: 1` or qdevice is needed — incorrect quorum configuration leads to split-brain in two-node setups
- **MUST NOT** enable `debug: true` in the logging section on production systems — it generates extremely verbose output that fills disk and degrades performance
- **MUST NOT** configure udpu transport with fewer than 2 nodes listed in nodelist — udpu has no multicast discovery mechanism; every node must explicitly know every other node's address
- **MUST NOT** change the cluster_name between nodes — all members of a cluster must share the identical cluster_name string to join the same membership ring
- **MUST NOT** skip testing membership formation with `corosync-cfgtool -l` after adding new interfaces or changing bindnetaddr values

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `pacemaker` | Manage Pacemaker resources, constraints, and fencing that run on top of the Corosync messaging layer |
| `linux-services` | Configure systemd units for Corosync service management, overrides, and integration with boot ordering |
| `networking` | Diagnose multicast connectivity, firewall rules, and network interfaces affecting cluster communication |

---

## Live References

> Authoritative documentation links for Corosync Cluster Engine. The model follows markdown links at load time to resolve external references and inline content.

- [Corosync Official Site](https://corosync.github.io/corosync/) — Project homepage with downloads, version history, and project status
- [corosync.conf Example Configuration](https://github.com/corosync/corosync/blob/main/conf/corosync.conf.example) — Canonical example config from the Corosync source repository
- [corosync.conf(5) Man Page](https://www.mankier.com/5/corosync.conf) — Complete reference for every configuration directive, transport option, and section
- [Corosync Overview (Man 7)](https://manpages.debian.org/unstable/corosync/corosync_overview.7.en.html) — Architecture overview covering totem protocol, CPG, quorum engine, and runtime data model
- [Corosync v3.1.10 Release](https://github.com/corosync/corosync/releases/tag/v3.1.10) — Latest stable release notes including CVE-2025-30472 fix and changelog
- [Corosync Source Repository](https://github.com/corosync/corosync) — Full source code, issue tracker, and development roadmap (including 4.x status)
- [Pacemaker + Corosync Architecture Guide](https://clusterlabs.org/pacemaker/doc/2.1/Pacemaker_Explained/singlehtml/) — How Pacemaker leverages the Corosync membership service and CPG for cluster operations
