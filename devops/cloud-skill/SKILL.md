---
name: cloud-skill
description: Cloud infrastructure with AWS, Azure, GCP - architecture, services, security, and cost optimization.
sasmp_version: "1.3.0"
bonded_agent: 07-cloud-infrastructure
bond_type: PRIMARY_BOND

parameters:
  - name: provider
    type: string
    required: false
    enum: ["aws", "azure", "gcp", "multi-cloud"]
    default: "aws"
  - name: service
    type: string
    required: false
    enum: ["compute", "storage", "database", "networking", "serverless"]
    default: "compute"

retry_config:
  strategy: exponential_backoff
  initial_delay_ms: 1000
  max_retries: 3

observability:
  logging: structured
  metrics: enabled
---

# Cloud Infrastructure Skill

## Overview
Master cloud platforms: AWS, Azure, and GCP.

## Parameters
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| provider | string | No | aws | Cloud provider |
| service | string | No | compute | Service type |

## Core Topics

### MANDATORY
- AWS: EC2, S3, RDS, Lambda, VPC
- Azure: VMs, Storage, AKS
- GCP: Compute Engine, GKE
- IAM and security
- Networking (VPCs, subnets)

### OPTIONAL
- Cost optimization
- Multi-cloud strategies
- Managed Kubernetes
- Serverless patterns

### ADVANCED
- Well-Architected Framework
- Landing zones
- Organizations/Control Tower
- FinOps

## Service Comparison
| Category | AWS | Azure | GCP |
|----------|-----|-------|-----|
| Compute | EC2 | VMs | Compute Engine |
| K8s | EKS | AKS | GKE |
| Serverless | Lambda | Functions | Cloud Functions |
| Storage | S3 | Blob | Cloud Storage |

## Quick Reference

```bash
# AWS CLI
aws sts get-caller-identity
aws ec2 describe-instances
aws s3 ls s3://bucket-name
aws eks update-kubeconfig --name cluster

# Azure CLI
az login
az account list
az vm list
az aks get-credentials --name cluster

# GCP CLI
gcloud auth login
gcloud projects list
gcloud compute instances list
gcloud container clusters get-credentials cluster
```

## Troubleshooting

### Common Failures
| Symptom | Root Cause | Solution |
|---------|------------|----------|
| Access Denied | IAM policy | Check policies |
| Quota Exceeded | Service limit | Request increase |
| Timeout | Network/SG | Check VPC, SGs |
| Cost spike | Runaway resources | Cost Explorer |

### Debug Checklist
1. Identity: `aws sts get-caller-identity`
2. Region: `echo $AWS_REGION`
3. Permissions: Check IAM
4. CloudTrail: Audit logs

### Recovery Procedures

#### Compromised Key
1. Disable key immediately
2. Review CloudTrail
3. Rotate credentials

## Resources
- [AWS Docs](https://docs.aws.amazon.com)
- [Azure Docs](https://docs.microsoft.com/azure)
- [GCP Docs](https://cloud.google.com/docs)
