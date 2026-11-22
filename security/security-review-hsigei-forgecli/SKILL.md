---
name: security-review
description: Security review of pending changes or a project - injection, secrets, auth, unsafe input handling, dependencies
---
# Security review

1. Scope: pending changes (`git diff`, `git diff --staged`) unless the user names files or asks for the
   whole project. For a whole project, start from entry points: routes, CLI arguments, file uploads,
   anything that reads user or network input.
2. Check, and only report what you can point to in the code:
   - injection: SQL built from strings, shell commands built from input, eval/exec, template injection,
     path traversal (`../` in file paths taken from users)
   - secrets: API keys, passwords or tokens in code, logs or committed .env files
   - auth: missing login or permission checks, IDs taken from the request without checking ownership,
     weak session or password handling
   - web: XSS (unescaped output), CSRF on state-changing forms, open redirects, CORS set to *
   - data: sensitive data in error messages or logs, missing TLS checks, insecure deserialization
   - dependencies: very old or known-vulnerable packages (`pip list --outdated`, `npm audit` if present)
3. For each finding give: severity (high/medium/low), file:line, what an attacker could do, and the fix.
4. Don't fix anything unless the user asks. If nothing real turns up, say so plainly.
