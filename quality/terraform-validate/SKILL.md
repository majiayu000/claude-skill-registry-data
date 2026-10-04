---
name: terraform-validate
description: Format and validate Terraform code with the fmt / init / validate / tflint loop. Use after editing any .tf file, before committing Terraform changes, when asked to lint, format, validate, or check Terraform modules and root configurations, or when setting up tflint for a repository.
license: MIT
---

# Terraform validation workflow

Run this loop after editing Terraform and before every commit. Fix findings and repeat until all
three stages are clean — never commit with failures.

## 1. Format

From the repository root:

```sh
terraform fmt -recursive
```

This rewrites files in place. In CI or to check without writing, use
`terraform fmt -recursive -check -diff`.

## 2. Validate

Per changed module or root configuration (validation is per-directory, not monorepo-wide):

```sh
terraform -chdir=<module-dir> init -backend=false   # first run only; downloads providers
terraform -chdir=<module-dir> validate
```

`-backend=false` skips state/backend configuration — validation needs providers, not state.
Validate catches type errors, unknown arguments, and missing required attributes.

## 3. Lint

```sh
tflint --init        # once per clone; downloads rulesets (needs network)
tflint --chdir=<module-dir>
```

If the repository has no `.tflint.hcl`, offer to seed one from this skill's bundled
[tflint.hcl](tflint.hcl) — it enables the recommended Terraform preset plus naming-convention,
documented-variables/outputs, unused-declarations, and required-version/providers rules. Add a
provider-specific ruleset (AWS/Azure/GCP) only if the repository targets that provider; the
bundled config keeps it commented out.

## 4. Repeat

Re-run the loop after fixing findings. The stages are ordered cheapest-first: fmt is instant,
validate needs providers, tflint needs rulesets. A module is done when all three pass.

Notes:

- `terraform validate` spawns provider plugins that communicate over local Unix sockets; in
  sandboxed environments, ensure Unix-socket connections are permitted or run validation outside
  the sandbox.
- tflint enforces several conventions from the `terraform-style` skill mechanically (documented
  variables/outputs, required version/provider constraints, naming) — treat its findings as style
  violations, not suggestions.
