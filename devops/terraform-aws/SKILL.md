---
name: terraform-aws
description: This skill should be used when the user asks to "create terraform configuration", "deploy static site", "set up cloudfront", "configure route53", "create lambda function", "ssl certificate", or mentions S3 website hosting, CDN, serverless, JAMstack, or static site infrastructure.
version: 0.2.0
---

# Terraform for Serverless & Static Sites

Focused guidance for creating serverless and static site infrastructure on AWS using Terraform.

This skill covers: **Route53**, **S3**, **CloudFront**, **ACM**, and **Lambda**.

## Overview

This skill provides best practices for managing serverless and static site infrastructure as code using Terraform. It covers the essential AWS services for JAMstack applications, static websites, and serverless functions.

## Core Principles

### Infrastructure as Code Fundamentals

Follow these foundational principles when writing Terraform:

1. **Declarative Configuration**: Define desired state, not procedural steps
2. **Immutable Infrastructure**: Replace rather than modify resources
3. **Version Control**: All Terraform code in Git with proper branching
4. **Modularity**: Reusable modules for common patterns
5. **Security First**: Always encrypt data, use HTTPS, follow least privilege

### File Organization

Structure Terraform projects consistently. Modern projects typically use a locals-first approach:

```
static-site-infra/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── locals.tf
│   │   ├── outputs.tf
│   │   ├── versions.tf
│   │   └── backend.tf
│   ├── staging/
│   └── prod/
├── modules/
│   ├── static-site/
│   ├── lambda-function/
│   └── cdn/
├── .terraform.lock.hcl
└── README.md
```

**File conventions:**
- `main.tf` - Primary resource definitions
- `variables.tf` - Input variable declarations (minimal, project-level only)
- `locals.tf` - Environment-specific configuration and computed values
- `outputs.tf` - Output value declarations
- `versions.tf` - Terraform and provider version constraints
- `backend.tf` - Remote state configuration

## State Management

### Remote State Configuration

Always use remote state for team environments:

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "static-site/prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

### State Management Best Practices

1. **Enable Encryption**: Always encrypt state files (contains secrets like Lambda env vars)
2. **State Locking**: Use DynamoDB for state locking (prevents conflicts)
3. **Separate States**: Different state files per environment/site
4. **Backup Strategy**: Enable S3 versioning on state bucket
5. **Access Control**: Restrict state bucket access via IAM

## Security Best Practices

### Secrets Management

Never hardcode credentials or sensitive data:

```hcl
# ❌ WRONG
resource "aws_lambda_function" "api" {
  environment {
    variables = {
      API_KEY = "sk-1234567890"  # NEVER DO THIS
    }
  }
}

# ✅ CORRECT - Use AWS Secrets Manager
data "aws_secretsmanager_secret_version" "api_key" {
  secret_id = "prod/api/key"
}

resource "aws_lambda_function" "api" {
  environment {
    variables = {
      API_KEY_ARN = data.aws_secretsmanager_secret_version.api_key.arn
    }
  }
}

# ✅ CORRECT - Use variables (set via environment)
variable "api_key" {
  description = "API key for external service"
  type        = string
  sensitive   = true
}

resource "aws_lambda_function" "api" {
  environment {
    variables = {
      API_KEY = var.api_key
    }
  }
}
```

### Security Checklist

- [ ] No hardcoded credentials or secrets
- [ ] Sensitive variables marked with `sensitive = true`
- [ ] S3 buckets block public access unless explicitly needed for static hosting
- [ ] CloudFront uses HTTPS only (or redirect HTTP to HTTPS)
- [ ] ACM certificates use DNS validation
- [ ] Lambda functions use IAM roles with least privilege
- [ ] S3 encryption enabled for non-public buckets
- [ ] CloudFront uses Origin Access Identity (OAI) for S3

## Configuration Strategies

### Locals vs Tfvars: Choosing the Right Approach

#### Recommended: Locals-First for Static Sites

For static sites and serverless apps, use locals for environment-specific configuration:

```hcl
# locals.tf
locals {
  environments = {
    dev = {
      domain_name      = "dev.example.com"
      lambda_memory    = 512
      cloudfront_price_class = "PriceClass_100"
    }
    prod = {
      domain_name      = "www.example.com"
      lambda_memory    = 1024
      cloudfront_price_class = "PriceClass_All"
    }
  }

  env = local.environments[var.environment]

  common_tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
    Project     = var.project_name
  }
}

# main.tf
resource "aws_lambda_function" "api" {
  memory_size = local.env.lambda_memory

  tags = local.common_tags
}
```

**Use tfvars for**: Project name, AWS region, shared configuration

## Provider Configuration

### Version Constraints

Always pin provider versions:

```hcl
# versions.tf
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# provider.tf
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = local.common_tags
  }
}

# ACM certificates must be in us-east-1 for CloudFront
provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"

  default_tags {
    tags = local.common_tags
  }
}
```

## Resource Patterns

### S3 Static Website Hosting

```hcl
# S3 bucket for static website
resource "aws_s3_bucket" "website" {
  bucket = "${var.project_name}-${var.environment}-site"

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project_name}-${var.environment}-website"
    }
  )
}

# Block public access for CloudFront OAI pattern
resource "aws_s3_bucket_public_access_block" "website" {
  bucket = aws_s3_bucket.website.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Versioning for rollback capability
resource "aws_s3_bucket_versioning" "website" {
  bucket = aws_s3_bucket.website.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Server-side encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "website" {
  bucket = aws_s3_bucket.website.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Lifecycle rules for old versions
resource "aws_s3_bucket_lifecycle_configuration" "website" {
  bucket = aws_s3_bucket.website.id

  rule {
    id     = "cleanup-old-versions"
    status = "Enabled"

    noncurrent_version_expiration {
      noncurrent_days = 90
    }
  }
}
```

### CloudFront Distribution

```hcl
# CloudFront Origin Access Identity for S3
resource "aws_cloudfront_origin_access_identity" "website" {
  comment = "OAI for ${var.project_name}-${var.environment}"
}

# S3 bucket policy to allow CloudFront OAI
resource "aws_s3_bucket_policy" "website" {
  bucket = aws_s3_bucket.website.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowCloudFrontOAI"
        Effect = "Allow"
        Principal = {
          AWS = aws_cloudfront_origin_access_identity.website.iam_arn
        }
        Action   = "s3:GetObject"
        Resource = "${aws_s3_bucket.website.arn}/*"
      }
    ]
  })
}

# CloudFront distribution
resource "aws_cloudfront_distribution" "website" {
  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"
  aliases             = [local.env.domain_name]
  price_class         = local.env.cloudfront_price_class

  origin {
    domain_name = aws_s3_bucket.website.bucket_regional_domain_name
    origin_id   = "S3-${aws_s3_bucket.website.id}"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.website.cloudfront_access_identity_path
    }
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-${aws_s3_bucket.website.id}"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
    compress               = true
  }

  # Custom error response for SPA routing
  custom_error_response {
    error_code         = 404
    response_code      = 200
    response_page_path = "/index.html"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate.website.arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  tags = local.common_tags
}
```

### ACM Certificate

```hcl
# ACM certificate (must be in us-east-1 for CloudFront)
resource "aws_acm_certificate" "website" {
  provider = aws.us_east_1

  domain_name       = local.env.domain_name
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }

  tags = local.common_tags
}

# Route53 DNS validation records
resource "aws_route53_record" "cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.website.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.main.zone_id
}

# Certificate validation
resource "aws_acm_certificate_validation" "website" {
  provider = aws.us_east_1

  certificate_arn         = aws_acm_certificate.website.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}
```

### Route53 DNS

```hcl
# Data source for existing hosted zone
data "aws_route53_zone" "main" {
  name = var.root_domain
}

# A record for CloudFront (IPv4)
resource "aws_route53_record" "website_ipv4" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = local.env.domain_name
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.website.domain_name
    zone_id                = aws_cloudfront_distribution.website.hosted_zone_id
    evaluate_target_health = false
  }
}

# AAAA record for CloudFront (IPv6)
resource "aws_route53_record" "website_ipv6" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = local.env.domain_name
  type    = "AAAA"

  alias {
    name                   = aws_cloudfront_distribution.website.domain_name
    zone_id                = aws_cloudfront_distribution.website.hosted_zone_id
    evaluate_target_health = false
  }
}
```

### Lambda Function

```hcl
# Lambda function
resource "aws_lambda_function" "api" {
  filename      = "lambda.zip"
  function_name = "${var.project_name}-${var.environment}-api"
  role          = aws_iam_role.lambda.arn
  handler       = "index.handler"
  runtime       = "python3.11"

  source_code_hash = filebase64sha256("lambda.zip")

  environment {
    variables = {
      ENVIRONMENT = var.environment
      TABLE_NAME  = aws_dynamodb_table.data.name
    }
  }

  timeout     = 30
  memory_size = local.env.lambda_memory

  tags = local.common_tags
}

# IAM role for Lambda
resource "aws_iam_role" "lambda" {
  name = "${var.project_name}-${var.environment}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })

  tags = local.common_tags
}

# Lambda basic execution policy
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# CloudWatch log group
resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${aws_lambda_function.api.function_name}"
  retention_in_days = 14

  tags = local.common_tags
}

# Lambda function URL (for simple APIs)
resource "aws_lambda_function_url" "api" {
  function_name      = aws_lambda_function.api.function_name
  authorization_type = "NONE"

  cors {
    allow_credentials = false
    allow_origins     = ["https://${local.env.domain_name}"]
    allow_methods     = ["GET", "POST"]
    allow_headers     = ["content-type"]
    max_age           = 86400
  }
}
```

### Lambda@Edge for CloudFront

```hcl
# Lambda@Edge must be in us-east-1
resource "aws_lambda_function" "edge" {
  provider = aws.us_east_1

  filename      = "edge-function.zip"
  function_name = "${var.project_name}-${var.environment}-edge"
  role          = aws_iam_role.lambda_edge.arn
  handler       = "index.handler"
  runtime       = "python3.11"
  publish       = true  # Required for Lambda@Edge

  source_code_hash = filebase64sha256("edge-function.zip")

  timeout     = 5  # Max 5 seconds for viewer-facing functions
  memory_size = 128

  tags = local.common_tags
}

# IAM role for Lambda@Edge
resource "aws_iam_role" "lambda_edge" {
  provider = aws.us_east_1
  name     = "${var.project_name}-${var.environment}-lambda-edge-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = [
            "lambda.amazonaws.com",
            "edgelambda.amazonaws.com"
          ]
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = local.common_tags
}

# Attach to CloudFront distribution
resource "aws_cloudfront_distribution" "website_with_edge" {
  # ... other configuration ...

  default_cache_behavior {
    # ... other settings ...

    lambda_function_association {
      event_type   = "viewer-request"
      lambda_arn   = aws_lambda_function.edge.qualified_arn
      include_body = false
    }
  }
}
```

## Module Design

### Static Site Module Structure

Create a reusable module for static sites:

```hcl
# modules/static-site/main.tf
resource "aws_s3_bucket" "website" {
  bucket = var.bucket_name
}

resource "aws_cloudfront_distribution" "website" {
  # ... configuration using variables
}

# modules/static-site/variables.tf
variable "bucket_name" {
  description = "S3 bucket name for static site"
  type        = string
}

variable "domain_name" {
  description = "Custom domain name"
  type        = string
}

variable "certificate_arn" {
  description = "ACM certificate ARN"
  type        = string
}

# modules/static-site/outputs.tf
output "cloudfront_domain" {
  description = "CloudFront distribution domain"
  value       = aws_cloudfront_distribution.website.domain_name
}

output "bucket_name" {
  description = "S3 bucket name"
  value       = aws_s3_bucket.website.id
}
```

## Workflow Best Practices

### Development Workflow

```bash
# 1. Initialize
terraform init

# 2. Format code
terraform fmt -recursive

# 3. Validate configuration
terraform validate

# 4. Plan changes
terraform plan -out=tfplan

# 5. Review plan carefully
terraform show tfplan

# 6. Apply if plan looks good
terraform apply tfplan

# 7. Verify outputs
terraform output
```

### Deployment Process

For static sites:

1. **Build**: Generate static files (Next.js, Hugo, etc.)
2. **Terraform Apply**: Ensure infrastructure is up to date
3. **Upload**: Sync files to S3 (`aws s3 sync build/ s3://bucket/`)
4. **Invalidate**: Clear CloudFront cache (`aws cloudfront create-invalidation`)

For Lambda:

1. **Package**: Create deployment zip with dependencies
2. **Terraform Apply**: Deploy infrastructure and code together
3. **Test**: Invoke function to verify deployment

## Common Patterns

### Complete Static Site Stack

```hcl
# Full example combining all services
module "static_site" {
  source = "./modules/static-site"

  project_name = var.project_name
  environment  = var.environment
  domain_name  = local.env.domain_name
  root_domain  = var.root_domain

  tags = local.common_tags
}

# Outputs for CI/CD
output "bucket_name" {
  description = "S3 bucket for uploads"
  value       = module.static_site.bucket_name
}

output "cloudfront_distribution_id" {
  description = "CloudFront distribution ID for cache invalidation"
  value       = module.static_site.distribution_id
}

output "website_url" {
  description = "Website URL"
  value       = "https://${local.env.domain_name}"
}
```

### Serverless API with CloudFront

```hcl
# Lambda function for API
resource "aws_lambda_function" "api" {
  # ... configuration ...
}

# Lambda function URL
resource "aws_lambda_function_url" "api" {
  function_name = aws_lambda_function.api.function_name
  authorization_type = "NONE"
}

# CloudFront distribution for caching
resource "aws_cloudfront_distribution" "api" {
  origin {
    domain_name = replace(aws_lambda_function_url.api.function_url, "https://", "")
    origin_id   = "lambda-api"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  # Cache based on query strings and headers
  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = "lambda-api"

    forwarded_values {
      query_string = true
      headers      = ["Authorization"]

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 0  # No caching for API by default
    max_ttl                = 3600
  }

  # ... rest of CloudFront config
}
```

## Troubleshooting

### CloudFront Updates Take Time

**Issue**: CloudFront changes take 15-30 minutes to deploy

**Solution**: Use `terraform apply -target` for other resources, plan CloudFront updates during maintenance windows

### ACM Certificate Validation Stuck

**Issue**: Certificate validation pending

**Solution**:
- Verify DNS records are created correctly
- Check Route53 hosted zone is correct
- Wait up to 30 minutes for DNS propagation
- Use `terraform refresh` to check validation status

### S3 Bucket Not Empty Error

**Issue**: Can't destroy S3 bucket with objects

**Solution**:
```bash
# Empty bucket before destroy
aws s3 rm s3://bucket-name --recursive

# Or use lifecycle policy
resource "aws_s3_bucket_lifecycle_configuration" "cleanup" {
  bucket = aws_s3_bucket.website.id

  rule {
    id     = "expire-all"
    status = "Enabled"
    expiration {
      days = 1
    }
  }
}
```

### Lambda Deployment Package Too Large

**Issue**: Lambda zip > 50MB

**Solution**: Use S3 for deployment package:
```hcl
resource "aws_s3_object" "lambda_zip" {
  bucket = aws_s3_bucket.deployments.id
  key    = "lambda/${var.version}/function.zip"
  source = "lambda.zip"
  etag   = filemd5("lambda.zip")
}

resource "aws_lambda_function" "api" {
  s3_bucket = aws_s3_bucket.deployments.id
  s3_key    = aws_s3_object.lambda_zip.key
  # ... rest of config
}
```

## Summary

When working with Terraform for static sites and serverless:

1. **Structure**: Use locals for environment config, modules for reusable components
2. **State**: Remote state with encryption and locking
3. **Security**: HTTPS everywhere, OAI for S3, least privilege IAM
4. **Certificates**: ACM in us-east-1 for CloudFront, DNS validation
5. **CloudFront**: Use OAI, enable compression, redirect HTTP→HTTPS
6. **Lambda**: Proper IAM roles, CloudWatch logs, appropriate timeouts
7. **Route53**: Use alias records for CloudFront
8. **Workflow**: Plan → Review → Apply → Test

For complete examples, see the `examples/` directory.
