---
name: Authentication & Security
description: Автоматизация JWT аутентификации, Telegram OAuth и security middleware
version: 3.0.0
author: Family Budget Team
tags: [auth, jwt, telegram-oauth, security, middleware]
dependencies: []
architecture_refs:
  - $ref: ../../docs/architecture/functionality/authentication.yaml
  - $ref: ../../docs/architecture/endpoints/auth.yaml
  - $ref: ../../docs/architecture/flows/telegram-oauth.yaml
---

# Authentication & Security Skill

Автоматизация JWT аутентификации, Telegram OAuth и security middleware.

## When to Use

- Добавить JWT authentication к endpoint
- Реализовать Telegram Login Widget
- Создать security middleware
- Проверить CORS, CSP, HSTS headers
- Добавить admin-only endpoint protection

## Architecture Context

**References:**
- Functionality: [$ref](../../docs/architecture/functionality/authentication.yaml)
- Endpoints: [$ref](../../docs/architecture/endpoints/auth.yaml)
- Telegram OAuth Flow: [$ref](../../docs/architecture/flows/telegram-oauth.yaml)

**Key Patterns:**
- **JWT in httpOnly cookies** - Security best practice
- **Telegram OAuth** - Telegram Login Widget
- **Admin-only operations** - Dimension tables CREATE/UPDATE/DELETE
- **Shared Budget** - NO user isolation for facts

## Commands

### Command: protect-endpoint

**Usage:**
```
Добавь JWT authentication к endpoint <endpoint-path> с ролью <admin|user>.
```

**What It Does:**
1. Add `CurrentUser` dependency to endpoint
2. Add admin check if needed (for dimension operations)
3. Ensure NO user_id filtering for Shared Budget

**Template Reference:**
- `templates/jwt-endpoint.py` - JWT protected endpoint template

**Example:**
```python
from backend.app.core.dependencies import CurrentUser

@router.get("/protected")
async def protected_endpoint(current_user: CurrentUser):
    # Admin-only check (for dimension tables)
    if not current_user.is_admin:
        raise HTTPException(403, "Admin access required")

    # ✅ CORRECT - Shared Budget: NO user_id filtering
    stmt = select(BudgetFact)  # All users see all facts
```

### Command: add-telegram-oauth

**Usage:**
```
Реализуй Telegram Login Widget для аутентификации.
```

**What It Does:**
1. Create Telegram OAuth endpoint (/auth/telegram)
2. Verify Telegram hash signature
3. Create/update user in database
4. Generate JWT tokens (access + refresh)
5. Set httpOnly cookies

**Template Reference:**
- `templates/telegram-oauth.py` - Complete OAuth flow

### Command: create-middleware

**Usage:**
```
Создай security middleware для <purpose>.
```

**What It Does:**
Creates middleware for JWT validation, CORS, CSP, HSTS

**Template Reference:**
- `templates/middleware.py` - Security middleware template

## Validation Checklist

- [ ] CurrentUser dependency added to endpoints
- [ ] Admin check for dimension CREATE/UPDATE/DELETE
- [ ] NO user_id filtering for fact tables (Shared Budget)
- [ ] HTTPException 401/403 used correctly
- [ ] JWT cookie validation works
- [ ] Telegram OAuth hash verified
- [ ] CORS origins configured correctly
- [ ] CSP headers configured

Reference: `_shared/validation-logic.md#3-shared-budget-model-consistency`

## Common Mistakes

**Filtering facts by user_id:**
- **Symptom**: Users can't see each other's transactions (breaks Shared Budget)
- **Fix**: Remove `.where(BudgetFact.user_id == current_user.id)`
- **Reference**: `_shared/validation-logic.md#3`

**Not verifying Telegram hash:**
- **Symptom**: Authentication bypass vulnerability
- **Fix**: Always verify hash with bot token

**JWT in localStorage:**
- **Symptom**: XSS vulnerability
- **Fix**: Use httpOnly cookies (already implemented)

## Related Skills

- **api-development**: Protect endpoints after creation

## Quick Links

- Telegram OAuth Flow: [$ref](../../docs/architecture/flows/telegram-oauth.yaml)
- Authentication Docs: [$ref](../../docs/architecture/functionality/authentication.yaml)
