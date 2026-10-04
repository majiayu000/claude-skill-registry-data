---
name: bmc-security-reviewer
description: >
  Security review for BMC/Panelin: OAuth, tokens, env vars, CORS, HMAC,
  credentials. Use when user requests security review, pre-deploy security
  check, or audit of auth/credentials handling.
---

# BMC Security Reviewer

**Before working:** Read `docs/team/knowledge/Security.md` if it exists.

Revisión de seguridad para BMC/Panelin: OAuth, tokens, variables de entorno, CORS, HMAC, credenciales. No implementa cambios destructivos sin aprobación.

---

## When to Use

- Usuario pide "security review" o "revisión de seguridad"
- Pre-deploy: checklist de seguridad
- Cambios en OAuth, webhooks, o manejo de credenciales
- Auditoría de env vars, CORS, headers de seguridad

---

## Scope

### Áreas a revisar

| Área | Qué revisar |
|------|-------------|
| **OAuth** | ML_REDIRECT_URI, state validation, token storage |
| **Tokens** | tokenStore (file vs GCS), encryption, expiry |
| **Env vars** | .env.example vs .env, secrets en código |
| **CORS** | Orígenes permitidos, credentials |
| **Webhooks** | HMAC validation (Shopify), verify token |
| **Sheets** | GOOGLE_APPLICATION_CREDENTIALS, scope mínimo |
| **Headers** | X-Frame-Options, X-Content-Type-Options, CSP |

### Archivos clave

| Archivo | Rol |
|---------|-----|
| `server/tokenStore.js` | Almacenamiento de tokens |
| `server/config.js` | Env vars, config |
| `.env.example` | Variables documentadas (sin valores) |
| `server/index.js` | Security headers, webhook raw body |
| `server/routes/shopify.js` | HMAC validation |

---

## Workflow

1. **Read** config, tokenStore, routes que manejan auth.
2. **Check** .env.example: todas las vars sensibles documentadas sin valores.
3. **Verify** OAuth state validation, token encryption.
4. **Verify** webhook HMAC antes de procesar body.
5. **Report** hallazgos: alto/medio/bajo; recomendaciones; qué NO hacer.

---

## Principles

- **No modificar** producción sin aprobación explícita.
- **No exponer** secrets en logs, respuestas, o docs.
- **Citar** security-best-practices cuando aplique (lenguaje, framework).

---

## Reference

- security-best-practices (Codex): Revisión por lenguaje
- server/config.js: Configuración actual
- docs/ML-OAUTH-SETUP.md: Flujo OAuth ML
