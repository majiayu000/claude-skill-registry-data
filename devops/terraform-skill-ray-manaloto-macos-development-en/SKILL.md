---
name: terraform-skill
description: Terraform/OpenTofu quick guide for authoring, testing, and operating infrastructure with safety and drift controls.
---

# Terraform / OpenTofu (Concise)

Use for: writing/reviewing Terraform/Tofu modules, plans, and pipelines.

## Project hygiene
- Pin provider & required_version; set backend (state locking, encryption). Separate root modules per env; minimal locals.
- Tag everything (owner, env, app, costcenter). Use workspaces only when appropriate; prefer directory-per-env.
- Modules: clear inputs/outputs; no hidden provider configs; document expectations.

## Security & safety
- State: remote backend with locking (S3+Dynamo, GCS, etc.), SSE, restricted IAM; rotate access.
- Plan gates: `fmt`, `validate`, `tflint`/`checkov`/`trivy`, `plan` with manual/PR approval; policy-as-code (OPA/Conftest or Sentinel).
- Avoid hard-coded secrets; use SM/Param Store; no plaintext in state if possible (use data sources or external data).

## Testing
- Unit: `terraform validate` + lint.
- Static analysis: tflint, checkov/trivy.
- Integration: `terraform plan` in ephemeral env; Terratest/native `test` for critical modules.

## CI/CD
- Pipeline: fmt → validate → lint → scan → plan (per workspace/env) → approval → apply. Store plans as artifacts; lock applies.
- Drift: scheduled `plan`/`tofu plan`; alert on drift; consider Config for critical resources.

## Operations
- Changes: prefer `-target` only for break-glass. Use `replace` for tainted resources explicitly.
- Imports: `terraform import` plus state file PR; keep sources of truth in code.
- Cleanup: `destroy` only in ephemeral env; guard production with approvals and retention policies.

## References
- HashiCorp/Terraform docs; OpenTofu; AWS/GCP/Azure provider best practices; OTel/OpenLIT for runtime telemetry.
