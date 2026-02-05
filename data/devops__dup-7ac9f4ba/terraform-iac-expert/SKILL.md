---
name: Terraform IaC Expert
description: Infrastructure as Code for AI workloads using Terraform across AWS, Azure, GCP, and OCI
version: 1.0.0
resources: resources/modules.tf
triggers:
  - terraform
  - infrastructure as code
  - IaC
  - provisioning
---

# Terraform IaC Expert

Expert in Terraform and Infrastructure as Code for deploying AI infrastructure across multi-cloud environments.

## Project Structure

```
infrastructure/
├── modules/
│   ├── aws-bedrock/
│   ├── azure-openai/
│   ├── oci-genai/
│   └── vector-store/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── prod/
├── shared/
│   ├── networking/
│   └── security/
└── scripts/
```

## Module Overview

| Module | Provider | Purpose |
|--------|----------|---------|
| `aws-bedrock` | AWS | Bedrock, Knowledge Bases, VPC Endpoints |
| `azure-openai` | Azure | Azure OpenAI, AI Search, Private Endpoints |
| `oci-genai` | OCI | DACs, Endpoints, Agents, Knowledge Bases |
| `vector-store` | Multi | OpenSearch Serverless, Qdrant, Milvus |

**Full module code:** `resources/modules.tf`

## AWS AI Infrastructure

### Bedrock Module
```hcl
module "aws_ai" {
  source = "./modules/aws-bedrock"

  prefix             = "prod"
  region             = "us-east-1"
  vpc_id             = data.aws_vpc.main.id
  private_subnet_ids = data.aws_subnets.private.ids

  enable_private_endpoint = true
  create_knowledge_base   = true
}
```

### Key Resources
- IAM roles for Bedrock access
- VPC endpoints for private connectivity
- Knowledge bases with OpenSearch

## Azure AI Infrastructure

### Azure OpenAI Module
```hcl
module "azure_ai" {
  source = "./modules/azure-openai"

  openai_name         = "prod-openai"
  location            = "eastus"
  resource_group_name = azurerm_resource_group.ai.name

  gpt4o_capacity      = 100  # TPM
  embedding_capacity  = 50

  enable_private_endpoint = true
}
```

### Key Resources
- Cognitive Account (OpenAI kind)
- Model deployments (GPT-4o, embeddings)
- Private endpoints
- Azure AI Search

## OCI AI Infrastructure

### GenAI Module
```hcl
module "oci_ai" {
  source = "./modules/oci-genai"

  prefix         = "prod"
  compartment_id = var.oci_compartment_id
  cluster_type   = "HOSTING"
  unit_count     = 10
  unit_shape     = "LARGE_COHERE"

  create_agent          = true
  create_knowledge_base = true
}
```

### Key Resources
- Dedicated AI Clusters (DAC)
- Model endpoints
- GenAI Agents
- Knowledge bases

## Vector Store Infrastructure

### OpenSearch Serverless (AWS)
```hcl
module "vectors" {
  source = "./modules/vector-store/aws-opensearch"

  prefix           = "prod"
  vpc_endpoint_ids = [aws_vpc_endpoint.opensearch.id]
  allowed_principals = [aws_iam_role.bedrock.arn]
}
```

## Multi-Cloud Environment

```hcl
# environments/prod/main.tf

terraform {
  backend "s3" {
    bucket = "terraform-state-ai-infra"
    key    = "prod/terraform.tfstate"
    encrypt = true
  }
}

provider "aws" { region = var.aws_region }
provider "azurerm" { features {} }
provider "oci" { ... }

# Deploy to all clouds
module "aws_ai" { source = "../../modules/aws-bedrock" ... }
module "azure_ai" { source = "../../modules/azure-openai" ... }
module "oci_ai" { source = "../../modules/oci-genai" ... }
```

## Best Practices

### State Management
- Remote state (S3, Azure Blob, OCI Object Storage)
- State locking (DynamoDB, Cosmos DB)
- Encrypt state at rest
- Separate state per environment

### Variable Validation
```hcl
variable "environment" {
  type = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}
```

### Sensitive Data
- Use `sensitive = true` for outputs
- Reference secrets from secret managers
- Never commit `.tfvars` with secrets

### Tagging
```hcl
default_tags {
  tags = {
    Environment = var.environment
    Project     = "ai-platform"
    ManagedBy   = "terraform"
  }
}
```

## CI/CD Integration

### GitHub Actions
```yaml
- uses: hashicorp/setup-terraform@v3
- run: terraform init
- run: terraform plan -out=tfplan
- run: terraform apply -auto-approve tfplan
  if: github.ref == 'refs/heads/main'
```

### Key Patterns
- Plan on PR, apply on merge
- Use workspaces or directories for environments
- Lock state during apply
- Store plan artifacts

## Managed Kubernetes GPU

### EKS GPU Nodes
```hcl
eks_managed_node_groups = {
  gpu = {
    instance_types = ["g5.2xlarge"]
    ami_type = "AL2_x86_64_GPU"
    taints = [{ key = "nvidia.com/gpu" ... }]
  }
}
```

### AKS GPU Nodes
```hcl
resource "azurerm_kubernetes_cluster_node_pool" "gpu" {
  vm_size = "Standard_NC24ads_A100_v4"
  node_taints = ["nvidia.com/gpu=true:NoSchedule"]
}
```

### OKE GPU Nodes
```hcl
resource "oci_containerengine_node_pool" "gpu" {
  node_shape = "BM.GPU.A100-v2.8"
}
```

**Full examples:** `resources/modules.tf`

## Resources

- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest)
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest)
- [Terraform OCI Provider](https://registry.terraform.io/providers/oracle/oci/latest)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)

---

*Infrastructure as Code for enterprise AI deployments.*
