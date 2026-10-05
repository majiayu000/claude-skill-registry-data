---
name: alfa-search-recall-deepresearch
description: >-
  Decision protocol for strategic work: recall the knowledge vault, run a gap analysis, emit a
  deep-research prompt for external tools, then synthesize the returned reports into a decision
  memo. Use before any new product, feature, market, pricing, GTM or architecture call, where
  local recall alone is not enough. Triggers: "/alfa-search-recall-deepresearch", "alpha
  protocol", "R+DR".
license: MIT
---

# 🅰️ Alpha Protocol — Recall + Deep Research before deciding

> 🧒 **When reporting to the operator:** end with a child-simple "In plain words" recap (his standing request; reports TO the operator only).

**Binding rule (must):** For ANY new strategic function, product, business model, tokenomics, AI-functionality, GTM, market, investment hypothesis, or architecture decision — it is **FORBIDDEN to go to implementation on recall alone**. Do `Recall → Gap → Deep Research → Synthesis → Decision Memo` first. Recall is necessary but NOT sufficient for strategic work. Canon: vault note `protocol-alpha-protocol-recall-plus-deep-research`.

## When this fires
- The operator writes the trigger: **`R+DR`** (= **`RDR`** — `+`/space & case don't matter), **`alpha protocol`** (or `/alpha`).
- OR you are about to start a **Level-2** task (below) — invoke this protocol proactively, don't wait for the trigger.

## Levels (size the response to the task)
- **L0 — Quick** (answer a question, fix a bug, tiny tweak): plain recall is enough. No DR.
- **L1 — Recall** (new module / hypothesis / feature / market): recall memory + internal docs + past research + form hypotheses. **Do NOT decide immediately.** Usually no external DR unless it turns strategic.
- **L2 — Recall + DR** (strategic — see binding rule): run the full flow below.

## ★ Proactive multi-agent reflex (EVERY task, not just strategic) — set 2026-06-25
The user FORGETS whether they need agents — so YOU remember and propose, reflexively, after RECALL on **any** task. Canon: vault `reglament-proaktivno-predlagay-agentov` + memory `multi-agent-offer-reflex`; tool-choice canon = `decision-adopt-agent-teams-scoped`.

1. **Cheap-first:** did SQL/grep/RAG already answer it? → done, no agents.
2. **Type = Decision · Comparison · Analysis · Research-synthesis** where several INDEPENDENT lenses materially improve the answer (inclusion test: *will one lens's finding redirect another before both finish?*)? NO (import/fix/ops/mechanical/trivial) → single agent, stay silent about agents. YES → multi-agent fits → fork:
   - **AUTO-RUN (announce, don't ask):** read-only · no vault write · no outbound · ~2 Sonnet agents · not huge → spawn advocate↔skeptic (or champion-X↔champion-Y, or N orthogonal lenses) then synthesize. First line: `🤝 Spawning 2 Sonnet agents (read-only)…`.
   - **OFFER + ASK (`+`):** vault-write/outbound · ≥3 agents or long/expensive · strategic-irreversible (→ full R+DR L2 below) · money/secrets/Tier-2. One line: `🤝 Agents: I recommend (…); shall I spawn them? (+)`.
3. Teammates on **Sonnet**; don't auto-keep an Opus lead; never ask for "consensus" — preserve dissent. Mechanism = Agent-tool subagents (cheap, ~80% of the value) or native Agent Teams when enabled.

This is **L1.5** — broader than the L2 strategic flow: it fires on everyday comparisons/analysis, not only big decisions. The advocate/skeptic/frontier panel below is the same machinery.

## The flow (what YOU, Claude Code, do)

**Step 1 — RECALL.** Pull EVERYTHING we already have on the topic (per the RECALL-before-activity rule):
- memory: `MEMORY.md` + grep the memory dir
- vault meaning: `python "$IMPORTS_ROOT/brain_ask.py" "<topic>"` (or `/ask`)
- vault exact: grep concepts/insights/protocols/people/leads
- SQLite facts where relevant (Platinum CRM, browser_history, etc.)
Report concisely: what we know · what we already researched · prior conclusions · prior mistakes.

**Step 2 — GAP ANALYSIS.** State plainly: what we do NOT know, which questions stay open. This sharpens the DR prompt so the external tool digs where we're blind, not where we're already strong.

**Step 3-pre — DR-DEDUP: first check whether this DR already exists (operator's order, 2026-07-14).** Plenty of sessions ordered a DR and never carried it to an external LLM; meanwhile the exporters (ChatGPT/Claude/Downloads) may have ALREADY pulled the report into the vault, the nightly `dr_collect.py` (hub, 05:05) flips the registry `issued→collected` on its own and `dr_synthesize` writes the digest — the registry status can be fresher than your memory. Before minting a NEW number, two cheap checks (0 tokens):
1. **The registry:** `grep -i "<topic keywords>" "$OBSIDIAN_VAULT/_DR-Registry.md"` (and/or `dr_registry.py list`) — is there already a DR on this topic, and in what state.
2. **The vault:** digests `03-Insights\insight-DR-*.md` + originals `_originals\deep-research\*<DR-ID>*` (grep by topic/ID).
The fork: **synthesized/collected** → do NOT re-order — read the finished report/digest and go straight to Step 4 (Synthesis); **issued** on the same topic → reuse THAT SAME ID (don't mint a new one) and emit the outbound prompt with it; **nothing** → mint a new one below. Canon: `reglament-numeratsiya-dr-i-reestr`, memory `dr-pipeline-endtoend`.

**Step 3 — DEEP RESEARCH PROMPT (hand-off).** ⭐ FIRST allocate the DR number (operator's order, 2026-07-03): `python $IMPORTS_ROOT/dr_registry.py new "<topic>" --tool <chatgpt|gemini|grok>` → prints `DRYY-MM-DD-MACHINE-NN` (machine code auto-detected — per-machine sequences, no sync collisions) and registers it in `_DR-Registry.md`. Put the ID as the FIRST line of the emitted prompt (`# DR26-07-03-ZB-01 — <topic>`) so the external chat inherits it as its title and exports match the registry. Counter unsure → `--gap` (+10). When the report comes back: `dr_registry.py update <ID> --status collected --file "<path>"` — OR do nothing: the nightly `dr_collect.py` will find the DR-ID in the imported chats/Downloads and flip the status itself (the ownership loop closes automatically; a manual update is only needed if you want the report RIGHT NOW). Canon: the house rule `reglament-numeratsiya-dr-i-reestr`. You do NOT run the deep research yourself. **Hybrid mode:** you MAY do a light in-session web pass (WebSearch/WebFetch) to sharpen the prompt and catch the obvious — but the deep, exhaustive DR is done in an EXTERNAL tool (ChatGPT/Gemini/Perplexity Deep Research). Emit the prompt for the operator to copy:
- Read the canonical template: `$OBSIDIAN_VAULT/08-Templates/deep-research-prompt-template.md` and emit it **filling `{topic}`**, prepending a `CONTEXT:` block with the recall findings + open questions from Step 2 (so the external DR doesn't redo what we know).
- ⭐ **Always append the `§1 UNIVERSAL ADD-ON` from `08-Templates\dr-platform-playbook.md`** (mandatory citations w/ URLs, confidence tiers, epistemic neutrality, decision-oriented ending). If the operator names the target vendor, or you know it, also append that vendor's block (§2 Grok / §3 Gemini / §4 ChatGPT) so the platform does DR better. Playbook = tuning layer over the universal template.
- Present it as one clean, clearly-marked copy-paste block. ⭐ **Standing mandate (operator, 2026-07-14): don't wait for him to carry the prompt anywhere — fan it out YOURSELF right away via `/dr-fanout` (ChatGPT+Gemini+Grok), any number of DRs, without asking** (we don't ration quotas; degradation is soft; duplicates are caught by Step 3-pre). The copy-paste block stays in the chat as a fallback in case he wants to run it himself.
- ⭐ **Two things into the chat, always (operator, 2026-07-17):** ① the full prompt text in a ```text``` block (paste-ready) + ② **a link to the actual research chat, the moment it exists**, without waiting for the report: `🔗 <vendor>: <url>` for every fan-out chat that started. The link = the private URL (`chatgpt.com/c/…` · `gemini.google.com/app/…` · `grok.com/chat/…`); a public share link is ⛔ by default (that is publishing outward). Couldn't capture the URL → say so honestly with the reason. Broader than DR: if you couldn't pull something out of the browser, give the operator the address to pull it from and he will. Canon: `reglament-vneshniy-resech-vsegda-promt-i-ssylka-v-chat`, memory [[dr-prompt-paste-in-chat]].

**Step 4 — SYNTHESIS + DECISION MEMO** (after the DR results come back). Merge memory + DR into a **Decision Memo**:
`the problem · what we already know · DR findings · options · risks · recommendation`.
Only AFTER the Decision Memo do we start implementation.
⭐ **Close the DR in the same pass (operator's "+", 2026-07-28):** the Decision Memo cites a DR-ID → in THAT SAME pass run `dr_registry.py update <ID> --status applied --note "<what closed it>"` (not adopting it → `--status parked --note "<why>"`). A memo that leaves the registry open = a half-built bridge. When ordering a DR in Step 3, name its consumer: `new --for "<the decision this report feeds>"` — with no consumer the report auto-parks after 30 days. Canon: the house rule `reglament-numeratsiya-dr-i-reestr` §amendment 2026-07-28, memory [[dr-finish-applied-or-parked]].

## Notes
- If a `/schedule`-style recurring research cadence emerges for a topic, evaluate per `evaluate-recurring-into-routine`.
- The DR prompt template is the single source — if it changes, edit the vault template file, not a copy.
- This skill is SEARCH+STRUCTURE; the deep-research harness skill (`deep-research`) is the in-session web variant the operator can opt into, but his default flow is the external hand-off above.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
