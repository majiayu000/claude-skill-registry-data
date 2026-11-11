---
name: pair-capability-assess-coupling
description: "Assesses architecture coupling against the three-dimensional model (integration strength x socio-technical distance x volatility + balance rule): `$scope: diff` — composed by /pair-process-review, emits a 1-line Architecture verdict + collapsed findings (D22), critical findings flagged for the merge decision; `$scope: full` — one-shot codebase audit written to .pair/working/reports/architecture/, handing every unbalanced integration (volatile as critical/significant, stable as tolerable) to the caller for tech-debt promotion. Reads real integration points, never structure alone; never a single-dimension decouple. Output-only; the model lives in one guideline (D37)."
version: 0.2.0
author: Foomakers
---

# /pair-capability-assess-coupling — Coupling Balance Assessment

Assess whether the coupling relationships in a change (or a whole codebase) are
**balanced**, in two scopes — `diff` (per-PR, composed by `/pair-process-review`) and `full`
(one-shot audit, standalone) — against the model resolved from the
[coupling-balance guideline](../../../.pair/knowledge/guidelines/architecture/design-patterns/coupling-balance.md):
the three dimensions (**integration strength**, **socio-technical distance**,
**volatility**), the **balance rule**, the **severity** criteria, the DDD mapping,
and the test implications. The model lives **only** in that guideline (D37); this
skill applies it and never restates it.

**Every finding is three-dimensional.** A coupling verdict is computed on all three
dimensions or it is not emitted — a finding grounded in fewer than three (e.g. a
structural dependency count alone) is invalid by construction (guideline "The Three
Dimensions"). The assessment **reads the actual code** — imports, calls, shared data
structures, data access — never the dependency graph's shape alone.

## Arguments

| Argument  | Required | Description                                                                                                                          |
| --------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `$scope`  | No       | `diff` — assess only the integration points the PR touches. `full` — audit the whole codebase. Auto-detected: called by `/pair-process-review` → `diff`; otherwise → `full`. |
| `$area`   | No       | Full scope only. Package/area to narrow the audit (default: whole codebase).                                                          |
| `$output` | No       | Full scope only. Directory the audit report is written to. Default: `.pair/working/reports/architecture/` (D14 — report path override). |

## Model Source (both scopes read this)

The model is resolved through the standard **Adoption > KB default** layering; the
KB guideline is the sole home of the criteria (D37):

1. **KB default** — [coupling-balance.md](../../../.pair/knowledge/guidelines/architecture/design-patterns/coupling-balance.md): strength levels (intrusive > functional > model > contract), the distance axes, essential-vs-accidental volatility, the balance rule, severity, DDD mapping, test implications.
2. **Volatility inputs (adoption)** — [adoption/product/subdomain/](../../../.pair/adoption/product/subdomain) (subdomain classification → essential volatility: core = high, supporting = medium, generic = low) and [adoption/tech/boundedcontext/](../../../.pair/adoption/tech/boundedcontext) (context boundaries → distance). Read when present; **asked or estimated** when absent (no-DDD degradation, never HALT — consistent with #246).
3. **Project delta (adoption)** — `tech/risk-matrix.md` `## Overrides` may tune severity thresholds; absent ⇒ KB defaults apply completely (D21).

A missing/malformed adoption file is treated as absent: warn and fall back (never HALT on adoption absence).

## Algorithm

### Step 0: Detect Scope

1. **Check**: Is `$scope` provided?
2. **Skip**: If provided, use it. Proceed to Step 1.
3. **Act**: Auto-detect: invoked with a PR/diff in context (i.e. by `/pair-process-review`) → `diff`; otherwise → `full`.
4. **Verify**: Scope is set.

### Scoped Context (package-local override)

Opt-in. When the central adoption file carries a `## Package-Local Adoption` router, resolve the rule set per [scoped context resolution](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/scoped-context-resolution.md) (diff-scoped here: globals + `<pkg>/.pair/` of the packages the diff touches, nothing else); report a central↔local conflict, a dangling router entry, and — when the [complexity signals](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/package-local-adoption.md#activation-proposal) fire — PROPOSE the override and wait for approval, never activate. No router ⇒ unchanged behaviour.

### Step 1: Load the Model

1. **Act**: Read [coupling-balance.md](../../../.pair/knowledge/guidelines/architecture/design-patterns/coupling-balance.md) (the criteria) and the volatility inputs (Model Source layers 2-3), skipping any adoption file that doesn't exist.
2. **Act**: If the guideline is **missing** (KB not installed), follow [Graceful Degradation](#graceful-degradation) — assess against the three dimensions from first principles and note the reduced basis; do not invent a different model.
3. **Verify**: Model + available volatility inputs loaded. Adoption absence is logged as "volatility asked/estimated", not an error.

### Step 2: Resolve Integration Points (read the real code)

1. **Act**: Identify the coupling relationships in the surface:
   - `diff` — only the integration points the diff **touches**: new/changed imports, cross-module calls, shared types/DTOs, direct data access across a boundary, duplicated business rules. Never the whole codebase (huge-diff edge case).
   - `full` — map integrations between components across `$area` (default: whole codebase).
2. **Act**: For each relationship, read the actual code at both ends — what knowledge is shared, which symbols cross the boundary — never the dependency graph shape alone.
3. **Verify**: Every relationship in scope has its real shared-knowledge surface identified. **Single-module project / no cross-component integration** → no relationships: emit verdict "balanced / not applicable", no noise findings (edge case).

### Step 3: Score the Three Dimensions

For each relationship, assign **all three** per the guideline:

1. **Integration strength** — intrusive / functional / model / contract, from what actually crosses the boundary (private access and duplicated rules are intrusive/functional even when they look incidental).
2. **Socio-technical distance** — code-structure + team + runtime distance, relative to the abstraction level under analysis (fractal: a cross-module imbalance counts even inside one deployable).
3. **Volatility** — essential from subdomain classification (core→high, supporting→medium, generic→low); accidental (provider/fashion-dependent implementation) flagged as such. **Never from commit frequency alone.** No DDD artifact → ask the developer or estimate from the code's business role, and **label the value "estimated"** in the output.

**Verify**: no relationship carries a partial (< 3 dimensions) score. A partial score is dropped, not emitted.

### Step 4: Apply the Balance Rule and Severity

1. **Act**: Apply the **balance rule** exactly as the guideline defines it — resolve the criteria from [The Balance Rule](../../../.pair/knowledge/guidelines/architecture/design-patterns/coupling-balance.md#the-balance-rule) (combine strength and distance; volatility is the multiplier). Do not restate the rule here.
2. **Act**: Assign severity from the guideline's [Severity](../../../.pair/knowledge/guidelines/architecture/design-patterns/coupling-balance.md#severity) table (critical / significant / tolerable) — the sole home of the criteria (D37); this skill applies it, never restates the conditions.
3. **Act**: Rank the findings — unbalanced **and** volatile (critical/significant), plus significant implicit-knowledge findings, earn *attention* and feed the merge decision. An unbalanced-but-low-volatility relationship is **retained as a tolerable finding** for tech-debt promotion — never dropped, never blocking. Only a **balanced** relationship (or a partial <3-dimension score) is **not** a finding ("few critical beat many minor").
4. **Verify**: every emitted finding is unbalanced on the rule and carries a severity backed by all three dimensions.

### Step 5: Attach a Rebalancing Proposal (two-dimensional, never "decouple")

1. **Act**: For each finding, propose a move that names the dimension it changes (guideline "Rebalancing"): **reduce strength** (introduce a contract / ACL / published event) or **reduce distance** (co-locate). Never a bare single-dimension "decouple".
2. **Act**: Decomposition raises distance — only suggest splitting when strength is already low enough to keep the split balanced; on a high-strength relationship, reduce strength first.
3. **Act**: Where relevant, name the test implication (contract-coupled → integration contract test + boundary/encapsulation test).
4. **Verify**: every finding has a grounded, multi-dimensional proposal.

### Step 6: Route by Scope

- `$scope = diff` → Step 7 (emit review verdict, write nothing).
- `$scope = full` → Step 8 (write audit report, hand off tech-debt promotion).

## Diff Scope (per-PR)

### Step 7: Emit Review Verdict

1. **Act**: Compute the overall verdict = highest severity among the diff's findings (a balanced diff → "balanced"). Render the 1-line verdict + collapsed `<details>` findings per Output Format — **output-only, no files written**. The caller (`/pair-process-review`) embeds it as the **Architecture** verdict-first row (1 line at top, details collapsed, D22).
2. **Act**: If any finding is **critical** → flag it explicitly for the caller: this is the signal `/pair-process-review` factors into its major/critical severity flow (the merge decision stays `/pair-process-review`'s — this skill never blocks). A **significant/tolerable** finding in a low-volatility area is reported for **tech-debt promotion**, not blocking.
3. **Verify**: Verdict emitted; critical findings flagged; nothing written.

## Full Scope (one-shot audit)

### Step 8: Write Audit Report + Hand Off Tech-Debt

1. **Act**: Render the report — the mapped integrations and, flagged, **every unbalanced** one: unbalanced+volatile as critical/significant (attention), unbalanced+low-volatility as **tolerable** (retained, surfaced as tech-debt, never dropped), each with its three-dimensional score, severity, real integration point (file/symbol), and rebalancing proposal. Estimated volatility (no-DDD) is labelled as estimated.
2. **Act**: Create `$output` (default `.pair/working/reports/architecture/`) if absent; write `$output/<YYYY-MM-DD>-coupling-audit.md`. This is a direct write — reports are operational artifacts (D14), the same exception `/pair-capability-assess-security` audit and `/pair-capability-design-manual-tests` use; this skill writes **no adoption content**.
3. **Act**: Assemble a tech-debt promotion tuple **per finding** for the caller to persist via `/pair-capability-write-issue` (topical label `tech-debt`, the #224 pipeline): title, the three-dimensional rationale, severity, rebalancing proposal. This skill **creates no issues itself** — it hands the tuples to the caller.
4. **Verify**: report written at the resolved path; tech-debt tuples assembled for handoff.

## Output Format

### Diff Scope

```text
COUPLING ASSESSMENT (composed by the review process — no files written):
├── Scope:     Diff
├── Verdict:   [balanced | tolerable | significant | critical] — [1-line summary]
├── Findings:  [N total — N critical, N significant, N tolerable]
├── Basis:     [KB model | + subdomain/boundedcontext adoption | volatility estimated (no DDD)]
└── Feeds:     Architecture row of the review report (D22) — critical flags the review decision, never blocks here
```

<details>
<summary>N coupling findings</summary>

1. [severity] [component A] ↔ [component B] — strength: [intrusive|functional|model|contract], distance: [low|moderate|high], volatility: [high|medium|low (est?)] — [unbalanced: cascading | low-cohesion] — proposal: [reduce strength: … | reduce distance: …] — test: [contract+boundary | …]
...

</details>

### Full Scope

```text
COUPLING AUDIT COMPLETE:
├── Scope:     [whole codebase | $area]
├── Mapped:    [N integrations]
├── Flagged:   [N unbalanced — N critical, N significant, N tolerable]
├── Report:    [.pair/working/reports/architecture/<file> — written]
├── Tech-debt: [N tuples handed to caller for the write-issue pipeline (tech-debt label, #224)]
└── Basis:     [KB model | + subdomain/boundedcontext adoption | volatility estimated (no DDD)]
```

A single-module / no-cross-component surface renders as `Verdict: balanced — not applicable (no cross-component integration)` with no findings.

## Composition Interface

When composed by `/pair-process-review` (review-time Architecture dimension, step 2.3):

- **Input**: `/pair-process-review` invokes `/pair-capability-assess-coupling` with `$scope: diff` against the PR diff.
- **Output**: returns the verdict + collapsed findings (Diff Scope output). `/pair-process-review` embeds it as the **Architecture** verdict-first row (D22) and, if any finding is critical, factors it into its own major/critical severity flow. **Capability absent** → `/pair-process-review` renders the row as **"not assessed"** and proceeds (standard graceful degradation) — this skill states the contract; the row/degradation rendering is `/pair-process-review`'s.
- **Persistence**: none — diff scope writes nothing.

When composed for full-audit tech-debt promotion:

- The caller persists each handed-off finding as a tech-debt item via `/pair-capability-write-issue` (topical `tech-debt` label — the #224 pipeline). This skill assembles the tuples; it creates no issues itself.

When read by `/pair-capability-assess-architecture`:

- The coupling-balance guideline is a reading input to `/pair-capability-assess-architecture`'s evaluation step — the coupling criteria inform pattern scoring. `/pair-capability-assess-coupling` and `/pair-capability-assess-architecture` share the guideline, not each other's logic.

When invoked **independently** (`/pair-capability-assess-coupling` on a branch, or `$scope: full`): full one-shot flow; the report (full) or verdict (diff) is returned to the developer.

> Review-side wiring (listing `/pair-capability-assess-coupling` as a Composed Skill in `/pair-process-review` step 2.3 and the Architecture row in the review template) is delivered separately (#228). This skill is authored ready-to-compose; nothing here depends on that wiring existing yet.

## Edge Cases

- **Huge diff**: assess only the changed integration points, never the whole codebase in diff scope (Step 2.1).
- **No DDD artifacts** (no subdomain/boundedcontext): ask or estimate volatility, label it "estimated", complete the assessment — **never HALT** (consistent with #246 degradation).
- **Capability absent in review**: `/pair-process-review` renders "not assessed" and proceeds (graceful degradation) — this skill has no say once uninstalled.
- **Single-module project**: no cross-component integrations → verdict "balanced / not applicable", no noise findings.
- **Unbalanced but stable** (low volatility): reported as **tolerable** → tech-debt, never blocks.
- **Structure-only signal** (a dependency count with no readable shared-knowledge surface): not a finding — a verdict on fewer than three dimensions is invalid (Step 3 verify).

## Graceful Degradation

See [graceful degradation](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/graceful-degradation.md) (guideline missing → minimal assessment, ask directly; adoption file missing → run against KB defaults; PM tool unreachable → n/a) for the standard scenarios. Additional cases:

- **coupling-balance guideline absent** (KB partially installed): assess the three dimensions from first principles and note the reduced basis in the output rather than HALTing — never substitute a different model.
- **`/pair-capability-map-subdomains` / `/pair-capability-map-contexts` not available**: infer volatility from the code's business role and label it estimated; infer boundaries from package structure — do not HALT.
- **`/pair-capability-write-issue` not installed** (full scope): the report (Step 8.2) is still written — it's this skill's own direct write; the tech-debt tuples stand in the report with no persistence path; note this explicitly.

## Notes

- **Writes exactly one kind of file itself**: the full-scope audit report under `.pair/working/reports/architecture/` (Step 8.2) — the same D14 exception `/pair-capability-assess-security` audit uses. Adoption content is never self-written; tech-debt items always go through the caller's `/pair-capability-write-issue` composition.
- **Never blocks** — no merge authority; a critical finding is a signal for `/pair-process-review`, not a gate this skill enforces.
- **Model lives in one guideline** (D37): [coupling-balance.md](../../../.pair/knowledge/guidelines/architecture/design-patterns/coupling-balance.md). This skill references it and never duplicates the strength levels, balance rule, or severity criteria — searching the KB for the model finds it only there.
- **Three dimensions, always**: a finding grounded in fewer than three is invalid; structure alone is never a finding.
- **Never blanket-decouple**: decomposition raises distance, so a split is proposed only when strength is already low enough to keep it balanced.
- **Idempotent** — see [idempotency convention](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/idempotency.md): a fresh verdict is computed every run against the current diff/codebase by design.
- **D22** (1-line verdict + collapsed details): a project-level rendering decision the caller honors; this skill emits in that shape.
