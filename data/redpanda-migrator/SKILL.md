---
name: redpanda-migrator
description: Generate Redpanda Migrator YAML configuration files for migrating data between Kafka-compatible clusters. Use when users request migration configurations for Kafka, Redpanda, Confluent Cloud, AWS MSK, or other Kafka-compatible systems. Handles data migration, schema migration, consumer offset translation, ACL migration, and topic filtering scenarios.
---

# Redpanda Migrator Configuration Generator

Generate Redpanda Migrator YAML configurations for migrating data, schemas, consumer groups, and ACLs between Kafka-compatible clusters.

## Core Workflow

When a user requests a Redpanda Migrator configuration:

1. **Gather Requirements** - Ask targeted questions to understand the migration scenario
2. **Load Reference Documentation** - Read `references/config-spec.md` for complete field specifications
3. **Generate Configuration** - Create a valid YAML configuration based on requirements
4. **Validate and Explain** - Ensure all required fields are present and explain key settings

## Gathering Requirements

Always ask these questions to build the configuration:

### Deployment Type (Ask First)

**Critical Question:**
- **Redpanda Connect deployment type:** Redpanda Cloud, Redpanda Serverless, Local, or Custom?
  - If Redpanda Cloud or Redpanda Serverless: Use environment variable secrets for credentials
  - If Local or Custom: Use direct credentials in configuration

**Important:** This determines whether credentials should be:
- **Cloud/Serverless**: Stored as secrets (${SECRET_NAME} format)
- **Local/Custom**: Embedded directly in YAML

### Source and Destination Clusters

**Required Information:**
- Source cluster type: Apache Kafka, Redpanda, Confluent Cloud, AWS MSK, Azure Event Hubs, or other
- Destination cluster type: same options as source
- Bootstrap servers for both clusters (format: `host:port`)

**Authentication (ask if not provided):**
- Authentication method: SASL/PLAIN, SASL/SCRAM-SHA-256, SASL/SCRAM-SHA-512, AWS_MSK_IAM, or none
- TLS/SSL enabled: yes/no
- If authentication required: credentials will be needed (username/password or IAM role)

### Migration Scope

**Ask the user:**
- Data migration: yes/no
- Schema migration: yes/no (requires Schema Registry URLs)
- Consumer offset translation: yes/no
- ACL migration: yes/no

### Topic and Schema Filtering

**Ask the user:**
- Migrate all topics or filter specific topics?
  - If filtering: provide topic patterns (regex) or specific topic names
  - Common pattern: `^[^_]` (excludes internal topics starting with `_`)
- Migrate all schemas or filter specific subjects?
  - If filtering: provide subject inclusion/exclusion patterns

### Replication Settings

**Ask the user:**
- Keep source cluster replication factor or override?
  - If override: specify new replication factor

### Additional Configuration

**Optional questions (ask if relevant):**
- Consumer group name for the migrator (default: `migrator_bundle`)
- Start from oldest messages or latest? (default: oldest)
- Include soft-deleted schemas? (default: true)
- Max in-flight messages for ordering preservation? (default: 1)

## Configuration Generation Process

After gathering requirements:

1. **Read the complete config specification:**
   ```
   file_read: references/config-spec.md
   ```

2. **Generate the YAML** using the template structure from config-spec.md

3. **Include these essential sections:**
   - `input.redpanda_migrator_bundle.redpanda_migrator` - source cluster config
   - `input.redpanda_migrator_bundle.schema_registry` - source schema registry (if schema migration enabled)
   - `output.redpanda_migrator_bundle.redpanda_migrator` - destination cluster config
   - `output.redpanda_migrator_bundle.schema_registry` - destination schema registry (if schema migration enabled)
   - `metrics.prometheus` - monitoring configuration

4. **Apply user requirements:**
   - Set seed_brokers for source and destination
   - Configure authentication (SASL, TLS)
   - Set topic filters
   - Configure schema registry if needed
   - Enable/disable consumer offset translation
   - Enable/disable ACL migration
   - Set replication factor override

5. **Add comments** explaining critical settings like:
   - Topic filtering patterns
   - Authentication configuration
   - Max in-flight for ordering
   - Consumer group offset translation behavior

## Common Migration Scenarios

Reference these patterns for typical requests:

**Kafka to Redpanda Cloud:**
- Source: Apache Kafka with standard authentication
- Destination: Redpanda Cloud with SASL/SCRAM-SHA-256
- Usually includes: data + schemas + consumer offsets + ACLs

**AWS MSK to Redpanda Cloud:**
- Source: AWS MSK with SCRAM-SHA-512 or IAM authentication
- Destination: Redpanda Cloud Dedicated with SASL/SCRAM-SHA-256
- Usually includes: data + consumer offsets, optional schema migration
- May need `topic_replication_factor` override
- Use `enable_renegotiation: true` for TLS if needed

**Confluent Cloud to Redpanda Cloud:**
- Source: Confluent Cloud with PLAIN authentication (API keys)
- Destination: Redpanda Cloud with SASL/SCRAM-SHA-256
- Requires `enable_renegotiation: true` for Confluent Cloud TLS
- Usually data-only, no schema migration
- Fast consumer offset sync (`interval: 10s`)

**Redpanda Dedicated to Redpanda Serverless:**
- Source: Redpanda Cloud Dedicated (.fmc.prd.cloud.redpanda.com)
- Destination: Redpanda Cloud Serverless (.mpx.prd.cloud.redpanda.com)
- **CRITICAL**: Set `serverless: true` in output
- Use `consumer_groups.exclude` to filter internal consumer groups
- Both data-only and data+schema migrations supported
- Full TLS and authentication for both clusters

**Redpanda to Redpanda (Data-Only):**
- Source: Redpanda cluster (local or BYOC)
- Destination: Another Redpanda cluster
- Data only with consumer offset translation
- Use `metadata_max_age: 30s` for faster regex topic discovery
- Configure `consumer_groups.interval` for offset sync frequency
- Disable schema registry with `enabled: false`

**Redpanda to Redpanda (with Schemas):**
- Source: Redpanda cluster with Schema Registry
- Destination: Another Redpanda cluster with Schema Registry
- One-time schema sync: Set `enabled: true` (no interval)
- Periodic schema sync: Set `interval: 10s` or desired frequency
- Use `versions: latest` for faster migration or `versions: all` for full history
- Filter schemas with `include` or `exclude` patterns

**Data-only migration:**
- Minimal config with just data streaming
- No schema registry configuration (or explicitly disabled)
- Consumer offset translation optional
- ACL migration disabled

## Important Notes

- **Message Ordering:** The Redpanda Migrator automatically preserves message ordering at the partition level (max_in_flight=1 is hardcoded)
- **Secrets Management:** When deploying to Redpanda Cloud or Serverless, always use environment variable secrets for credentials
  - Format: `${SECRET_NAME}` instead of plain text values
  - Required for: seed_brokers, username, password, schema_registry URLs
  - Documentation: https://docs.redpanda.com/redpanda-cloud/develop/connect/configuration/secret-management/
- **Schema Registry Mode:** Destination Schema Registry must be in READWRITE or IMPORT mode
- **Consumer Group Offsets:** Require identical partition counts between source and destination
- **ACL Safety:** ALLOW WRITE permissions are excluded, ALLOW ALL is downgraded to ALLOW READ
- **Topic Creation:** Destination topics are created automatically if they don't exist
- **Monitoring:** The `input_redpanda_migrator_lag` metric tracks migration progress

## Secrets Management for Cloud Deployments

When Redpanda Connect deployment type is **Redpanda Cloud** or **Redpanda Serverless**, use environment variable secrets for all sensitive credentials.

### Standard Secret Names by Platform

**Redpanda Cloud/Serverless:**
- `${REDPANDA_BROKERS}` - Seed brokers
- `${REDPANDA_USER}` - Username
- `${REDPANDA_USER_PWD}` - Password

**Confluent Cloud:**
- `${CC_BROKERS}` - Bootstrap brokers
- `${CC_USER}` - API key (username)
- `${CC_USER_PWD}` - API secret (password)

**AWS MSK / Custom Kafka:**
- `${KAFKA_BROKERS}` - Bootstrap brokers
- `${KAFKA_USER}` - Username
- `${KAFKA_USER_PWD}` - Password

### Example: Redpanda Cloud to Redpanda Cloud

```yaml
input:
  redpanda_migrator:
    seed_brokers: ["${REDPANDA_BROKERS}"]
    sasl:
      - mechanism: "SCRAM-SHA-256"
        username: "${REDPANDA_USER}"
        password: "${REDPANDA_USER_PWD}"
    tls:
      enabled: true

output:
  redpanda_migrator:
    seed_brokers: ["${REDPANDA_BROKERS}"]
    sasl:
      - mechanism: "SCRAM-SHA-256"
        username: "${REDPANDA_USER}"
        password: "${REDPANDA_USER_PWD}"
    tls:
      enabled: true
```

### Example: Confluent Cloud to Redpanda Cloud

```yaml
input:
  redpanda_migrator:
    seed_brokers: ["${CC_BROKERS}"]
    sasl:
      - mechanism: "PLAIN"
        username: "${CC_USER}"
        password: "${CC_USER_PWD}"
    tls:
      enabled: true
      enable_renegotiation: true

output:
  redpanda_migrator:
    seed_brokers: ["${REDPANDA_BROKERS}"]
    sasl:
      - mechanism: "SCRAM-SHA-256"
        username: "${REDPANDA_USER}"
        password: "${REDPANDA_USER_PWD}"
    tls:
      enabled: true
```

### Example: Custom Kafka to Redpanda Cloud

```yaml
input:
  redpanda_migrator:
    seed_brokers: ["${KAFKA_BROKERS}"]
    sasl:
      - mechanism: "SCRAM-SHA-512"
        username: "${KAFKA_USER}"
        password: "${KAFKA_USER_PWD}"
    tls:
      enabled: true

output:
  redpanda_migrator:
    seed_brokers: ["${REDPANDA_BROKERS}"]
    sasl:
      - mechanism: "SCRAM-SHA-256"
        username: "${REDPANDA_USER}"
        password: "${REDPANDA_USER_PWD}"
    tls:
      enabled: true
```

### Creating Secrets in Redpanda Cloud

When deployment type is Redpanda Cloud or Serverless:

1. **Create secrets** in Redpanda Cloud Console or via CLI
2. **Reference secrets** using `${SECRET_NAME}` format in configuration
3. **Never use plain text** credentials in Cloud/Serverless deployments

**Documentation:** https://docs.redpanda.com/redpanda-cloud/develop/connect/configuration/secret-management/

### Local vs Cloud Configuration

**Local/Custom Deployment:**
```yaml
seed_brokers: ["localhost:9092"]
username: "admin"
password: "admin-password"
```

**Cloud/Serverless Deployment:**
```yaml
seed_brokers: ["${REDPANDA_BROKERS}"]
username: "${REDPANDA_USER}"
password: "${REDPANDA_USER_PWD}"
```

### Advanced Configuration Options

- **metadata_max_age:** Controls how often regex topic patterns are re-evaluated (default: 5m)
  - Reduce to `30s` or `1m` for faster discovery of newly created topics
  - Lower values = more frequent metadata refreshes = more broker queries
  
- **consumer_groups.interval:** Sync frequency for consumer group offsets
  - Can be boolean `true` (default behavior) or object with `interval` field
  - Example: `consumer_groups: { interval: 1m }` syncs offsets every minute
  - Recommended: 1m to 10m depending on lag tolerance
  
- **consumer_groups.exclude:** Filter consumer groups from migration
  - List of regex patterns to exclude internal/system consumer groups
  - Essential for Redpanda Cloud migrations (console, connect, kminion groups)
  - Example: `exclude: ["console-consumer-.*", "__.*", "connect.*"]`
  
- **schema_registry.enabled:** Explicitly enable/disable schema migration
  - Set to `false` for data-only migrations even when URL is configured
  - Useful when schema registry exists but migration not needed
  
- **schema_registry.interval:** Periodic schema synchronization
  - Without this field: One-time sync on startup
  - With interval (e.g., `10s`): Continuous sync for ongoing schema updates
  - Use for active schema evolution during migration
  
- **schema_registry.versions:** Schema version migration strategy
  - `all`: Migrate complete version history (DEFAULT - recommended for production)
  - `latest`: Migrate only the latest version (faster, less history)
  - When combined with `interval`: `latest` captures new versions as they become latest
  
- **schema_registry.include:** Filter schemas by subject patterns
  - List of regex patterns to include specific schema subjects
  - Only matching subjects will be migrated
  - Example: `include: ["orders.*", "users.*"]`
  
- **schema_registry.exclude:** Exclude schemas by subject patterns
  - List of regex patterns to exclude schema subjects
  - Takes precedence over `include` patterns
  - Example: `exclude: [".*test.*", ".*temp.*"]`
  
- **schema_registry.normalize:** Schema normalization
  - Set to `true` to transform schemas to canonical format
  - Collapses semantically identical but syntactically different schemas
  - Prevents duplicate registrations from formatting differences
  - Use when source has inconsistent schema formatting
  
- **serverless:** Required flag for Redpanda Cloud Serverless
  - **MUST** be set to `true` when destination is Serverless
  - Applies serverless-specific configurations and restrictions
  
- **topic_replication_factor:** Override replication factor for new topics
  - Useful when source/destination have different replication requirements
  - Example: MSK RF=2 to Redpanda RF=3
  
- **enable_renegotiation:** TLS renegotiation support
  - Set to `true` for Confluent Cloud compatibility
  - Required for some cloud providers' TLS implementations
  
- **logger.level:** Set log verbosity (TRACE, DEBUG, INFO, WARN, ERROR)
  - Use `DEBUG` for troubleshooting migration issues
  - Use `INFO` (default) for normal operation

## Example Output Format

Always output the complete YAML configuration with:
- Clear section headers (as YAML comments)
- Inline comments for critical settings
- Proper YAML indentation (2 spaces)
- All required fields populated
- Optional fields commented with defaults when relevant

After generating the configuration, explain:
- How to run it: `redpanda-connect run <filename>.yaml`
- What the configuration will do
- Any prerequisites (Schema Registry mode, network access, credentials)
- How to monitor progress (prometheus metrics)
