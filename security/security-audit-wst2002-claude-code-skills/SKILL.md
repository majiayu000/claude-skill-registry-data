---
name: security-audit
description: Use when asked to review code for security, find vulnerabilities, run an OWASP check, audit before a release, or answer "is this secure?" — any language or framework, whole repo or a single feature.
---

# Security Audit

## Overview

Find vulnerabilities an attacker can actually reach, prove each one with code, and say exactly how to fix it. A short list of real, exploitable findings beats a long list of maybes.

## Method

1. **Scope.** Identify entry points: HTTP routes, CLI args, file uploads, message consumers, webhooks, scheduled jobs. Note the framework and auth mechanism.
2. **Map trust boundaries.** For each entry point, follow untrusted input to where it is used (query, shell, file path, HTML, redirect, deserializer, template).
3. **Sweep by class.** Search systematically with the patterns in [checklist.md](checklist.md). Do not stop at the first hit per class.
4. **Verify every candidate** before reporting:
   - Is the input attacker-controlled? Trace it.
   - Is there validation, escaping, parameterisation or an auth check on the path?
   - Is the code reachable in production (not a test, fixture, or dead code)?
   If any answer removes the risk, drop it or mark it Low confidence.
5. **Check configuration and dependencies:** CORS, cookies, headers, debug flags, secrets in repo, known-vulnerable versions in lockfiles.
6. **Report** using the contract below.

## Output contract

Start with one line: `N findings: X critical, Y high, Z medium, W low.` Then one block per finding, highest severity first:

```
### [SEVERITY] Title
- Location: path/to/file.ext:line
- Evidence: the 1-5 lines of code that are vulnerable
- Attack: concrete input or request an attacker sends and what they get
- Fix: the corrected code, or the exact change
- Confidence: High | Medium | Low
```

End with **Checked and clean:** the classes you searched that had no findings. If nothing was found, say so plainly. Do not pad.

## Severity

| Severity | Meaning |
|---|---|
| Critical | Remote, unauthenticated: code execution, auth bypass, full data access |
| High | Authenticated user reaches other users' data or admin actions; injection; stored XSS |
| Medium | Needs user interaction or a specific condition; reflected XSS; weak crypto |
| Low | Defense in depth: missing headers, verbose errors, minor info leak |

## Common mistakes

- Reporting a `query()` call as SQL injection without checking it is parameterised.
- Flagging secrets in `.env.example`, tests or docs as leaked credentials.
- Missing authorization bugs (IDOR) because every route "has auth" — check that the record belongs to the caller.
- Listing generic advice ("use HTTPS") instead of findings in this code.
- Stopping after the first file. Audit every entry point.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
