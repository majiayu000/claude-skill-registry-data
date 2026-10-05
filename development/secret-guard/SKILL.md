---
name: secret-guard
description: Use when reviewing changes or committing ANY code in this project — prevents leaking secrets and sensitive information to git/GitHub. Pairs with the deterministic gitleaks pre-commit gate.
---

# Secret Guard

Goal: **nothing sensitive ever reaches git history / GitHub.** Two layers:

- **Deterministic** — `gitleaks git --staged` runs in the git `pre-commit` hook
  (`mise run scan:secrets:staged`) and blocks the commit on a regex/entropy match.
  Full history is re-scanned in CI (`mise run scan:secrets`).
- **AI review (this skill)** — when you (Claude) are about to `git commit`, the
  PreToolUse hook injects this checklist so you confront the staged diff against the
  things regex misses (internal hostnames, PII, private URLs, unknown token shapes).

## What counts as a leak — review the staged diff for:

- **Credentials & keys**: API keys/tokens, passwords, `Authorization:` headers,
  private keys (`-----BEGIN ... PRIVATE KEY-----`), `.pem`/`.p12`, SSH keys,
  cloud creds (AWS `AKIA…`, GCP service-account JSON), DB connection strings with
  passwords, OAuth client secrets, JWTs, webhook signing secrets.
- **Config that should be local**: `.env` files, `*.local.*`, credential files,
  `kubeconfig`, `.netrc`, `.npmrc` with `_authToken`.
- **Internal/PII**: real internal hostnames/IPs, private endpoints, customer data,
  emails, names, phone numbers, account IDs in fixtures or logs.
- **Accidental inclusions**: pasted terminal output containing tokens, debug dumps,
  build artifacts, `dist/`, coverage files with embedded data.

## How to act

1. Run `git diff --cached` and scan for the categories above.
2. If you find a secret: **do not commit.** Remove it, move it to an env var /
   secret manager, and add the file to `.gitignore`. If it was a real credential
   that already touched the working tree, treat it as compromised → rotate it.
3. For false positives in gitleaks, add a scoped allowlist to `.gitleaks.toml`
   (never disable scanning wholesale) or a `.gitleaksignore` entry with a comment.
4. Prefer placeholders in examples: `ghp_xxx`, `<API_KEY>`, `password=REDACTED`.

## Notes

- The deterministic gate uses `--redact`, so matched secrets are not printed back.
- This skill is a safety net for what gitleaks can't pattern-match; it does not
  replace the gate. Both run before every commit.
