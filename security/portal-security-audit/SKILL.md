---
name: portal-security-audit
description: Run the pre-PR and pre-deploy security checklist for the Portal Centralizado de Datos Financieros — endpoint scope coverage, 401/403 permission matrix, admin self-protection, secret and prompt leakage scans, timing-attack defenses, and scope creep guard (R11). Use before merging auth-related PRs and before every deploy.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal Security Audit Skill

## Rules — NON-NEGOTIABLE

- 100% de endpoints de datos con `Security(get_current_user, scopes=[...])`. Un endpoint de datos sin scopes bloquea el PR.
- Matriz de permisos verificada por pruebas: 401 sin/mal token (`WWW-Authenticate: Bearer`), 403 autenticado sin permiso, parametrizado por los 4 roles (`docs/security.md` es la fuente).
- Un admin NO puede desactivarse ni degradarse a sí mismo; `username`/`email` duplicados → 409.
- Contraseñas jamás en respuestas, logs ni trazas; prompts crudos jamás en logs — solo `llm.prompt_hash` SHA-256.
- Secrets fuera del repo: `.env.local` (gitignored) en dev, Secret Manager en prod. Pydantic Settings estricto: la app no arranca sin `DATABASE_URL`/`GEMINI_API_KEY`/`JWT_SECRET_KEY`.
- Login con hash dummy anti-timing: si el usuario no existe se verifica igualmente contra un hash falso (pwdlib), para que la duración no delate usernames válidos.
- JWT en cookie httpOnly (nunca localStorage); CORS restringido a los orígenes del frontend.
- El agente hereda el Bearer del usuario en cada tool call: jamás un token de servicio con más permisos.

## Scope creep guard (R11)

FUERA del MVP — rechazar en review y documentar como trabajo futuro en `docs/security.md`:

| Propuesta | Veredicto |
|-----------|-----------|
| Refresh tokens | NO — expiración 30 min + re-login limpio (decisión de alcance por escrito) |
| Recuperación de contraseña | NO — el admin resetea vía CRUD de usuarios |
| OAuth/SSO externo | NO — OAuth2 password flow local únicamente |
| RLS por fila en PostgreSQL | NO — RBAC por scopes a nivel endpoint basta para el MVP |

## Verificación de cobertura de scopes

```bash
# Todo router de datos debe usar Security(...) — el diff de estas listas debe ser vacio
grep -rLn "Security(get_current_user" backend/app/api/ \
  --include="*.py" | grep -v "auth.py\|__init__\|healthz" \
  && echo "FAIL: router sin scopes" || echo "OK"

# Ningun endpoint con Depends pelado donde deberia haber scopes
grep -rn "Depends(get_current_user)" backend/app/api/ && echo "WARN: revisar si requiere scopes"
```

## Scans de fuga

```bash
# scripts/security_audit.sh
set -euo pipefail

echo "=== 1. Secrets en repo ==="
gitleaks detect --no-banner --redact

echo "=== 2. Contrasenas/prompts en logs ==="
grep -rEn "logger\.\w+\(.*(password|hashed_password|prompt=|messages=)" backend/ ml/ \
  && exit 1 || echo "OK"

echo "=== 3. Password en response models ==="
grep -rn "hashed_password" backend/app/models/ | grep -i "out\|response\|public" \
  && exit 1 || echo "OK"

echo "=== 4. Deps con CVEs ==="
poetry run pip-audit --strict && pnpm audit --audit-level=high

echo "=== 5. Ruff security ==="
poetry run ruff check --select=S backend/ ml/
```

## Hash dummy anti-timing (patrón exigido en login)

```python
# backend/app/core/auth.py
DUMMY_HASH = password_hash.hash("dummy-timing-guard")

async def authenticate(username: str, password: str) -> AppUser | None:
    user = await get_user(username)
    hashed = user.hashed_password if user else DUMMY_HASH
    valid = password_hash.verify(password, hashed)   # SIEMPRE se verifica algo
    return user if (user and valid and not user.disabled) else None
```

## Reglas de negocio del CRUD admin

```python
# Un admin no puede auto-degradarse ni auto-desactivarse
if target.id == current_user.id and (body.role != "admin" or body.disabled):
    raise HTTPException(status_code=409, detail="admin_cannot_self_demote")
```

Soft delete únicamente (`disabled = true`); cambios de rol surten efecto en el siguiente request (`get_current_user` valida usuario activo).

## Pre-PR / Pre-Deploy Checklist

- [ ] `gitleaks` sin findings; `.env.local` gitignored
- [ ] 100% endpoints de datos con `Security(scopes=...)` (grep de cobertura limpio)
- [ ] Matriz 401/403 por rol en verde (skill `portal-testing`)
- [ ] Auto-degradación/desactivación de admin bloqueada (409) y probada
- [ ] 409 en `username`/`email` duplicados
- [ ] Cero contraseñas en respuestas/logs/trazas; cero prompts crudos (solo hash)
- [ ] Hash dummy anti-timing presente en login
- [ ] Cookie httpOnly + CORS restringido a orígenes conocidos
- [ ] Tools del agente propagan el Bearer del usuario (sin token de servicio)
- [ ] `pip-audit` / `pnpm audit` sin Critical/High; `ruff --select=S` limpio
- [ ] Sin scope creep R11 (refresh/recovery/OAuth/RLS) — futuro en `docs/security.md`
