---
name: aws
description: |
  Use when working with Aws — mANDATORY parallel execution patterns (30x
  speedup), CloudWatch statistics syntax, Cost Explorer aggregation, output
  token limits, and common pitfalls.
connection_type: aws
preload: false
---

# AWS CLI Skill

Execute AWS CLI commands with proper credential injection.

## CLI Tips

### Parallel Execution Requirement (CRITICAL)

🚨 **CRITICAL PERFORMANCE REQUIREMENT - VIOLATION WILL REJECT THE SCRIPT** 🚨

**ALL independent operations MUST run in parallel using background jobs (&) and wait**

ENFORCEMENT RULES:

- **FORBIDDEN**: Sequential loops like `for item in $items; do cmd $item; done` (causes O(n) runtime)
- **MANDATORY**: Every independent operation spawns a background job: `{ cmd1 } & { cmd2 } & { cmd3 } & wait`
- **DETECTION**: If your script processes N resources/metrics/regions and N > 1, the script MUST contain at least N background jobs
- **TIME IMPACT**: Sequential execution with 30 instances x 2 seconds per call = 60 seconds. Parallel = 2 seconds (30x faster)
- **VALIDATION CHECKLIST** (agent must mentally verify before output):
  - Count independent operations: \_\_\_
  - Count background jobs (&): \_\_\_
  - These numbers MUST match, or script will be REJECTED
  - Do all operations depend on each other? (Only valid exception to parallel requirement)

PARALLEL PATTERN (CORRECT):

```bash
for instance in $instances; do
  operation "$instance" &  # ← Spawn as background job
done
wait  # ← Wait for all to complete
```

SEQUENTIAL PATTERN (FORBIDDEN - ONLY if operations have data dependencies):

```bash
result=$(operation1)
operation2 "$result"  # ← Only valid if operation2 requires operation1's output
```

### Agent Output Rules

- Output is for the agent to parse, not humans; keep it machine-friendly plain text
- Do not add decorative formatting, icons, borders, or echo-based separators
- Never print or expose environment variables, credentials, or AWS keys
- **TOKEN EFFICIENCY IS CRITICAL**: Output must be minimal and aggregated
  - Target ≤50 lines for any script output
  - Use `| head -N` to limit results (e.g., top 10 services)
  - Aggregate time-series data (daily → weekly/monthly totals)
  - If output would exceed 100 lines, the script is WRONG - aggregate more

### Execution Guidelines

- **PARALLEL EXECUTION IS MANDATORY**: See Parallel Execution Requirement for full rules
- **DISABLE PAGER IN SCRIPTS**: Add `export AWS_PAGER=""` at script start (AWS CLI v2 uses `less` by default)
- Produce actionable insights (e.g., "avg CPU 45%, peak 89%") instead of raw dumps
- Consolidate related steps into a single Bash script whenever feasible
- Use read-only commands only (list, describe, get)
- **CLOUDWATCH STATISTICS**: See CloudWatch Statistics Validation for syntax rules (space-separated, not commas)
- **FILTERING**: Use server-side --filters BEFORE client-side --query (see Filtering Hierarchy)
- **PAGINATION**: Use --page-size/--max-items for large datasets (see Pagination Guidelines)
- **STS ROLE ASSUMPTION**: If user requested to assume an AWS role, see STS Assume Role Pattern for detection, session management, and credential setup

### STS Assume Role Pattern

**STS ASSUME ROLE - Session-Wide Credential Management**

**DETECTION PATTERNS** (user requests to assume a role):

- "assume (the)? Role ARN arn:aws:iam::"
- "use (this|the) role for (this|the) session"
- "switch to role arn:aws:iam::"
- "AssumeRole with arn:aws:iam::"
- Any message containing a Role ARN with context suggesting assumption

**WHEN DETECTED - IMMEDIATE ACTIONS**:

1. Acknowledge the role assumption request
2. Extract the full Role ARN (format: arn:aws:iam::ACCOUNT_ID:role/ROLE_NAME)
3. Track in your reasoning: "ACTIVE_ASSUMED_ROLE: {role_arn}"
4. Inform user: "I'll use this assumed role for all AWS operations in this session until you ask me to stop."

**CONVERSATION CONTINUITY**:

- Check conversation history for prior role assumption requests
- If a role was assumed earlier and not cancelled, CONTINUE using it
- The assumed role persists across all turns until explicitly cancelled
- If you're unsure whether a role is active, check recent conversation context

**TERMINATION PATTERNS** (stop using assumed role):

- "stop using (the)? assumed role"
- "reset (to)? (original|default) credentials"
- "don't use the assumed role (anymore)?"
- "clear role assumption"
- "use my default credentials"

**SCRIPT PATTERN** - Use at the START of every Bash script when role assumption is active:

```bash
#!/bin/bash
export AWS_PAGER=""

# Assume role and export credentials (call ONCE at script start)
assume_role() {
    local role_arn="$1"
    local session_name="${2:-CloudThinkerSession}"

    CREDS=$(aws sts assume-role \
        --role-arn "$role_arn" \
        --role-session-name "$session_name" \
        --duration-seconds 3600 \
        --output text \
        --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]')

    if [ -z "$CREDS" ]; then
        echo "ERROR: Failed to assume role $role_arn" >&2
        exit 1
    fi

    export AWS_ACCESS_KEY_ID=$(echo "$CREDS" | cut -f1)
    export AWS_SECRET_ACCESS_KEY=$(echo "$CREDS" | cut -f2)
    export AWS_SESSION_TOKEN=$(echo "$CREDS" | cut -f3)
}

# Replace with the Role ARN from user's request
assume_role "arn:aws:iam::ACCOUNT_ID:role/ROLE_NAME"

# All subsequent AWS commands use the assumed role automatically
aws ec2 describe-instances --output text --query '...'
aws rds describe-db-instances --output text --query '...'
```

**CRITICAL RULES**:

- Call `assume_role` ONCE at script start, NOT before each command
- Credentials are exported as environment variables, subsequent commands inherit them
- Default session duration is 1 hour (3600 seconds)
- If multiple scripts run in same session, each needs its own assume_role call (env vars don't persist across script executions)

**ERROR HANDLING**:

- If assume-role fails, the script should exit with error message
- Common failures: invalid ARN, insufficient permissions, role trust policy
- On failure, inform user to verify the Role ARN and their permissions to assume it

**SECURITY REQUIREMENTS**:

- NEVER echo, print, or expose credential values in output
- NEVER include credentials in group_chat messages
- NEVER log AccessKeyId, SecretAccessKey, or SessionToken
- If credentials fail, inform user and request re-confirmation of the role ARN

### Output Format Strategy

- **DEFAULT TO `--output text --query`** for ALL commands - this is mandatory for token efficiency
- If you think you need JSON, first attempt the same result with --query and --output text
- Format as tab-delimited for easy parsing with awk/cut/sort
- `--output json` + jq is ONLY acceptable when:
  - --query cannot express the transformation (e.g., conditional logic, complex nested arrays)
  - The jq pipeline MUST end with text output: `| jq -r '... | @tsv'` or `| jq -r '... | "\(.field1)\t\(.field2)"'`
  - NEVER end jq pipelines with `| @json` or `| jq -s` that produces JSON
- **CRITICAL**: The final output to the agent must ALWAYS be plain text (tab/space delimited), never JSON
- When in doubt, use --output text

### Data Processing

- Filter at the API level using `--query` and service-specific filters first
- When post-processing, favor `awk` → `sed` → `cut` → `grep`; avoid jq for simple tasks
- If using `--output json` + jq, you MUST filter/reduce the data before output
- Allow stderr to surface; avoid patterns like `2>/dev/null | grep -E ...`
- Remember: `jq @csv` requires array input such as `[value1, value2] | @csv`
- **TOKEN EFFICIENCY**: Raw JSON dumps waste tokens; always extract only needed fields

### Filtering Hierarchy

**FILTERING ORDER MATTERS - Server-side first, client-side second**

1. **`--filter` / `--filters` (SERVER-SIDE)** - Use FIRST
   - AWS service filters data BEFORE sending HTTP response
   - Dramatically reduces network payload and response time
   - Syntax varies by service (--filter, --filters, --filter-expression)

2. **`--query` (CLIENT-SIDE)** - Use SECOND
   - AWS CLI filters AFTER receiving full HTTP response
   - Good for field selection and transformation --filter can't do
   - Still downloads full payload first

3. **awk/sed/cut (POST-PROCESSING)** - Use LAST
   - For final text formatting only

**PERFORMANCE IMPACT**:

- Server-side: AWS returns 10 matching records → 10 records transferred
- Client-side: AWS returns 10,000 records → filters to 10 → 10,000 records transferred

**EXAMPLES**:

```bash
# ❌ SLOW: Downloads ALL instances, filters client-side
aws ec2 describe-instances --query 'Reservations[].Instances[?State.Name==`running`]'

# ✅ FAST: Server returns only running instances (use --filters)
aws ec2 describe-instances --filters Name=instance-state-name,Values=running \
    --query 'Reservations[].Instances[].[InstanceId,InstanceType]' --output text

# ❌ SLOW: Downloads all security groups, filters by name client-side
aws ec2 describe-security-groups --query "SecurityGroups[?GroupName=='my-sg']"

# ✅ FAST: Server filters by name
aws ec2 describe-security-groups --filters Name=group-name,Values=my-sg \
    --query 'SecurityGroups[].[GroupId,GroupName]' --output text
```

**COMMON SERVICE FILTERS**:

- EC2: `--filters Name=key,Values=val1,val2`
- RDS: `--filters Name=key,Values=val`
- S3: No server-side filter (use --prefix for listing)
- CloudWatch: Namespace, dimensions are server-side; use --query for datapoints
- Cost Explorer: --filter parameter with JSON filter expression

### Pagination Guidelines

**PAGINATION FOR LARGE DATASETS - Prevent timeouts and memory issues**

**KEY PARAMETERS**:

- `--page-size N`: Items per API call (internal pagination, still returns all)
- `--max-items N`: Total items to return (stops early, provides NextToken)
- `--starting-token TOKEN`: Resume from NextToken

**WHEN TO USE**:

- Large resource lists (1000+ items): Add `--page-size 100` to prevent timeouts
- Top-N queries: Use `--max-items N` instead of fetching all then limiting
- Batch processing: Use `--starting-token` to iterate through pages

**CRITICAL WARNING WITH --output text**:
When using `--output text`, the `--query` filter runs PER PAGE, not on full dataset!
This causes unexpected results. Use `--output json` for full-dataset queries.

**EXAMPLES**:

```bash
# Get only first 20 instances (stops early - faster)
aws ec2 describe-instances --max-items 20 --output text \
    --query 'Reservations[].Instances[].[InstanceId,InstanceType]'

# Prevent timeout on large S3 bucket listing
aws s3api list-objects-v2 --bucket my-bucket --page-size 100 --max-items 1000 \
    --query 'Contents[].[Key,Size]' --output text

# Batch describe with specific IDs (faster than pagination)
aws ec2 describe-instances --instance-ids i-111 i-222 i-333 \
    --query 'Reservations[].Instances[].[InstanceId,State.Name]' --output text
```

**PREFER BATCH APIs**: When you have specific resource IDs, pass them directly:

- ✅ `describe-instances --instance-ids id1 id2 id3` (single call, up to 1000 IDs)
- ❌ Loop with `describe-instances --instance-ids $id` for each ID

### JMESPath Functions

**USEFUL JMESPATH FUNCTIONS - Reduce post-processing with built-in functions**

**AGGREGATION**:

- `max_by(array, &field)` - Find item with max field value
- `min_by(array, &field)` - Find item with min field value
- `sort_by(array, &field)` - Sort array by field
- `reverse(array)` - Reverse array order
- `length(array)` - Count items

**FILTERING**:

- `[?field == `value`]` - Exact match (note backticks for literals)
- `[?contains(field, `substring`)]` - Substring match
- `[?starts_with(field, `prefix`)]` - Prefix match
- `[?field > `100`]` - Numeric comparison

**SELECTION**:

- `[*].field` - Extract field from all items
- `[0]` - First item only
- `[-1]` - Last item only
- `[:5]` - First 5 items
- `[-5:]` - Last 5 items

**EXAMPLES**:

```bash
# Top 5 largest EBS volumes (sorted, limited)
aws ec2 describe-volumes --query 'reverse(sort_by(Volumes, &Size))[:5].[VolumeId,Size]' --output text

# Find largest RDS instance by storage
aws rds describe-db-instances --query 'max_by(DBInstances, &AllocatedStorage).[DBInstanceIdentifier,AllocatedStorage]' --output text

# Count running instances
aws ec2 describe-instances --filters Name=instance-state-name,Values=running \
    --query 'length(Reservations[].Instances[])' --output text

# Instances with Name tag containing "prod"
aws ec2 describe-instances --query 'Reservations[].Instances[?Tags[?Key==`Name`] | [0].Value | contains(@, `prod`)].[InstanceId]' --output text
```

### Throttling and Retries

**API THROTTLING AWARENESS - Important for parallel execution**

**AWS CLI BUILT-IN RETRIES**:

- Default: Legacy mode with 5 max attempts, exponential backoff up to 20 seconds
- Handles transient errors (5xx) and throttling (429) automatically

**WHEN PARALLEL EXECUTION HITS RATE LIMITS**:

- AWS APIs have per-account rate limits (varies by service)
- Running 50+ parallel calls may trigger throttling
- CLI retries automatically, but adds latency

**MITIGATION STRATEGIES**:

```bash
# 1. Add small delay between spawning jobs (reduces burst)
for instance in $instances; do
    process_instance "$instance" &
    sleep 0.05  # 50ms stagger
done
wait

# 2. Use batch APIs when available
aws ec2 describe-instances --instance-ids $all_ids  # Single call for up to 1000 IDs

# 3. Configure adaptive retry mode (optional, for heavy workloads)
export AWS_RETRY_MODE=adaptive
export AWS_MAX_ATTEMPTS=10
```

**RETRY MODES** (set via AWS_RETRY_MODE or ~/.aws/config):

- `legacy`: Default, 5 attempts, simple exponential backoff
- `standard`: Better jitter, handles more error codes
- `adaptive`: Client-side rate limiting (experimental)

**NOTE**: For most scripts, default retries are sufficient. Only add delays or change retry mode if seeing consistent throttling.

### Efficient CLI Script Example

**ANTI-PATTERN EXAMPLE (SEQUENTIAL - SLOW - 🚫 UNACCEPTABLE)**

```bash
# #!/bin/bash
# RUNTIME: ~60 seconds for 30 instances (2 sec per call x 30)
END_TIME=$(date -u +"%Y-%m-%dT%H:%M:%S")
START_TIME=$(date -u -d "30 days ago" +"%Y-%m-%dT%H:%M:%S")

for instance in "${INSTANCES[@]}"; do
    echo "Processing: $instance"
    # This SEQUENTIAL loop is FORBIDDEN
    aws cloudwatch get-metric-statistics \
        --namespace AWS/RDS \
        --metric-name CPUUtilization \
        --dimensions Name=DBInstanceIdentifier,Value="$instance" \
        --start-time "$START_TIME" \
        --end-time "$END_TIME" \
        --period 86400 \
        --statistics Average \
        --output text
done
# TOTAL TIME: ~60 seconds (UNACCEPTABLE for 30+ instances)
```

**CORRECT EXAMPLE (PARALLEL - FAST - ✅ REQUIRED)**

```bash
#!/bin/bash
# RUNTIME: ~2 seconds for 30 instances (all run simultaneously)
export AWS_PAGER=""  # Disable pager for scripting
END_TIME=$(date -u +"%Y-%m-%dT%H:%M:%S")
START_TIME=$(date -u -d "30 days ago" +"%Y-%m-%dT%H:%M:%S")

# Fetch a single metric (called in parallel)
get_metric() {
    local instance=$1 metric=$2 stat=$3
    aws cloudwatch get-metric-statistics \
        --namespace AWS/RDS \
        --metric-name "$metric" \
        --dimensions Name=DBInstanceIdentifier,Value="$instance" \
        --start-time "$START_TIME" --end-time "$END_TIME" \
        --period 86400 --statistics "$stat" \
        --output text --query "Datapoints[*].[$stat]" \
        | awk -v m="$metric" -v s="$stat" -v i="$instance" \
            '{sum+=$1; count++} END {if(count>0) printf "%s\t%s\t%s\t%.2f\n", i, m, s, sum/count}'
}

# Process one instance: fetch multiple metrics in parallel
process_instance() {
    local instance=$1
    get_metric "$instance" "CPUUtilization" "Average" &
    get_metric "$instance" "CPUUtilization" "Maximum" &
    get_metric "$instance" "FreeableMemory" "Average" &
    wait  # Wait for all metrics of this instance
}

# Process ALL instances in parallel
for instance in "db-prod-1" "db-prod-2" "db-staging"; do
    process_instance "$instance" &
done
wait  # Wait for all instances to complete
```

**PERFORMANCE COMPARISON**
| Pattern | Instances | Time/Call | Total Time | Speedup |
|---------|-----------|-----------|------------|---------|
| Sequential (❌) | 30 | 2 sec | ~60 sec | 1x |
| Parallel (✅) | 30 | 2 sec | ~2 sec | **30x** |

**KEY PARALLEL PATTERNS**
✅ `get_metric ... &` - Each metric fetch runs in background
✅ `process_instance ... &` - Each instance processed in background
✅ `wait` - Synchronizes before continuing (at end of function and script)

**VALIDATION CHECKLIST FOR AGENT**
Before outputting ANY script, check every item:

- [ ] Count number of independent resources/metrics/regions to process: \_\_\_
- [ ] Count number of `&` background job spawns in script: \_\_\_
- [ ] If these counts don't match, the script is WRONG - REJECT it and rewrite
- [ ] Verify each background job block is followed by a `wait` statement
- [ ] Check that NO sequential loops exist for independent operations
- [ ] Confirm expected runtime is ~2-10 seconds (not ~30+ seconds)
- [ ] **CRITICAL**: Search entire script for `--statistics` with commas (`,`). If found, REJECT and rewrite with spaces
  - ❌ `--statistics Average,Maximum` ← WRONG
  - ✅ `--statistics Average Maximum` ← CORRECT
- [ ] Verify all CloudWatch `--statistics` values are EXACT case: SampleCount, Average, Sum, Minimum, Maximum (no lowercase)
- [ ] Confirm script has no `--output json` without proper `--query` or jq filtering

### Parallel vs Sequential Rules

- **ALWAYS PARALLEL**: Multiple instances, multiple metrics, multiple regions, multiple services
- **ONLY SEQUENTIAL**: Operations that depend on previous results (e.g., create then modify, query then filter)
- **PARALLEL PATTERN**: `{ operation1 & operation2 & operation3 & }; wait`
- **SEQUENTIAL PATTERN**: Only when operation B requires result from operation A
- **NEVER**: Sequential loops for independent operations - this wastes time and tokens

**FORBIDDEN ANTI-PATTERNS** (will cause script rejection):

- ❌ `for item in $list; do aws ... ; done` (causes O(n) delays; use `for item in $list; do aws ... & done; wait`)
- ❌ `while read line; do aws ... ; done < file` (sequential processing; parallelize with background jobs)
- ❌ Nested loops without background jobs: `for i in $list1; do for j in $list2; do cmd; done; done`
- ❌ One call at a time when batch API is available (e.g., describe-instances for each ID instead of describe-instances --instance-ids id1 id2 id3)
- ❌ Processing outputs sequentially when they could be fetched in parallel: `result1=$(cmd1); result2=$(cmd2)` → should be `cmd1 & cmd2 & wait`

**REQUIRED ANTI-PATTERN FIXES**:

- ✅ BEFORE: `for instance in $instances; do aws ec2 describe-instances --instance-ids $instance; done`
- ✅ AFTER: `for instance in $instances; do aws ec2 describe-instances --instance-ids $instance & done; wait`
- ✅ BEFORE: `aws describe-instances --filters Name=tag:Name,Values=$tag1 ; aws describe-instances --filters Name=tag:Name,Values=$tag2`
- ✅ AFTER: `aws describe-instances --filters Name=tag:Name,Values=$tag1 & aws describe-instances --filters Name=tag:Name,Values=$tag2 & wait`

### CloudWatch Statistics Validation

- **CRITICAL**: CloudWatch GetMetricStatistics ONLY accepts these 5 statistics: SampleCount, Average, Sum, Minimum, Maximum
- **SYNTAX RULES (NO COMMAS ALLOWED)**:
  - ❌ NEVER use commas: `--statistics Average,Maximum` (CAUSES ERROR)
  - ✅ ALWAYS use spaces: `--statistics Average Maximum` (CORRECT)
  - ✅ OR use repeated flags: `--statistics Average --statistics Maximum` (ALSO CORRECT)
- **COMMON MISTAKES TO AVOID**:
  - ❌ Commas: `--statistics Average,Maximum` → InvalidParameterValue error
  - ❌ Quoted comma list: `--statistics "Average,Maximum"` → Still a syntax error
  - ❌ Invalid names: Mean, Median, p95, p99, Percentile, StandardDeviation
  - ❌ Case variations: "average", "AVERAGE", "max" (must be exact: Average, Maximum)
  - ❌ Any custom or derived statistic names
- **CORRECT USAGE EXAMPLES**:
  - ✅ `--statistics Average Maximum` (space-separated, no quotes)
  - ✅ `--statistics Average --statistics Maximum` (repeated flags)
  - ✅ `--statistics SampleCount Average Sum Minimum Maximum` (all valid stats space-separated)
- **DETECTION CHECKLIST**: Before running script, search for any `--statistics` with a comma (`,`) - if found, REJECT script immediately
- **ERROR MESSAGE**: If you see "The parameter Statistics.member.1 must be a value in the set [...]", you used a comma - fix by using spaces instead

### Common Pitfalls

🚨 **CLOUDWATCH STATISTICS**: See CloudWatch Statistics Validation - use SPACES not COMMAS.
🚨 **HEREDOC SYNTAX**: See aws-billing/SKILL.md → "Heredoc Syntax" - options MUST come BEFORE `<<EOF`.
🚨 **CLOUDTRAIL EVENTS**: See aws-billing/SKILL.md → "CloudTrail Lookup Efficiency" - use `jq` with `fromjson`, NOT `--query`.

**SERVICE-SPECIFIC PITFALLS**:

- Cost Explorer RI/SP dimension restrictions: see `aws-billing/SKILL.md` Rule 11 for the authoritative dimension table per API. Key: `get-reservation-utilization` only supports `SUBSCRIPTION_ID`; `get-reservation-coverage` supports `AZ`, `CACHE_ENGINE`, `DATABASE_ENGINE`, `DEPLOYMENT_OPTION`, `INSTANCE_TYPE`, `INVOICING_ENTITY`, `LINKED_ACCOUNT`, `OPERATING_SYSTEM`, `PLATFORM`, `REGION`, `TENANCY`; use `get-cost-and-usage` for SERVICE-level data
- Reservation coverage/utilization APIs require `YYYY-MM-DDTHH:MM:SSZ` timestamps; prefer `date -u +"%Y-%m-%dT%H:%M:%SZ"`
- Do not run exploratory commands that enumerate EC2 instance specifications; rely on static documentation instead
- When grouping or aggregating S3/API data, use `--output text --query` with awk/sort/uniq instead of jq; complex jq filters with `//` operators cause shell quoting errors in multi-line scripts
- **Security Groups/NACLs**: Always use `--output text` with specific --query fields (GroupId, GroupName, IpPermissions summary) rather than dumping full JSON rules arrays
- **Network discovery**: Extract only essential fields (IDs, names, CIDR blocks) using --query; avoid returning entire nested structures
- **Cost Explorer output explosion**: Using DAILY granularity for 30 days with SERVICE grouping produces 30 x N_services lines (~1000+ lines). ALWAYS aggregate with awk and limit with `| head -N`. Use MONTHLY granularity unless daily breakdown is specifically requested.
- **CloudWatch `--output text` single-line trap**: `--output text --query 'Datapoints[*].Average'` outputs ALL values tab-separated on ONE line, not one per row. Awk scripts that expect `{sum+=$1; count++}` per-line will only process one "line" and produce wrong totals. Fix: use `--query 'Datapoints[*].[Timestamp,Average]'` (two-field projection gives one row per datapoint), or pipe through `tr '\t' '\n'` before awk.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

