---
name: portal-auth-jwt
description: Implement JWT authentication and role-based authorization with PyJWT HS256, pwdlib Argon2, OAuth2PasswordBearer, and SecurityScopes for roles operativo/analista/directivo/admin. Use when touching /api/auth/token, /api/users, get_current_user, the permission matrix, bearer propagation to agent tools, or the Nuxt auth middleware.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal Auth JWT Skill (guía oficial FastAPI, verificada C7)

Auth module: `! ls backend/app/core/auth.py 2>/dev/null || echo "not created yet"`

## Rules — NON-NEGOTIABLE

- Hashing con pwdlib `PasswordHash.recommended()` (argon2id); en login con usuario inexistente SIEMPRE verificar contra un hash dummy (anti timing attack).
- JWT con PyJWT HS256: `SECRET_KEY` de 32 bytes (`openssl rand -hex 32`, en `.env.local` dev / Secret Manager prod), expiración 30 min, claims `sub` (username) + `scope` (rol). SIN refresh tokens (decisión de alcance: re-login limpio).
- Roles como scopes del token: `operativo | analista | directivo | admin`. Endpoints los exigen con `Security(get_current_user, scopes=[...])` → 401 sin/mal token con `WWW-Authenticate: Bearer`, 403 autenticado sin permiso.
- Usuario `disabled` → rechazado en `get_current_user` (patrón `get_current_active_user`): el soft delete surte efecto en el siguiente request.
- `/api/chat` propaga el Bearer DEL USUARIO a cada tool call del agente: el agente jamás ve datos que el usuario no puede ver.
- CRUD `/api/users` solo `admin`; un admin no puede desactivarse ni degradarse a sí mismo; `username`/`email` duplicado → 409; contraseñas jamás en respuestas ni logs.
- Frontend: JWT en cookie httpOnly; middleware Nuxt redirige a login sin sesión y oculta módulos por rol.

## Matriz de permisos (docs/security.md)

| Recurso | operativo | analista | directivo | admin |
|---------|-----------|----------|-----------|-------|
| `/api/catalog/search` | X | X | X | X |
| Consultas puntuales `/api/{silo}` | X | X | X | X |
| Agregaciones/cruces `/api/{silo}` | — | X | X | X |
| `/api/export` | — | X | X | X |
| Resúmenes directivos | — | — | X | X |
| `/api/users` CRUD | — | — | — | X |
| `/api/chat` | X (tools limitadas por su scope) | X | X | X |

## Núcleo de auth (backend/app/core/auth.py)

```python
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from pwdlib import PasswordHash
from app.core.config import settings
from app.models.user import AppUser, Role
password_hash = PasswordHash.recommended()          # argon2id
DUMMY_HASH = password_hash.hash("dummy-timing-guard")
ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES = "HS256", 30
ROLE_HIERARCHY = {"operativo": 0, "analista": 1, "directivo": 2, "admin": 3}  # implicit hierarchy

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token",
                                     scopes={r.value: f"Role {r.value}" for r in Role})

async def authenticate_user(username: str, password: str) -> AppUser | None:
    user = await UserService.get_by_username(username)
    if user is None:
        password_hash.verify(password, DUMMY_HASH)   # constant-time even if user missing
        return None
    return user if password_hash.verify(password, user.hashed_password) else None

def create_access_token(user: AppUser) -> str:
    payload = {"sub": user.username, "scope": user.role.value,
               "exp": datetime.now(timezone.utc)
                      + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(security_scopes: SecurityScopes,
                           token: str = Depends(oauth2_scheme)) -> UserOut:
    """Decode JWT, enforce active user and role hierarchy against required scopes."""
    www_auth = f'Bearer scope="{security_scopes.scope_str}"' if security_scopes.scopes else "Bearer"
    cred_exc = HTTPException(status.HTTP_401_UNAUTHORIZED, "Could not validate credentials",
                             headers={"WWW-Authenticate": www_auth})
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username, token_role = payload["sub"], payload["scope"]
    except (jwt.InvalidTokenError, KeyError):
        raise cred_exc
    user = await UserService.get_by_username(username)
    if user is None or user.disabled:                # get_current_active_user pattern
        raise cred_exc                               # disabled -> effective next request
    for required in security_scopes.scopes:
        if ROLE_HIERARCHY[token_role] < ROLE_HIERARCHY[required]:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Not enough permissions",
                                headers={"WWW-Authenticate": www_auth})
    return UserOut.model_validate(user)
```

## Token endpoint

```python
# backend/app/api/auth.py
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = await authenticate_user(form.username, form.password)
    if user is None:
        raise HTTPException(401, "Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    return Token(access_token=create_access_token(user), token_type="bearer")
```

## Reglas CRUD /api/users

```python
@router.patch("/{user_id}", response_model=UserOut)
async def update_user(user_id: uuid.UUID, body: UserUpdate,
                      admin: UserOut = Security(get_current_user, scopes=["admin"])):
    if user_id == admin.id and body.role is not None and body.role != Role.admin:
        raise HTTPException(409, "An admin cannot demote themselves")
    return await UserService.update(user_id, body)   # hashes password; unique clash -> 409
# DELETE = soft delete (disabled=true); admin self-deactivation -> 409
```

## Propagación del Bearer a las tools del agente

```python
# ml/agent/tools/base.py — every ADK tool wraps a governed endpoint with the USER token
async def call_portal_api(path: str, payload: dict, bearer: str) -> dict:
    async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
        r = await client.post(path, json=payload, headers={"Authorization": f"Bearer {bearer}"})
        r.raise_for_status()      # 403 here means the USER lacks the scope; surface it
        return r.json()
```

## Frontend: cookie httpOnly + middleware Nuxt

```typescript
// frontend/app/middleware/auth.global.ts — httpOnly cookie read server-side by the composable
export default defineNuxtRouteMiddleware((to) => {
  const session = useUserSession()
  if (!session.value.loggedIn && to.path !== '/login') return navigateTo('/login')
  const required = to.meta.roles as string[] | undefined
  if (required && !required.includes(session.value.role)) return navigateTo('/')
})
```

## Pruebas obligatorias (QA gate)

- Login ok / credenciales malas / usuario disabled → 400/401; token expirado o manipulado → 401 con `WWW-Authenticate: Bearer`.
- Matriz 401/403 parametrizada por rol y endpoint (`pytest.mark.parametrize`).
- CRUD: duplicados 409, auto-degradación/desactivación de admin 409, soft delete efectivo en el siguiente request.
