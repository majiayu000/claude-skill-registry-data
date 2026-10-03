---
name: restart-gemini
description: 重啟 LazyGravity → Antigravity（Google 的 Gemini IDE）整條遙控鏈並驗證有在動。當使用者說「重啟 gemini / antigravity / lazygravity」、Discord 回報 "Workbench page for workspace ... not found within 30 seconds"、workspace 連不上、或 /restart-gemini 時使用。會依序：起 Xvfb :99、在 CDP 9223 上啟動 Antigravity、重啟 lazygravity-bot 與 autoapprove service，最後透過 CDP 實際驗證 workbench 頁面可連。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [lazygravity, antigravity, gemini, discord, cdp, restart, xvfb]
---

# Restart Gemini (LazyGravity → Antigravity control chain)

Use when Antigravity / LazyGravity needs restarting — typically the Discord error
**`Failed to connect to workspace: Workbench page for workspace "X" not found within 30 seconds`**,
or the user says「重啟 gemini / antigravity / lazygravity」.

## Just run it

```bash
bash ~/.hermes/skills/restart-gemini/scripts/restart.sh
```

Idempotent: safe to run anytime. Flags: `--no-bot` leaves the Discord bot untouched
(only fixes Xvfb + Antigravity); `--no-clean` keeps orphan blank windows instead of
closing them. Then tell the user to retry the workspace command in Discord.

## Not every failure is a restart problem

**Read step [5/5] of the output before telling the user to retry.** A restart fixes a
dead/frozen IDE. It cannot fix a *stale binding*, and the two look nothing alike:

| Discord error | Meaning | Fix |
|---|---|---|
| `Workbench page for workspace "X" not found within 30 seconds` | Antigravity/Xvfb down | this skill |
| `Timeout calling CDP method Runtime.enable` | renderers frozen (GPU process died) | this skill (step 2 auto-retries) |
| `Failed to activate session "X" after N attempt(s) (direct: Chat title not found in side panel; past: Conversation not found in Past Conversations)` | **the conversation is gone from Antigravity** | **`/new` in that channel** — restarting is useless |

The third case is real: on 2026-07-21 all 7 named sessions in `antigravity.db` were
stale — Past Conversations held ~22 chats, none newer than ~1 month and **none labeled
`src`** — while the stack itself was perfectly healthy. Bot-created conversations do not
survive in the history the way workspace-opened ones do, so bindings rot silently.
Step [5/5] (`check_sessions.cjs`) now detects this by driving the real Past Conversations
widget per bound session, so the skill stops recommending a pointless restart.

## Why this is needed (the architecture)

LazyGravity (Discord bot `Ado#4549`, `~/src/LazyGravity`) drives the Antigravity IDE
remotely over Chrome DevTools Protocol. As of 2026-07-05 the **whole stack is systemd
`--user`**, tied together by `lazygravity.target`:

| Unit | What |
|------|------|
| `openclaw-xvfb.service` | headless X display **:99** |
| `lazygravity-antigravity.service` | Antigravity IDE on :99, CDP **9223** (Requires xvfb; forces X11 ozone) |
| `lazygravity-bot.service` | the Discord bot (`DISPLAY=:99`); ordered `After=` antigravity |
| `lazygravity-autoapprove.service` | clicks "Always Allow" browser prompts |
| `lazygravity.target` | pulls in all four; `WantedBy=default.target` (starts at boot) |

All enabled → **survive reboot**. The antigravity unit holds in `activating` (via
`ExecStartPost` polling) until CDP 9223 actually answers, so the bot won't start talking
to a not-yet-ready IDE.

**Historical gotcha (now solved by the target):** in the task path the bot does NOT
auto-launch Antigravity — it only launches it via the `open` command. Before it was a
service, if Antigravity wasn't up on CDP 9223 every workspace command timed out with
"workbench page not found". Two causes were: Xvfb :99 down, or Antigravity not running.
Now the target keeps both up (and `Restart=always` respawns Antigravity if it crashes).

Key facts:
- Port **9223** is fixed by `ANTIGRAVITY_ACCOUNTS=default:9223` in `~/src/LazyGravity/.env`
  (9222 is Hermes's own Chrome — don't touch it).
- The antigravity unit runs the **Electron binary directly**
  (`/usr/share/antigravity/antigravity`), not the `bin/antigravity` CLI wrapper (which
  detaches). It **must force X11** (`--ozone-platform=x11` + `XDG_SESSION_TYPE=x11`);
  the login session is Wayland and the binary otherwise picks Wayland and **segfaults**.

## What the script does

1. Restarts `lazygravity.target` (or, with `--no-bot`, just Xvfb + Antigravity) and waits
   for CDP 9223 to answer HTTP.
2. **Renderer liveness probe** (`scripts/probe_cdp.cjs`): attaches a WebSocket to EVERY
   workbench page and runs a real `Runtime.evaluate`. This matters because the HTTP
   `/json` endpoints are served by the *browser* process and stay green even when every
   renderer is frozen — seen 2026-07-18: Antigravity's **GPU process died on startup**,
   all renderers blocked waiting for a GPU channel, 12 page targets listed but every
   `Runtime.enable` timed out (Discord error: `Failed to connect to workspace: Timeout
   calling CDP method Runtime.enable`). **If any page hangs, the script automatically
   restarts Antigravity once more and re-probes** (2 attempts max, then tells you to
   check the GPU process: `ps -eo pid,args | grep -F -- --type=gpu-process`).
3. **Closes orphan blank windows** (`scripts/clean_windows.cjs`, `--close`; skip with
   `--no-clean`). Restarts leave behind folder-less windows with an untouched new-chat
   panel — useless to the bot (it routes by workspace) but each keeps a renderer alive.
   On 2026-07-21 there were **32 of them holding ~20.4 GB RSS**; closing them dropped
   Antigravity to **3.0 GB**, which matters because system-wide earlyoom SIGKILLs at
   1.5 GB free during GPU jobs. A window counts as blank only if `document.title` is
   *exactly* `Antigravity`, the Explorer has 0 roots, and the agent panel still shows the
   empty composer; unresponsive pages are left alone.
   **They come back**: Antigravity session-restores its window list, so closing them via
   CDP does not stick across a restart — that is why this runs on every invocation
   rather than as a one-off fix.
4. Prints each unit's active state, CDP status, and the open **workbench** pages
   (workspaces the bot can reach, e.g. `ComfyUI - Antigravity - …`).
5. **Verifies bound chat sessions still exist** (`scripts/check_sessions.cjs`) — see
   "Not every failure is a restart problem" above. Reads `antigravity.db`, and for each
   named session drives the real Past Conversations widget in that workspace's window.
   Prints `ok` / `STALE` / `?` per session.

## Manual verification (if needed)

```bash
curl -s http://localhost:9223/json/version                  # CDP alive?
curl -s http://localhost:9223/json/list | python3 -c "import sys,json;[print(p['type'],p.get('title')) for p in json.load(sys.stdin)]"
cd ~/src/LazyGravity && node dist/bin/cli.js doctor          # full check (CDP ports)
```

To prove the chain end-to-end you can connect to a workbench page's
`webSocketDebuggerUrl` and `Runtime.evaluate` (e.g. check `document.querySelector('.monaco-workbench')`).

## Antigravity UI selectors (verified 2026-07-21)

Needed by `check_sessions.cjs`; re-verify these if Antigravity updates:

- Agent panel: `.antigravity-agent-side-panel`
- Past Conversations toggle: `[data-past-conversations-toggle]` (the clock icon)
- The conversation picker is a **custom React widget, `.jetski-fast-pick`** — *not* a
  VS Code quick-pick. Its rows are plain `div`s, so `.monaco-list-row`,
  `[role="option"]` and `li` all miss them (this is why LazyGravity's own
  `buildActivateViaPastConversationsScript` fails to select a conversation).
- Search box inside it: `input[placeholder="Select a conversation"]`; it is React-
  controlled, so type with CDP `Input.dispatchKeyEvent` char events — setting `.value`
  does not filter the list.
- Empty result renders the literal text `No items found`.
- **Beware**: typing without focusing that input first lands in VS Code's quick-open
  overlay, which also shows "No items found" — an easy way to fake a false STALE.

## Notes / caveats

- (Outdated note removed: Antigravity *is* a `systemd --user` unit now —
  `lazygravity-antigravity.service`, `Restart=always` — see the table above.)
- Workspaces live under `WORKSPACE_BASE_DIR=~/src` (e.g. `~/src/ComfyUI`).
- Don't kill CDP **9222** — that's Hermes's Chrome, not Antigravity.
