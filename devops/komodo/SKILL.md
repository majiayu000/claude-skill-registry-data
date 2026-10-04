---
name: komodo
description: >-
  Install, configure, troubleshoot and operate Komodo server and Docker
  management. Covers Core and Periphery, container Deployments, Compose
  Stacks, Docker Swarm, image builds, Procedures and Actions, schedules,
  webhooks, Resource Sync, variables and secrets, permissions, backup and
  recovery, and the km CLI and API. Use for Komodo setup, connecting hosts,
  Git-driven deployments, resource reconciliation and multi-step automation,
  including requests phrased as managing an existing app through Komodo.
  Not for unrelated products named Komodo or coding-agent swarms.
---

# Komodo

Komodo manages servers and Docker workloads. **Core** hosts its UI and API.
**Periphery** is the agent on a managed server. A **resource** is a configured
object such as a Server, Deployment, Stack, Build or Procedure.

A **Deployment** manages one container. A **Stack** manages a Compose application.
Docker **Swarm** has separate cluster resources. Determine which model the user
has before choosing commands, configuration or diagnostics.

## How references work

Read only the references for the current task. Descriptive references teach
stable concepts and decisions, then link canonical documentation for changing
configuration fields and defaults. Fetch those pages before generating
version-sensitive configuration. If browsing is unavailable, state the gap
and avoid guessing executable settings.

The operational [CLI reference](references/cli.md) starts with installed help.
Its examples do not authorize executions. A separately installed `komodo-cli`
skill may provide deeper command guidance, but this package does not require it.

## Working sequence

1. Identify the requested outcome and whether it is explanation, configuration
   authoring, diagnosis or execution. Read the appropriate reference below.
2. For real operations, establish Core/profile, installed version, Server and
   resource identity. Determine who owns current configuration: UI, host files,
   a Git repository or Resource Sync. Do not adopt an existing app by deploying
   over it before reconciling that ownership.
3. Inspect the smallest relevant read-only state. Prefer status and redacted
   logs over dumping configuration or environment variables.
4. Describe the exact intended change and affected resources. Get explicit
   approval for production changes, destructive sync, restore/copy, privilege
   elevation, public exposure or arbitrary shell execution. Loading this skill
   is not permission to mutate infrastructure.
5. Verify the observable result: resource status, workload health, execution
   outcome or recovery check. Report what was tested and what remains unknown.

Never reset passwords. Keep credentials out of command arguments, logs and
examples. Do not bypass confirmations with `-y` by default. Do not silently
install tools or request interactive terminal sessions in a noninteractive
harness. Preserve existing network policy rather than broadening access to
make a connection work.

## Find the right approach

```text
What does the user need?
├─ Start managing infrastructure
│  ├─ Install Core or choose a database → installation.md
│  ├─ Connect or diagnose a host → servers-and-terminals.md
│  └─ Give a teammate limited access → access-control.md
├─ Manage an application
│  ├─ One container → containers.md
│  ├─ Compose application → compose.md
│  └─ Docker Swarm cluster/service → docker-swarm.md
├─ Ship and automate
│  ├─ Build or publish images → builds.md
│  ├─ React to image changes or Git pushes → updates-and-triggers.md
│  ├─ Sequence steps or schedule work → automation.md
│  └─ Reconcile TOML resource declarations → resource-sync.md
├─ Integrate tools → api.md or cli.md
└─ Recover or upgrade → backup-and-upgrades.md
```

## Reference map

| Topic | Read when |
| --- | --- |
| [Installation](references/installation.md) | Setting up Core, Periphery, databases or advanced configuration. |
| [Servers and terminals](references/servers-and-terminals.md) | Connecting hosts, checking reachability or accessing runtime sessions. |
| [Access control](references/access-control.md) | Configuring authentication, groups and resource permissions. |
| [Configuration and providers](references/configuration-and-providers.md) | Managing variables, secrets, Git, registry or cloud accounts. |
| [Containers](references/containers.md) | Managing a single-container Deployment and its lifecycle. |
| [Compose](references/compose.md) | Managing a Stack from UI, host files or Git. |
| [Docker Swarm](references/docker-swarm.md) | Managing cluster services/stacks, not coding agents. |
| [Builds](references/builds.md) | Building images, choosing builders or publishing to registries. |
| [Updates and triggers](references/updates-and-triggers.md) | Selecting image updates, Git webhooks and deployment triggers. |
| [Automation](references/automation.md) | Sequencing Procedures, distinguishing Actions or scheduling work. |
| [Resource Sync](references/resource-sync.md) | Reviewing and applying declared resource differences. |
| [API](references/api.md) | Writing integrations using Core APIs and clients. |
| [CLI](references/cli.md) | Forming and safely running installed `km` commands. |
| [Backup and upgrades](references/backup-and-upgrades.md) | Protecting management state, restoring or migrating versions. |

## Authoring defaults

- Keep configuration authority singular. Image watchers, Git webhooks and
  Resource Sync can create competing writers if enabled without coordination.
- Review pending Resource Sync differences before application. Resource
  reconciliation is not the same operation as deploying a Compose app.
- Procedures run stages sequentially and executions within a stage in parallel.
  Actions are TypeScript scripts using Komodo's pre-initialized API client, not
  Procedure stages. Verify version-matched APIs and behavior before writing code.
- Treat terminal and Periphery access as privileged host access. Diagnose trust,
  reachability and permissions separately rather than disabling them together.
- Use build secret mounts, not ordinary build arguments, for secrets.
- Komodo database backup protects management state, not all workload data.
  Include application volumes and external databases in a recovery plan.

## Sources and evidence

Canonical entry point: <https://komo.do/docs/intro>. References were authored
from official documentation consulted 2026-09-28. Site documentation can be
newer than the user's deployment. Verify version-sensitive behavior locally.
This package supplies guidance, not certification of a live deployment or
harness-specific automatic activation.
