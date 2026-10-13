---
name: security-auditor
description: Audits repository security — hardcoded secrets, dependency vulnerabilities, environment variable management, and authentication patterns. Use when the user asks to "check security", "find secrets", "audit dependencies", or "secure my repo". Don't use for code review, deployment, or monitoring.
---

# Security Auditor

Finds and fixes common security issues in repositories built by solo founders and small teams.

## How It Works

1. Scan for hardcoded secrets and credentials
2. Check environment variable management
3. Audit dependencies for known vulnerabilities
4. Review authentication and authorization patterns
5. Check for common security misconfigurations

## Step-by-Step Procedure

### Step 1: Scan for Hardcoded Secrets
```bash
# Check for common secret patterns
grep -rn --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" --include="*.py" --include="*.env" \
  -E "(sk-[a-zA-Z0-9]{20,}|api_key\s*=\s*['\"][^'\"]+|password\s*=\s*['\"][^'\"]+|secret\s*=\s*['\"][^'\"]+|AWS_ACCESS_KEY|PRIVATE_KEY)" . \
  | grep -v node_modules | grep -v '.env.example' | head -30
```

If matches found: **flag as critical** and recommend moving to environment variables.

### Step 2: Check Environment Variable Management
- `.env` should be in `.gitignore` (if not: **critical**)
- `.env.example` should exist listing all required variables
- No `.env` files committed to git history
- Check for `process.env.` or `os.environ` usage without defaults

### Step 3: Audit Dependencies
For Node.js:
```bash
npm audit --production 2>/dev/null || echo "npm audit not available"
```

For Python:
```bash
pip-audit 2>/dev/null || echo "pip-audit not available"
```

Flag: critical and high severity vulnerabilities.

### Step 4: Review Auth Patterns
- Is there authentication? (NextAuth, Clerk, Auth0, Supabase Auth, custom JWT)
- Are API routes protected? Check for middleware/guards
- Are admin routes separated from public routes?
- Is CSRF protection in place for forms?

### Step 5: Check Common Misconfigurations
- CORS: Is it set to `*` in production? (flag as warning)
- Rate limiting: Any on API routes?
- Input validation: Are user inputs sanitized?
- HTTPS: Is the app enforcing HTTPS?

## Output Format
```markdown
## 🔒 Security Audit

### Critical Issues
- {issue}: {location} — {fix}

### Warnings
- {issue}: {location} — {recommendation}

### Good Practices Found
- {practice already in place}
```

## Important
- NEVER print or expose actual secret values in output
- Always recommend `.env` + `.env.example` pattern
- Prioritize: hardcoded secrets > dependency vulns > auth gaps > misconfigs
