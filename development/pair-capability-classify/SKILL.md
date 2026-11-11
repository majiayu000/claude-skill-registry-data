---
name: pair-capability-classify
description: "Builds the classification matrix by applying the quality model (KB default + `tech/risk-matrix.md` adoption delta) — from the story context in refinement, from the code/diff in review (confirm-or-raise, never lower). Emits chromatic tags only when the adoption declares the matrix→tag projection. Composed by /pair-process-refine-story (refinement context) and /pair-process-review (review context); invoke directly to classify a card or PR on demand."
version: 0.2.0
author: Foomakers
---

# /pair-capability-classify — Objective Classification

Compile the classification matrix for a card or PR by **applying the [quality model](../../../.pair/knowledge/guidelines/quality-assurance/quality-model.md)** — never by inventing criteria. The model is the single source of rules (§3 risk dimensions, §3.2 tier = max, §5 tag projection); this skill is the Layer-2 *skill* that runs those rules on demand and produces the artifact (quality-model §1). Downstream consumers (gate, `/pair-process-review`, `/pair-next`, automation) read the resulting matrix and tags **without owning any criteria** (D18).

Two invocation contexts, one model:

- **refinement** — evidence is the **story context** (declared/estimated scope, touched subdomains, cross-context integrations). Shift-left (R1.3): the matrix exists before code does.
- **review** — evidence is the **code/diff** (observed footprint, `/pair-capability-assess-security` verdict, `/pair-capability-assess-coupling` verdict). The review value is a **floor**: it confirms or **raises** the refinement tier, and **never lowers** it (quality-model §3.2, D17).

## Arguments

| Argument   | Required | Description                                                                                                                             |
| ---------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `$context` | No       | `refinement` — classify from the story context. `review` — classify from the diff. Auto-detected: called by `/pair-process-refine-story` → `refinement`; by `/pair-process-review` → `review`; a PR/diff in context → `review`; otherwise → `refinement`. |
| `$target`  | No       | The card/PR to classify (story ID or PR number). Default: the item in context. **The target names the side every write goes to**: a **card ⇒ the PM tool**, a **PR ⇒ the code host** (they are the same tool unless the project declares `code-host` — see the [routing table](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/way-of-working-pm-resolution.md)). |
| `$override`| No       | An explicit tier or dimension override passed by a human (resolution cascade **Argument** layer, quality-model §Resolution order). Raises only — never lowers a review value below the model result. |

## Prerequisite: the quality model

The rules this skill applies live entirely in the [quality model](../../../.pair/knowledge/guidelines/quality-assurance/quality-model.md) (#221) plus its optional adoption delta `tech/risk-matrix.md` (§6). This skill contains **no classification criteria of its own** — it is grep-verifiably a model-applier, not a model-owner.

**No quality model doc installed** ⇒ **HALT** with a pointer to the #221 prerequisite: `classify` cannot apply rules that are not present. This is the one hard stop; every other absence degrades gracefully to a KB default (D21).

## Resolution order

Every rule resolves through the quality model's cascade — **Argument (`$override`) > Adoption (`tech/risk-matrix.md`) > KB default (quality-model.md)**. A malformed adoption file is treated as absent: warn and fall back to KB defaults entirely, including no tag emission (quality-model §6, D21).

## Algorithm

### Step 0: Detect Context

1. **Check**: Is `$context` provided?
2. **Skip**: If provided, use it. Proceed to Step 1.
3. **Act**: Auto-detect — invoked by `/pair-process-refine-story` → `refinement`; by `/pair-process-review`, or with a PR/diff in context → `review`; otherwise → `refinement`.
4. **Verify**: Context is set to exactly one of `refinement` | `review`.

### Step 1: Load the Model

1. **Act**: Read [quality-model.md](../../../.pair/knowledge/guidelines/quality-assurance/quality-model.md). If absent → **HALT** (pointer to #221).
2. **Act**: Read `tech/risk-matrix.md` if present — its up-to-three independent sections (`## Tag Projection`, `## Criticality Table`, `## Overrides`, quality-model §6); the presence of one never implies the others. Absent or malformed ⇒ KB defaults apply completely (D21).
3. **Verify**: The effective rule set is assembled — KB defaults, plus whichever adoption sections parsed cleanly. Adoption absence is logged as "KB defaults" in the output, not treated as a gap.

### Step 2: Gather Evidence

Per `$context`, collect the source for each dimension (quality-model §3.1, "Source" column):

- **refinement** — from the story body: declared scope (change/diff-risk proxy), the subdomain classification of what it touches (business impact), touched-path heuristics (security relevance), and — if `subdomain/`/`boundedcontext/` artifacts exist — the volatility of touched subdomains plus the cross-context integrations the story introduces (coupling balance).
- **review** — from the diff: observed footprint (change/diff risk), the `/pair-capability-assess-security` review verdict (security relevance, quality-model §3.1), and the `/pair-capability-assess-coupling` verdict on the diff (coupling balance). An unreadable diff (huge/binary) falls back to file-path/service-level evidence and flags **low confidence** in the `<details>`.

**Coupling sources absent** (no subdomain/bounded-context artifacts in refinement, `/pair-capability-assess-coupling` not installed in review) ⇒ the coupling dimension is reported **not assessed**, excluded from the tier max, and never blocks (quality-model §3.1, D21).

### Step 3: Compile the Matrix

1. **Act**: Resolve each of the five dimensions (Service/domain criticality, Change/diff risk, Business impact, Security relevance, Coupling balance) to `green`/`yellow`/`red` per quality-model §3.1, applying the resolution cascade (Step 1's effective rule set) to each — e.g. a service listed `High` in the Criticality Table overrides the Medium default (AC5); a service **not** listed in an existing table resolves to conservative High.
2. **Act**: **Risk tier = max(assessed dimensions)** (quality-model §3.2), projected as `risk:green|yellow|red`. Compute the **cost class** independently as the highest detected signal (quality-model §3.3, `cost:green|yellow|orange|red`) — always written to the body, never part of the risk max.
3. **Act** (review only, never-lower): read the refinement-time tier from the story body — **an item read ⇒ `pm-tool`** ([routing table](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/way-of-working-pm-resolution.md)), the opposite side from Step 4's PR write. **When the tools are split, resolve the story's item id from the PR's `Refs:` cross-link line first** (composed from `/pair-process-review` the story is already in session; the standalone `$target: <PR>` path has only the PR, and without the id the refinement floor is unreadable — the never-lower rule would silently degrade to the review value alone, the D17 violation this point exists to prevent). `Refs:` absent on a split project ⇒ report the floor as **unreadable** and keep the review value, flagged, rather than treating it as `green`. The review tier is `max(review-computed, refinement-tier)` per dimension and overall — the review pass may **raise** a dimension (e.g. the diff reveals a schema migration ⇒ `risk:red`) but **never lowers** a value the story's refinement already set (quality-model §3.2, D17). A `$override` may raise further; it never lowers below the model result.
4. **Verify**: Every dimension is `green`/`yellow`/`red`/`not assessed`; the tier equals the max of the assessed dimensions; in review, no dimension is below its refinement value. **Determinism**: the same card/PR under the same model + adoption yields an identical matrix and tier on every run (AC4).

### Step 4: Write the Matrix to the Body (always)

1. **Act**: Render the matrix as **1 line + `<details>`** (D22 reading budget — never an inline table) and write it into the target body's classification section — **card ⇒ the PM tool, PR ⇒ the code host** (routing by target, per the [routing table](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/way-of-working-pm-resolution.md); one tool unless `code-host` is declared). In review context the target is the **PR**, so this is a code-host write. This write happens **regardless of tag projection** — §3.2/§3.3 body output never depends on it.
2. **Verify**: The body carries a 1-line verdict (`risk:<tier>`, plus `cost:<class>` and any not-assessed note) and a collapsed `<details>` with the per-dimension breakdown and confidence.

### Step 5: Tag Projection (adoption-gated)

Tag *emission* is declared, not implicit (quality-model §5) — the matrix in Step 4 stands whether or not any tag is emitted.

1. **Check**: Does `tech/risk-matrix.md` have a `## Tag Projection` section?
2. **Skip**: If yes, use it exactly as written — apply the chromatic tag for each `Active` parameter (`risk:green|yellow|red`; `cost:green|yellow|orange|red` only if `cost` is listed; a renamed label per §5 keeps the same color values) — and **never propose again**. `Active: none` is a durable opt-out: emit no tags, do not ask.
3. **Act**: If no `## Tag Projection` section, **propose only the `risk` default** (propose-then-write-if-confirmed, the pattern `/pair-capability-verify-quality` uses for its first-run Custom Gate Registry):

   > No Tag Projection declared yet. Activate `risk:green|yellow|red` on stories and PRs? (recommended — other model parameters can be exposed as tags later, if you decide you want them)
   > 1. Yes, activate `risk` (writes the declaration)
   > 2. No, don't tag anything (records the opt-out so this isn't asked again)

   On **yes**, write the `## Tag Projection` → `Active: risk` section into `tech/risk-matrix.md`; on **no**, write `Active: none`. This registry write is `classify`'s own (the §5 precedent — the same self-write `/pair-capability-verify-quality` performs for its gate registry), not adoption **decision** content, so it does not route through `/pair-capability-record-decision`.
4. **Act**: Apply the resolved tags to the target — **card ⇒ PM-tool labels, PR ⇒ code-host labels** (same routing as Step 4). `classify` output wins for **classification** tags (`risk:*`, `cost:*`, …); foreign/manual tags are left untouched. **The target's host lacks label-API access** (PM tool for a card, code host for a PR) ⇒ the matrix stays in the body (Step 4), the tagging failure is reported, **non-blocking** (AC edge case).
5. **Verify**: Either the declared tags are applied, or the proposal was answered and recorded (no re-prompt next run), or the opt-out is honored — and the body matrix from Step 4 exists in every case.

## Output Format

```text
CLASSIFY ([refinement | review]):
├── Target:   [#story | #PR]
├── Tier:     risk:[green | yellow | red]   [(raised from refinement risk:yellow) — review only | (refinement floor unreadable — review value only, NOT confirmed) — review only]
├── Cost:     cost:[green | yellow | orange | red]
├── Model:    [KB defaults | + Criticality Table | + Overrides | + Tag Projection]
├── Tags:     [applied: risk:red | proposed (awaiting answer) | opted out (Active: none) | tagging failed — non-blocking]
└── Body:     matrix written (1 line + <details>, D22)

<details>
<summary>Matrix — per dimension</summary>

| Dimension | Tier | Source | Note |
| --- | --- | --- | --- |
| Service/domain criticality | [g/y/r] | [Criticality Table | KB default] | |
| Change/diff risk | [g/y/r] | [story scope | diff footprint] | |
| Business impact | [g/y/r] | [subdomain class] | |
| Security relevance | [g/y/r] | [path heuristic | assess-security verdict] | |
| Coupling balance | [g/y/r | not assessed] | [subdomain volatility + integrations | assess-coupling verdict | absent] | |

Confidence: [high | low — unreadable diff, path/service-level fallback | low — refinement floor unreadable]

</details>
```

## Worked Examples

Hand-traced fixtures that pin the two behavioural invariants — **determinism** (AC4) and **never-lower** (D17) — to concrete matrices. Each example lists every dimension value and the resulting tier so the rule (`risk` tier = the max of the assessed dimensions, floored by the refinement pass in review) is auditable, not merely asserted. These fixtures are conformance-checked (`src/conformance/capability-classify.test.ts`): each must carry all five dimensions and a tier that follows the max-rule — and, in review, the refinement floor.

Legend — dimension values are `green` | `yellow` | `red` | `not assessed`; `not assessed` is excluded from the max (D21). Tier is `risk:<green|yellow|red>`.

### Worked Example 1 — Determinism (refinement)

Same story context classified on two independent runs yields an identical matrix (AC4). Story context: an internal supporting-subdomain UI tweak — reposition the settings icon; no data-model change, no security-relevant paths, no cross-context integration, no DDD artifacts present.

| Run | Service/domain criticality | Change/diff risk | Business impact | Security relevance | Coupling balance | Tier |
| --- | --- | --- | --- | --- | --- | --- |
| A | green | green | green | green | not assessed | risk:green |
| B | green | green | green | green | not assessed | risk:green |

Run A and Run B are byte-identical — no randomness, no time-dependence. Tier = max(green, green, green, green) = `risk:green` on both runs.

### Worked Example 2 — Never-lower, benign diff (review)

The story was refined at `risk:yellow` (Change/diff risk yellow — a moderate declared scope). The review diff is benign: a docs paragraph and a user-facing copy string, no logic, no schema, no security paths. The review-computed dimensions are all green, but the **refinement floor** holds the tier at yellow — the review confirms, it never lowers (D17).

| Pass | Service/domain criticality | Change/diff risk | Business impact | Security relevance | Coupling balance | Tier |
| --- | --- | --- | --- | --- | --- | --- |
| refinement | green | yellow | green | green | not assessed | risk:yellow |
| review | green | green | green | green | not assessed | risk:yellow |

Review raw max = green, but `max(review, refinement-floor)` = `max(green, yellow)` = `risk:yellow`. The tier stays yellow; nothing is lowered.

### Worked Example 3 — Never-lower, risky diff raises (review)

Same refinement start (`risk:yellow`), but the review diff reveals a database schema migration plus a change to an authentication path. Change/diff risk rises to red and Security relevance rises to red, so the tier is **raised** to `risk:red` — above both the review-nothing case and the refinement floor.

| Pass | Service/domain criticality | Change/diff risk | Business impact | Security relevance | Coupling balance | Tier |
| --- | --- | --- | --- | --- | --- | --- |
| refinement | green | yellow | green | green | not assessed | risk:yellow |
| review | green | red | green | red | not assessed | risk:red |

Review raw max = red (Change/diff risk, Security relevance), so `max(red, yellow-floor)` = `risk:red`. The tier is raised, never lowered — a later benign diff could confirm red but could not drop it below the refinement floor.

## Composition Interface

**Composed by `/pair-process-refine-story`** (refinement): invoked with `$context: refinement` after the technical analysis. Returns the matrix; `/pair-process-refine-story` embeds the 1-line + `<details>` into the story body (D22) and lets `classify` apply/propose tags. Absent ⇒ `/pair-process-refine-story` warns and continues without a matrix (graceful degradation — never HALTs on classify's absence).

**Composed by `/pair-process-review`** (review, Phase 1): invoked with `$context: review` against the PR diff. Produces the review-time matrix (confirm-or-raise, never lower). The `/pair-capability-assess-security` verdict (Phase 2) feeds the **Security relevance** dimension and the `/pair-capability-assess-coupling` verdict feeds **Coupling balance** — both raise-only, consistent with the review floor. Any raise to `risk:red` is surfaced for `/pair-process-review`'s own decision step; `classify` never blocks or merges — it has no such authority.

**Invoked directly**: classify a single card or PR on demand; same algorithm, `$context` auto-detected.

## Edge Cases

- **No quality model doc installed**: **HALT**, pointer to #221. (The only hard stop.)
- **`tech/risk-matrix.md` absent or malformed**: KB defaults apply completely; no tags emitted; nothing fails (quality-model §6, D21).
- **Conflicting manual tags on the card**: `classify` output wins for classification tags (`risk:*`, `cost:*`); foreign tags untouched.
- **Unreadable diff (huge/binary)**: fall back to file-path/service-level evidence; flag low confidence in the `<details>`.
- **Projection defined but the target's host lacks label-API access** (PM tool for a card, code host for a PR): matrix still written to the body; tagging failure reported, non-blocking.
- **Coupling sources absent**: coupling dimension "not assessed", excluded from the max, never blocks (D21).
- **Refinement floor unreadable** (review, split tools, the PR carries no `Refs:` line — or the PM item is unreachable): the never-lower `max()` has no floor to apply, so report the tier as the **review-computed value, explicitly flagged as unconfirmed** (`Tier: risk:yellow (refinement floor unreadable — review value only, NOT confirmed)`, `Confidence: low`) and name the missing cross-link. Never silently present it as a confirmed tier: the floor may have been higher (D17).
- **PR with no classification present** (read by a downstream consumer, not produced here): treated as `red` (fail-safe, quality-model §3.2).

## Graceful Degradation

See [graceful degradation](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/graceful-degradation.md) (guideline missing → minimal run, ask directly; adoption file missing → run against KB defaults; the target's host unreachable — PM tool for a card, code host for a PR → matrix returned to caller, tagging deferred). Additional cases:

- **`/pair-capability-assess-security` not available** (review): fall back to the path-heuristic security relevance (quality-model §3.1) instead of the verdict; note the fallback.
- **`/pair-capability-assess-coupling` not installed / no DDD artifacts**: coupling dimension "not assessed" (never a HALT).
- **`/pair-process-refine-story` or `/pair-process-review` absent as caller**: run standalone via direct invocation.

## Notes

- **Applies the model, owns no criteria** (D18) — grep-verifiable: no green/yellow/red threshold lives in this file that is not a reference back to quality-model §3. Consumers downstream (gate, `/pair-process-review`, `/pair-next`) read tags only.
- **Built exactly twice per work item** (D17): refinement (story context) and review (diff). Review **confirms or raises, never lowers** — the never-lower rule is a floor over the refinement tier, per dimension and overall.
- **Deterministic**: same input (card/PR + model + adoption) ⇒ same matrix and tags every run (AC4). No randomness, no time-dependence.
- **Reading budget** (D22): the body/report output is 1 line + `<details>`, never an inline table.
- **Writes two kinds of thing itself**: the matrix into the card/PR body (Step 4) and — only on a confirmed first-run proposal — the `## Tag Projection` registry section in `tech/risk-matrix.md` (Step 5, the quality-model §5 self-write precedent, mirroring `/pair-capability-verify-quality`'s Custom Gate Registry). Adoption **decision** content is never self-written — that routes through `/pair-capability-record-decision`; the Tag Projection section is config-registry state, not a decision record.
- **No eligibility tag**: automation eligibility is an adoption-declared filter over classification tags (`risk:green`, …), not a special tag — `/pair-next` consumes it generically (quality-model §5, D18).
- **Idempotent** — see [idempotency convention](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/idempotency.md): re-running on an already-classified card recomputes the same matrix; a declared or opted-out Tag Projection is never re-proposed. Review re-runs recompute against the current diff (a raise can happen commit-to-commit; a lower never can).
