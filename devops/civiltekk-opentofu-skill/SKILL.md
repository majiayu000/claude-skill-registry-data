---
name: civiltekk-opentofu-skill
description: >-
  OpenTofu/Terraform infrastructure as code, four routes. first-time-setup:
  configure cloud providers, authentication, and remote state backends (S3,
  Azure Storage, GCS). plan-apply: provisioning workflow — plan→apply
  discipline, resource lifecycle, state management and drift. explore:
  AWS, Kubernetes, Neon Postgres, and Keycloak resources as code.
  shared-infra-split: provision-once shared modules (ECR/Amplify pattern)
  vs per-env stacks, and live migrations between the two. Triggers:
  opentofu, tofu, terraform plan, terraform apply, infrastructure as code,
  IaC, provider setup, provider pin, state backend, remote state, drift,
  tofu import, Neon branching, Keycloak realm, Helm release, Kubernetes as
  code, shared module, provision once, module split, shared infra.
license: Apache-2.0
compatibility: opencode
category: OpenTofu
---

Consolidates opentofu-provider-setup-skill + opentofu-provisioning-workflow-skill
+ opentofu-aws-explorer-skill + opentofu-kubernetes-explorer-skill +
opentofu-neon-explorer-skill + opentofu-keycloak-explorer-skill +
opentofu-ecr-provision-skill (#604). Alias: formerly those seven skills.

## What I do

OpenTofu/Terraform infrastructure as code across four routes — provider
bootstrap, provisioning workflow, per-platform resource exploration, and
shared-module organization. OpenTofu/Terraform are interchangeable (OpenTofu is
provider-compatible); house commands use `tofu`.

1. **Detect the route** (§Routes) — explicit > inferred > ask-once.
   Explicit: the request names the activity ("set up providers", "state
   backend" → `first-time-setup`; "plan and apply", "update infrastructure",
   "state drift" → `plan-apply`; "AWS/Kubernetes/Neon/Keycloak resources"
   → `explore`; "shared
   module", "split the module", "provision once", "which module owns X" →
   `shared-infra-split`). Inferred:
   the artifact shape (a bootstrap `versions.tf` → `first-time-setup`; a
   reviewed change → `plan-apply`; platform resource work → `explore`;
   a singleton resource
   claimed by multiple env stacks → `shared-infra-split`). Ambiguous →
   ask once per run, then proceed on the answer.
2. **Load the route's reference file** (§Side files) and apply its pins,
   conventions, and rules — do not improvise provider versions or backend
   shapes.
3. **Follow the route's workflow discipline** — canonical commands in
   `references/workflow.md` apply to every route; route-specific workflows
   live in the reference files.

## Route chain (stated once)

**`first-time-setup` precedes everything** — provider authentication and the
remote state backend must exist before any `plan-apply` or `explore`
work. The former per-skill prerequisite chain
("Complete opentofu-provider-setup-skill first") is this internal ordering:
when a request assumes infrastructure that has not been bootstrapped, run
`first-time-setup` (or verify its outputs) first. Every
`explore` platform additionally flows through `plan-apply` discipline for any
change they make.

## Routes

| Situation | Route |
|-----------|-------|
| New OpenTofu project; provider blocks, authentication, remote state backend (S3/Azure/GCS) | `first-time-setup` |
| Creating/updating/destroying infrastructure; plan review; state management, drift, imports; lifecycle rules | `plan-apply` |
| AWS, Kubernetes (incl. Helm), Neon Postgres, or Keycloak resources as code | `explore` |
| Which module owns a resource; creating a shared provision-once module (ECR/Amplify pattern); migrating a live resource out of an env stack into a shared module | `shared-infra-split` |
| Ambiguous | ask once (§What I do step 1), then route |

## Side files (load rules)

| Read | When | Use |
|------|------|-----|
| `references/provider-setup.md` | route `first-time-setup` | Chain-root values: provider pin table, per-provider auth essentials, state-backend selection + migration learning |
| `references/workflow.md` | route `plan-apply` (and any route that changes state) | Canonical command workflow, plan-file discipline, lifecycle/state rules, imports, the two CI/CD anti-patterns |
| `references/explorers.md` | route `explore` | Four sections — AWS, Kubernetes, Neon, Keycloak: provider pins, connection methods, house conventions, learnings |
| `references/shared-infra-split.md` | route `shared-infra-split` | Ownership decision table, shared-module contracts, live-migration recipe, for_each/sensitive trap |

Side files carry VALUES only; this file carries the METHOD — route
detection, the chain, and the workflow discipline pointer.

## Boundaries

- AWS IaC safety review (pre-apply blast radius, destructive-change triage)
  is `aws-iac-safety-skill`'s space — this skill provisions; that skill
  audits.
- Container image building and registry composition is
  `docker-containerization-skill`'s space.
- Provider schemas and per-resource HCL are model knowledge — side files
  carry house pins and conventions only; do not expect full resource
  walkthroughs.
- `opentofu-explorer-subagent` is the agent that runs this skill by route
  (delegated IaC work keeps `tofu` output out of the primary context).

## Agent behavior rules

- **Never bare `tofu apply`** — always `plan -out` then `apply tfplan`
  (full rule in `references/workflow.md`).
- **Ask once on ambiguity** — then proceed; headless/CI: no asks, read the
  route from the delegation prompt and use the documented default.
- **Verify before success** — a change is successful only after `tofu
  apply` of the reviewed plan and `tofu state list` shows the expected
  resources.
- `tofu` CLI commands need bash (git-bash/WSL on Windows).

## Return Contract

```
**Status:** [success | partial | failed]
**Output:** [resources/modules changed + route used — one line]
**Summary:** [2–3 sentences max]
**Issues:** [blockers, warnings, uninspected consumers, or "None"]
```
