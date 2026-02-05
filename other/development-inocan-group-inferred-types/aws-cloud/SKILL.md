---
name: aws-cloud
description: AWS cloud infrastructure patterns and best practices. Use when designing or implementing AWS solutions including EC2, Lambda, S3, RDS, and infrastructure as code with Terraform or CloudFormation.
---

# AWS Cloud Skill

This skill provides AWS architecture patterns and best practices.

## Core Services

| Service | Use Case |
|---------|----------|
| EC2 | Virtual servers |
| Lambda | Serverless functions |
| S3 | Object storage |
| RDS | Managed databases |
| ECS/EKS | Container orchestration |
| CloudFront | CDN |
| Route 53 | DNS |

## Well-Architected Framework

1. **Operational Excellence** - Automation, monitoring
2. **Security** - IAM, encryption, compliance
3. **Reliability** - Multi-AZ, backups, DR
4. **Performance** - Right-sizing, caching
5. **Cost Optimization** - Reserved instances, spot

## Terraform Patterns

```hcl
# VPC with public/private subnets
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "my-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true
}
```

## Security Best Practices

- Use IAM roles, not access keys
- Enable MFA for root and IAM users
- Encrypt data at rest (KMS)
- Use VPC for network isolation
- Enable CloudTrail for audit
- Use Security Groups as firewalls

## Cost Optimization

- Use Reserved Instances for steady workloads
- Use Spot Instances for flexible workloads
- Right-size instances based on metrics
- Use S3 lifecycle policies
- Enable Cost Explorer alerts
