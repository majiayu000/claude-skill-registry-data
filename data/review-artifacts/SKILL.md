---
name: review-artifacts
description: Review artifact scan results for reportable bug bounty findings. Analyzes archives, SQL dumps, binary databases, and source backups for secrets, code vulnerabilities, misconfigurations, and PII exposure. Focuses on high-confidence findings with clear security impact.
---

# Review Artifact Findings

Triage artifact scan results to find **reportable bug bounty vulnerabilities**. Artifacts are files that automated scanners (Trufflehog, Semgrep) cannot process directly - they require extraction or manual analysis.

**Goal**: Find high-confidence findings with verified exploitability and clear security impact.

## Project Structure

All paths are relative to the project root (working directory):

```
threat_hunting/                    # Project root (working directory)
├── <org-name>/                    # Cloned repositories (e.g., jitsi/, tronprotocol/)
│   └── <repo-name>/               # Individual repository source code
├── findings/<org-name>/           # All scan results for an organization
│   ├── semgrep-results/
│   ├── trufflehog-results/
│   ├── artifact-results/          # Artifact scan JSON output
│   │   └── <repo-name>.json
│   ├── kics-results/
│   └── reports/                   # Final consolidated reports
└── scripts/                       # ALL extraction and scanning scripts
```

**Repository source code location**: `<org-name>/<repo-name>/` (e.g., `jitsi/jicofo/src/main/java/...`)
**Scan results location**: `findings/<org-name>/artifact-results/<repo-name>.json`

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
- `./scripts/extract-and-scan-archives.sh` - Extract archives and scan for secrets
- `./scripts/safe-extract-archive.sh` - Safely extract individual archives

If you need functionality not provided by existing scripts, ask the user to update the scripts rather than writing one-off solutions.

## Quick Start

```bash
# Extract from findings/ directory (per-repo files)
./scripts/extract-artifact-findings.sh <org-name>                  # All repos, summary
./scripts/extract-artifact-findings.sh <org-name> archives         # Just archives
./scripts/extract-artifact-findings.sh <org-name> sql              # Just SQL dumps

# Extract from catalog scans (merged gzipped files)
./scripts/extract-artifact-findings.sh <org-name> --catalog         # Latest scan
./scripts/extract-artifact-findings.sh <org-name> --scan 2025-12-24 # Specific scan

# Extract archives and scan for secrets
./scripts/extract-and-scan-archives.sh <org-name>
```

**Data Sources:**
- `findings/<org>/artifact-results/*.json` - Per-repo results (uncompressed)
- `catalog/tracked/<org>/scans/<timestamp>/artifacts.json.gz` - Merged scan (gzipped)

## Workflow

### Step 1: Discover Artifacts and Verify Counts

Run the extraction script with count format first:

```bash
# Step 1a: Get counts to verify totals
./scripts/extract-artifact-findings.sh <org-name> count

# Step 1b: Get full summary
./scripts/extract-artifact-findings.sh <org-name>
```

**CRITICAL COUNT VERIFICATION**: The summary output shows totals at the bottom. These MUST match the sums from step 1a. If they don't match, the extraction may be truncating results - investigate before proceeding.

This categorizes artifacts by type:
- **Archives** - Need extraction before scanning
- **SQL dumps** - May contain PII (marked `[CONTAINS DATA]` if they have actual records)
- **Binary databases** - SQLite, etc. requiring manual inspection
- **Source backups** - `.bak`, `.old` files that may reveal past vulnerabilities

### Step 2: Extract and Scan Archives

**CRITICAL: Always use safe extraction - NEVER extract manually!**

```bash
# Scan all archives for secrets
./scripts/extract-and-scan-archives.sh <org-name>

# Or extract a single archive for manual review
./scripts/safe-extract-archive.sh <archive-path> [output-dir]
```

Safe extraction protects against:
- Path traversal (zip-slip) attacks
- Symlink/hardlink attacks
- Decompression bombs (size limits enforced)

### Step 3: Analyze for Vulnerabilities

After secret scanning, review extracted content for:
1. **Code vulnerabilities** - Injection, auth bypass, dangerous functions
2. **Misconfigurations** - Privileged containers, overly permissive access
3. **PII exposure** - Real user data in dumps
4. **Architectural intel** - Internal endpoints, attack surface details

### Step 4: Assess Reportability

For each finding, evaluate:
- **Is it exploitable?** - Can you demonstrate the impact?
- **Is it in production code?** - Not test fixtures or examples
- **Is it in scope?** - Check the bug bounty program policy
- **Is it high confidence?** - Clear security impact, not theoretical

### Step 5: Document Findings

Use the templates below for reportable findings.

---

## Analysis by Artifact Type

### Archives

Archives may contain secrets, vulnerable code, or sensitive configurations.

#### High-Risk Indicators
- Names: `backup`, `prod`, `production`, `deploy`, `config`
- Location: `deploy/`, `infrastructure/`, `scripts/`
- Size: Large archives may contain full codebases or database dumps

#### Low-Risk (Often Skip)
- Test/sample data: `test/`, `fixtures/`, `samples/`
- Asset bundles: images, fonts, icons
- Vendored dependencies (report upstream instead)

#### What to Look For

**Secrets** (via Trufflehog - automatic):
- API keys, tokens, credentials
- Private keys (SSH, TLS)
- Database connection strings

**Kubernetes/Helm Misconfigurations**:
```bash
# Privileged containers (container escape risk)
grep -r "privileged: true" <dir>
grep -rE "host(Network|PID|IPC): true" <dir>

# Running as root
grep -r "runAsUser: 0" <dir>
grep -r "runAsNonRoot: false" <dir>

# Overly permissive RBAC
grep -rE "cluster-admin" <dir>
grep -rE "verbs:.*\*" <dir>

# Exposed services
grep -rE "type: (LoadBalancer|NodePort)" <dir>
```

**Infrastructure Misconfigurations**:
```bash
# Public cloud resources
grep -rE "acl.*public" <dir>
grep -rE "0\.0\.0\.0/0" <dir>

# Disabled encryption
grep -rE "encrypted.*false" <dir>
```

**Code Vulnerabilities**:
```bash
# Command injection
grep -rnE "(exec|system|popen|subprocess|shell_exec|eval)\s*\(" <dir>

# Deserialization
grep -rnE "(pickle\.load|yaml\.load|unserialize|readObject)" <dir>

# SQL injection patterns
grep -rn "SELECT.*\+\|INSERT.*\+\|UPDATE.*\+" <dir>

# Debug/admin endpoints
grep -rnE "(debug.*true|DEBUG.*=.*1|/debug/|/admin/)" <dir>
```

**Architectural Intelligence**:
```bash
# Internal hostnames
grep -rE "\.internal\.|\.local\.|\.corp\." <dir>

# Database connection strings (even without creds - reveals topology)
grep -rE "(mysql|postgres|mongodb|redis)://" <dir>

# API endpoints
grep -rE "/api/v[0-9]|/internal/" <dir>
```

---

### SQL Dumps

SQL dumps with `[CONTAINS DATA]` have INSERT/COPY statements - real data.

#### Reportable Findings

**PII Exposure** (CRITICAL if real user data):
```bash
# Sensitive table names
grep -iE 'CREATE TABLE.*(user|customer|account|payment|order)' <file.sql>

# PII columns
grep -iE '(email|password|ssn|phone|address|credit_card)' <file.sql>

# Sample the data
grep -A5 'INSERT INTO' <file.sql> | head -50
```

**What makes it reportable:**
- Real user data (not obviously fake like `test@example.com`)
- Password hashes (even hashed passwords are sensitive)
- Payment/financial information
- Health/medical data

**Likely false positive:**
- Schema-only dumps (no INSERT statements)
- Clearly fake data (`John Doe`, `123 Main St`, sequential IDs)
- Files in `test/`, `fixtures/`, `samples/`

---

### Binary Databases

SQLite and other binary databases need manual inspection.

```bash
# List tables
sqlite3 <file.db> ".tables"

# Show schema
sqlite3 <file.db> ".schema"

# Look for sensitive tables
sqlite3 <file.db> ".tables" | grep -iE '(user|account|session|token|key|secret|cred)'

# Sample data
sqlite3 <file.db> "SELECT * FROM <table> LIMIT 5;"
```

**What to look for:**
- Session tokens or API keys
- User credentials
- Cached sensitive data
- Application secrets

---

### Source Code Backups

Files like `.php.bak`, `.py.old`, `.env.bak` may reveal:

1. **Removed secrets** - Credentials deleted from current version
2. **Fixed vulnerabilities** - Bugs that were patched (check if fix is complete)
3. **Debug code** - Logging passwords, disabled auth checks

```bash
# Compare backup to current file
diff file.php file.php.bak

# Search for secrets
grep -n 'password\|secret\|key\|token\|api_key' file.bak

# Search for vulnerabilities
grep -n 'eval\|exec\|system\|shell_exec' file.bak
```

**High-risk backups:**
- `.env.bak`, `.env.production.old` - Environment files
- `config.php.old`, `settings.py.bak` - Configuration files
- `auth.php.bak`, `login.py.old` - Authentication code

---

## Reportability Assessment

### Directly Reportable

| Finding Type | Severity | Requirements |
|--------------|----------|--------------|
| Verified active secret | CRITICAL | Confirmed working (API responds, login succeeds) |
| Real PII in SQL dump | CRITICAL | Actual user data, not test fixtures |
| Privileged container + hostNetwork | HIGH | In production Helm chart, not examples |
| Command injection in code | HIGH | Reachable code path, not dead code |

### Requires Further Investigation

| Finding Type | Next Steps |
|--------------|------------|
| Internal hostnames discovered | Check if they resolve externally, test for SSRF |
| Unverified secrets | Attempt to use them, check if rotated |
| Misconfiguration in Helm chart | Verify it's deployed, not just in repo |
| Architectural intel | Use to inform testing of main application |

### Likely Not Reportable

- Secrets in test fixtures or example code
- Schema-only SQL dumps
- Misconfigurations in vendored dependencies
- Findings in archived/deprecated code that's no longer deployed

---

## Documentation Templates

### Secret in Archive

```markdown
## SECRET EXPOSURE - [Type]

**Repository**: org/repo-name
**Archive**: path/to/archive.tgz
**File**: extracted/path/to/file

**Secret Type**: AWS Access Key / API Token / Database Password / etc.
**Verified**: Yes/No (describe verification)

**Impact**:
- What access does this secret provide?
- What data/systems are at risk?

**Reproduction**:
1. Extract archive: `./scripts/safe-extract-archive.sh <path>`
2. Secret location: `<file>:<line>`
3. Verification: `<command or steps>`

**Recommendation**: Rotate immediately, remove from repository history
```

### PII Exposure

```markdown
## PII EXPOSURE - SQL Dump

**Repository**: org/repo-name
**File**: path/to/dump.sql
**Size**: X MB

**Data Exposed**:
- Table: users (X records)
  - Columns: email, password_hash, phone, address
- Table: payments (X records)
  - Columns: credit_card_last4, billing_address

**Real vs Test Data**: [Evidence this is real data]

**Impact**: X user records exposed including [specific PII types]

**Recommendation**:
1. Remove from repository and git history
2. Assess if breach notification required
3. Force password reset if credentials exposed
```

### Code Vulnerability in Archive

```markdown
## CODE VULNERABILITY - [Type]

**Repository**: org/repo-name
**Archive**: path/to/archive.tgz
**Location**: extracted/file.py:45

**Vulnerability**: [Type - e.g., Command Injection, Privileged Container]

**Details**:
[Explain the vulnerability]

**Exploitability**:
- Is this code deployed/reachable?
- What's required to exploit?

**Impact**: [What can an attacker do?]

**Recommendation**: [Specific fix]
```

### Architectural Intelligence

```markdown
## ARCHITECTURAL DISCOVERY

**Repository**: org/repo-name
**Source**: path/to/config

**Discovered**:
- Internal endpoints: [list]
- Service topology: [description]
- Authentication mechanism: [details]

**Security Relevance**:
[How this informs further testing]

**Follow-up Actions**:
- [ ] Test endpoint X for vulnerability Y
- [ ] Check if internal hostname resolves externally
```

---

## False Positive Indicators

**Skip these:**
- Files in `test/`, `fixtures/`, `testdata/`, `samples/`, `examples/`
- Files with `example`, `sample`, `demo`, `dummy`, `mock` in name
- Vendored/third-party code (report upstream)
- Schema-only SQL (no INSERT/COPY statements)
- Obviously fake data (`test@example.com`, `password123`)

**Investigate these:**
- Files in `config/`, `deploy/`, `scripts/`, `backup/`, `infrastructure/`
- Files with `prod`, `production`, `live` in name
- SQL dumps marked `[CONTAINS DATA]`
- Environment file backups (`.env.*`)
- Large files (>1MB may contain real data)

---

## Reference

### Safe Extraction Commands

```bash
# Extract and scan all archives (preferred)
./scripts/extract-and-scan-archives.sh <org-name>

# Extract single archive
./scripts/safe-extract-archive.sh <archive-path>

# Extract to specific directory
./scripts/safe-extract-archive.sh <archive-path> <output-dir>

# Adjust limits for large archives
SAFE_EXTRACT_MAX_ARCHIVE_SIZE=209715200 \
SAFE_EXTRACT_MAX_EXTRACTED_SIZE=1073741824 \
./scripts/safe-extract-archive.sh <archive-path>
```

### Extraction Script Options

```bash
# Summary view (default)
./scripts/extract-artifact-findings.sh <org>

# Filter by type
./scripts/extract-artifact-findings.sh <org> archives
./scripts/extract-artifact-findings.sh <org> sql
./scripts/extract-artifact-findings.sh <org> sources

# Full JSON
./scripts/extract-artifact-findings.sh <org> full
```
