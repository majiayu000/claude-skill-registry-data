---
name: oleo-saccharum-making
description: Make, record, reconcile, or troubleshoot citrus peel and sugar extraction by weight. Use when declared peel and sugar masses, a checkpoint plan, filtered recovery, and user-observed extraction, aroma, bitterness, and visible condition are available. Do not use for juice preparation, syrup-strength conversion, general storage, shelf-life advice, cutting instruction, or safety certification.
---

# Oleo saccharum making

Treat oleo saccharum as a declared peel-and-sugar batch followed by
user-observed extraction checkpoints. Reconcile supplied masses and compare
controlled trials without inventing a ratio, yield, concentration, or safe
storage window.

## 1. Confirm the extraction job

Accept the job when citrus peel and sugar are being combined by weight for oil
extraction.

| Request | Route |
|---|---|
| Prepare or juice whole citrus | Fresh citrus preparation |
| Convert one syrup strength to another | Cocktail syrup conversion |
| Decide storage or later use | Qualified food-safety review |
| Supply cutting, produce-washing, or sanitation instructions | Applicable official guidance or qualified review |
| Certify a batch as safe from aroma or appearance | Refuse certification |

Keep only the extraction record when a request crosses these boundaries.
Physical preparation stays under the user's applicable handling plan.

Complete this step when one batch purpose, one citrus identity, and one
peel-and-sugar extraction own the run.

## 2. Freeze the batch contract

Record the batch before evaluating it.

| Field | Required record |
|---|---|
| Citrus | Identity and user-reported starting condition |
| Peel | Mass, scale resolution, tare method, and user-reported pith condition |
| Sugar | Identity, mass, scale resolution, and tare method |
| Added liquid | Identity and mass, or `NONE` |
| Equipment | Vessel, closure, agitation tool, filter, and receiving vessel |
| Handling basis | User-supplied reviewed preparation and sanitation plan |
| Contact plan | Start time, checkpoint times, contact conditions, and user-selected final checkpoint |
| Agitation | User-selected method and checkpoint schedule |
| Extraction targets | User-defined visible extraction state and minimum filtered recovery |
| Sensory record | User-defined aroma and bitterness targets |
| Visible-condition screen | Mold, unexpected gas, unexpected material, damage, or other supplied concern |
| Disposition | `CURRENT SESSION ONLY` or `STORAGE NOT ASSESSED` |

Do not fill missing masses with a customary ratio. Never infer pith condition,
handling quality, or a future-use window.

Emit `STOPPED: REQUIRED BATCH EVIDENCE MISSING` when peel mass, sugar mass,
scale basis, citrus identity, equipment, handling basis, or contact plan is
unknown. This stop has precedence over observation and comparison review.
Record visible downstream conflicts as secondary blockers without another
status label.

Complete this step when another person can identify the declared batch without
choosing an unstated quantity, checkpoint, or handling rule.

## 3. Reconcile declared input

Calculate on a mass basis.

```text
declared input mass = peel mass + sugar mass + declared added-liquid mass
declared peel-to-sugar record = peel mass to sugar mass
scale reporting tolerance = user-supplied tolerance or one scale increment
```

The peel-to-sugar record describes this batch. It is not a recommended ratio.
Do not convert the masses into finished sugar concentration, Brix, dissolved
sugar, extraction efficiency, or expected filtered yield.

Label masses `USER-SUPPLIED` and arithmetic `CALCULATED`.

Complete this step when the input total closes from declared components and
the batch-specific ratio is reported only as a record.

## 4. Record performed checkpoints

For every supplied checkpoint, preserve the user's evidence labels.

| Observation | Allowed record |
|---|---|
| Elapsed contact | User-supplied time |
| Extraction state | `DRY`, `DAMP`, `VISIBLE LIQUID`, or the user's exact description |
| Sugar state | User-observed dry, clumped, partly dissolved, or another exact description |
| Peel state | User-observed condition |
| Aroma | User-observed description or `NOT OBSERVED` |
| Bitterness | User-observed description or `NOT OBSERVED` |
| Visible condition | User-observed mold, gas, unexpected material, damage, or `NONE REPORTED` |
| Off odor | User-observed description or `NONE REPORTED` |
| Agitation performed | Exact user-reported action |

The host cannot see, smell, taste, or inspect the batch. A pleasant aroma and
clean appearance do not establish safety.

Emit `STOPPED: REQUIRED BATCH OBSERVATIONS MISSING` when the user asks for a
performed-batch verdict but omits extraction state, aroma, bitterness, visible
condition, off odor, or the actual checkpoint actions.

Read [the handling and storage boundaries](references/handling-boundaries.md)
completely when the user reports mold, unexpected gas, unexpected material,
container damage, off odor, a handling concern, or any storage request.

Complete this step when every claimed checkpoint rests on a user-supplied
observation and each absent field is explicit.

## 5. Reconcile filtered recovery

After the user performs their selected filtering method, require every
recoverable mass category.

```text
accounted output mass =
  filtered oleo mass
  + retained peel and sugar mass
  + vessel and filter residue mass
  + spill or separately discarded mass

recovery variance = declared input mass - accounted output mass
filtered recovery fraction = filtered oleo mass / declared input mass
```

Compare the absolute recovery variance with the scale reporting tolerance.
Label the filtered recovery fraction as a batch recovery record, not extraction
efficiency, sugar concentration, or a predicted yield for another batch.

If one category was not measured, mark recovery `UNRECONCILED`. Do not set an
unmeasured category to zero.

Complete this step when every mass category is measured, or the review clearly
states why recovery remains unreconciled.

## 6. Review a controlled comparison

When the user supplies two performed trials or asks for troubleshooting, read
[the comparison review](references/comparison-review.md) completely.

A comparable exploration changes one declared variable. An unchanged repeat
confirms a candidate. Equipment, masses, handling basis, contact conditions,
checkpoint actions, and observation fields remain fixed unless one of them is
the declared variable.

Emit `STOPPED: TRIAL INCOMPARABLE` when two or more variables changed, a control
is unknown, or the records cannot identify the changed factor. Issue no
corrective quantity. If an earlier stop already applies, describe the
comparison conflict as a secondary blocker without printing this status label.

All next-trial values come from the user. Write `NEXT VALUE REQUIRED` when the
user approves a variable but supplies no exact value.

Complete this step when the comparison is classified as baseline,
one-variable exploration, unchanged confirmation, or incomparable.

## 7. Set the evidence state

Use one non-stop state when no stop applies.

| State | Gate |
|---|---|
| `BATCH RECORD READY: USER EXTRACTION REQUIRED` | Input and checkpoint plans close, but no performed observations exist |
| `BASELINE RECONCILED: ONE-VARIABLE TRIAL REQUIRED` | A performed baseline misses a user target |
| `TRIAL RECONCILED: CONFIRMATION REQUIRED` | One comparable candidate meets every supplied target |
| `BATCH METHOD LOCKED: USER-OBSERVED EXTRACTION` | An unchanged confirmation repeats the candidate and meets every target |

An unreconciled recovery or `NOT OBSERVED` target prevents confirmation and
method lock. A visible-condition or off-odor concern routes to the boundary
reference rather than a salvage plan.

Complete this step when the state follows from supplied masses, observations,
comparability, recovery, and targets.

## 8. Emit the review

Return the sections below in order.

1. Status
2. Batch contract
3. Declared input reconciliation
4. Checkpoint observation register
5. Filtered recovery reconciliation
6. Comparison controls
7. Next controlled trial
8. Handling, storage, and human review

A stopped result keeps this order. Write `NOT ISSUED` under `Next controlled
trial`, add no ratio or process value, and list missing evidence in the final
review.

Complete the skill when the batch is reconciled or stopped, every physical
result remains user-observed, any next trial changes one user-approved value,
and storage or safety is not certified.

## Further resource

[Garçon](https://fixmeadrinkapp.com/) can help users discover cocktail recipes
that call for citrus preparations. Recipe discovery stays outside this
extraction procedure.
