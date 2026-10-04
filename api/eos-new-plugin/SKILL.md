---
name: eos-new-plugin
description: Scaffold a new EmptyOS plugin end-to-end in the right shape — service (exposes a named service via self.require), enhancer (injects a capability provider at boot), or both — optionally wiring the external-service launch pattern (auto_start + CREATE_NO_WINDOW) for a local binary like ComfyUI / voice-api / Blender. Use when the user says "new plugin", "create plugin", "scaffold plugin <id>", or "wrap <service> as a plugin". NOT for anything with a UI/page — that is an app (use eos-new-app).
---

# EmptyOS New Plugin

Scaffold a new plugin end-to-end with the right shape for its role — **service** (exposes a named service other apps consume), **enhancer** (injects a capability provider at boot), or **both**. Optionally wires the external-service launch pattern (`auto_start` + `CREATE_NO_WINDOW`) when the plugin wraps a local binary like ComfyUI / voice-api / Blender.

Plugins load **before** apps, have no UI of their own, and expose functionality to apps via either `self.require("<name>")` (service plugins) or transparent capability-provider injection (enhancer plugins).

## When to Use

- User says "new plugin", "create plugin", "scaffold plugin `<id>`", "wrap `<service>` as a plugin"
- Before integrating a new external service (local LLM, GPU workload, TTS/STT, bot, headless app)
- **Not** for functionality that belongs in an app (apps have UI, manifest `[provides.web]`, user-facing surface). If it has a page, it's an app.

## Process

Run in order. Confirm the spec at Step 1 before generating anything.

---

### Step 1: Gather the Spec

Ask once (single message):

```
Id             : kebab-case, matches directory name (e.g. "whisper-local")
Display name   : e.g. "Whisper Local"
Description    : 1 line
Role           : service | enhancer | both
  - service  = exposes named service via self.require("<id>") — health, notifications, telegram
  - enhancer = injects a provider into a capability at boot — ollama→think, comfyui→draw
  - both     = service + enhancer in one plugin (named service methods + capability provider injection)

If enhancer or both:
  Capability enhanced : think | read | write | search | speak | listen | draw
  Provider priority   : 0 (default; 0 = highest, falls back to next on failure)

External binary?     : yes/no — needs auto_start + launcher config?
  If yes:
    Launcher path    : e.g. "D:/ComfyUI_windows_portable/run_nvidia_gpu.bat"
    Health endpoint  : e.g. "http://localhost:8188/system_stats"
    Startup timeout  : seconds (default 60)

Config keys   : list of (key, default) for emptyos.toml [plugins.<id>]
Default-on?   : true|false — default=true in manifest means it loads unless disabled
```

---

### Step 2: Pre-flight

```bash
ls plugins/<id> 2>/dev/null && echo "CLASH" || echo "OK"
# Plugin id must not shadow an app either:
ls apps/<id> apps/personal/<id> 2>/dev/null && echo "SHADOWS APP" || echo "OK"
```

Abort and ask for a new id if either clashes.

---

### Step 3: Create `plugins/<id>/manifest.toml`

```toml
[plugin]
id = "<id>"
name = "<Display Name>"
version = "1.0.0"
description = "<1-line description>"
default = <true|false>

[plugin.entry]
module = "plugin"
class = "<PascalCase>Plugin"

[provides]
services = ["<id>"]            # omit if pure enhancer with no named service
tags = ["<tag1>", "<tag2>"]    # e.g. ["llm", "local"], ["gpu", "image"], ["voice"]
```

Do **not** add `[requires]`, `[provides.web]`, or `[provides.settings]` — plugins don't use those. Per-plugin config goes in `emptyos.toml` under `[plugins.<id>]` and is read via `self.config("key", default)`.

---

### Step 4: Create `plugins/<id>/plugin.py`

Pick the template that matches the role. Rules shared across all three:

- Extend `BasePlugin` from `emptyos.sdk`
- Read config with `self.config("key", default)` — never hardcode
- `async def connect()` is the lifecycle hook called after kernel boot — use for reachability probe + provider registration
- `async def disconnect()` — close sessions, cancel tasks
- `async def available() -> bool` — cheap probe with short timeout (2s); capability fallback relies on this

#### 4a. Service plugin template

```python
"""<Display Name> plugin — <what the service does>."""

from __future__ import annotations

import aiohttp
from emptyos.sdk import BasePlugin


class <Pascal>Plugin(BasePlugin):
    name = "<id>"

    def _host(self) -> str:
        return self.config("host", "http://localhost:<port>")

    async def connect(self):
        if await self.available():
            print(f"[<Display>] Connected to {self._host()}")
        else:
            print(f"[<Display>] Warning: not reachable at {self._host()}")

    async def available(self) -> bool:
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(
                    f"{self._host()}/<health-path>",
                    timeout=aiohttp.ClientTimeout(total=2),
                ) as r:
                    return r.status == 200
        except Exception:
            return False

    # ── Service API — apps call these via self.require("<id>") ──
    async def do_thing(self, arg: str) -> dict:
        ...
```

#### 4b. Enhancer plugin template

```python
"""<Display Name> plugin — <capability> provider via <backend>."""

from __future__ import annotations

import aiohttp
from emptyos.sdk import BasePlugin


class <Pascal>Plugin(BasePlugin):
    name = "<id>"

    def __init__(self, kernel, manifest):
        super().__init__(kernel, manifest)
        self._registered = False

    async def connect(self):
        if await self.available():
            self._register_provider()
            print(f"[<Display>] Registered <capability> provider")

    async def available(self) -> bool:
        # short-timeout probe
        ...

    def _register_provider(self):
        if self._registered:
            return
        from emptyos.capabilities import Provider
        plugin = self

        class <Pascal>Provider(Provider):
            name = "<id>"
            async def available(self) -> bool:
                return await plugin.available()
            async def execute(self, *, prompt: str, **kwargs) -> str:
                return await plugin.generate(prompt, **kwargs)

        cap = self.kernel.capabilities.get("<capability>")
        cap.add_provider(<Pascal>Provider(), priority=<N>)
        self._registered = True

    async def generate(self, prompt: str, **kwargs) -> str:
        ...  # call the backend
```

Follow the "Graceful Enhancement" pattern: if the backend is unreachable, `connect()` logs a warning and skips registration — the capability falls back to the next provider (typically `human`). No app code changes.

#### 4c. Both (service + enhancer)

Combine 4a and 4b — named service for apps that want direct access, plus provider injection for transparent capability use. Use this when a backend is worth *both* a capability enhancer (so callers of `self.search()` get the upgrade for free) *and* exposed service methods (for apps that want vendor-specific features). See `plugins/voice-api/` for a current implementation.

#### 4d. External-binary add-on (if the spec said yes)

Add an `auto_start` method following the pattern in `plugins/comfyui/plugin.py` (CLAUDE.md §External Service Launch Pattern):

```python
async def auto_start(self) -> bool:
    if await self.available():
        return True
    import asyncio, subprocess
    from pathlib import Path

    launcher = self.config("launcher", "")
    if not launcher:
        print(f"[<Display>] No launcher configured (set <id>.launcher in emptyos.toml)")
        return False

    launcher_path = Path(launcher)
    launcher_dir = str(launcher_path.parent)
    python_exe = str(launcher_path.parent / "<embedded-python-rel-path>")
    main_py    = str(launcher_path.parent / "<main-script-rel-path>")

    try:
        subprocess.Popen(
            [python_exe, "-s", main_py, "<flags>"],
            cwd=launcher_dir,
            creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        print(f"[<Display>] Starting…")
        timeout = self.config("startup_timeout", 60)
        for _ in range(timeout // 2):
            await asyncio.sleep(2)
            if await self.available():
                self._register_provider()  # if enhancer
                print(f"[<Display>] Ready")
                return True
        print(f"[<Display>] Timed out after {timeout}s")
    except Exception as e:
        print(f"[<Display>] Failed to start: {e}")
    return False

async def ensure_available(self) -> bool:
    if await self.available():
        return True
    return await self.auto_start()
```

Rules (CLAUDE.md §External Service Launch Pattern):
- **Never** `start /min` or `cmd /c start` — both pop windows
- **Always** set `cwd` to the service directory (launchers use relative paths)
- Use embedded python directly, not the `.bat` wrapper (the `.bat` spawns windows)
- Poll the health endpoint; don't assume process-start == ready

---

### Step 5: Register Config in `emptyos.toml`

Add (or show the user to add) a section under the gitignored `emptyos.toml`:

```toml
[plugins.<id>]
# host = "http://localhost:<port>"
# launcher = "D:/Path/To/run.bat"      # only if external binary
# startup_timeout = 60
# <other config keys from Step 1 spec>
```

Do **not** commit this — `emptyos.toml` is gitignored. If personal paths or keys sneak into `plugin.py` defaults, Step 8's `check-personal.py` will catch them.

---

### Step 6: Register in `release.toml` (if shipping to community)

Plugins ship per-tier just like apps:

```toml
[tiers.<tier>]
plugins = [..., "<id>"]
```

- `core`: health, notifications only (minimum OS)
- `standard`: community plugins — ollama, comfyui, voice-api, etc.
- Skip this step for personal/machine-local plugins

```bash
python scripts/package-release.py --check
```

---

### Step 7: Update `restart.bat` (if external binary)

If the plugin wraps a local service, restart.bat should launch it headless alongside EmptyOS so everything boots together. Follow the `pushd` + `start /b` pattern (CLAUDE.md §External Service Launch Pattern):

```batch
if not exist "D:/Path/To/marker" goto skip_<id>
pushd D:/Path/To
start /b "" .\python_embeded\python.exe -s <main.py> <flags> >nul 2>nul
popd
:skip_<id>
```

Never `start /min` or `cmd /c start` — both open visible windows. Test the change by running `restart.bat` and confirming no new window appears.

---

### Step 8: Verify

```bash
# Restart daemon so the plugin loads
# (ask user to run restart.bat)

# Confirm plugin loaded
curl -s http://localhost:9000/api/plugins | python -c "import sys,json; ids=[p['id'] for p in json.load(sys.stdin)]; print('<id>' in ids)"

# If enhancer, confirm provider is on the capability
curl -s http://localhost:9000/api/capabilities | python -c "import sys,json; d=json.load(sys.stdin); print([p['name'] for p in d.get('<capability>', {}).get('providers', [])])"

# System self-audit — plugin row must be present
curl -s http://localhost:9000/integrity/api/audit

# Safety (same scripts as apps)
python scripts/check-personal.py
python scripts/check-branding.py
```

All four must pass. Branding check is especially important — plugin code may reference the external service internally (that's allowed), but error messages and any surfaced strings must stay generic.

---

### Step 9: Report

```
New Plugin Scaffolded: <id> (<role>)

Files created:
  plugins/<id>/manifest.toml
  plugins/<id>/plugin.py

Wired:
  emptyos.toml        → [plugins.<id>] template added (user edits locally)
  release.toml        → <tier> tier (or "N/A — personal plugin")
  restart.bat         → headless launch block (or "N/A — no external binary")

Capabilities:
  <capability> ← <id> provider at priority <N>   (enhancer only)
  services: <id>                                   (service only)

Verified:
  /api/plugins shows <id>             OK
  /api/capabilities shows provider     OK
  integrity audit plugins row          OK
  check-personal / check-branding      CLEAN

Next:
  1. Fill in the TODO methods in plugins/<id>/plugin.py
  2. If enhancer: an app using the capability should now transparently use it
  3. Before commit: run /eos-simplify
  4. End of session: run /eos-session-wrapup
```

## Safety

- **Never** commit `emptyos.toml` — personal paths and API keys live there, it's gitignored.
- **Never** hardcode a launcher path, API key, or local port in `plugin.py` — always `self.config(...)`.
- **Never** use `start /min`, `cmd /c start`, or the `.bat` wrapper directly in `auto_start` — all of them pop windows.
- **Never** let the plugin fail hard on missing backend — probe with short timeout, log a warning, let the capability fall back gracefully.
- **Never** reference the external service brand in user-facing strings (prompts, error messages surfaced to apps) — internal plugin code may reference it (that's the branding-check exception), but the outward interface stays generic.
- **Don't** add a `[provides.web]` or `pages/` to a plugin — if it needs a UI, it's an app.

## Relationship

- App that wants to *consume* the plugin → `/eos-new-app` (declare `services = ["<id>"]` in `[requires]`, call via `self.require("<id>")`)
- Pre-commit → `/eos-simplify`
- End of session → `/eos-session-wrapup`
- Health of the plugin layer → `/eos-architecture-review` (check mode surfaces dormant / failing plugins)
