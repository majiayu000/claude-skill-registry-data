---
name: pii-exposure-audit
description: Systematic repo-wide audit for personal information exposure — API keys, tokens, passwords, Windows paths, usernames, emails, Discord IDs, Nostr keys, personal domains, and business contact info. Use when asked to sanitize a repo before going public or to generate a remediation checklist.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [security, audit, pii, sanitization, credentials]
    triggers: [pii audit, sanitize repo, check credentials, personal info scan, repo security audit]
    related_skills: [github, repo-sanitization-audit, pii-exposure-audit]
---

# PII Exposure Audit

Systematic multi-pattern scanning to find personal information committed to a repo. Complements `codebase-hardening` (which covers app-security vulnerabilities, fork cleanup, and generic key removal) by focusing on **what the repo reveals about its owner**.

## When to Use

When asked to:
- "Audit this repo for personal info before making it public"
- "Generate a sanitization checklist"
- "Find all instances of my name, email, or paths in the codebase"
- "Check for credentials committed to the repo"
- "What sensitive information is in this config?"
- "Prepare this repo for open-sourcing"

## Workflow

### Phase 1: Map the Repo

```
find . -not -path './.git/*' -type f | sort
```

Identify high-value targets: config files (`.yaml`, `.json`), scripts (`.py`, `.sh`), documentation (`.md`), profile/SOUL files, key stores.

### Phase 2: Parallel Pattern Scan

Run all searches simultaneously — do NOT serialize them. Each searches the repo root (excluding `.git`).

| Category | Pattern | What It Finds |
|----------|---------|---------------|
| OpenAI/standard keys | `sk-[a-zA-Z0-9]{20,}` | OpenAI-style API keys |
| GitHub tokens | `gh[ps]_[a-zA-Z0-9]{10,}` | GH PATs/OAuth |
| HuggingFace tokens | `hf_[a-zA-Z0-9]{10,}` | HF API tokens |
| GitLab tokens | `glpat-[a-zA-Z0-9]{10,}` | GitLab PATs |
| Slack tokens | `xox[bp]-[a-zA-Z0-9]{10,}` | Slack bot/user tokens |
| Bearer tokens | `Bearer\s+[a-zA-Z0-9_-]{20,}` | Raw bearer auth headers |
| Generic key/secret | `(Token\|Secret\|Password\|Api[_-]?Key)\s*[:=]\s*['"][a-zA-Z0-9_\-\.]{8,}` | Catch-all credentials |
| Nostr nsec | `nsec1[ac-z][a-z0-9]{50,}` | Nostr private keys |
| SHA-256 hex | `[0-9a-f]{64}` | Potential private keys (verify context — also catches hashes) |
| Discord IDs | `\b[0-9]{17,19}\b` | Discord channel/guild/user IDs |
| Emails | `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}` | Email addresses |
| Windows paths | `C:\\Users\\\|C:/Users/` | Reveals Windows username |
| Owner data folder | `<detected_owner_string>` | Personal folder layout |
| IP addresses | `\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b` | Hardcoded IPs |
| Calendar URLs | `cal\.com\|calendly` | Personal booking links |
| Phone numbers | `\(?[0-9]{3}\)?[-. ]?[0-9]{3}[-. ]?[0-9]{4}` | Contact numbers |
| Personal domains | `<owner_domain>\.[a-z]+` | Personal/business domain |

### Phase 3: Read High-Value Files Directly

After pattern search, read the files most likely to carry credentials:

- `*config.yaml` / `*config.yml` — MCP server `env:` sections often have **plaintext credential fallbacks** alongside `${VAR_REF}` markers
- `*keys.json` — Nostr key stores, API key directories
- `.env.example` — Reveals credential naming conventions
- Scripts referencing `gmail`, `smtp`, `password`, `token`, `api_key` as Python constants
- Profile/SOUL identity files — leak real names and contact info

### Phase 4: Cross-Reference Env-Ref Credentials

When a config says `${VAR_NAME}`, check:
- `.env.example` for hardcoded fallback values for the same name
- Python scripts for constants matching the env var name
- **The real-secrets escape** happens when config says `${SECRET_KEY}` but a sibling script hardcodes `SECRET_KEY = "plaintext-value"` as a Python constant

### Phase 5: Triage by Severity

| Tier | Label | Criteria | Example |
|------|-------|----------|---------|
| 🔴 CRITICAL | Live credentials | Plaintext key/password that actually authenticates | `GMAIL_SENDER_PASSWORD: ${GMAIL_APP_PASSWORD}` |
| 🟠 HIGH | Credential-adjacent | Partially redacted keys, default passwords, internal auth keys | Truncated Nostr secrets, `postgres:postgres@localhost` |
| 🟡 MEDIUM | Personal info & paths | Absolute paths with owner name, emails, domains, calendar links | `${MY_REPOS}/Documents/...`, `your-domain.example` |
| ⚪ LOW | Metadata & IDs | Channel UUIDs, Discord IDs, org GitHub handles | Discord channel IDs, Nostr channel UUIDs |

### Phase 6: Produce Sanitization Checklist

Output as a grouped checklist. Each item has: file path, line number, what was found, what to replace it with.

```
CRITICAL (do first):
☐ config/config.yaml:431 — GMAIL_SENDER_PASSWORD in plaintext → replace with ${GMAIL_APP_PASSWORD}
☐ scripts/email_intelligence.py:23 — same Gmail app password as Python constant → use env var

HIGH:
☐ buzz/keys.json — 47 Nostr secret keys exposed → regenerate if repo goes public
...

MEDIUM:
☐ config/gateway.yaml:712 — Absolute path ${MY_REPOS}/... → use relative or $REPO_ROOT
...
```

## See Also

- `codebase-hardening` skill — app security audits (auth, injection, SSRF, CORS) and general code quality fixes
- `references/hermes-config-pii-audit.md` — full worked example covering a Hermes config repo with 20+ findings across 151 files

## Pitfalls

- **Template files look safe but reveal naming conventions**: `.env.example` files with `KEY_PLACEHOLDER` names tell attackers what env vars you use. This is low severity but worth noting.
- **Discord IDs are not credentials but reveal infra**: Channel/guild IDs in config let anyone who sees them know your Discord server structure. Obfuscate or remove before public sharing.
- **Nostr key files with "...truncated" secrets**: If the key is truncated with `...` it's NOT safe — the full key exists somewhere or was pasted in full at some point. Regenerate before going public. Caveat: read the file's raw bytes first — `...` in TOOL OUTPUT may be display-side redaction of a full key on disk. Both cases are findings, but disk-truncation means the value is already gone while display-truncation means the full key is sitting in the file.
- **Tool output masks secret-adjacent strings**: `process.env.OPENROUTER_API_KEY` renders as `proces..._KEY`, emails may render as `[email protected]`, JWTs render truncated. Never declare a file clean (or corrupt) from displayed content — grep the real unmasked pattern (e.g. `process.env`) or read raw bytes. Use `secrets-safe-config-audit`'s `scripts/classify-secret.py` for redaction-proof classification (length/prefix/sha evidence, never values).
- **555 phone numbers feel fake but may be real**: If a config has `OFFER_PHONE: (555) 123-4567`, verify it's actually the 555-reserved prefix before declaring it safe.
- **Duplicated Gmail credentials in multiple config files**: A real Gmail app password often gets copy-pasted into every MCP server config section. Search for the password string once, find it in every file.
- **Don't conflate env-refs with plaintext**: `${GITHUB_TOKEN}` is fine (reads from environment). `GITHUB_TOKEN: ghp_xxxxx` is critical. Check the actual value, not just the variable name.
