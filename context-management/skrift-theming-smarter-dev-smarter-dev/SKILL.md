---
name: skrift-theming
description: "Skrift theming and template system — theme discovery, directory resolution, per-request theme switching via filter hooks, and template hierarchy."
---

# Skrift Theming & Templates

Skrift uses a three-tier directory hierarchy for templates and static files. Themes are optional packages that sit at the top of this hierarchy.

## Template Resolution Order

```
1. themes/<active>/templates/   (active theme — highest priority)
2. ./templates/                  (project-level overrides)
3. skrift/templates/             (package defaults — lowest priority)
```

Static files follow the same pattern with `static/` directories.

Without a theme, tiers 2 and 3 apply (the original two-tier system).

## Theme Directory Structure

```
themes/
  my-theme/
    theme.yaml          # optional metadata (name, description, version, author)
    templates/           # required — template overrides
    static/              # optional — static file overrides
    screenshot.png       # optional — preview for selection UI
```

A theme directory is valid if it has a `templates/` subdirectory.

## Theme Discovery API (`skrift/lib/theme.py`)

```python
from skrift.lib.theme import (
    ThemeInfo,           # dataclass with directory_name, name, description, version, author, templates_dir, static_dir, screenshot
    get_themes_dir,      # -> Path: ./themes/ relative to cwd
    themes_available,    # -> bool: themes/ dir exists with at least one valid theme
    discover_themes,     # -> list[ThemeInfo]: all valid themes, sorted by name
    get_theme_info,      # (name: str) -> ThemeInfo | None: lookup by directory name
)
```

### ThemeInfo Fields

| Field | Type | Description |
|-------|------|-------------|
| `directory_name` | str | Directory name (the theme identifier) |
| `name` | str | Display name from theme.yaml (or directory name) |
| `description` | str | From theme.yaml |
| `version` | str | From theme.yaml |
| `author` | str | From theme.yaml |
| `templates_dir` | Path | Path to `templates/` subdirectory |
| `static_dir` | Path \| None | Path to `static/` (None if absent) |
| `screenshot` | Path \| None | Path to `screenshot.png` (None if absent) |

## Theme Setting

The active theme is stored as `site_theme` in the settings table (key-value).

```python
from skrift.db.services.setting_service import (
    SITE_THEME_KEY,          # = "site_theme"
    get_cached_site_theme,   # -> str: cached theme name (empty = no theme)
)
```

The setting is included in `SITE_DEFAULTS` (default: `""`), loaded into the in-memory cache at startup, and invalidated when changed.

## Directory Resolution (`skrift/app_factory.py`)

```python
from skrift.app_factory import (
    get_template_directories_for_theme,  # (theme_name: str) -> list[Path]
    get_static_directories_for_theme,    # (theme_name: str) -> list[Path]
    get_template_directories,            # -> list[Path]: uses cached site_theme
    get_static_directories,              # -> list[Path]: uses cached site_theme
    update_template_directories,         # updates Jinja loader searchpath in-place
)
```

- `get_template_directories_for_theme("")` returns `[./templates/, skrift/templates/]`
- `get_template_directories_for_theme("my-theme")` returns `[themes/my-theme/templates/, ./templates/, skrift/templates/]`
- `update_template_directories()` is called after changing the theme in admin to hot-reload without restart

## Template Class (`skrift/lib/template.py`)

WordPress-style template resolver with theme support:

```python
from skrift.lib.template import Template

# Tries: page-about.html -> page.html
# Searches each directory in the resolution order
template = Template("page", "about")
response = template.render(TEMPLATE_DIR, theme_name="my-theme", page=page)
```

### Template.resolve(template_dir, theme_name="")

Searches `get_template_directories_for_theme(theme_name)` for the most specific candidate.

### Template.render(template_dir, theme_name="", **context)

Resolves and returns a `TemplateResponse`.

## Per-Request Theme Switching

The `RESOLVE_THEME` filter hook in `skrift/lib/hooks.py` allows overriding the theme per-request:

```python
from skrift.lib.hooks import RESOLVE_THEME  # = "resolve_theme"
```

Applied in `WebController` before template resolution:

```python
theme_name = get_cached_site_theme()
theme_name = await apply_filters(RESOLVE_THEME, theme_name, request)
# theme_name is then passed to Template.render()
```

### Plugin Examples

```python
from skrift.lib.hooks import filter

# Per-user theme preference via session
@filter("resolve_theme")
async def user_theme(theme_name, request):
    return request.session.get("user_theme", theme_name)

# Query parameter preview: ?theme=my-theme
@filter("resolve_theme")
async def theme_preview(theme_name, request):
    preview = request.query_params.get("theme")
    if preview:
        from skrift.lib.theme import get_theme_info
        if get_theme_info(preview):
            return preview
    return theme_name
```

## Scope

Themes only affect frontend templates. Admin (`admin/*`) and setup (`setup/*`) templates are unaffected because they use direct `TemplateResponse("admin/...")` paths.

## Template Globals

| Global | Type | Description |
|--------|------|-------------|
| `active_theme()` | str | Current theme name (empty if none) |
| `themes_available()` | bool | Whether `themes/` dir has valid themes |

## Setup Wizard Integration

- `SetupStep.THEME` in `skrift/setup/state.py` — appears between SITE and ADMIN steps
- Only shown when `themes_available()` returns True
- Step numbering is dynamic: 5 steps with themes, 4 without
- Routes: `GET /setup/theme`, `POST /setup/theme`, `GET /setup/theme-screenshot/{name}`

## Admin Integration

- `SettingsAdminController` in `skrift/admin/settings.py` — theme dropdown in site settings
- Only shown when `themes_available()` returns True
- Saves `site_theme` setting, calls `update_template_directories()` for instant switch
- Route: `GET /admin/theme-screenshot/{name}` for preview images

## Creating a Theme

1. Create `themes/<name>/templates/` (minimum requirement)
2. Override any template from `skrift/templates/` (e.g., `base.html`, `page.html`, `index.html`)
3. Optionally add `static/` for CSS/JS overrides
4. Optionally add `theme.yaml` for metadata
5. Optionally add `screenshot.png` for admin preview

## Key Files

| File | Purpose |
|------|---------|
| `skrift/lib/theme.py` | Theme discovery, `ThemeInfo` dataclass, metadata parsing |
| `skrift/lib/template.py` | `Template` class with theme-aware resolution |
| `skrift/app_factory.py` | Directory builders, `update_template_directories()`, Jinja env ref |
| `skrift/db/services/setting_service.py` | `SITE_THEME_KEY`, `get_cached_site_theme()` |
| `skrift/lib/hooks.py` | `RESOLVE_THEME` filter hook constant |
| `skrift/controllers/web.py` | Per-request theme resolution via filter hook |
| `skrift/asgi.py` | Template globals (`active_theme`, `themes_available`) |
| `skrift/setup/state.py` | `SetupStep.THEME`, `is_theme_configured()` |
| `skrift/setup/controller.py` | Theme setup step handlers |
| `skrift/admin/settings.py` | Admin theme selection + screenshot endpoint |
| `skrift/templates/setup/theme.html` | Setup wizard theme selection UI |
| `skrift/templates/admin/settings/site.html` | Admin settings theme dropdown |
