---
name: orbit-sec-secrets-leak
description: Scan a WordPress plugin codebase + git history for hardcoded secrets — API keys, OAuth tokens, .env file leakage, password hashes, AWS keys, Stripe keys, Twilio tokens. Uses gitleaks-style entropy + regex detection. Use when the user says "secrets leak", "API key in code", "scan for secrets", "gitleaks", "before open-sourcing".
---

# 🪐 orbit-sec-secrets-leak — Secrets in source / git history

The most embarrassing security bug. Hardcoded API key → posted publicly → real charges. This skill catches it before the commit goes out.

---

## Quick start

```bash
# Install gitleaks once
brew install gitleaks

# Scan working tree + full git history
gitleaks detect --source ~/plugins/my-plugin --verbose

# Or via Orbit
bash ~/Claude/orbit/scripts/scan-secrets.sh ~/plugins/my-plugin
```

---

## What it detects

### 1. Common API key patterns (regex)

| Pattern | Service |
|---|---|
| `sk_live_[0-9a-zA-Z]{24,}` | Stripe live secret |
| `pk_live_[0-9a-zA-Z]{24,}` | Stripe live publishable (less sensitive but still flag) |
| `xoxp-[0-9a-zA-Z-]+` | Slack user token |
| `xoxb-[0-9a-zA-Z-]+` | Slack bot token |
| `ghp_[A-Za-z0-9]{36}` | GitHub PAT |
| `gho_[A-Za-z0-9]{36}` | GitHub OAuth |
| `AKIA[0-9A-Z]{16}` | AWS Access Key ID |
| `AC[a-z0-9]{32}` | Twilio Account SID |
| `SK[a-z0-9]{32}` | Twilio Auth Token |
| `pk_[a-z0-9]{32}` | ClickUp API |
| `mailgun-[a-f0-9]{32}` | Mailgun |
| `key-[a-f0-9]{32}` | Mailgun (alt) |
| `EAA[A-Za-z0-9]+` | Facebook access |
| `ya29\.[A-Za-z0-9_-]+` | Google OAuth |

### 2. Generic-secret entropy detection
**Whitepaper intent:** Strings with high entropy (close to random) + named like `_key`, `_token`, `_secret`, `_password` are likely secrets even if they don't match a known pattern.

```php
// Auditor flags all of these:
$apiKey = 'sk_a1b2c3d4e5...';
$secret = 'AKIA...';
define( 'MY_TOKEN', 'eyJhbGciOiJIUzI1NiJ9...' );
```

### 3. .env / .env.example contamination
- `.env` should NEVER be in source / zip
- `.env.example` (template) is OK but should have placeholders, not real values

### 4. Password hashes in test fixtures
```php
// Test fixtures committed:
$wpdb->insert( ..., [ 'user_pass' => '$P$BabcDEFhash' ] );
```

Even hashed, this is a real password hash → can be brute-forced. Use a placeholder.

### 5. Git history (not just current state)
```bash
gitleaks detect --redact --log-opts="--all"
```

A secret committed and reverted is STILL in git history. Anyone who clones can find it.

### 6. Authorization headers in tests / docs
```bash
# README often has examples that include real keys
$ curl -H "Authorization: Bearer sk_live_xxx" ...
```

### 7. SSH private keys, GPG keys
Less common but devastating if leaked.

---

## Output

```markdown
# Secrets Scan — my-plugin

## Working tree
- ❌ includes/class-stripe.php:42 — sk_live_xxxxx... (Stripe live secret)
   Severity: CRITICAL
- ❌ tests/fixtures/users.sql:18 — bcrypt hash starting $2y$10$... (test password)
   Severity: HIGH

## Git history (full --all scan)
- ❌ Commit a1b2c3d (2024-09-12): added .env with real Mailgun key
   "Removed in commit f9e8d7..." — but key is STILL in history
   ACTION: rotate Mailgun key + force-push history rewrite (high-risk; rotate key first)

## .env files
- ⚠ .env exists in working tree — should be gitignored
- ✓ .env.example uses placeholders only

## Recommendation
1. ROTATE the Stripe key revealed in includes/class-stripe.php immediately
2. Move Stripe key to wp_options (encrypted at rest preferred)
3. Add `.env` to .gitignore (NOT just .gitignore for the parent — also for the plugin)
4. For the leaked Mailgun key in history: rotate FIRST, then optionally rewrite history
   (force-push is destructive — may not be worth it once key is rotated)
```

---

## Pair with

- `/orbit-zip-hygiene` — secrets shouldn't be in release zips
- `/orbit-pay-stripe` / `/orbit-pay-paypal` — secret-handling for these specifically
- `/orbit-sec-supply-chain` — sometimes secrets hide in lockfiles

---

## Sources & Evergreen References

### Canonical docs
- [Gitleaks](https://github.com/gitleaks/gitleaks) — scanner reference
- [TruffleHog](https://github.com/trufflesecurity/trufflehog) — alt scanner with verification
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning) — built-in for public repos
- [Have I Been Pwned](https://haveibeenpwned.com/) — credential breach DB

### Rule lineage
- gitleaks 8.x (2023+) — current generation, supports v2 config
- Pattern catalog updated continuously (new providers added monthly)

### Last reviewed
- 2026-04-29 — pattern list re-fetched from gitleaks default rules on every run
