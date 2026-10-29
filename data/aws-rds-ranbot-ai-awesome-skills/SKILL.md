---
name: aws-rds
description: Provision and manage RDS databases. Configure backups, replication, and security. Use when deploying managed relational databases on AWS. 
category: AI & Agents
source: antigravity
tags: [api, ai, agent, template, security, aws, rag, cro]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/aws-rds
---


# AWS RDS

Deploy and manage Amazon RDS relational databases with production-grade backups, replication, monitoring, and security.

## When to Use This Skill

- Provisioning a managed PostgreSQL, MySQL, MariaDB, Oracle, or SQL Server database
- Setting up Multi-AZ deployments for high availability
- Creating read replicas for horizontal read scaling
- Configuring automated backups, snapshots, and point-in-time recovery
- Tuning database parameters for performance
- Migrating from self-managed databases to RDS
- Monitoring database performance and setting up alarms

## Prerequisites

- AWS CLI v2 installed and configured
- Least-privilege IAM actions for the selected RDS, subnet, monitoring and KMS resources; avoid service-wide wildcard grants
- A VPC with at least two subnets in different AZs (for subnet group)
- Security group allowing database port access from application subnets only

## Create a DB Subnet Group

```bash
# Create a subnet group spanning two AZs
aws rds create-db-subnet-group \
  --db-subnet-group-name production-db-subnets \
  --db-subnet-group-description "Production database subnets" \
  --subnet-ids subnet-private-a subnet-private-b

# List subnet groups
aws rds describe-db-subnet-groups \
  --query "DBSubnetGroups[].{Name:DBSubnetGroupName,VPC:VpcId,Status:SubnetGroupStatus}" \
  --output table
```

## Create a Production Database

```bash
# Create a PostgreSQL 16 Multi-AZ instance
aws rds create-db-instance \
  --db-instance-identifier production-api-db \
  --db-instance-class db.r6g.large \
  --engine postgres \
  --engine-version 16.4 \
  --master-username appadmin \
  --manage-master-user-password \
  --allocated-storage 100 \
  --max-allocated-storage 500 \
  --storage-type gp3 \
  --storage-encrypted \
  --kms-key-id alias/rds-key \
  --vpc-security-group-ids sg-db-access \
  --db-subnet-group-name production-db-subnets \
  --db-name appdb \
  --backup-retention-period 14 \
  --preferred-backup-window "03:00-04:00" \
  --preferred-maintenance-window "sun:05:00-sun:06:00" \
  --multi-az \
  --auto-minor-version-upgrade \
  --deletion-protection \
  --copy-tags-to-snapshot \
  --monitoring-interval 60 \
  --monitoring-role-arn arn:aws:iam::123456789012:role/rds-monitoring-role \
  --enable-performance-insights \
  --performance-insights-retention-period 7 \
  --enable-cloudwatch-logs-exports '["postgresql","upgrade"]' \
  --tags '[
    {"Key":"Environment","Value":"production"},
    {"Key":"Team","Value":"backend"},
    {"Key":"Backup","Value":"daily"}
  ]'

# Wait for instance to become available
aws rds wait db-instance-available --db-instance-identifier production-api-db

# Get connection endpoint
aws rds describe-db-instances \
  --db-instance-identifier production-api-db \
  --query "DBInstances[0].Endpoint.{Address:Address,Port:Port}" \
  --output table
```

## Retrieve Master Password from Secrets Manager

```bash
# When using --manage-master-user-password, RDS stores the password in Secrets Manager
aws rds describe-db-instances \
  --db-instance-identifier production-api-db \
  --query "DBInstances[0].MasterUserSecret.SecretArn" \
  --output text

# Retrieve the secret value
aws secretsmanager get-secret-value \
  --secret-id arn:aws:secretsmanager:us-east-1:123456789012:secret:rds-db-secret-abc123 \
  --query SecretString --output text
```

## Parameter Groups

```bash
# Create a custom parameter group
aws rds create-db-parameter-group \
  --db-parameter-group-name production-pg16 \
  --db-parameter-group-family postgres16 \
  --description "Production PostgreSQL 16 parameters"

# Set performance parameters
aws rds modify-db-parameter-group \
  --db-parameter-group-name production-pg16 \
  --parameters \
    "ParameterName=max_connections,ParameterValue=200,ApplyMethod=pending-reboot" \
    "ParameterName=shared_buffers,ParameterValue={DBInstanceClassMemory/32768},ApplyMethod=pending-reboot" \
    "ParameterName=effective_cache_size,ParameterValue={DBInstanceClassMemory*3/32768},ApplyMethod=pending-reboot" \
    "ParameterName=work_mem,ParameterValue=65536,ApplyMethod=immediate" \
    "ParameterName=maintenance_work_mem,ParameterValue=524288,ApplyMethod=immediate" \
    "ParameterName=random_page_cost,ParameterValue=1.1,ApplyMethod=immediate" \
    "ParameterName=log_min_duration_statement,ParameterValue=1000,ApplyMethod=immediate" \
    "ParameterName=log_statement,ParameterValue=ddl,ApplyMethod=immediate" \
    "ParameterName=idle_in_transaction_session_timeout,ParameterValue=60000,ApplyMethod=immediate"

# Apply parameter group to the instance
aws rds modify-db-instance \
  --db-instance-identifier production-api-db \
  --db-parameter-group-name production-pg16 \
  --apply-immediately
```

## Read Replicas

```bash
# Create a read replica in the same region
aws rds create-db-instance-read-replica \
  --db-instance-identifier production-api-db-read1 \
  --source-db-instance-identifier production-api-db \
  --db-instance-class db.r6g.large \
  --availability-zone us-ea
