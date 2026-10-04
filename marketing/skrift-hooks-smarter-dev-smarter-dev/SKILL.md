---
name: skrift-hooks
description: "Hook/filter extensibility system for Skrift CMS — WordPress-style actions and filters for decoupled plugin-like architecture."
---

# Skrift Hook/Filter System

Skrift provides a WordPress-inspired hook system for extensibility. **Actions** trigger side effects (no return value). **Filters** transform and return values through a chain of handlers.

## Core API

```python
from skrift.lib.hooks import hooks, action, filter
```

### Registration — Decorators (auto-register on import)

```python
@action("after_page_save", priority=10)
async def invalidate_cache(page, is_new: bool):
    """Clear cache when page is saved."""
    cache.delete(f"page:{page.slug}")

@filter("page_seo_meta", priority=10)
async def add_default_author(meta: dict, page) -> dict:
    """Add default author to SEO meta."""
    if "author" not in meta:
        meta["author"] = "Site Author"
    return meta
```

### Registration — Direct (runtime)

```python
hooks.add_action("hook_name", callback, priority=10)
hooks.add_filter("hook_name", callback, priority=10)
```

### Triggering

```python
# Actions (fire and forget)
await hooks.do_action("hook_name", arg1, arg2)

# Filters (chain transforms — each handler receives the previous return value)
result = await hooks.apply_filters("hook_name", initial_value, arg1)
```

### Priority

Lower numbers execute first. Default is 10.

## Built-in Hook Points

**Actions:**

| Hook | Arguments | Fired when |
|------|-----------|------------|
| `before_page_save` | `(page, is_new)` | Before saving a page |
| `after_page_save` | `(page, is_new)` | After saving a page |
| `before_page_delete` | `(page,)` | Before deleting a page |
| `after_page_delete` | `(page,)` | After deleting a page |
| `NOTIFICATION_SENT` | `(notification,)` | After a notification is sent |
| `NOTIFICATION_DISMISSED` | `(notification_id,)` | After a notification is dismissed |

**Filters:**

| Hook | Signature | Purpose |
|------|-----------|---------|
| `page_seo_meta` | `(meta, page) → meta` | Modify SEO metadata dict |
| `page_og_meta` | `(meta, page) → meta` | Modify OpenGraph metadata dict |
| `sitemap_urls` | `(urls,) → urls` | Modify sitemap URL list |
| `sitemap_page` | `(page_data, page) → page_data` | Modify single sitemap entry |
| `robots_txt` | `(content,) → content` | Modify robots.txt content |
| `template_context` | `(context,) → context` | Modify template context dict |
| `resolve_theme` | `(theme_name, request) → theme_name` | Override active theme per-request (see `/skrift-theming`) |
| `form_{name}_validated` | `(data,) → data` | Modify form data after validation (form-specific) |
| `form_validated` | `(data, name) → data` | Modify form data after validation (global) |

## Patterns

### Custom Hook Points

```python
# Define hook constants
MY_BEFORE_SAVE = "my_before_save"
MY_AFTER_SAVE = "my_after_save"
MY_DATA_FILTER = "my_data_filter"

# Trigger in service
async def save_thing(db_session: AsyncSession, data: dict) -> Thing:
    data = await hooks.apply_filters(MY_DATA_FILTER, data)

    thing = Thing(**data)
    await hooks.do_action(MY_BEFORE_SAVE, thing)

    db_session.add(thing)
    await db_session.commit()

    await hooks.do_action(MY_AFTER_SAVE, thing)
    return thing
```

### Service with Hooks

```python
from skrift.lib.hooks import hooks

BEFORE_ITEM_SAVE = "before_item_save"
AFTER_ITEM_SAVE = "after_item_save"

async def create(db_session: AsyncSession, name: str) -> Item:
    item = Item(name=name)
    await hooks.do_action(BEFORE_ITEM_SAVE, item, is_new=True)

    db_session.add(item)
    await db_session.commit()
    await db_session.refresh(item)

    await hooks.do_action(AFTER_ITEM_SAVE, item, is_new=True)
    return item
```

### Adding Global Template Variables

```python
@filter("template_context", priority=20)
async def add_global_vars(context: dict) -> dict:
    context["current_year"] = datetime.now().year
    context["version"] = "1.0.0"
    return context
```

### Testing Hooks

```python
from skrift.lib.hooks import hooks

async def test_hook_called(db_session):
    called_with = []

    async def track_save(page, is_new):
        called_with.append((page.title, is_new))

    hooks.add_action("after_page_save", track_save)

    try:
        await page_service.create(db_session, slug="test", title="Test")

        assert len(called_with) == 1
        assert called_with[0] == ("Test", True)
    finally:
        hooks.remove_action("after_page_save", track_save)
```

## Key Files

| File | Purpose |
|------|---------|
| `skrift/lib/hooks.py` | Hook registry, `@action`/`@filter` decorators, `hooks` singleton |
