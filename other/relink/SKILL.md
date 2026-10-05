---
name: relink
description: >-
  Weave a new node (concept, framework, theory, project, principle) into the whole vault graph
  rather than just creating a note. Mode A links one new node against the vault by top-K
  retrieval, with the LLM judging only those candidates; mode --deep finds orphaned islands and
  wires them in. Backup before edits, preview before writing. Triggers: "/relink", "integrate
  this concept".
license: MIT
---

# /relink — wire the important stuff into the graph (don't just add a note)

> 🧒 **When reporting to a non-technical operator:** end with a child-simple "In plain words" recap in their language.

**The principle (canon: [concept-creation-rules.md]($OBSIDIAN_VAULT/08-Templates/concept-creation-rules.md) §11):** an important new idea that only *exists* as a note is an island, not part of the Second Brain. It must be *integrated* into the knowledge graph. Mirror of [[no-orphan-notes-rule]] (passive "≥1 inbound"); this is the active "maximize meaningful connectivity for important nodes" side.

**Architecture law (from the DR):** **retrieval first → judgment second → writing last.** The LLM never decides links by reading the whole vault; it gets a bounded, diverse candidate pool, then types relations and proposes edits. Less hallucination, explainable, repeatable.

## What counts as "important" (don't run for every note)
A NEW: concept · mental model · framework · theory · term · project · philosophy · research cluster · personal principle · knowledge-organization system. Threshold = §1 of concept-creation-rules (≥3 recurrences, noun-entity, domain-bound). Routine notes → passive no-orphan check, not this.

## ⚠️ Token law — channels FIND, LLM JUDGES (never scan all 154k notes)
The operator's law ([[vault-data-architecture]]): cheap tools first; the LLM judges only the top-K.

---

## Mode A — integrate ONE new node (default)
Input: the new note's path/name (or freshly pasted text → first save via obsidian-ingest, then relink).

### 1. Extract entities (cheap — read ONLY the new note)
List: canonical concepts · aliases/acronyms · key claims · related domains · possible parent/child concepts · candidate MOCs. (LLM + the note's own frontmatter; no vault scan.)

### 2. Gather candidates from 3 channels (NOT scan-all)
- **Lexical** — `python "$IMPORTS_ROOT/namesearch/find_name.py" "<each named entity>"` (exact/translit/typo, 0 tokens) + grep literal mentions + alias/unlinked-mention matches.
- **Semantic** — `python "$IMPORTS_ROOT/brain_ask.py" "<node + its entities>"` (e5+reranker; finds hidden 2nd/3rd-order links: causality, analogy, shared mechanism, opposing view). e5 is multilingual → RU/EN drift is covered.
- **Hub-awareness** — `incoming_counts` in `$IMPORTS_ROOT/orphan-scan/reverse-index.json` (basename→inbound count, free): mark which candidates are **hubs/MOCs** (high count) vs **orphans** (0). Used by the reverse-link + MOC policy below. *(Full 1/2-hop adjacency graph = deferred future enhancement; semantic channel already covers conceptual neighbours.)*
- Cross-check `06-Concepts/` + aliases + `09-Bridges/` so you don't propose a dupe (defer to concept-creation-rules §5).

### 3. Fuse + rank P0–P3
Fuse the channels (RRF-style — don't add raw scores from different rankers). Soft ranking heuristic:
`≈ 0.35·semantic + 0.20·lexical + 0.15·entity_overlap + 0.20·hub/MOC_fit + 0.10·freshness` (zero freshness if evergreen).
- **P0** — missing link breaks navigation/understanding; exact alias/unlinked mention; parent concept; canonical MOC missing; evidence from 2+ channels.
- **P1** — strong thematic / cross-domain bridge / method / example / contrast.
- **P2** — useful "see also"; add only if it doesn't bloat the note.
- **P3** — weak/speculative → DON'T write; log in the memo as backlog.
**No link without evidence.** Low confidence → defer, don't write.

### 4. Type each accepted link (closed vocabulary)
`defines · defined_by · extends · depends_on · contrasts · example_of · evidence_for · method_for · same_cluster · moc_member · see_also`. Write it as a short gloss after the link: `- [[Target]] — method_for: <one phrase why>`.

### 5. Build the change-set (PREVIEW — don't write yet)
For each edit produce an internal record `{path, target_type: heading|frontmatter, target: "Related", operation: append_once, text, dedupe_key: "source::target::relation"}`.
- **Forward links** — into the new note's `## Related` (always for P0/P1, sometimes P2).
- **Explicit reverse links — SELECTIVE, not for symmetry's sake.** A forward link already creates an automatic backlink, so add an explicit reverse inline link ONLY if: target is a concept hub/MOC · relation is asymmetric & operationally important (`depends_on`/`defined_by`/`extends`) · target loses context without it · source gives target a new example/contrast/method. **Do NOT** add a reverse link into a dense hub/glossary where the auto-backlink already suffices (avoids overlinking).
- **MOC/hub wiring — this is the real "old→new" that matters:** ensure the new node appears in the right MOC/hub (≤2 MOCs; new MOC only in `--deep`). Prefer MOC sections `Core/Related/Methods/Debates/Examples` over a dump.
- **Missing notes** — propose; create concepts yourself per concept-creation-rules §1 (no-ask).
- **Caps:** ≤5–7 new links per normal evergreen note per run (MOCs exempt), ≤3 per section.
- Show the change-set as a BEFORE→AFTER table on the operator's REAL notes ([[show-before-after]]). **Wait for their OK.**

### 6. Backup → apply (idempotent)
- `python "$IMPORTS_ROOT/vault_backup.py"` BEFORE any write ([[vault-backup-rule]]; runbook = skill `obsidian-backup`).
- Apply each change-set record with `append_once` semantics: **before adding a link, check it isn't already in the section** (dedupe_key) — re-running /relink must be a no-op on already-done links.
- Insert into the `## Related` block; never mangle adjacent list lines (⚠️ dedup-skill grabli: never batch-Edit list deletions).
- Optionally stamp `relink_last_run: <date>` in the new note's frontmatter (feeds the monthly audit).

### 7. QA → reindex → report
- **Preflight/QA (blocking):** broken target, duplicate patch, missing evidence for a P0/P1, too many links in one section, MOC update without a relevance reason.
- `python "$IMPORTS_ROOT/validate_links.py"` → 0 broken.
- orphan re-check on touched notes; `python "$IMPORTS_ROOT/brain_embed_update.py"` → RAG sees the new edges ([[reindex-routine]]).
- **Integration Memo** to the operator: importance reason · main bridges (typed) · notes updated · links added · MOCs touched · concepts created · deferred/rejected candidates · QA counts. End with 🧒 recap.

---

## Mode B — `--deep` (deep relink: whole vault → islands)
Monthly/on-command sweep over the ALREADY-COMPUTED orphan list (not a fresh full scan).
1. `python "$IMPORTS_ROOT/orphan-scan/orphan_scan.py"` → refresh `orphans.csv` / `orphans-by-folder.csv` ([[vault-orphan-baseline]]).
2. `python "$IMPORTS_ROOT/orphan-scan/build_dashboard.py"` → `$OBSIDIAN_VAULT/_Dashboards/Vault-Orphans.html` (the operator works by eye).
3. Also surface: orphan clusters · missing MOC membership · alias gaps · high-centrality notes (high `incoming_counts`) without a hub · stale MOCs. Run top island clusters through Mode A steps 2–7. Loop-until-dry (stop at intentional orphans: archives, raw originals).
4. Dupes/near-dupes found → hand to skill `dedup` (don't merge here).
5. New MOC may be proposed here for a stable 5+ note cluster with no hub. Report what got woven in + what was deliberately left.

## Mode C — relink a whole THEME / topic cluster ("relink everything about X")
Between A and B: the operator names a TOPIC, not one note. Run **Mode A steps 2–7 with the THEME's entities as the query** (RAG + namesearch + grep on theme terms → judge top-K). Then, before proposing links:
- **Map what already exists** (concepts + MOCs + bridges in the domain) — don't assume it's empty; mature themes already have a rich cluster.
- **⚠️ Watch for FRAGMENTED HUBS — the #1 finding of a theme run.** A long-lived theme often grew **2–3 rival hub/MOC notes** that don't cross-link (e.g. a personal-POV concept + an import-corpus MOC + a thematic MOC). Pick ONE umbrella hub (usually the `90_MOCs/` one), wire the others up to it, and roster the sub-concepts under it. This consolidation is the highest-value edit — bigger than any single link.
- **Don't re-link an already-dense sub-cluster** (siblings already cross-linked) — only its membership in the umbrella + auto-backlinks. Avoids overlinking.
- **The recurring signature to hunt FIRST: THREE LEGS of fragmentation that don't cross-link.** Confirmed 5× (archaeology · health · PhD · dedup · father). The three legs of any personal-domain cluster:
  1. **Import-corpus MOC** — holds the operator's OWN raw data (TG export, email archive) e.g. `_Health-MOC`, `_Perepiska-s-Ottsom-MOC`
  2. **Thematic `90_MOCs/` MOC** — holds external/field knowledge, parent `MOC-index` e.g. `MOC-Biohacking-Longevity`, `MOC-Family-Life`
  3. **Identity-layer `_Self-Bible-MOC`** — holds the "this is who I am" view (cofounder of digital twin) e.g. PhD-as-scholar, family-as-influence
- A long-lived theme typically has the body of one leg but is **invisible from the others**. The highest-value Mode C move = wire all three together (+ make sure root `MOC-index` lists the import-corpus too, not just the thematic).
- Don't re-link an already-dense intra-cluster (overlinking guard).
- Proven runs:
  - 2026-06-14 (archaeology/alt-history): 3 fragmented hubs unified, research-swarm argument map woven into the concept layer — 7 notes / ~30 typed links / 0 new broken.
  - 2026-06-16 (health): personal `_Health-MOC` (830 notes) was orphaned from thematic `MOC-Biohacking-Longevity` + `MOC-index` — bridged both ways, 6 personal concepts rostered, 5 concepts up-linked — 8 notes / ~16 typed links / 0 new broken.
  - 2026-06-20 (PhD): minor — utility morning consolidation had already done ~90%; only 3 hub edits needed (`MOC-index` + cross-domain bridges to crypto/AI) — 3 notes / ~3 links / 0 broken. **Lesson: always verify-existing first; PhD was already 90% done.**
  - 2026-06-20 (a close family member): all three legs missing in the integration — created a **person-card** `person-<name>` + **`MOC-Family-Life`** (closed long-standing TODO in `MOC-index`) + identity link in `_Self-Bible-MOC` (father = "identity-brick of the twin"). 5 notes / ~12 typed links / 0 broken.

## Safety (hard gates)
- Bidirectional = WRITING into old notes → **backup before, preview before, never auto-write** without the operator's OK.
- Never delete; never blanket-glob; never pattern-touch `concept-*`/`person-*` ([[operating-agreement]], [[vault-conventions]]).
- New concepts: create per concept-creation-rules (no-ask per §1); the LINK plan into old notes is shown for approval.

## Rejected complications (don't re-pitch — see [[relink-mechanism]] / [[declined-decisions]])
The DR suggested, and we declined for AK-47: a Local REST API + MCP plugin (Edit targets sections fine), a new vector DB (have e5+reranker), spaCy 3-layer NER (LLM+namesearch suffice), a JSON-schema validation runtime, and a full link-adjacency graph engine (hub counts are enough for v1).

## See also
- [concept-creation-rules.md]($OBSIDIAN_VAULT/08-Templates/concept-creation-rules.md) §1 (when) + §11 (integration) — the canon.
- skill `ask` (RAG engine), `dedup` (dupes), `obsidian-ingest` (first-time save of a raw dump), `obsidian-backup` (backup runbook).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
