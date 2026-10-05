---
name: portret
description: >-
  Build a dossier on a person: recall everything the vault already knows, map their public
  profiles by web research, emit a deep-research prompt for external tools, and persist a
  well-linked person card. Triggers: "/portret <name>", "dossier on <name>", "profile <name>".
license: MIT
---

# /portrait — a deep dossier on a person

> 🧒 **When reporting to a non-technical operator:** end with a child-simple "In plain words" recap in their language.

An orchestrator: **RECALL (everything we already have) → WEB (all social profiles) → a DR prompt (Alpha Protocol) → a card in the vault → synthesis once the operator brings the DR back**. It chains `/find` + `/ask` + the Alpha Protocol + ingest, aimed at ONE person — a role model, a lead or a partner.

## Step 0 — RECALL first (cheap, before the web)
Pull up EVERYTHING we already have (the recall-before-activity rule):
- Memory: `grep` through `~/.claude/.../memory/` for the name and its variants.
- Exact name: `/find <name>` → `PYTHONUTF8=1 python "$IMPORTS_ROOT/namesearch/find_name.py" <name>` (catches transliteration, wrong layout, typos).
- Meaning: `/ask "<name> / topic"` (RAG over the vault).
- A direct vault grep for the Latin slug (`07-People\person-<slug>.md`, `01-Conversations\...\<slug>`, CRM leads, Facebook posts about them).
- **Check for an existing card** `07-People\person-<slug>.md` (plus `-2` duplicates) — ENRICH it, never breed a new one; duplicates → supersede (skill `dedup`).

## Step 1 — WEB: all social profiles (in parallel)
`WebSearch`/`WebFetch` (Chrome MCP when paywalled). Build a table: X/Twitter, Telegram (channel + personal), Medium/Substack/blog, LinkedIn, Facebook, Instagram, YouTube, GitHub/Gist, Keybase, personal site, fund/company, podcasts, academic trail. Mark confidence and any dead/suspended links. Cross-verify identity (handle ↔ Keybase/GitHub proof) and separate namesakes by handle, topics and companies.

## Step 2 — the DR prompt (Alpha Protocol; the deep DR is run by the operator in an external tool)
Emit a filled-in DEEP RESEARCH PROMPT as one clean block (subject, sources, CONTEXT from recall, 6-8 questions: psyche/character, mental models, evolution, influences, contradictions/blind spots, personal philosophy, "the imprint worth emulating"). Template: `08-Templates\deep-research-prompt-template.md`. I do not run the deep DR myself — a light web pass is fine.

## Step 3 — the card into the vault (backup → write → reindex)
1. `python $IMPORTS_ROOT/vault_backup.py "<label>"` BEFORE writing ([[vault-backup-rule]]).
2. `07-People\person-<latin-slug>.md` (Latin slug! the native-script name goes into `title:`/`aliases:`): who they are · ⭐ why they matter to the owner + the link to their goals · a table of every social profile · a map of how they think · what the vault already holds (the recall index) · personal history (DMs/calls/CRM) · connections and concepts. At least 1 inbound link (no-orphan).
3. Reindex: `python $IMPORTS_ROOT/brain_embed_update.py [--cpu]` (15-minute cooldown → `--force`).

## Step 4 — synthesis (once the operator brings the DR back)
Merge recall + DR → a Decision Memo `03-Insights\insight-*` ("what to adopt / how they think") and weave it into the dossier. Original reports → `_originals\<slug>-deep-research\` ([[preserve-originals-rule]]).

## Gates
- We do not touch their social accounts from the outside; outreach to the person is draft-first + an explicit "yes" from the operator (Tier-2).
- Grunt work (collecting profiles, frequency analysis of a corpus) can run on cheap-model subagents; the synthesis and the map of thinking need the top model.
- Reference precedent: an earlier dossier built exactly this way (see the matching `person-*` and `insight-*` notes).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
