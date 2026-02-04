---
name: kubekey
description: "Manage Kubernetes clusters with KubeKey: check installation, install KubeKey, create clusters, scale nodes, upgrade clusters, and view configurations. Use when working with Kubernetes cluster deployment, management, or when the user mentions KubeKey, kk, or Kubernetes cluster operations."
license: MIT
compatibility: "Requires Linux or macOS, SSH access to nodes, and network connectivity. KubeKey tool (kk) should be installed or will be installed by the skill."
---

# KubeKey Skill

## Description

KubeKey is a tool for deploying Kubernetes clusters. This skill provides capabilities to check, install KubeKey, create and scale Kubernetes clusters, and view cluster configurations.

## Capabilities

This skill enables the agent to:

1. **Check KubeKey installation**: Verify if KubeKey is installed and check its version
2. **Install KubeKey**: Download and install KubeKey tool with specified version
3. **Generate cluster configurations**: Create KubeKey cluster configuration files based on user requirements, including:
   - Kubernetes version selection
   - CNI (Container Network Interface) plugin selection
   - CRI (Container Runtime Interface) selection
   - Network CIDR configuration
   - Node role assignment
   - Registry configuration
4. **Create Kubernetes clusters**: Deploy new Kubernetes clusters using KubeKey configuration files
5. **Scale clusters**: Add nodes using `kk add nodes` or remove nodes using `kk delete node` from existing Kubernetes clusters
6. **Upgrade clusters**: Upgrade Kubernetes and optionally KubeSphere to newer versions
7. **View cluster configurations**: Display and analyze cluster installation configurations

## Instructions

When the user needs to work with KubeKey or Kubernetes cluster management:

### Checking KubeKey Installation

1. Run the check script: `scripts/check_kubekey.sh`
2. The script will check if `kk` command is available in PATH
3. If installed, it will display the version
4. If not installed, provide guidance on installation

### Installing KubeKey

1. Determine the desired version (default: latest)
2. Run the install script: `scripts/install_kubekey.sh [VERSION]`
3. The script will:
   - Download KubeKey from GitHub releases
   - Extract and install to `/usr/local/bin/kk`
   - Verify installation
4. Ensure the user has appropriate permissions (may require sudo)

### Creating a Kubernetes Cluster Configuration

When the user wants to create a Kubernetes cluster, you need to gather requirements and generate a configuration file. Follow this process:

#### Step 1: Gather Cluster Requirements

Ask the user or infer from context the following information:

**Essential Information:**
- **Node Information**: 
  - IP addresses of all nodes
  - SSH credentials (username, password, or SSH key path)
  - Node roles (master/worker/etcd)
  - Internal IP addresses (if different from external)
  
**Kubernetes Configuration:**
- **Kubernetes Version**: 
  - Common versions: v1.28.x, v1.27.x, v1.26.x, v1.25.x
  - If not specified, recommend latest stable (v1.28.x)
  - Format: `v1.28.0` (with 'v' prefix)
  
- **Container Runtime Interface (CRI)**:
  - Options: `docker`, `containerd`, `cri-o`, `isula`
  - Default: `containerd` (recommended for newer K8s versions)
  - Docker: Traditional, widely used
  - Containerd: Lightweight, CNCF standard
  
- **Network Plugin (CNI)**:
  - Options: `calico`, `flannel`, `cilium`, `kube-ovn`, `weave`
  - **Calico**: Best for production, supports network policies, BGP routing
  - **Flannel**: Simple, good for small clusters
  - **Cilium**: eBPF-based, high performance
  - **Kube-OVN**: Advanced networking features
  - **Weave**: Simple, automatic mesh networking
  - Default: `calico` (if not specified)
  
- **Pod CIDR**: 
  - Default: `10.233.64.0/18` (if not specified)
  - Should not overlap with service CIDR
  - Calculate based on expected pod count: `/18` = ~16k pods, `/16` = ~65k pods
  
- **Service CIDR**: 
  - Default: `10.233.0.0/18` (if not specified)
  - Should not overlap with pod CIDR or node networks
  
- **Control Plane Endpoint**:
  - Load balancer domain or IP (for HA)
  - Or leave empty for single master
  - Port: typically `6443`

**Optional Advanced Settings:**
- **Image Registry**: 
  - Private registry URL (if using private registry)
  - Registry mirrors (for faster downloads in China)
  - Insecure registries list
  
- **Proxy Mode**: 
  - `iptables` (default, simpler)
  - `ipvs` (better performance for large clusters)
  
- **Max Pods per Node**: 
  - Default: `110`
  - Calculate: (available IPs in node CIDR) - 1
  
- **Node CIDR Mask Size**: 
  - Default: `24`
  - Determines subnet size for each node

#### Step 2: Generate Configuration File

1. Use the configuration template in `examples/cluster-config.yaml` as a base
2. Use the script `scripts/generate_config.sh` to interactively generate a config, OR
3. Manually create the YAML file with the following structure:

```yaml
apiVersion: kubekey.kubesphere.io/v1alpha2
kind: Cluster
metadata:
  name: <cluster-name>
spec:
  hosts:
  - {name: <node-name>, address: <external-ip>, internalAddress: <internal-ip>, user: <ssh-user>, password: "<password>"}
  # Or use privateKeyPath for SSH key authentication
  # - {name: <node-name>, address: <external-ip>, internalAddress: <internal-ip>, user: <ssh-user>, privateKeyPath: "<key-path>"}
  roleGroups:
    etcd:
    - <master-node-names>
    master:
    - <master-node-names>
    worker:
    - <worker-node-names>
  controlPlaneEndpoint:
    domain: <lb-domain-or-empty>
    address: ""
    port: 6443
  kubernetes:
    version: <k8s-version>  # e.g., v1.28.0
    imageRepo: kubesphere
    clusterName: cluster.local
    masqueradeAll: false
    maxPods: 110
    nodeCidrMaskSize: 24
    proxyMode: ipvs  # or iptables
  network:
    plugin: <cni-plugin>  # calico, flannel, cilium, etc.
    kubePodsCIDR: <pod-cidr>
    kubeServiceCIDR: <service-cidr>
    multusCNI:
      enabled: false
  registry:
    privateRegistry: "<registry-url>"
    namespaceOverride: ""
    registryMirrors: []
    insecureRegistries: []
  addons: []
```

#### Step 3: Validate Configuration

1. Check YAML syntax is valid
2. Verify IP addresses are reachable
3. Ensure CIDR ranges don't overlap
4. Confirm SSH credentials are correct
5. Validate node roles are assigned correctly

#### Step 4: Create the Cluster

1. Run: `kk create cluster -f <config-file>`
2. Monitor the installation process
3. Handle any errors that occur
4. Verify cluster is running: `kubectl get nodes`

#### Configuration Examples by Use Case

**Small Development Cluster (3 nodes, 1 master + 2 workers):**
- Version: v1.28.0
- CNI: flannel (simpler)
- CRI: containerd
- Pod CIDR: 10.233.64.0/18
- Service CIDR: 10.233.0.0/18

**Production Cluster (5+ nodes, HA):**
- Version: v1.28.0 (or latest stable)
- CNI: calico (network policies, production-ready)
- CRI: containerd
- Proxy Mode: ipvs
- Control Plane Endpoint: Load balancer required
- Pod CIDR: 10.233.64.0/18 or larger
- Service CIDR: 10.233.0.0/18

**High Performance Cluster:**
- CNI: cilium (eBPF-based)
- CRI: containerd
- Proxy Mode: ipvs
- Larger CIDR ranges if needed

### Scaling a Cluster

KubeKey uses separate commands for adding and deleting nodes:

#### Adding Nodes to a Cluster

1. **Get current cluster configuration**:
   ```bash
   kk create config --from-cluster -f current-cluster.yaml
   ```
   This generates a configuration file with all existing nodes from the current cluster.
   
   **Note**: The `--from-cluster` flag is used to generate a config file from an existing cluster. For new clusters, create the config file manually or use `scripts/generate_config.sh`.

2. **Edit the configuration file**:
   - Add new node information to `spec.hosts` section
   - Add new node names to appropriate `roleGroups` (worker, master, etcd)
   - Example:
     ```yaml
     spec:
       hosts:
       - {name: master1, address: 192.168.0.2, ...}  # existing
       - {name: worker1, address: 192.168.0.3, ...}  # existing
       - {name: worker2, address: 192.168.0.4, ...}  # existing
       - {name: worker3, address: 192.168.0.5, ...}  # NEW node
       roleGroups:
         worker:
         - worker1
         - worker2
         - worker3  # NEW node added
     ```

3. **Add nodes**:
   ```bash
   kk add nodes -f current-cluster.yaml
   ```
   Or use the script: `scripts/add_nodes.sh current-cluster.yaml`

4. **Verify**: `kubectl get nodes`

#### Deleting Nodes from a Cluster

1. **Drain the node** (recommended before deletion):
   ```bash
   kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data
   ```
   This safely evicts all pods from the node.

2. **Delete the node**:
   ```bash
   kk delete node <node-name>
   ```
   Or use the script: `scripts/delete_node.sh <node-name>`

3. **Verify**: `kubectl get nodes`

**Important Notes**:
- When adding nodes, the config file must include ALL existing nodes plus new ones
- Before deleting a node, ensure workloads are migrated or stopped
- Master nodes should not be deleted unless you have HA setup (3+ masters)

### Upgrading a Cluster

KubeKey supports upgrading Kubernetes clusters and optionally KubeSphere. Follow these steps:

#### Prerequisites for Upgrade

1. **Backup**: Ensure all important data is backed up
2. **Node Time Sync**: All nodes must have synchronized time (use NTP)
3. **Resource Check**: Verify nodes have sufficient resources
4. **Version Compatibility**: Check compatibility between current and target versions
5. **Low Traffic Period**: Perform upgrade during low-traffic periods if possible

#### Upgrade Process

1. **Check Current Versions**:
   ```bash
   kubectl version --short
   kk version
   ```

2. **Determine Target Version**:
   - Kubernetes: Typically upgrade one minor version at a time (e.g., v1.27.x → v1.28.x)
   - KubeSphere: Check compatibility with target Kubernetes version
   - Common upgrade paths:
     - v1.26.x → v1.27.x → v1.28.x
     - v1.27.x → v1.28.x

3. **Upgrade Options**:

   **Option A: Interactive Upgrade (Recommended)**
   ```bash
   ./scripts/upgrade_cluster.sh
   ```
   The script will prompt for:
   - Target Kubernetes version
   - Whether to upgrade KubeSphere
   - Target KubeSphere version (if applicable)

   **Option B: Command Line with Options**
   ```bash
   # Upgrade Kubernetes only
   ./scripts/upgrade_cluster.sh --k8s-version v1.28.0
   
   # Upgrade Kubernetes and KubeSphere
   ./scripts/upgrade_cluster.sh --k8s-version v1.28.0 --ks-version v3.4.1 --with-kubesphere
   
   # Using configuration file
   ./scripts/upgrade_cluster.sh --config cluster-config.yaml --k8s-version v1.28.0
   ```

   **Option C: Direct KubeKey Command**
   ```bash
   # Kubernetes only
   kk upgrade --with-kubernetes --kubernetes-version v1.28.0
   
   # Kubernetes + KubeSphere
   kk upgrade --with-kubernetes --with-kubesphere \
     --kubernetes-version v1.28.0 \
     --kubesphere-version v3.4.1
   ```

4. **Monitor Upgrade Progress**:
   - The upgrade process typically takes 30-60 minutes
   - Monitor node status: `kubectl get nodes -w`
   - Check pod status: `kubectl get pods -A`
   - Review KubeKey logs if issues occur

5. **Verify Upgrade**:
   ```bash
   kubectl version --short
   kubectl get nodes
   kubectl get pods -A
   ```

#### Upgrade Considerations

**Kubernetes Version Selection**:
- Upgrade one minor version at a time (e.g., 1.27 → 1.28, not 1.26 → 1.28)
- Check Kubernetes release notes for breaking changes
- Verify CNI plugin compatibility with new version
- Ensure CRI version is compatible

**KubeSphere Upgrade**:
- Only upgrade if KubeSphere is installed
- Check KubeSphere compatibility matrix with Kubernetes versions
- Review KubeSphere upgrade documentation for specific versions
- Some KubeSphere features may require specific Kubernetes versions

**Rollback**:
- KubeKey does not provide automatic rollback
- Manual rollback requires restoring from backups
- Always backup before upgrading

**Common Issues**:
- Node time synchronization errors → Ensure NTP is configured
- Insufficient resources → Check node CPU/memory/disk
- Network connectivity issues → Verify all nodes are reachable
- Pod eviction failures → Drain nodes manually if needed

### Viewing Cluster Configuration

1. If a configuration file exists, display its contents
2. Explain the key configuration parameters:
   - Kubernetes version
   - Node specifications (master/worker nodes)
   - Network plugins
   - Storage configurations
   - Authentication settings
3. Use `kk version` to check KubeKey version and cluster info

## Prerequisites

- Linux or macOS system
- SSH access to target nodes (for cluster deployment)
- Root or sudo privileges (for installation)
- Network connectivity to download KubeKey and container images

## Common Workflows

### Initial Setup
1. Check if KubeKey is installed
2. If not, install KubeKey
3. Verify installation with `kk version`

### Creating a New Cluster
1. Review example configuration
2. Create cluster configuration file
3. Validate configuration
4. Deploy cluster
5. Verify cluster status

### Adding Nodes to Existing Cluster
1. Get current cluster config: `kk create config --from-cluster -f config.yaml`
2. Edit config file to add new nodes to `spec.hosts` and `roleGroups`
3. Run: `kk add nodes -f config.yaml` (or use `scripts/add_nodes.sh`)
4. Verify new nodes joined: `kubectl get nodes`

### Removing Nodes from Cluster
1. Drain the node: `kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data`
2. Delete the node: `kk delete node <node-name>` (or use `scripts/delete_node.sh`)
3. Verify node removed: `kubectl get nodes`

### Upgrading Cluster
1. Check current versions: `kubectl version --short`
2. Determine target Kubernetes version (upgrade one minor version at a time)
3. Run upgrade: `./scripts/upgrade_cluster.sh` (interactive) or with options
4. Monitor progress and verify: `kubectl get nodes` and `kubectl version`

## Error Handling

- If KubeKey is not found, suggest installation
- If configuration file is invalid, help user fix YAML syntax
- If cluster creation fails, check:
  - Network connectivity
  - SSH access to nodes
  - Node prerequisites (Docker, etc.)
  - Disk space and resources
- If adding nodes fails, verify:
  - Config file includes ALL existing nodes plus new ones
  - New nodes meet requirements (CPU, memory, disk)
  - SSH access to new nodes
  - Network connectivity
  - New nodes are not already in the cluster
- If deleting nodes fails, verify:
  - Node name is correct
  - Node is not a critical master (unless HA setup)
  - Workloads have been drained/migrated
- If upgrade fails, check:
  - Node time synchronization (NTP)
  - Sufficient resources on all nodes
  - Version compatibility (upgrade one minor version at a time)
  - Network connectivity to all nodes
  - CNI/CRI compatibility with target Kubernetes version

## Configuration Reference

For detailed information about all configuration options, see:
- `references/config-options.md` - Complete reference of all configuration options
- `examples/cluster-config.yaml` - Example configuration file
- `scripts/generate_config.sh` - Interactive configuration generator

Key configuration decisions:
- **Kubernetes Version**: Latest stable (v1.28.x) unless compatibility required
- **CNI Plugin**: Calico for production, Flannel for simple deployments
- **CRI**: Containerd (recommended) or Docker
- **Proxy Mode**: iptables for small/medium, ipvs for large clusters
- **CIDR Ranges**: Ensure no overlaps, use /18 for pods and services typically

## References

For detailed technical references, see:
- [KubeKey Reference Guide](references/reference.md) - Comprehensive links to KubeKey, Kubernetes, CNI plugins, and related documentation
- [KubeKey Commands Reference](references/commands.md) - Quick reference for all kk commands
- [Configuration Options](references/config-options.md) - Detailed configuration options reference
- [Example Configuration](examples/cluster-config.yaml) - Sample cluster configuration file

Key resources:
- KubeKey GitHub: https://github.com/kubesphere/kubekey
- KubeKey Documentation: https://kubesphere.io/docs/installing-on-linux/introduction/kubekey/
- Kubernetes Documentation: https://kubernetes.io/docs/

