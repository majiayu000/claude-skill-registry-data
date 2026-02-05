---
name: security-validation
description: Pre-merge security validation detecting secrets, user-specific paths, insecure SSH configurations, and security-weakening flags. Use before committing code/documentation, before creating PRs, or during QA validation. Supports automated scanning with severity-based enforcement (CRITICAL blocks merge, HIGH requires fixes).
---

# Security Validation

Comprehensive security scanning for code and documentation changes before merge. Detects and enforces remediation of:
- Secret exposure (API keys, tokens, passwords, credentials)
- Path portability issues (user-specific absolute paths)
- Insecure SSH configurations (disabled host verification)
- Security-weakening flags (without proper warnings)

## When to Use

Execute security-validation at these critical gates:

1. **Before committing** - Action Agent, Frontend Developer (catch issues early)
2. **Before creating PR** - All implementation agents (pre-merge gate)
3. **During QA validation** - QA Agent Step 8 (Security & Quality Gates)
4. **After security fixes** - Verify remediation applied correctly
5. **When modifying security-sensitive code** - Authentication, secrets management, configs

## Validation Workflow

### 1. Run Automated Security Scan

Execute the security scanner script on your changes:

**Scan entire repository:**
```bash
./scripts/security_scanner.sh .
```

**Scan specific directory:**
```bash
./scripts/security_scanner.sh docs/
```

**JSON output (for programmatic parsing):**
```bash
./scripts/security_scanner.sh . json
```

**Continue on CRITICAL findings (for reporting):**
```bash
./scripts/security_scanner.sh . text false
```

### 2. Interpret Scan Results

#### Text Output Format

```
🔍 Scanning for hardcoded secrets...
🔍 Scanning for user-specific paths...
🔍 Scanning for insecure SSH configurations...
🔍 Scanning for security-weakening flags...

📊 Scan complete!
   CRITICAL: 2
   HIGH: 3
   MEDIUM: 1

❌ CRITICAL FINDINGS (BLOCK MERGE):
  • docs/setup.md:42 - Potential hardcoded secret detected
  • infrastructure/ssh-config:15 - AWS credential detected

⚠️  HIGH PRIORITY FINDINGS (FIX REQUIRED):
  • docs/deployment.md:78 - macOS user-specific path detected
  • scripts/deploy.sh:23 - StrictHostKeyChecking disabled
  • src/config.ts:105 - Potential hardcoded secret detected

ℹ️  MEDIUM PRIORITY FINDINGS (REVIEW):
  • docs/troubleshooting.md:67 - Insecure connection flag (has warning)
```

#### JSON Output Format

```json
{
  "scan_path": "./",
  "total_findings": 6,
  "findings_by_severity": {
    "CRITICAL": 2,
    "HIGH": 3,
    "MEDIUM": 1
  },
  "findings": [
    {
      "severity": "CRITICAL",
      "file": "docs/setup.md",
      "line": 42,
      "category": "secret_exposure",
      "message": "Potential hardcoded secret detected",
      "context": "API_KEY=sk_live_abc123..."
    },
    {
      "severity": "HIGH",
      "file": "docs/deployment.md",
      "line": 78,
      "category": "path_portability",
      "message": "macOS user-specific path detected",
      "context": "cd /Users/colinaulds/Desktop/project"
    }
  ]
}
```

### 3. Take Action Based on Severity

#### CRITICAL Findings → BLOCK MERGE

**Action:** Stop immediately, do NOT proceed with commit/PR.

**Common CRITICAL findings:**
- Secrets in documentation (`.md`, `.txt`, `.rst`)
- AWS credentials: `AKIA...`, `aws_access_key_id`
- Stripe keys: `sk_live_...`
- GitHub tokens: `ghp_...`
- Google API keys: `AIza...`
- User-specific paths in documentation

**Resolution:**
1. Report to Action Agent with specific file:line references
2. Request immediate fixes
3. Re-run security scan after fixes
4. Proceed only when CRITICAL findings = 0

**Example Report:**
```
❌ SECURITY VIOLATION - BLOCKING MERGE

CRITICAL findings detected:

1. docs/setup.md:42 - Hardcoded API key detected
   Context: API_KEY=sk_live_abc123...
   Fix: Replace with placeholder: API_KEY=<your-stripe-secret-key>

2. docs/deployment.md:78 - User-specific path in documentation
   Context: cd /Users/colinaulds/Desktop/project
   Fix: Use repo-relative path: cd ~/project-name

Cannot proceed until ALL CRITICAL findings resolved.
```

#### HIGH Findings → REQUIRE FIXES

**Action:** Report to Action Agent, request fixes before approval.

**Common HIGH findings:**
- Secrets in code files
- User-specific paths in code
- Insecure SSH configurations
- Security-weakening flags without warnings

**Resolution:**
1. Document each finding with file:line reference
2. Provide remediation guidance (see `references/security-standards.md`)
3. Request Action Agent fixes
4. Re-run scan after fixes
5. Approve when HIGH findings resolved or justified

**Example Report:**
```
⚠️  HIGH PRIORITY - FIXES REQUIRED

3 HIGH findings require attention:

1. src/config.ts:105 - Hardcoded API key in code
   Remediation: Load from environment variable
   Example: const apiKey = process.env.STRIPE_SECRET_KEY;

2. scripts/deploy.sh:23 - StrictHostKeyChecking disabled
   Remediation: Use StrictHostKeyChecking yes or accept-new
   Example: ssh -o StrictHostKeyChecking=accept-new user@host

3. docs/api-guide.md:67 - curl --insecure without warning
   Remediation: Add security warning block above command
   See security-standards.md for warning format
```

#### MEDIUM Findings → REVIEW & JUSTIFY

**Action:** Review findings, accept if appropriate (e.g., has warning), or request fixes.

**Common MEDIUM findings:**
- Security-weakening flags WITH security warning present
- Potentially false positives

**Resolution:**
1. Review context of each finding
2. If legitimate need (e.g., development-only command with warning) → Accept
3. If no justification → Request fix
4. Document acceptance rationale

### 4. Generate Security Validation Report

Combine scan results with LLM review for comprehensive report:

```markdown
## Security Validation for [ISSUE-ID]

### Automated Scan Summary
- Files Scanned: [path]
- Total Findings: X
- CRITICAL: Y findings
- HIGH: Z findings
- MEDIUM: W findings

### Critical Findings (BLOCK)
[If any CRITICAL findings, list with file:line and remediation]
[If zero CRITICAL, state: "No critical findings - scan passed"]

### High Priority Findings (FIX REQUIRED)
[List HIGH findings with file:line and remediation guidance]

### Medium Priority Findings (REVIEW)
[List MEDIUM findings with justification or fix request]

### Manual Review Notes
- [Any context-dependent concerns not caught by scanner]
- [False positives identified and verified]
- [Additional security considerations]

### Recommendation
[BLOCKED | CHANGES REQUIRED | APPROVED]

### Action Items
[Specific fixes needed with file:line references]
[Or: "All security checks passed - approved for merge"]
```

## Finding Categories Reference

### secret_exposure (CRITICAL in docs, HIGH in code)
Hardcoded credentials, API keys, tokens, passwords detected.
**Action:** Replace with environment variables or placeholders.

### path_portability (CRITICAL in docs, HIGH in code)
User-specific absolute paths that won't work for other developers.
**Action:** Convert to repo-relative paths.

### ssh_security (HIGH)
Insecure SSH configurations bypassing host verification.
**Action:** Enable StrictHostKeyChecking or use accept-new.

### security_flags (HIGH without warning, MEDIUM with warning)
Commands using security-weakening flags.
**Action:** Remove flag, add security warning, or justify usage.

## Integration with Agent Workflows

### QA Agent Integration

At **Step 8: Security & Quality Gates**:
1. Run security-validation scan on changed files
2. Interpret findings by severity
3. BLOCK if CRITICAL findings present
4. Request fixes for HIGH findings
5. Review MEDIUM findings
6. Include security report in final QA summary

### Action Agent / Frontend Developer Integration

**Before committing:**
1. Run security-validation scan locally
2. Fix any CRITICAL or HIGH findings
3. Commit only when scan is clean
4. Include scan results in handoff to QA

**After QA feedback:**
1. Re-run security scan after fixes
2. Verify findings resolved
3. Report clean scan to QA

### Tracking Agent Integration

**Before creating PR:**
1. Verify security scan has been run
2. Confirm no CRITICAL findings
3. Document scan results in PR description

## Common Remediation Patterns

### Secret Exposure

**Wrong:**
```javascript
const apiKey = "sk_live_abc123...";
```

**Right:**
```javascript
const apiKey = process.env.STRIPE_SECRET_KEY;
```

**Documentation:**
```markdown
\`\`\`bash
export API_KEY=<your-stripe-secret-key>
# Or use .env file:
API_KEY=$STRIPE_SECRET_KEY
\`\`\`
```

### Path Portability

**Wrong:**
```bash
cd /Users/colinaulds/Desktop/project-name
```

**Right:**
```bash
cd ~/project-name
# Or: Navigate to the project directory
```

### SSH Security

**Wrong:**
```bash
ssh -o StrictHostKeyChecking=no user@host
```

**Right:**
```bash
ssh -o StrictHostKeyChecking=accept-new user@host
# Or pre-populate:
ssh-keyscan -p <port> <hostname> >> ~/.ssh/known_hosts
```

### Security Flags

**Wrong (no warning):**
```bash
curl --insecure https://api.example.com
```

**Right (with warning):**
```markdown
⚠️ **Security Warning:** This command uses `--insecure` which disables SSL certificate verification. Only use in controlled development environments.

\`\`\`bash
curl --insecure https://localhost:8443/api
\`\`\`
```

## Resources

- **Scripts:**
  - `scripts/security_scanner.sh` - Automated security scanning with severity-based findings

- **References:**
  - `references/security-standards.md` - Detailed patterns, examples, remediation guidance, enforcement rules

## Notes

- Run scanner BEFORE committing (catch issues early)
- CRITICAL findings MUST block merge (non-negotiable)
- HIGH findings should be fixed unless explicitly justified
- MEDIUM findings require review and documentation
- False positives: Verify manually, document rationale, consider refactoring to be more obvious
- Re-run scan after fixes to verify remediation
- Include scan results in QA reports and PR descriptions
