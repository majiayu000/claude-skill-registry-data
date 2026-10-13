---
name: code-review-secrets-detection
description: >
  Find leaked secrets in code, git history, and CI. Load on "secrets", "leaked key", a repo/
  git history in scope, exposed .git, CI config review, or public-repo OSINT. Signals: API keys,
  tokens, .env files, private keys, cloud creds, hardcoded passwords.
domain: code-review
type: technique
stability: learning
modes: [bugbounty, defense]
severity: high
cwe: [CWE-798, CWE-540]
mitre: [T1552.001]
tools: [trufflehog, gitleaks, git]
schema_version: 1
---

# Secrets detection

## When it applies
Any source you can read: an in-scope repo, an exposed `.git/` on a web server, public GitHub
repos of the org, or CI/CD config. Live secrets are direct, high-impact findings.

## Why it works
Secrets get committed and then "removed" — but git keeps history, so they persist in old
commits, branches, and stashes. Config/CI files and client bundles also embed keys that ship to users.

## Method
1. **Scan history, not just HEAD**: `trufflehog git file://. --only-verified` or
   `gitleaks detect --source . -v` — these walk every commit and (trufflehog) verify keys live.
2. **Exposed .git on a target**: `git-dumper http://target/.git/ out/` then scan the recovered repo.
3. **Org-wide OSINT**: GitHub dorks / `trufflehog github --org=<org>` for public leaks (in scope only).
4. **Client-side & config**: grep JS bundles, mobile apps, `.env`, Dockerfiles, k8s manifests,
   CI YAML for keys and tokens.
5. **Validate & scope impact**: confirm the key works with a read-only call (e.g.
   `aws sts get-caller-identity`) — a live, privileged key is the report; a dead one is informational.

## Gotchas
- Report *verified/live* secrets; example/placeholder keys inflate severity and get closed as N/A.
- Rotate-awareness: note it may be live now; don't exfiltrate data with it — prove access, stop.
- Deleted-from-HEAD ≠ gone — always scan full history.

## Verify success
A secret that authenticates successfully (minimal proof), with where it lives (commit/file) —
don't paste the secret value into reports, reference its location.

## References
trufflehog & gitleaks docs; GitHub secret-scanning; OWASP secrets management.
