---
name: ha:security
description: "Enforce Home Assistant security — config-flow auth, OAuth2, reauth, webhooks, secrets, template injection, input validation, diagnostics redaction. Use when editing config flows, token handling, webhooks, or diagnostics."
effort: medium
user-invocable: false
paths:
  - "**/config_flow.py"
  - "**/application_credentials.py"
  - "**/diagnostics.py"
  - "**/*auth*.py"
---

# Home Assistant Security Reference

> **Config-flow-centered integrations**: integrations built around the `config-flow` skill's selector + validate-before-create pattern have their own step/error-recovery conventions for credential entry — see that skill. Diagnostics redaction, XSS, and secret-handling patterns below still apply universally.

Quick reference for security patterns in Home Assistant integrations and ha-frontend.

## Iron Laws — Never Violate These

1. **VALIDATE AT BOUNDARIES** — Never trust service-call or webhook input. All service schemas are strict voluptuous — never `vol.ALLOW_EXTRA` (P18); user errors raise `ServiceValidationError` with translation keys (P3)
2. **NEVER INTERPOLATE UNTRUSTED INPUT** — Never f-string user or remote input into templates, YAML, or shell commands. Protocol/transport code belongs in the published PyPI library anyway (P11)
3. **NO UNVALIDATED DYNAMIC LOOKUPS** — Never act on a raw `entity_id`/`device_id`/`config_entry_id` from a service call; resolve it through the registries first and raise `ServiceValidationError` when it doesn't belong to this integration
4. **NEVER TRUST STALE CREDENTIALS** — On auth failure raise `ConfigEntryAuthFailed` so core starts the automatic reauth flow; never silently retry with the same token (`reauthentication-flow`, Silver)
5. **ESCAPE BY DEFAULT** — Never use the `unsafeHTML()` directive or `innerHTML` with untrusted content in ha-frontend
6. **SECRETS NEVER IN CODE, LOGS, OR STATES** — Credentials live in `entry.data`, clients in typed `runtime_data` (P6) — never module globals; never logged at any level (PS12); always behind `async_redact_data` in diagnostics (PS7)

## Quick Patterns

### Timing-Safe Webhook Validation

```python
import hmac

async def handle_webhook(hass: HomeAssistant, webhook_id: str, request: Request) -> None:
    body = await request.read()
    signature = request.headers.get("X-Signature", "")
    expected = hmac.new(secret, body, "sha256").hexdigest()

    if not hmac.compare_digest(expected, signature):
        # Reject silently - don't reveal whether the ID or the signature was wrong
        return None

    payload = json_loads(body)  # parse defensively - remote input
```

`==` on secrets short-circuits at the first mismatched byte and leaks prefix
information through response timing — always `hmac.compare_digest`.

### Reauth on Stale Credentials (CRITICAL)

```python
# RAISE ConfigEntryAuthFailed — CORE HANDLES THE REST
async def _async_update_data(self) -> MyData:
    try:
        return await self.client.fetch_data()
    except AuthenticationError as err:
        # Don't retry with the same stale token — hand off to the reauth flow!
        raise ConfigEntryAuthFailed(
            translation_domain=DOMAIN, translation_key="invalid_auth"
        ) from err
```

A token that worked at setup is never guaranteed to still work — providers expire,
revoke, and rotate. `ConfigEntryAuthFailed` makes core start `async_step_reauth`
automatically and notify the user; a silent retry loop just hammers the API with dead
credentials. ("can we add a reauth flow for renewing the oauth token?" — emontnemery,
https://github.com/home-assistant/core/pull/136460#discussion_r2303806443)

### Template Injection Prevention

```python
# SAFE: user-authored template from their own config, rendered by the helper
Template(user_config_template, hass).async_render(parse_result=False)
# VULNERABLE: remote payload rendered as a template
Template(webhook_payload["message"], hass).async_render()
# Templates can read the ENTIRE state machine — a remote sender must never author one

# SAFE: subprocess with list argv (and only in the library — P11)
await asyncio.create_subprocess_exec("ping", "-c", "1", validated_host)
# VULNERABLE: shell interpolation
await asyncio.create_subprocess_shell(f"ping -c 1 {user_host}")
```

## Quick Decisions

### What to validate?

- **Service input** → strict voluptuous schema + selectors; bad values raise `ServiceValidationError` (P3)
- **Config flow input** → validate the connection before `async_create_entry` (P16)
- **Webhook payloads** → verify signature (`hmac.compare_digest`), then parse defensively
- **Paths/URLs from users** → `hass.config.is_allowed_path` / `is_allowed_external_url`

### What to redact?

- **Diagnostics** → `async_redact_data` over entry data AND coordinator data (PS7 — "The name might contain personal information?" — frenck)
- **Logs** → never log `entry.data`, tokens, or coordinates at any level (PS12)
- **State attributes** → no PII, no credentials; static/debug data goes to device info or diagnostics, not attributes

## Anti-patterns

| Wrong | Right |
|-------|-------|
| `Template(remote_payload, hass).async_render()` | Only render templates the user authored in their own config |
| Acting on a raw `device_id` from service data | Resolve via `dr.async_get(hass)` and verify it belongs to this integration |
| `re.compile(user_input)` | `re.escape` user input first, or avoid dynamic regex entirely (ReDoS) |
| `html\`${unsafeHTML(remoteText)}\`` in ha-frontend | `html\`${remoteText}\`` (auto-escaped) |
| Hardcoded `client_secret` in integration source | `application_credentials` platform; per-entry secrets in `entry.data` |
| Catching auth errors and retrying with the same token | Raise `ConfigEntryAuthFailed` → automatic reauth flow |

## References

For detailed patterns, see:

- `${CLAUDE_SKILL_DIR}/references/authentication.md` - Config flow credentials, 2FA steps, secret storage
- `${CLAUDE_SKILL_DIR}/references/authorization.md` - Unique IDs, reauth account matching, frontend admin checks
- `${CLAUDE_SKILL_DIR}/references/input-validation.md` - Voluptuous schemas, paths, template injection
- `${CLAUDE_SKILL_DIR}/references/security-headers.md` - HTTP views, webhook hardening, audit tools
- `${CLAUDE_SKILL_DIR}/references/oauth-linking.md` - OAuth2 via application_credentials, token management
- `${CLAUDE_SKILL_DIR}/references/rate-limiting.md` - Polling discipline, PARALLEL_UPDATES, debouncers
- `${CLAUDE_SKILL_DIR}/references/advanced-patterns.md` - SSRF prevention, secrets management, supply chain
