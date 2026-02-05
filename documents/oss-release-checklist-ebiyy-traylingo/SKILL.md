---
name: oss-release-checklist
description: Comprehensive checklist for releasing OSS projects. Covers security (CSP, PII, secrets), legal compliance (licenses, API terms, trademarks), privacy (GDPR, telemetry opt-out), and documentation. Use when preparing to open source a project, adding telemetry/error monitoring, auditing dependencies, or creating privacy policies.
---

# OSS Release Checklist

Everything to verify before making a project public.

## Quick Reference

| Category | Risk | Reference |
|----------|------|-----------|
| Security | 🔴 Critical | [security.md](references/security.md) |
| Legal/Licensing | 🔴 Critical | [legal.md](references/legal.md) |
| Privacy | 🟠 High | [privacy.md](references/privacy.md) |

## Pre-Release Checklist

### Security (Critical)

- [ ] CSP is not `null` in tauri.conf.json
- [ ] `sendDefaultPii` is NOT `true` in Sentry
- [ ] Sentry `beforeSend` scrubs sensitive data
- [ ] API keys/DSNs injected via CI, not hardcoded
- [ ] Event listeners have corresponding cleanup

### Legal (Critical)

- [ ] API terms of service reviewed (caching, commercial use)
- [ ] `cargo deny check` passes (no GPL contamination)
- [ ] `pnpm licenses:check` passes (npm dependencies)
- [ ] LICENSE file present and matches package.json

### Privacy (High)

- [ ] PRIVACY.md exists
- [ ] All third-party services documented
- [ ] Telemetry opt-out available in Settings
- [ ] "Takes effect after restart" noted where applicable

### Documentation

- [ ] SECURITY.md network destinations accurate
- [ ] PRIVACY.md matches implementation
- [ ] README setup instructions current

## Risk Matrix

| Issue | Severity | Consequence |
|-------|----------|-------------|
| CSP `null` | 🔴 Critical | XSS → full system access |
| `sendDefaultPii: true` | 🔴 Critical | User clipboard sent to Sentry |
| GPL dependency | 🔴 Critical | Project becomes GPL |
| No privacy policy | 🟠 High | GDPR violation, trust loss |
| Hardcoded DSN | 🟠 High | Forks send errors to your Sentry |
| No opt-out | 🟠 High | No user control over data |

## Common Mistakes by Framework

### Tauri

| Mistake | Fix |
|---------|-----|
| `"csp": null` | Set proper CSP directives |
| Missing `unlisten()` | Always cleanup event listeners |
| Sentry in Rust without scrub | Use `before_send` filter |

### Error Monitoring (Sentry)

| Mistake | Fix |
|---------|-----|
| `sendDefaultPii: true` | Never enable for clipboard apps |
| Hardcoded DSN | Use `import.meta.env` / `option_env!` |
| No opt-out | Add Settings toggle + restart note |

### Dependencies

| Mistake | Fix |
|---------|-----|
| No license audit | Add `cargo deny` + npm check to CI |
| GPL crate slipped in | Check `deny.toml` deny list |
| MPL without understanding | MPL is file-level copyleft, usually OK |

## Audit Commands

```bash
# Rust licenses
cargo deny check

# npm licenses
pnpm licenses:check

# Find hardcoded secrets
grep -r "sk-" --include="*.rs" --include="*.ts" .
grep -r "dsn.*sentry" --include="*.rs" --include="*.ts" .
```

## For Forks

When someone forks your OSS:
1. Secrets should be empty (CI-injected)
2. Sentry disabled by default (no DSN)
3. Clear instructions for their own setup
