---
name: cloud-architect
description: Multi-cloud architecture expertise for AWS, Azure, and GCP. Use when designing cloud infrastructure, implementing Well-Architected Framework principles.
---

# Cloud Architect

Specialized expertise in cloud architecture across AWS, Azure, and GCP, providing guidance on Well-Architected Framework principles, high availability patterns, security best practices, cost optimization, and cloud-native design.

## When to Use This Skill

Use this skill for:

- Designing cloud infrastructure architecture
- Implementing Well-Architected Framework reviews
- Multi-region and multi-cloud deployments
- High availability and disaster recovery planning
- Cloud cost optimization and FinOps
- Serverless architecture design
- Cloud security and compliance
- Migration from on-premises to cloud

**Trigger phrases**: "cloud architecture", "AWS", "Azure", "GCP", "serverless", "cloud migration", "well-architected", "high availability", "disaster recovery", "cloud security"

## What This Skill Does

Provides production-ready cloud patterns including:

- **Architecture Design**: Scalable, resilient, secure cloud solutions
- **Well-Architected**: Six pillars implementation guidance
- **High Availability**: Multi-AZ, multi-region, failover patterns
- **Security**: Identity, encryption, network security
- **Cost Optimization**: Right-sizing, reserved capacity, FinOps
- **Serverless**: Event-driven, managed services patterns

## Instructions

### Step 1: Apply Well-Architected Framework Principles

**Six Pillars Overview**:

| Pillar | Focus Areas |
|--------|-------------|
| **Operational Excellence** | Automation, observability, incident response |
| **Security** | Identity, encryption, compliance, incident response |
| **Reliability** | Fault tolerance, recovery, change management |
| **Performance Efficiency** | Right-sizing, caching, global distribution |
| **Cost Optimization** | Right-sizing, reserved capacity, waste elimination |
| **Sustainability** | Resource efficiency, carbon footprint reduction |

### Step 2: Design for High Availability

**Multi-AZ Architecture (Standard)**:

```
                    ┌─────────────────────────────────────────┐
                    │              Route 53 / DNS              │
                    └─────────────────┬───────────────────────┘
                                      │
                    ┌─────────────────▼───────────────────────┐
                    │           Application Load Balancer      │
                    │              (Cross-AZ)                  │
                    └─────────────────┬───────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
┌─────────▼─────────┐     ┌──────────▼──────────┐    ┌──────────▼──────────┐
│   Availability    │     │   Availability      │    │   Availability      │
│     Zone A        │     │     Zone B          │    │     Zone C          │
│                   │     │                     │    │                     │
│  ┌─────────────┐  │     │  ┌─────────────┐    │    │  ┌─────────────┐    │
│  │  App Tier   │  │     │  │  App Tier   │    │    │  │  App Tier   │    │
│  │  (ASG)      │  │     │  │  (ASG)      │    │    │  │  (ASG)      │    │
│  └──────┬──────┘  │     │  └──────┬──────┘    │    │  └──────┬──────┘    │
│         │         │     │         │           │    │         │           │
│  ┌──────▼──────┐  │     │  ┌──────▼──────┐    │    │  ┌──────▼──────┐    │
│  │  RDS Replica│  │     │  │  RDS Primary│    │    │  │  RDS Replica│    │
│  └─────────────┘  │     │  └─────────────┘    │    │  └─────────────┘    │
└───────────────────┘     └─────────────────────┘    └─────────────────────┘
```

**Multi-Region Architecture (Mission Critical)**:

```
                              Global DNS (Route 53)
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
            ┌───────▼───────┐                   ┌───────▼───────┐
            │  US-EAST-1    │                   │  EU-WEST-1    │
            │  (Primary)    │◄─────────────────►│  (Secondary)  │
            │               │   Cross-Region    │               │
            │  ┌─────────┐  │    Replication    │  ┌─────────┐  │
            │  │   ALB   │  │                   │  │   ALB   │  │
            │  └────┬────┘  │                   │  └────┬────┘  │
            │       │       │                   │       │       │
            │  ┌────▼────┐  │                   │  ┌────▼────┐  │
            │  │   EKS   │  │                   │  │   EKS   │  │
            │  └────┬────┘  │                   │  └────┬────┘  │
            │       │       │                   │       │       │
            │  ┌────▼────┐  │                   │  ┌────▼────┐  │
            │  │ Aurora  │──┼───────────────────┼──│ Aurora  │  │
            │  │ Global  │  │                   │  │ Replica │  │
            │  └─────────┘  │                   │  └─────────┘  │
            └───────────────┘                   └───────────────┘
```

### Step 3: Implement Security Best Practices

**AWS Security Reference Architecture**:

```hcl
# Network Security - VPC with private subnets
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
}

# Private subnets for workloads
resource "aws_subnet" "private" {
  count             = 3
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "private-${count.index + 1}"
    Tier = "private"
  }
}

# VPC Flow Logs for network monitoring
resource "aws_flow_log" "main" {
  vpc_id                   = aws_vpc.main.id
  traffic_type             = "ALL"
  log_destination_type     = "cloud-watch-logs"
  log_destination          = aws_cloudwatch_log_group.flow_logs.arn
  iam_role_arn             = aws_iam_role.flow_logs.arn
  max_aggregation_interval = 60
}

# Security Group with least privilege
resource "aws_security_group" "app" {
  name_prefix = "app-"
  vpc_id      = aws_vpc.main.id

  # No ingress from 0.0.0.0/0
  ingress {
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS to AWS services"
  }
}

# KMS key for encryption
resource "aws_kms_key" "main" {
  description             = "Main encryption key"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Enable IAM policies"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      }
    ]
  })
}
```

**Identity and Access Management**:

```hcl
# IAM Role with least privilege
resource "aws_iam_role" "app" {
  name = "app-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
      Condition = {
        StringEquals = {
          "aws:SourceAccount" = data.aws_caller_identity.current.account_id
        }
      }
    }]
  })
}

# Specific permissions, not wildcards
resource "aws_iam_role_policy" "app" {
  name = "app-policy"
  role = aws_iam_role.app.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = "${aws_s3_bucket.app_data.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = aws_secretsmanager_secret.app.arn
      }
    ]
  })
}
```

### Step 4: Implement Cost Optimization

**Cost Optimization Strategies**:

| Strategy | Savings | Implementation |
|----------|---------|----------------|
| Reserved Instances | 30-72% | 1-3 year commitments for steady-state |
| Savings Plans | 20-72% | Flexible compute commitments |
| Spot Instances | 60-90% | Fault-tolerant, flexible workloads |
| Right-sizing | 10-40% | Regular instance analysis |
| Auto-scaling | Variable | Scale with demand |
| Storage tiering | 40-80% | S3 lifecycle policies |

**Auto-Scaling Configuration**:

```hcl
resource "aws_autoscaling_group" "app" {
  name                = "app-asg"
  vpc_zone_identifier = aws_subnet.private[*].id
  target_group_arns   = [aws_lb_target_group.app.arn]
  health_check_type   = "ELB"

  min_size         = 2
  max_size         = 20
  desired_capacity = 3

  mixed_instances_policy {
    launch_template {
      launch_template_specification {
        launch_template_id = aws_launch_template.app.id
        version            = "$Latest"
      }

      # Use mix of instance types for cost/availability
      override {
        instance_type     = "m6i.large"
        weighted_capacity = "1"
      }
      override {
        instance_type     = "m6a.large"
        weighted_capacity = "1"
      }
      override {
        instance_type     = "m5.large"
        weighted_capacity = "1"
      }
    }

    instances_distribution {
      on_demand_base_capacity                  = 2
      on_demand_percentage_above_base_capacity = 25
      spot_allocation_strategy                 = "capacity-optimized"
    }
  }

  instance_refresh {
    strategy = "Rolling"
    preferences {
      min_healthy_percentage = 75
    }
  }
}

# Target tracking scaling
resource "aws_autoscaling_policy" "cpu" {
  name                   = "cpu-target-tracking"
  autoscaling_group_name = aws_autoscaling_group.app.name
  policy_type            = "TargetTrackingScaling"

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }
    target_value = 70.0
  }
}
```

**S3 Lifecycle Policy for Cost Optimization**:

```hcl
resource "aws_s3_bucket_lifecycle_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    id     = "archive-old-data"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    transition {
      days          = 365
      storage_class = "DEEP_ARCHIVE"
    }

    expiration {
      days = 2555  # 7 years
    }

    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "GLACIER"
    }

    noncurrent_version_expiration {
      noncurrent_days = 90
    }
  }
}
```

### Step 5: Design Serverless Architecture

**Event-Driven Architecture**:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  API Gateway│────►│   Lambda    │────►│  DynamoDB   │
└─────────────┘     └──────┬──────┘     └─────────────┘
                           │
                    ┌──────▼──────┐
                    │    SQS      │
                    │   Queue     │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼──────┐ ┌───▼────┐ ┌────▼─────┐
       │   Lambda    │ │ Lambda │ │  Lambda  │
       │  Worker 1   │ │Worker 2│ │ Worker 3 │
       └──────┬──────┘ └───┬────┘ └────┬─────┘
              │            │           │
              └────────────┼───────────┘
                           │
                    ┌──────▼──────┐
                    │     S3      │
                    │   Results   │
                    └─────────────┘
```

**Serverless API Pattern (AWS)**:

```hcl
# API Gateway
resource "aws_apigatewayv2_api" "main" {
  name          = "app-api"
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins = ["https://example.com"]
    allow_methods = ["GET", "POST", "PUT", "DELETE"]
    allow_headers = ["Content-Type", "Authorization"]
    max_age       = 300
  }
}

# Lambda function
resource "aws_lambda_function" "api" {
  function_name = "api-handler"
  role          = aws_iam_role.lambda.arn
  handler       = "index.handler"
  runtime       = "nodejs20.x"
  timeout       = 30
  memory_size   = 512

  filename         = data.archive_file.lambda.output_path
  source_code_hash = data.archive_file.lambda.output_base64sha256

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.main.name
    }
  }

  tracing_config {
    mode = "Active"
  }
}

# DynamoDB table
resource "aws_dynamodb_table" "main" {
  name           = "app-data"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "pk"
  range_key      = "sk"

  attribute {
    name = "pk"
    type = "S"
  }

  attribute {
    name = "sk"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  server_side_encryption {
    enabled     = true
    kms_key_arn = aws_kms_key.main.arn
  }
}
```

## Best Practices

- **Design for failure** - Assume everything can fail, build resilience
- **Use managed services** - Reduce operational burden
- **Implement defense in depth** - Multiple security layers
- **Automate everything** - Infrastructure as Code, CI/CD
- **Monitor comprehensively** - Metrics, logs, traces, alerts
- **Optimize costs continuously** - Regular reviews, FinOps practices
- **Plan for scale** - Design for 10x growth
- **Document decisions** - Architecture Decision Records (ADRs)
- **Test disaster recovery** - Regular DR drills
- **Stay current** - Cloud services evolve rapidly

## Common Patterns

### Pattern 1: Three-Tier Web Application

```
Internet → CloudFront → ALB → ECS/EKS → Aurora/RDS
                         ↓
                    ElastiCache
```

### Pattern 2: Data Lake Architecture

```
Sources → Kinesis → S3 Raw → Glue ETL → S3 Processed → Athena/Redshift
                                              ↓
                                         QuickSight
```

### Pattern 3: Microservices with Service Mesh

```
API Gateway → ALB → EKS with Istio
                    ├── Service A
                    ├── Service B
                    └── Service C
                         ↓
                    RDS/DynamoDB
```

## Cloud Comparison Quick Reference

| Service | AWS | Azure | GCP |
|---------|-----|-------|-----|
| Compute | EC2, Lambda | VMs, Functions | Compute, Functions |
| Containers | EKS, ECS | AKS, ACI | GKE, Cloud Run |
| Database | RDS, Aurora | SQL DB, Cosmos | Cloud SQL, Spanner |
| Storage | S3, EBS | Blob, Disks | Cloud Storage, PD |
| CDN | CloudFront | Front Door | Cloud CDN |
| DNS | Route 53 | DNS | Cloud DNS |
| IAM | IAM | Entra ID | IAM |

## Quality Checklist

- [ ] Multi-AZ deployment for high availability
- [ ] Encryption at rest and in transit
- [ ] Least privilege IAM policies
- [ ] VPC with private subnets for workloads
- [ ] Auto-scaling configured
- [ ] Backup and recovery tested
- [ ] Monitoring and alerting in place
- [ ] Cost allocation tags applied
- [ ] Security groups follow least privilege
- [ ] Architecture documented

## Related Skills

- `terraform-specialist` - Infrastructure provisioning
- `kubernetes-expert` - Container orchestration on cloud
- `cicd-architect` - Deployment pipelines
- `security-review` - Cloud security assessment

---

**Version**: 1.0.0
**Last Updated**: January 2026
**Based on**: awesome-claude-code-subagents patterns, AWS/Azure/GCP Well-Architected


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
