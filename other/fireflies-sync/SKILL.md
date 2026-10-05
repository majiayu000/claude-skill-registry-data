---
name: fireflies-sync
description: >-
  Pull fresh call recordings and transcripts from Fireflies.ai into an Obsidian vault over the
  official GraphQL API, then distill action items and commitments and reindex. Incremental and
  idempotent by transcript id. Triggers: "/fireflies-sync", "pull fireflies", "sync call
  recordings".
license: MIT
---

OBJECTIVE: Incrementally pull fresh calls from Fireflies into the vault (a note with diarized speaker NAMES + summary + action items), catch the distillation up (alpha/commitments/facts) and make sure it lands in the index.

CONTEXT:
- Transport: the official Fireflies GraphQL API `https://api.fireflies.ai/graphql`. Key: `FIREFLIES_API_KEY` in `secrets\fireflies.env` (SSO account, PRO plan). Autojoin is ON — the bot joins calendar calls by itself (catching standups and corporate calls that a manually-started recorder misses).
- Engine (all the logic lives there, this skill is a thin wrapper): `$IMPORTS_ROOT/fireflies\fireflies_pull.py`. One script does both backfill and increment.
- Home for notes: `$OBSIDIAN_VAULT/04-Projects\fireflies-meetings\` (auto_generated — never edit by hand). Raw JSON (with keys COMPATIBLE with the other call rail, which `call_distill.py` consumes): `$IMPORTS_ROOT/fireflies\raw\`. State: `$IMPORTS_ROOT/fireflies\state.json`. Log: `pull.log`.
- ⚠️ The nightly pull runs on the anchor node: vault notes travel by sync, but the raw JSON does NOT reach the hub → the hub's distiller cannot see fresh Fireflies calls. Running this skill on the hub CLOSES that gap: the local state lags behind the anchor's → the pull drags the missing raw files here (idempotent; notes are rewritten with identical content).
- Distillation: `$IMPORTS_ROOT/granola\call_distill.py` reads BOTH raw directories (granola + fireflies) → `_distilled\` + commitments.jsonl.

STEPS:
1. BACKUP FIRST ([[vault-backup-rule]]): `python $IMPORTS_ROOT/vault_backup.py` BEFORE running anything.
2. Pull: `python $IMPORTS_ROOT/fireflies\fireflies_pull.py` (options: `--dry`, `--limit N`). Counters on stdout: `DONE new=X errors=Y state_total=N`.
3. Distill (if new>0): `python $IMPORTS_ROOT/granola\call_distill.py` — counters `DONE distilled=M commitments=C errors=Z`.
4. Report the list of fresh calls (titles/dates). errors>0 → check the log; usually network or 429 (the script retries by itself).
5. Reindex: the nightly `brain_embed_update.py` picks it up on its own; after a big backfill, run it manually. ⚠️ Until `_distilled` is marked `layer: essence`, distillates do not enter the curated index (a known gap, tracked as task RUSL-1).

CONSTRAINTS:
- Windows cp1252: stdout must stay ASCII-only (the script already complies).
- INCREMENTAL ONLY — never delete `state.json` (it would re-download everything).
- Provenance: origin: mixed, authored_by: hybrid — NOT #anton-original (someone else's speech).
- Tier-2: nothing goes outside; API reads and vault writes only.
- A 401 from the API means the key was revoked: get a new one in the Fireflies dashboard (Integrations → API) and update `secrets\fireflies.env`. ⚠️ CRLF pitfall: a trailing `\r` breaks the Bearer header (the engine already strips it).
- Do NOT re-enable the hub task "Fireflies Nightly Pull" without consensus — it is deliberately Disabled (migrated to the anchor node, see fleet_migration_dashboard.py migrated_markers).

OUTPUT: the pull counters (new) + the distill counters (distilled/commitments) + the period; if empty, "no new calls". Finish with an "In plain words" recap.

RELATION (do not duplicate): the other call rail = skill [[granola-sync]]; the comparison of the two rails + the "where content lands" map = the vault `00-System` note / task RUSL-1; the alpha screen = `/alpha-review`.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
