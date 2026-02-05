---
name: auditing-dependencies
description: Auditing and updating npm dependencies to prevent security vulnerabilities in TypeScript projects
---

# Security: Dependency Management

**Purpose:** Prevent security vulnerabilities through proper npm dependency auditing, updating, and monitoring.

**When to use:** Before adding new dependencies, during security reviews, when setting up CI/CD pipelines, or when package.json changes.

## Critical Security Principle

**Dependencies are attack vectors.** Each package you add introduces potential vulnerabilities:
- Direct vulnerabilities in the package code
- Transitive dependencies (dependencies of dependencies)
- Supply chain attacks (malicious package updates)
- Unmaintained packages with known CVEs

**Default stance:** Minimize dependencies. Every package is a liability.

## Dependency Audit Workflow

### 1. Check for Known Vulnerabilities

**Before installing any package:**

```bash
npm audit
```

This shows:
- Severity levels (critical, high, moderate, low)
- Vulnerable packages and versions
- Recommended fixes
- Dependency path showing how vulnerability entered

**Read the output carefully.** Not all vulnerabilities affect your code:
- Check if vulnerable code path is used
- Assess actual risk vs theoretical risk
- Prioritize fixes by severity and exploitability

### 2. Update Vulnerable Packages

**Automatic fixes (use with caution):**

```bash
npm audit fix
```

This updates packages to non-breaking versions that patch vulnerabilities.

**Breaking changes:**

```bash
npm audit fix --force
```

This updates to latest versions, potentially breaking your code. Use only after:
- Reading breaking change notes
- Having comprehensive test coverage
- Being prepared to fix broken code

**Manual selective updates:**

```bash
npm update package-name
```

Update specific packages after reviewing their changelogs.

### 3. Prevent Vulnerable Installations

**Block installations with vulnerabilities:**

Create `.npmrc` in project root:

```
audit-level=moderate
```

This fails `npm install` if moderate or higher severity vulnerabilities exist.

**In CI/CD:**

```yaml
- name: Security audit
  run: |
    npm audit --audit-level=moderate
    if [ $? -ne 0 ]; then
      echo "Security vulnerabilities found!"
      exit 1
    fi
```

### 4. Monitor Dependencies Continuously

**GitHub Dependabot:**

Enable in repository settings → Security → Dependabot alerts.

Automatically:
- Scans dependencies daily
- Creates PRs for security updates
- Provides vulnerability details

**npm-check-updates:**

```bash
npx npm-check-updates
```

Shows available updates for all dependencies.

```bash
npx npm-check-updates -u
```

Updates package.json (still need to run `npm install`).

## Dependency Selection Best Practices

### Before Adding Any Dependency

**Ask these questions:**

1. **Do I actually need this?**
   - Can I write the functionality myself in < 100 lines?
   - Am I using 10% of the package's features?
   - Is this adding significant bundle size for trivial functionality?

2. **Is this package trustworthy?**
   - Check npm weekly downloads (high is better)
   - Check GitHub stars and recent activity
   - Check last publish date (recent is better, but stable packages may be older)
   - Look for security track record

3. **Is this package maintained?**
   - When was last commit?
   - Are issues being responded to?
   - Are security issues addressed quickly?
   - Is there a clear maintenance policy?

4. **What are the transitive dependencies?**
   ```bash
   npm ls package-name
   ```
   Each transitive dependency is another attack vector.

### Red Flags

**Avoid packages with:**
- No TypeScript types (requires `@types/` package or no types at all)
- Abandoned for > 2 years with no successor
- Known security vulnerabilities with no fix available
- Excessive transitive dependencies (> 50 packages)
- Requires `postinstall` scripts (potential supply chain attack vector)
- Very small packages doing trivial things (left-pad scenario)

### Safer Alternatives

**Use built-in Node.js/browser features when possible:**

```typescript
import { randomBytes } from 'crypto';
const id = randomBytes(16).toString('hex');
```

Better than installing `uuid` package if you just need random IDs.

```typescript
const url = new URL('/api/users', 'https://api.example.com');
url.searchParams.set('limit', '10');
```

Better than installing query string builder packages.

## Lock Files and Reproducible Builds

### Always Commit Lock Files

**package-lock.json** (npm) or **yarn.lock** (Yarn) must be committed:
- Ensures exact same dependency versions across environments
- Prevents supply chain attacks via dependency version updates
- Makes builds reproducible

**Never:**
- Add lock files to `.gitignore`
- Delete lock files to "fix" problems
- Run `npm install` with `--no-package-lock`

### Use Specific Version Ranges

**In package.json, prefer exact versions for critical dependencies:**

```json
{
  "dependencies": {
    "express": "4.18.2",
    "zod": "3.22.4"
  }
}
```

Not:
```json
{
  "dependencies": {
    "express": "^4.18.2",
    "zod": "~3.22.4"
  }
}
```

**Rationale:** Caret (`^`) and tilde (`~`) allow automatic updates that could introduce breaking changes or vulnerabilities.

**Exception:** Development dependencies can use ranges if you regularly update them.

## CI/CD Integration

### Required Security Checks

**Every CI pipeline must:**

1. **Run audit on every build:**
   ```yaml
   - run: npm audit --audit-level=moderate
   ```

2. **Check for outdated dependencies weekly:**
   ```yaml
   schedule:
     - cron: '0 0 * * 1'
   jobs:
     update-check:
       - run: npx npm-check-updates
   ```

3. **Prevent merging PRs with vulnerabilities:**
   ```yaml
   - name: Security gate
     run: npm audit --production --audit-level=moderate
   ```

### Example GitHub Actions Workflow

```yaml
name: Security Audit

on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: '0 0 * * 1'

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm audit --audit-level=moderate
      - name: Check for outdated packages
        run: npx npm-check-updates
```

## Handling Vulnerabilities That Can't Be Fixed

### Scenario: Dependency has vulnerability, no fix available

**Options:**

1. **Find alternative package:**
   - Research similar packages without the vulnerability
   - Consider rewriting functionality if simple

2. **Assess actual risk:**
   - Is vulnerable code path used in your application?
   - Is vulnerability exploitable in your context?
   - Document risk assessment

3. **Audit exception (last resort):**
   ```bash
   npm audit --json > audit-baseline.json
   ```

   Document why exception is acceptable:
   - What is the vulnerability?
   - Why can't it be fixed?
   - What mitigations are in place?
   - When will this be reviewed again?

   **Never ignore vulnerabilities permanently.**

## Common Mistakes

### Mistake 1: Installing packages without checking

```bash
npm install some-random-package
```

**Correct approach:**

1. Check package on npm registry
2. Review GitHub repository
3. Check bundle size: `bundlephobia.com`
4. Run `npm audit` after installation
5. Review lock file changes in git diff

### Mistake 2: Ignoring audit warnings

"It's just a moderate severity in a dev dependency, doesn't matter."

**Wrong.** Development dependencies:
- Can be compromised and steal secrets
- Run with same permissions as your code
- Can modify source files during build

### Mistake 3: Using `--force` without understanding

```bash
npm install --force
```

This bypasses dependency resolution and can install incompatible versions.

**Only use when:**
- You understand exactly what it does
- You've read the conflict details
- You have tests to verify nothing broke

## Maintenance Schedule

**Weekly:**
- Review Dependabot PRs
- Run `npm audit`

**Monthly:**
- Run `npx npm-check-updates`
- Update non-breaking dependencies
- Test thoroughly

**Quarterly:**
- Plan major version updates
- Review all dependencies for continued need
- Remove unused packages

## TypeScript-Specific Considerations

### Type Definition Security

**Check if types match runtime:**

```typescript
import { z } from 'zod';

const APIResponseSchema = z.object({
  data: z.array(z.string()),
});

type APIResponse = z.infer<typeof APIResponseSchema>;
```

This ensures types and runtime validation stay synchronized.

### Type-Only Imports for Tree-Shaking

```typescript
import type { User } from 'huge-library';
```

This imports only types, not runtime code, reducing bundle size.

## Resources

**Tools:**
- `npm audit` - Built-in vulnerability scanner
- `npm-check-updates` - Dependency update checker
- Snyk - Commercial vulnerability scanning
- GitHub Dependabot - Automated security updates

**References:**
- [npm audit documentation](https://docs.npmjs.com/cli/v10/commands/npm-audit)
- [OWASP Dependency Check](https://owasp.org/www-project-dependency-check/)
- [Sonatype State of Software Supply Chain](https://www.sonatype.com/state-of-the-software-supply-chain)

## Summary Checklist

Before merging any dependency changes:

- [ ] `npm audit` passes at moderate level or higher
- [ ] Reviewed what the package does and alternatives considered
- [ ] Checked package maintenance status and security history
- [ ] Lock file committed with changes
- [ ] CI pipeline includes security audit
- [ ] Transitive dependencies reviewed (not excessive)
- [ ] Bundle size impact assessed for frontend projects
- [ ] Types available and trustworthy

**Remember:** The best dependency is the one you don't add. The second best is one that's actively maintained with a strong security track record.
