---
name: security
description: >-
  Scan and redact PII and sensitive data (emails, phone numbers, SSNs, API keys,
  IP addresses, credentials, amounts, company/person names) from repository files.
  Includes a pre-commit hook to block commits containing PII. Use when asked to
  audit code for sensitive data, sanitize files before publishing, or install PII
  detection hooks. For application security hardening see security-engineering.
when_to_use: |
  Triggers on: "PII scan", "redact", "sanitize files", "pre-commit hook",
  "sensitive data at rest", "accidentally committed", "open-source sanitize".

  Use when auditing a repository for accidentally committed PII or secrets,
  sanitizing files before open-sourcing or publishing, or installing a pre-commit
  hook to block future PII commits. Focused exclusively on data-at-rest scanning
  and redaction using regex pattern matching.

  Not when: hardening application code against OWASP vulnerabilities, implementing
  auth/sessions/input validation, or doing a cross-stack security review — use
  security-engineering instead.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# Security Sanitizer

Scans and redacts PII / sensitive data from files in this repo. Uses only Python standard library — no external dependencies.

## Tools

Resolve scripts project-first, then global install ([findings-ledger references/install-paths.md](../findings-ledger/references/install-paths.md) — same pattern, swap skill name):

```sh
PROJ="${CLAUDE_PROJECT_DIR:-.}"
SAN="$PROJ/.claude/skills/security/scripts/sanitizer.py"
[ -f "$SAN" ] || SAN="$PROJ/.agents/skills/security/scripts/sanitizer.py"
[ -f "$SAN" ] || SAN="$HOME/.claude/skills/security/scripts/sanitizer.py"
[ -f "$SAN" ] || SAN="$HOME/.agents/skills/security/scripts/sanitizer.py"
```

| Script | Purpose | Key Command |
|--------|---------|-------------|
| `scripts/sanitizer.py` | Scan or redact PII in files | `python3 "$SAN" --scan --dir . --recursive` |
| `scripts/pre-commit-hook.sh` | Git hook to block commits with PII | Copy it from the resolved skill directory to `.git/hooks/pre-commit`, then `chmod +x` it |

## Configuration

Edit `scripts/sanitizer-config.json` beside this skill (same directory as `$SAN`) to customize blocklists, custom regex patterns, skip paths, and placeholder format.

## Exit Codes

`0` = clean, `1` = PII found (useful for CI).

## Related skills

- [security-engineering](../security-engineering/SKILL.md) — application security, OWASP, auth hardening, input validation, auth/session patterns for web applications
