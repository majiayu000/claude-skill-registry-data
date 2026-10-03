---
name: infrastructure-as-code
description: Manage infrastructure using Terraform, CloudFormation, or Pulumi. Version control infrastructure, automate provisioning, and ensure consistency.
triggers:
- /iac
- /terraform
- /infrastructure
---

# Infrastructure as Code

This skill covers managing infrastructure using code with tools like Terraform, AWS CloudFormation, Azure Bicep, and Pulumi for consistent, version-controlled infrastructure.

## When to use this skill

Use this skill when you need to:
- Provision cloud infrastructure automatically
- Manage infrastructure versioning
- Ensure environment consistency
- Implement disaster recovery
- Scale infrastructure efficiently

## Prerequisites

- Cloud provider account (AWS, Azure, GCP)
- IaC tool installed (Terraform, Pulumi)
- Understanding of target architecture
- Access credentials (service principals, IAM roles)

## Guidelines

### Terraform Workflow

**Project Structure**
```
terraform/
├── modules/
│   ├── vpc/
│   ├── compute/
│   └── database/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── prod/
├── variables.tf
├── outputs.tf
├── main.tf
└── backend.tf
```

**Basic Configuration**
```hcl
# main.tf
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "infrastructure/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

module "vpc" {
  source = "./modules/vpc"
  
  vpc_cidr     = var.vpc_cidr
  environment  = var.environment
  azs          = var.availability_zones
}
```

**Variable Definitions**
```hcl
# variables.tf
variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}
```

### Terraform Best Practices

**State Management**
- Use remote state (S3, Azure Storage, GCS)
- Enable state locking (DynamoDB, Cosmos DB)
- Separate state per environment
- Use state workspaces or separate directories

**Module Design**
- Create reusable modules
- Version modules explicitly
- Document inputs and outputs
- Use composition over inheritance

**Security**
- Never commit state files
- Mark sensitive outputs
- Use least privilege credentials
- Scan with Checkov/TFSec

### CloudFormation (AWS)

**Template Structure**
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Web Application Infrastructure'

Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - prod

Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-vpc'

Outputs:
  VPCId:
    Description: VPC ID
    Value: !Ref VPC
    Export:
      Name: !Sub '${Environment}-vpc-id'
```

### Bicep (Azure)

**Template Example**
```bicep
// main.bicep
param environment string
param location string = resourceGroup().location

var resourcePrefix = '${environment}-app'

module vnet 'modules/vnet.bicep' = {
  name: 'vnetDeployment'
  params: {
    vnetName: '${resourcePrefix}-vnet'
    location: location
    addressPrefix: '10.0.0.0/16'
  }
}

module appService 'modules/app-service.bicep' = {
  name: 'appServiceDeployment'
  params: {
    appName: '${resourcePrefix}-api'
    location: location
    subnetId: vnet.outputs.subnetId
  }
}

output appServiceUrl string = appService.outputs.url
```

### CI/CD Integration

**Terraform in CI/CD**
```yaml
# .github/workflows/terraform.yml
name: Terraform

on:
  push:
    paths:
      - 'terraform/**'
  pull_request:
    paths:
      - 'terraform/**'

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: "1.6.0"
      
      - name: Terraform Format Check
        run: terraform fmt -check -recursive
      
      - name: Terraform Init
        run: terraform init
      
      - name: Terraform Validate
        run: terraform validate
      
      - name: Terraform Plan
        run: terraform plan -out=tfplan
      
      - name: Terraform Apply
        if: github.ref == 'refs/heads/main'
        run: terraform apply -auto-approve tfplan
```

### Best Practices

**Environment Management**
- Use separate directories for environments
- Or use Terraform workspaces
- Share modules across environments
- Environment-specific variables

**Testing**
- Use terraform plan in PR checks
- Implement policy as code (OPA, Sentinel)
- Run security scanning (Checkov)
- Test modules with Terratest

**Documentation**
- Auto-generate docs (terraform-docs)
- Document design decisions
- Maintain architecture diagrams
- Keep README files updated

## Examples

See the `examples/` directory for:
- `terraform-aws/` - AWS infrastructure with Terraform
- `bicep-azure/` - Azure infrastructure with Bicep
- `cloudformation/` - AWS CloudFormation templates
- `modules/` - Reusable Terraform modules

## References

- [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
- [AWS CloudFormation](https://docs.aws.amazon.com/cloudformation/)
- [Azure Bicep](https://docs.microsoft.com/azure/azure-resource-manager/bicep/)
- [Pulumi documentation](https://www.pulumi.com/docs/)
- [Terraform best practices](https://www.terraform-best-practices.com/)
