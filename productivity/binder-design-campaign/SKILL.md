---
name: binder-design-campaign
description: >-
  Plan and run a protein design campaign within a user-approved stage and
  resource boundary. Branches: de novo binder design (epitope
  choice, generation, co-folding ensemble ranking, ranked order sheet);
  structure and complex prediction with calibrated confidence; protein
  engineering (stability, enzyme, interface). Fires on designing binders or
  miniproteins, picking an epitope or hotspots, running RFdiffusion, BindCraft,
  BoltzGen, ProteinMPNN, ESMFold2 or Protenix, computing ipSAE or DockQ,
  ranking designs to order, auditing such a campaign, or 蛋白结合子设计,
  表位选择, 结构预测.
license: MIT
---

# Protein design campaign

Three branches, one core. First turn the user's goal into a reviewable campaign
plan; after the user chooses how far to execute, the evidence rules and
deliverable discipline below hold for all three branches.

| Branch | Read | For |
|---|---|---|
| binder design | `workflows/binder-design.md` | miniprotein binders against a protein target |
| structure prediction | `workflows/structure-prediction.md` | folds or complexes with calibrated confidence |
| protein engineering | `workflows/protein-design-general.md` | stability, enzyme, interface, scaffold redesign |

Provenance and rationale: `docs/` and `NOTICE.md`, relative to this skill.

## Non-negotiables

These hold at every depth, including inside sub-agents, and bind hardest on the
steps nobody is watching.

1. **State only what you established.** Every claim in a report, update or
   manifest traces to an executed computation or a saved artifact you can point
   at. *Verified* means you ran the check and hold its output.
2. **Every external identifier is fetched.** DOIs, PMIDs, PDB IDs, UniProt
   accessions, residue ranges and URLs in any deliverable are the literal output
   of a lookup executed in this session.
3. **Anomalies are bugs until investigated.** A score of exactly zero, a gate
   that passes everything, a gate that fails everything, a constant metric, a
   perfect metric, an impossible runtime, zero variance across seeds: halt that
   stage, diagnose, then proceed.
4. **Cheapest falsifying check first.** Run the seconds-scale check that could
   kill a plan before committing hours of GPU to it.
5. **Lead with the unfavourable reading.** Headline the worst defensible
   interpretation of your own data. Disclose deviations from the stated method,
   and name analyses tuned after seeing results along with how many
   configurations you tried. Report inconclusive results as inconclusive.
6. **The instrument is a filter, never an oracle.** In silico confidence ranks
   designs *within* a target. It does not tell you whether a target will work,
   and it relates only weakly to affinity — measured, not assumed
   (`references/failure-modes.md` §1). Every summary you write says so.
7. **Verify inherited inputs.** Check target structures, construct definitions
   and hotspot numbering against their primary source before building on them.
8. **Scope.** This protocol is in silico and it **ends at the design sheet**.
   Validation is in vitro, by the user or a CRO; analysing returned assay data
   is a different task and does not run under these gates. Results from an
   earlier round enter here as operator input at G0, never as something this
   protocol goes and fetches. Work on select agents or toxins, and enhancement
   of pathogen function, is out of scope: stop and say so. See
   `docs/responsible-use.md`.

## Plan, authorization and checkpoints

Read `references/campaign-planning.md` before G0. Research what can be found
independently, then ask the user for the remaining outcome, constraint and
resource boundaries in one concise round. Create `state/campaign_plan.md` from
`templates/campaign_plan.md`. It states the stage sequence, evidence needed at
each checkpoint, expected outputs, estimated compute, unresolved assumptions,
and actions needing separate permission. **G0 is the one required review:** do
not start execution until the user approves the plan and selects an
`authorized_through_stage` from 0 to 10. A value of 0 means plan only; 10
authorizes the in-silico campaign through delivery. Record that decision in
`state/decisions.jsonl` and `state/authorization.json`.

G1–G6 are scientific and artifact checkpoints. At each, read the corresponding
section of `checklists/gate-checklists.md`, save its evidence and decision, and
continue when the approved stage limit covers the next stage. The agent makes
in-scope scientific choices from sourced evidence; the user may require a
review stop at any checkpoint or override a choice. A checkpoint never serves
as a request for an unqualified user to certify a protein-engineering claim.
Stop and return a reviewable result when the approved stage limit is reached,
when a material premise changes, or when an action needs resources or external
permission outside the approved plan. Do not silently widen the scope.

| Checkpoint | Records | Stage reached |
|---|---|---|
| G0 | user-approved plan, execution limit, resources and permissions | 0 |
| G1 | assay construct, reference structure, cofactors | 2 |
| G2 | epitope and hotspot residues | 3 |
| G3 | scoring evidence level and frozen instrument | 4 |
| G4 | compute allocation per target | 5 |
| G5 | the ranked set proposed for testing | 9 |
| G6 | acceptance checks against delivered artifacts | 10 |

Two carry most of the risk:

- **G2 decides most of the outcome.** Epitope choice dominates model choice.
- **G3 is mechanical.** Production jobs require a validated gate file. A
  fold-only gate is visibly weaker than positive-control separation and requires
  explicit inclusion in the approved plan; `scripts/preflight.py` refuses it
  otherwise. A stated belief that the instrument works is not evidence.

Checkpoints also re-open **mid-run**. Changing the assay
construct, a catalytic or otherwise load-bearing residue, the off-target
definition, or the endpoint the campaign is aimed at changes the scientific
question — so return to the checkpoint that owns it and obtain approval for
the revised plan when the change affects the user's goal, resource ceiling,
external actions or authorized stage limit.

**Completion bar for an authorized segment:** every stage through its approved
limit has saved artifacts and checks; G6 completion requires the full campaign
artifacts. The user's G0 authorization and any later amendments are recorded in
`state/decisions.jsonl`. Agent scientific decisions are recorded separately as
agent decisions with their evidence.

## Between gates

You work on your own here, subject to five standing obligations.

- **Ledger before narrative.** Every job appends one row to the JSONL ledger
  (`scripts/ledger.py`). Every count you state anywhere is an aggregation over
  that ledger computed at report time.
- **Nothing is discarded.** If it was computed, it is saved: the exact config
  that produced it (model, version, weights checksum, environment id, command
  line, contig or epitope spec, seeds, input paths), every structure file, every
  metric at the level it was computed, the run manifest, stdout and stderr.
- **Canary before fan-out.** Any fan-out past roughly 10 jobs follows one canary
  from the same spec, confirmed past startup with sane output.
- **Progress, not liveness.** A job alive and producing nothing is a failure in
  progress. Gate completion on output counts and explicit markers.
- **Surface a blocker when it blocks**, not at the next gate.

## Campaign spine

```
G0 approved plan -> setup + tool bring-up -> G1 dossier -> G2 epitope
   -> G3 instrument validation -> G4 scale -> generate & screen
   -> optimisation -> final-tier scoring -> G5 selection -> G6 delivery
```

Bring-up runs before G1 because it is slow and its outcome constrains what you
can honestly promise at G2 and G4. A tool joins the **roster** only after
running end to end on a real campaign target, in the environment and flags
production will use, with its output consumed by the next stage — the handoff,
not the tool alone (`references/tool-catalog.md` §1).

## Sub-agents

Where the runtime offers parallel sub-tasks, split by (target x stage) or
(target x model); each brief inherits the non-negotiables and owns only its
scope. Where it does not, run the same decomposition serially and say so — the
protocol depends on the decomposition, not on the parallelism.

Adversarial review is part of the protocol. Before G6, one reviewer re-derives a
sample of scores from raw inputs, and one forms its verdict from raw data
without reading your conclusions. Every finding ships with the query or script
that produced its numbers.

## Reference index

| File | Read it |
|---|---|
| `references/campaign-planning.md` | before G0, and when the authorized stage or scope changes |
| `checklists/gate-checklists.md` | at every gate — G0 also sets the scale preset |
| `templates/campaign_plan.md` | write the staged plan for user review at G0 |
| `references/target-dossier-guide.md` | building the dossier, before G1 |
| `references/failure-modes.md` | before G2, before G5, and whenever a result looks too good |
| `references/validation-gates.md` | at G3, or when a control fails |
| `references/scoring-instrument.md` | defining, running or changing the score |
| `templates/scoring_policy.yaml` | the ranking formula itself — frozen at G3, and the only place it is written |
| `references/thresholds.md` | choosing absolute cutoffs, or diagnosing a low pass rate |
| `references/tool-catalog.md` | choosing, sizing, installing or dropping a tool |
| `references/compute-backends.md` | wiring the scheduler, at G0 |
| `references/deliverables-spec.md` | building any deliverable |
| `templates/` | starting a dossier, config, sheet schema or report |
| `scripts/` | before G5, and against the as-shipped artifacts before G6 |

Tool names, flags, weight URLs and licence facts here were correct at their
recorded date and are re-verified against the upstream README, model card or
paper before use; upstream wins, and the discrepancy goes in the campaign log.
