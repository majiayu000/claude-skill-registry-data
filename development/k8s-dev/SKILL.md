---
name: k8s-dev
description: "Assistance with Remote Kubernetes Development (Telepresence, Okteto, DevSpace). Use when: k8s dev, remote dev, telepresence, okteto, devspace, tilt, scaffold, remote cluster."
license: CC-BY-SA-4.0
metadata:
  source: "agents/skills/ops/k8s-dev.skill.md"
  tags: "ops"
  core: "false"
  context_cost: "medium"
---
# Kubernetes Dev Skill

## Goal
To develop directly against a remote Kubernetes cluster, enabling access to cloud dependencies and effectively "infinite" resources.

## Capabilities

### 1. Remote Interception (Telepresence)
-   **Intercept**: Route traffic from a remote service to your laptop.
-   **Debug**: Step through code locally while handling live remote requests.
-   **Preview URLs**: Share a specific intercept version with teammates.

### 2. Sync & Hot Reload (Okteto / DevSpace)
-   **File Sync**: Bi-directional sync between local folder and remote pod.
-   **Terminal**: Get a shell inside the remote pod.
-   **Environment**: Spin up ephemeral namespaces for each developer.

### 3. Configuration
-   **DevSpace**: Generate `devspace.yaml` for pipeline + sync.
-   **Okteto**: Generate `okteto.yaml` for hybrid dev.

## Steps
1.  **When to use**: Recommend Remote Dev when the app is too large for Docker Desktop (RAM/CPU limits) or depends on cloud-only resources (RDS, SQS).
2.  **Isolation**: Ensure developers work in their own Namespaces to avoid stepping on toes.
3.  **Security**: Use RBAC to limit developer permissions in the cluster.

## Deliverables
-   `devspace.yaml` configuration.
-   `telepresence` intercept commands.
-   `okteto.yaml` manifest.

## Security & Guardrails

### 1. Skill Security (Kubernetes Dev)
- **Local Intercept Isolation**: When using tools like Telepresence to route cluster traffic to a local machine, the connection must be strictly tunneled over mTLS. The local agent process must drop privileges to a non-root user to mitigate risks if the intercepted traffic is malicious.
- **Ephemeral Namespace Cleanup**: DevSpace or Okteto configurations must include hard TTLs (Time-To-Live) for developer namespaces. Stale namespaces abandoned by agents/developers must be automatically purged to reduce the cluster's attack surface.

### 2. System Integration Security
- **RBAC Developer Constraints**: The generated Kubernetes configurations must enforce strict Role-Based Access Control (RBAC). A remote developer shell must NEVER have `cluster-admin` privileges; it should only have edit/exec capabilities within its targeted, isolated namespace.
- **Network Policy Egress**: Developer pods must be constrained by NetworkPolicies that block arbitrary egress to the public internet or production namespaces, preventing a compromised dev pod from being used as a staging ground for lateral movement.

### 3. LLM & Agent Guardrails
- **Production Intercept Block**: The agent must violently reject any user prompt attempting to use Telepresence or DevSpace to intercept traffic directly from the `production` namespace. It must enforce that remote dev only occurs in `dev` or `staging` clusters.
- **Secret Syncing Prohibition**: DevSpace/Okteto file sync mechanisms must explicitly exclude `.env` files or folders containing local secrets from being synced *up* to the cluster, preventing accidental exposure of local credentials to the remote pod environment.
