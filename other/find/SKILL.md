---
name: find
description: >-
  Find a person, lead, contact or company by name in any spelling: a deterministic search that
  catches transliteration across alphabets, wrong-keyboard-layout typing and typos. This is the
  exact-name lane (zero tokens), complementary to semantic vault search. Triggers: "/find
  <name>", "show everyone named <X>".
license: MIT
---

# /find — smart search for a name or company by SPELLING

> 🧒 **When reporting to a non-technical operator:** end with a child-simple "In plain words" recap in their language.

Deterministic, 0 tokens — **NOT RAG**. Embeddings do not understand mangled spellings, typos or a wrong keyboard layout; that is caught by separate code using phonetic fingerprints + fuzzy comparison. For search by MEANING use `/ask`, not this.

## When to come here
"find Viktor" · "all the Viktors" · "find the company Merlion" · "who is <name>" · wrong-layout gibberish / typos / transliteration — any PERSON, lead, contact or COMPANY name in any spelling.

## Run (ALWAYS with `PYTHONUTF8=1` — otherwise a cp1252 crash on the Windows console)
`PYTHONUTF8=1 python "$IMPORTS_ROOT/namesearch/find_name.py" <name> [--html] [--all]`
- by default: leads + people + companies + Apple contacts (vault note titles hidden)
- `--all` — also include the note titles of the whole vault
- `--html` — a visual dashboard in `_Dashboards\Name-Search-*.html` (the operator works visually — offer it for long lists)

A name written in its native script produces a clean query; a wrong-layout or typo'd query is expanded automatically.

## Neighbours
- `expand_query.py <word> [--grep] [--line]` — expand a word into every spelling, for grepping the vault or feeding into `/ask` (the RAG hook).
- The `names.db` index is rebuilt by a weekly task (and manually via `name_index.py --vault`). If something is missing right after a big import, mention that a rebuild is due; do not run it unasked.

## The answer
- Give a list/table (display · type · file link); for a long one, the `--html` dashboard.
- A company surfaces first for a company query, together with its related people.
- 0 hits → say so plainly, suggest checking the spelling or rebuilding the index; never guess.
- Keep it short; end with the 🧒 recap.

## Do not confuse
`/ask` = by meaning (RAG, embeddings). `/find` = by spelling (a deterministic fingerprint). Canon memory [[smart-name-search]].


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
