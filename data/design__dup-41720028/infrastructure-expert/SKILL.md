---
name: infrastructure-expert
description: Expert infrastructure design including networking, compute, storage, and operations
version: 1.0.0
author: USER
tags: [infrastructure, networking, compute, storage, operations]
---

# Infrastructure Expert

## Purpose
Design robust infrastructure including networking, compute resources, storage systems, and operational practices.

## Activation Keywords
- infrastructure, infra
- networking, VPC, subnet
- compute, servers, instances
- storage, disk, volume
- operations, SRE

## Core Capabilities

### 1. Networking
- VPC design
- Subnet planning
- Security groups
- Load balancers
- DNS/CDN

### 2. Compute
- Instance selection
- Container orchestration
- Serverless
- Spot/Preemptible
- Reserved capacity

### 3. Storage
- Block storage
- Object storage
- File storage
- Backup strategies
- Data lifecycle

### 4. Operations
- Monitoring
- Logging
- Alerting
- Incident response
- Runbooks

### 5. Disaster Recovery
- RPO/RTO definitions
- Backup verification
- Failover testing
- Multi-region design

## Network Architecture

```
VPC Design:
┌─────────────────────────────────────┐
│ VPC (10.0.0.0/16)                   │
│  ├─ Public Subnet (10.0.1.0/24)    │
│  │   └─ NAT Gateway, Bastion       │
│  ├─ Private Subnet (10.0.2.0/24)   │
│  │   └─ Application servers        │
│  └─ Data Subnet (10.0.3.0/24)      │
│      └─ Databases                   │
└─────────────────────────────────────┘
```

## Infrastructure as Code

```hcl
# Terraform example
module "vpc" {
  source = "./modules/vpc"

  name             = "production"
  cidr             = "10.0.0.0/16"
  azs              = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets   = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = false  # High availability

  tags = {
    Environment = "production"
    Terraform   = "true"
  }
}
```

## Storage Selection Guide

| Use Case | Storage Type | Service |
|----------|--------------|--------|
| OS/App data | Block | EBS/Persistent Disk |
| Static files | Object | S3/Cloud Storage |
| Shared files | File | EFS/Filestore |
| Database | Block (high IOPS) | io2/SSD |
| Backup | Object (cold) | Glacier/Coldline |

## Operational Checklist

```markdown
## Monitoring
- [ ] System metrics (CPU, Memory, Disk)
- [ ] Application metrics
- [ ] Business metrics
- [ ] Synthetic monitoring

## Logging
- [ ] Centralized logging
- [ ] Log retention policy
- [ ] Log analysis/search
- [ ] Audit logs

## Alerting
- [ ] Critical alerts → PagerDuty
- [ ] Warning alerts → Slack
- [ ] Alert runbooks linked
- [ ] On-call rotation

## Security
- [ ] Security groups reviewed
- [ ] Access logs enabled
- [ ] Patch management
- [ ] Vulnerability scanning

## Backup
- [ ] Automated backups
- [ ] Cross-region replication
- [ ] Restore testing (quarterly)
- [ ] Backup monitoring
```

## Disaster Recovery Tiers

| Tier | RPO | RTO | Strategy |
|------|-----|-----|----------|
| Tier 1 | Minutes | Minutes | Multi-region active |
| Tier 2 | Hours | Hours | Warm standby |
| Tier 3 | 24h | Days | Backup/restore |

## Example Usage

```
User: "Design infrastructure for a new production environment"

Infrastructure Expert Response:
1. Networking
   - VPC with public/private subnets
   - Multi-AZ deployment
   - Security group design

2. Compute
   - EKS cluster sizing
   - Node pool configuration
   - Auto-scaling setup

3. Storage
   - EBS for databases
   - S3 for static assets
   - Backup to Glacier

4. Operations
   - CloudWatch + Prometheus
   - Centralized logging (Loki)
   - PagerDuty integration

5. DR Plan
   - RPO: 1 hour
   - RTO: 4 hours
   - Cross-region backup
```
