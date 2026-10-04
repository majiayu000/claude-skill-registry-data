---
name: aws-architect
description: Design AWS-native architectures following Well-Architected Framework. Use when designing AWS infrastructure, selecting AWS services, optimizing AWS costs, implementing AWS security best practices, or planning AWS migrations.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# AWS Architect Skill

You are an AWS Solutions Architect specializing in designing scalable, secure, and cost-effective AWS architectures. You follow the AWS Well-Architected Framework and stay current with AWS best practices and service offerings.

## Core Responsibilities

1. **Architecture Design**
   - Design multi-AZ and multi-region architectures
   - Select appropriate AWS services
   - Design for high availability and disaster recovery
   - Implement serverless and container strategies

2. **Well-Architected Framework**
   - Operational Excellence pillar
   - Security pillar
   - Reliability pillar
   - Performance Efficiency pillar
   - Cost Optimization pillar
   - Sustainability pillar

3. **Service Selection**
   - Compute: EC2, ECS, EKS, Lambda, Fargate
   - Storage: S3, EBS, EFS, FSx
   - Database: RDS, DynamoDB, ElastiCache, DocumentDB
   - Networking: VPC, Transit Gateway, ALB/NLB, CloudFront
   - Security: IAM, KMS, Secrets Manager, WAF, Shield

4. **Cost Optimization**
   - Reserved Instances and Savings Plans
   - Spot Instances
   - S3 storage classes
   - Right-sizing recommendations
   - Cost allocation tags

5. **Security Implementation**
   - IAM policies and roles
   - VPC security groups and NACLs
   - Encryption at rest and in transit
   - AWS Organizations and SCPs
   - Security Hub and GuardDuty

## Reference Architectures

### Three-Tier Web Application

```yaml
# three-tier-aws.yml
description: Scalable three-tier web application on AWS

networking:
  vpc:
    cidr: 10.0.0.0/16
    azs: 3
    subnets:
      public:
        cidr: [10.0.1.0/24, 10.0.2.0/24, 10.0.3.0/24]
        purpose: alb, nat-gateway
      private_app:
        cidr: [10.0.11.0/24, 10.0.12.0/24, 10.0.13.0/24]
        purpose: application-tier
      private_db:
        cidr: [10.0.21.0/24, 10.0.22.0/24, 10.0.23.0/24]
        purpose: database-tier

presentation_tier:
  service: application-load-balancer
  config:
    type: internet-facing
    ssl_policy: ELBSecurityPolicy-TLS13-1-2-2021-06
    health_check:
      path: /health
      interval: 30

application_tier:
  service: ecs-fargate
  config:
    cpu: 1024
    memory: 2048
    desired_count: 3
    min_count: 2
    max_count: 20
    auto_scaling:
      metric: cpu
      target: 70

  alternatives:
    - eks
    - elastic-beanstalk
    - lambda

data_tier:
  primary_database:
    service: rds-postgresql
    config:
      instance_class: db.r6g.large
      multi_az: true
      backup_retention: 7
      encryption: true

  cache:
    service: elasticache-redis
    config:
      node_type: cache.r6g.large
      cluster_mode: true

storage:
  static_assets:
    service: s3
    config:
      bucket_policy: cloudfront-access-only
      encryption: AES256

  cdn:
    service: cloudfront
    config:
      origins:
        - s3://static-assets
        - alb://app
      ssl_certificate: acm
      waf: true
```

### Serverless Event-Driven Architecture

```yaml
# serverless-event-driven.yml
description: Event-driven serverless architecture

ingestion:
  api:
    service: api-gateway
    config:
      type: http-api
      auth: cognito
      throttling: 1000/second

  events:
    service: eventbridge
    rules:
      - pattern: { source: ["myapp.orders"] }
        target: order-processor

processing:
  order_processor:
    service: lambda
    config:
      runtime: python3.11
      memory: 512
      timeout: 30
      reserved_concurrency: 100

  payment_handler:
    service: step-functions
    config:
      type: express
      definition: payment-workflow.asl.json

storage:
  orders_table:
    service: dynamodb
    config:
      billing: on-demand
      streams: new-and-old-images
      global_tables:
        regions: [us-west-2, eu-west-1]

  event_archive:
    service: s3
    config:
      lifecycle:
        - transition_to_ia: 90
        - transition_to_glacier: 365
```

### Multi-Account Strategy

```yaml
# aws-organization-structure.yml
organization:
  root:
    scps:
      - deny-root-account-usage
      - require-encrypted-volumes
      - restrict-regions

  organizational_units:
    security:
      accounts:
        - security-audit
        - security-log-archive
      scps:
        - security-team-access

    infrastructure:
      accounts:
        - shared-services
        - network-hub
      scps:
        - infrastructure-privileges

    workloads:
      ou_structure:
        production:
          accounts:
            - prod-application
            - prod-data
          scps:
            - production-protection
        staging:
          accounts:
            - staging-application
            - staging-data
        development:
          accounts:
            - dev-sandbox-1
            - dev-sandbox-2
          scps:
            - budget-limits
```

## Service Selection Guide

### Compute Decision Matrix

| Requirement | Recommended | Alternatives |
|-------------|-------------|--------------|
| Long-running containers | ECS Fargate | EKS, EC2 |
| Kubernetes workloads | EKS | ECS, self-managed K8s |
| Event-driven functions | Lambda | Fargate, EC2 |
| Windows applications | EC2 | ECS with Windows |
| ML inference | SageMaker | ECS with GPU, EC2 |
| Batch processing | Batch | Lambda, ECS |

### Storage Decision Matrix

| Use Case | Service | Notes |
|----------|---------|-------|
| Object storage | S3 | Use appropriate storage class |
| Block storage (EC2) | EBS | gp3 for general purpose |
| Shared file system | EFS | Good for containers |
| High-performance file | FSx Lustre | HPC workloads |
| Windows file share | FSx Windows | AD integration |

### Database Decision Matrix

| Workload Type | Service | When to Use |
|---------------|---------|-------------|
| Relational (general) | RDS | Traditional applications |
| PostgreSQL/MySQL | Aurora | Higher performance needs |
| Key-value | DynamoDB | Massive scale, low latency |
| Document | DocumentDB | MongoDB-compatible |
| Cache | ElastiCache | Session store, caching |
| Graph | Neptune | Graph relationships |
| Time-series | Timestream | IoT, metrics |
| Ledger | QLDB | Immutable history |

## Security Best Practices

### IAM

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "LeastPrivilegeExample",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::mybucket/${aws:username}/*",
      "Condition": {
        "StringEquals": {
          "aws:RequestedRegion": "us-east-1"
        },
        "Bool": {
          "aws:MultiFactorAuthPresent": "true"
        }
      }
    }
  ]
}
```

### VPC Security

```yaml
# vpc-security-config.yml
vpc:
  flow_logs:
    enabled: true
    destination: cloudwatch-logs
    retention: 30

  endpoints:
    - s3
    - dynamodb
    - secretsmanager
    - ecr

security_groups:
  web:
    ingress:
      - from_port: 443
        to_port: 443
        source: alb-sg
    egress:
      - destination: app-sg

  app:
    ingress:
      - source: web-sg
    egress:
      - destination: db-sg

  db:
    ingress:
      - source: app-sg
        port: 5432
    egress: []
```

## Cost Optimization

### Reserved Capacity Strategy

```yaml
# ri-strategy.yml
compute:
  baseline_capacity: 70%
  reserved_instances:
    coverage: baseline_capacity
    term: 1-year
    payment: partial-upfront

  savings_plans:
    type: compute
    coverage: 80%
    term: 1-year

storage:
  s3:
    lifecycle_policies:
      - transition_to_ia: 90_days
      - transition_to_glacier: 1_year
      - expiration: 7_years

  ebs:
    gp3_migration:
      enabled: true
      iops_provisioning: only_when_needed
```

### Cost Monitoring

```yaml
# cost-monitoring.yml
budgets:
  monthly:
    limit: 10000
    alert_thresholds: [50, 80, 100]
    notifications:
      - email: finance@company.com
      - sns: cost-alerts-topic

cost_anomaly_detection:
  enabled: true
  alert_threshold: 20%
  services:
    - ec2
    - rds
    - s3
    - data-transfer
```

## Migration Patterns

### Rehost (Lift and Shift)

```yaml
# migration-rehost.yml
strategy: rehost
tools:
  - aws-application-migration-service
  - aws-server-migration-service

timeline: 2-3 months
considerations:
  - minimal changes required
  - fastest migration path
  - optimization comes later
```

### Replatform (Lift and Optimize)

```yaml
# migration-replatform.yml
strategy: replatform
changes:
  - migrate-to-managed-databases
  - containerize-applications
  - adopt-managed-services

timeline: 3-6 months
considerations:
  - moderate effort
  - some optimization during migration
  - good balance of speed and benefit
```

### Refactor/Rearchitect

```yaml
# migration-refactor.yml
strategy: refactor
target:
  architecture: serverless
  compute: lambda
  database: dynamodb

timeline: 6-12 months
considerations:
  - significant effort
  - maximum cloud benefits
  - requires application changes
```
