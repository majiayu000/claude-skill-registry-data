---
name: nick-secrets-guard
description: Local-first secret scanning for repos and git history. Use before every push, when scanning for exposed keys, checking for committed credentials, or auditing a repo for accidental secret leaks. Designed for Nick's workflow and safer than forcing suspicious marketplace secret scanners.
---

# Nick Secrets Guard

Use this as the default secrets scanner.

## Purpose
Detect exposed secrets in:
- current working tree
- tracked files
- common env/config files
- git history

## Hard rules
- Alert immediately if secrets are found
- Scan git history, not just current files
- Never print full secrets in normal output
- Show file path, line number, commit/hash when possible, and secret type
- Prefer local-only scanning; do not rely on external APIs

## What to detect
- API keys
- OAuth tokens
- passwords and connection strings
- private keys
- Supabase keys
- OpenAI-style keys
- GitHub tokens
- Stripe-like keys
- database URLs
- `.env`/credential file exposure

## Standard workflow
1. Scan current repo files
2. Scan likely env/config files
3. Scan git history
4. Classify findings by type and severity
5. Report clearly with safe redaction
6. Recommend remediation steps

## Output format
- Severity
- Secret type
- File path
- Line number if available
- Commit hash if from history
- Redacted value preview
- Remediation

## References
- Read `references/patterns.md` for what is detected
- Read `references/remediation.md` for response steps
- Read `references/pre-push-usage.md` for pre-push workflow

## Bundled scripts
- `scripts/scan_repo_secrets.py` — scan files and git history for likely secrets
- `scripts/pre_push_secret_scan.sh` — repo-local pre-push scan wrapper
