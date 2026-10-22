---
name: cdp
type: reference
description: Reference for attaching to a running Chromium browser over the Chrome DevTools Protocol (CDP). Covers the chrome://inspect remote-debugging toggle, DevToolsActivePort discovery, browser socket URLs, browser paths, and client commands. Read before connecting to a live browser or writing CDP tooling.
---

## Chrome DevTools Protocol (CDP) Reference

CDP is the protocol behind browser automation and the Chrome DevTools frontend. Chromium-based browsers speak it directly over HTTP and WebSocket. No MCP server, Puppeteer, or Playwright is required to attach.

### Server Modes

Two server modes exist. They are not interchangeable.

| Mode | Enabled by | `/json/version`, `/json/list` | Page socket (`/devtools/page/<id>`) | Browser socket (`/devtools/browser/<id>`) |
| --- | --- | --- | --- | --- |
| Debug port | `--remote-debugging-port=<port>` at launch | 200 OK | 200 OK | 200 OK |
| Remote debugging toggle | `chrome://inspect/#remote-debugging` | 404 Not Found | 403 Forbidden | 101 Switching Protocols (after user clicks Allow) |

#### Debug Port Restrictions (Chrome 136+)

Since Chrome 136, `--remote-debugging-port` and `--remote-debugging-pipe` are ignored when Chrome runs on its default user data directory. The flags work only when paired with a non-default `--user-data-dir=<path>`. When ignored, the flag fails silently with no warning to block infostealers from reading the primary cookie jar.

```bash
# Works: explicit non-default data directory
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug

# Ignored silently on Chrome 136+: uses default profile
google-chrome --remote-debugging-port=9222
```

To debug your primary profile with existing cookies and extensions, use the remote debugging toggle instead.

#### Remote Debugging Toggle (Chrome 144+)

Open `chrome://inspect/#remote-debugging` and check "Allow remote debugging for this browser instance". Chrome starts a debugging server inside the running browser on the active profile without a restart.

- **Random port**: The listening port is assigned dynamically each time the toggle is enabled.
- **No HTTP discovery**: `/json/version`, `/json/list`, and `/json/new` all return `404`.
- **No direct page sockets**: Connecting directly to `/devtools/page/<id>` returns `403`.
- **Browser socket only**: Only the browser-level WebSocket `/devtools/browser/<id>` accepts connections.
- **Per-connection approval**: Every WebSocket handshake triggers an "Allow remote debugging?" dialog in the browser. Permission belongs to that single WebSocket connection, not to the client tool or session.
- **Handshake blocking**: Chromium completes the `101 Switching Protocols` upgrade only after the user clicks **Allow**. If the user declines, it returns `403 Connection rejected`. While the dialog is open, the handshake hangs with no response—set a client timeout (e.g., 20s) and **never auto-retry** on timeout, as each retry spawns another confirmation dialog.

---

### Endpoint Discovery

When either debugging server starts, Chromium writes two lines to `DevToolsActivePort` inside the user data directory:

1. Line 1: The listening TCP port (e.g., `41823`).
2. Line 2: The browser WebSocket path (e.g., `/devtools/browser/a1b2c3d4-...`).

```bash
profile="$HOME/.config/google-chrome" # or your browser's profile path
port=$(head -n 1 "$profile/DevToolsActivePort")
path=$(sed -n '2p' "$profile/DevToolsActivePort")
ws="ws://127.0.0.1:${port}${path}"
```

#### Stale `DevToolsActivePort` Files

`DevToolsActivePort` can outlive the server if the toggle is turned off or the browser crashes. Treat the file as a hint and verify that the port is listening before connecting:

```bash
# Verify TCP port is open without triggering an approval dialog
nc -z 127.0.0.1 "$port"
```

Do not probe the port with a WebSocket upgrade or HTTP request to `/devtools/browser/<id>` unless you are ready for the user to click **Allow**.

---

### Browser Paths

Chromium-family browsers share the same CDP implementation and `DevToolsActivePort` format.

| Browser | Binary | Linux User Data Dir | macOS User Data Dir | Windows User Data Dir |
| --- | --- | --- | --- | --- |
| Chrome | `google-chrome`, `google-chrome-stable` | `~/.config/google-chrome` | `~/Library/Application Support/Google/Chrome` | `%LOCALAPPDATA%\Google\Chrome\User Data` |
| Chromium | `chromium`, `chromium-browser` | `~/.config/chromium` | `~/Library/Application Support/Chromium` | `%LOCALAPPDATA%\Chromium\User Data` |
| Helium | `helium` | `~/.config/net.imput.helium` | `~/Library/Application Support/net.imput.helium` | `%LOCALAPPDATA%\net.imput.helium\User Data` |
| Edge | `microsoft-edge`, `msedge` | `~/.config/microsoft-edge` | `~/Library/Application Support/Microsoft Edge` | `%LOCALAPPDATA%\Microsoft\Edge\User Data` |
| Brave | `brave-browser`, `brave` | `~/.config/BraveSoftware/Brave-Browser` | `~/Library/Application Support/BraveSoftware/Brave-Browser` | `%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data` |
| Vivaldi | `vivaldi` | `~/.config/vivaldi` | `~/Library/Application Support/Vivaldi` | `%LOCALAPPDATA%\Vivaldi\User Data` |

- On macOS, binaries inside app bundles live at `/Applications/<App>.app/Contents/MacOS/<Binary>`.
- `DevToolsActivePort` is always written to the root **User Data Dir** (not inside profile subdirectories such as `Default/` or `Profile 1/`).

---

### Attaching with `agent-browser`

`agent-browser` maintains a background daemon per session, keeping a single persistent WebSocket open across CLI invocations so the user only clicks **Allow** once. **User-attached browsers are exempt from the 1-hour daemon idle timeout**, so an attached daemon stays alive indefinitely until `agent-browser close` is run or the browser quits.

#### 1. Check and Reuse an Existing Session First

Before connecting, check whether a daemon is already running and attached. Reusing an active daemon avoids opening a new WebSocket and prevents another "Allow remote debugging?" popup:

```bash
agent-browser session list
agent-browser session info --json
```

If an active session is already connected to the browser, reuse that `--session <name>` (along with the same `AGENT_BROWSER_CDP` or `--auto-connect` flag).

#### 2. Keep `AGENT_BROWSER_CDP` Consistent Across Every Command

**Critical pitfall**: If a daemon is attached via `--cdp "$ws"` and you run a subsequent command on that same session _without_ `AGENT_BROWSER_CDP` or `--cdp`, `agent-browser` sees a launch-config mismatch, tears down the attached CDP connection, and launches a separate headless browser—forcing a new approval popup the next time you pass `--cdp`.

Always export `AGENT_BROWSER_CDP` in every shell invocation (or use a persistent shell environment):

```bash
export AGENT_BROWSER_CDP="$ws"

# First attach (triggers Allow prompt only if no daemon is connected yet)
agent-browser --pin-tab open https://example.com

# Subsequent commands reuse the same daemon and WebSocket without prompting
agent-browser tab list
agent-browser snapshot -i
```

#### 3. Auto-Connect (Default Chrome Profile Only)

`--auto-connect` (or `AGENT_BROWSER_AUTO_CONNECT=1`) reads `DevToolsActivePort` from the default Chrome data directory, connects to the browser WebSocket, and waits up to 20 seconds for user approval. If `DevToolsActivePort` is absent, it falls back to probing ports `9222` and `9229`.

```bash
export AGENT_BROWSER_AUTO_CONNECT=1
agent-browser --pin-tab tab list
agent-browser snapshot -i
```

#### 4. Do NOT Run `agent-browser close` After Tasks

**Do not run `agent-browser close` (or `close --all`) when attached to the user's browser.** Closing the session kills the `agent-browser` daemon and drops the approved WebSocket, which forces the user to click **Allow** again on the next task.

Instead, close only the tab you opened and leave the daemon running for reuse:

```bash
# Close only the tab you created, keeping the daemon and WebSocket alive
agent-browser tab close
```

#### 5. Tab Pinning in a Shared Browser

When multiple sessions or tasks share the user's browser over CDP, pass `--pin-tab` (or `AGENT_BROWSER_PIN_TAB=1`) on the first command so the session binds strictly to its own tab by CDP `targetId`:

```bash
export AGENT_BROWSER_CDP="$ws"
export AGENT_BROWSER_PIN_TAB=1
agent-browser open https://site-a.com
```

- Attaching with no existing binding opens a fresh tab instead of navigating the user's active tab.
- Tabs opened by the user or other sessions never steal focus from the pinned session.
- If the bound tab is closed, commands fail with `"code": "tab_gone"` instead of silently acting on another tab. Recover with `agent-browser tab new <url>` or `agent-browser tab <targetId>`.
- `--pin-tab` is sticky per session; pass `--no-pin-tab` to disable it.

---

### Attaching with Raw CDP (Flattened Sessions)

Because `/devtools/page/<id>` returns `403` in remote-debugging toggle mode, all page commands must be multiplexed over the single browser WebSocket using flattened target sessions (`flatten: true`):

1. **Discover targets** — send `Target.getTargets` on the browser socket (no `sessionId`):

   ```json
   { "id": 1, "method": "Target.getTargets" }
   ```

2. **Attach to a page target** — pass the page's `targetId` with `flatten: true`:

   ```json
   {
     "id": 2,
     "method": "Target.attachToTarget",
     "params": { "targetId": "<targetId>", "flatten": true }
   }
   ```

   The response returns `{"id": 2, "result": {"sessionId": "<sessionId>"}}` (and a `Target.attachedToTarget` event).

3. **Send page-scoped commands** — include `sessionId` at the top level of every message directed at that tab:

   ```json
   {"id": 3, "sessionId": "<sessionId>", "method": "Runtime.enable"}
   {"id": 4, "sessionId": "<sessionId>", "method": "Page.navigate", "params": {"url": "https://example.com"}}
   ```

   Events emitted by that tab also carry `"sessionId": "<sessionId>"` at the top level.

4. **Detach from the target when done** — leave the browser WebSocket open if a daemon owns it, or detach from the page target without closing the user's tab:

   ```json
   {
     "id": 5,
     "method": "Target.detachFromTarget",
     "params": { "sessionId": "<sessionId>" }
   }
   ```

---

### Other Clients

- **Playwright**:
  ```ts
  const browser = await chromium.connectOverCDP(wsUrl);
  const context = browser.contexts()[0];
  const page = context.pages()[0];
  ```
- **Puppeteer**:
  ```ts
  const browser = await puppeteer.connect({
    browserWSEndpoint: wsUrl,
    defaultViewport: null,
  });
  const pages = await browser.pages();
  ```
  Always call `browser.disconnect()` instead of `browser.close()` so the user's browser stays running.
- **`bdg`**: CLI for raw CDP inspection and session management (`bdg cdp --list`, `bdg cdp --describe Page`).

---

### Operational Rules

1. **Reuse the daemon and WebSocket**: Chrome does not remember the **Allow** decision across WebSocket connections. Never run `agent-browser close` on an attached session, and never omit `AGENT_BROWSER_CDP` / `--cdp` on a follow-up command (which reconfigures the daemon and drops the socket).
2. **Clean up tabs, not the browser**: Close only the tab you opened (`agent-browser tab close`), or detach (`Target.detachFromTarget`). Never send `Browser.close` or close tabs the user opened unless explicitly requested.
3. **Background tabs do not render**: `Page.captureScreenshot` and layout-dependent checks can hang on occluded or backgrounded tabs. Call `Page.bringToFront` first (or use a separate window).
4. **Late attach replays logs, not network bodies**: Enabling domains on an already-loaded page replays buffered history:
   - `Runtime.enable` replays console messages and uncaught exceptions.
   - `Log.enable` replays browser/network log entries.
   - `Audits.enable` replays DevTools Issues panel findings.
   - `Network.enable` does **not** replay prior request headers, response bodies, or timings—reload the page or attach before navigation to capture network payloads.
5. **Scope `Target.setAutoAttach`**: Calling `Target.setAutoAttach({ autoAttach: true, waitForDebuggerOnStart: false, flatten: true })` on the **browser** session attaches to every open tab in the browser. Send it with a page's `sessionId` to limit auto-attach to that tab's child iframes and workers.

### Security

The debugging server grants full control over the active browser profile on `127.0.0.1`. Any local process that obtains an approved socket can read cookies, inspect storage, and execute arbitrary JavaScript in any origin. Enable the toggle only on a trusted machine, approve only prompts you initiated, and turn the toggle off when finished.
