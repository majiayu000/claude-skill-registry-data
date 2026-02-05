---
name: review-kics
description: Review KICS Infrastructure as Code scan results to identify exploitable misconfigurations. Use when analyzing KICS output, triaging IaC findings, or when the user has kics-results directories to review. Automatically performs safe verification of discovered resources using read-only operations.
---

# Review KICS IaC Findings

Expert analysis workflow for triaging KICS Infrastructure as Code scan results. **Critical distinction**: IaC findings are reconnaissance, not vulnerabilities. The code describes *intended* infrastructure - you must verify actual deployment.

## Project Structure

All paths are relative to the project root (working directory):

```
threat_hunting/                    # Project root (working directory)
├── <org-name>/                    # Cloned repositories (e.g., jitsi/, tronprotocol/)
│   └── <repo-name>/               # Individual repository source code
├── findings/<org-name>/           # All scan results for an organization
│   ├── semgrep-results/
│   ├── trufflehog-results/
│   ├── artifact-results/
│   ├── kics-results/              # KICS JSON output files
│   │   └── <repo-name>.json
│   └── reports/                   # Final consolidated reports
└── scripts/                       # ALL extraction and scanning scripts
```

**Repository source code location**: `<org-name>/<repo-name>/` (e.g., `jitsi/infra-provisioning/terraform/...`)
**Scan results location**: `findings/<org-name>/kics-results/<repo-name>.json`

## CRITICAL: Do NOT Write Custom Scripts

**All extraction scripts already exist in `./scripts/`**. Never write custom jq, Python, or shell scripts to parse findings. The existing scripts handle:
- Complex JSON/NDJSON parsing
- Large file handling
- Edge cases and error handling
- Consistent output formatting

Available extraction scripts:
- `./scripts/extract-semgrep-findings.sh` - Parse semgrep results
- `./scripts/extract-trufflehog-findings.sh` - Parse trufflehog results
- `./scripts/extract-artifact-findings.sh` - Parse artifact results
- `./scripts/extract-kics-findings.sh` - Parse KICS results

If you need functionality not provided by existing scripts, ask the user to update the scripts rather than writing one-off solutions.

## The IaC Reality Check

```
IaC Finding (code)  →  Resource Identifier  →  Auto-Verify  →  Reportable Finding
     ↑                       ↑                      ↑
   KICS scan           Extraction           Safe GET requests
```

## CRITICAL: Always Use the Extraction Script First

**MANDATORY**: Before doing ANY manual analysis, run the extraction script:

```bash
./scripts/extract-kics-findings.sh <org-name>
```

Then extract resource identifiers:

```bash
./scripts/extract-kics-findings.sh <org-name> resources
```

## Quick Reference

```bash
# Extract from findings/ directory (per-repo files)
./scripts/extract-kics-findings.sh <org-name>                  # All repos, summary
./scripts/extract-kics-findings.sh <org-name> resources        # Resource identifiers
./scripts/extract-kics-findings.sh <org-name> count            # Counts only

# Extract from catalog scans (merged gzipped files)
./scripts/extract-kics-findings.sh <org-name> --catalog         # Latest scan
./scripts/extract-kics-findings.sh <org-name> --scan 2025-12-24 # Specific scan
```

**Data Sources:**
- `findings/<org>/kics-results/*.json` - Per-repo results (uncompressed)
- `catalog/tracked/<org>/scans/<timestamp>/kics.json.gz` - Merged scan (gzipped)

## Workflow

### Step 1: Extract Findings and Verify Counts

```bash
# Step 1a: Get counts to verify total findings
./scripts/extract-kics-findings.sh <org-name> count

# Step 1b: Get summary of all findings
./scripts/extract-kics-findings.sh <org-name>

# Or from catalog scans
./scripts/extract-kics-findings.sh <org-name> --catalog

# Step 1c: Extract resource identifiers for verification
./scripts/extract-kics-findings.sh <org-name> resources
```

**CRITICAL COUNT VERIFICATION**: The summary output shows "Total: N findings" at the bottom. This MUST match the sum of all counts from step 1a (summing the 'total' column). If they don't match, the extraction may be truncating results - investigate before proceeding.

**Note**: Findings are sorted by severity (HIGH first, then MEDIUM, then LOW). All HIGH severity findings appear at the top of the output for immediate attention.

### Step 2: Read IaC Files to Extract Resource Names

For each HIGH/MEDIUM finding, read the IaC file to extract actual resource identifiers:

**Terraform** - Look for:
- `bucket = "actual-bucket-name"`
- `name = "resource-name"`
- Hardcoded values (not `var.` or `local.` references)

**Kubernetes** - Look for:
- `metadata.name`
- Service `type: LoadBalancer` or `NodePort`
- Ingress hostnames

**CloudFormation** - Look for:
- `BucketName:`
- Resource logical names and properties

### Step 3: Automatic Safe Verification

**YOU MUST AUTOMATICALLY RUN THESE VERIFICATIONS** for any discovered resource identifiers. All commands below are safe, read-only operations.

#### S3 Buckets (Safe - Anonymous HEAD/LIST)

For each S3 bucket name found:

```bash
# Check if bucket exists and is public (HEAD request)
curl -s -I "https://BUCKET_NAME.s3.amazonaws.com/" | head -20

# Check bucket region
curl -s -I "https://BUCKET_NAME.s3.amazonaws.com/" 2>&1 | grep -i "x-amz-bucket-region"

# Try anonymous listing (read-only)
curl -s "https://BUCKET_NAME.s3.amazonaws.com/?max-keys=5"
```

**Interpreting results:**
- `HTTP 200` + XML listing = PUBLIC BUCKET (reportable!)
- `HTTP 403 AccessDenied` = Bucket exists but not public
- `HTTP 404 NoSuchBucket` = Bucket doesn't exist
- `HTTP 301` = Bucket exists, different region

#### GCS Buckets (Safe - Anonymous GET)

```bash
# Check if bucket is public
curl -s "https://storage.googleapis.com/BUCKET_NAME?maxResults=5"
```

#### Azure Blob Storage (Safe - Anonymous GET)

```bash
# Check if container is public (format: account.blob.core.windows.net/container)
curl -s "https://ACCOUNT.blob.core.windows.net/CONTAINER?restype=container&comp=list&maxresults=5"
```

#### Web Endpoints / APIs (Safe - GET only)

For discovered hostnames, endpoints, or IPs:

```bash
# Check if endpoint responds (GET request only)
curl -s -I -m 10 "https://HOSTNAME/" | head -10

# Check HTTP (if HTTPS fails)
curl -s -I -m 10 "http://HOSTNAME/" | head -10
```

#### DNS Verification (Safe - Lookup only)

```bash
# Check if hostname resolves
dig +short HOSTNAME

# Check for internal hostnames that might resolve externally
dig +short internal.company.local
```

#### Kubernetes API (Safe - Unauthenticated probe only)

If you find a potential K8s API endpoint:

```bash
# Check if API is exposed (GET only)
curl -s -k -m 10 "https://HOSTNAME:6443/version"
curl -s -k -m 10 "https://HOSTNAME:443/version"
```

**DO NOT** run kubectl commands or attempt authentication.

### Step 4: Triage Findings

#### Automatically Verify These (HIGH Priority)

| Finding Type | Extract | Verify With |
|--------------|---------|-------------|
| S3 Public ACL | Bucket name from `bucket =` | `curl -s https://BUCKET.s3.amazonaws.com/` |
| GCS Public | Bucket name | `curl -s https://storage.googleapis.com/BUCKET` |
| Azure Public Blob | Account + container | `curl -s https://ACCOUNT.blob.core.windows.net/CONTAINER?comp=list` |
| Exposed Service | Hostname/IP + port | `curl -s -I https://HOST:PORT/` |
| K8s API Exposed | Endpoint | `curl -s -k https://HOST:6443/version` |

#### Skip These (Not Verifiable via Safe Methods)

- IAM policy issues (requires authenticated access)
- Encryption-at-rest issues (requires data access)
- Internal network configurations
- Container privilege issues (requires runtime access)

### Step 5: Document Results

For each verification, record:

```
Resource: s3://company-backup-bucket
Source: terraform/storage.tf:23
Verification: curl -s "https://company-backup-bucket.s3.amazonaws.com/?max-keys=5"
Result: [PASTE OUTPUT]
Status: PUBLIC / PRIVATE / NOT_FOUND
```

### Step 6: Report Confirmed Findings

**Only report findings you verified with actual evidence.**

```markdown
## VERIFIED - Public S3 Bucket

**Repository**: org/repo-name
**IaC File**: terraform/storage.tf:45
**Bucket Name**: company-data-bucket

**IaC Code**:
```hcl
resource "aws_s3_bucket" "data" {
  bucket = "company-data-bucket"
  acl    = "public-read"
}
```

**Verification Command**:
```bash
curl -s "https://company-data-bucket.s3.amazonaws.com/?max-keys=10"
```

**Verification Output**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<ListBucketResult>
  <Name>company-data-bucket</Name>
  <Contents>
    <Key>backup-2024-01.sql</Key>
    <Size>1234567</Size>
  </Contents>
  ...
</ListBucketResult>
```

**Impact**: Bucket is publicly listable and contains database backups

**Recommendation**:
1. Remove public ACL immediately
2. Review bucket contents for sensitive data exposure
3. Enable bucket policy to restrict access
```

## Safe Verification Commands Reference

### ALWAYS SAFE (Run automatically)

| Resource Type | Command | What It Does |
|---------------|---------|--------------|
| S3 Bucket | `curl -s -I https://BUCKET.s3.amazonaws.com/` | HEAD request, checks existence |
| S3 Bucket | `curl -s https://BUCKET.s3.amazonaws.com/?max-keys=5` | Anonymous list (5 items max) |
| GCS Bucket | `curl -s https://storage.googleapis.com/BUCKET?maxResults=5` | Anonymous list |
| Azure Blob | `curl -s https://ACCT.blob.core.windows.net/CONTAINER?comp=list&maxresults=5` | Anonymous list |
| Web Endpoint | `curl -s -I -m 10 https://HOST/` | HEAD request with timeout |
| DNS | `dig +short HOSTNAME` | DNS lookup only |
| K8s API | `curl -s -k -m 10 https://HOST:6443/version` | Version check (no auth) |

### NEVER RUN (Potentially harmful)

- `aws s3 cp` or `aws s3 sync` - Downloads files
- `nmap` - Active port scanning (may trigger alerts)
- `kubectl` with any write operations
- `docker` commands against remote hosts
- Any POST/PUT/DELETE requests
- Brute force or enumeration scripts
- Anything requiring or attempting authentication

## False Positive Indicators

**Skip verification for:**
- Resources in `test/`, `examples/`, `samples/` directories
- Parameterized values (`var.bucket_name`, `${var.name}`)
- Obviously fake names (`example-bucket`, `my-test-bucket`)
- Template files (`.example`, `.template`)

**Always verify:**
- Hardcoded bucket/resource names
- Production directories (`prod/`, `production/`)
- CI/CD configurations
- Helm values.yaml with real-looking values

## Output Summary Format

After verification, provide a summary:

```
## KICS Review Summary: <org-name>

### Verified Exposures (Reportable)
1. PUBLIC S3: company-backup-bucket (terraform/storage.tf:23)
   - Contains: database backups, config files
   - Evidence: [curl output showing listing]

### Verified Private (Not Reportable)
1. s3://company-internal - Returns 403 AccessDenied
2. s3://company-logs - Returns 403 AccessDenied

### Not Found (IaC May Be Stale)
1. s3://old-bucket-name - Returns 404 NoSuchBucket

### Could Not Verify (No Resource Identifier)
1. terraform/network.tf:45 - Security group rule, no target IP to test

### Skipped (Test/Example Code)
1. examples/demo-bucket - In examples/ directory
```

## Guidelines

- **Automatically verify** all discovered resource identifiers using safe commands
- **Only report** findings with verified evidence
- **Document everything** - show the command and its output
- **Be conservative** - if curl returns 403, it's working as intended
- **Check context** - same bucket name in test/ vs prod/ means different things
- IaC code ≠ deployed infrastructure - verification is mandatory
