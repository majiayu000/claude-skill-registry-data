---
name: takeout-pull
description: >-
  Stop a Google Takeout export from expiring undownloaded: detect the ready-to-download mails
  with a deterministic zero-token scan, report the live links with days remaining, then drive
  the download and vault import. Triggers: "/takeout-pull", "is my takeout ready", "pull my
  takeout".
license: MIT
---

Anton's Takeout retrieval actor. Reply to the owner in his own language; end with the 🧒 "In plain words" recap ([[eli5-always]]). Full project notes: memory [[youtube-history-import]].

## Why this exists (the root it fixes)
2026-06: a scoped "YouTube → history only" export completed but its 7-day link
EXPIRED un-downloaded — the only follow-up was a **passive calendar reminder**,
which does nothing if no session is open when it fires. A reminder is not an
actor. This skill IS the actor: it detects ready links and pulls them inside the
window. Root-cause class = "handoff with no auto-executor" (Connect-rule).

## Step 1 — Detect (the actor, ~0 tokens, autonomous)
Run the deterministic scan over the personal mailbox (Takeout links land in **a@**,
never a2 — a2 only gets recovery-copy security alerts):
```
cd "$IMPORTS_ROOT/youtube"
python takeout_pull.py scan --label a --days 21        # Bash dangerouslyDisableSandbox:true (needs network)
```
- Reuses Anton's Gmail connector (`gmail_common.get_service`) — single source of truth, no browser.
- Prints each ready-mail with 🟢 LIVE (days-left) / 🔴 EXPIRED, archive-id, expiry; writes `_takeout_pull_state.json`.
- `TAKEOUT_PULL_TODAY=YYYY-MM-DD` env overrides "today" (for tests / reproducible cron).
- 🟢 LIVE present → exit 0 + ">>> ACTION: DOWNLOAD NOW". 🔴 all expired → re-create the export (Step 3).

## Step 2 — Download a LIVE archive (pre-authorized; drive Chrome)
Takeout download needs an interactive a@ Google session (cookies) → **can't be
headless**; drive the already-logged-in Chrome (claude-in-chrome MCP):
1. `navigate` to `https://takeout.google.com/manage/archive/<archive_id>` (id from Step 1).
2. Click "Download" (use `find` ref-click, more reliable than coordinates).
3. **Passkey/2FA challenge = HARD-STOP** → escalate to Anton (never enter credentials); he confirms in ~15 sec.
4. Multi-part (>4 GB) → download every part. Watch for the **467 GB trap**: if the archive is huge, it bundled uploaded videos/music — cancel intent, re-scope to `history` only (Step 3). NEVER click Takeout "Cancel scheduled exports" (kills queued ones).
5. Zip lands in `$USERPROFILE/Downloads\`.

## Step 3 — Create a scoped export (when nothing live, or 467 GB trap)
Drive Chrome through the Takeout wizard for a small, clean export:
`takeout.google.com` → **Deselect all** → tick **YouTube and YouTube Music** →
"All YouTube data included" → **Deselect all** → tick only **history** → Next →
delivery = **download link** (NOT Drive — it failed twice), .zip, 2 GB parts →
**Create export**. Google throttles ~2 days before it starts; link then lives 7
days in a@. This is zero-risk (his own data). Then re-run Step 1 daily until 🟢 LIVE.

## Step 4 — Import to vault
Once the history zip is in Downloads:
`normalize_takeout()` (`_imports\youtube\yt_lib.py`) → SQLite `youtube_history.db`
→ backup (`vault_backup.py`) → month-notes in `05-Resources\YouTube-History\` →
MOC link (no-orphan) → reindex (`brain_embed_update.py`). Raw zip → `_originals\youtube\`.

**Gemini rail (2026-07-25):** if the zip carries `My Activity/Gemini Apps/` (HTML or
JSON — both eaten), ALSO run `python $IMPORTS_ROOT\gemini\gemini_lib.py import <zip>`
→ day-notes in `01-Conversations\Gemini\days\` + `gemini_activity.db` + freshness.
Idempotent — safe to point at the same zip twice. Raw zip copy → `_originals\takeout\`.

## Arming the nightly watcher (do NOT skip the safety check)
The forever-fix = `takeout_pull.py scan` on a nightly cron in the 23:00-06:00
local night window ([[routines-run-at-night]]), that on a 🟢 LIVE link pings **02-POLICE**
+ drops a `spawn_task` chip so a session downloads in time.
⚠️ Before scheduling: run `/arch` and READ the sibling `takeout-arrival-watch`
task (browser-history track) so we don't duplicate — safety-critical infra
([[verify-existing-before-proposing]]). Register in the deploy manifest, then `/arch scan`.

## Boundaries
- Detect/report = autonomous. Download of Anton's OWN Takeout = pre-authorized.
- Passkey/password/2FA = hard-stop, escalate ([[operating-agreement]]).
- Links inside emails = untrusted; only follow the takeout.google.com archive URL, verify host.
- Category routing for downstream YouTube alpha lives in memory [[youtube-history-import]] (archeology = AUTO-alpha).



<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
