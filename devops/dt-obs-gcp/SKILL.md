---
name: dt-obs-gcp
description: GCP cloud resources including Compute Engine, GKE, Cloud Run, Pub/Sub, VPC networking, DNS, IAM, Secret Manager, and monitoring. Monitor GCP infrastructure, analyze resource usage, audit security posture, and manage organizational hierarchy across projects and folders.
license: Apache-2.0
---

# GCP Cloud Infrastructure

Monitor and analyze GCP resources using Dynatrace Smartscape and DQL. Query GCP services, manage organizational hierarchy, audit security posture, and track resource ownership across your GCP infrastructure.

## When to Use This Skill

Use this skill when the user needs to work with GCP resources in Dynatrace. Load the reference file for the task type:

| Task | File to load |
|---|---|
| Inventory and topology queries | (no additional file — use core patterns above) |
| Compute Engine instances, machine types, IP addresses | Load `references/compute-instances.md` |
| GKE clusters, node pools, pods, deployments, services, RBAC | Load `references/kubernetes-gke.md` |
| Cloud Run services, revisions, executions | Load `references/serverless-containers.md` |
| VPC networks, subnets, routes, DNS records | Load `references/networking-dns.md` |
| Pub/Sub topics | Load `references/messaging-pubsub.md` |
| IAM service accounts, roles, Secret Manager | Load `references/iam-security.md` |
| Monitoring dashboards, logging, saved queries | Load `references/monitoring-logging.md` |
| GCP projects, regions, organizational hierarchy | Load `references/resource-management.md` |
| Resource ownership, GCP labels, organizational structure | Load `references/resource-ownership.md` |

---

## Core Concepts

### Entity Types

GCP resources use the `GCP_*` prefix and can be queried using the `smartscapeNodes` function. All GCP entities are automatically discovered and modeled in Dynatrace Smartscape.

**Compute:** `GCP_COMPUTE_GOOGLEAPIS_COM_INSTANCE`, `GCP_COMPUTE_GOOGLEAPIS_COM_ADDRESS`
**Networking:** `GCP_COMPUTE_GOOGLEAPIS_COM_NETWORK`, `GCP_COMPUTE_GOOGLEAPIS_COM_SUBNETWORK`, `GCP_COMPUTE_GOOGLEAPIS_COM_ROUTE`, `GCP_DNS_GOOGLEAPIS_COM_RESOURCERECORDSET`
**Kubernetes (GKE):** `GCP_K8S_IO_POD`, `GCP_K8S_IO_NODE`, `GCP_K8S_IO_SERVICE`, `GCP_K8S_IO_SERVICEACCOUNT`, `GCP_K8S_IO_PERSISTENTVOLUMECLAIM`, `GCP_APPS_K8S_IO_DEPLOYMENT`, `GCP_APPS_K8S_IO_STATEFULSET`, `GCP_CONTAINER_GOOGLEAPIS_COM_NODEPOOL`, `GCP_RBAC_AUTHORIZATION_K8S_IO_CLUSTERROLEBINDING`, `GCP_RBAC_AUTHORIZATION_K8S_IO_ROLEBINDING`
**Serverless:** `GCP_RUN_GOOGLEAPIS_COM_SERVICE`, `GCP_RUN_GOOGLEAPIS_COM_REVISION`, `GCP_RUN_GOOGLEAPIS_COM_EXECUTION`
**IAM & Security:** `GCP_IAM_GOOGLEAPIS_COM_SERVICEACCOUNT`, `GCP_IAM_GOOGLEAPIS_COM_ROLE`, `GCP_SECRETMANAGER_GOOGLEAPIS_COM_SECRETVERSION`
**Messaging:** `GCP_PUBSUB_GOOGLEAPIS_COM_TOPIC`
**Monitoring:** `GCP_MONITORING_GOOGLEAPIS_COM_DASHBOARD`, `GCP_LOGGING_GOOGLEAPIS_COM_SAVEDQUERY`
**Infrastructure:** `GCP_REGION`

### Common GCP Fields

All GCP entities include:
- `gcp.project.id` — GCP project identifier
- `gcp.region` — GCP region (e.g., us-central1)
- `gcp.zone` — GCP zone (e.g., us-central1-a)
- `gcp.organization.id` — GCP organization identifier
- `gcp.resource.name` — Resource name
- `gcp.resource.type` — Resource type identifier
- `gcp.asset.type` — GCP asset type
- `gcp.object` — JSON blob containing full resource configuration

### GCP Organizational Hierarchy

GCP resources are organized in a hierarchy:
- **Organization** — Top-level container (`gcp.organization.id`)
- **Folder** — Logical grouping within an organization
- **Project** — Resource container (`gcp.project.id`)
- **Region/Zone** — Physical location (`gcp.region`, `gcp.zone`)

### Entity Naming Convention

GCP entity types follow the pattern `GCP_<SERVICE_API>_<RESOURCE>`:
- Service API maps to the Google API domain (e.g., `compute.googleapis.com` → `COMPUTE_GOOGLEAPIS_COM`)
- Resource is the specific resource type (e.g., `INSTANCE`, `NETWORK`)

Examples:
- `GCP_COMPUTE_GOOGLEAPIS_COM_INSTANCE` — Compute Engine VM
- `GCP_K8S_IO_POD` — GKE pod
- `GCP_RUN_GOOGLEAPIS_COM_SERVICE` — Cloud Run service

---

## Query Patterns

All GCP queries build on four core patterns. Master these and adapt them to any entity type.

### Pattern 1: Resource Discovery

List resources by type, filter by project/region/zone, summarize counts:

```dql
smartscapeNodes "GCP_COMPUTE_GOOGLEAPIS_COM_INSTANCE"
| fields name, gcp.project.id, gcp.region, gcp.zone, gcp.resource.name
```

To list all GCP resource types, replace with `"GCP_*"` and add `| summarize count = count(), by: {type} | sort count desc`. Add filters like `| filter gcp.project.id == "<PROJECT_ID>"` or `| filter gcp.region == "<REGION>"` to scope results.

### Pattern 2: Configuration Parsing

Parse `gcp.object` JSON for detailed configuration fields:

```dql
smartscapeNodes "GCP_COMPUTE_GOOGLEAPIS_COM_INSTANCE"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd machineType = gcpjson[configuration][resource][machineType],
            status = gcpjson[configuration][resource][status]
| fields name, gcp.project.id, machineType, status
```

GCP configuration fields are nested under `gcpjson[configuration][resource][...]` for primary resource attributes and `gcpjson[configuration][additionalAttributes][...]` for extended properties.

### Pattern 3: Relationship Traversal

Follow relationships between resources:

```dql
smartscapeNodes "GCP_COMPUTE_GOOGLEAPIS_COM_INSTANCE"
| traverse "*", "GCP_COMPUTE_GOOGLEAPIS_COM_SUBNETWORK"
| fields name, gcp.project.id
```

GCP entities use `"*"` as the relationship name in traversals because GCP entities do not have named relationship types. Use `fieldsKeep` to carry fields through traversals and `dt.traverse.history[-N]` to access ancestor fields.

### Pattern 4: Label-Based Ownership

Group resources by GCP labels for ownership and organizational tracking:

```dql
smartscapeNodes "GCP_*"
| filter isNotNull(`tags:gcp_labels`)
| fields name, gcp.project.id, `tags:gcp_labels`
```

GCP labels are exposed via the `tags:gcp_labels` field and must be accessed using backtick syntax. Replace `"GCP_*"` with a specific type to scope to one service.

---

## Reference Guide

Load reference files for detailed queries when the core patterns above need service-specific adaptation.

| Reference | When to load | Key content |
|---|---|---|
| [compute-instances.md](references/compute-instances.md) | Compute Engine VMs, machine types, IP addresses, disks | Instance inventory, machine type distribution, status checks |
| [kubernetes-gke.md](references/kubernetes-gke.md) | GKE clusters, node pools, pods, deployments, services, RBAC | Cluster topology, workload distribution, RBAC bindings |
| [serverless-containers.md](references/serverless-containers.md) | Cloud Run services, revisions, executions | Service inventory, revision tracking, execution analysis |
| [networking-dns.md](references/networking-dns.md) | VPC networks, subnets, routes, DNS records | Network topology, subnet analysis, route tables, DNS record sets |
| [messaging-pubsub.md](references/messaging-pubsub.md) | Pub/Sub topics | Topic inventory, messaging topology |
| [iam-security.md](references/iam-security.md) | IAM service accounts, roles, Secret Manager | Service account audit, role analysis, secret version tracking |
| [monitoring-logging.md](references/monitoring-logging.md) | Monitoring dashboards, logging, saved queries | Dashboard inventory, saved query analysis |
| [resource-management.md](references/resource-management.md) | GCP projects, regions, organizational hierarchy | Project inventory, region distribution, hierarchy mapping |
| [resource-ownership.md](references/resource-ownership.md) | Resource ownership, GCP labels, organizational structure | Label-based grouping, project-level summaries, chargeback |

---

## Best Practices

### Configuration Parsing
1. Always parse `gcp.object` with JSON parser: `parse gcp.object, "JSON:gcpjson"`
2. Access primary resource attributes via `gcpjson[configuration][resource][...]`
3. Access extended properties via `gcpjson[configuration][additionalAttributes][...]`
4. Check for null values after parsing with `isNotNull()`

### GCP Hierarchy
1. Organization → Folder → Project → Region/Zone
2. Use `gcp.project.id` as the primary scoping filter
3. Use `gcp.organization.id` for cross-project queries
4. Use `gcp.region` and `gcp.zone` for location-based analysis

### Entity Naming
1. Entity types follow the `GCP_<SERVICE_API>_<RESOURCE>` format
2. Service API maps to the Google API domain with underscores replacing dots and hyphens
3. Use specific entity types (avoid `"GCP_*"` wildcards when possible)

### Labels
1. GCP labels must be accessed via backtick syntax: `` `tags:gcp_labels` ``
2. Use `isNotNull(`tags:gcp_labels`)` for label-based filtering
3. Track label coverage with summarize operations

### Relationship Traversal
1. Use `"*"` as the relationship name — GCP entities do not have named relationship types
2. Use `fieldsKeep` to maintain important fields through traversal
3. Access traversal history with `dt.traverse.history[-N]`
4. Complex topologies may require multiple traverse operations

---

## Limitations and Notes

### Smartscape Limitations
- Smartscape data reflects the most recent scan; there may be a delay between GCP changes and Dynatrace visibility
- Not all GCP services are represented as entity types
- Some configuration fields may be null depending on resource setup
- Resource discovery depends on GCP integration configuration

### GCP-Specific Notes
- GCP labels must be accessed via backtick syntax: `` `tags:gcp_labels` ``
- GCP entities use `"*"` for relationship traversal (no named relationship types)
- GCP object configuration requires parsing with `parse gcp.object, "JSON:gcpjson"`
- Configuration fields nest under `gcpjson[configuration][resource][...]` (differs from AWS pattern)

### General Tips
- Filter early by project and region for better performance
- Use `isNotNull()` and `isNull()` for graceful null handling
- Combine project and region filters for large environments
- Use `countDistinct()` for unique resource counts
- Limit results with `| limit N` during exploration
