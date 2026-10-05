---
name: ask
description: >-
  Ask the second brain in plain words: semantic search over the curated vault with embeddings
  plus a reranker, returning the smallest relevant slice instead of a corpus dump. Token-cheap.
  Triggers: "/ask <question>", "what do I have on <topic>", "what did I write about X".
license: MIT
---

# /ask — query the Second Brain

> 🧒 **When reporting to a non-technical operator:** end with a child-simple "In plain words" recap in their language.

Deterministic-first (the operator's token law): RAG retrieves the smallest relevant slice; synthesize ONLY that — never dump the corpus.

**Wrong lane?** /ask = semantic MEANING over the curated vault. For exact WORDS inside chats → `/search`; an exact PERSON name → `/find`; a CHAT by name → `/chat` (all 0 tokens, deterministic). Use those when the question isn't conceptual.

## 🖥️ Visual search (a live server — the operator works visually)
For interactive eyes-on search: `python "$IMPORTS_ROOT/ask_server.py"` (or `start_ask.bat`) → open `http://127.0.0.1:8770`. It loads e5 + reranker ONCE, after which each query takes ~3s. A search box + filter chips (my writing only / concepts / insights / leads / people / conversations / notes), cards with the rerank score, type, date and a ⏳ staleness flag. CPU by default (does not fight the GPU fleet, holds 0 VRAM); `--gpu` when the GPU is free. This is the GUI for the operator; `--ask` below is for me synthesizing an answer in chat.

## Run (CLI — for synthesizing an answer in chat)
`python "$IMPORTS_ROOT/brain_ask.py" "<question>"`
Scope with filters (cheaper + sharper):
- `--anton` (only the owner's own writing) · `--concepts` (distilled "what I think about X") · `--insights`
- `--person <name>` · `--conv` (conversations) · `--leads` (CRM)
Returns top-K chunks (chunked + tagged + edit-aware index); may flag `⚠ STALE` on volatile facts >90d.

## Answer
- Synthesize the returned hits into a DIRECT answer; **cite the note titles** so the operator can open them.
- If a hit is `⚠ STALE`, say so and offer to re-verify (per the epistemic-decay layer).
- If retrieval is thin/irrelevant → say so, suggest a sharper query or a filter; do NOT pad with guesses.
- Keep it tight; end with 🧒 recap.

## Note
The index is kept fresh by the reindex routine. If results feel stale right after a big import, mention a reindex may be due (`brain_embed_update.py`) — but don't reindex unprompted.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
