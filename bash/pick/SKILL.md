---
name: pick
description: Pick an element from the browser by clicking it (starts the dev server if needed) and get back its CSS selector, tag, classes, and text. Manual only.
argument-hint: [prompt]
disable-model-invocation: true
allowed-tools: Bash(playwright-cli:*), Bash(google-chrome:*), Bash(open:*), Bash(curl:*), Bash(ss:*), Bash(lsof:*), Bash(seq:*), Bash(sleep:*), Bash(cat:*), Bash(npm:*), Bash(grep:*), Read, Glob
---

# pick

## Context

- Current working directory: !`pwd`
- Package.json dev script (if exists): !`cat package.json 2>/dev/null | grep -E '"dev":|"start":' | head -2 || echo "No dev/start script"`
- Dev host/port hint (from CLAUDE.md, if any): !`grep -rhoE 'https?://[a-zA-Z0-9.-]+:[0-9]+' CLAUDE.md .claude/CLAUDE.md 2>/dev/null | sort -u | head -3 || echo "No CLAUDE.md dev URL hint"`
- LISTEN ports (candidate dev servers): !`{ ss -tlnH 2>/dev/null | awk '{print $4}' || lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null | awk 'NR>1{print $9}'; } | grep -oE ':[0-9]+$' | tr -d ':' | sort -un | grep -vE '^(22|53|631)$' | head -10 || echo "none"`
- Debuggable browser on :9222 (Chrome OR Edge — both CDP): !`curl -s --max-time 1 http://localhost:9222/json/version 2>/dev/null | grep -oE '"Browser": *"[^"]*"' || echo "nothing on :9222"`

## Your task

Help the user pick an element from the browser. `playwright-cli` attaches to
any Chromium browser over CDP (Chrome, Edge, Electron) — there is **no native
picker**, so we inject a JS overlay and poll for the result.

Every command below runs in the named session `-s=pick` (the flag goes before
the command), so it never touches the user's other playwright-cli sessions.

**Step 0: Preflight**

```bash
${CLAUDE_PLUGIN_ROOT}/skills/playwright-cli/check.sh
```

If it fails, stop and relay its message to the user — it says what to install.

**Step 1: Get a debuggable browser**

- **Reuse what's already on :9222** if the context shows one (the user's normal
  Chrome/Edge — best, keeps logged-in sessions). Skip to Step 1b.
- **Else launch a fresh Chrome.** Must be _detached_ (`nohup … &`) or it dies
  when the command returns. `--ignore-certificate-errors --test-type` handles
  flaky dev TLS (e.g. self-signed `*.local` hosts). 9222 is often taken by
  Edge/Teams, so use a free port. The binary name differs per OS: `google-chrome`
  (Linux), `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"`
  (macOS), `chrome.exe` or `msedge.exe` (Windows) — Edge takes the same flags.
  ```bash
  nohup google-chrome --remote-debugging-port=9223 \
    --user-data-dir="$HOME/.chrome-debug-profile" \
    --ignore-certificate-errors --test-type "<start-url>" \
    </dev/null >/dev/null 2>&1 &
  until curl -s http://localhost:9223/json/version >/dev/null 2>&1; do sleep 0.3; done
  ```

**Step 1b: Attach + select the tab**

Attach to the browser, list its tabs, and select the one showing the app. Tab
selection is explicit and sticky: every later `eval` hits that tab.

```bash
PORT=9222   # or 9223 if you launched fresh
playwright-cli -s=pick close 2>/dev/null   # drop a stale pick session, if any
playwright-cli -s=pick attach --cdp=http://localhost:$PORT
playwright-cli -s=pick tab-list                 # "- 1: (current) [Title](url)"
playwright-cli -s=pick tab-select <n>
playwright-cli -s=pick --raw eval 'location.href + " | " + document.title'   # confirm right tab
```

**Step 2: Find the page to pick from**

- Prefer the dev URL hint from CLAUDE.md (context above) — it carries the right
  host (some apps key locale/routing off the Host header, so `localhost` ≠ the
  project hostname).
- Else pick the dev server from the LISTEN ports above (ignore system ports).
- If nothing is listening, start the app the way this project starts it: a
  `run` skill for the project if one is available, else whatever CLAUDE.md or
  the README prescribes, else the repo's own package manager and dev script.
  Background it and wait until its port is LISTEN.

**Step 3: Navigate**

```bash
playwright-cli -s=pick goto "<dev-url>"
playwright-cli -s=pick --raw eval 'location.href + " | " + document.title'   # confirm
```

**Step 4: Arm the picker overlay, then poll**

Inject the overlay (multi-select via Ctrl/Cmd+click, Enter finishes, single
click resolves one, ESC cancels):

```bash
playwright-cli -s=pick --raw eval "$(cat "${CLAUDE_SKILL_DIR}/picker.js")"
```

The overlay lives in [`picker.js`](picker.js) next to this file: it highlights
whatever the cursor is over, and on click leaves the pick (selector, text,
truncated HTML, attributes) on `window.__picked` with `window.__pickerDone` set.
Returns `"armed"`, or `"already-armed"` if it is on the page already.

Then poll (eval is one-shot, so loop). `--raw eval` prints the value as JSON,
so returning the object itself gives clean, parseable output:

```bash
for i in $(seq 1 120); do
  r=$(playwright-cli -s=pick --raw eval 'window.__pickerDone ? window.__picked : null' 2>/dev/null)
  [ -n "$r" ] && [ "$r" != "null" ] && { echo "$r"; break; }
  sleep 1
done
[ -z "$r" ] || [ "$r" = "null" ] && echo "TIMEOUT: no element picked in 120s"
```

Use the user's prompt below to tell the user what to click before you start
polling.

**Step 5: Return results**

- If `cancelled`, report the user cancelled.
- For a single pick or each multi entry, show `tag` / `id` / `classes` / `text`
  and the ready-to-use CSS `selector`.
- Detach so the user's browser stays up: `playwright-cli -s=pick detach`.

## User prompt (if any)

$ARGUMENTS
