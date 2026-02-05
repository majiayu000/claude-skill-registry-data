---
name: duckdb-alb-log-analyzer
description: Analyze AWS Application Load Balancer (ALB) logs stored in S3 using DuckDB. Use when users request ALB log analysis, error investigation, performance analysis, traffic analysis, or need to query ALB access logs. Supports analyzing response times, status codes, error patterns, and traffic trends from S3-stored logs.
---

# ALB Log Analyzer

Analyze AWS Application Load Balancer (ALB) logs using DuckDB for fast, flexible S3-based queries.

## Quick Start

### Secure Method (Recommended for Named Profiles)

For AWS named profiles, use these secure scripts that keep credentials private:

```bash
# One-time setup (credentials read from ~/.aws/credentials)
./scripts/setup_with_profile.sh your-profile-name

# Load logs (profile name only, credentials stay secure)
./scripts/load_with_profile.sh your-profile-name 's3://bucket/path/**/*.log.gz'

# Analyze
./scripts/analyze.sh errors
./scripts/analyze.sh performance
```

**Security**: Only profile names appear in commands and logs. Credentials are read internally from `~/.aws/credentials`.

### Standard Method

Basic workflow for ALB log analysis:

1. Setup DuckDB with AWS extensions
2. Load logs from S3 into a table
3. Run analysis queries (errors, performance, traffic, etc.)
4. Export results or create custom queries

## Prerequisites

Ensure DuckDB is installed:

```bash
# Install DuckDB (if not already installed)
brew install duckdb  # macOS
# or download from https://duckdb.org/docs/installation/
```

AWS credentials must be configured. See **AWS Credentials Setup** section below for details.

## Database File Location

By default, the DuckDB database file is stored at:
```
/tmp/alb-log-analyzer-${USER}/alb_analysis.duckdb
```

**Important**: The database file is automatically deleted when you run `setup` or `load` commands. This ensures:
- Clean start with each analysis
- No accumulation of old data in /tmp
- Reduced disk space usage

This temporary location also:
- Keeps your skill directory clean
- Prevents data from being packaged with the skill
- May be cleared on system restart

To use a custom location, set the `DB_FILE` environment variable:
```bash
export DB_FILE=/path/to/custom/database.duckdb
```

## Setup

### Method 1: Using CREDENTIAL_CHAIN (Recommended)

This method automatically detects AWS credentials from environment variables, ~/.aws/credentials, or IAM roles:

```bash
./scripts/analyze.sh setup
```

### Method 2: Using Environment Variables

If CREDENTIAL_CHAIN doesn't work, explicitly set environment variables.

**For default profile:**

```bash
# Set AWS credentials
export AWS_ACCESS_KEY_ID=your_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=ap-northeast-1

# Setup DuckDB
./scripts/analyze.sh setup-env
```

**For named profile:**

```bash
# Export credentials from your profile
export AWS_PROFILE=your-profile-name
export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id --profile your-profile-name)
export AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key --profile your-profile-name)
export AWS_DEFAULT_REGION=$(aws configure get region --profile your-profile-name)

# Setup DuckDB
./scripts/analyze.sh setup-env
```

### Method 3: Manual SQL

```bash
duckdb alb_analysis.duckdb < scripts/setup.sql
# or
duckdb alb_analysis.duckdb < scripts/setup_s3_env.sql
```

### Verify Setup

Diagnose your AWS credentials configuration:

```bash
./scripts/analyze.sh diagnose
```

This will show:
- Extension installation status
- Environment variable configuration
- Configured secrets in DuckDB

## AWS Credentials Setup

DuckDB needs AWS credentials to access S3. Choose one of these methods:

### Option 1: AWS CLI Configuration (Recommended)

If you have AWS CLI configured, DuckDB can use those credentials:

```bash
# Check if AWS CLI is configured
aws s3 ls

# If not configured, run:
aws configure
```

### Option 2: Environment Variables

Export credentials in your shell:

```bash
export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
export AWS_DEFAULT_REGION=ap-northeast-1
```

### Option 3: AWS Credentials File

Create or edit `~/.aws/credentials`:

```ini
[default]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

And `~/.aws/config`:

```ini
[default]
region = ap-northeast-1
```

### Option 4: AWS Profile (For Named Profiles)

If you're using a named AWS profile (not `[default]`), you need to explicitly export the credentials.

**Easy way (using helper script):**

```bash
# List available profiles
aws configure list-profiles

# Load credentials from your profile
source scripts/load_profile.sh your-profile-name

# Setup and use
./scripts/analyze.sh setup-env
./scripts/analyze.sh load 's3://your-bucket/path/**/*.log.gz'
```

**Manual way:**

```bash
# Check your profiles
aws configure list-profiles

# Export credentials from your profile
export AWS_PROFILE=your-profile-name
export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id --profile your-profile-name)
export AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key --profile your-profile-name)
export AWS_DEFAULT_REGION=$(aws configure get region --profile your-profile-name)

# Setup DuckDB with these credentials
./scripts/analyze.sh setup-env

# Load logs
./scripts/analyze.sh load 's3://your-bucket/path/**/*.log.gz'
```

**Why this is needed**: DuckDB doesn't automatically read from named AWS profiles. It only supports environment variables or the `[default]` profile. By exporting the profile's credentials as environment variables, DuckDB can access them.

### Option 5: IAM Role (EC2/ECS)

If running on EC2 or ECS, DuckDB can use the instance's IAM role automatically.

## Loading Logs

Load ALB logs from S3 into a DuckDB table.

### Using the analyze.sh script

```bash
# Load logs from S3
./scripts/analyze.sh load 's3://my-bucket/AWSLogs/123456789012/elasticloadbalancing/us-east-1/2024/11/**/*.log.gz'
```

### Manual SQL approach

1. Generate SQL from template:

```bash
# Replace placeholders
sed -e "s|{{TABLE_NAME}}|alb_logs|g" \
    -e "s|{{S3_PATH}}|s3://my-bucket/path/to/logs/**/*.log.gz|g" \
    scripts/load_template.sql > load_logs.sql
```

2. Execute:

```bash
duckdb alb_analysis.duckdb < load_logs.sql
```

### S3 Path Patterns

Use glob patterns to load multiple files:

```
# Single month
s3://bucket/AWSLogs/account-id/elasticloadbalancing/region/2024/11/**/*.log.gz

# Multiple months
s3://bucket/AWSLogs/account-id/elasticloadbalancing/region/2024/*/**/*.log.gz

# Specific day
s3://bucket/AWSLogs/account-id/elasticloadbalancing/region/2024/11/01/**/*.log.gz
```

## Analysis Tasks

### Error Analysis

Analyze HTTP errors, status code distributions, and error patterns:

```bash
./scripts/analyze.sh errors
```

This provides:
- Status code distribution
- Error details (non-200 responses)
- 5xx errors by hour
- Common error reasons

### Performance Analysis

Analyze response times and latency:

```bash
./scripts/analyze.sh performance
```

This provides:
- Response time statistics (avg, p50, p95, p99)
- Slowest requests
- Response time trends by hour
- Slow request percentage

### Custom Queries

Execute custom SQL queries:

```bash
# Using a custom SQL file
./scripts/analyze.sh query my_query.sql

# Or directly with DuckDB
duckdb alb_analysis.duckdb
```

## Common Analysis Patterns

### Find requests from specific IP

```sql
SELECT *
FROM alb_logs
WHERE client_ip_port LIKE '192.168.1.%'
ORDER BY timestamp DESC;
```

### Analyze specific URL path

```sql
SELECT
    elb_status_code,
    COUNT(*) as count,
    ROUND(AVG(target_processing_time), 3) as avg_time
FROM alb_logs
WHERE request LIKE '%/api/users%'
GROUP BY elb_status_code;
```

### Traffic by time of day

```sql
SELECT
    EXTRACT(HOUR FROM timestamp) as hour,
    COUNT(*) as request_count
FROM alb_logs
GROUP BY hour
ORDER BY hour;
```

### Filter by date range

```sql
SELECT *
FROM alb_logs
WHERE timestamp BETWEEN '2024-11-01' AND '2024-11-30'
AND elb_status_code >= 500;
```

## Advanced Usage

### Create aggregated summaries

```sql
CREATE TABLE daily_summary AS
SELECT
    DATE_TRUNC('day', timestamp) as day,
    COUNT(*) as total_requests,
    SUM(CASE WHEN elb_status_code >= 500 THEN 1 ELSE 0 END) as errors_5xx,
    ROUND(AVG(target_processing_time), 3) as avg_response_time
FROM alb_logs
GROUP BY day;
```

### Export results

```sql
-- Export to CSV
COPY (SELECT * FROM alb_logs WHERE elb_status_code >= 500)
TO 'errors.csv' (HEADER, DELIMITER ',');

-- Export to Parquet
COPY alb_logs TO 'alb_logs.parquet' (FORMAT PARQUET);
```

### Multiple table analysis

Load logs into separate tables for comparison:

```bash
# Load last week's logs
sed -e "s|{{TABLE_NAME}}|alb_logs_last_week|g" \
    -e "s|{{S3_PATH}}|s3://bucket/logs/2024/10/**/*.log.gz|g" \
    scripts/load_template.sql | duckdb alb_analysis.duckdb

# Compare with this week
SELECT
    'last_week' as period,
    COUNT(*) as requests,
    AVG(target_processing_time) as avg_time
FROM alb_logs_last_week
UNION ALL
SELECT
    'this_week' as period,
    COUNT(*) as requests,
    AVG(target_processing_time) as avg_time
FROM alb_logs;
```

## Troubleshooting

### S3 Access Issues

If you get "Access Denied" or credential errors when loading from S3:

**Step 1: Diagnose the issue**

```bash
./scripts/analyze.sh diagnose
```

This shows your AWS credential configuration status.

**Step 2: Verify AWS credentials work**

Test with AWS CLI:

```bash
aws s3 ls s3://your-bucket/path/to/logs/
```

If this fails, fix your AWS credentials first.

**Step 3: Try different setup methods**

**3a. If using default AWS profile:**

```bash
# Set credentials
export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
export AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
export AWS_DEFAULT_REGION=$(aws configure get region)

# Setup DuckDB with environment variables
./scripts/analyze.sh setup-env

# Try loading again
./scripts/analyze.sh load 's3://your-bucket/path/**/*.log.gz'
```

**3b. If using a named AWS profile:**

```bash
# Check which profile you're using
aws configure list-profiles

# Replace 'your-profile-name' with your actual profile
export AWS_PROFILE=your-profile-name
export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id --profile your-profile-name)
export AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key --profile your-profile-name)
export AWS_DEFAULT_REGION=$(aws configure get region --profile your-profile-name)

# Setup DuckDB with environment variables
./scripts/analyze.sh setup-env

# Try loading again
./scripts/analyze.sh load 's3://your-bucket/path/**/*.log.gz'
```

**Step 4: Alternative - Load from local files**

If S3 access still doesn't work, download logs locally:

```bash
# Download logs from S3
aws s3 sync s3://your-bucket/path/to/logs/ ./local-logs/

# Modify load_template.sql to use local path
sed -e "s|{{TABLE_NAME}}|alb_logs|g" \
    -e "s|{{S3_PATH}}|./local-logs/**/*.log.gz|g" \
    scripts/load_template.sql | duckdb alb_analysis.duckdb
```

### "Extension aws not found"

Run setup script first:

```bash
./scripts/analyze.sh setup
```

Or manually:

```bash
duckdb alb_analysis.duckdb < scripts/setup.sql
```

### "Invalid Input Error" when loading

This usually means the S3 path pattern doesn't match any files:

```bash
# Check if files exist
aws s3 ls --recursive s3://your-bucket/path/to/logs/ | head

# Verify the path pattern matches your bucket structure
# ALB logs are typically at:
# s3://bucket/AWSLogs/{account-id}/elasticloadbalancing/{region}/{year}/{month}/{day}/*.log.gz
```

### Empty results after loading

```bash
# Check table contents
duckdb alb_analysis.duckdb -c "SELECT COUNT(*) FROM alb_logs"

# If 0, verify S3 path and try loading again
```

### Out of memory

Use persistent database instead of `:memory:`:

```bash
# Already using persistent storage by default
# alb_analysis.duckdb is a file-based database
```

### Permission errors on scripts

```bash
chmod +x scripts/analyze.sh
```

### Region-specific issues

Ensure the region matches your S3 bucket:

```bash
export AWS_DEFAULT_REGION=ap-northeast-1  # Change to your region
./scripts/analyze.sh setup-env
```

## References

### ALB Log Schema

See [references/alb_schema.md](references/alb_schema.md) for complete field definitions and data types.

Key fields:
- `timestamp`: Request timestamp
- `elb_status_code`: HTTP status from ALB
- `target_status_code`: HTTP status from target
- `request`: Full HTTP request line
- `target_processing_time`: Response time from target
- `client_ip_port`: Client address and port
- `target_ip_port`: Target address and port
- `error_reason`: Error details if applicable
- `transformed_host`, `transformed_uri`, `request_transform_status`: Request transformation fields

### Query Examples

See [references/query_examples.md](references/query_examples.md) for comprehensive query examples including:
- Error analysis queries
- Performance metrics
- Traffic analysis
- SSL/TLS analysis
- Data export patterns

## Scripts Reference

### analyze.sh

Main analysis script with subcommands:

```bash
# Setup (uses CREDENTIAL_CHAIN)
./scripts/analyze.sh setup

# Setup with environment variables (if CREDENTIAL_CHAIN doesn't work)
./scripts/analyze.sh setup-env

# Diagnose S3 access and credentials
./scripts/analyze.sh diagnose

# Load logs
./scripts/analyze.sh load '<s3_path>'

# Analyze errors
./scripts/analyze.sh errors

# Analyze performance
./scripts/analyze.sh performance

# Custom query
./scripts/analyze.sh query <sql_file>

# Options
--db <file>      # Database file (default: alb_analysis.duckdb)
--table <name>   # Table name (default: alb_logs)
```

### setup_with_profile.sh (Secure - Recommended)

Securely setup DuckDB with AWS profile. Credentials are read internally and never exposed in commands:

```bash
# Usage
./scripts/setup_with_profile.sh your-profile-name

# Security: Only profile name is visible, credentials read from ~/.aws/credentials
```

**Security advantage**: Credentials stay private. Only profile names appear in command history and logs.

### load_with_profile.sh (Secure - Recommended)

Securely load logs with AWS profile. Credentials are read internally and never exposed in commands:

```bash
# Usage
./scripts/load_with_profile.sh your-profile-name 's3://bucket/path/**/*.log.gz' [table_name]

# Security: Only profile name and S3 path are visible
```

**Security advantage**: Credentials stay private. Only profile names appear in command history and logs.

### load_profile.sh (Legacy - For Manual Setup)

Helper script to load AWS credentials from a named profile into environment variables:

```bash
# Usage
source scripts/load_profile.sh your-profile-name

# This exports:
# - AWS_PROFILE
# - AWS_ACCESS_KEY_ID
# - AWS_SECRET_ACCESS_KEY
# - AWS_DEFAULT_REGION
```

**Note**: Must be sourced (not executed) to export variables to your current shell.

**Security consideration**: This exports credentials to environment variables, which may be visible in process listings. Use `setup_with_profile.sh` and `load_with_profile.sh` for better security.

### SQL Files

- `setup.sql`: Initialize DuckDB extensions with CREDENTIAL_CHAIN
- `setup_s3_env.sql`: Initialize DuckDB extensions with environment variables
- `diagnose_s3.sql`: Diagnose AWS credentials and S3 access
- `load_template.sql`: Template for loading logs (requires variable substitution)
- `analyze_errors.sql`: Error analysis queries
- `analyze_performance.sql`: Performance analysis queries
