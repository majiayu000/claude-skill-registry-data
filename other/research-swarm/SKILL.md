---
name: research-swarm
description: >-
  Turn any hypothesis, however fringe, into an argument map rather than a verdict: five
  independent lenses (consensus, skeptic, frontier, historian, experimental design), then a
  synthesis of for and against, evidence quality, a confidence tier and the cheapest decisive
  experiment. Triggers: "/research-swarm <hypothesis>", "map the arguments on X".
license: MIT
---

# /research-swarm — an argument map for any hypothesis (a swarm of research agents)

> 🧒 **When reporting to a non-technical operator:** end with a child-simple "In plain words" recap in their language.
> ⚖️ **Doctrine:** this skill IS the operational arm of `protocol-epistemic-neutrality-fringe-research`. NEVER judge or mock the hypothesis. Consensus ≠ truth. Build a map of arguments + confidence — **an investigation, not a verdict**. Bounded by `operating-agreement` safety invariants (no illegal/harm/bypass/fraud).

## When to use
The operator hands a hypothesis — frontier science (antigravity, perpetual motion, anomalous materials, radical longevity, models of consciousness/time), an unusual business model (DAO/network states, no-employee AI co, token labor markets), or a controversial/stigmatized vertical (adult, gaming, gambling). Goal: a balanced, grounded **argument map**, not a yes/no.

## The 5 lenses (run as a parallel swarm)
1. **Consensus** — steelman the current mainstream/established view. What does well-replicated science / the market actually hold, and why.
2. **Skeptic** — strongest arguments AGAINST. Where the idea breaks, hidden assumptions, falsification points, known failure modes.
3. **Frontier** — strongest arguments FOR. Steelman the believer: what would have to be true, adjacent emerging evidence, why it's not obviously impossible.
4. **Historian** — precedents and base rates. Ideas once dismissed then vindicated (and once hyped then debunked); the historical analog for THIS idea.
5. **Experimental-Design** — what measurement/experiment would confirm or refute, the **cheapest decisive test**, what data to gather first.

Each lens does light, targeted web grounding (WebSearch/WebFetch) — claims should be evidenced, not just model priors — but stays token-aware. The synthesis NEVER returns a verdict; it returns a confidence tier + open questions.

## Control node — Verifier-Calibrator (added 2026-06-15, via Alpha R+DR)
After synthesis, one **Verifier-Calibrator** node runs (the swarm's *acceptance function*, not another opinion). It (1) audits the strongest for/against claims — supported / partial / unsupported, (2) re-derives the confidence tier from **evidence** (support density + cross-lens agreement), not vibe, lowering tiers that rest on unsupported or single-lens claims, and (3) may **abstain**: the new tier `insufficient` is a first-class honest answer when evidence is too thin to place the idea on the established→fringe axis. The calibrated tier + claim audit + flags surface in the note and dashboard. This is the DR-recommended **control plane** over the 5-lens **content plane** (gaps: no verifier / qualitative-not-calibrated tiers / no abstain lane). Decision: vault `02-Decisions\decision-research-swarm-v2-upgrade`.

## How to run

**Step 0 — parse** the hypothesis from the operator's message (everything after the trigger). If it's a vague one-liner, ask ONE clarifying question first (scope/domain), else proceed.

**Step 1 — RECALL first** (token law — cheap before LLM/web). Pull what the operator already thinks on the topic:
```
python "$IMPORTS_ROOT/brain_ask.py" "<hypothesis>" --k 8
```
Keep the synthesized recall as `recall_context` (the operator's prior notes/leanings on the topic — feeds every lens so the swarm builds on their own thinking, not from zero).

**Step 2 — run the swarm** via the Workflow tool (this skill IS your explicit opt-in to orchestrate):
```
Workflow({ scriptPath: "%USERPROFILE%\.claude\\skills\\research-swarm\\workflow.js",
           args: { hypothesis: "<hypothesis>", recall_context: "<from step 1>" } })
```
The script fans out the 5 lenses (parallel barrier — synthesis needs all), a synthesis agent merges them, then the **Verifier-Calibrator** audits the strongest claims and calibrates the tier (or abstains → `insufficient`). Returns the structured **argument map** object with a `calibration` block.

**Step 3 — persist (backup first).** `python "$IMPORTS_ROOT/vault_backup.py"` then:
- Write the map as a vault note in `03-Insights\Research-Swarm\<YYYY-MM-DD>-<slug>.md` (frontmatter `type: insight`, `origin: anton`, `tags: [research-swarm, argument-map]`; body = for/against tables, confidence tier, historical analogs, open questions, the decisive experiment). Link it to `[[protocol-epistemic-neutrality-fringe-research]]` + `[[insight-glavnaya-tsel-tsifrovoj-dvojnik]]` and any concept the topic touches (no-orphan: ≥1 inbound).
- Dump the map object to `<skill>\last_map.json` and build the visual:
```
python "$USERPROFILE/.claude/skills/research-swarm/build_argmap_dashboard.py" <map.json> <out.html>
```
Dashboard → `$OBSIDIAN_VAULT/_Dashboards/Research-Swarm/<slug>.html`. Offer to open it (the operator works by eye).

**Step 4 — reindex** so the new note is searchable: `python "$IMPORTS_ROOT/brain_embed_update.py"`.

**Step 5 — report** to the operator: the confidence tier, the 2-3 strongest for/against, the cheapest decisive experiment, link to the dashboard — and the ELI5 recap. NEVER editorialize a verdict; present the map.

## Scaling (AK-47)
Default = 5 lenses, single pass. For a big/important hypothesis the operator can say "go deeper" → add a second round per lens or 3-vote adversarial verification of the strongest claims (loop-until-dry). Don't over-build by default.

## Relation
Operational arm of vault `protocol-epistemic-neutrality-fringe-research` · memory [[epistemic-neutrality]]. Pairs with `/alfa-search-recall-deepresearch` (R+DR — recall→gap→deep-research→synthesis; the swarm is the multi-lens synthesis engine). Distinct from `/ask` (single recall) and `/deep-research` (web fan-out, single perspective). Serves [[main-goals]] goal #1 — the twin reasons like the operator-the-researcher.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
