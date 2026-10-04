---
name: terraform-iac
description: Deep Terraform/IaC workflow—module boundaries, state, workspaces, plan/apply safety, drift, secrets, CI integration, and team governance. Use when building infra as code, refactoring modules, or debugging state issues.
---

# Terraform / IaC (Deep Workflow)

Terraform’s sharp edges are **state**, **modules**, **dependencies**, and **team workflow**. Guide users toward **reviewable plans**, **least blast radius**, and **recoverable** mistakes.

## When to Offer This Workflow

**Trigger conditions:**

- Greenfield IaC, module extraction, upgrading providers
- “Drift”, failed applies, state lock issues, wrong env destroyed
- CI integration for plan-on-PR, policy-as-code (Sentinel/OPA)

**Initial offer:**

Use **six stages**: (1) scope & structure, (2) modules & interfaces, (3) state & workspaces, (4) secrets & providers, (5) plan/apply & CI, (6) operations & drift. Confirm **cloud(s)** and **remote state backend**.

---

## Stage 1: Scope & Structure

**Goal:** **Repo layout** matches team ownership and blast radius.

### Patterns

- **Monorepo** vs **multi-repo** per env—trade-offs in coordination vs isolation
- **Live** vs **modules** folders; **environment** composition at root

### Naming & tags

- Consistent **resource naming**; **mandatory tags** (owner, env, cost center)

**Exit condition:** Directory layout diagram; **what lives together** vs separate states justified.

---

## Stage 2: Modules & Interfaces

**Goal:** **Reusable** modules with **clear inputs/outputs**—not copy-paste with vars.

### Practices

- **Small** modules with single responsibility; **composition** over mega-modules
- **Variables** with validation blocks; **sensible defaults** documented
- **Outputs** only what consumers need—avoid leaking internals

### Versioning

- **Module registry** or **git refs** pinned; **changelog** for breaking changes

**Exit contract:** Module README: purpose, inputs table, example snippet.

---

## Stage 3: State & Workspaces

**Goal:** **One state** per blast-radius boundary; **no shared state** accidents.

### Remote state

- **Locking** (DynamoDB, native backends); **encryption** at rest
- **IAM** least privilege for state bucket—**state contains secrets sometimes**

### Workspaces vs directories

- Workspaces for **parallel envs** only when truly symmetric; many teams prefer **separate folders** + separate state for clarity

### Imports & moves

- **`moved` blocks** (Terraform 1.x) for refactors; **import** for brownfield—**plan carefully**

**Exit condition:** State **ownership** documented; **who can run apply** in prod.

---

## Stage 4: Secrets & Providers

**Goal:** **No secrets in .tf** committed; **dynamic secrets** where possible.

### Practices

- **Vault/AWS/GCP** providers for secrets; **CI OIDC** over long-lived keys
- **Provider** version pins; **parallelism** awareness for rate limits

**Exit condition:** Secret **flow** diagram; **rotation** doesn’t require editing TF files by hand for normal ops.

---

## Stage 5: Plan / Apply & CI

**Goal:** **Plan before apply**; **peer review** for prod.

### CI

- **`terraform fmt`**, **`validate`**, **`plan`** on PR; **policy checks** optional
- **Artifact** or **comment** plan output; **apply** from protected branch or pipeline only

### Safety

- **`prevent_destroy`** on critical resources when appropriate
- **Targets** for surgical applies—**dangerous** if habitual

**Exit condition:** **Definition of done** for infra change includes reviewed plan.

---

## Stage 6: Operations & Drift

**Goal:** **Detect** manual console changes; **reconcile** safely.

### Drift

- **Periodic** `plan` in automation; **import** or **revert** manual changes with intent

### Break-glass

- Document when **console** changes allowed and how to **backport** to code

### State recovery

- **Backups** if supported; **state file** corruption playbook—**never** edit blindly

---

## Final Review Checklist

- [ ] Module boundaries and versioning strategy clear
- [ ] Remote state + locking + IAM documented
- [ ] Secrets not in VCS; providers pinned
- [ ] CI plan/apply governance defined
- [ ] Drift detection and recovery understood

## Tips for Effective Guidance

- Emphasize **state is truth**—code must match or you pay interest forever.
- Warn: **`count`/`for_each` changes** can destroy/recreate—use **`moved`** and **`lifecycle`** thoughtfully.
- Multi-cloud: abstract patterns, but **don’t hide** provider-specific footguns.

## Handling Deviations

- **Terragrunt/Pulumi**: map stages to equivalent concepts—**stack**, **state**, **modules**.
- **Kubernetes-only**: separate **cluster** IaC from **in-cluster** resources (Helm) boundaries.
