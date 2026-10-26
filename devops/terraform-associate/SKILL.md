---
name: terraform-associate
description: Use when preparing for HashiCorp Certified Terraform Associate (004) — the objective areas (IaC concepts, providers and state, the core workflow, configuration language, modules, state management, maintaining infrastructure, HCP Terraform), practising by running real Terraform commands locally, and verifying answers against Terraform documentation. Also use when writing or checking Terraform practice questions, especially ones about command behaviour.
---

# HashiCorp Certified: Terraform Associate (004)

Bottom line: **run the commands instead of memorising them**. Most questions are about what Terraform does in a situation (what `plan` shows, what `init` changes, what happens to state), and a local sandbox with a provider that needs no cloud account answers them reliably.

## Exam shape (confirm on the official page)

- Online proctored, about one hour, in English; multiple-choice style questions. The credential is valid for a limited period (renew by re-taking).
- Objective areas: (1) Infrastructure as Code with Terraform, (2) Terraform fundamentals — providers and state, (3) core workflow — `init`, `validate`, `plan`, `apply`, `destroy`, `fmt`, (4) configuration — resources vs data sources, references, variables and outputs, complex types, expressions and functions, dependencies, custom conditions, sensitive data, (5) modules — sources, variable scope, versions, (6) state management — local backend, locking, remote backends, drift, (7) maintaining infrastructure — import, state inspection, verbose logging, (8) HCP Terraform — workspaces, projects, collaboration and governance.

Primary sources: HashiCorp certification pages (https://developer.hashicorp.com/certifications/infrastructure-automation), the official review guide that maps each objective to documentation, the sample questions, and the Terraform documentation (https://developer.hashicorp.com/terraform).

## Sandbox for verification

Use providers that need no credentials — `hashicorp/random`, `hashicorp/local`, `hashicorp/null`, `terraform_data` — and a local backend:

```bash
mkdir lab && cd lab
cat > main.tf <<'HCL'
terraform { required_providers { random = { source = "hashicorp/random", version = "~> 3.6" } } }
resource "random_pet" "name" { length = 2 }
output "name" { value = random_pet.name.id }
HCL
terraform init && terraform plan && terraform apply -auto-approve
terraform state list && terraform state show random_pet.name
```

Then test each objective: change `length` and read the plan symbol (`-/+` replace), add `lifecycle { prevent_destroy = true }` and try `destroy`, move a resource with a `moved` block, import with an `import` block, run `terraform plan -refresh-only`, set `TF_LOG=DEBUG`.

## Concepts that decide many questions

- **State** maps configuration to real objects; `terraform.tfstate` can contain secrets; remote backends add locking and sharing.
- **`.terraform.lock.hcl`** pins provider versions; `terraform init -upgrade` changes it.
- **Data sources** read, resources manage.
- **Implicit dependencies** come from references; `depends_on` only for hidden ones.
- **`count` vs `for_each`**: index-based addresses shift; key-based addresses are stable.
- **Module variables** are scoped to the module; outputs are the only way out.
- **Sensitive values** are redacted in output but still stored in state.
- **HCP Terraform** workspaces hold state and variables; runs can be VCS-driven, CLI-driven or API-driven; policies (Sentinel/OPA) gate runs.

## Writing practice questions

- Verify each command-behaviour claim by running it in the sandbox with a pinned Terraform version, and record the version.
- Quote terms exactly as the documentation uses them.
- Vary scenarios; avoid templated distractors.

## Pitfalls

- Confusing `terraform refresh` (deprecated alias) with `plan -refresh-only`.
- Thinking `terraform fmt` validates configuration (it only formats).
- Assuming `destroy` removes resources not in state.
- Mixing up workspace concepts in the CLI and in HCP Terraform.
- Studying from material for an older exam version; check which objectives were added or removed.

## Self-check

- Answer the official sample questions with reasons for every option.
- For each objective, show it working in the sandbox in under five minutes.
- Explain what happens to state in import, move, taint/replace and refresh-only runs.
