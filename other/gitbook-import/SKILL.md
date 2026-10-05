---
name: gitbook-import
description: >-
  Import a GitBook space (company docs, a whitepaper) into an Obsidian vault as linked atomic
  notes plus a map-of-content, concept links and a RAG reindex. Idempotent re-import supported.
  Triggers: "/gitbook-import <url>", "import this gitbook", "gitbook to vault".
license: MIT
---

# /gitbook-import — GitBook space → vault

> 🧒 When reporting to Anton end with a child-simple "In plain words" recap. (memory `eli5-always`)

Turns a live GitBook space into atomic vault notes. Proven on the Palo Alto / AAA «C(H+A)RM» GitBook (85 pages, 10 chapters, 694 links, 0 broken). Pipeline + slug rules = memory [[palo-alto-gitbook-import]]. This is the GitBook source-adapter; for any other source use [[obsidian-ingest]].

**Pipeline home:** `$IMPORTS_ROOT/gitbook/live/` — `slugs.py` (derive page URLs from TOC titles) + `build_live.py` (per-page notes + nav + concept links → `live\md\`). ⚠️ Both are **TEMPLATED for the Palo-Alto / AAA space** (org+space IDs, page-title list, `pa-gitbook-NN` slug, concepts, `origin`, MOC name are hardcoded; they do NOT read the `<url>`). So this command's clean path is **refreshing the Palo-Alto GitBook**. A **different** space = first edit those constants in the two scripts (or hand the raw pages to [[obsidian-ingest]]). There is **no** MOC-builder or copy-to-vault script — those steps are manual (see Steps 5–6).

## Credential boundary (Anton must clear it once)
GitBook login is a boundary I can't pass alone. Anton logs into the GitBook org in Chrome (the Palo Alto org = **bbplatinum** Google acct), THEN I scrape. If not logged in → escalate per [[chrome-autonomy-self-drive]] (open the login page in its own window, ask Anton to sign in, then continue). Don't try to brute the login.

## Steps
1. **Resolve pages:** from the space URL, get the TOC; `python $IMPORTS_ROOT/gitbook/live/slugs.py` derives per-page URLs. **GitBook slug rules:** lowercase, space→`-`, `&`→`and`, `(`/`)`→`-`, apostrophes/quotes/`$`→dropped (`$`→`usd` once), keep `.`/`+`/digits. Wrong slug → 404 → recover via the "Next"-link walk from the prior good page.
2. **Scrape (delegate to a Sonnet subagent — keep bulk text out of main context, [[model-routing-sonnet-grunt]]):** the subagent drives Claude-in-Chrome: navigate + wait ~3s + `get_page_text` per page, writes each to `pages\NN.txt`, returns ONLY a short report (page count + any 404s).
3. **Originals first ([[preserve-originals-rule]]):** copy raw pages to `_originals\<space-slug>\live-pages-<date>\`. Never delete.
4. **Backup ([[vault-backup-rule]]):** `python $IMPORTS_ROOT/vault_backup.py`.
5. **Build:** `python $IMPORTS_ROOT/gitbook/live/build_live.py` → per-page notes (`pa-gitbook-NN-*`) + nav + `_index.json` into **`live\md\`** (a staging dir, NOT the vault). Provenance is set by the script (`origin: Palo Alto Research Lab`); for a non-Palo-Alto space change that constant first.
6. **Move into the vault + MOC (manual):** copy the `md\*.md` notes to `05-Resources\<space-slug>\` and build/refresh the chapter-grouped MOC there (no script does this — by hand or via [[obsidian-ingest]]).
7. **Concept-link the NEW notes** (mandatory per concept-creation-rules) — create concepts where the §1 threshold is met (≥3 repeats, noun-entity, domain-anchored); self-create, don't ask ([[capture-rules-into-bible]] reflex).
8. **Validate + reindex:** link-check (expect BROKEN=0, 0 orphans), then `python $IMPORTS_ROOT/brain_embed_update.py --wait-gpu 10` (or rely on nightly reindex).

## Output
Pages imported · notes + MOC created · concepts added · links 0-broken/0-orphan confirmed. Then 🧒 recap. Re-import of an already-imported space = idempotent rebuild (md5 source vs `_originals` first, like [[crypto-essays-reimport-idempotent]]).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
