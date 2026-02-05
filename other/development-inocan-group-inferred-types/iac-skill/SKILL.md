---
name: iac-skill
description: Infrastructure as Code with Terraform, Ansible, and CloudFormation.
sasmp_version: "1.3.0"
bonded_agent: 04-infrastructure-as-code
bond_type: PRIMARY_BOND

parameters:
  - name: tool
    type: string
    required: false
    enum: ["terraform", "ansible", "cloudformation", "pulumi"]
    default: "terraform"
  - name: operation
    type: string
    required: true
    enum: ["plan", "apply", "destroy", "validate", "import"]

retry_config:
  strategy: exponential_backoff
  initial_delay_ms: 1000
  max_retries: 3

observability:
  logging: structured
  metrics: enabled
---

# Infrastructure as Code Skill

## Overview
Master IaC with Terraform, Ansible, and CloudFormation for automated infrastructure.

## Parameters
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| tool | string | No | terraform | IaC tool |
| operation | string | Yes | - | Operation type |

## Core Topics

### MANDATORY
- Terraform HCL syntax and providers
- State management and locking
- Modules and workspaces
- Ansible playbooks and roles
- Inventory management

### OPTIONAL
- CloudFormation templates
- Pulumi and CDK
- Testing IaC (terratest)
- Secret management

### ADVANCED
- Custom providers
- Complex module design
- Multi-cloud strategies
- Drift detection

## Quick Reference

```bash
# Terraform
terraform init
terraform plan -out=plan.tfplan
terraform apply plan.tfplan
terraform destroy
terraform fmt -recursive
terraform validate
terraform state list
terraform import aws_instance.web i-123

# State Management
terraform state mv old new
terraform state rm resource
terraform force-unlock LOCK_ID

# Ansible
ansible-playbook -i inventory playbook.yml
ansible-playbook playbook.yml --check --diff
ansible-playbook playbook.yml --tags nginx
ansible all -m ping -i inventory
ansible-vault encrypt secrets.yml
```

## Troubleshooting

### Common Failures
| Symptom | Root Cause | Solution |
|---------|------------|----------|
| State lock | Concurrent ops | Wait or force-unlock |
| Resource exists | Drift | Import or delete |
| Provider auth | Credentials | Check AWS_PROFILE |
| Cycle error | Dependencies | Restructure |

### Debug Checklist
1. Validate: `terraform validate`
2. Check state: `terraform state list`
3. Debug: `TF_LOG=DEBUG terraform plan`
4. Verify credentials

### Recovery Procedures

#### Corrupted State
1. Restore from S3 versioning
2. Or import: `terraform import` for each resource

## Resources
- [Terraform Docs](https://developer.hashicorp.com/terraform/docs)
- [Ansible Docs](https://docs.ansible.com)
