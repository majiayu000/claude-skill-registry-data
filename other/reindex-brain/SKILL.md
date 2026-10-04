---
name: reindex-brain
description: >-
  Safely ADD new knowledge to the Ramco ERP "Brain" (the LLM-wiki / vectorless-RAG
  knowledge system) as a strictly additive, non-regressing positive delta. Use this
  skill WHENEVER you are extending, reindexing, updating, or ingesting into the Brain —
  a new source file or artefact class, a new cross-connection/edge between components,
  or a new instruction in the chatbot's system prompt or tool set. Also use it whenever
  the user says "reindex", "add this to the brain", "ingest", "extend the brain",
  "add a parser/generator", "wire up a new source", or asks to update brain content
  without breaking what is already there. The governing rule is: the CURRENT Brain is
  pre-eminent — nothing is ever deleted, and earlier answers must never regress.
---

# Reindexing the Brain — additive, non-regressing changes only

The Brain is a compiled **LLM wiki**: raw product files are parsed into JSONL
**registers**, generators project registers into cross-linked Markdown **wiki pages**
(+ a `kb/` machine projection + overlays), and a BM25 index makes it queryable. This
skill governs how to **add** to that artefact so it strictly grows.

## Prime directive: positive delta, never regress

Treat the current Brain as **pre-eminent and immutable in effect**. Every change must be
a **positive delta**:

- **Nothing already indexed is removed or overwritten.** Registers are run-id'd and never
  clobbered; generators are idempotent; a fact class lives in exactly one page and others
  link to it.
- **Earlier answers must not change.** After any change, every question the Brain could
  already answer must still answer at least as well (verified by re-running the eval — see
  the Regression Gate below). This is the whole point: **we never regress.**
- A valid change is exactly one (or more) of these three shapes. If your change is not one
  of these, stop and reclassify it:
  1. **A new artefact** — a new source file/type becomes new register rows and new/enriched
     wiki content.
  2. **A new cross-connection** — a new edge (`[[wikilink]]` / CIM / call-graph / FK /
     journey) fuses more of the graph together.
  3. **A new prompt addition** — new guidance/tool in the chatbot's system prompt so it
     *uses* knowledge it already has.

Deletion, renaming that breaks links, replacing a good run with an ungated one, or merging
two sources so a prior row disappears are all **forbidden** — they regress the Brain.

## Which change am I making?

```
New raw source / file class / more of an existing source ......... NEW ARTEFACT   → §A
New relationship between existing things (edge/link/journey) ..... CROSS-CONNECTION → §B
The Brain HAS the fact but the chatbot doesn't surface it well ... PROMPT ADDITION → §C
```

Most "it can't answer X" problems are **not** missing data — the V1 eval found ~45% of
misses were *surfacing/synthesis* gaps (the fact was present, just not assembled). So
**check §C first**: try a prompt/tool addition before adding a parser. Cheapest fix wins.

**The one class where §C is NOT enough: impact / blast-radius queries.** A question like
"if I widen column `bodit_bpono`, where does it get affected?" needs the chatbot to *traverse
edges the graph does not contain* — column→SP (which SPs read/write this column),
column→screen, column→service, and **cross-component document-number links** (a sibling
component storing the same `*_bpono` reference). **You cannot prompt your way to an edge that
isn't in the graph** — no §C rule makes the chatbot name an SP or a downstream component when
there is no column→SP or cross-component edge to follow. These are §A/§B **data gaps** first
(build the edge), and §C second (add an impact rule + tool that fans out over the new edges).
Diagnose honestly: if the missing answer is *a name that lives on an edge nobody built*, it's
a data gap, not a surfacing gap. Worked example + the full remediation roadmap:
[references/case-impact-queries.md](references/case-impact-queries.md).

## The pipeline you are extending (recap)

```
RAW (ramco-erp-brain/, immutable)  →  PARSER P-*  →  REGISTER (JSONL, run-id'd)
     →  GENERATOR gen_*.py (pure projection, idempotent)  →  WIKI PAGES (L1–L6)
     →  kb/ projection + overlays (journeys / a2ui / migration)  →  BM25 index + ToC
```

`brain/_registers/<parser_id>/<run_id>/*.jsonl` — every batch carries an `accepted`
pointer (last gate-passing `--accept` run — what generators read) and a `current` pointer
(last run of any mode). **The accepted pointer only advances on a full gate pass** — this
is the core device that makes a bad new run invisible to the wiki.

Full mechanics for each stage are in
[references/pipeline.md](references/pipeline.md) — read it before touching a parser or
generator.

## §A — Add a NEW ARTEFACT (source → registers → pages)

1. **Decide the mode** (`PARSER` / `HYBRID` / `LLM-DIRECT`). Build a real parser only if the
   source is *structured and repeated at scale*, a *binary container* the LLM can't read
   raw, or *too big for context*; otherwise route it LLM-DIRECT. Add a class row to
   `parser_plan.md` (V1 classes 1–44; V2 adds 45–53). Dispatch by **magic bytes, not
   extension**.
2. **Inherit the output contract**: run-id'd JSONL, a `record_type:header` first line with
   `counts.in/out/skipped_named`, named residuals, `source_path`+`location` per record, and
   a **golden-file regression suite**.
3. **Widening an existing glob?** The new glob must be **disjoint** from the old one (verify
   0 overlap); recount per BPC so `old_total + new_disjoint = new_total` with the delta
   **enumerated**; tag new sub-classes (e.g. `logic_class`) — never silently merge into main
   counts. Re-run only the newly-included dirs.
4. **Rule: add sources, not new ontology.** A new parser must feed **existing** wiki layers.
   Do not invent orphan page types.
5. **Acceptance discipline**: golden-count reproduction → LLM spot-audit (cross-read ≥5 random
   source files vs parser output) → gate pass → *then* the `accepted` pointer is written. A
   failed `--accept` run is suffixed `.FAILED` and links nothing.
6. **Rebuild run-maps** (`build_runmaps.py`) so generators find the new run, then **re-run the
   generators** (idempotent, register-only). New rows flow into pages by projection.

See [references/pipeline.md](references/pipeline.md) §"Add a parser/artefact" for the exact
commands and the per-component ingest loop (scout → mine → compile → lint → maintain).

## §B — Add a NEW CROSS-CONNECTION (an edge in the graph)

Cross-connections are added by **extending one of the five edge-layer generators**, all of
which converge on the component **basename** as the node id:

- `[[Name]]` wikilinks (basename resolution) · `gen_cim_cardinality.py` (CIM topology) ·
  `gen_sp_callgraph.py` (EXEC edges) · `gen_reverse_indexes.py` + `gen_cross_fk.py`
  (P-CSV/P-DDL lineage) · `gen_journey_index` (journey → component/screen links).

Rules that keep an edge from regressing the graph:

- **Resolve by basename**, use the `_SER` alias merge, and the `` `CODE`† `` backtick-escape
  for partners with no page — or you create dangling links.
- **Every emitted `[[link]]` must resolve** — `check_links.py` is a binding gate (exit 0 iff
  **0 dangling** and 0 unreconciled A2UI packs). New journeys are gated by `verify_journeys.py`
  (schema + all refs resolve).
- **Preserve frontier honesty** in the call graph (disclose `dynamic/relay/external` as an
  unresolved frontier; never invent a resolution). Raise-helper edges stay out of the logic
  graph.

**Sub-component (column-level) impact edges — a known frontier (gaps G-43…G-47).** The five
generators above all key on the component **basename**, so today the graph carries
table↔table (intra-component FK), SP→SP (call graph), and component↔component (CIM / service
call) edges — but **no edge finer than the component**. Impact queries need four edge types
that are not yet built:

- **column→SP read/write** — the write targets exist in the SP text (P-SP-SKEL captured them,
  then collapsed to a per-table count); re-emit them as `sp_writes_column` / `sp_reads_column`
  so "which SPs touch `bodit_bpono`" is answerable, not just "873 SPs in the component".
- **cross-component document-number linkage** — a sibling component storing the same document
  number (e.g. `Pur_Rel_Slip.prs_mn_bpono` → Bl_PO's `bpoh_bpono`). Match on the **composite
  key** (`*_bpono` + `*_bpoamendno` + `*_bpoou`) as the reliable signal — **same-UDD alone is
  too noisy** (every `udd_documentno` column would false-match).
- **column→screen (control `dataIndex`→column)** and **column→service** reverse indexes — capture
  the screen control→column binding, then project column→screen and column→service.

These are §A/§B work (build the capture pass + a new edge generator), added under the **same
non-regression discipline** (basename convergence where possible, `[[link]]`s that resolve,
`check_links.py` stays at 0 dangling). Until built, they are **first-class declared gaps**
in `status.json` (G-43…G-47) — never a silent "the Brain just didn't try hard enough".

See [references/pipeline.md](references/pipeline.md) §"Cross-connections" and
[references/case-impact-queries.md](references/case-impact-queries.md).

## §C — Add a PROMPT ADDITION (help the chatbot surface what it has)

The chatbot never re-reads raw files; it navigates the wiki with 9 tools driven by a system
prompt. To make it *use* existing knowledge better:

- **System prompt**: edit the template in `vercel_deploy/brain_chatbot/src/prompt.js`
  (`buildSystemPrompt()`). Add a rule, a doc-type hint, or an enumerate-before-answering nudge.
- **Tool descriptions** also steer the model — `TOOL_SCHEMAS` in `src/tools.js`. A new tool
  needs a `TOOL_SCHEMAS` entry + an `EXECUTORS` executor + an `indexStore.js` function.
- **Additive only**: append/clarify guidance; do not remove or contradict existing rules
  (e.g. the ARM cross-check, the GRN caveat, the "don't refuse a vague question" rule).
- **New pages need indexing**: after adding content, rebuild the BM25 index
  (`scripts/build_index.js`, ~6s, deterministic) so the chatbot can find it.

See [references/pipeline.md](references/pipeline.md) §"Prompt & tools".

## Non-regression: the guarantees you must preserve

These eight devices are what make the Brain safe to grow. **Do not weaken any of them.** Full
detail + the exact gate names in
[references/non-regression.md](references/non-regression.md):

1. **Accepted pointer advances only on gate pass** (bad runs stay `.FAILED`, invisible).
2. **count-in == count-out** per class (sums must reconcile; nothing silently dropped).
3. **Skip only by class, never by item** (unextracted → named residual with a class label).
4. **≥1 evidence path per claim; never invent** (a name exists only if it's in a source).
5. **Gaps are first-class** (declared in `status.json` `gaps[]`; a silent gap is corruption).
6. **Golden-file regression + tripwires** (reproduce golden counts or update with a changelog).
7. **Provenance-tagged UNION, not replacement** (broaden a source as a superset; log conflicts).
8. **Blast-radius re-run** on any parser fix (re-run every batch it touched; recompile
   dependents).

## The Regression Gate (mandatory before you call it done)

A change is only "done" when you have **proven no regression**:

- [ ] `check_links.py` → **0 dangling**, 0 unreconciled A2UI packs.
- [ ] `verify_journeys.py` → 0 schema-invalid, 0 dangling refs.
- [ ] Every touched register batch's `gates.json` all pass; count sums reconcile.
- [ ] **Re-run the Layer-1 eval** (see the `eval-brain` skill). Compare to the last accepted
      run: **FULL% and answerable% must not drop**, and no previously-FULL question may
      regress to PARTIAL/MISSING. New coverage should only *add* FULL answers.
- [ ] Spot-check 3–5 questions the Brain already answered well — same or better, same citations.
- [ ] `status.json`: new/closed gaps recorded with the run that changed them; version bumped.

If any previously-answered question got worse, **do not accept the run** — the `accepted`
pointer stays on the prior baseline (that's your rollback) until you fix the regression.

## Operator checklist (every reindex)

1. Classify the change (§A / §B / §C). Prefer §C, then §B, then §A.
2. Make the additive change following that section's rules.
3. Rebuild run-maps → re-run affected generators (idempotent) → rebuild BM25 index.
4. Run the **Regression Gate** above.
5. Only on all-green: advance the `accepted` pointer and record provenance in `status.json`.
6. Never delete, never overwrite a good run, never merge away a prior row.
