---
name: mk:devops
description: "Plan and implement infrastructure, containers, CI/CD, deployment safety, observability, and rollback changes. Use for Docker, IaC, cloud runtime, Kubernetes, pipeline, deployment, or operational reliability work. Does not read dotenv files or approve/release deployments."
version: 1.0.0
argument-hint: '[platform or infrastructure change]'
source: local
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
keywords:
  - infrastructure
  - containers
  - ci-cd
  - deployment-safety
  - rollback
  - runtime-config
  - observability
  - incident-diagnosis
  - blast-radius
when_to_use: Use when changing infrastructure-as-code, containers, pipelines, runtime configuration, or observability, or when planning deployment safety, rollback, or operational diagnosis. NOT for approving or executing a release, reading secrets, code root-cause analysis (mk:investigate), schema semantics (mk:database), or the security verdict.
user-invocable: true
owner: portability
criticality: high
status: active
runtime: portable
---

# DevOps

Infrastructure and delivery safety. It designs and prepares the change; a human performs the
production effect.

## Ownership

| Owner | Owns | Does NOT own |
|---|---|---|
| `mk:api-design-principles` | Interface contract: resource/type/message shape, error and authorization *requirements*, compatibility and deprecation, consumer discovery | Implementation, persistence, security verdict, release |
| `mk:backend-development` | End-to-end backend change: discovery, classification, service/handler/integration work | Contract authorship, schema/SQL, security verdict, deploy |
| `mk:database` | Data invariants, schema, migration and recovery, query/index evidence, ORM boundary | API contract, authorization verdict, infrastructure execution |
| `mk:devops` | Infrastructure-as-code, containers, CI, runtime config, deployment *safety design*, rollback planning, incident diagnosis | Deploy approval and execution, security verdict, code root-cause, schema semantics |

Routing rules — identical in all four skills:

- **Contract-only API question → `mk:api-design-principles`**, even in the middle of a task
  owned by another skill. "Contract" means what a consumer can observe: field set, error
  shape, status semantics, pagination, versioning. Extending an endpoint without changing
  any of those is not a contract change.
- **End-to-end backend change → `mk:backend-development`**, which invokes the API skill only
  when a new, public, or breaking contract is in scope.
- **A message-based change (event, webhook, RPC) splits**: the message contract belongs to
  `mk:api-design-principles`; the producer or consumer implementation belongs to
  `mk:backend-development`.
- **Schema, migration, query, index, or ORM work → `mk:database`.** No other skill writes a
  migration or generic SQL.
- **Infrastructure, containers, delivery, or deployment safety → `mk:devops`.**
- **An unscoped performance request is triaged by evidence, never by guess**:
  `mk:backend-development` locates where the time actually goes, then hands a query or index
  question to `mk:database` and a capacity or runtime question to `mk:devops`. No skill
  invents the target.
- **Code root cause → `mk:investigate`.** `mk:devops` owns the operational picture — what
  changed, where it fails, which signal proves it — and hands the defect over.
- **An auth-sensitive change**: the owning skill states the *requirement*; the security
  workflow owns the verdict.
- **Any production effect → `mk:ship` or a human.**

## Secret boundary

Not negotiable, and not conditional on the task.

- Never read, grep, print, or otherwise open a `.env` or `.env.*` file at any depth,
  including toolkit- and agent-directory dotenv files, a keystore, a credential file, or a
  generated config that carries credentials.
- Never ask the user to paste a secret value into the conversation.
- Never echo command output that contains a secret; if a command would print one, do not
  run it.
- Read only committed templates, configuration, and infrastructure definitions. Rely on the
  environment the runtime injects into the subprocess.
- If availability of a value cannot be proven from a tracked file, stop at a readiness
  report naming the missing capability. Never infer that a secret exists, and never infer
  that it does not.

## Workflow

### 1. Discover the platform

Read the tracked evidence: container definitions, infrastructure-as-code, pipeline
definitions, runtime manifests, deployment configuration, and the project's own
documentation.

If the platform is not discoverable, **ask**. Do not pick a cloud, an orchestrator, or a
hosting model as a default — a guessed platform produces confidently wrong configuration.

### 2. Classify

| Class | The question being answered |
|---|---|
| Local container | How does this build and run reproducibly? |
| CI | What runs on a change, and what must it prove? |
| Infrastructure | What resources exist, and what does changing them touch? |
| Runtime config | What does the process need at start, and where does it come from? |
| Observability | What signal would show this failing? |
| Release / rollback | How does the change reach production, and how does it come back? |
| Incident diagnosis | What is failing now, and what evidence says so? |

### 3. Safety design

Before writing any change, state:

- **Blast radius** — what this can affect if it is wrong, including resources not named in the diff.
- **Stateful resources** — anything holding data. Deleting or replacing one is not a
  configuration change; call it out separately.
- **Environment contract** — which variables the runtime requires, taken from the tracked
  template only, as names and purposes. Never values.
- **Rollback or forward recovery** — the concrete path back. "Redeploy the previous version"
  is only a plan if the previous version is still available and the change is reversible.
- **Approval point** — the exact step a human performs.
- **Validation** — the read-only check that proves the change is right before anyone applies it.

Load `references/infrastructure-change-safety.md` for an infrastructure, deployment, or
rollback change. Load `references/container-and-ci.md` for container or pipeline work.

### 4. Implement inside an approved plan

Write the configuration, manifest, or pipeline change. Produce the read-only plan or diff
evidence for the tool in use, and read it — an unread plan output is not evidence.

Do not run the apply, deploy, destroy, or release step, and do not emit one as a
ready-to-run command. Describe what the operator will run and what they should see.

### 5. Hand off

The production effect goes to `mk:ship` or a human, with: the change, the plan/diff
evidence, the blast radius, the rollback path, and the validation to run after.

## Output

A change plus a safety record: platform evidence, classification, blast radius, stateful
resources, environment contract (names only), rollback path, approval point, validation
command, and the handoff.

## References

| File | Load when |
|---|---|
| `references/container-and-ci.md` | Container images, local runtime composition, or pipeline definitions |
| `references/infrastructure-change-safety.md` | Infrastructure-as-code, deployment, rollback, or incident diagnosis |

## Gotchas

- **No cloud is the default.** Not the one in the last project, not the one the tooling
  makes easiest. Discover it or ask.
- **A plan or diff that nobody read is not evidence.** Quote the resources it would change,
  especially the ones being replaced rather than updated.
- **"Replace" on a stateful resource is data loss.** Read every plan for replacement of a
  database, volume, bucket, or disk before anything else in it.
- **A rollback that requires the failing system to be healthy is not a rollback.** Check
  that the recovery path works when the thing being rolled back is down.
- **Invent no number.** No availability target, replica count, timeout, resource limit, or
  retention period unless the repository states it or the user chose it.
- **A missing environment variable is a readiness finding, not a prompt for the value.**
  Report the name and where the template expects it.
- **An operational symptom is not a root cause.** Elevated errors after a deploy point at a
  change window; the defect itself belongs to `mk:investigate`.
- **CI credentials live in the platform's secret store, never in a tracked file** — a
  pipeline change must reference a secret by name only.
