---
name: infrastructure-as-code
description: Infrastructure as Code with Terraform and AWS CDK. Use when writing Terraform configurations (HCL), provisioning cloud resources (VPC, subnets, EC2, ECS, RDS, S3), setting up AWS CDK stacks in TypeScript, managing multi-environment infrastructure (dev/staging/prod), or automating cloud provisioning. Triggers on Terraform, CDK, infrastructure provisioning, cloud setup, IaC, HCL, CloudFormation, or environment management.
---

# Infrastructure as Code - Terraform & AWS CDK

**Purpose**: Automate infrastructure provisioning with code for consistency, version control, and repeatability

**Agent**: Amazon Cloud Architect / Google SRE
**Use When**: Setting up cloud infrastructure, managing environments, or automating deployments

---

## Terraform

### Basic Example

```hcl
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name = "${var.project_name}-vpc"
  }
}

# Subnet
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-public-subnet"
  }
}

# Security Group
resource "aws_security_group" "web" {
  name        = "${var.project_name}-web-sg"
  description = "Allow HTTP/HTTPS inbound traffic"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 Instance
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.web.id]

  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y nginx
              systemctl start nginx
              EOF

  tags = {
    Name = "${var.project_name}-web-server"
  }
}

# Output
output "instance_public_ip" {
  value = aws_instance.web.public_ip
}
```

### Variables

```hcl
# variables.tf
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name prefix"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}
```

### Commands

```bash
# Initialize
terraform init

# Plan (preview changes)
terraform plan

# Apply (create resources)
terraform apply

# Destroy (delete resources)
terraform destroy

# Format code
terraform fmt

# Validate syntax
terraform validate
```

---

## AWS CDK (TypeScript)

### Basic Stack

```typescript
import * as cdk from 'aws-cdk-lib'
import * as ec2 from 'aws-cdk-lib/aws-ec2'
import * as ecs from 'aws-cdk-lib/aws-ecs'
import * as ecs_patterns from 'aws-cdk-lib/aws-ecs-patterns'

export class AppStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props)

    // VPC with public and private subnets
    const vpc = new ec2.Vpc(this, 'AppVpc', {
      maxAzs: 2,
      natGateways: 1
    })

    // ECS Cluster
    const cluster = new ecs.Cluster(this, 'AppCluster', {
      vpc,
      clusterName: 'app-cluster'
    })

    // Fargate Service with ALB
    const service = new ecs_patterns.ApplicationLoadBalancedFargateService(
      this,
      'AppService',
      {
        cluster,
        taskImageOptions: {
          image: ecs.ContainerImage.fromRegistry('nginx'),
          containerPort: 80,
          environment: {
            NODE_ENV: 'production'
          }
        },
        desiredCount: 2,
        publicLoadBalancer: true
      }
    )

    // Auto scaling
    const scaling = service.service.autoScaleTaskCount({
      minCapacity: 2,
      maxCapacity: 10
    })

    scaling.scaleOnCpuUtilization('CpuScaling', {
      targetUtilizationPercent: 70
    })

    // Output
    new cdk.CfnOutput(this, 'LoadBalancerDNS', {
      value: service.loadBalancer.loadBalancerDnsName
    })
  }
}
```

### App Entry Point

```typescript
// bin/app.ts
#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib'
import { AppStack } from '../lib/app-stack'

const app = new cdk.App()

new AppStack(app, 'DevStack', {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: 'us-east-1'
  },
  tags: {
    Environment: 'dev'
  }
})

new AppStack(app, 'ProdStack', {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: 'us-east-1'
  },
  tags: {
    Environment: 'production'
  }
})
```

### Commands

```bash
# Install CDK
npm install -g aws-cdk

# Bootstrap (first time)
cdk bootstrap

# Synthesize CloudFormation
cdk synth

# Deploy
cdk deploy DevStack

# Destroy
cdk destroy DevStack

# Diff
cdk diff DevStack
```

---

## Best Practices

### General
- Version control everything
- Use modules/constructs for reusability
- Separate environments (dev, staging, prod)
- Use remote state (S3 + DynamoDB for Terraform)
- Tag all resources
- Implement least privilege IAM

### Terraform
- Use workspaces for environments
- Lock state file
- Use `terraform plan` before `apply`
- Store sensitive data in AWS Secrets Manager
- Use data sources for existing resources

### CDK
- Use constructs library (L2/L3)
- Test stacks with assertions
- Use aspects for cross-cutting concerns
- Leverage TypeScript type safety

---

**Remember**: IaC makes infrastructure reproducible and auditable. Treat it like application code: version control, review, test.

**Created**: 2026-02-04
**Maintained By**: Amazon Cloud Architect
