---
name: notebooklm
description: >-
  Drive NotebookLM over a programmatic CLI with no browser: turn a vault slice into an audio
  overview, study guide or mind map, and fold the artifacts back into the vault. Browser
  automation is the fallback if CLI auth breaks. Triggers: "/notebooklm", "make an audio digest
  of <topic>", "podcast from the vault".
license: MIT
---

# /notebooklm — audio/artifact layer over the Second Brain

> 🧒 When reporting to Anton end with a child-simple "In plain words" recap. (memory `eli5-always`)

NotebookLM = the **artifact/explanation layer** (Audio Overview, study guide, mind map, reports) over the vault — NOT memory or RAG (that stays Obsidian + e5/rerank + SQLite). Flow: `vault → Claude Code curates a NARROW packet → NotebookLM → artifacts back into vault as Derived`. Full state = memory [[notebooklm-integration]].

## Rail = CLI (verified 2026-07-04, ADOPT — H16)
Programmatic CLI `teng-lin/notebooklm-py` (17k⭐, MIT). No Chrome window, no DOM, no truncation. Works on Anton's consumer `a2@` PRO (no Enterprise API).
- **CLI binary:** `%USERPROFILE%\notebooklm-cli\venv\Scripts\notebooklm.exe` (venv, v0.7.3). Set `NB="%USERPROFILE%\notebooklm-cli\venv\Scripts\notebooklm.exe"`.
- **Auth:** browser-cookies from Firefox (Chrome/Edge blocked by App-Bound Encryption + Chrome 146 DBSC, TPM-bound — Firefox does neither, see `02-Decisions\decision-2026-07-16-browser-automation-layer.md`). Stored `%USERPROFILE%\.notebooklm\profiles\default\storage_state.json`, account `owner.work@example.com`.
- **Cookies expire ~every few weeks** → on any `auth`/`401` failure, RE-LOGIN: Anton opens NotebookLM in **Firefox** (a2@), then `"$NB" login --browser-cookies firefox --account owner.work@example.com`. Verify with `"$NB" auth check`.
- **⚠️ Fallback if `login --browser-cookies firefox` picks the WRONG profile or fails to find the session** (the CLI's cookie-reader can hit the same class of bug as generic browser_cookie3-style libs: it may grab a stale `[ProfileN] Default=1` profile instead of the one Firefox actually launches — fixed once already in our own helper, see [[deterministic-script-gotchas]]): build `storage_state.json` directly with the fleet-shared, /tt-tested helper instead of fighting the CLI's own extractor:
  ```bash
  python "$env:USERPROFILE\.claude\scripts\_shared\firefox_cookies.py" --domain google.com --export "%USERPROFILE%\.notebooklm\profiles\default\storage_state.json"
  ```
  Then `"$NB" auth check` to confirm. Canon: `02-Decisions\decision-2026-07-16-browser-automation-layer.md`, DR26-07-16-HUB-01. (Note: fb-post/x-post/fb-reply do NOT use this path — they drive Anton's live logged-in Chrome tab via Claude-in-Chrome MCP, a deliberate anti-ban choice; `firefox_cookies.py`/`firefox_login.py` are for API-style clients like this one, not for social posting.)
- **Anti-abuse:** run from the hub (residential IP), **no VPN**.

## digest (default) — vault → audio
1. **RECALL + curate a NARROW packet** ([[vault-data-architecture]]): `brain_ask.py`/`/ask` + grep to pull ONLY the relevant slice. Write it to a clean `.txt`/`.md` packet.
2. **Create + add source + generate (CLI):**
   ```bash
   NB="%USERPROFILE%\\notebooklm-cli\\venv\\Scripts\\notebooklm.exe"
   "$NB" create "<Title>" --use                       # --use sets current context (don't parse --json 'id' — key differs)
   "$NB" source add "<packet.md>" --type file          # uses current context; or --type text "<inline>", or a URL. Wait for Status=ready.
   "$NB" generate audio "<style hint>" --length short --wait   # uses current; or generate mind-map / report / flashcards…
   ```
   Other artifacts: `generate mind-map | report | flashcards | quiz | slide-deck | video | data-table | infographic`.
3. **Pull artifacts back:** `"$NB" download audio "05-Resources\NotebookLM\artifacts\audio\<name>.mp3"` (current context; or `--all <dir>`, `-n <id>`). Non-audio: `artifact export`. Get the notebook id for the index: `NBID=$("$NB" list --json | python -c "import sys,json;print(json.load(sys.stdin)[0]['id'])")` (newest first).
4. **Index + link:** add the notebook/artifact to `05-Resources\NotebookLM\_NotebookLM-Index.md`; link the derived note back to its source concept(s). Backup before vault write ([[vault-backup-rule]]).

## pull — Phase B
Pull existing artifacts from the top notebooks into the vault as Derived notes: `"$NB" list` → `download ... --all` per notebook → index + link.

## Fallback — Chrome-autonomy (only if CLI breaks)
If Google rotates endpoints and the CLI errors (and a re-login doesn't fix it), drive the logged-in UI via Claude-in-Chrome ([[chrome-autonomy-self-drive]]) on `a2@`: Create notebook → Add sources → Studio → generate → **Download** menu (NOT DOM-scrape, truncates ~1000 chars). This was the old primary rail; kept as backstop.

## Safety
- CLI uses undocumented Google APIs (community project) — same ToS surface as driving the logged-in UI of the same account; low-med risk for personal volumes.
- Audio/video generation has a **daily quota** — don't burn it on test runs; add `--retry` + delays for batches.
- Stay on a2 PRO (free, included — [[prefer-included-limits-before-paid-api]]).

## Output
Notebook created/used · artifact type + where saved · index updated. Then 🧒 recap. Routine candidate: weekly "audio digest of my brain" — see /skill-gap and [[evaluate-recurring-into-routine]]. Decision: `02-Decisions\decision-notebooklm-claude-code-artifact-layer`.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
