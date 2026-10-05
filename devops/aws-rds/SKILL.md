---




name: aws-rds
description: Deploys managed relational databases (MySQL, PostgreSQL, MariaDB, Oracle, SQL Server) with multi-AZ failover, automated backups, read replicas, and encryption for production-grade database infrastructure.
license: MIT
compatibility: opencode
metadata:
  version: "1.0.0"
  domain: cncf
  output-format: manifests
  role: implementation
  scope: infrastructure
  triggers: aws rds, relational database, mysql, postgresql, automated backup, multi-az, read replica
  related-skills: aws-sdk, aws-cloudwatch, aws-kms
  archetypes:
    - educational
    - tactical
  anti_triggers:
    - mismanaged storage
    - weak security
  response_profile:
    verbosity: high




---




---

## When to Use

Use this skill when:

- Provisioning a managed relational database (MySQL, PostgreSQL, MariaDB, Oracle, SQL Server) for production workloads
- Setting up multi-AZ failover for high availability requirements
- Creating read replicas to offload read-heavy query traffic from the primary instance
- Configuring automated backups with point-in-time recovery for regulatory compliance
- Migrating an existing database to AWS RDS with minimal downtime using DMS or logical exports

## When NOT to Use

Avoid this skill for:

- Simple development databases that can use a local Docker container instead of managed infrastructure
- Workloads requiring kernel-level tuning (e.g., custom MySQL settings, shared memory tweaks) — use EC2-based MySQL/PostgreSQL
- Situations where you need direct SSH access to the database server for emergency debugging

---

## Core Workflow

1. **Define Database Configuration** — Choose engine type, instance class, storage size, and backup retention based on workload requirements and cost constraints. Always enable encryption at rest with a KMS key.
   **Checkpoint:** Verify that the selected instance class supports the required IOPS and that the storage type (gp3 or io2) matches performance needs.

2. **Configure Multi-AZ and Read Replicas** — Enable multi-AZ for automatic failover (required for production). Add read replicas when read traffic exceeds primary capacity, distributing read load across replica instances.
   **Checkpoint:** Ensure the VPC has subnets across at least two availability zones with private networking.

3. **Set Up Security Group and IAM Authentication** — Attach a security group that restricts inbound access to application subnets only (never 0.0.0.0/0 for production). Enable IAM database authentication to eliminate password storage.
   **Checkpoint:** Verify security group rules use explicit CIDR blocks from your VPC, not wildcard addresses.

4. **Configure Automated Backup and Monitoring** — Set backup retention period (minimum 7 days), enable CloudWatch enhanced monitoring at 60-second intervals, and create alarms for CPU utilization, free storage, and replica lag.
   **Checkpoint:** Verify that backup window does not overlap with peak production hours.

5. **Deploy Using IaC (CloudFormation or Terraform)** — Define the RDS instance, subnet group, parameter group, and security group in infrastructure-as-code. Use tags for cost allocation and resource tracking.
   **Checkpoint:** The deployment must be idempotent — applying it twice should produce no unintended changes.

---

## Implementation Patterns

### Pattern 1: Provisioning a PostgreSQL RDS Instance with Boto3

```python
import boto3
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def provision_rds_instance(
    client: boto3.client,
    db_identifier: str,
    engine: str = "postgres",
    engine_version: str = "16.4",
    instance_class: str = "db.r6g.xlarge",
    storage_gb: int = 100,
    multi_az: bool = True,
    kms_key_arn: Optional[str] = None,
    subnet_group_name: str = "app-db-subnet-group",
    security_group_ids: list[str] | None = None,
) -> dict:
    """Provision an RDS database instance with production-ready configuration.

    Args:
        client: Boto3 RDS client instance.
        db_identifier: Unique identifier for the DB instance.
        engine: Database engine (postgres, mysql, mariadb).
        engine_version: Specific engine version to deploy.
        instance_class: EC2 instance class for the DB instance.
        storage_gb: Allocated storage in GiB.
        multi_az: Enable multi-AZ deployment for failover.
        kms_key_arn: ARN of KMS key for encryption at rest.
        subnet_group_name: Name of the DB subnet group.
        security_group_ids: List of security group IDs to attach.

    Returns:
        Dict with DB instance metadata including Endpoint and Status.
    """
    if security_group_ids is None:
        security_group_ids = []

    params: dict = {
        "DBInstanceIdentifier": db_identifier,
        "Engine": engine,
        "EngineVersion": engine_version,
        "DBInstanceClass": instance_class,
        "AllocatedStorage": storage_gb,
        "StorageType": "gp3",
        "MultiAZ": multi_az,
        "BackupRetentionPeriod": 7,
        "PreferredBackupWindow": "03:00-04:00",
        "PubliclyAccessible": False,
        "Tags": [
            {"Key": "Environment", "Value": "production"},
            {"Key": "ManagedBy", "Value": "terraform"},
        ],
    }

    # Enable encryption if KMS key is provided
    if kms_key_arn:
        params["StorageEncrypted"] = True
        params["KmsKeyId"] = kms_key_arn

    try:
        response = client.create_db_instance(**params)
        logger.info("RDS instance creation initiated: %s", db_identifier)
        return response["DBInstance"]
    except client.exceptions.InvalidParameterCombination as e:
        logger.error("Invalid parameter combination for RDS: %s", e)
        raise
    except client.exceptions.StorageLimitExceeded as e:
        logger.error("Storage limit exceeded: %s", e)
        raise


def create_read_replica(
    client: boto3.client,
    source_identifier: str,
    replica_identifier: str,
    instance_class: Optional[str] = None,
    kms_key_arn: Optional[str] = None,
) -> dict:
    """Create a read replica from an existing RDS instance.

    Args:
        client: Boto3 RDS client.
        source_identifier: Source DB instance identifier.
        replica_identifier: Name for the new read replica.
        instance_class: Override instance class (defaults to source).
        kms_key_arn: KMS key ARN for encryption at rest.

    Returns:
        Dict with read replica metadata.
    """
    params = {
        "DBInstanceIdentifier": replica_identifier,
        "SourceDBInstanceIdentifier": source_identifier,
    }

    if instance_class:
        params["DBInstanceClass"] = instance_class
    if kms_key_arn:
        params["StorageEncrypted"] = True
        params["KmsKeyId"] = kms_key_arn

    try:
        response = client.create_db_read_replica(**params)
        logger.info("Read replica created from %s: %s", source_identifier, replica_identifier)
        return response["DBInstance"]
    except client.exceptions.DBInstanceNotFoundFault as e:
        logger.error("Source DB instance not found: %s", e)
        raise
```

### Pattern 2: Terraform Module for Production-Grade PostgreSQL RDS

```terraform
# modules/rds-postgresql/main.tf
resource "aws_db_instance" "postgres" {
  identifier         = var.db_identifier
  engine             = "postgres"
  engine_version     = var.engine_version
  instance_class     = var.instance_class
  allocated_storage  = var.storage_gb
  storage_type       = "gp3"
  storage_encrypted  = true
  kms_key_id         = aws_kms_key.rds.arn
  multi_az           = true

  # Networking
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  # Backup & Recovery
  backup_retention_period = 7
  preferred_backup_window = "03:00-04:00"
  copy_tags_to_snapshot = true
  deletion_protection   = true

  # Monitoring
  performance_insights_enabled = true
  monitoring_interval          = 60
  monitoring_role_arn          = aws_iam_role.rds_monitor.arn

  # Parameters
  parameter_group_name = aws_db_parameter_group.main.name

  # IAM Authentication
  iam_database_authentication_enabled = true

  # Tags
  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
    Team        = var.team
  }

  skip_final_snapshot = false
  final_snapshot_identifier = "${var.db_identifier}-final-${timestamp()}"
}

resource "aws_db_subnet_group" "main" {
  name       = var.subnet_group_name
  subnet_ids = var.private_subnet_ids
}

resource "aws_security_group" "rds" {
  name_prefix = "${var.db_identifier}-sg-"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = var.app_cidr_blocks
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_kms_key" "rds" {
  description             = "KMS key for ${var.db_identifier} encryption at rest"
  deletion_window_in_days = 7
  enable_key_rotation     = true
}
```

## Constraints

### MUST DO
- Configure all AWS resources with explicit tagging for cost allocation, ownership tracking, and compliance
- Use AWS SDK (Boto3) typed clients instead of resource API where type safety matters — prefer client() over resource()
- Implement error handling that distinguishes between retryable (Throttling, RequestLimitExceeded) and non-retryable errors
- Use IAM roles with least-privilege policies scoped to specific actions and resources, never wildcard permissions

### MUST NOT DO
- Do not hardcode AWS credentials — use IAM roles, environment variables, or AWS Secrets Manager
- Avoid unencrypted S3 buckets or RDS instances in production without explicit KMS encryption configuration
- Never launch EC2 instances without specifying a security group and subnet — always use VPC networking explicitly
- Do not use the default endpoint region — always specify the target region explicitly in all SDK calls

### MUST DO
- Configure all AWS resources with explicit tagging for cost allocation, ownership tracking, and compliance
- Use AWS SDK (Boto3) typed clients instead of resource API where type safety matters — prefer client() over resource()
- Implement error handling that distinguishes between retryable (Throttling, RequestLimitExceeded) and non-retryable errors
- Use IAM roles with least-privilege policies scoped to specific actions and resources, never wildcard permissions

### MUST NOT DO
- Do not hardcode AWS credentials — use IAM roles, environment variables, or AWS Secrets Manager
- Avoid unencrypted S3 buckets or RDS instances in production without explicit KMS encryption configuration
- Never launch EC2 instances without specifying a security group and subnet — always use VPC networking explicitly
- Do not use the default endpoint region — always specify the target region explicitly in all SDK calls


## Live References

> Authoritative documentation links for this skill's domain. The model follows markdown links at load time to resolve external references and inline content.

- [Primary Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.html)
- [API Reference or Getting Started](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CreateDatabaseInstance.html)
- [Configuration Guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html)
- [Best Practices](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.AmazonRDS.CommonIssues.html)
- [Common Patterns or Tutorials](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html)