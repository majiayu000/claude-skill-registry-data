---
name: aks
description: "Expert coverage of Azure Kubernetes Service (AKS): node pools, workload identity, Azure CNI options, AKS Automatic, NAP (Karpenter), add-ons, and hybrid scenarios. Use for \"AKS\", \"Azure Kubernetes\", \"Azure CNI\", \"AKS Automatic\", \"workload identity Azure\", \"az aks\", \"Node Auto Provisioning AKS\"."
license: MIT
---

# Azure AKS

This skill covers Azure Kubernetes Service (AKS), including:

- AKS managed control plane (free and paid tiers, SLA)
- Node pools (system vs user, VM sizes, autoscaling, taints)
- AKS Automatic (fully managed, GA since 2026)
- Node Auto Provisioning (Karpenter on AKS, GA 2026)
- Networking (Azure CNI, kubenet, Azure CNI Overlay, Cilium-powered CNI)
- Workload Identity (replacing AAD Pod Identity)
- AKS add-ons (monitoring, policy, Istio, secrets CSI, Defender)
- Storage (Azure Disk CSI, Azure Files CSI, Blob CSI)
- Security (Defender for Containers, Azure Policy, managed identity)
- Hybrid and multi-cloud (Azure Arc-enabled Kubernetes)

## How to Approach Tasks

1. **Classify** the request:
   - **Architecture** -- Load `references/architecture.md` for control plane, networking, compute, identity
   - **Node management** -- Node pool design, autoscaling, AKS Automatic, NAP
   - **Networking** -- CNI selection, ingress, load balancing, DNS
   - **Security** -- Workload identity, Defender, Azure Policy, managed identity
   - **Troubleshooting** -- Node issues, networking, identity errors, upgrade failures

2. **Identify context** -- Which tier (free/standard/premium)? Which CNI? AKS Automatic or standard? Ask if unclear.

3. **Load context** -- Read the reference file for deep technical detail.

4. **Apply** -- Provide Azure CLI (`az aks`), Bicep, Terraform, or kubectl examples as appropriate.

5. **Validate** -- Suggest `az aks show`, `kubectl get nodes`, Azure Monitor queries.

## AKS Control Plane

- Managed by Azure: API server and etcd run in Azure-managed infrastructure
- **Free tier**: no SLA, no uptime guarantee (dev/test only)
- **Standard tier**: 99.95% SLA (or 99.99% with Availability Zones), Cluster Autoscaler, multiple node pools
- **Premium tier**: Standard + long-term support (LTS), Microsoft-backed patch SLA
- Upgrade: one minor version at a time; automatic upgrades available (patch, stable, rapid, node image channels)

```bash
# Create AKS cluster
az aks create \
  --resource-group myRG \
  --name myAKS \
  --node-count 3 \
  --node-vm-size Standard_D4s_v5 \
  --network-plugin azure \
  --network-plugin-mode overlay \
  --tier standard \
  --enable-managed-identity \
  --enable-oidc-issuer \
  --enable-workload-identity \
  --zones 1 2 3
```

## Node Pools

### System vs User Node Pools

```bash
# System pool (runs kube-system, CoreDNS, metrics-server)
az aks nodepool add \
  --resource-group myRG \
  --cluster-name myAKS \
  --name system \
  --node-count 3 \
  --node-vm-size Standard_D4s_v5 \
  --mode System \
  --node-taints CriticalAddonsOnly=true:NoSchedule

# User pool (application workloads)
az aks nodepool add \
  --resource-group myRG \
  --cluster-name myAKS \
  --name workers \
  --node-count 3 \
  --node-vm-size Standard_D8s_v5 \
  --mode User \
  --enable-cluster-autoscaler \
  --min-count 2 \
  --max-count 20 \
  --zones 1 2 3
```

**Best practice**: separate system and user node pools. Taint system pool with `CriticalAddonsOnly=true:NoSchedule` to prevent application pods from landing on system nodes.

### Specialized Node Pools

```bash
# GPU node pool
az aks nodepool add \
  --resource-group myRG \
  --cluster-name myAKS \
  --name gpu \
  --node-vm-size Standard_NC6s_v3 \
  --node-count 1 \
  --node-taints sku=gpu:NoSchedule \
  --labels workload=gpu

# Spot VM pool (cost optimization)
az aks nodepool add \
  --resource-group myRG \
  --cluster-name myAKS \
  --name spot \
  --priority Spot \
  --spot-max-price -1 \
  --eviction-policy Delete \
  --node-vm-size Standard_D4s_v5 \
  --enable-cluster-autoscaler \
  --min-count 0 \
  --max-count 10
```

## AKS Automatic

GA since 2026. Removes infrastructure decisions -- Azure manages node pools, autoscaling, OS patching, and security hardening automatically. Comparable to GKE Autopilot.

```bash
az aks create \
  --resource-group myRG \
  --name myAKS-auto \
  --sku automatic
```

**What AKS Automatic manages**:
- Node pool creation and sizing based on workload requirements
- OS patching and security updates
- Default security hardening (Pod Security Standards enforced)
- Network policy enforcement
- Built-in monitoring and logging

**When NOT to use AKS Automatic**:
- Custom node configurations needed (kernel tuning, custom kubelet settings)
- Specific VM SKUs required (GPU, high-memory, confidential computing)
- Windows containers
- Need for SSH access to nodes

## Node Auto Provisioning (NAP)

Karpenter-based node provisioning for AKS (GA early 2026):

```bash
az aks update --resource-group myRG --name myAKS --enable-node-auto-provisioning
```

NAP dynamically creates nodes matching pending pod requirements, similar to Karpenter on EKS. Selects optimal VM sizes and consolidates underutilized nodes.

## Networking

### CNI Options

| CNI | Pod IP Source | Performance | Use Case |
|-----|-------------|-------------|----------|
| kubenet | Non-VNet IPs (NAT) | Lower (NAT overhead) | Simple, IP conservation |
| Azure CNI | VNet IPs per pod | High (direct routing) | VNet integration needed |
| Azure CNI Overlay | Overlay IPs, node VNet IPs | High | Scale + VNet integration |
| Azure CNI + Cilium | eBPF dataplane | Highest | Best performance + observability |

**Azure CNI Overlay** (recommended for most new clusters): pods get IPs from a private overlay CIDR (e.g., 10.244.0.0/16), nodes get VNet IPs. Eliminates IP exhaustion issues while maintaining VNet integration for node-level communication.

**Azure CNI powered by Cilium**: eBPF-based dataplane for service load balancing, NetworkPolicy enforcement, and observability (Hubble). Replaces kube-proxy.

```bash
az aks create \
  --resource-group myRG \
  --name myAKS \
  --network-plugin azure \
  --network-plugin-mode overlay \
  --network-dataplane cilium
```

### Ingress Options

| Option | Type | Managed By |
|--------|------|-----------|
| Application Gateway Ingress Controller (AGIC) | L7 | Azure (add-on) |
| NGINX Ingress | L7 | Self-managed |
| Azure Service Mesh (Istio) | L7 + mTLS | Azure (add-on) |
| Internal Load Balancer | L4 | Azure (annotation) |

```yaml
# Internal load balancer annotation
apiVersion: v1
kind: Service
metadata:
  annotations:
    service.beta.kubernetes.io/azure-load-balancer-internal: "true"
spec:
  type: LoadBalancer
```

## Workload Identity

Replaces the deprecated AAD Pod Identity. Federated credentials between Azure AD and Kubernetes ServiceAccounts:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: storage-reader
  namespace: production
  annotations:
    azure.workload.identity/client-id: "CLIENT_ID_GUID"
  labels:
    azure.workload.identity/use: "true"
```

```bash
# Enable on cluster
az aks update --resource-group myRG --name myAKS \
  --enable-oidc-issuer --enable-workload-identity

# Create federated credential
az identity federated-credential create \
  --name aks-fed-cred \
  --identity-name myManagedIdentity \
  --resource-group myRG \
  --issuer "$(az aks show -g myRG -n myAKS --query oidcIssuerProfile.issuerUrl -o tsv)" \
  --subject "system:serviceaccount:production:storage-reader"
```

**Pod must have the label**: `azure.workload.identity/use: "true"` on the pod (not just the ServiceAccount) for the webhook to inject the AZURE_CLIENT_ID, AZURE_TENANT_ID, and AZURE_FEDERATED_TOKEN_FILE environment variables.

## AKS Add-ons

| Add-on | Purpose |
|--------|---------|
| Azure Monitor (Container Insights) | Metrics, logs, Live View |
| Azure Policy | OPA/Gatekeeper-based policy enforcement |
| Istio Service Mesh | mTLS, traffic management |
| Secrets Store CSI (Key Vault) | Mount Key Vault secrets as volumes |
| Defender for Containers | Runtime threat detection |
| Blob CSI Driver | Azure Blob storage volumes |
| Web App Routing | Managed NGINX ingress + cert management |

## Common Patterns

### Multi-Region HA

```bash
# Cluster per region
az aks create -g myRG-eastus -n aks-eastus --location eastus ...
az aks create -g myRG-westus -n aks-westus --location westus ...

# Azure Front Door for global load balancing
# Azure Traffic Manager for DNS-based failover
```

### Hybrid with Azure Arc

```bash
# Connect non-AKS cluster to Azure
az connectedk8s connect --name on-prem-cluster --resource-group myRG

# Deploy configurations via GitOps (Flux)
az k8s-configuration flux create \
  --name app-config \
  --cluster-name on-prem-cluster \
  --resource-group myRG \
  --cluster-type connectedClusters \
  --url https://github.com/myorg/k8s-config \
  --branch main
```

## Reference Files

- `references/architecture.md` -- Node pool internals, CNI deep dive, workload identity mechanics, AKS Automatic architecture, storage options, security model. Read for architecture and design questions.
