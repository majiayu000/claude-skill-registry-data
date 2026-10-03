---
name: aws-cloud
description: Provision and operate AWS infrastructure with Terraform — ECS/Fargate, networking, IAM, security-first production patterns.
when_to_use: Reach for this when the target cloud is AWS (provider "aws", ECS/Lambda/S3 resources). For Azure infra use using-terraform-azure; for Kubernetes orchestration use kubernetes; for Fly.io PaaS use flyio. If you don't know which cloud the project uses, run cloud-provider-detector first. AWS infra/IaC skill.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
paths:
  - "**/*.tf"
  - "**/*.tfvars"
  - "**/cloudformation/**/*.{yml,yaml,json}"
  - "**/serverless.yml"
---

# AWS Cloud Infrastructure Skill

**Quick reference for AWS infrastructure automation with Terraform, security-first design, and production-ready patterns.**

## Core Services Quick Reference

### Compute

**ECS/Fargate** (Managed Containers):
```hcl
resource "aws_ecs_cluster" "app" {
  name = "app-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_task_definition" "app" {
  family                   = "app"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn           = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([{
    name  = "app"
    image = "123456789012.dkr.ecr.us-east-1.amazonaws.com/app:latest"
    portMappings = [{
      containerPort = 8080
      protocol      = "tcp"
    }]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = "/ecs/app"
        "awslogs-region"        = "us-east-1"
        "awslogs-stream-prefix" = "app"
      }
    }
  }])
}
```

**EKS** (Managed Kubernetes):
```hcl
resource "aws_eks_cluster" "main" {
  name     = "production-cluster"
  role_arn = aws_iam_role.eks_cluster.arn
  version  = "1.28"

  vpc_config {
    subnet_ids              = aws_subnet.private[*].id
    endpoint_private_access = true
    endpoint_public_access  = false
    security_group_ids      = [aws_security_group.eks_cluster.id]
  }

  encryption_config {
    provider {
      key_arn = aws_kms_key.eks.arn
    }
    resources = ["secrets"]
  }
}

resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "main-node-group"
  node_role_arn   = aws_iam_role.eks_nodes.arn
  subnet_ids      = aws_subnet.private[*].id

  scaling_config {
    desired_size = 3
    max_size     = 10
    min_size     = 2
  }

  instance_types = ["t3.large"]

  labels = {
    Environment = "production"
  }
}
```

**Lambda** (Serverless Functions):
```hcl
resource "aws_lambda_function" "api" {
  filename         = "lambda.zip"
  function_name    = "api-handler"
  role            = aws_iam_role.lambda_execution.arn
  handler         = "index.handler"
  runtime         = "nodejs18.x"
  timeout         = 30
  memory_size     = 512

  environment {
    variables = {
      DB_HOST = aws_db_instance.main.endpoint
      BUCKET  = aws_s3_bucket.data.id
    }
  }

  vpc_config {
    subnet_ids         = aws_subnet.private[*].id
    security_group_ids = [aws_security_group.lambda.id]
  }
}
```

### Storage

**S3** (Object Storage):
```hcl
resource "aws_s3_bucket" "data" {
  bucket = "company-data-bucket"
}

resource "aws_s3_bucket_versioning" "data" {
  bucket = aws_s3_bucket.data.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "data" {
  bucket                  = aws_s3_bucket.data.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

**RDS** (Managed Databases):
```hcl
resource "aws_db_instance" "postgres" {
  identifier              = "app-postgres"
  engine                  = "postgres"
  engine_version          = "15.4"
  instance_class          = "db.t3.medium"
  allocated_storage       = 100
  storage_type            = "gp3"
  storage_encrypted       = true
  kms_key_id             = aws_kms_key.rds.arn

  db_name  = "app"
  username = "admin"
  password = random_password.db_password.result

  multi_az               = true
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "mon:04:00-mon:05:00"

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  deletion_protection = true
  skip_final_snapshot = false
  final_snapshot_identifier = "app-postgres-final-snapshot"
}
```

### Networking

**VPC** (Virtual Private Cloud):
```hcl
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "production-vpc"
  }
}

resource "aws_subnet" "public" {
  count             = 3
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-${count.index + 1}"
    Type = "public"
  }
}

resource "aws_subnet" "private" {
  count             = 3
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 10}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "private-subnet-${count.index + 1}"
    Type = "private"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
}

resource "aws_nat_gateway" "main" {
  count         = 3
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id
}
```

**Security Groups**:
```hcl
resource "aws_security_group" "alb" {
  name        = "alb-security-group"
  vpc_id      = aws_vpc.main.id
  description = "Security group for Application Load Balancer"

  ingress {
    description = "HTTPS from internet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "app" {
  name        = "app-security-group"
  vpc_id      = aws_vpc.main.id
  description = "Security group for application containers"

  ingress {
    description     = "HTTP from ALB"
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### CDN & DNS

**CloudFront** (CDN):
```hcl
resource "aws_cloudfront_distribution" "cdn" {
  enabled             = true
  is_ipv6_enabled     = true
  http_version        = "http2and3"
  price_class         = "PriceClass_100"

  origin {
    domain_name = aws_s3_bucket.static.bucket_regional_domain_name
    origin_id   = "S3-static-content"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.main.cloudfront_access_identity_path
    }
  }

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD", "OPTIONS"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "S3-static-content"
    viewer_protocol_policy = "redirect-to-https"
    compress              = true

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    min_ttl     = 0
    default_ttl = 3600
    max_ttl     = 86400
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate.main.arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }
}
```

**Route53** (DNS):
```hcl
resource "aws_route53_zone" "main" {
  name = "example.com"
}

resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "www.example.com"
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.cdn.domain_name
    zone_id                = aws_cloudfront_distribution.cdn.hosted_zone_id
    evaluate_target_health = false
  }
}
```

## Security Best Practices

### IAM Roles & Policies

**Least Privilege Principle**:
```hcl
resource "aws_iam_role" "ecs_task" {
  name = "ecs-task-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "ecs_task_s3" {
  name = "ecs-task-s3-access"
  role = aws_iam_role.ecs_task.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "s3:GetObject",
        "s3:PutObject"
      ]
      Resource = [
        "${aws_s3_bucket.data.arn}/*"
      ]
    }]
  })
}
```

### Encryption

**KMS Keys**:
```hcl
resource "aws_kms_key" "main" {
  description             = "Main encryption key"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid    = "Enable IAM User Permissions"
      Effect = "Allow"
      Principal = {
        AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
      }
      Action   = "kms:*"
      Resource = "*"
    }]
  })
}

resource "aws_kms_alias" "main" {
  name          = "alias/main-key"
  target_key_id = aws_kms_key.main.key_id
}
```

## Common Patterns

### High Availability Architecture
- Multi-AZ deployment (minimum 3 availability zones)
- Auto Scaling Groups with target tracking
- Application Load Balancer with health checks
- RDS Multi-AZ with automated backups
- S3 cross-region replication for critical data

### Cost Optimization
- Reserved Instances for predictable workloads
- Spot Instances for fault-tolerant workloads
- S3 Intelligent-Tiering for automatic cost savings
- CloudWatch alarms for budget monitoring
- Rightsizing recommendations via AWS Compute Optimizer

### Disaster Recovery
- Automated RDS snapshots with 7-30 day retention
- S3 versioning and lifecycle policies
- Cross-region backup strategy
- Infrastructure as Code (Terraform) for rapid rebuild
- Regular disaster recovery drills

## Terraform Best Practices

### State Management
```hcl
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

### Variable Management
```hcl
variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be dev, staging, or production."
  }
}

variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to access resources"
  type        = list(string)
  sensitive   = true
}
```

### Module Organization
```
infrastructure/
├── modules/
│   ├── networking/
│   ├── compute/
│   ├── database/
│   └── security/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── production/
└── terraform.tfvars.example
```

## Quick Decision Guide

**When to use ECS vs EKS vs Lambda?**
- **ECS/Fargate**: Dockerized apps, moderate complexity, AWS-native
- **EKS**: Kubernetes expertise, multi-cloud portability, complex orchestration
- **Lambda**: Event-driven, short-lived functions, serverless

**Database Selection**:
- **RDS PostgreSQL**: Relational data, ACID compliance, complex queries
- **Aurora**: High availability, read replicas, MySQL/PostgreSQL compatible
- **DynamoDB**: NoSQL, millisecond latency, infinite scale

**Storage Selection**:
- **S3**: Object storage, static assets, backups, archives
- **EFS**: Shared file system for containers/EC2
- **EBS**: Block storage for EC2 instances

## File Size

- **SKILL.md**: ~25KB (this quick reference)
- **REFERENCE.md**: ~200KB (comprehensive guide with examples)
- **Total**: ~225KB for complete AWS infrastructure knowledge

## Version

- **Version**: 1.0.0
- **Last Updated**: October 2025
- **Maintainer**: Fortium Infrastructure Team
- **Terraform Compatibility**: ≥1.5.0
- **AWS Provider**: ≥5.0.0
