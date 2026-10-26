---
name: terraform
description: Use when declaring cloud and DNS resources with Terraform — importing resources that already exist, provider major-version migrations, remote or local state, plan-then-apply discipline, cost guardrails before creating paid resources, and splitting stacks per service. Also use when plan shows unexpected changes, state is empty but resources exist, or a provider upgrade breaks resource schemas.
---

# Terraform

Default: one stack (directory) per service, pinned Terraform and provider versions, `plan` reviewed before every `apply`, existing resources imported rather than recreated, budgets and alerts created before anything that costs money.

## Layout

```text
<service>/
  versions.tf     required_version + required_providers with ~> constraints
  main.tf         resources
  variables.tf    inputs (no secrets in defaults)
  outputs.tf
```

- Credentials come from the environment (provider-specific variables or a CLI login), never from `.tf` files or committed variable files.
- Commit `.terraform.lock.hcl`; do not commit state or `.terraform/`.

## Adopting existing resources

When resources were created by hand or by another tool:

1. Write the resource blocks to match reality.
2. `terraform import` (or `import` blocks) each one.
3. `terraform plan` → repeat editing until it reports **No changes**.
4. Only then make real changes.

An empty state with existing resources is dangerous: `apply` would try to create duplicates or fail midway.

## Provider major upgrades

- Read the provider's upgrade guide; many majors rename resources and change nested blocks into attributes (and vice versa).
- Use the provider's migration tool if one exists, then `moved` blocks or `state mv` for renamed resources.
- Watch for fields that became required or changed defaults (e.g. explicit flags that used to default to a value); state them explicitly.
- Success criterion: `plan` is empty after the migration with no real infrastructure change.

## Cost guardrails first

Before the first paid resource in a new cloud account: create the budget and alert (for example a monthly budget with email notification), and tag everything with owner and purpose. Order matters: guardrails → resources. List resources with their monthly cost regularly and delete unused ones through Terraform.

## Workflow

```bash
terraform fmt -check && terraform validate
terraform plan -out tf.plan
terraform show tf.plan        # read it; look for destroy/replace
terraform apply tf.plan
```

- `-/+` (replace) on a stateful resource (database, storage) needs a human decision.
- Keep applies from a single place at a time; use state locking where the backend supports it.

## Verification loop

1. `fmt`, `validate` clean.
2. `plan` shows exactly the intended changes.
3. After apply, a second `plan` is empty.

## Pitfalls

- **Drift from console edits:** someone changes a setting by hand and the next apply reverts it. Re-run `plan` regularly and fold manual changes back into code.
- **`count` index shifts** recreate resources when a list changes; use `for_each` with stable keys.
- **Sensitive values in state:** state files contain secrets in plain text; protect the backend.
- **Data sources at plan time** can fail if the referenced resource is created in the same apply; use explicit dependencies.
- **Lifecycle `prevent_destroy`** on critical resources turns an accidental destroy into an error.
