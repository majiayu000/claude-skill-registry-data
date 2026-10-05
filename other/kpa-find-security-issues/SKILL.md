---
name: kpa-find-security-issues
description: Find 3 security issues ranked by severity - injection, auth, data exposure, API, dependencies
context: fork
agent: Sonnet
metadata:
  author: kpa
  updated-date: "2026-03-19"
---

Find 3 security issues in the codebase, ranked by severity (critical > high > medium > low).

## Steps

1. Read the project structure and understand the tech stack (see CLAUDE.md / AGENTS.md for context).
2. Systematically scan the codebase for security vulnerabilities in the categories below.
3. For each issue found, report:
   - **Severity**: Critical / High / Medium / Low
   - **Category**: Which category from the list below
   - **Location**: File path and line number(s)
   - **Description**: What the vulnerability is and why it matters
   - **Recommendation**: Concrete fix with a code example if possible

## Categories to Check

### Injection & Input Validation
- SQL injection or unsafe raw queries
- NoSQL injection patterns
- Command injection (e.g., in scripts or server actions)
- XSS vulnerabilities in rendered content (especially `dangerouslySetInnerHTML` or unescaped user input)

### Authentication & Authorization
- Missing or improper auth checks on API routes and server actions
- Routes or server components that access user data without verifying the session
- IDOR (Insecure Direct Object Reference) — accessing another user's data by manipulating IDs
- Missing CSRF protections on state-changing operations

### Data Exposure
- Secrets, API keys, or credentials hardcoded in source (not using environment variables)
- Sensitive data leaked to the client (e.g., server-only data in client components)
- Overly permissive queries returning more fields than needed
- Error messages that expose internal details (stack traces, DB schema)

### API & Network Security
- Missing rate limiting on API routes or server actions
- Missing input validation/sanitization on API endpoints
- Open redirects
- SSRF (Server-Side Request Forgery) in any URL-fetching logic

### Dependency & Configuration
- Known vulnerable dependencies (check package.json versions)
- Insecure configuration (missing security headers, permissive CORS)
- Exposed environment variable patterns
- Unsafe config settings

### Data Storage
- Sensitive data stored without encryption
- Insecure cookie settings
- Missing database-level access controls

## Notes

- Focus on real, exploitable issues — not theoretical concerns or style preferences.
- Prioritize issues that could lead to data breaches, unauthorized access, or service disruption.
- Be creative and think outside the box — look at the actual data flow, not just patterns.
- Do NOT fix the issues, only report them.
