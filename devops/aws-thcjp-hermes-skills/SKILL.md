---
name: aws
slug: aws
displayName: "Aws"
version: "1.0.2"
summary: "AWS架构设计、部署、成本优化,规避资源浪费与安全陷阱,降低云上运维成本"
description: "AWS架构设计、部署、成本优化,规避资源浪费与安全陷阱,降低云上运维成本。Architect, deploy, and optimize AWS infrastructure avoiding cost explosions。触发关键词: web, deploy, architect, avoiding, aws, optimize, infrastructure, amazon。"
license: "MIT"
tools:
  - read
---

# AWS | Amazon Web Services

## Setup

On first use, read `setup.md` for integration options. The skill works immediately — setup is optional for personalization.

## When to Use

User needs AWS infrastructure guidance. Agent handles architecture decisions, service selection, cost optimization, security hardening, and deployment patterns.

## Architecture

Memory lives in `~/aws/`. See `memory-template.md` for structure.

```text
~/aws/
├── memory.md        # Account context + preferences
├── resources.md     # Active infrastructure inventory
└── costs.md         # Cost tracking + alerts
```

## Quick Reference

| Topic | File |
| --- | --- |
| Setup process | `setup.md` |
| Memory template | `memory-template.md` |
| Service patterns | `services.md` |
| Cost optimization | `costs.md` |
| Security hardening | `security.md` |

## Core Rules

### 1. Verify Account Context First

Before any operation, confirm:

* Region (default: us-east-1, but ask)
* Account type (personal/startup/enterprise)
* Existing infrastructure (VPC, subnets, security groups)

```bash
aws sts get-caller-identity
aws ec2 describe-vpcs --query 'Vpcs[].{ID:VpcId,CIDR:CidrBlock,Default:IsDefault}'
```

### 2. Cost-First Architecture

Every recommendation includes cost impact:

| Stage | Recommended Stack | Monthly Cost |
| --- | --- | --- |
| MVP (<1k users) | Single EC2 + RDS | ~$50 |
| Growth (1-10k) | ALB + ASG + RDS Multi-AZ | ~$200 |
| Scale (10k+) | ECS/EKS + Aurora + ElastiCache | ~$500+ |

**Default to smallest viable instance.** Scaling up is easy; scaling down wastes money.

### 3. Security by Default

Every resource includes:

* Principle of least privilege IAM
* Encryption at rest (KMS default key minimum)
* VPC isolation (no public subnets for databases)
* Security groups with explicit deny-all inbound

### 4. Infrastructure as Code

Generate Terraform or CloudFormation for reproducibility:

```bash
terraform init && terraform plan
```

Never rely on console-only changes.

### 5. Tagging Strategy

Every resource gets tagged for cost allocation:

```bash
--tags Key=Environment,Value=prod Key=Project,Value=myapp Key=Owner,Value=team
```

### 6. Monitoring from Day 1

Deploy CloudWatch alarms with infrastructure:

* Billing alerts (before you get surprised)
* CPU/Memory thresholds
* Error rate spikes

## Cost Traps

**NAT Gateway data processing ($0.045/GB):**
VPC endpoints are free for S3/DynamoDB. A busy app can burn $500/month on NAT alone.

```bash
aws ec2 create-vpc-endpoint --vpc-id vpc- \
  --service-name com.amazonaws.us-east-1.s3 --route-table-ids rtb-
```

**EBS snapshots accumulate forever:**
Automated backups create snapshots that never delete. Set lifecycle policies.

```bash
aws ec2 describe-snapshots --owner-ids self \
  --query 'Snapshots[?StartTime<=`2024-01-01`].[SnapshotId,StartTime,VolumeSize]'
```

**CloudWatch Logs default retention is forever:**

```bash
aws logs put-retention-policy --log-group-name /aws/lambda/fn --retention-in-days 14
```

**Idle load balancers cost $16/month minimum:**
ALBs charge even with zero traffic. Delete unused ones.

**Data transfer between AZs costs $0.01/GB each way:**
Chatty microservices across AZs add up fast. Co-locate when possible.

## Security Traps

**S3 bucket policies override ACLs:**
Console shows ACL as "private" but a bucket policy can still expose everything.

```bash
aws s3api get-bucket-policy --bucket my-bucket 2>/dev/null || echo "No policy"
aws s3api get-public-access-block --bucket my-bucket
```

**Default VPC security groups allow all outbound:**
Attackers exfiltrate through outbound. Restrict it.

**IAM users with console access + programmatic access:**
Credentials in code get leaked. Use roles + temporary credentials.

**RDS publicly accessible defaults to Yes in console:**
Always verify:

```bash
aws rds describe-db-instances --query 'DBInstances[].{ID:DBInstanceIdentifier,Public:PubliclyAccessible}'
```

## Performance Patterns

**Lambda cold starts:**

* Use provisioned concurrency for latency-sensitive functions
* Keep packages small (<50MB unzipped)
* Initialize SDK clients outside handler

**RDS connection limits:**

| Instance | Max Connections |
| --- | --- |
| db.t3.micro | 66 |
| db.t3.small | 150 |
| db.t3.medium | 300 |

Use RDS Proxy for Lambda to avoid connection exhaustion.

**EBS volume types:**

| Type | Use Case | IOPS |
| --- | --- | --- |
| gp3 | Default (consistent) | 3,000 base |
| io2 | Databases (guaranteed) | Up to 64,000 |
| st1 | Big data (throughput) | 500 MiB/s |

## Service Selection

| Need | Service | Why |
| --- | --- | --- |
| Static site | S3 + CloudFront | Pennies/month, global CDN |
| API backend | Lambda + API Gateway | Zero idle cost |
| Container app | ECS Fargate | No cluster management |
| Database | RDS 关系型数据库 | Managed, Multi-AZ ready |
| Cache | ElastiCache Redis | Session/cache, < DynamoDB latency |
| Queue | SQS | Simpler than SNS for most cases |
| Search | OpenSearch | Elasticsearch managed |

## CLI Essentials

```bash
aws configure --profile myproject

export AWS_PROFILE=myproject

aws sts get-caller-identity

aws ec2 describe-regions --query 'Regions[].RegionName'

aws ce get-cost-forecast --time-period Start=$(date +%Y-%m-01),End=$(date -v+1m +%Y-%m-01) \
  --metric UNBLENDED_COST --granularity MONTHLY
```

## Security & Privacy

**Credentials:** This skill uses the AWS CLI, which reads credentials from `[REDACTED_AWS_PATH] or environment variables. The skill never stores, logs, or transmits AWS credentials.

**Local storage:** Preferences and context stored in `~/aws/` — no data leaves your machine.

**CLI commands:** All commands shown are read-only by default. Destructive operations (delete, terminate) require explicit user confirmation.

## Related Skills

Install with `* 安装此Skill请参考SkillHub平台指南

* `infrastructure` — architecture decisions
* `cloud` — multi-cloud patterns
* `docker` — container basics
* `backend` — API design

## Feedback

* If useful: `
* Stay updated: `

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent( Code / Cursor / Codex /  CLI等)
- **操作系统**: Windows / macOS / Linux

### 依赖说明
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 本Skill基于Markdown指令,无需额外API Key(除内容中明确标注的外部API)

### 可用性分类
- **分类**: MD+execute(纯Markdown指令,部分功能需要exec命令行执行能力)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行任务

## 核心能力

- Architect, deploy, and optimize AWS infrastructure avoiding cost explosions
  and security pitfalls
- 触发关键词: web, deploy, architect, avoiding, aws, optimize, infrastructure, amazon

## 适用场景

| 场景 | 输入 | 输出 |
|------|------|------|
| 基础使用 | 用户请求 | 处理结果 |

**不适用于**：需要人工判断的复杂决策场景

## 使用流程

1. 确认运行环境满足依赖说明中的要求
2. 根据适用场景选择合适的使用方式
3. 执行操作并检查输出结果
4. 如遇错误，参考错误处理章节

## 示例

### 示例1：基础用法

```
输入: 用户请求
处理: 根据使用流程执行
输出: 处理结果
```

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 检查网络连接后重试，参考国内替代方案 |

## 常见问题

### Q1: 如何开始使用Aws？
A: 请先阅读使用流程章节，确认环境满足依赖说明中的要求。

### Q2: 遇到错误怎么办？
A: 请参考错误处理章节，按照表格中的处理方式操作。

### Q3: Aws有什么限制？
A: 请参考已知限制章节了解具体限制。

## 已知限制

- 依赖云服务，需要网络连接
