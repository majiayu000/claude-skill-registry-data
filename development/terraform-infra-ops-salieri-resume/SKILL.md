---
name: terraform-infra-ops
description: Operate and update the Terraform infrastructure in ops/infra, including init/apply flows, formatting, and linting. Use when modifying Cloudflare Pages/R2 resources, updating Terraform state config, or running infra operations.
---

# Terraform Infra Ops

## Overview
Apply and maintain the Cloudflare Terraform infrastructure using the repo's documented workflow.

## Workflow
1. Work from `ops/infra` and follow the runbook in `ops/infra/README.md` for first-run vs subsequent runs.
2. Export required backend variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_ENDPOINT_URL_S3`) before running Terraform.
3. Run `terraform fmt` and `tflint` on changes before completion.
