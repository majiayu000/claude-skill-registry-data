---
name: aws-expert
description: AWS cloud architecture and serverless expertise from Amazon veterans (Distinguished Engineers, Prime Day scale). Use when setting up AWS infrastructure (EC2, ECS, EKS, Lambda, S3, RDS, DynamoDB), designing high-availability architectures, optimizing cloud costs, building serverless APIs with API Gateway, or deploying multi-region systems. Triggers on AWS services, cloud infrastructure, serverless, auto-scaling, VPC, CloudFront, IAM, or any Amazon Web Services task.
category: infrastructure
level: 8-10
companies: [Amazon, Netflix, Airbnb]
related_skills: [terraform, kubernetes-expert, serverless]
---

# AWS Expert Skill

## Overview

AWS cloud expertise from Amazon engineers who built and operate the world's largest cloud platform.

## What Qualifies as "AWS Expert"

### Level 10/10 (Distinguished)
- 12+ years at AWS or using AWS at massive scale
- Designed AWS services or major platform components
- Handles Prime Day level traffic (100M+ req/min)
- Deep knowledge of 50+ AWS services
- Examples: Amazon Distinguished Engineers, AWS Solutions Architects

### Level 9/10 (Principal)
- 10+ years of AWS experience
- Architected multi-region, highly available systems
- Expert in cost optimization at scale
- Can design complex microservices on AWS
- Examples: Principal Engineers at Amazon, Netflix, Airbnb

### Level 8/10 (Senior)
- 7+ years of AWS experience
- Can architect production-grade systems
- Strong DevOps and automation skills
- Handles millions of users

## Key Capabilities

### Compute Services
- **EC2**: Instances, auto-scaling, spot instances
- **ECS**: Container orchestration
- **EKS**: Kubernetes on AWS
- **Lambda**: Serverless functions
- **Fargate**: Serverless containers

### Storage & Database
- **S3**: Object storage, lifecycle policies, versioning
- **RDS**: PostgreSQL, MySQL, Aurora
- **DynamoDB**: NoSQL at scale, GSI/LSI, DAX caching
- **ElastiCache**: Redis, Memcached
- **EBS**: Block storage, snapshot strategies

### Networking & Content Delivery
- **VPC**: Networking, subnets, security groups
- **CloudFront**: CDN, edge computing, Lambda@Edge
- **Route53**: DNS, health checks, failover
- **API Gateway**: REST/WebSocket APIs
- **ALB/NLB**: Load balancing

### Developer Tools
- **CodePipeline**: CI/CD automation
- **CodeBuild**: Build automation
- **CodeDeploy**: Deployment strategies
- **CloudFormation**: Infrastructure as Code
- **CDK**: AWS Cloud Development Kit

### Monitoring & Operations
- **CloudWatch**: Metrics, logs, alarms, dashboards
- **X-Ray**: Distributed tracing
- **Systems Manager**: Operations management
- **CloudTrail**: Audit logs

### Security & Compliance
- **IAM**: Users, roles, policies
- **KMS**: Encryption key management
- **Secrets Manager**: Secret rotation
- **WAF**: Web application firewall
- **Shield**: DDoS protection

## Notable AWS Architectures at FAANG

### Amazon.com
- Prime Day infrastructure (100M+ req/min)
- Multi-region active-active
- Microservices on ECS/EKS
- DynamoDB for cart (scales to zero)

### Netflix
- Global streaming on AWS (all workloads)
- 200+ microservices
- Multi-region disaster recovery
- Chaos engineering (Chaos Monkey)

### Airbnb
- Payment processing on AWS
- Search on ElasticSearch
- Data pipeline on EMR

## Architecture Patterns

### High Availability Pattern
```
┌─────────────────────────────────────┐
│         Route53 (DNS)               │
│    Health checks + Failover         │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│       CloudFront (CDN)              │
│    Global edge caching              │
└─────────────┬───────────────────────┘
              │
         ┌────▼────┐
         │   ALB   │
         │ (Multi-AZ)
         └────┬────┘
    ┌────────┼────────┐
    │        │        │
┌───▼──┐ ┌──▼───┐ ┌─▼────┐
│ ECS  │ │ ECS  │ │ ECS  │
│ (AZ1)│ │(AZ2) │ │(AZ3) │
└──────┘ └──────┘ └──────┘
```

### Serverless Pattern
```
API Gateway → Lambda → DynamoDB
                │
                ├→ S3 (storage)
                └→ SQS (async tasks)
```

### Microservices Pattern
```
ALB
 ├→ Service 1 (ECS) → RDS (PostgreSQL)
 ├→ Service 2 (Lambda) → DynamoDB
 └→ Service 3 (ECS) → ElastiCache (Redis)
```

## Cost Optimization Techniques

From Amazon experts:

1. **Right-sizing**: Use Compute Optimizer
2. **Reserved Instances**: 1-year or 3-year for steady workloads
3. **Spot Instances**: 90% discount for fault-tolerant workloads
4. **Savings Plans**: Flexible commitment
5. **S3 Lifecycle**: Move to Glacier, Intelligent-Tiering
6. **Auto-scaling**: Scale down during off-peak
7. **Lambda**: Pay per use, scales to zero
8. **DynamoDB On-Demand**: For unpredictable traffic

Amazon Prime Day example: $2M+ saved through spot instances and pre-warming strategies.

## Typical Responsibilities

AWS experts at Amazon/FAANG:
- Design cloud architectures
- Optimize costs (millions in savings)
- Ensure 99.99%+ uptime
- Automate infrastructure (IaC)
- Set up monitoring and alerting
- Security and compliance
- Disaster recovery planning
- Capacity planning
- Performance optimization

## When to Need AWS Experts

Projects requiring:
- Cloud infrastructure setup
- High availability (99.99%+)
- Scalability (millions of users)
- Cost optimization
- Microservices on AWS
- Serverless architectures
- Multi-region deployments
- Disaster recovery
- DevOps automation

## Related Skills

AWS experts often also have:
- **Terraform**: Infrastructure as Code
- **Docker & Kubernetes**: Containers
- **Linux**: Systems administration
- **Networking**: VPC, DNS, load balancing
- **Security**: IAM, encryption, compliance
- **Monitoring**: CloudWatch, Datadog, Prometheus
- **CI/CD**: Jenkins, GitHub Actions
- **Scripting**: Python, Bash
