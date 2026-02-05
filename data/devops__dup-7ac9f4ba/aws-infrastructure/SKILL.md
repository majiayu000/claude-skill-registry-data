---
name: aws-infrastructure
description: AWS infrastructure as code with Terraform and CDK, including VPC design, EKS cluster setup, S3 bucket configuration, RDS databases, DynamoDB tables, Lambda functions, API Gateway, CloudWatch monitoring, IAM policies, security groups, cost optimization, multi-account strategies, CI/CD with CodePipeline, infrastructure testing, disaster recovery, compliance automation, and cloud-native best practices for production workloads.
---

# AWS Infrastructure Skill

## Purpose

Build production-grade AWS infrastructure using Infrastructure as Code (Terraform/CDK) following cloud-native best practices, security, and cost optimization.

## When to Use This Skill

Auto-activates when working with:
- Terraform configurations
- AWS CDK applications
- CloudFormation templates
- AWS service configuration
- Infrastructure automation
- Multi-account AWS setups
- Security and compliance
- Cost optimization

## Core Principles

### 1. Infrastructure as Code
- Version control all infrastructure
- Modular, reusable components
- Automated deployment
- State management

### 2. Security by Design
- Least privilege IAM
- Encryption at rest and in transit
- Network segmentation
- Audit logging

### 3. Cost Optimization
- Right-sizing resources
- Auto-scaling
- Reserved instances
- Lifecycle policies

## Quick Start Examples

### Terraform Project Structure

```
infrastructure/
├── terraform/
│   ├── environments/
│   │   ├── dev/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── terraform.tfvars
│   │   ├── staging/
│   │   └── prod/
│   ├── modules/
│   │   ├── vpc/
│   │   ├── eks/
│   │   ├── rds/
│   │   └── s3-data-lake/
│   └── shared/
│       └── backend.tf
```

### VPC Module (Terraform)

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(var.tags, {
    Name = "${var.environment}-vpc"
  })
}

# Public subnets
resource "aws_subnet" "public" {
  count                   = length(var.public_subnet_cidrs)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = merge(var.tags, {
    Name = "${var.environment}-public-subnet-${count.index + 1}"
    "kubernetes.io/role/elb" = "1"  # For EKS
  })
}

# Private subnets
resource "aws_subnet" "private" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = merge(var.tags, {
    Name = "${var.environment}-private-subnet-${count.index + 1}"
    "kubernetes.io/role/internal-elb" = "1"  # For EKS
  })
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = merge(var.tags, {
    Name = "${var.environment}-igw"
  })
}

# NAT Gateway
resource "aws_eip" "nat" {
  count  = var.enable_nat_gateway ? length(var.public_subnet_cidrs) : 0
  domain = "vpc"

  tags = merge(var.tags, {
    Name = "${var.environment}-nat-eip-${count.index + 1}"
  })
}

resource "aws_nat_gateway" "main" {
  count         = var.enable_nat_gateway ? length(var.public_subnet_cidrs) : 0
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = merge(var.tags, {
    Name = "${var.environment}-nat-${count.index + 1}"
  })
}

# Route tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = merge(var.tags, {
    Name = "${var.environment}-public-rt"
  })
}

resource "aws_route_table" "private" {
  count  = length(var.private_subnet_cidrs)
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[count.index].id
  }

  tags = merge(var.tags, {
    Name = "${var.environment}-private-rt-${count.index + 1}"
  })
}
```

### EKS Cluster (Terraform)

```hcl
# modules/eks/main.tf
resource "aws_eks_cluster" "main" {
  name     = "${var.environment}-eks-cluster"
  role_arn = aws_iam_role.eks_cluster.arn
  version  = var.kubernetes_version

  vpc_config {
    subnet_ids              = var.subnet_ids
    endpoint_private_access = true
    endpoint_public_access  = true
    public_access_cidrs     = var.cluster_endpoint_public_access_cidrs

    security_group_ids = [aws_security_group.eks_cluster.id]
  }

  encryption_config {
    provider {
      key_arn = aws_kms_key.eks.arn
    }
    resources = ["secrets"]
  }

  enabled_cluster_log_types = ["api", "audit", "authenticator", "controllerManager", "scheduler"]

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy,
    aws_cloudwatch_log_group.eks,
  ]

  tags = var.tags
}

# Node group
resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "${var.environment}-node-group"
  node_role_arn   = aws_iam_role.eks_nodes.arn
  subnet_ids      = var.private_subnet_ids

  scaling_config {
    desired_size = var.desired_size
    max_size     = var.max_size
    min_size     = var.min_size
  }

  instance_types = var.instance_types
  capacity_type  = var.capacity_type  # ON_DEMAND or SPOT

  update_config {
    max_unavailable_percentage = 33
  }

  labels = {
    Environment = var.environment
    ManagedBy   = "terraform"
  }

  tags = var.tags

  depends_on = [
    aws_iam_role_policy_attachment.eks_worker_node_policy,
    aws_iam_role_policy_attachment.eks_cni_policy,
    aws_iam_role_policy_attachment.eks_container_registry_policy,
  ]
}
```

### S3 Data Lake Bucket (Terraform)

```hcl
# modules/s3-data-lake/main.tf
resource "aws_s3_bucket" "data_lake" {
  bucket = "${var.environment}-data-lake-${var.bucket_suffix}"

  tags = merge(var.tags, {
    Name        = "${var.environment}-data-lake"
    Purpose     = "Data Lake Storage"
    Environment = var.environment
  })
}

# Versioning
resource "aws_s3_bucket_versioning" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.data_lake.arn
    }
    bucket_key_enabled = true
  }
}

# Lifecycle policy
resource "aws_s3_bucket_lifecycle_configuration" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  rule {
    id     = "archive-old-data"
    status = "Enabled"

    transition {
      days          = 90
      storage_class = "INTELLIGENT_TIERING"
    }

    transition {
      days          = 180
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }

    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }

  rule {
    id     = "delete-temp-data"
    status = "Enabled"

    filter {
      prefix = "temp/"
    }

    expiration {
      days = 7
    }
  }
}

# Block public access
resource "aws_s3_bucket_public_access_block" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Bucket policy
resource "aws_s3_bucket_policy" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "DenyInsecureTransport"
        Effect = "Deny"
        Principal = "*"
        Action = "s3:*"
        Resource = [
          aws_s3_bucket.data_lake.arn,
          "${aws_s3_bucket.data_lake.arn}/*"
        ]
        Condition = {
          Bool = {
            "aws:SecureTransport" = "false"
          }
        }
      }
    ]
  })
}
```

### RDS Database (Terraform)

```hcl
# modules/rds/main.tf
resource "aws_db_instance" "main" {
  identifier = "${var.environment}-${var.db_name}"

  engine               = "postgres"
  engine_version       = "15.4"
  instance_class       = var.instance_class
  allocated_storage    = var.allocated_storage
  storage_type         = "gp3"
  storage_encrypted    = true
  kms_key_id           = aws_kms_key.rds.arn

  db_name  = var.db_name
  username = var.master_username
  password = random_password.master.result

  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  backup_retention_period = var.backup_retention_period
  backup_window           = "03:00-04:00"
  maintenance_window      = "mon:04:00-mon:05:00"

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
  performance_insights_enabled    = true
  performance_insights_retention_period = 7

  deletion_protection = var.environment == "prod" ? true : false
  skip_final_snapshot = var.environment == "prod" ? false : true
  final_snapshot_identifier = "${var.environment}-${var.db_name}-final-snapshot"

  tags = var.tags
}
```

## Resource Files

### [resources/terraform-best-practices.md](resources/terraform-best-practices.md)
- Module design
- State management
- Variable patterns
- Testing strategies

### [resources/aws-cdk-patterns.md](resources/aws-cdk-patterns.md)
- CDK constructs
- TypeScript patterns
- Testing CDK apps
- Custom constructs

### [resources/security-compliance.md](resources/security-compliance.md)
- IAM least privilege
- Encryption strategies
- Network security
- Compliance automation

### [resources/cost-optimization.md](resources/cost-optimization.md)
- Right-sizing
- Spot instances
- Reserved capacity
- Cost monitoring

### [resources/multi-account-strategy.md](resources/multi-account-strategy.md)
- AWS Organizations
- Account structure
- Cross-account access
- Centralized logging

## Best Practices

- Use remote state with locking (S3 + DynamoDB)
- Implement modules for reusability
- Tag all resources consistently
- Enable encryption by default
- Use IAM roles over access keys
- Implement least privilege access
- Enable CloudTrail and Config
- Use VPC endpoints for AWS services
- Implement backup and disaster recovery
- Monitor costs with budgets and alerts
- Use infrastructure testing (Terratest)
- Implement CI/CD for infrastructure
- Document architecture decisions

## Common Patterns

### Multi-Environment Setup
```hcl
# environments/prod/main.tf
module "vpc" {
  source = "../../modules/vpc"

  environment = "prod"
  vpc_cidr    = "10.0.0.0/16"

  public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnet_cidrs = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]

  tags = local.common_tags
}
```

### Remote State
```hcl
terraform {
  backend "s3" {
    bucket         = "terraform-state-bucket"
    key            = "prod/vpc/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

---

**Status**: Production-Ready
**Last Updated**: 2025-11-04
**Focus**: Security, scalability, cost optimization
