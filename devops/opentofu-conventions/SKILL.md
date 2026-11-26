---
name: opentofu-conventions
description: "OpenTofu conventions for file layout, typed variables, providers, state, naming, sensitive secrets and the Kubernetes provider boundary. Use when writing, reviewing or refactoring OpenTofu or Terraform code, or running a tofu command."
---

# OpenTofu conventions

Infrastructure as code is written with OpenTofu. Terraform only where configured.

## When to use

- Writing or changing `.tf` files.
- Reviewing infrastructure code.
- Setting up a new root module or a module.
- Running `tofu init`, `plan`, `apply`, `validate` or `tflint`.

## Rules

### Tooling

- `tofu` is the binary. `terraform` only in a repository whose config sets `iac: terraform`.
- `tofu fmt`, `tofu validate` and `tflint` before every commit. They, `tofu plan` and
  `trivy config` (the misconfiguration scan) run freely, no confirmation needed.
- `tofu apply` asks for confirmation first. `tofu destroy` is never run by an agent.
- `tofu output` and `tofu state show` are never run, both print secrets in clear. Read a secret
  through a `sensitive` aware path in code, or ask the user to read it themselves.
- `required_version` is set, provider versions constrained with `~>`. Lock file committed.

### Files

- `main.tf` for resources, `variables.tf` for inputs, `outputs.tf` for outputs, `versions.tf` for
  `required_version` and `required_providers`, `providers.tf` for provider configuration,
  `locals.tf` for locals.
- Every variable is declared in `variables.tf`, never in another file.
- Split `main.tf` by topic once it grows, for example `network.tf` or `storage.tf`.

### File order

- A data source comes before the resource or module call that reads it.
- Inside a resource: `count`/`for_each`, arguments, `tags`, blocks, `lifecycle`, `depends_on`.
- Inside a variable: `type`, `description`, `default`, `sensitive`, `validation`, in that order.
- Multiple provider configurations: the default, without `alias`, comes first, aliases after it.

### Naming

- Resource and variable names are stable, descriptive, snake_case. No index encoded into a name.
- One name per concept, consistent between a root module and the modules it calls.

### Variables and outputs

- Every variable has a `type` and a `description`. A default only where it is genuinely safe.
- Secret variables and outputs carry `sensitive = true`. Never a secret as a literal default.
- Values in named tfvars files, committed. Secrets only in `secrets.tfvars`, ignored by git.
- A secret read from a provider that does not mark it sensitive is wrapped in `sensitive()` at
  every use.
- No secret goes into an output in clear, marked sensitive or not: state keeps an output's value in
  plain text regardless of the flag. Pass a value between modules through a remote state data
  source instead.
- `validation` blocks where a wrong value would fail late or silently.

### Providers

- Official provider from the registry, pinned with `~>`. Never a fork or an abandoned provider.
- Provider configuration lives in the root module only. A module declares `required_providers` and
  configures nothing.
- The Kubernetes provider is used directly for a typed resource when a chart would add nothing:
  Namespace, ConfigMap, Secret, ServiceAccount, RBAC, StorageClass. See `kubernetes-conventions`
  for the full boundary against `helm_release`.

### Resources

- `for_each` over `count`. Adding or removing one element must not recreate the others.
- No environment specific value hardcoded. Use a variable instead.
- `prevent_destroy = true` on a server and on a stateful resource: a database, a volume, a bucket.

### State

- `backend "s3"` against S3 compatible object storage, with `use_lockfile = true` for locking.
  No separate lock table or lock resource. Never local state, never a state file committed.
- `encryption {}` sits inside `terraform {}`, in `versions.tf`: `key_provider "pbkdf2"` derives
  the key, `method "aes_gcm"` encrypts `state` and `plan` with it. No default, it fails without one.
- `unencrypted` is a declared `method`, used from the `fallback` block in `state` or `plan`, for the
  migration off plaintext state. Remove it once every module has applied once with encryption on.
- A scheduled backup of the state to a second provider, different from the one holding the
  primary copy. Object storage with no previous version to restore has no other way back.
- `tofu init -backend=false` for a check that needs no state and no backend credentials.
- One root module per blast radius, reading the state of the module before it, never the
  reverse. No wrappers, no generated HCL: resources are written out by hand.

### Secrets

- A provider token comes from a data source against the secret manager, declared in
  `providers.tf`. Never a token pasted into a file or left as a default.
- A provider that does not mark a value sensitive gets it wrapped in `sensitive()` at every use.
- A key that may not exist yet is read behind a guard, not a lookup that fails the whole plan.
- Backend credentials and the encryption passphrase come from the environment, never the secret
  manager: both resolve before any provider is configured and cannot read one.
- A value that must never reach state, a kubeconfig, say: an `ephemeral` resource reads it, a
  write-only attribute (write-only pattern, `_wo` provider convention) passes it on, null in state.

### Adoption

- An existing resource is brought under management with an `import {}` block, applied through the
  plan workflow, never by deleting and recreating it.
- The ID in the block gets a comment: a read-only inventory command, or a documented API call
  where the CLI has no listing command, run once and not part of the apply.

## Guardrails

- Never run `tofu destroy`. Report the need and let the user run it.
- Never run `tofu output` or `tofu state show`. Both print secrets in plain text.
- Never apply without a plan that was reviewed and confirmed first.
- Never run a `terraform` command unless `.agent-skills.json` sets `iac: terraform`.
- Never give a chart or an inline manifest a job a typed provider resource already does cleanly.

## Config

- `iac`: infrastructure tool. Default: `opentofu`. `terraform` only when set explicitly.

## References

- `tofu-plan` for the plan and apply workflow.
- `tofu-module` for module layout.
- `kubernetes-conventions` for the Kubernetes provider and Helm boundary.
