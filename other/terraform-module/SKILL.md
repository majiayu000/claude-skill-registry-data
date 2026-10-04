---
name: terraform-module
description: Scaffold a new Terraform module with the canonical file layout — terraform.tf, main.tf, variables.tf, outputs.tf, README.md — and house style. Use when creating a new Terraform module, adding a module under a modules/ directory, or restructuring an existing module to the standard layout.
license: MIT
---

# Scaffold a Terraform module

Creates a module with the canonical five-file layout. Apply the `terraform-style` skill's
conventions while filling in real content, and finish with the `terraform-validate` workflow.

## 1. Name the module and pick providers

- Directory: kebab-case, named for what the module manages (`modules/ecr-registry`, not
  `modules/registry-stuff`). One cohesive concern per module.
- Decide which providers the module needs and their major-version constraints before writing
  resources — they go in `terraform.tf` on day one.

## 2. Create the five canonical files

Copy the skeletons from this skill's [templates/](templates/) directory into the new module
directory and replace the placeholder content:

| File | Template shows |
| --- | --- |
| `terraform.tf` | `required_version` + `required_providers` with major-version pins |
| `main.tf` | a primary resource named `main`, plus naming-convention reminders |
| `variables.tf` | a required flat variable, an object variable with `optional()` defaults |
| `outputs.tf` | flat primary-attribute outputs and one grouped object output |
| `README.md` | title, purpose paragraph, Usage example, Inputs/Outputs tables |

Every variable and output keeps a `description` — the linter enforces this.

## 3. Apply the house style

While implementing, follow the `terraform-style` skill. The rules that most often shape a new
module's interface:

- `set(string)` for unordered unique inputs; primary resource named `main`;
- `name_prefix` (trailing `-`) for account-unique named resources;
- boolean-gated resources via `for_each = toset(var.x ? ["true"] : [])`;
- outputs named for the attribute, cohesive facets grouped into one object;
- optional strings default to `null`, never `""`.

Split cohesive resource families into domain files (`iam-node.tf`, `signing.tf`) once `main.tf`
grows past a screenful — the five canonical files are the floor, not the ceiling.

## 4. Document and validate

- Fill in the README's Usage example with a realistic call (`module "x" { source = "../..." }`)
  showing only the inputs a typical caller sets.
- Run the `terraform-validate` workflow (fmt → init/validate → tflint) on the new module before
  committing.
