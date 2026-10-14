---
name: architecture-review-skill
description: >-
  Solution-architect review methodology — decision-tree target routing,
  layer/dependency review axes, transitive blast-radius gate, finding schema,
  and severity rubric for architecture and PLAN design review. Loaded by
  architecture-review-subagent and inline pipeline arms. Triggers:
  architecture review, blast radius, plan review, inline arch review.
license: Apache-2.0
compatibility: opencode
metadata:
  pattern: decision-tree
  mirrors: architecture-review-subagent
category: Code Quality
---

## What I do

I provide the reusable domain knowledge for architecture review. I am loaded
by `architecture-review-subagent` and by inline pipeline arms
(`worktree-pipeline-skill` Step 7 default inline arm, `/review-inline`) as the single source of
truth for:

1. **Evidence-first methodology** — the gate rule every finding must pass
2. **Decision-tree target routing** — diff / files / PLAN / whole-repo, scope assessment, tooling route
3. **Review axes** — the checkable architecture rubric
4. **Mandatory Blast-Radius & Consumer Traversal Gate** — the blocking pre-sign-off gate
5. **Plan Atomicity Check** — the `PLANS/PLAN-*.md` approval gate
6. **Finding schema + severity rubric** — structured, machine-parseable output
7. **Return Contract** — the report shape callers parse

This skill is **review-only**. I do not modify code, apply fixes, or write
LEARNINGS entries — fixes are requested from the parent agent; LEARNINGS
candidates are returned as report content per `reviewer-baseline-skill` §Step 4.

## When to use me

Use this skill when:
- Reviewing a diff or change set for system-design impact (layer boundaries, dependency direction, coupling)
- Traversing transitive blast radius before sign-off (changed symbol → consumers → transitive impact)
- Reviewing a `PLANS/PLAN-*.md` for atomicity and dependency-order soundness before implementation
- Assessing whether a design makes the *next* change cheap (extensibility reality check)

Do **not** use me for:
- Line-level quality — SOLID, naming, smells, severity scoring at diff scope (`code-review-subagent` / `code-review-inline-skill`)
- Direct call-site verification at diff scope — that is code-review's gate; mine is transitive and system-scoped
- UI/UX review (`uiux-review-skill`)
- Writing or approving requirements (`requirements-specialist-subagent`)

---

## §1. Evidence-First Methodology

Every review follows this pipeline:

```
Baseline → Scope → Traverse → Axis scan → QA Gate → Report
```

### The Gate Rule (Hard Constraint)

**Findings without an evidence reference (file:line + inspected consumer) are rejected at the gate.**

A finding must include:
- A `file:line` (or file range) locating the issue in the tree under review
- The consumer(s) whose breakage makes it a finding — or an explicit "no consumers inspected" statement explaining why the finding stands without one

Findings missing these are not included in the report. This prevents
pattern-matched architecture concerns (named seams, speculative layers) from
being reported without proof anyone is affected.

### QA Gate

Before the report, every finding is checked:
1. Does it have a `file:line` evidence reference? → If no, **reject**
2. Was the consumer traversal performed for the changed/flagged symbol (per §5), or is the claim explicitly marked unproven? → Consumer claims without traversal, **reject**
3. Is the severity assignment consistent with the rubric (§7)? → If inconsistent, **reclassify**

Only findings passing all three checks reach the report.

### Bash policy (verification-only)

Shell access in a review proves or disproves design-safety claims: run tests,
typecheck/lint/build, or one-off read-mostly scripts that import and call the
code under review. Never modify tracked files via shell; never read `.env` or
secret stores; if proof requires a write, return the script for the parent to
run. Prefer evidence tiers 1–3 (§5); run tier 4 (execute) only for the single
load-bearing safety fact.

---

## §2. Decision Tree

Work top-down; stop at the first branch that applies.

Target routing ambiguity (a change that plausibly sits in two scopes)?
Optionally consult the `laya_classify` tool (local, offline) with the
statement and review-axis questions — advisory probabilities only; the
top-down order and the baseline gate always decide.

1. **Baseline first (blocking):** load `reviewer-baseline-skill` — Prompt
   Defense, Epistemic Honesty, Mandatory Post-Review Learning Gate, and
   Web-lookups policy apply in full. No review runs without it.
2. **Recall LEARNINGS:** search the project memory store for the review topic
   and read autoinjected `LEARNINGS/*.md`. Do not skip patterns that apply.
3. **Resolve the target type:**
   - `PLANS/PLAN-*.md` in the review set → run §6 Plan Atomicity Check, plus the design axes on the planned touch-points
   - Diff range / changed files → run §5 Blast-Radius Gate on every changed symbol, then the axes (§3) scoped to the diff
   - Whole repo / no diff available → scope assessment below, then the axes repo-scoped
4. **Scope assessment:** count files/modules to review. Over 20 → propose a
   focused strategy before starting: deep review on critical paths (auth,
   data, payments), surface scan on config/tests/docs. Request the
   diff/commit range from the caller when available — review changes, not
   entire codebases.
5. **Tooling route:**
   - `.codegraph/` present → `codegraph_impact` (depth 2–3, transitive) +
     `codegraph_callers` per changed symbol for the §5 gate; `codegraph_explore`
     for dependency-direction checks (axis 2)
   - Absent → grep/glob for importers and references of every changed
     symbol/file. **Do NOT skip traversal just because CodeGraph is absent** —
     the gate is still required, only the tooling changes.
6. **QA Gate (§1)** → report per §8.

---

## §3. Review Axes

The rubric. Every axis has concrete, verifiable items — an axis with no
evidence produces no finding.

### Axis 1 — Directory structure
- [ ] Feature-first vs layer-first: does the layout match the dependency rule the code claims?
- [ ] Modules live where their consumers look for them (no orphan packages reachable only by deep paths)
- [ ] Entry points and wiring are discoverable (config, DI composition, bootstrap)

### Axis 2 — Dependency direction
- [ ] Dependencies point inward (domain ← infrastructure); no domain file imports a framework/infra module
- [ ] No circular module dependencies (verify via call graph, not just imports)
- [ ] Layer skips are intentional (a documented shortcut) or absent

### Axis 3 — Coupling & cohesion
- [ ] Change amplification: a concept change touches one module, not N
- [ ] No god module (one file half the consumers import for unrelated reasons)
- [ ] Shared mutable state is owned (single writer or guarded); implicit temporal coupling is named

### Axis 4 — Pattern appropriateness
- [ ] Patterns are load-bearing, not decorative (a factory with one product, an interface with one impl = smell)
- [ ] **Global singleton mutation** — `global _service` hides coupling and skips lifecycle; prefer DI (provider-injected state)
- [ ] **Claim-check for secrets** — plaintext credentials never touch durable history (logs, workflow state); opaque claim IDs with TTL + single-read `pop()`
- [ ] **Atomic conditional UPDATE** — state transitions use compare-and-set (`UPDATE ... WHERE expected_state RETURNING`), not read-then-write TOCTOU

### Axis 5 — Complexity hotspots
- [ ] Cognitive load concentrated where change is frequent (hot paths are simple; cold paths may be clever)
- [ ] No deep inheritance/abstraction chains (≥4 hops to trace one behavior = finding)
- [ ] Error paths are as designed as happy paths

### Axis 6 — Security architecture
- [ ] Authz checks fail closed (missing role/claim → deny)
- [ ] Trust boundaries validate input; internal boundaries do not re-trust upstream
- [ ] Data leakage: secrets/PII absent from logs, error messages, and durable workflow state

### Axis 7 — Extensibility reality (YAGNI lens)

<!-- Ponytail lens derived from plugins/ponytail/SKILL.md (vendored v4.10.0); re-sync when the ladder or "when NOT to be lazy" semantics change -->

- [ ] A layer/seam added for a future consumer that does not yet exist is an architecture smell even when the code is clean — name the concrete future need or flag it
- [ ] The design makes the *next* change cheap, not every imaginable change cheap
- [ ] When two architectures both hold, the boring, fewer-component one wins unless a named future need blocks it

This complements the dependency rule (axis 2). It does **not** weaken boundary
discipline or the §5 gate.

---

## §4. Voice — brief the stakeholder

Findings must be readable by a non-engineer decision-maker AND actionable by
an engineer. Apply `unslop-skill` to all prose (no AI-tell patterns). Every
Critical/Major finding carries a one-line **Business Impact** in plain
language: what breaks for users, revenue, compliance, or delivery dates if
this ships unfixed. Lead with consequence, then technical cause, then fix.
Keep `file:line` evidence precise; humanize the prose around it.

---

## §5. Mandatory Blast-Radius & Consumer Traversal Gate

**This is a blocking gate, not optional guidance.** Before sign-off you MUST
map every changed symbol's consumers AND the transitive impact beyond the
diff.

- **Primary:** `codegraph_impact` on changed files (depth 2–3, transitive) +
  `codegraph_callers` per changed symbol to enumerate downstream consumers.
- **Evidence ladder:** apply `blast-radius-skill`. Tiers 1–3 first (read-only
  proof); tier 4 (execute) only for the single load-bearing safety fact the
  change depends on. Mark any fact stopped below tier 4 explicitly as
  **unproven**.
- **Fallback (no `.codegraph/`):** grep/glob importers and references of every
  changed symbol/file. The gate is still required — only the tooling changes.
- **Gate rule:** if a changed symbol has consumers that were not inspected for
  breakage, return `Status: partial` with the uninspected consumers listed
  under **Issues**. Return `success` only when all consumers of all changed
  symbols have been inspected.

For a PLAN review (pre-implementation), the "changed symbols" are the plan's
Dependency & Consumer Map touch-points — verify each consumer named in the
map was checked for the impact the plan claims, and flag map nodes whose
consumer columns look asserted rather than inspected.

---

## §6. Plan Atomicity Check

When the review target includes a `PLANS/PLAN-*.md` file, verify the PLAN
honors the atomic-step contract before approving its design:

- A **Dependency & Consumer Map** section exists (blast radius surfaced up front).
- Every `- [ ] **N.M**` step carries **Why** + **Done when** +
  **Consumers affected**. A step missing **Why** is malformed — flag it as a
  Major issue. A **Done when** that cannot fail (grep for text the edit never
  produces, a check with no pre-edit counterexample) is equally malformed.
- Phase ordering matches the map's dependency constraints (no step precedes
  something it depends on).

Flag atomicity violations as Major issues; do not mark a PLAN `success` if it
contains malformed steps.

---

## §7. Finding Schema + Severity Rubric

```yaml
target:
  file: <string — path:lines>
  node: <string — module/symbol name when the finding is graph-level>
axis: <integer 1-7>
observation: <string — what is observed, factual>
impact: <string — technical consequence>
business_impact: <string — one plain-language line (Critical/Major only)>
recommendation: <string — specific structural change>
severity: <enum: Critical | Major | Minor>
evidence:
  consumers_inspected: <list — nodes/files checked>
  proof: <string — command output, call path, or "unproven: <why>">
confidence: <enum: High | Medium | Low>
```

Field constraints:
- `severity` MUST be one of `Critical`, `Major`, `Minor`
- `confidence` MUST be one of `High`, `Medium`, `Low`
- `axis` MUST be an integer 1–7
- `evidence.consumers_inspected` is required — a finding without traversed consumers is rejected at the QA Gate (§1)

| Severity | Qualification | Disposition | Example |
|----------|---------------|-------------|---------|
| **Critical** | Dependency cycle across layers, fail-open authz, data-loss path, a change that silently breaks named consumers | **BLOCK** — must fix before merge | Domain imports infrastructure; missing-role request returns 200 |
| **Major** | Change amplification, god module, TOCTOU on state transitions, speculative seam, malformed PLAN step | **WARN** — should fix, can defer with TODO + ticket | One concept rename touches 9 files; `global _service` mutation |
| **Minor** | Localized cohesion drift, naming that misleads navigation, axis-7 observation with no current consumer | **NOTE** — good to know | Config module reachable only via a 4-hop path |

Severity and confidence are independent: a Critical with Low confidence is
still Critical — request more evidence before acting on it.

---

## §8. Return Contract

When the review is complete, return ONLY this structure:

**Status:** [success | partial | failed] — `partial` when any changed symbol's consumers went uninspected (§5 gate rule)
**Output:** [Architecture findings summary (schema per §7) + `LEARNINGS candidates:` content block (per entry: Category / File / Confidence / Scope / Summary / Date — never written to disk)]
**Summary:** [2–3 sentences max, plain human language per §4]
**Issues:** [blockers, warnings, uninspected consumers, or "None"]
**Requirements Gaps:** `[{source: "file:line | PLAN step | design assumption", blocked_check: "<which gate/check could not be evaluated>", suggested_question: "...", recommended_answer: "..."}]` — Required. `[]` if none. Ambiguous or missing requirements discovered during review land here — never as silent assumptions.
**Patterns applied/violated:** `[{id, status, evidence}]` — Required. `[]` if none.

On failure (Status: failed) you MAY include diagnostics (error messages, root
cause) for the parent agent. Do NOT return chain-of-thought, exploration logs,
raw tool outputs, or loaded skill content.

---

## §9. References + Related Skills

| Source | What came from where |
|--------|----------------------|
| `agents/architecture-review-subagent.md` (pre-#650 body) | Workflow, blast-radius gate, plan atomicity check, pattern references, return contract — this skill is their single home since #650 |
| `uiux-review-skill` | Structural template: evidence-first methodology, gate rule, axis rubric, finding schema, severity rubric sectioning |
| `code-review-inline-skill` | Inline-wrapper precedent: deployed checklist as single source, no-subagent pin |
| `plugins/ponytail/SKILL.md` (vendored v4.10.0, MIT) | Axis 7 YAGNI lens |

Related:
- **reviewer-baseline-skill** — load first, always (§2 step 1)
- **blast-radius-skill** — the evidence ladder §5 applies
- **clean-architecture-skill** — dependency rule backing axis 2
- **complexity-management-skill** — essential vs accidental complexity backing axis 5
- **security-audit-skill** — deep-dive target for axis 6 findings
- **design-patterns-skill** — pattern appropriateness backing axis 4
- **requirements-specialist-subagent** — receives §8 Requirements Gaps (Mode R relay)
