---
name: kubernetes-ontology-access
description: Use this skill whenever a user wants to onboard, deploy, install, or operate kubernetes-ontology; set up its Helm chart, release CLI, daemon, or topology viewer; run Kubernetes topology queries; diagnose Pod or Workload failures with AI-agent workflows; or connect human visual troubleshooting to the CLI and HTTP API. This skill should trigger for requests about Kubernetes ontology onboarding, Helm deployment, topology query, diagnostic subgraph, ImagePullBackOff or storage/RBAC/Event graph troubleshooting, viewer usage, and agent integration.
metadata:
  author: Colvin-Y
  version: "0.1.8"
  license: Apache-2.0
  category: devops
  tags:
    - kubernetes
    - troubleshooting
    - topology
    - ontology
    - ai-agent
    - devops
---

# Kubernetes Ontology Access

Guide users from zero to useful diagnosis with `kubernetes-ontology`.

This skill is the repository's onboarding playbook for three connected modes:

1. AI-agent automatic troubleshooting through stable daemon-backed queries.
2. CLI-driven topology and diagnostic inspection.
3. Human visual intervention through the topology viewer.

Prefer read-only, daemon-backed workflows. The project observes Kubernetes
objects and builds an in-memory graph; it must not mutate observed workloads.

## Operating Posture

Do not merely summarize the docs. Drive the user toward the next useful action:

- Identify the user's current state: no setup, existing daemon, CLI-only query,
  diagnostic request, viewer handoff, or source development.
- Choose the shortest path that satisfies the request.
- Give concrete commands the user or agent can run next, with safe defaults
  named inline.
- When command output is needed, ask for or run that command before moving to
  later steps.
- Keep cluster-changing actions explicit: ask for confirmation before running
  `helm upgrade --install` or any command that changes cluster resources.
- Do not require a repository checkout for CLI-only diagnostics against an
  already running daemon.

## First Response Checklist

When this skill triggers, quickly establish:

- Whether the user is inside a local checkout of this repository.
- Target cluster context and logical cluster name.
- Desired namespaces for collection (`contextNamespaces`).
- Deployment path: release binary server + client for private clusters or
  short-lived local diagnosis, Helm + release CLI when cluster nodes can pull
  the image, source build for development.
- Whether the environment can reach GitHub Releases and whether cluster nodes
  can pull `ghcr.io` or an internal mirror.
- Diagnostic entry, if known: `Pod` or `Workload`, namespace, and name.
- Whether they want the viewer opened for human inspection.

If values are missing and a safe default exists, proceed with the default and
name it. Ask only for values that are required and cannot be inferred, such as
the target namespace/name for a diagnostic query.

## Safety Model

Explain this once when onboarding a new user:

- Runtime collection is read-only against observed Kubernetes resources.
- Helm installs this project's own Deployment, Service, ServiceAccount,
  ConfigMap, viewer, and read-only RBAC.
- Release binary mode installs nothing in the cluster. It starts
  `kubernetes-ontologyd` on the host that has kubeconfig access, and optionally
  starts `kubernetes-ontology-viewer` on that host.
- The default RBAC includes `get`, `list`, and `watch`; Secret reads are disabled
  by default. Use `--set rbac.readSecrets=true` only when Secret nodes and
  `uses_secret` edges are needed.
- Keep the HTTP API and viewer behind `kubectl port-forward` or a controlled
  private network. Do not expose them directly to the public internet.
- For short-lived diagnosis, tell the user exactly how to stop port-forwards,
  host-local binaries, and Helm resources after use.

## Repository Pointers

When working from a checkout, read only the files needed for the current task:

- `README.md` or `README.zh-CN.md` for project overview.
- `QUICKSTART.md` for end-to-end setup and commands.
- `AI_CONTRACT.md` for downstream agent consumption rules.
- `charts/kubernetes-ontology/values.yaml` for Helm values.
- `Makefile` for local build, server, CLI, and viewer targets.

## Recommended Onboarding Flow

Choose the deployment path from network constraints first:

- Use release binary server + client when the cluster is private, air-gapped,
  cannot pull public images, or the user wants no in-cluster footprint.
- Use Helm + release CLI when the cluster can pull the configured image, or the
  image has been mirrored to an internal registry.
- Use source build only for contributors or local code changes.

Only guide the user to clone the repository when the current path needs files
from the checkout, such as the local Helm chart under
`charts/kubernetes-ontology`, source development, or local viewer development.
If the user only needs CLI queries against an existing daemon, skip the clone.

When a checkout is needed and the user does not already have one, use:

```bash
git clone https://github.com/Colvin-Y/kubernetes-ontology.git
cd kubernetes-ontology
```

If the user is not ready to deploy yet, first verify prerequisites and collect
the target cluster, logical cluster name, and namespaces. Then return to the
checkout step only when deploying the chart or using source-local commands.

### 1. Verify Prerequisites

Check or ask the user to check:

```bash
kubectl config current-context
kubectl get namespace
```

Check `helm version` only for the Helm path. For private environments, explicitly
ask whether cluster nodes can pull `ghcr.io/colvin-y/kubernetes-ontology` or an
internal mirror. If they cannot, prefer the release binary path.

If the user expects the agent to run commands, confirm before using any command
that changes cluster resources, including `helm upgrade --install`.

### 2. Release Binary Server + Client

Use this path when the user wants a simple binary workflow or the cluster cannot
pull the published image. A GitHub Release archive contains:

- `kubernetes-ontologyd`: the read-only server that talks to the Kubernetes API.
- `kubernetes-ontology`: the CLI client that talks to the server.
- `kubernetes-ontology-viewer`: optional local viewer.
- `local/kubernetes-ontology.yaml.example`: a config template.

Download or transfer the archive for the selected version and platform:

```bash
export KO_VERSION=v0.1.8
curl -LO "https://github.com/Colvin-Y/kubernetes-ontology/releases/download/${KO_VERSION}/kubernetes-ontology_${KO_VERSION}_linux_amd64.tar.gz"
tar -xzf "kubernetes-ontology_${KO_VERSION}_linux_amd64.tar.gz"
cd "kubernetes-ontology_${KO_VERSION}_linux_amd64"
```

Use `linux_amd64`, `linux_arm64`, `darwin_amd64`, `darwin_arm64`, or
`windows_amd64.zip` for other hosts. If the private environment cannot access
GitHub, tell the user to download the archive elsewhere and transfer it through
their approved internal channel.

Release CLI binaries check GitHub Releases with a short best-effort timeout
during normal use when version metadata is present. When a release CLI is
already installed, prefer checking before longer troubleshooting sessions:

```bash
./kubernetes-ontology --version
./kubernetes-ontology --check-update
```

If a newer release is available and the environment permits downloading from
GitHub, the user can update the CLI in place:

```bash
./kubernetes-ontology --update
```

Use `--no-update-check` or `KUBERNETES_ONTOLOGY_SKIP_UPDATE_CHECK=1` for
offline or tightly controlled scripts.

Create or adapt `kubernetes-ontology.yaml`:

```bash
cp local/kubernetes-ontology.yaml.example kubernetes-ontology.yaml
```

Then edit the kubeconfig path, logical cluster name, namespace scope, and any
cluster-specific workload, controller, or CSI rules:

```yaml
kubeconfig: /absolute/path/to/kubeconfig.yaml
cluster: your-logical-cluster
contextNamespaces:
  - default
  - kube-system
server:
  addr: 127.0.0.1:18080
bootstrapTimeout: 2m
streamMode: informer
```

Run the server in the foreground unless the user explicitly wants a background
process:

```bash
./kubernetes-ontologyd --config ./kubernetes-ontology.yaml
```

If a background process is useful for a short session:

```bash
nohup ./kubernetes-ontologyd --config ./kubernetes-ontology.yaml > kubernetes-ontologyd.log 2>&1 &
echo $! > kubernetes-ontologyd.pid
```

Confirm readiness from another terminal:

```bash
./kubernetes-ontology --server "http://127.0.0.1:18080" --status
```

Optional local viewer:

```bash
./kubernetes-ontology-viewer --server "http://127.0.0.1:18080"
```

When done, stop foreground processes with `Ctrl-C`. For background processes:

```bash
kill "$(cat kubernetes-ontologyd.pid)"
```

If the viewer was backgrounded, kill that PID too. Remind the user to remove
temporary logs, pid files, and copied kubeconfigs according to their local
security policy.

### 3. Deploy The Helm Chart

Use a release version and image. If the user did not specify one, use the latest
project release they selected or the version already present in the repository
docs. Do not invent a future version.

```bash
export KO_VERSION=v0.1.8
export KO_IMAGE=ghcr.io/colvin-y/kubernetes-ontology
curl -LO "https://github.com/Colvin-Y/kubernetes-ontology/releases/download/${KO_VERSION}/kubernetes-ontology-0.1.8.tgz"

helm upgrade --install kubernetes-ontology kubernetes-ontology-0.1.8.tgz \
  --namespace kubernetes-ontology \
  --create-namespace \
  --set image.repository="${KO_IMAGE}" \
  --set image.tag="${KO_VERSION}" \
  --set cluster="your-logical-cluster" \
  --set contextNamespaces='{default,kube-system}'
```

For private clusters, mirror the image to an internal registry and set
`KO_IMAGE` to that mirror. If image mirroring is not available, use the release
binary path instead.

For all namespaces, remove the `--set contextNamespaces=...` line and use the
chart default empty list. To opt into Secret collection:

```bash
helm upgrade --install kubernetes-ontology kubernetes-ontology-0.1.8.tgz \
  --namespace kubernetes-ontology \
  --reuse-values \
  --set rbac.readSecrets=true
```

Wait for rollout:

```bash
kubectl -n kubernetes-ontology rollout status deploy/kubernetes-ontology
```

The viewer rollout exists when `viewer.enabled=true`, which is the chart
default:

```bash
kubectl -n kubernetes-ontology rollout status deploy/kubernetes-ontology-viewer
```

### 3. Port-Forward Server And Viewer

Use separate terminals or background sessions:

```bash
kubectl -n kubernetes-ontology port-forward svc/kubernetes-ontology 18080:18080
```

The viewer service exists when `viewer.enabled=true`, which is the chart
default:

```bash
kubectl -n kubernetes-ontology port-forward svc/kubernetes-ontology-viewer 8765:8765
```

If the user disabled the viewer, expose only the server or re-enable the viewer
later.

Default endpoints:

- Server: `http://127.0.0.1:18080`
- Viewer: `http://127.0.0.1:8765`

### 4. Download The CLI

Download `kubernetes-ontology` from GitHub Releases for the selected
`KO_VERSION`. The repository release workflow packages `kubernetes-ontology`,
`kubernetes-ontologyd`, and `kubernetes-ontology-viewer` under an archive root
named `kubernetes-ontology_${KO_VERSION}_${GOOS}_${GOARCH}`. Choose the archive
suffix by platform:

- macOS Apple Silicon: `darwin_arm64.tar.gz`
- macOS Intel: `darwin_amd64.tar.gz`
- Linux x86_64: `linux_amd64.tar.gz`
- Linux ARM64: `linux_arm64.tar.gz`
- Windows x86_64: `windows_amd64.zip`

Example for macOS Apple Silicon:

```bash
curl -LO "https://github.com/Colvin-Y/kubernetes-ontology/releases/download/${KO_VERSION}/kubernetes-ontology_${KO_VERSION}_darwin_arm64.tar.gz"
tar -tzf "kubernetes-ontology_${KO_VERSION}_darwin_arm64.tar.gz" | head
tar -xzf "kubernetes-ontology_${KO_VERSION}_darwin_arm64.tar.gz"
sudo install "kubernetes-ontology_${KO_VERSION}_darwin_arm64/kubernetes-ontology" /usr/local/bin/kubernetes-ontology
```

If the user is installing from a fork or custom release, inspect the archive
contents first and adjust the install path to the actual extracted directory.
If the user cannot use `sudo`, keep the binary in a local directory and invoke
it by path.

After installation, run `kubernetes-ontology --check-update` when network
access to GitHub Releases is allowed. Normal CLI calls also do this with a
short best-effort timeout and print a stderr notice when a newer release exists.

### 5. Confirm The Daemon Is Ready

```bash
kubernetes-ontology --server "http://127.0.0.1:18080" --status
```

Continue only when status shows `Ready: true` or `Phase: ready`. List,
entity, relation, expand, and diagnostic responses include lowercase
`freshness.ready` metadata that agents can use after the daemon is serving
queries. If the daemon is not ready, inspect rollout logs and retry status.

### 6. Cleanup For Short-Lived Use

For Helm path:

```bash
# Stop any foreground port-forward terminals with Ctrl-C first.
helm uninstall kubernetes-ontology --namespace kubernetes-ontology
```

Only delete the namespace if it was created exclusively for this install:

```bash
kubectl delete namespace kubernetes-ontology
```

For release binary path, stop `kubernetes-ontologyd` and any viewer process on
the host. The binary path leaves no cluster-side resources to uninstall.

## AI-Agent Automatic Troubleshooting

Use this flow when the user asks the agent to diagnose a workload or pod.

### Pod Entry

```bash
kubernetes-ontology \
  --server "http://127.0.0.1:18080" \
  --machine-errors \
  --diagnose-pod \
  --namespace default \
  --name my-pod
```

### Workload Entry

```bash
kubernetes-ontology \
  --server "http://127.0.0.1:18080" \
  --machine-errors \
  --diagnose-workload \
  --namespace default \
  --name my-deployment
```

### Recipe Hints

Use `--recipe` when the user question is more specific than the entry kind:

- `pod-incident` for bad Pods and runtime symptoms.
- `workload-incident` for rollout or controller failures.
- `storage-csi` for PVC/PV/StorageClass/CSI and VolumeAttachment questions.
- `service-routing` for Ingress, Service selector, EndpointSlice, and
  NetworkPolicy questions.
- `identity` for ServiceAccount, RoleBinding, and ClusterRoleBinding evidence.
- `node-context` for node placement and node condition context.
- `helm-ownership` for release/chart provenance.
- `helm-upgrade-runtime-failure` when Helm failed and only current Kubernetes
  state is available.

Example:

```bash
kubernetes-ontology \
  --server "http://127.0.0.1:18080" \
  --entry-kind Service \
  --namespace default \
  --name my-service \
  --recipe service-routing
```

### Agent Reasoning Rules

- Treat the response as a bounded evidence graph, not complete cluster truth.
- Check `schemaVersion`, `recipe`, `lanes`, `partial`, `warnings`,
  `degradedSources`, `budgets`, `rankedEvidence`, and `conflicts` before
  forming a conclusion.
- Use `managed_by_helm_release` and `installs_chart` edges as Helm/package
  provenance when present, but describe them as label-derived evidence unless
  future exact manifest evidence is explicitly available.
- For "helm upgrade failed" requests, diagnose current cluster state even if
  the user lacks Helm CLI output. Say clearly that template, values,
  repository, client, hook, and `--atomic` rollback causes need user-provided
  Helm stderr/status/history.
- When `helm_cli_output_not_observed` or `helm_manifest_evidence_not_collected`
  appears, include it in the answer before naming a root cause.
- Index nodes by `canonicalId`; join edges by `from` and `to`.
- Prefer edge/node attributes and provenance over explanation text for hard
  conclusions.
- Use `rankedEvidence` first for suspicion ranking, then explanation text for
  narrative.
- If `budgets.truncated=true`, say which budget was hit and suggest narrowing
  namespace/depth before raising graph caps.
- If evidence is missing, report that it is missing from the current graph
  slice rather than claiming the object does not exist anywhere.
- Prefer asserted and observed facts before inferred shortcuts.
- Preserve conflicts in the user-facing answer instead of choosing one owner or
  cause silently.
- For contract details, consult `AI_CONTRACT.md`.

Current limits to keep visible in agent reasoning:

- `rankedEvidence` currently starts with Event evidence; not every signal type
  is ranked yet.
- `explanation` content is useful but best-effort narrative.
- Traversal policy can hide valid facts outside the selected graph slice.
- Diagnostic budgets can intentionally truncate the graph. Treat
  `partial=true` as a correctness constraint, not a cosmetic warning.
- CSI component correlation is configurable with `csiComponentRules`; no
  driver-specific component inference runs unless a matching rule is configured.
- A missing edge in one diagnostic response should be treated as missing
  evidence in that slice, not global absence.

### Agent Output Template

For diagnostic answers, respond with:

````markdown
## Summary
[1-3 sentence diagnosis]

## Evidence
- [partial/warning/budget/conflict status, if present]
- [rankedEvidence item, if present]
- [node/edge/provenance fact]
- [node/edge/provenance fact]

## Next Queries
```bash
[one or two targeted CLI commands]
```

## Human Viewer
Open http://127.0.0.1:8765 and load the same Pod or Workload diagnostic graph.
````

Avoid recommending cluster mutations unless the user explicitly asks for
remediation and the evidence supports it.

## CLI Query Playbook

Status:

```bash
kubernetes-ontology --server "http://127.0.0.1:18080" --status
```

List entities:

```bash
kubernetes-ontology \
  --server "http://127.0.0.1:18080" \
  --list-entities \
  --entity-kind Pod \
  --namespace default \
  --limit 20
```

Resolve an entity and capture `entity.entityGlobalId`:

```bash
kubernetes-ontology \
  --server "http://127.0.0.1:18080" \
  --resolve-entity \
  --entity-kind Pod \
  --namespace default \
  --name my-pod
```

Diagnose a Helm release after a failed upgrade:

Use this Incident Context Pack flow only with `v0.1.6` or newer.

```bash
kubernetes-ontology \
  --server "http://127.0.0.1:18080" \
  --diagnose-helm-release \
  --namespace default \
  --name my-release \
  --recipe helm-upgrade-runtime-failure
```

Use this when the user knows the release name but does not have the original
Helm CLI output. Follow the returned `rankedEvidence`, `warnings`,
`degradedSources`, and release-owned Workload/Pod nodes. If the response only
shows Helm metadata and no rollout blocker, ask for `helm upgrade` stderr,
`helm status`, or `helm history`.

Expand one entity:

```bash
kubernetes-ontology \
  --server "http://127.0.0.1:18080" \
  --expand-entity \
  --entity-id 'your/entityGlobalId' \
  --expand-depth 1 \
  --limit 100
```

List filtered relations:

```bash
kubernetes-ontology \
  --server "http://127.0.0.1:18080" \
  --list-filtered-relations \
  --from 'your/entityGlobalId' \
  --relation-kind scheduled_on \
  --limit 50
```

Common stable relation kinds include:

- `controlled_by`
- `owns_pod`
- `scheduled_on`
- `selects_pod`
- `uses_config_map`
- `uses_secret`
- `uses_service_account`
- `bound_by_role_binding`
- `mounts_pvc`
- `bound_to_pv`
- `managed_by_helm_release`
- `installs_chart`
- `reported_by_event`
- `affected_by_webhook`
- `managed_by_csi_controller`
- `served_by_csi_node_agent`

## Human Visual Troubleshooting

Use the viewer when the user wants to inspect topology manually, validate an
agent conclusion, compare graph branches, or export a visible subgraph.

Steps:

1. Port-forward the viewer service.
2. Open `http://127.0.0.1:8765`.
3. Load live topology or a focused Pod/Workload diagnostic graph.
4. Select nodes to inspect attributes, provenance, and edge kinds.
5. Expand one hop when a relation needs more context.
6. Export the visible graph as JSON when the agent needs to continue from the
   exact human-inspected state.

The Helm chart enables the viewer by default. If the user installed with
`viewer.enabled=false`, skip the viewer rollout and port-forward commands, or
enable it with:

```bash
export KO_VERSION=v0.1.8
curl -LO "https://github.com/Colvin-Y/kubernetes-ontology/releases/download/${KO_VERSION}/kubernetes-ontology-0.1.8.tgz"
helm upgrade --install kubernetes-ontology kubernetes-ontology-0.1.8.tgz \
  --namespace kubernetes-ontology \
  --reuse-values \
  --set viewer.enabled=true
```

If using the local development viewer instead of Helm:

```bash
make visualize
```

Or use the dependency-free release viewer:

```bash
kubernetes-ontology-viewer --server "http://127.0.0.1:18080"
```

## Runtime Footprint And Cleanup

Always make the runtime footprint explicit during onboarding:

- Release binary path starts `kubernetes-ontologyd` on the host, and optionally
  `kubernetes-ontology-viewer`. It creates no Kubernetes resources.
- Helm path creates Kubernetes Deployments for the server and viewer, Services,
  a ServiceAccount, a ConfigMap, and read-only ClusterRole/ClusterRoleBinding
  resources. It may also require `kubectl port-forward` processes on the user's
  workstation.
- Source path starts local `make serve` and optional `make visualize`
  processes from the checkout.

For short-lived use, tell the user how to clean up before ending the session:

```bash
# Binary path, when backgrounded:
kill "$(cat kubernetes-ontologyd.pid)"

# Helm path:
helm uninstall kubernetes-ontology --namespace kubernetes-ontology

# Source path:
# stop the foreground make serve / make visualize terminals with Ctrl-C
```

Only suggest deleting the `kubernetes-ontology` namespace when it was created
solely for this install and the user confirms no other resources should remain.

## Source Development Path

Use this path for contributors or local code changes:

```bash
make build build-daemon build-viewer
cp local/kubernetes-ontology.yaml.example local/kubernetes-ontology.yaml
```

Edit `local/kubernetes-ontology.yaml`, then run in separate terminals:

```bash
make serve
make visualize
```

CLI checks:

```bash
make status-server
make list-entities-server ENTITY_KIND=Pod NAMESPACE=default LIMIT=20
make diagnose-pod-server NAMESPACE=default NAME=my-pod
```

For code changes, verify:

```bash
make verify
make live-check NAMESPACE=default NAME=my-pod
```

## Troubleshooting The Onboarding

If `entry not found`:

- Check exact namespace/name.
- List available entities in the namespace.
- Confirm `contextNamespaces` includes the target namespace, or is empty for
  all namespaces.

If status is not ready:

- Check the server rollout and pod logs.
- Confirm the ServiceAccount has read access to the needed resources.
- Increase `bootstrapTimeout` for large or slow clusters.

If graph evidence seems too small:

- Increase diagnostic depth with `--max-depth` or `--storage-max-depth`.
- Use `--expand-terminal-nodes` for deliberate fan-out.
- Expand selected viewer nodes one hop instead of loading the whole cluster.

If the viewer cannot load data:

- Confirm both port-forwards are running.
- Check `http://127.0.0.1:18080/status`.
- Restart the viewer port-forward and reload the page.
