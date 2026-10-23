---
name: add-route
description: >-
  Add or modify a Flask endpoint in the Lyrion Dashboard. Use this whenever a
  task adds a new URL/route, a JSON API endpoint, or a page — anything that
  registers a handler in `routes/`. Covers the repo's route → service → test
  layering, input validation, caching headers, security headers, i18n wiring,
  and the exact test pattern, so a new endpoint matches how `routes/` already
  works instead of reinventing the structure.
---

# Adding a Flask endpoint

This app layers strictly: **routes** parse the request and shape the response, **services** do the work (Lyrion calls, DB reads, lyrics), **tests** cover the route's contract. A route should read like a thin adapter — if a handler grows real logic, that logic belongs in a `services/` module.

## Where things go

- `routes/nowplaying.py` — the dashboard and its JSON endpoints (`/`, `/now-playing.json`, `/cover/...`, `/stats.json`, `/lyrics.json`, ...). Registered as `nowplaying_bp`.
- `routes/custom.py` — the `/files/` static server. Registered as `custom_bp`.
- Blueprints are created in the route module and registered in `app.py`'s `create_app()`. A brand-new blueprint must be both created **and** `register_blueprint`-ed there; adding a route to an existing blueprint needs no `app.py` change.

## The pattern

Handlers import service functions and translations at the top of the module — they do not build Lyrion payloads or open the DB inline:

```python
from services.lyrion import get_active_now_playing
from services.database import get_stats

@nowplaying_bp.route("/stats.json")
def stats_json():
    return jsonify(get_stats())
```

For anything with new domain logic, add a function to the relevant `services/` module first (see the `lyrion-api` skill for Lyrion calls, `services/database.py` for reads), then call it from the route.

## Validate untrusted input, always

Every value from the client is validated before it reaches a service or an upstream URL. The module keeps compiled regexes for this and clamps numbers:

```python
COVERID_RE = re.compile(r"[0-9a-fA-F]+")

@nowplaying_bp.route("/cover/<coverid>.jpg")
def cover(coverid):
    if not COVERID_RE.fullmatch(coverid):
        abort(404)
    size = request.args.get("size", type=int)
    if size is not None:
        size = min(max(size, 16), 512)   # clamp, don't trust
```

- Match path/query params against a `fullmatch` regex; `abort(404)` on junk.
- Clamp numeric `?limit=` / `?size=` params with `min(max(...))` so a hostile value can't blow up a query or a fetch (see `mosaic_covers_json`).
- Anything that fans out to a third party (the web lyrics search) sits behind `services.ratelimit` — `RateLimiter` per IP and `Cooldown` per track. Reuse those, don't roll your own throttle.

## Response conventions

- JSON endpoints return `jsonify(...)`. Keep the endpoint name suffix `.json`.
- Cacheable binary responses set `Cache-Control` explicitly, e.g. covers use `headers={"Cache-Control": "public, max-age=86400"}`.
- Security headers are applied app-wide by `set_security_headers` in `app.py` via `setdefault` (CSP `default-src 'self'`, `nosniff`, `SAMEORIGIN`). You get them for free. Only set a header on the response yourself to **override** the default for one route — as `/files/` does with `Content-Security-Policy: sandbox` for untrusted files.

## i18n for pages (not JSON)

HTML pages pick the language per-request and hand the whole translation dict to the template. JSON endpoints don't localize. See the `i18n` skill; the wiring is:

```python
from i18n import pick_lang, TRANSLATIONS

lang = pick_lang(request.accept_languages)
return render_template("nowplaying.html", lang=lang, t=TRANSLATIONS[lang], ...)
```

Any new user-facing string added to a template needs a key in **both** `fr` and `en` in `i18n.py`.

## Test the route's contract

Every endpoint gets a `tests/test_<name>_route.py` using `unittest` + `unittest.mock.patch`. The setup is deliberately duplicated per file so each stands alone (`# pylint: disable=duplicate-code`):

1. Set `LYRION_HOST`, `DB_DIR`, `DB_PERSIST_DIR` env vars via `os.environ.setdefault` **before** importing `app` (config reads them at import).
2. Build a client with `create_app().test_client()`.
3. Patch the **service functions the route imports** — patch them at the route module path, e.g. `@patch("routes.nowplaying.get_track_lyrics")`, never the real Lyrion server or DB.
4. Assert on status, JSON body, and that services were called with the right args (`mock.assert_called_with(...)`).

`tests/test_now_playing_route.py` is the reference example — mirror its shape.

## Keep the docs in sync

The public surface is documented in the READMEs and under `docs/`, and they must not drift from the app. Each page is an EN/FR pair edited together (see the `i18n` skill's documentation parity rule):

- **New/changed route** → the **Endpoints** table in `docs/endpoints.md` (Method / Route / Description).
- **New config env var** the route relies on → the table in `docs/configuration.md`, the single place operators discover it.
- **User-visible feature** → the **Features** list in the README.

## Checklist

1. Put domain logic in a `services/` function; keep the handler thin.
2. Register the route on the right blueprint (new blueprint → wire it in `app.py`).
3. Validate/clamp every client input; `abort()` on bad input.
4. Set `Cache-Control` on cacheable responses; rely on the global security headers unless overriding.
5. Localize page strings in both `fr` and `en`; leave JSON unlocalized.
6. Add `tests/test_<name>_route.py` patching the imported services.
7. Public surface changed? Update `docs/endpoints.md`, `docs/configuration.md` or the README Features list — each in **both** languages.
8. Run `python -m unittest discover` and `pylint app.py config.py i18n.py routes services scripts tests` — both gate CI (`.github/workflows/python-ci.yml`).
