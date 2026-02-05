---
name: confighub-usage-guide
description: |
  A comprehensive guide for using ConfigHub to manage Kubernetes configuration across multiple environments using Configuration as Data principles. This rulebook covers installation, configuration management, variant handling, and operational workflows.
license: MIT
tags:
  - confighub
  - kubernetes
  - configuration-management
  - gitops-alternative
  - config-as-data
  - multi-environment
metadata:
  author: Stakpak <team@stakpak.dev>
  version: "1.0.2"
---

# ConfigHub Usage Guide

## Goals

This rulebook helps you:
- Adopt ConfigHub's Configuration as Data approach for managing Kubernetes deployments
- Manage configuration variants across multiple environments (dev, staging, prod)
- Implement safe change workflows with review, approval, and rollback capabilities
- Eliminate configuration drift between desired and live state
- Automate configuration validation, transformation, and deployment

---

## Key Concepts

### Configuration as Data vs Infrastructure as Code

ConfigHub stores **fully rendered, literal configuration** (WET - Write Every Time) instead of templates with variables. This means:
- No Helm templates, no variable interpolation, no conditionals
- Every environment's config is stored independently in standard YAML
- Changes are made via API/CLI, not git commits and CI/CD pipelines
- Configuration can be queried, validated, and transformed using composable tools

### Core Entities

- **Unit:** A collection of related Kubernetes resources (e.g., Deployment + Service + Ingress)
- **Space:** Logical grouping for units, typically representing an environment or team
- **Revision:** Immutable snapshot of a unit's configuration at a point in time
- **Worker:** Process running in your infrastructure that executes apply/destroy/refresh operations
- **Target:** Represents a deployment destination (Kubernetes cluster)
- **Function:** Code that reads/writes configuration data (readonly, mutating, or validating)
- **Trigger:** Automated function execution on configuration changes (validation, policy enforcement)
- **Link:** Dependency relationship between units for value propagation and apply ordering

---

## Workflow

### Step 1: Install the CLI

Install the `cub` CLI tool:

```bash
curl -fsSL https://hub.confighub.com/cub/install.sh | bash
```

Add to your PATH:

```bash
# Choose one method:
sudo ln -sf ~/.confighub/bin/cub /usr/local/bin/cub
# OR
export PATH=~/.confighub/bin:$PATH
```

**Reasoning:** The CLI is your primary interface for ConfigHub operations. It provides both interactive and scriptable access to all ConfigHub features.

### Step 2: Authenticate and Set Context

Login and configure your default space:

```bash
# Authenticate via browser
cub auth login

# Set default space (replace with your space slug)
cub context set --space <SPACE_SLUG>

# Verify context
cub context get
```

**Reasoning:** Context configuration reduces repetitive flags in subsequent commands.

### Step 3: Create Space Hierarchy for Environments

Organize your environments using spaces with labels:

```bash
# Create a home space for shared entities
cub space create home

# Create environment-specific spaces
cub space create app-dev --label Environment=dev --label Application=myapp
cub space create app-staging --label Environment=staging --label Application=myapp
cub space create app-prod --label Environment=prod --label Application=myapp

# Create platform spaces for shared infrastructure
cub space create platform-dev --label Environment=dev
cub space create platform-prod --label Environment=prod
```

**Reasoning:** Spaces provide isolation boundaries. Labels enable bulk operations across related spaces using where filters.

### Step 4: Set Up Validation Triggers

Install essential validation triggers in your home space:

```bash
# Schema validation (always recommended)
cub trigger create --space home valid-k8s Mutation Kubernetes/YAML vet-schemas

# Placeholder validation (prevents applying incomplete config)
cub trigger create --space home complete-k8s Mutation Kubernetes/YAML vet-placeholders

# Context enforcement (adds metadata to resources)
cub trigger create --space home context-k8s Mutation Kubernetes/YAML ensure-context true
```

Apply triggers to other spaces:

```bash
homeSpaceID="$(cub space get home --jq '.Space.SpaceID')"
cub space create app-dev --label Environment=dev --where-trigger "SpaceID = '$homeSpaceID'"
```

**Reasoning:** Triggers enforce policies automatically. Installing them early prevents invalid configurations from being created or applied.

### Step 5: Deploy and Configure Workers

Create and deploy a worker to enable apply/destroy/refresh operations:

```bash
# Create worker entity
cub worker create --space platform-dev cluster-worker

# Install worker in your cluster
cub worker install cluster-worker \
  --space platform-dev \
  --env IN_CLUSTER_TARGET_NAME=dev-cluster \
  --export --include-secret | kubectl apply -f -

# Verify worker is connected
cub worker list --space "*"
```

**Reasoning:** Workers execute operations in your infrastructure with your credentials. They never send credentials to ConfigHub, maintaining security boundaries.

### Step 6: Import or Create Initial Configuration

**Option A: Import from existing cluster**

```bash
# Import specific resources
cub unit import --space app-dev frontend \
  --namespace myapp \
  --resource-type apps/v1/Deployment \
  --resource-name frontend

# Import entire namespace
cub unit import --space app-dev myapp-all \
  --namespace myapp
```

**Option B: Create from Helm chart**

```bash
# Add Helm repo
helm repo add bitnami https://charts.bitnami.com/bitnami --force-update

# Install chart as ConfigHub unit
cub helm install myapp bitnami/nginx \
  --space app-dev \
  --namespace myapp \
  --values values.yaml
```

**Option C: Create from YAML files**

```bash
# Validate locally first
cub function local vet-schemas deployment.yaml

# Create unit
cub unit create --space app-dev frontend deployment.yaml
```

**Reasoning:** ConfigHub works with existing infrastructure. Import captures current state, while Helm integration leverages the ecosystem. Direct YAML creation works for custom configurations.

### Step 7: Create Configuration Variants

Clone units to create environment variants:

```bash
# Clone single unit to another space
cub unit create --space app-staging \
  --upstream-space app-dev \
  --upstream-unit frontend

# Clone all units from dev to multiple prod spaces
cub unit create --space app-dev \
  --where-space "Labels.Environment = 'prod'"
```

**Reasoning:** Cloning maintains upstream/downstream relationships, enabling controlled propagation of changes while preserving environment-specific overrides.

### Step 8: Manage Dependencies with Links

Create links to propagate values and control apply order:

```bash
# Link backend to namespace (propagates namespace value)
cub link create --space app-dev - backend app-namespace

# Link backend to database (establishes apply order)
cub link create --space app-dev - backend database

# Bulk link all units to namespace
cub link create --space "*" \
  --where-space "Slug = 'app-dev'" \
  --where-from "Slug != 'app-namespace'" \
  --where-to "Slug = 'app-namespace'"
```

**Reasoning:** Links automate value substitution (replacing placeholders) and ensure correct apply/destroy ordering based on dependencies.

### Step 9: Attach Targets to Units

Attach deployment targets to enable apply operations:

```bash
# Attach target to specific unit
cub unit set-target --space app-dev frontend platform-dev/dev-cluster

# Bulk attach to all units in environment
cub unit set-target --space "*" \
  --where "Space.Labels.Environment = 'dev'" \
  platform-dev/dev-cluster
```

**Reasoning:** Targets specify where configuration should be applied. Units without targets cannot be applied.

### Step 10: Make Configuration Changes

Use functions to modify configuration:

```bash
# Update container image
cub function do --space app-dev --unit frontend \
  --change-desc "Update to v1.2.3" \
  set-image-reference main ":v1.2.3"

# Set resource limits
cub function do --space app-dev --unit frontend \
  set-container-resources main all 500m 512Mi 2

# Set environment variable
cub function do --space app-dev --unit frontend \
  set-env-var main DATABASE_URL "postgres://db:5432/myapp"

# Bulk update across environments
cub function do --space "*" \
  --where "Labels.Application = 'myapp' AND Space.Labels.Environment = 'prod'" \
  --change-desc "Production image update" \
  set-image-reference main ":v1.2.3"
```

**Reasoning:** Functions provide type-safe, validated configuration changes. They're more reliable than manual YAML editing and support bulk operations.

### Step 11: Implement Change Management with ChangeSets

Group related changes using ChangeSets:

```bash
# Create ChangeSet
cub changeset create --space home release-v123 \
  --description "Release v1.2.3: Bug fixes and new features"

# Open ChangeSet (add units to it)
cub unit update --patch --space app-prod \
  --filter home/prod-app-filter \
  --changeset home/release-v123 \
  --change-desc "Starting release v1.2.3 rollout"

# Make changes (they'll be part of the ChangeSet)
cub function do --space app-prod \
  --changeset home/release-v123 \
  --filter home/prod-app-filter \
  --change-desc "Update image to v1.2.3" \
  set-image-reference main ":v1.2.3"

# Close ChangeSet
cub unit update --patch --space app-prod \
  --filter home/prod-app-filter \
  --changeset -
```

**Reasoning:** ChangeSets provide atomic, trackable change groups. They enable coordinated rollouts and rollbacks across multiple units.

### Step 12: Review and Approve Changes

If approval triggers are configured:

```bash
# Approve specific revision
cub unit approve --space app-prod frontend --revision 5

# Bulk approve ChangeSet
cub unit approve --space app-prod \
  --filter home/prod-app-filter \
  --changeset home/release-v123
```

### Step 13: Apply Configuration

Apply changes to clusters:

```bash
# Apply single unit
cub unit apply --space app-dev frontend

# Apply all units in environment
cub unit apply --space "*" \
  --where "Space.Labels.Environment = 'dev'"

# Apply with dry-run first
cub unit apply --space app-prod frontend --dry-run
```

### Step 14: Monitor and Refresh State

Keep ConfigHub in sync with live state:

```bash
# Refresh single unit
cub unit refresh --space app-dev frontend

# Bulk refresh
cub unit refresh --space "*" \
  --where "Space.Labels.Environment = 'dev'"

# Check drift
cub unit get --space app-dev frontend --jq '.Unit.DriftStatus'
```

### Step 15: Rollback When Needed

Revert to previous configurations:

```bash
# View revision history
cub unit get --space app-dev frontend --jq '.Unit.Revisions'

# Rollback to specific revision
cub unit rollback --space app-dev frontend --revision 3

# Rollback entire ChangeSet
cub unit rollback --space app-prod \
  --filter home/prod-app-filter \
  --changeset home/release-v123
```

---

## References

- [ConfigHub Documentation](https://docs.confighub.com)
- [Configuration as Data Principles](https://docs.confighub.com/concepts/config-as-data)
- [CLI Reference](https://docs.confighub.com/cli)
