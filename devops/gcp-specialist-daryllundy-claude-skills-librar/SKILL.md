---
name: gcp-specialist
description: Google Cloud Platform infrastructure, services, and architecture using
  gcloud CLI, Deployment Manager, and Terraform. Use when asked to deploy to GCP,
  set up Compute Engine or Cloud Run or GKE, configure GCP IAM and service accounts,
  write Deployment Manager templates, set up Cloud SQL or Cloud Storage, configure
  Cloud Monitoring, or optimize GCP costs.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: infrastructure-cloud
  tags:
  - gcp
  - google-cloud
  - gke
  - cloud-run
  - bigquery
  - terraform
  - iam
---

# GCP Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `deploy to GCP`, `Google Cloud`, `Cloud Run`.
- The requested work fits this skill's lane: Compute Engine, Cloud Run, GKE, Cloud SQL, Cloud Storage, IAM, Cloud Monitoring.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: AWS or Azure work; Terraform HCL writing (use terraform-specialist).

## First actions
1. `Glob('**/*.tf', '**/deployment-manager/**', '**/cloudbuild.yaml')` — find existing GCP IaC
2. Identify: project ID, region preference, whether Workload Identity is in use for GKE
3. Confirm IaC approach: Terraform (preferred), Deployment Manager, or gcloud CLI scripts

## Decision rules
- For service-to-service auth: always use Workload Identity (GKE) or service account impersonation — never service account key files
- For secrets: use Secret Manager, not environment variables or config files
- If Terraform files exist: use terraform-specialist for provisioning

## Output contract
- Primary artifact: Terraform module, Deployment Manager YAML, or gcloud bash script
- Required: IAM bindings follow least-privilege; service accounts have minimal roles

## Constraints
- NEVER export service account key files for workload authentication
- Scope boundary: Kubernetes manifests belong to kubernetes-specialist

## Reference
- `references/legacy-agent.md`: full GCP service reference, Well-Architected patterns, IAM best practices, cost optimization
