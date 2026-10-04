---
name: nomad
description: "Write Nomad jobspecs and task groups, configure networking and variables, and manage workload rollouts."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["nomad", "hashicorp", "scheduler", "jobs", "hcl", "orchestration"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# HashiCorp Nomad Scheduler AI Skill Guide

## Overview

Nomad schedules **jobs** composed of **task groups** and **tasks** onto a client fleet. Drivers include Docker, exec, Java, and others. Compared to Kubernetes, Nomad's jobspec is compact HCL and often pairs with Consul (discovery) and Vault (secrets). Agents should version jobspecs in Git, use constraints/affinities deliberately, and prefer canary/blue-green updates over in-place surprise restarts.

```
nomad job run jobspec.hcl
        |
        v
Servers evaluate + place allocations
        |
        v
Client agents start tasks (docker/exec/...)
        |
        +--> Consul service registration (optional)
        +--> Vault secret templates (optional)
```

## When to use

- Deploying batch or service jobs on Nomad clusters
- Debugging failed allocations, stuck placements, or driver errors
- Defining update strategies (canary, auto-revert)
- Integrating Consul service registration from jobspecs

## Operational directives

1. Always `nomad job plan` before `nomad job run` on shared clusters.
2. Set resource CPU/memory on every task; avoid unbounded tasks.
3. Use distinct job IDs per environment (`api-prod`, `api-dev`).
4. Prefer Docker images by digest; avoid `:latest` in production jobspecs.
5. Store non-secret config in Nomad variables; secrets via Vault when available.

## Concrete examples

### Service jobspec (Docker)

```hcl
job "api" {
  datacenters = ["dc1"]
  type        = "service"

  group "api" {
    count = 2

    network {
      port "http" { to = 8080 }
    }

    update {
      max_parallel = 1
      canary       = 1
      auto_revert  = true
      healthy_deadline = "3m"
    }

    task "api" {
      driver = "docker"
      config {
        image = "ghcr.io/example/api@sha256:..."
        ports = ["http"]
      }
      resources {
        cpu    = 200
        memory = 256
      }
      service {
        name = "api"
        port = "http"
        check {
          type     = "http"
          path     = "/healthz"
          interval = "10s"
          timeout  = "2s"
        }
      }
    }
  }
}
```

### CLI workflow

```bash
nomad job plan api.hcl
nomad job run api.hcl
nomad status api
nomad alloc status <alloc-id>
nomad alloc logs <alloc-id>
nomad job scale api api 4
nomad job stop -purge api   # only with explicit approval
```

### Placement troubleshooting

| Symptom | Cause | Action |
| :--- | :--- | :--- |
| queued / exhausted | Insufficient CPU/memory | Scale clients or lower asks |
| driver failure | Docker image/auth | Check client logs; registry creds |
| unhealthy canary | Check failing | `alloc logs`; auto-revert should fire |
| constraint mismatch | Class/unique constraints | Relax or label nodes |

## Best practices

1. Pin Nomad version skew between servers and clients within support policy.
2. Use namespaces and ACLs on multi-team clusters.
3. Emit job versions via CI; annotate with Git SHA in meta.
4. Prefer host volumes / CSI carefully - document data lifecycle.

## Limitations

- Ecosystem differs from Kubernetes; not all k8s controllers map 1:1.
- Advanced networking (CNI/bridge) needs cluster-specific docs.
- Without Consul/Vault, service discovery and secrets are DIY.

## Related skills

- `consul` - service discovery and checks from Nomad tasks
- `vault` - secret injection patterns
- `docker` - task image build/publish
- `packer` - golden client node images
