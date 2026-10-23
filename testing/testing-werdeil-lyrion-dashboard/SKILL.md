---
name: testing
description: >-
  Write or fix a test in the Lyrion Dashboard's suite. Use this whenever a task
  adds a test, changes one, or asks why the suite fails — anything touching
  `tests/`. Covers the standalone-per-file scaffolding, the env-before-import
  rule, where to patch (the route/service the code under test imports), the
  cache-and-clock testing pattern, and how to run one test vs the whole suite.
  Reach for it any time you touch `tests/` so new tests match the existing
  shape instead of re-inventing setup.
---

# Testing conventions

Tests use **`unittest` + `unittest.mock.patch`** (no pytest, no fixtures library). They run in CI via `python -m unittest discover` from the repo root (`.github/workflows/python-ci.yml`), and must never touch a real Lyrion server or a real SQLite DB.

## Run them

```bash
python -m unittest discover                       # whole suite (what CI runs)
python -m unittest tests.test_now_playing_route   # one file
python -m unittest tests.test_now_playing_route.NowPlayingKnownTest          # one case
python -m unittest tests.test_now_playing_route.NowPlayingKnownTest.test_no_known_includes_lyrics  # one method
```

## The standalone-file rule

Each `tests/test_*.py` stands entirely on its own — no shared conftest, no base class. That means the env scaffolding is **duplicated in every file on purpose**, marked `# pylint: disable=duplicate-code`. Don't try to factor it out; the duplication is the design (a test file can be read and run in isolation).

## Env before import

`config.py` reads env vars **at import time**, so the config vars must be set **before** anything imports `app`. Every test file opens the same way:

```python
import os, tempfile, unittest
from unittest.mock import patch

os.environ.setdefault("LYRION_HOST", "http://localhost:9000")
os.environ.setdefault("DB_DIR", tempfile.mkdtemp())
os.environ.setdefault("DB_PERSIST_DIR", tempfile.mkdtemp())

# pylint: disable=wrong-import-position
from app import create_app
```

Build a client per test with `create_app().test_client()` in `setUp`.

## Patch where the code *imports* the name, not where it's defined

Routes do `from services.database import get_track_lyrics`, so the name to patch is `routes.nowplaying.get_track_lyrics` — the route module's binding — **not** `services.database.get_track_lyrics`. Patching the definition site misses the already-imported reference the route holds.

```python
@patch("routes.nowplaying.get_track_lyrics", return_value="la la la")
@patch("routes.nowplaying.get_active_now_playing", return_value=dict(NOW))
class NowPlayingKnownTest(unittest.TestCase):
    ...
```

- Assert on **status, JSON body, and how the service was called** (`mock.assert_called_once_with(42)`, `mock.assert_called_with(selected_id=None)`).
- For a service test, patch one layer down instead — e.g. `test_lyrion_request.py` patches the HTTP session, `test_get_track_lyrics.py` builds a temp SQLite DB.

## What to cover, by layer

- **Routes** (`test_*_route.py`) — the request/response contract: input validation and clamping (`test_files_route.py`, `test_cover_route.py`), the `?known=` / `?player=` behaviours (`test_now_playing_route.py`), security headers (`test_security_headers.py`). Patch the services the route imports.
- **Services** — the logic itself: the lyrics cache and TTLs (`test_lyrics_cache.py`), verification (`test_lyrics_verify.py`), the rate limiter/cooldown (`test_ratelimit.py`), the now-playing snapshot cache.

## Asserting on logs

`tests/__init__.py` pins `LOG_LEVEL=CRITICAL` so the suite's output stays readable. A diagnostic log line worth guarding is asserted with `assertLogs`, which raises the level of the logger it names, so it works despite that pin:

```python
with self.assertLogs("services.lyrics", level="INFO") as captured:
    L.fetch_lyrics("1", "A", "T")
self.assertTrue(any("-> lrclib" in line for line in captured.output))
```

Match a stable fragment of the message, not the whole formatted line (`tests/test_logging.py`).

## Testing caches and the clock

Several services cache behind a lock and age values by wall-clock time (`get_active_now_playing`, the lyrics cache, `RateLimiter`/`Cooldown`). To test time-dependent behaviour deterministically, **patch `time.time`** at the service module (`@patch("services.lyrics.time.time", ...)`) and step it, rather than calling `time.sleep`. Reset any module-level cache/state between tests so one test's snapshot doesn't leak into the next (see `test_now_playing_cache.py`, `test_stats_cache.py`).

## Checklist for a new test

1. Name it `tests/test_<thing>.py`; copy the env-before-import header verbatim.
2. `create_app().test_client()` in `setUp`.
3. Patch the service/HTTP/DB boundary **at the module that imports it**; never reach a real Lyrion or DB.
4. Assert on the observable contract and on how the boundary was called.
5. For time-based logic, patch `time.time` and reset module state between tests.
6. Run `python -m unittest discover` and `pylint ... tests` — both gate CI.
