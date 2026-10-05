---
name: whatsapp-sync
description: >-
  Refresh WhatsApp text into an Obsidian vault (data layer, dashboard, group labels, contact
  notes). Text only, never downloads media, and pulls the recent window the live companion
  bridge exposes rather than a full multi-year archive. Semi-automatic by design: it drives the
  live bridge and needs the phone nearby. Triggers: "/whatsapp-sync", "pull whatsapp".
license: MIT
---

OBJECTIVE: Refresh the WhatsApp slice of the Second Brain — pull the recent text the live bridge exposes, rebuild the SQLite+FTS5 data layer, re-resolve names, re-label active groups, rebuild the dashboard, and refresh the vault notes (MOC + groups + optionally contact notes). Fully deterministic except the group-label step (Sonnet). Idempotent: `build_db.py` is a full rebuild from `raw_train/`, so re-runs never duplicate.

CONTEXT:
- Live bridge = `@oss_maintainer/whatsapp-mcp` (Baileys), main number "Tony PaloAlto ResearchLab" (jid `16213388980@s.whatsapp.net`). Memory [[whatsapp-mcp-integration]] has the full setup + pairing playbook.
- Pipeline home: `$IMPORTS_ROOT/whatsapp/`. Data: `whatsapp_train.db` (SQLite+FTS5) + `raw_train\` (JSON). Vault home: `$OBSIDIAN_VAULT/01-Conversations/WhatsApp/` (`_WhatsApp-MOC.md`, `_WhatsApp-Groups.md`, 9 contact notes). Dashboard: `_Dashboards\WhatsApp-Dashboard.html`.
- SCOPE: **TEXT ONLY.** Never `download_media`; ignore the `hasMedia` flag.
- Model routing: the group-label step is grunt classification → **Sonnet subagent** (per [[model-routing-sonnet-grunt]]). Contact-note summaries (CRM intel, not Anton's authorial voice) → Sonnet draft acceptable under the quality gate; escalate to Opus if weak.

⚠️ HARD SAFETY (corrected model, proven 2026-06-16):
- A 2nd client doing READ-ONLY (list_chats/list_messages) does NOT trigger AUTH_KEY_DUPLICATED — the server degrades it to read-only and coexists. Only WRITE ops (resolve_contacts) need sole-client (else they error harmlessly into read-only). So a read pull can run alongside the registered MCP.
- On Windows `subprocess.terminate()/.kill()` does NOT reliably kill the node child → zombies ACCUMULATE (found 11 once). Any spawn script must `taskkill /F /T /PID <its-own-pid>` in a finally block (see `nightly_pull.py`). The nightly twin does this; it kills ONLY its own child, never the registered server.
- Gentle on the main number ([[telegram-safety]] sibling): read-only, modest pacing; ban-risk was accepted consciously (variant A).

STEPS:
1. PULL-MODE decision. Call `mcp__whatsapp__get_my_profile`.
   - If it returns the profile → bridge is LIVE → use **PULL-LIVE** (step 2a). NEVER spawn `train_pull.py`.
   - If the tool is absent/errors (headless) → use **PULL-SPAWN** (step 2b).
2a. PULL-LIVE (preferred, no double-client risk):
   - `mcp__whatsapp__list_chats {limit:100}` → the chat list (jid, name, isGroup).
   - For EACH chat: `mcp__whatsapp__list_messages {jid, limit:50}` (bump to 100 only if a chat is high-value). Collect {id, from, fromMe, type, text, timestamp, hasMedia}. Pace gently.
   - Assemble `$IMPORTS_ROOT/whatsapp/live_pull.json` = `[{jid,name,isGroup,messages:[...]}, ...]` (Write tool) and run `python ingest_live.py` (→ raw_train/ + train_summary.json, the format build_db eats).
2b. PULL-SPAWN (headless only): pre-flight kill stray node, then `python train_pull.py` (it spawns ONE temporary client, waits ~45s for history sync, writes raw_train/ + train_summary.json), then hard-kill node.
3. BUILD DATA: `python build_db.py` (drops + rebuilds `whatsapp_train.db` from raw_train/ — idempotent; categorizes; named=0/1).
4. NAMES (DMs): if PULL-SPAWN, `python names_fix.py` (resolve_contacts + re-snapshot chats2.txt). If PULL-LIVE, optionally call `mcp__whatsapp__resolve_contacts {resync:true}` then re-list to upgrade numeric DM names. (Group subjects: the server is PATCHED to fetch real group subjects via groupMetadata on `get_chat` — after the next MCP restart `list_messages`/`get_chat` return real names; until then groups are labeled by content in step 6.)
5. DASHBOARD: `python build_dash_export.py` (→ `_Dashboards\WhatsApp-Dashboard.html` + `valuable_chats.json`).
6. GROUP LABELS (active groups, n_mine≥3):
   - `python extract_active_groups.py` (→ `active_groups.json`, compact content samples, 0 tokens).
   - Spawn ONE **Sonnet** subagent (Agent tool, model:'sonnet') to read `active_groups.json` and write `group_labels.json` = `[{jid,label,category,lang,confidence,one_line}]` (categories: work-business|household-community|project-windmill|family-personal|crypto-web3|longevity-health|services-vendors|other). No media, no WhatsApp tools.
   - `python apply_group_labels.py` (writes labels into DB, named=2 = INFERRED) then re-run `python build_dash_export.py` so the dashboard shows the labels.
6.5 GRAPH-LINK (Rail 1 people + Rail 2 concepts — the [[relink-mechanism]] applied to WhatsApp; rich path only):
   - `python link_people.py` (0 tokens): phone-join WhatsApp DM jid (=phone `last10`) → `apple-contacts\contacts.db` → `vault_matches` → CRM/person note → `people_matches.json`. Phone match = T1 (trust); name-only = T2 (DO NOT trust — surname-blind false positives).
   - For T2 candidates spawn a **Sonnet judge** (Agent, model:'sonnet') → `people_verified.json` (conservative: confirm only on surname+role match, else null = WA note stays canonical). Identity-critical: a wrong link corrupts the graph.
   - Concepts: create/confirm any NEW topic-concept (windmill-park, etc.) per concept-creation-rules (DUP-CHECK first — e.g. household already = `concept-bible-household`/`concept-bible-staff-hr`).
   - `python link_apply.py` (idempotent): writes "## 🔗 Graph" into each WA note (verified person/CRM + concepts) + back-links into the 4 rich targets = BIDIRECTIONAL. Run AFTER vault_backup. Verify 0 broken targets.
7. VAULT (BACKUP FIRST — [[vault-backup-rule]]): `python $IMPORTS_ROOT/vault_backup.py`, then:
   - `python build_groups_note.py` (→ `_WhatsApp-Groups.md`).
   - Refresh `_WhatsApp-MOC.md` counts if chat/msg totals changed. (Contact notes: refresh only if a key chat changed materially — keep open-action-items current; that's the high-value part.)
8. REINDEX (RAG): rely on the nightly Brain Reindex @04:00, or `python $IMPORTS_ROOT/brain_embed_update.py --wait-gpu 10` if Anton wants it searchable now.
9. REPORT: chats/msgs pulled, named vs ✎-inferred counts, new/changed open-action-items flagged for Anton, dashboard path. End with a 🧒 In plain words recap (messages TO Anton only).

CONSTRAINTS:
- WINDOWS cp1252: never print Cyrillic to python stdout (crashes) — scripts write UTF-8 files; keep stdout ASCII (counts only). ([[deterministic-script-gotchas]])
- The bridge has NO history pagination (`list_messages` limit≤100, no offset) — this refreshes only the recent window, NOT all years. Full archive = separate phone-backup path (variant B, not built). State this honestly; don't imply completeness.
- Re-applying the server group-subject patch: it lives in node_modules `dist\whatsapp.js` (getChat) — re-apply after any `npm update @oss_maintainer/whatsapp-mcp` (documented in [[whatsapp-mcp-integration]]).

ALWAYS-MODEL (Anton 2026-06-16): graph-linking is NOT optional — it is how we ALWAYS work with WhatsApp. Split by cost:
- **NIGHTLY auto (0 tokens, deterministic): Windows Task "WhatsApp Nightly Sync" @ 03:00 daily** = `nightly_sync.cmd`: `nightly_pull.py` → build_db → apply_group_labels (re-applies persistent `group_labels.json`) → dashboard → groups note → **`link_people.py` → `link_apply.py`** (re-weaves KNOWN verified people from `people_verified.json`, idempotent) → vault_backup. Keeps data + dashboard + known labels + known people-links fresh every night.
- **MANUAL/weekly (LLM): THIS skill** does the judgment-needing parts — Sonnet labels brand-NEW groups, the Sonnet judge confirms identity of NEW people (appends to `people_verified.json`), and contact-note open-items get refreshed. So: new people/groups enter via the rich path; the nightly twin then maintains them forever, free. Single source of truth = the scripts in `_imports\whatsapp\` + `people_verified.json`.

RELATION (do not duplicate):
- First-time setup + pairing + gotchas + the nightly task: memory [[whatsapp-mcp-integration]] (single source of truth). Automation registry: [[automation-inventory]].
- Sibling sync skills: [[health-sync]] / [[faaa-sync]] / [[telegram-reimport]] (same on-demand-refresh architecture). Routine policy: [[evaluate-recurring-into-routine]] — nightly cheap data twin + this richer manual LLM path.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
