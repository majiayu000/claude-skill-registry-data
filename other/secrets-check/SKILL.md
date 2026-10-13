---
name: secrets-check
description: >
  Scan staged changes for secrets before commit. Blocks the commit if any known
  pattern matches (AWS keys, Stripe live keys, JWTs, PEM blocks, GitHub tokens,
  Google API keys, generic high-entropy strings).

  Trigger this skill when:
  - Before running `git commit` (auto).
  - User says "check for secrets", "scan for keys", or invokes `/secrets-check`.
  - Before staging any `.env*` or `credentials*` file.
---

## Why

Nimbus repos are public or semi-public. A single leaked live key in git history
means an emergency rotation across Stripe/AWS/Neon/Clerk/whatever. Cheap to
prevent, expensive to fix.

## Patterns to block (regex)

Run against `git diff --cached` output:

| Category | Pattern (regex) | Note |
|---|---|---|
| AWS Access Key | `AKIA[0-9A-Z]{16}` | Access key ID |
| AWS Secret | `(?i)aws.{0,20}?['\"][0-9a-zA-Z/+]{40}['\"]` | Contextual match |
| Stripe live | `sk_live_[0-9a-zA-Z]{24,}` | Also `rk_live_`, `pk_live_` OK to warn on since public keys |
| Stripe restricted | `rk_live_[0-9a-zA-Z]{24,}` | |
| GitHub PAT | `ghp_[0-9a-zA-Z]{36}` | Fine-grained: `github_pat_[0-9a-zA-Z_]{82}` |
| GitHub OAuth | `gho_[0-9a-zA-Z]{36}` | |
| Google API key | `AIza[0-9A-Za-z\-_]{35}` | |
| JWT | `eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+` | Signed JWT (three-segment) |
| PEM header | `-----BEGIN (RSA \|EC \|OPENSSH \|)PRIVATE KEY-----` | Private key material |
| Slack | `xox[baprs]-[0-9a-zA-Z-]{10,}` | Slack tokens |
| Anthropic | `sk-ant-[0-9a-zA-Z-]{95,}` | Anthropic API key |
| OpenAI | `sk-[0-9a-zA-Z]{48}` | OpenAI API key |
| Clerk secret | `sk_(test\|live)_[0-9a-zA-Z]{40,}` | Clerk secret key |
| Neon | `postgres(ql)?://[^:\s]+:[^@\s]+@[^/\s]+/` | Connection string with password |
| Generic .env | `^[A-Z_]{3,}=(?!\s*['\"]?(true\|false\|\d+\|\$\{)).{20,}` | High-entropy env-style assignments |

## Behavior

1. `git diff --cached` (unified format).
2. Run each regex against the added-lines only (`^+` prefix, not context/removed lines).
3. If any match:
   - **BLOCK the commit**.
   - Print `❌ Potential secret detected in <file>:<line-approx>:` + redacted preview (show first 10 chars, mask the rest).
   - Give the user options:
     - `git restore --staged <file>` to unstage.
     - Add to `.gitignore` + rewrite via `git rm --cached`.
     - If it's a false positive, run `git commit --no-verify` (user must type explicitly).
4. If clean → `✅ no secrets detected` and let the commit proceed.

## Filename triggers

Any staged file matching these — warn + require explicit user confirmation
before proceeding:

- `.env`, `.env.*` (except `.env.example`, `.env.template`)
- `credentials.json`, `credentials.*.json`
- `*.pem`, `*.key`, `*.pfx`, `*.p12`
- `id_rsa`, `id_ed25519`, `known_hosts`
- `*.sqlite*` (may contain PII)
- Anything under `nocommit/` or `secrets/` at repo root.

## Do not

- Do NOT log the actual matched value — mask to first 10 chars + `…`.
- Do NOT delete the offending file on your own — always ask the user first.
- Do NOT skip the `--no-verify` escape hatch. If the user needs it, they need it.
  Just make sure the user knows what they're doing.
- Do NOT run this against unstaged changes — only staged.

## False positives

Common ones:
- `AIza…` in a Google Maps widget config that's meant to be public. Warn, don't block.
- JWTs in tests / fixtures. Warn, don't block, if under `**/tests/` or `**/fixtures/`.
- `.env.example` — always allow.

When in doubt, warn + let user decide. Never destructive.
