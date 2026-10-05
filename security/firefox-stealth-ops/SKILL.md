---
name: firefox-stealth-ops
description: >-
  Complete Firefox/Camoufox/Stealthfox undetectable automation suite with
  proxy/OPSEC and Tor Browser hardening. Integrates ultimate-firefox-mcp,
  camoufox, and tor-browser-mcp into one unified capability. Three-tier
  browser ops: Firefox (accounts), Camoufox (anti-detection), Tor (anonymity).
version: 2.0.0
author: the operator
metadata:
  hermes:
    tags: [firefox, camoufox, stealth, proxy, opsec, tor, anti-detection, browser-automation]
    triggers:
      - firefox stealth
      - undetectable browser
      - camoufox automation
      - firefox proxy
      - browser opsec
      - clean browser
      - fingerprint spoof
      - firefox ops
      - three tier browser
      - browser automation suite
    related_skills:
      - firefox-stealth-automation
      - tor-circuit-rotation
---

# Firefox Stealth OPS Suite

## Architecture

Three browser tiers, each with increasing anonymity:

| Tier | Browser | Binary | xul.dll | Port | MCP Server |
|------|---------|--------|---------|------|-----------|
| 1 | Firefox w/ accounts | `firefox-portable\\firefox.exe` | ❌ Not used — **deprecated for automation** (headless GFX crash). System FF 152+ at `C:\\Program Files\\Mozilla Firefox\\firefox.exe` used instead. | 9239 | `ultimate-firefox-mcp` |
| 2 | Camoufox | `camoufox\camoufox.exe` | ✅ Patched (0 remaining) | 9238 | `camoufox-mcp` |
| 3 | Tor Browser | `TorBrowser\Browser\firefox.exe` | ✅ Patched (0 remaining) | 9250/9251 | `tor-browser-mcp` |

## xul.dll Status (all browsers patched June 21, 2026 — 4 occurrences each)

Two patterns patched in each xul.dll:
| Pattern | Bytes | Occurrences | Replacement |
|---------|-------|-------------|-------------|
| `b"webdriver"` | 9 | 3 | `b"w3bdrv3r_"` |
| `b"WEBDRIVER_BIDI"` | 14 | 1 | `b"W3BDRVR_BIDI__"` |
| **Total** | | **4** | |

| Browser | Status | Backups | Size |
|---------|--------|---------|------|
| Tor Browser | ✅ Clean | `xul.dll.bak` + `xul.dll.bak2` | 154MB |
| Portable Firefox | ✅ Clean | `xul.dll.bak` + `xul.dll.bak2` | 164MB |
| Camoufox | ✅ Clean | `xul.dll.bak` + `xul.dll.bak2` | 145MB |
| System Firefox | ❌ Not patched (main browsing) | N/A | 166MB |

## Repos

- **ultimate-firefox-mcp**: `https://github.com/pmb2/ultimate-firefox-mcp` (branch: master, latest: `909f608`)
- **tor-browser-mcp**: `https://github.com/pmb2/tor-browser-mcp` (branch: `pmb2/hardened-tor-mcp`, latest: `a8c7eb5`)
- **Camoufox**: `https://github.com/daijro/camoufox` (pre-patched Firefox fork, binary install)

## xul.dll Patch Audit (June 21, 2026)

Across ALL three xul.dll files (Tor Browser, Portable Firefox, Camoufox):

| Pattern | Hex | Bytes | Occurrences | Replacement |
|---------|-----|-------|-------------|-------------|
| `webdriver` | `77 65 62 64 72 69 76 65 72` | 9 | 3 | `w3bdrv3r_` |
| `WEBDRIVER_BIDI` (`BLOCKING_REASON_WEBDRIVER_BIDI`) | `57 45 42 44 52 49 56 45 52 5F 42 49 44 49` | 14 | 1 | `W3BDRVR_BIDI__` |

**Total before patch:** 4 occurrences per xul.dll (3 webdriver + 1 WEBDRIVER_BIDI)
**Total after patch:** 0

**Patch method:** Python mmap (binary safe for 150MB+ files):
```python
import mmap, os
with open(path, 'r+b') as f:
    with mmap.mmap(f.fileno(), 0) as mm:
        for pattern, repl in [(b'webdriver', b'w3bdrv3r_'), (b'WEBDRIVER_BIDI', b'W3BDRVR_BIDI__')]:
            pos = 0
            while (pos := mm.find(pattern, pos)) != -1:
                mm[pos:pos+len(pattern)] = repl
                pos += len(pattern)
```

**The `WEBDRIVER_BIDI` string was discovered June 21, 2026** — it was not caught by the
original `strings | grep -i webdriver` check because the all-caps variant was missed.
The original patch only replaced lower-case `webdriver` (3 occurrences). The all-caps
`WEBDRIVER_BIDI` (a Gecko internal constant `BLOCKING_REASON_WEBDRIVER_BIDI`) required
a second pass. Always check BOTH cases with a case-insensitive binary scan after patching.

## New Code Built This Session

### `launcher.py` (in ultimate-firefox-mcp repo)
Unified Firefox launcher supporting all 4 browser variants with proxy chaining:

```python
from ultimate_firefox_mcp.launcher import launch_browser

# Launch Camoufox with SOCKS5 proxy
result = launch_browser(
    variant="camoufox",
    port=9238,
    proxy="socks5://127.0.0.1:9050",
    headless=True,
    opsec_check=True
)
```

CLI usage:
```bash
python -m ultimate_firefox_mcp.launcher --camoufox --proxy socks5://127.0.0.1:9050 --opsec-check
python -m ultimate_firefox_mcp.launcher --tor-browser --headless
python -m ultimate_firefox_mcp.launcher --portable --profile "path/to/profile"
```

### `opsec.py` (in ultimate-firefox-mcp repo)
Comprehensive OPSEC verification suite. 15-point stealth check via CDP + WebRTC leak detection + proxy routing check:

```python
from ultimate_firefox_mcp.opsec import full_opsec_report, check_via_cdp

# Full report
report = full_opsec_report(cdp_port=9239)
print(report["stealth_summary"])  # "14/15 checks passed"
print(report["overall"]["all_clear"])  # True/False

# Stealth-only check
stealth = check_via_cdp(port=9239)
# Returns per-check pass/fail + counts
```

### BiDi Protocol Support for OPSEC (`launcher.py` — commit `909f608`)
Camoufox uses WebDriver BiDi (WebSocket), not CDP (HTTP). The original
`check_fingerprint()` only tried `http://127.0.0.1:9239/json/version` which
returned 404 on a BiDi browser. **Fixed with BiDi fallback (commit `909f608`):**

```python
def check_fingerprint(port):
    # Try CDP first (standard Firefox)
    try:
        resp = urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=3)
        return {"protocol": "cdp", "info": json.loads(resp.read())}
    except Exception:
        pass
    # Try BiDi WebSocket fallback (Camoufox / Firefox 136+)
    try:
        s = socket.socket()
        s.settimeout(3)
        s.connect(("127.0.0.1", port))
        s.send(b"GET /session HTTP/1.1\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n...")
        resp = s.recv(1024)
        if b"101" in resp:
            return {"protocol": "bidi", "connected": True}
    except Exception as e2:
        return {"connected": False, "error": str(e2)}
```

**Detection logic:**
1. Try CDP HTTP endpoint (`/json/version`) — works for standard Firefox with CDP
2. If 404, try BiDi WebSocket upgrade on `/session` — works for Camoufox / Firefox 136+
3. If `101 Switching Protocols` → browser is alive and speaking BiDi
4. If neither responds → browser not running or wrong port

## MCP Server Config (in config.yaml)

```yaml
mcp:
  ultimate-firefox-mcp:
    args:
    - -m
    - ultimate_firefox_mcp.main
    - --protocol
    - auto
    - --port
    - '9239'
    command: python
    timeout: 300
    workdir: ${USER_HOME}\ultimate-firefox-mcp

  camoufox-mcp:                           # <-- ADD for Camoufox support
    args:
    - -m
    - ultimate_firefox_mcp.main
    - --protocol
    - auto
    - --port
    - '9239'
    command: python
    timeout: 300
    workdir: C:\\Users\\<you>\\ultimate-firefox-mcp

  tor-browser-mcp:
    args:
    - -m
    - torbrowser_mcp
    - --tbb-root
    - ${USER_HOME}/TorBrowser
    - --output-dir
    - ${USER_HOME}/tor-browser-outputs
    - --geckodriver-path
    - ${USER_HOME}/tor-browser-mcp/bin/geckodriver.exe
    - --max-restarts
    - '10'
    - --restart-delay
    - '5.0'
    - --headless
    command: ${USER_HOME}/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe
    timeout: 300
    workdir: ${MY_REPOS}/Documents/github/tor-browser-mcp
```

## Using Firefox for Scraping (Not Just Account Sessions)

The same `ultimate-firefox-mcp` stack used for authenticated account sessions also works for public-site scraping when HTTP clients fail.

### Direct Python Wrapper Pattern

```python
import asyncio, threading
from ultimate_firefox_mcp.browser import FirefoxBrowser

class _LoopThread:
    """Keep one asyncio loop alive for BiDi WebSocket reuse."""
    def __init__(self):
        self._loop = asyncio.new_event_loop()
        threading.Thread(target=self._run, daemon=True).start()
    def _run(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()
    def run(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self._loop).result()

_loop = _LoopThread()

class FirefoxScraperClient:
    def fetch_html(self, url: str, port: int = 9239, wait: float = 3.0) -> str:
        browser = FirefoxBrowser(host="127.0.0.1", port=port)
        _loop.run(browser.connect())
        async def _fetch():
            ctx = (await browser.list_contexts())[0]["context"]
            await browser.navigate(ctx, url)
            await asyncio.sleep(wait)
            return (await browser.evaluate_script(ctx, "document.documentElement.outerHTML"))["result"]["value"]
        return _loop.run(_fetch())
```

### Why Not asyncio.run() Per Request?

`FirefoxBrowser` creates internal tasks bound to the loop that opened the WebSocket. Calling `asyncio.run()` for each request creates and destroys a new loop, killing those tasks and raising `RuntimeError: Event loop is closed`. Use a persistent background loop instead.

### When to Switch from HTTP to Firefox

- Site returns SSR shell but target data is in `__NEXT_DATA__` that only populates after JS runs
- Bookmaker odds tables come back `null` via curl_cffi but render in browser
- Anti-bot returns 403 / CAPTCHA / challenge to HTTP clients
- User explicitly says "use ultimate firefox"

### Cleanup

Firefox processes launched for scraping must be killed explicitly:

```bash
taskkill /f /im firefox.exe
```

Or call `browser.disconnect()` then kill. Do not rely on disconnect alone — it closes the WebSocket but leaves `firefox.exe` running.

## Launching Each Tier

### Tier 1 — Firefox with Accounts
```bash
# Launched automatically by ultimate-firefox-mcp MCP server
# Uses automation profile for saved logins
# StealthEngine (22 measures) auto-applies
```

### Tier 2 — Camoufox
```bash
# Terminal 1: Launch Camoufox with remote debugging
"${USER_HOME}/camoufox/camoufox.exe" --remote-debugging-port 9238 --no-remote

# Terminal 2: MCP server connects to port 9238 (via camoufox-mcp config)
# Or use the unified launcher:
python -m ultimate_firefox_mcp.launcher --camoufox
```

### Tier 3 — Tor Browser
```bash
# Handled by tor-browser-mcp MCP server (auto-launches tor + browser)
# Tools available via mcp_tor_browser_mcp_* prefix
```

## When to Switch from Playwright/Chromium to Firefox Tiers

Hermes native `browser_*` tools and the `playwright-mcp` server both drive Chromium. If they fail (CDP connection refused, Playwright MCP unreachable, or the site behaves differently under Chromium), pivot to the Firefox tiers — especially when the operator explicitly says "use ultimate firefox" or when the task involves personal accounts/logins stored in his Firefox profile.

### Preferred fallback order
1. `ultimate-firefox-mcp` (Tier 1) — use for authenticated sites, saved logins, or when the operator says "use ultimate firefox."
2. `camoufox-mcp` (Tier 2) — use when anti-bot protection blocks Tier 1.
3. `tor-browser-mcp` (Tier 3) — use when anonymity or Tor exit rotation is required.

### Discovering MCP browser tools at runtime
If a browser tool fails, use `tool_search` to list MCP alternatives, then `tool_describe` + `tool_call` to invoke them. Common qualified names:
- `mcp__playwright_mcp__browser_navigate`
- `mcp__playwright_mcp__browser_click`
- `mcp__playwright_mcp__browser_fill_form`
- `mcp__tor_camoufox_bridge__browser_navigate`
- `mcp__tor_camoufox_bridge__camoufox_navigate`

Note: `ultimate-firefox-mcp` tools may not appear in `tool_search` if the server is not loaded in the active session's tool registry. Verify with `hermes mcp list` and use the `mcp__ultimate_firefox_mcp__*` naming if available.

## Tor MCP Tools

| Tool | Purpose |
|------|---------|
| `tor_status` | Tor health, bootstrap, version |
| `tor_rotate_identity(post_signal_sleep=15)` | Full circuit rotation (NEWNYM + before/after verify) |
| `tor_apply_stealth(xul_patch, inject_js)` | Apply all anti-detection measures |
| `tor_verify_stealth()` | Check 8+ detection vectors pass |
| `tor_recover_browser()` | Restart browser only when it crashes (tor/circuits stay up) |
| `tor_browser_health()` | Check browser + tor + current URL responsiveness |
| `tor_circuit_health()` | Comprehensive circuit diagnostics |
| `tor_dns_leak_test()` | DNS leak verification |
| `tor_exit_node_info()` | Current exit node details |

## Cron Job

**Job ID:** `7e8baae3c06d` (in skill: tor-circuit-rotation)
**Schedule:** Every 6 hours
**Workflow:** health check → recover if crashed → rotate circuit → verify stealth
**Reports to:** Origin conversation

## QA Verification (June 21, 2026)

| Check | Result |
|-------|--------|
| xul.dll Tor Browser | ✅ 0 remaining (4 patched: 3 webdriver + 1 WEBDRIVER_BIDI) |
| xul.dll Portable Firefox | ✅ 0 remaining |
| xul.dll Camoufox | ✅ 0 remaining |
| Launcher module imports | ✅ 4 browser paths |
| OPSEC module (check JS) | ✅ 3,524 chars |
| OPSEC `check_fingerprint` BiDi fallback | ✅ Added (commit `909f608`) |
| Crash recovery loop (tor-browser-mcp) | ✅ Confirmed working (commit `a8c7eb5`) |
| New tor MCP tools registered | ✅ 5 tools (stealth, rotation, health, recover, verify) |
| Stealth JS syntax | ✅ Parses clean |
| All binaries exist | ✅ 4/4 |

## Pitfall: Headless Firefox needs `--disable-gpu` on this machine

System Firefox 152.0.5 (and all versions on this Windows machine) crashes in headless mode without `--disable-gpu`. The D3D11 compositor fails to initialize when there's no physical display adapter.

**Symptom:** Firefox starts, briefly binds the port, then exits within 1-15 seconds with GFX errors:
```
[GFX1-]: Failed to launch GPU process after 3 attempts
[GFX1-]: [D3D11] failed to get compositor device.
[GFX1-]: RenderCompositorSWGL failed mapping default framebuffer, no dt
```

**Fix:** Always include `--disable-gpu` in Firefox launch commands for headless automation on this machine. This applies to all three browser tiers when running headless.

**Verification:**
```bash
"/c/Program Files/Mozilla Firefox/firefox.exe" --headless --disable-gpu --remote-debugging-port 9239 -no-remote --profile "${USER_HOME}\AppData\Local\hermes\firefox-profile-temp" &
sleep 12
python -c "import socket; s=socket.socket(); s.settimeout(3); s.connect(('127.0.0.1',9239)); print('OK'); s.close()"
```

## Pitfall: Zombie Firefox accumulation from BiDi session exhaustion

Every Firefox headless instance used for BiDi automation spawns a `firefox.exe` process bound to the debugging port. When the connection lifecycle is not properly managed, **unlimited zombie Firefox processes accumulate**, exhausting system resources.

**Symptom:** `tasklist //FI "IMAGENAME eq firefox.exe" //NH` returns 10+ Firefox processes. The machine may run out of memory or port availability. New Firefox instances fail to bind the debugging port because old instances still hold it.

**Common causes:**
1. **Connector `close()` doesn't kill Firefox** — The `close()` method only closes the WebSocket. The Firefox process stays running, still bound to the port, accumulating indefinitely.
2. **`reconnect()` doesn't kill Firefox before relaunch** — When BiDi sessions exhaust (Firefox has a ~5 session hard limit), `reconnect()` tries to start a new Firefox but the old one still holds the port. Result: zombie process + port contention.
3. **Pipeline orphan cleanup only kills by port** — Killing only the process on port 9239 misses Firefox processes on other ports or child processes.

**Fix (apply in order of impact):**
1. **`close()` must kill Firefox** — Always call `self._kill_firefox()` in `close()` to ensure cleanup when a connector finishes.
2. **`reconnect()` must kill before relaunch** — In `reconnect()`, call `self._kill_firefox()` + `await asyncio.sleep(2)` BEFORE `ensure_firefox()`. This releases the port and allows a clean launch.
3. **Pipeline cleanup should kill ALL Firefox** — Use `taskkill -f -im firefox.exe` in the pipeline's cleanup phase, not just port-specific killing.

**Detection:**
```bash
tasklist //FI "IMAGENAME eq firefox.exe" //NH //FO CSV
# If more than 1-2 entries, zombie accumulation is active.
```
**Remediation:** `taskkill -f -im firefox.exe` (kills all Firefox instances immediately).

**Prevention audit:** For any Firefox-based connector or automation script, verify:
- [ ] `close()` kills the Firefox process (not just closes WebSocket)
- [ ] `reconnect()` kills before relaunching
- [ ] Pipeline/automation cleanup uses `taskkill -f -im firefox.exe` (not just port-based kill)
