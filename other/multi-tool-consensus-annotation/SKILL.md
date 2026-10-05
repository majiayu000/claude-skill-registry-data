---
name: multi-tool-consensus-annotation
description: "Runs a PANEL of independent cell-type voters (markers, atlas transfer, scANVI/scArches, popV, treeArches novelty, Census scVI-KNN), reconciled into one label space by a conservative, flag-heavy consensus (confidence, basis_of_label, novelty_flag per cell). Use when no single method's confidence suffices. For single-method transfer use scvi-scanvi."
license: MIT
---

# Multi-Tool Consensus Annotation

A framework for cell-type / cell-state annotation as a **panel of independent voters**. Each voter
answers the annotation question with a different method and a different evidence base; a conservative,
flag-heavy consensus reconciles their per-cell votes into one defensible label set. The design goal:
no single method is the oracle, genuine cross-method corroboration raises confidence, and any
disagreement or out-of-distribution signal is preserved rather than forced into a coarse label.

This skill is the **index** that composes the per-tool voter skills. Route to each voter's own skill
for its implementation; use this skill to decide which voters to run, how to harmonize their
vocabularies, how to read their agreement honestly, and how to fuse them into a frozen label set.

## When this framework fits

- You have (or are building) an annotation pipeline where several methods each produce a per-cell
  label and you need one reconciled answer with a confidence you can defend.
- Your cohort has aging / treatment-remodeled states, so you need a novelty guard that can say
  "known lineage, novel state" instead of snapping every cell to a young/control label.
- Votes in different nomenclatures "never agree" and your agreement threshold is unreachable — the
  vocabulary dead-tally symptom (see Stage 1).
- You want to read an agreement matrix without being fooled by legs that are correlated by
  construction (see Stage 2).

---

## The voter panel

Each voter contributes **one per-cell vote**. Voters differ in evidence base and in how independent
they are from each other — the independence class matters when you count agreement (Stage 2).

| Voter | Question it answers | Per-tool skill | Independence class |
|---|---|---|---|
| **Broad-marker consensus** | Which coarse lineage, by canonical markers? | `scanpy` (`score_genes` / `rank_genes_groups`) | coarse anchor (not a fine vote) |
| **Cluster-level reference voting** | Which public-atlas label does this cluster match (KNN over per-atlas scVI latents)? | `scvi-basic` + `scvi-scarches-reference-mapping` | reference-seed (feeds the internal legs) |
| **Public-atlas scANVI / scArches transfer** | What public type is this, in the atlas nomenclature (whole data as pure query onto a frozen atlas)? | `scvi-scarches-reference-mapping`, `scvi-scanvi` | **independent** corroborator |
| **Internal control→treatment scANVI** | Which control-defined state does treatment remodel? | `scvi-scanvi` | correlated with the reference-seed |
| **popV ensemble** | What do many classifiers (KNN-on-scVI, SCANVI, SVM, RF, …) agree on? | (popV package; see `scvi-framework` for scvi-tools setup) | **independent** corroborator |
| **treeArches / scHPL open-set novelty** | Does this cell fit ANY known type, or is it out-of-distribution? | `treearches-hierarchy-learning` | authoritative OOD guard |
| **CELLxGENE Census scVI-KNN** | What does a large public atlas call this, via a projected KNN vote? | `cellxgene-census-annotation` | **supplementary** (bounded tie-breaker) |
| **Tissue-specific expert dictionary** | For a known compartment (e.g. immune), which curated fine state? | curated marker dictionary via `scanpy` | domain prior (compartment-scoped) |

Modality variants: for scATAC queries the reference-transfer voter is `scembed-atac-annotation`
(region2vec + KNN); for a reference-free marker-only panel of LLMs, `mllmcelltype-consensus-annotation`
is a self-contained alternative voter. A semi-supervised transfer voter fits when a good reference
exists; an ensemble (popV) adds robustness; the novelty guard (treeArches) earns its place whenever
aging or treatment can produce states absent from every reference.

---

## Stage 1 — Harmonize vocabularies FIRST (a separate concern)

Every voter speaks its own native vocabulary: LungMAP `celltype_level3`, a popV panel's
`ref_cell_type`, CELLxGENE-ontology names ("classical monocyte", "CD8-positive, alpha-beta T cell"),
an internal marker dictionary's underscore labels. Before any tally, map **every** voter's label into
**one canonical label space** through crosswalk adapters. This is a distinct stage, kept out of the
fusion logic so the fusion stays vocabulary-agnostic.

**Why it is load-bearing — the dead-tally bug.** If two legs sit in different nomenclatures, their
labels never string-match, so they never agree, so an N-of-legs agreement threshold is unreachable
and the fine-type tally is silently dead. The fix is a `label_synonyms` map
`{ normalize(native_label) → canonical_label }` built from a crosswalk table (never an empty map),
applied to each leg before counting. Already-canonical legs (e.g. a popV panel harmonized at its
source) map to themselves; native-vocabulary legs (atlas transfer, Census) canonicalize here. Tokens
with no crosswalk row (`Unknown`, `Novel`, coarse lineages, treeArches `Rejected`) pass through
unchanged, so disagreement is preserved, never coerced.

**Guard it.** After canonicalization, assert that the genuinely reference-independent legs land in the
same label space as the seed leg on a non-trivial fraction of confidently-labeled cells; a ~0% match
signals the crosswalk failed to bridge vocabularies and the tally is dead.

**Census is the worked example.** `cellxgene-census-annotation` emits CELLxGENE-ontology names; its
crosswalk-to-canonical is a normalization adapter that is its own step. Treat each voter's vocabulary
map the same way — an adapter in front of the tally, not logic inside it.

---

## Stage 2 — Vote independence & reading the agreement matrix

An "N legs agree" claim only means something if the N legs are **genuinely independent**. Two
correlation traps recur:

**1. Legs correlated by construction.** A single evidence chain can wear several hats. In the
implemented lung recipe: the cluster-level **reference vote seeds** the internal scANVI's
`scanvi_seed_label`, which trains both the internal scANVI classifier **and** the treeArches tree —
so `reference_vote → scanvi_seed → {scanvi_pred, treearches_pred}` is one chain producing three
votes. Their mutual agreement is partly tautological. The legs that add genuinely
reference-independent corroboration are the **public-atlas scArches transfer** (whole data as pure
query onto a frozen atlas) and the **popV ensemble** (independent panel). When you read an agreement
matrix, the cells to watch are the independent-vs-correlated blocks: agreement inside the correlated
trio is expected; agreement between an independent leg and the trio is the signal.

**2. Atlas-witness double-counting.** Several methods can hit the **same** reference atlas — e.g. a
per-atlas reference vote, a Seurat transfer, and an scANVI transfer all onto LungMAP CellRef. That is
one atlas witnessed three ways, not three independent corroborators. Group such witnesses
(`atlas_witness_groups: { lungmap: [...] }`) so the group contributes ~1 (not 3) to a corroboration
count, and keep both the raw pairwise matrix and the down-weighted summary. A single-atlas-support
guard can additionally downgrade a high call to medium (and flag
`uncertain_reference_disagreement`) when its only corroboration is one atlas's witnesses with no
independent popV / scANVI backing.

Record this correlation structure in a provenance note (`reasoning-trace`) and surface it beside the
agreement matrix, so a reader interprets the matrix with the independence map in hand.

---

## Stage 3 — The conservative fusion policy (the output contract)

The consensus emits, per cell, a small fixed vocabulary the whole project (and any cross-dataset
integration) can join on:

- `annotation_confidence ∈ {high, medium, uncertain}`
- `basis_of_label ∈ {PI_curated, reference_transfer, de_novo, consensus}`
- `novelty_flag ∈ {none, uncertain_low_quality, uncertain_reference_disagreement,
  known_lineage_unknown_state, old_enriched_candidate_state, treatment_enriched_candidate_state,
  possible_doublet, possible_ambient}`
- plus the frozen `consensus_cell_type` / `consensus_cell_state`, a continuous `consensus_entropy`,
  and the raw fine-leg agreement count `n_legs_agree`.

**Evaluate the rules in order** — the ordering encodes the conservatism:

1. **Curated anchors first.** A cell whose cluster carries a PI-curated control label keeps it at
   `high`, `basis_of_label = PI_curated`. Human-curated anchors are authoritative and never
   overwritten.
2. **treeArches-authoritative OOD → Novel.** A treeArches distance/RE rejection routes the cell to a
   de-novo state: `consensus_cell_state = Novel_<subcluster>`, `consensus_cell_type` = its coarse
   lineage, `basis_of_label = de_novo`, and a condition-routed `novelty_flag`
   (`old_enriched_candidate_state` for aged controls, `treatment_enriched_candidate_state` for
   treatment arms, else `known_lineage_unknown_state`). Closed-simplex signals (an atlas-transfer
   "novel" flag, scANVI uncertainty) **reinforce** this routing but do not trigger it — treeArches is
   the authoritative OOD guard because its distance/RE rejection is threshold-invariant geometry, not
   a tunable softmax.
3. **Ambiguity → Uncertain.** A treeArches root-ambiguous call, or scANVI uncertainty with no
   fine-leg majority, resolves to the coarse lineage (or `Uncertain`) at `annotation_confidence =
   uncertain`, `basis_of_label = consensus`, `novelty_flag = uncertain_reference_disagreement`.
4. **N legs agree → high / medium.** When at least `min_legs_agree` fine-type legs share the modal
   canonical label, that label is frozen at `basis_of_label = consensus`. It reaches `high` only when
   an independent robustness signal concurs — gate on the ensemble's own confidence
   (`popv_confidence == "high"`, which already folds any method-count rescale) **and** the internal
   scANVI's calibrated probability clearing its threshold — otherwise `medium`. The single-atlas guard
   (Stage 2) downgrades `high → medium` when the corroboration is one atlas's witnesses alone.
5. **Weak majority → medium.** Exactly two fine legs agreeing is a weak majority: take the label at
   `medium`, `basis_of_label = reference_transfer`, `novelty_flag = uncertain_reference_disagreement`.
6. **Split with no majority → supplementary tie-break, else Uncertain.** On a tie, the **supplementary
   Census vote** (or another bounded corroborator) breaks it toward the label it supports at `medium`,
   `basis_of_label = reference_transfer`. With no supplementary vote, keep the coarse lineage and set
   the state to `Uncertain`. The supplementary vote never elevates a call to `high`, never stands as
   the sole leg, and is ignored when it reads `not_run`.

**Supplementary vs load-bearing.** Load-bearing legs (markers, reference vote, the two scArches
transfers, popV, treeArches) can carry a majority. The Census leg is **supplementary**: a bounded
tie-breaker / corroborator only, ignored when `not_run`. Keep that boundary explicit — a supplementary
leg must never be a cell's sole label source.

**Flag-heavy by design.** When in doubt, flag or reject rather than force a label. A high-confidence
call may not carry a disagreement flag (enforce the invariant: `high ⟹ novelty_flag == none`), and
quality seeds from QC (`uncertain_low_quality`, `possible_doublet`, `possible_ambient`) overlay onto
otherwise-unflagged cells. The flagged fraction (Novel + Uncertain), stratified by condition, is a
readout in its own right — a treatment-arm spike surfaces candidate remodeling.

---

## Composition & sequencing

A workable order for a fresh dataset:

1. **Broad lineages by marker consensus** (`scanpy`) — the coarse anchor; do not force fine labels yet.
2. **Cluster-level reference votes** across public atlases (`scvi-scarches-reference-mapping`) — the
   seed the internal legs build on.
3. **Public-atlas scANVI/scArches transfer** (`scvi-scanvi`, `scvi-scarches-reference-mapping`) — the
   independent public-nomenclature vote; keep `Unknown` a valid outcome.
4. **Internal control→treatment scANVI** (`scvi-scanvi`) — anchored on high-confidence controls,
   treatment arms as query.
5. **popV ensemble** — robustness across many classifiers; the second independent corroborator.
6. **treeArches / scHPL** (`treearches-hierarchy-learning`) — the open-set novelty guard.
7. **Census scVI-KNN** (`cellxgene-census-annotation`) — the supplementary bounded vote.
8. **Harmonize all vocabularies** (Stage 1) → **fuse** (Stage 3) → freeze the label set → emit the
   agreement matrix + flagged-fraction tables (Stage 2) and persist the policy via `reasoning-trace`.

For an immune compartment, add a curated tissue-specific dictionary as a compartment-scoped fine leg
alongside the public references. Reserve embeddings for geometry, QC, annotation, and discovery;
leave the embedding for the measurement layer (pseudobulk DE, differential abundance) once labels are
frozen.

---

## Frozen `.obs` contract (what downstream consumes)

```text
consensus_cell_type        # frozen canonical fine/coarse type
consensus_cell_state       # fine state or Novel_<subcluster>
annotation_confidence      # high | medium | uncertain
basis_of_label             # PI_curated | reference_transfer | de_novo | consensus
novelty_flag               # none | uncertain_* | *_candidate_state | possible_doublet | possible_ambient
consensus_entropy          # continuous uncertainty (from the internal scANVI leg)
n_legs_agree               # raw count of fine-type legs sharing the modal canonical label
# every per-leg vote rides forward for audit (reference vote, atlas transfer, scANVI, popV,
# treeArches, census_label, ...)
```

Freeze once; do not recluster or rename after the freeze. `annotation_confidence` and
`basis_of_label` are the umbrella-harmonized axis that cross-dataset integration joins on;
`novelty_flag` is dataset-local and maps to an integration-level `uncertainty_reason` at the boundary.

---

## Resources

- The conservative multi-leg policy and the leg-independence caveat are the recurring pattern behind
  the per-tool voter skills above; this skill is the framework that composes them.

---

## When not to use

- Do not use for a reference-free multi-LLM consensus over marker genes. Use mllmcelltype-consensus-annotation.
- Do not use to run a single annotation method. Route to that method's own skill (scvi-scanvi, treearches-hierarchy-learning, cellxgene-census-annotation, ...); this skill is the framework that composes several.
- Do not treat the consensus as a way to manufacture agreement — its job is to preserve disagreement as Uncertain/Novel, not to coerce a label.

---

## See also

- `scvi-scanvi` — Voter; scANVI semi-supervised label transfer from seed cell-type labels (public or internal reference), always initialized from a trained scVI model
- `scvi-scarches-reference-mapping` — Voter; scArches surgery to project a query onto a frozen atlas
- `treearches-hierarchy-learning` — Voter (authoritative OOD); open-set novelty / OOD rejection guard
- `cellxgene-census-annotation` — Voter (supplementary); pulls a CELLxGENE Census reference slice and takes a local KNN vote in its scVI embedding, without the tiledb stack
- `scembed-atac-annotation` — Voter (ATAC modality); region2vec KNN vote against a pre-trained HuggingFace databio reference, no retraining
- `mllmcelltype-consensus-annotation` — Alternative voter / self-contained panel; reference-free multi-LLM marker consensus
- `scanpy` — Prerequisite (markers + coarse anchor); marker scoring, clustering, `rank_genes_groups`
- `reasoning-trace` — Provenance; persist the fusion policy + correlation structure
