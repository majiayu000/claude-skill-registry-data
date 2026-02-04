---
name: reviewing-prisma-patterns
description: Review Prisma code for common violations, security issues, and performance anti-patterns found in AI coding agent stress testing. Use when reviewing Prisma Client usage, database operations, or performing code reviews on projects using Prisma ORM.
review: true
allowed-tools: Grep, Glob, Bash
version: 1.0.0
---

# Review Prisma Patterns

This skill performs systematic code review of Prisma usage, catching critical violations, security vulnerabilities, and performance anti-patterns identified through comprehensive stress testing of AI coding agents.

---

<role>
This skill systematically reviews Prisma codebases for 7 critical violation categories that cause production failures, security vulnerabilities, and performance degradation. Based on real-world failures found in 5 AI agents producing 30 violations during stress testing.
</role>

<when-to-activate>
This skill activates when:
- User requests code review of Prisma-based projects
- Performing security audit on database operations
- Investigating production issues (connection exhaustion, SQL injection, performance)
- Pre-deployment validation of Prisma code
- Working with files containing @prisma/client imports
</when-to-activate>

<overview>
The review checks for critical issues across 7 categories:

1. **Multiple PrismaClient Instances** (80% of agents failed)
2. **SQL Injection Vulnerabilities** (40% of agents failed)
3. **Missing Serverless Configuration** (60% of agents failed)
4. **Deprecated Buffer API** (Prisma 6 breaking change)
5. **Generic Error Handling** (Missing P-code checks)
6. **Missing Input Validation** (No Zod/schema validation)
7. **Inefficient Queries** (Offset pagination, missing select optimization)

Each violation includes severity rating, remediation steps, and reference to detailed Prisma 6 skills.
</overview>

<workflow>
## Standard Review Workflow

**Phase 1: Discovery**

1. Find all Prisma usage:
   - Search for @prisma/client imports
   - Identify PrismaClient instantiation
   - Locate raw SQL operations

2. Identify project context:
   - Check for serverless deployment (vercel.json, lambda/, app/ directory)
   - Detect TypeScript vs JavaScript
   - Find schema.prisma location

**Phase 2: Critical Issue Detection**

Run validation checks in order of severity:

1. **CRITICAL: SQL Injection** (P0 - Security vulnerability)
2. **CRITICAL: Multiple PrismaClient** (P0 - Connection exhaustion)
3. **HIGH: Serverless Misconfiguration** (P1 - Production failures)
4. **HIGH: Deprecated Buffer API** (P1 - Runtime errors)
5. **MEDIUM: Generic Error Handling** (P2 - Poor UX)

**Phase 3: Report Generation**

1. Group findings by severity
2. Provide file path + line number
3. Include code snippet
4. Reference remediation skill
5. Estimate impact (Low/Medium/High/Critical)
</workflow>

<validation-checks>
## Quick Check Summary

### P0 - CRITICAL (Must fix before deployment)

**1. SQL Injection Detection**
```bash
grep -rn "\$queryRawUnsafe\|Prisma\.raw" --include="*.ts" --include="*.js" .
```
Red flag: String concatenation with user input
Fix: Use `$queryRaw` tagged template

**2. Multiple PrismaClient Instances**
```bash
grep -rn "new PrismaClient()" --include="*.ts" --include="*.js" . | wc -l
```
Red flag: Count > 1
Fix: Global singleton pattern

### P1 - HIGH (Fix before production)

**3. Missing Serverless Configuration**
```bash
grep -rn "connection_limit=1" --include="*.env*" .
```
Red flag: No connection_limit in serverless app
Fix: Add `?connection_limit=1` to DATABASE_URL

**4. Deprecated Buffer API**
```bash
grep -rn "Buffer\.from" --include="*.ts" --include="*.js" . | grep -i "bytes"
```
Red flag: Buffer usage with Prisma Bytes fields
Fix: Use Uint8Array instead

See `references/validation-checks.md` for complete validation patterns with examples.
</validation-checks>

<review-workflow>
## Automated Review Process

**Step 1: Find Prisma Files**

```bash
find . -type f \( -name "*.ts" -o -name "*.js" \) -exec grep -l "@prisma/client" {} \;
```

**Step 2: Run All Checks**

Execute checks in severity order (P0 → P3):

1. SQL Injection check
2. Multiple PrismaClient check
3. Serverless configuration check
4. Deprecated Buffer API check
5. Error handling check
6. Input validation check
7. Query efficiency check

**Step 3: Generate Report**

Format:
```
Prisma Code Review - [Project Name]
Generated: [timestamp]

CRITICAL Issues (P0): [count]
HIGH Issues (P1): [count]
MEDIUM Issues (P2): [count]
LOW Issues (P3): [count]

---

[P0] SQL Injection Vulnerability
File: src/api/users.ts:45
Impact: CRITICAL - Enables SQL injection attacks
Fix: Use $queryRaw tagged template
Reference: @prisma-6/SECURITY-sql-injection

[P0] Multiple PrismaClient Instances
Files: src/db.ts:3, src/api/posts.ts:12
Count: 3 instances found
Impact: CRITICAL - Connection pool exhaustion
Fix: Use global singleton pattern
Reference: @prisma-6/CLIENT-singleton-pattern
```

</review-workflow>

<output-format>
## Report Format

Provide structured review with:

**Summary:**
- Total files reviewed
- Issues by severity (P0/P1/P2/P3)
- Overall assessment (Pass/Needs Fixes/Critical Issues)

**Detailed Findings:**
For each issue:
1. Severity badge ([P0] CRITICAL, [P1] HIGH, etc.)
2. Issue title
3. File path and line number
4. Code snippet (5 lines context)
5. Impact explanation
6. Specific remediation steps
7. Reference to detailed skill

**Remediation Priority:**
1. P0 issues must be fixed before deployment
2. P1 issues should be fixed before production
3. P2 issues improve code quality
4. P3 issues optimize performance

</output-format>

<constraints>
## Review Guidelines

**MUST:**
- Check all 7 critical issue categories
- Report findings with file path + line number
- Include code snippets for context
- Reference specific Prisma 6 skills for remediation
- Group by severity (P0 → P3)

**SHOULD:**
- Prioritize P0 (CRITICAL) issues first
- Provide specific fix recommendations
- Estimate impact of each violation
- Consider project context (serverless vs traditional)

**NEVER:**
- Skip P0 security checks
- Report false positives without verification
- Recommend fixes without testing patterns
- Ignore serverless-specific issues in serverless projects

</constraints>

<progressive-disclosure>
## Reference Files

For detailed information on specific topics:

- **Validation Checks**: See `references/validation-checks.md` for all 7 validation patterns with detailed examples
- **Example Reviews**: See `references/example-reviews.md` for complete review examples (e-commerce, dashboard)

Load references when performing deep review or encountering specific violation patterns.
</progressive-disclosure>

<validation>
## Review Validation

After generating review:

1. **Verify Findings:**
   - Re-run grep commands to confirm matches
   - Check context around flagged lines
   - Eliminate false positives

2. **Test Remediation:**
   - Verify recommended fixes are valid
   - Ensure skill references are accurate
   - Confirm impact assessments

3. **Completeness Check:**
   - All 7 categories checked
   - All Prisma files reviewed
   - Severity correctly assigned

</validation>

---

**Integration:** This skill is discoverable by the review plugin via `review: true` frontmatter. Invoke with `/review prisma-patterns` or automatically when reviewing Prisma-based projects.

**Performance:** Review of typical project (50 files) completes in < 10 seconds using grep-based pattern matching.

**Updates:** As new Prisma violations emerge, add patterns to validation checks with corresponding skill references.
