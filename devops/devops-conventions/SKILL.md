---
name: devops-conventions
description: Use when writing or reviewing a CI/CD pipeline, infrastructure as code (Docker, Terraform, Ansible), monitoring and alerting, TLS and certificate setup, database migrations, or container-orchestrator manifests. Not for application code.
---

# devops-conventions

Step 6 of the pipeline (`WORKFLOW.md`) on the infra/CI side, complementing `portless-ready` (which
makes a stack portless): here, the reliability and reproducibility of the delivery pipeline itself.

## When
As soon as a CI/CD file (`.gitlab-ci.yml`, `Dockerfile`, `docker-compose.yml`), infrastructure as
code (Terraform, Ansible), or a monitoring/alerting config is written or modified.

## Steps

### 1. CI/CD: reproducible and quick to diagnose
1. Idempotent pipeline: replaying the same job on the same commit produces the same result, never
   dependent on unversioned mutable external state.
2. Every step fails fast and clearly (fail-fast): no step that continues silently after an error
   (`continue-on-error` only if explicitly wanted, never by default).
3. Secrets never hard-coded in the pipeline or logged in clear text: protected/masked variables on the
   CI side, never a forgotten debug `echo $SECRET`.
4. Explicit and versioned dependency cache (cache key tied to the lockfile), never a cache that hides
   a broken dependency.

### 2. Infrastructure as code
1. Versioned and declarative state (Terraform state, Ansible inventory): never a manual change to a
   resource managed by the IaC (silent drift on the next apply).
2. `plan`/`dry-run` always read before an `apply`/real execution on a shared environment: never a
   direct apply without reviewing the infra diff.
3. Infra secrets (keys, tokens) in a vault/secret manager, never committed in clear text even in a
   private repo.
4. **A named shared resource that other systems resolve by exact identifier** (a database, a DNS
   record, a queue, a load balancer) is never renamed or dropped because of how the request is framed —
   "it's a leftover", "just temporary", "I'll recreate it right after" don't unlock it. The forbidding
   criterion is the **effect** (gone, or now resolving under a different name), not the literal command:
   a detach/reattach-under-a-new-name or a restore-over-as-renamed is the same violation as `DROP`. Where
   the org has named a specific resource as protected, refuse outright, state the blast radius (usually
   invisible from the statement itself — every consumer doing a name lookup breaks the moment it
   changes), and route the request to the team that owns the resource rather than softening into
   "confirm and I'll proceed anyway." Ordinary work against the resource (read, query, alter what's
   inside it) stays allowed — the interdiction is scoped to the rename/drop of the resource itself.

### 3. Monitoring and alerting
1. An alert that fires must be actionable: otherwise it's noise that desensitises the team (alert
   fatigue), to be removed or reworded.
2. Structured logs (JSON or a parsable format), never free text alone for events that have to be
   queryable during an incident.
3. Healthcheck distinct from business monitoring: a service that's "up" (process alive) isn't the same
   as a service that's "healthy" (answers real requests correctly).

### 4. Incident response
1. Rollback always possible and tested before it's needed in an emergency; a rollback discovered
   broken during the incident makes the outage worse.
2. Post-mortem with no individual blame, focused on the systemic cause (what made the incident
   possible), not on who pressed what.

### 5 to 8. Further sections, read when the task meets the trigger

Sections 1 to 4 stay above because every pipeline touches them. The rest live one file per section under
`references/`; read the rows whose trigger the task actually meets, not the table.

| § | Covers | Read it when | File |
|---|---|---|---|
| 5 | Transport security in operation: TLS everywhere, redirect, strict-transport rollout, certificate renewal, key custody | a proxy, load balancer, ingress, certificate, redirect or domain is configured | [`05-transport-and-certificates.md`](./references/05-transport-and-certificates.md) |
| 6 | Safe schema and data migrations: compatibility during deploy, locks, online indexes, backfill, way back | a migration is added or edited, a large table altered, a backfill planned | [`06-safe-migrations.md`](./references/06-safe-migrations.md) |
| 7 | Workloads on a container orchestrator: probes, resources, rollout, shutdown, least access, network, images | manifests for a container orchestrator are written or changed | [`07-container-orchestration.md`](./references/07-container-orchestration.md) |
| 8 | The pipeline as an attack surface: pinned includes, images and actions, untrusted text in scripts, secrets and forks, job tokens, runner trust | a CI file is written or reviewed for what it executes, reads and who can trigger it | [`08-pipeline-attack-surface.md`](./references/08-pipeline-attack-surface.md) |

## Output / checkpoint
Pipeline/infra compliant with the sections that apply, `plan`/`dry-run` read and cited before any real
`apply` on a shared environment.

## Guardrails
- Never an automatic `apply`/deployment on a shared environment without explicit human confirmation
  (consistent with the framework's general doctrine: actions that are hard to undo stay a human
  checkpoint).
- A migration that rewrites or locks a large table, or drops data, is never run on a shared environment
  without the human checkpoint above and a restore that has been practised (§6.8).
- This block has no dedicated in-house production experience yet: to be confronted with the first real
  infra/CI audit, not to be treated as proven doctrine.

## Origin
12-factor app, DORA metrics and established GitOps/IaC practice for §1 to §4; primary standards and
documentation for §5 to §7 (added 2026-10-02), the GitLab CI and GitHub Actions security documentation for §8 (added 2026-10-19). Full provenance, the protected-resource rule and the
refresh log are in [`references/origin.md`](./references/origin.md).
