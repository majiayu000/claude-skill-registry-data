---
name: skrift-auth
description: "Skrift authentication and authorization — OAuth providers, session management, role-based guards and permissions."
---

# Skrift Auth & Authorization

Skrift uses OAuth for authentication and a guard system for role-based authorization.

## OAuth Flow

```
/auth/{provider}/login → Provider → /auth/{provider}/callback → Session created
```

Providers configured in `app.yaml`:

```yaml
auth:
  redirect_base_url: "https://example.com"
  allowed_redirect_domains: []
  providers:
    google:
      client_id: $GOOGLE_CLIENT_ID
      client_secret: $GOOGLE_CLIENT_SECRET
      scopes: ["openid", "email", "profile"]
```

Available providers: `google`, `github`, `microsoft`, `discord`, `facebook`, `twitter`, `skrift`.

The `skrift` provider authenticates against another Skrift instance's OAuth2 server. See `/skrift-oauth2` for hub/spoke setup.

## Session Management

Client-side encrypted cookies (Litestar's CookieBackendConfig):
- 7-day expiry
- HttpOnly, Secure (in production), SameSite=Lax

## Guard System

Protect routes with `auth_guard`, `Permission`, and `Role` guards:

```python
from skrift.auth import auth_guard, Permission, Role

class AdminController(Controller):
    path = "/admin"
    guards = [auth_guard, Permission("manage-pages")]

    @get("/")
    async def admin_dashboard(self) -> TemplateResponse:
        return TemplateResponse("admin/dashboard.html")
```

### Combining Guards

```python
# AND: Both required
guards = [auth_guard, Permission("edit") & Permission("publish")]

# OR: Either sufficient
guards = [auth_guard, Role("admin") | Role("editor")]
```

### Per-Route Guards

```python
class ArticleController(Controller):
    path = "/articles"
    guards = [auth_guard]  # All routes require auth

    @get("/")
    async def list_articles(self, db_session: AsyncSession):
        # Anyone authenticated can list
        ...

    @post("/", guards=[Permission("create-articles")])
    async def create_article(self, db_session: AsyncSession, data: ArticleCreate):
        # Only users with create-articles permission
        ...

    @delete("/{id:uuid}", guards=[Permission("delete-articles")])
    async def delete_article(self, db_session: AsyncSession, id: UUID):
        # Only users with delete-articles permission
        ...
```

## Built-in Roles

| Role | Permissions | Notes |
|------|-------------|-------|
| `admin` | `administrator` | Bypasses all permission checks |
| `editor` | Can manage pages | |
| `author` | Can view drafts | |
| `moderator` | Can moderate content | |

## Custom Role Registration

```python
from skrift.auth import register_role

# Register before database sync (app startup)
register_role(
    "contributor",
    "create-articles",
    "edit-own-articles",
    display_name="Contributor",
    description="Can create and edit their own articles",
)

register_role(
    "reviewer",
    "view-drafts",
    "approve-articles",
    display_name="Reviewer",
    description="Can review and approve articles",
)
```

## Controller with Session Access

```python
from litestar import Request

class AuthController(Controller):
    path = "/auth"

    @get("/profile")
    async def profile(
        self, request: Request, db_session: AsyncSession
    ) -> TemplateResponse:
        user_id = request.session.get("user_id")
        if not user_id:
            raise NotAuthorizedException()

        user = await user_service.get_by_id(db_session, UUID(user_id))
        return TemplateResponse("auth/profile.html", context={"user": user})

    @post("/logout")
    async def logout(self, request: Request) -> Redirect:
        request.session.clear()
        return Redirect("/")
```

## OAuth Token Persistence

On every login, `access_token` and `refresh_token` from the provider's token response are saved on the `OAuthAccount` record:

```python
# In find_or_create_oauth_user():
oauth_account.access_token = tokens.get("access_token")
oauth_account.refresh_token = tokens.get("refresh_token")
```

The `tokens` kwarg on `find_or_create_oauth_user()` accepts the raw token dict from the OAuth exchange. Both fields are `String(2048)`, nullable.

Tokens are refreshed (overwritten) on every login. Skrift does not auto-refresh expired tokens — apps must handle refresh themselves.

## Key Files

| File | Purpose |
|------|---------|
| `skrift/auth/` | Guards, roles, permissions |
| `skrift/controllers/auth.py` | OAuth login/callback controller |
| `skrift/auth/oauth_account_service.py` | `find_or_create_oauth_user()` with token persistence |
| `skrift/db/models/user.py` | `User`, `Role` models |
| `skrift/db/models/oauth_account.py` | `OAuthAccount` model (`access_token`, `refresh_token` fields) |
