---
name: terraform-iac
description: "Terraform infrastructure as code, remote state locking, modular design, and drift detection."
---

# Terraform Infrastructure Protocol

1. Use S3/GCS remote backend with DynamoDB/state locking.
2. Separate state files per environment (dev, staging, prod).
3. Run terraform plan in CI and enforce code review before terraform apply.
