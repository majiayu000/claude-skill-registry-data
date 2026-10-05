---
name: claudeai-sync
description: >-
  Pull new and changed claude.ai web conversations into an Obsidian vault, extract artifacts as
  first-class notes, concept-link them, and refresh the RAG index and dashboard. Idempotent:
  curated notes are never overwritten. Triggers: "/claudeai-sync", "pull claude.ai", "grab new
  claude.ai chats".
license: MIT
---

# claudeai-sync — pull what's new from claude.ai into the vault

Account **owner.work@example.com** (Claude Max). claude.ai chats do NOT live on disk — they are pulled live through the logged-in session (Claude-in-Chrome). Semi-automatic: **PULL** (step 1) is done by me while the session is open; everything after that is deterministic and idempotent.

Scripts: `$IMPORTS_ROOT/claude-ai/` · originals → `$OBSIDIAN_ROOT/_originals/claude-ai-export/` · live layer → `01-Conversations/Claude-AI/`.

## ⚠️ The main landmine
The API exposes artifacts **ONLY** with `rendering_mode=messages`. `raw`/`default` silently return 0 artifacts. Always use messages + verify the artifact counter.

## ⚠️ Anti-recents (hunting for one specific chat by hand)
When looking for ONE specific chat by hand (not a full PULL) — NEVER conclude "the chat isn't there" from a glance at the recents list: (1) use the built-in "Search chats…" with keywords; (2) check Projects/archive/pinned; (3) confirm the active ACCOUNT by the email in the profile menu. More reliable still — the full API listing `chat_conversations?limit=1000` (the PULL step) instead of reading /recents with your eyes. Canon: memory [[web-ui-search-not-recents]] (incident 2026-07-23).

## Steps

### 1. PULL (in-session, ~30 sec)
- Claude-in-Chrome → `navigate https://claude.ai/recents`.
- `javascript_tool` (same-origin authed fetch), org = `<YOUR_ORG_UUID>` (roles chat+claude_max; a second org on the account is API-only, returns 403, ignore it):
  - the list: `/api/organizations/{ORG}/chat_conversations?limit=1000&offset=0`
  - each chat: `/api/organizations/{ORG}/chat_conversations/{uuid}?tree=True&rendering_mode=messages` → cache into `window.__convs`
  - projects: `/api/organizations/{ORG}/projects` + `/{uuid}` (descr + prompt_template) + `/{uuid}/docs` (content inline)
  - Blob-download it as ONE file `claude-ai-export-YYYY-MM-DD.json` (schema `claude-ai-export/v1`: {conversations, projects, filesManifest}).
    - ⚠️ `conversations` MUST be an OBJECT `{uuid: conv}`, NOT a list — the converter `claudeai_export_to_vault.py:120` calls `convs.items()` (a list → `AttributeError: 'list' object has no attribute 'items'`). `filesManifest` is a list of `{conv, msg, kind, meta}`. Under `rendering_mode=messages` artifacts arrive as `<antArtifact …>` INSIDE text items (NOT as `tool_use` blocks) — that is normal, the converter parses them.
- Move it out of Downloads into `raw\` + archive into `_originals\claude-ai-export\` (sha256). The full JS lives in the session journal of 2026-06-12 / memory [[claude-ai-export-to-vault]].
- (A delta pull is optional — the converter is idempotent by uuid; a full pull only adds what's new.)

### 2. SYNC (deterministic)
```
python $IMPORTS_ROOT/claude-ai/claudeai_sync.py
```
Converts into a temporary staging area → copies into the live layer **only the NEW** notes (existing ones, including linked ones, are left untouched) → refreshes the MOC + dashboard → writes the paths of new artifacts into `_new_artifacts.txt`. Prints `new_conversations / new_artifacts / new_projects`.

### 3. CONCEPT-LINK the new artifacts (MANDATORY — `concept-creation-rules.md` §1)
If `_new_artifacts.txt` is not empty:
- Workflow `claudeai-artifact-curation` (sonnet, one agent per artifact; ⚠️ above ~40 you hit a server-side rate limit, finish with `resume`) → concept proposals.
- `python apply_curation.py --result <workflow .output>` — validates slugs against the real `06-Concepts`/`09-Bridges`, writes links idempotently (a `<!-- curation -->` block + `related_concepts`/`summary`/`value_score`/tags).
- **Recurring themes with no concept → create new concepts** (threshold §1 ≥3), show them to the operator, then re-run apply (the new ones get picked up). One-offs — don't breed concepts for those.

### 4. RAG + commit
```
python $IMPORTS_ROOT/brain_embed_update.py        # or wait for the nightly run at 04:00
python $IMPORTS_ROOT/vault_backup.py
```
(`claudeai_sync.py --reindex --commit` does step 4 in one call; reindex rc=3 = the lock is busy, the nightly task will catch up.)

### 5. PING
A short summary to the operator (Telegram Saved Messages works fine): "claude.ai: +N chats, +M artifacts, linked."

## Notes
- **Idempotent**: a repeat run with no new data = "nothing new", and existing links are never lost.
- **Provenance**: artifacts get `origin: claude-ai, authored_by: claude` (NOT #anton-original); project instructions get `origin: anton`.
- **Binaries** (images/docs, 524 of them in the manifest) — the operator asked NOT to pull those (2026-06-12).
- **Auto mode**: the nightly Windows task `Claude-AI Sync Daily` runs the back half over any fresh export; the PULL stays in-session. Full headless ("it downloads itself") = moving to a dedicated Chrome profile + Playwright + a deterministic RAG linker — deferred (the operator chose the safe semi-automatic path).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
