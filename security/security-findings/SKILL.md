---
name: security-findings
description: How to handle CodeQL, Trivy, Dependency Review and secret scanning findings - fixing them, when a dismissal or .trivyignore entry is acceptable, and who decides. Use when a security check fails or a code scanning alert is raised.
metadata:
  scope: repository
---

# Security findings

## The rule

Security checks report and block; people decide. A finding is fixed in code whenever a fix exists. Only the maintainer dismisses an alert or accepts a risk, and every accepted risk has a written reason next to it.

| Tool | Finds | Where the reason goes if it's accepted |
| --- | --- | --- |
| CodeQL | Code and workflow weaknesses | The alert's dismissal comment ("won't fix" with why) |
| Trivy | Vulnerable OS or .NET packages in the image, Dockerfile and compose misconfiguration | `.trivyignore`, one id per line with a comment above it |
| Dependency Review | Vulnerable or wrongly licensed packages added in a pull request | Not dismissible; change the package |
| Secret scanning and push protection | Credentials in commits | Not dismissible; rotate the secret and remove it |

Private vulnerability reports arrive through `SECURITY.md`, never as public issues.

## Steps

1. Read the finding and confirm it applies. A CodeQL "missing authorization" on an endpoint that's meant to be anonymous is a real decision, not noise.
2. Fix it: update the package or base image, change the code, tighten the config.
3. If no fix exists yet (an unfixed OS package), Trivy's `ignore-unfixed` already skips it. If a fix exists but can't be taken, ask the maintainer.
4. When the maintainer accepts a risk, record the reason where the table says, in the same pull request.

## Don't

- Dismiss an alert or add a `.trivyignore` entry yourself.
- Lower a severity threshold or remove a scanner.
- Commit a secret, even to a branch, even briefly.
- Discuss an unfixed vulnerability in a public issue or pull request.

## Check

Static Analysis and Container Scan are green, and the repository's Security tab shows no new open alerts.
