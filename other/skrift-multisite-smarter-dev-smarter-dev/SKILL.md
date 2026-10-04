---
name: skrift-multisite
description: "Skrift multi-subdomain site architecture — single deployment serving multiple subdomains with shared auth, database, and sessions via ASGI-level dispatch."
---

# Skrift Multisite Architecture

A single Skrift deployment serves multiple subdomains. Each subdomain gets its own Litestar app with its own controllers and theme. All share the same database engine, session cookie (scoped to `.example.com`), and middleware stack. Auth and admin live only on the primary domain.

## Request Flow

```
incoming request
  → AppDispatcher (setup vs main)
    → create_app()
      → SiteDispatcher (only when domain + sites configured)
        ├── example.com       → primary Litestar app
        ├── blog.example.com  → blog Litestar app
        └── docs.example.com  → docs Litestar app
```

## Configuration (`app.yaml`)

```yaml
domain: example.com              # required for multisite

controllers:                     # primary site controllers
  - skrift.controllers.auth:AuthController
  - skrift.admin.controller:AdminController
  - skrift.controllers.web:WebController

sites:
  blog:
    subdomain: blog              # → blog.example.com
    controllers:
      - controllers.blog:BlogController
    theme: blog-theme            # optional, falls back to primary theme
    page_types:                  # optional, site-specific page types
      - name: post
        plural: posts
        icon: pen-tool

session:
  cookie_domain: .example.com   # required for cross-subdomain sessions

auth:
  redirect_base_url: https://example.com
  allowed_redirect_domains:
    - "*.example.com"            # required for post-login redirect to subdomains
```

Three settings are critical for multisite: `domain`, `session.cookie_domain` (leading dot), and `auth.allowed_redirect_domains` with a wildcard.

## Config Schema (`skrift/config.py`)

```python
from skrift.config import SiteConfig, PageTypeConfig

# SiteConfig fields:
#   subdomain: str           — subdomain prefix
#   controllers: list[str]   — controller import specs
#   theme: str               — theme name (default: "")
#   page_types: list[PageTypeConfig]  — site-specific page types (default: [])

# Added to Settings:
#   domain: str = ""
#   sites: dict[str, SiteConfig] = {}
```

Parsed in `get_settings()` from the `domain` and `sites` keys in app.yaml.

## SiteDispatcher (`skrift/middleware/site_dispatch.py`)

ASGI middleware that extracts the subdomain from the `Host` header and dispatches to the matching Litestar app:

```python
from skrift.middleware.site_dispatch import SiteDispatcher

# Created automatically in create_app() when settings.sites is non-empty
dispatcher = SiteDispatcher(
    primary_app=primary_asgi,
    site_apps={"blog": blog_app, "docs": docs_app},
    domain="example.com",
    force_subdomain="",  # set via --subdomain CLI flag
)
```

### Helper functions

- `_extract_host(scope)` — extracts host from ASGI scope headers, strips port, lowercases
- `_get_subdomain(host, domain)` — returns subdomain prefix or empty string

### Dispatch logic

1. Non-HTTP scopes (websocket, lifespan) → primary app
2. If `force_subdomain` is set → use it directly (skips Host header extraction)
3. Otherwise extract host, compute subdomain
4. If subdomain matches a site app → route to it, set `scope["state"]["site_name"]`
5. Otherwise → route to primary app, set `scope["state"]["site_name"] = ""`

### Lifespan forwarding

`_handle_lifespan()` sends startup/shutdown to all apps (primary + sites) in parallel, waits for all to complete.

## Site App Builder (`skrift/asgi.py`)

### `load_site_controllers(specs: list[str]) -> list`

Like `load_controllers()` but takes explicit import specs and skips AdminController auto-expansion.

### `_build_site_app(...) -> ASGIApp`

Creates a lightweight Litestar app for a subdomain site. Receives shared configs from `create_app()`:

**Shared with primary:**
- `db_config` (SQLAlchemyAsyncConfig — same engine)
- `session_config` (CookieBackendConfig — same cookie domain)
- `csrf_config`
- Security headers middleware
- Rate limit middleware
- User-defined middleware from app.yaml

**Site-specific:**
- Controllers from `site_config.controllers`
- Template directories from `get_template_directories_for_theme(site_config.theme)`
- Template globals: `login_url()` → `https://{domain}/auth/login`
- `site_name()` returns the site config key name
- `active_theme()` returns the site's configured theme

**Excluded from site apps:**
- AdminController and sub-controllers
- AuthController (login on primary domain)
- NotificationsController
- Setup routes

### `create_app()` wiring

At the end of `create_app()`, after building the primary app:

```python
forced_subdomain = os.environ.get("SKRIFT_SUBDOMAIN", "")
need_dispatch = (settings.sites or subdomain_page_types) and (settings.domain or forced_subdomain)

if need_dispatch:
    site_apps = {}
    for name, site_cfg in settings.sites.items():
        site_apps[site_cfg.subdomain] = _build_site_app(...)

    return SiteDispatcher(
        primary_app=primary_asgi,
        site_apps=site_apps,
        domain=settings.domain or "localhost",
        force_subdomain=forced_subdomain,
    )

return primary_asgi  # no sites configured — single-site behavior
```

The `SKRIFT_SUBDOMAIN` env var is set by the `--subdomain` CLI flag. When set, `SiteDispatcher` routes all HTTP requests to that subdomain's app regardless of the `Host` header.

## Auth Flow from Subdomain

1. User visits `blog.example.com`, clicks login link
2. Link goes to `https://example.com/auth/login?next=https://blog.example.com/`
3. OAuth completes on primary domain
4. Session cookie set with `domain=.example.com` (readable by all subdomains)
5. Redirect back to `https://blog.example.com/` — user is logged in

Template global: `{{ login_url() }}?next={{ request.url }}`

No code changes needed in auth — `allowed_redirect_domains: ["*.example.com"]` handles it.

## Template Globals (Site Apps)

| Global | Value |
|--------|-------|
| `site_name()` | Site config key name (e.g., `"blog"`) |
| `site_tagline()` | From DB settings cache (shared) |
| `active_theme()` | Site's configured theme |
| `themes_available()` | Always `False` (no theme switching UI on subdomains) |
| `login_url()` | `https://{domain}/auth/login` |
| `static_url(path)` | Same hasher as primary |
| `theme_url(path)` | Resolves via site's theme |

## Local Development with `--subdomain`

Use the `--subdomain` CLI option to serve a single subdomain site on its own port:

```bash
skrift serve --subdomain blog --port 8081
```

All HTTP requests to `localhost:8081` are routed to the blog subdomain's app. No `/etc/hosts` or local DNS changes needed. Run multiple instances on different ports to test all subdomains simultaneously.

## Backward Compatibility

No `sites:` key = existing single-site behavior. `SiteDispatcher` is only instantiated when both `domain` and `sites` are configured (or when `--subdomain` is used).

## Project Structure

```
my-site/
├── app.yaml
├── controllers/
│   ├── web.py            # primary
│   ├── blog.py           # blog.example.com
│   └── docs.py           # docs.example.com
├── themes/
│   ├── main-theme/
│   ├── blog-theme/
│   └── docs-theme/
├── templates/            # shared overrides
└── static/               # shared assets
```

## Key Files

| File | Purpose |
|------|---------|
| `skrift/config.py` | `SiteConfig` model, `domain`/`sites` on `Settings` |
| `skrift/middleware/site_dispatch.py` | `SiteDispatcher` ASGI middleware, host/subdomain extraction |
| `skrift/asgi.py` | `load_site_controllers()`, `_build_site_app()`, `SiteDispatcher` wiring in `create_app()` |
| `skrift/app_factory.py` | `get_template_directories_for_theme()` — reused by site apps |
| `skrift/controllers/auth.py` | `_is_safe_redirect_url()` — handles `*.example.com` wildcards |
| `tests/test_site_dispatch.py` | SiteDispatcher unit tests |
| `tests/test_site_config.py` | SiteConfig and Settings parsing tests |
