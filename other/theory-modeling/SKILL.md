---
name: theory-modeling
description: Mathematical-modeling discipline. Use for assumptions, FOCs, equilibria, proofs, comparative statics, numerical checks, or renderable model notes.
user-invocable: true
---

# Theory Modeling

## Stage-Scoped References

Load per stage, not all at once.

| Reference | Load when |
|---|---|
| `references/planning.md` | PLAN phase - covers the **Model Inventory / Assumption Map** and the **Verification Plan**. Loaded by `superplan` when the work is theory/modeling. |
| `references/integrate-drift-tests.md` | `protection` stage when a drift test was selected - modeling-result candidates, symbolic and numerical tolerance conventions, and theory-modeling failure modes. |
| `references/integration.md` | `integration` stage - readability layer for reader-ready output: ex-post structural rewriting (objective-first), per-step local obviousness, cross-document coherence, prose-to-math precision, rendering legibility, and refactor-survival of correctness artifacts. |
| `references/objective-first.md` | `integration` stage - worked bad/good walkthrough and identification-training drills for objective-first structural rewriting; loaded on demand from `references/integration.md` Section A. |

The four gates below are the creation-time correctness floor — walked at every implementation dispatch, including rough exploratory work. `references/integration.md` is the readability layer, loaded when the document needs polishing for a human reader.

## The Iron Law

```
NO MANIPULATION WITHOUT DEFINED OBJECTS, INTERPRETABLE ASSUMPTIONS, AND STATED INTUITION
```

Every symbol has a meaning. Every assumption has a plain-language interpretation a researcher can defend. Every non-trivial move has a one-sentence reason.

Symbol with no stated meaning, assumption with no economic reading, derivation step invoked mechanically: back up and write the missing meaning, interpretation, or reason first.

**Non-default constraints** (traps the gates don't catch):

- Restrictions live on primitives. Do not silently move one onto an endogenous variable because the latter is shorter to write.
- Notation is fixed. Do not rename objects mid-derivation without an explicit old-to-new mapping.
- Restrictions are stated up front. Do not back-fill a key restriction (e.g., "assume interior solution") after the algebra is already written.

---

## The Four Gates

Ordered by the reader's trust chain: **Objects & Notation → Assumptions → Derivations → Verification & Rendering**. Each gate has an **artifact** the implementer produces and a **checklist** walked while producing it. The gates are **concurrent** — every modeling step exercises all four, with documentation built into the artifact.

`[BLOCKING]` items must be fixed for APPROVE; `[ADVISORY]` items are recorded and do not block. Verdict mechanics live in `superRA:review-task`.

### Falsification tests (per ledger entry in Gates 1 and 2)

Reviewer diagnostics run against a slot suspected of not pulling its weight — text that *looks* like a justification but would survive any small change to the object it claims to justify.

- **Substitution test.** Read the entry's "What the name carries" / "What this assumption carries" slot, then mentally swap in a hypothetical sibling — a different symbol $\mathbf{z}_q$ from the same proof, or a different assumption on the same primitive. **Re-read the slot under the swap.** Still true for the substituted object → generic, pins nothing down → BLOCKING. The slot must contain something *false* of any other object: a specific sign meaning, a specific structural role, a named scalar cited at a specific site.

  *Worked example.* "Plays a role in the proof of Lemma 3.1" stays true under a swap to $\mathbf{z}_q$ — vacuous → BLOCKING. "Sign-bearing scalar — positive iff the comparative static of price w.r.t. dividend $k$ is positive, cited at eq. (12)" goes false under the swap unless $\mathbf{z}_q$ carries the same sign meaning at the same site → passes.

- **Proof-deletion test (Meaning slot).** Cover the surrounding proof and re-read only the Meaning slot. **Can it still tell a reader what the object is** — type, denotation in already-introduced terms, construction? A slot that evaporates without the proof was stating what the symbol is *used for*, not what it *is* → BLOCKING.

  *Worked example.* "Used to verify $h_k = m_D \beta_{E,k}$" has nothing left once the proof is gone — usage, not meaning → BLOCKING. "Column-$k$ object of the loading matrix $H \in \mathbb{R}^{N\times K}$, with $\mathbf{c}_k := H^\top e_k$" still carries the type ($K$-vector), the parent object ($H$), and the construction → passes.

### Gate 1 — Objects & Notation

Pin down the objects and their names before manipulating them.

At write-up, review the notation you reasoned with and replace each shorthand rather than justify keeping it — substitute its expression inline, or map it to an existing symbol. Shorthand left standing in the output is a defect.

A new symbol earns its place two ways: standard notation an economist writes without prompting ($r$, $w$, $\beta$), defined at first use; or writing its expression out each time would lose real meaning — the one-site test in the ledger's `What the name carries` slot, applied to every new output symbol. A symbol meeting neither is inlined — introducing notation that fails this bar counts against the work like an algebra error.

**Artifact: notation ledger table at the end of the task's `## Results`.** One row per object. An indexed family ($x_k$ for $k=1,\dots,K$) is one row; distinct symbols never share a row. Tasks introducing no new symbols record "None."

| Symbol | Meaning | First use | Reuse | Inline alternative | Carries | Nearest existing | Why not existing |
|---|---|---|---|---|---|---|---|
| `<name>` | `<type; denotation; origin>` | `<ref>` | `<refs / none>` | `<expression>` | `<lost meaning>` | `<symbol / none in scope>` | `<only if applicable>` |

Symbols in the governing ancestor's canonical Notation Conventions table are reused with their canonical meaning and need no row.

**Writing the Meaning slot.** Three components, all required:

1. **Type / space.** Scalar in $(0,1)$, $K$-vector in $\mathbb{R}^K$, $N\times N$ symmetric matrix, function $X \to Y$, random variable on $(\Omega,\mathcal{F},\mathbb{P})$ — dimension and domain wherever applicable.
2. **Denotation in the model's vocabulary.** What the object represents in already-introduced terms: "the coefficient on $X_t$ in eq. (12)", "the Lagrange multiplier on the resource constraint", "row $k$ of the dividend-loading matrix $H$". References only objects already defined.
3. **Origin if derived.** Construction from prior symbols, e.g. $\mathbf{c}_k := H^\top e_k$ — the construction, not a step that uses it later.

The Proof-deletion test diagnoses whether the slot satisfies this recipe.

**Anti-patterns for Meaning:**

| Bad meaning | Why it fails |
|---|---|
| "Used to verify $h_k = m_D \beta_{E,k}$" | Role in proof, not what the object is. |
| "An auxiliary vector" | Adjective + type, no denotation. |
| "The column-$k$ object" | Tautology — restates the index. |
| "Defined as $\mathbf{c}_k = \dots$ below" | Forward reference; meaning must be defensible at first use. |
| "Local proof-only construct" | Locality is scope, not content. |

**Checklist:**

- `[BLOCKING]` Ledger entry written **before** the symbol appears in proof text. Other documentation runs concurrently with the math; symbol introduction does not — post-hoc entries reverse-engineer justifications for choices already made.
- `[BLOCKING]` Notation is interpretable or genuinely conventional. Placeholder labels (`A/B/C/D`, `T1/T2`, `eq1`, `var2`) are not acceptable; conventional notation (`r` for an interest rate, `w` for a wage) is, defined at first use.
- `[BLOCKING]` Meaning slot satisfies the type / denotation / origin recipe and survives the proof-deletion test.
- `[BLOCKING]` Reuse-sites slot cites every additional appearance with line or equation refs, or states "none." Claims of reuse without refs are REVISE.
- `[BLOCKING]` Inline-alternative slot shows the actual substituted expression, not a description of it ("would be unwieldy" is not an inline alternative).
- `[BLOCKING]` One-site symbols (Reuse sites: none) justify via concrete content in "What the name carries" — sign meaning, structural role, named scalar cited elsewhere. One-time abbreviation fails regardless of length.
- `[BLOCKING]` Every new non-standard symbol in the shipped output clears the bar — standard notation, or meaning that inlining would lose. A symbol clearing neither is inlined or mapped to an existing one. "Nearest existing symbol considered: none in scope" is falsifiable: a candidate in the canonical Notation Conventions table, the active lemma, or an upstream derivation is REVISE.
- `[BLOCKING]` One entry per object. Indexed families ($x_k$ for $k=1,\dots,K$) count as one; bundling distinct objects under a shared justification is REVISE.
- `[BLOCKING]` Domains, units, and sign restrictions stated whenever they matter for the algebra, comparative statics, or numerical checks.
- `[ADVISORY]` Multiple reasonable notation choices: prefer the one matching the literature or existing project docs; note the mapping on any deviation.

### Gate 2 — Assumptions

Assumptions carry the economic content. Each is attached to a primitive object, readable as economics, and no weaker than it needs to be — one interpretable primitive over a scattering of weak technical restrictions.

**Artifact: assumption ledger table at the end of the task's `## Results`.** One row per assumption. Tasks introducing no new assumptions record "None."

| Assumption | Interpretation | Primitive | First bite | Scope | Without it | New restriction | Nearest existing | Why not existing |
|---|---|---|---|---|---|---|---|---|
| `<statement>` | `<plain reading>` | `<primitive>` | `<ref>` | `<results>` | `<changed conclusion>` | `<increment>` | `<assumption / none>` | `<only if applicable>` |

**Checklist:**

- `[BLOCKING]` Assumption attached to a primitive (preferences, technology, endowments, information, timing, distributions, parameter domains, boundary conditions, normalizations). Assumptions stated as desired properties of endogenous objects are REVISE unless those properties are later proved.
- `[BLOCKING]` Interpretation slot carries a one-sentence plain-language reading a researcher can defend ("risk aversion bounded so the value function is finite"). Math-only restrictions with no economic interpretation are REVISE.
- `[BLOCKING]` "Without this assumption" slot names a specific conclusion that changes. Vague claims ("the result would be weaker") are REVISE.
- `[BLOCKING]` "What this assumption carries" slot names the additional restriction on the named primitive that existing assumptions do not impose. Generic claims ("makes the proof cleaner") are REVISE.
- `[BLOCKING]` Multiple scattered assumptions replaceable by one stronger primitive assumption with a cleaner interpretation: prefer the synthesis, record the trade in "Why state it this way." Reviewer applies a judgement margin — flag only a clearly cleaner synthesis.

### Gate 3 — Derivations

Derivations must be auditable — a correct result that cannot be checked is not an acceptable handoff artifact. Every non-trivial move needs both the technical rule and a reason for invoking it here.

**Artifact: the proof / derivation body in the task's `## Results`.**

**Checklist:**

- `[BLOCKING]` The active solution concept named before derivation starts: planner problem, competitive equilibrium, recursive equilibrium, steady state, fixed point, or other.
- `[BLOCKING]` Top-level proof goal stated in one sentence before the first displayed equation. Derivations opening with algebra and no stated target are REVISE. (Reader-facing recursive signposting — sub-arguments at every level, transition prose — is `references/integration.md` Section A.)
- `[BLOCKING]` A derivation step depending on a previously established equation, lemma, or proposition cites it by name or equation number. Asserted equations with no path to a named source are REVISE. (Cite-with-operative-form-recall for distant sources, and prose-level precision — math symbol vs. English description, equation reference vs. positional pointer — are Section B.)
- `[BLOCKING]` One logical algebraic move per displayed step. No collapsing multiple substitutions, cancellations, and sign changes into "therefore". (Section B's half-page mask test is the integration-stage detection layer.)
- `[BLOCKING]` Each non-obvious step names the rule it invokes — substitute a constraint, differentiate, apply the envelope theorem, impose market clearing, linearize — **and** a one-sentence reason for invoking it. A rule-label without a reason is REVISE.
- `[BLOCKING]` Results depending on case splits or domains (interior vs corner, positive vs negative branch, existence/uniqueness conditions): the active case stated, excluded cases checked or explicitly deferred.
- `[BLOCKING]` Comparative statics state what is held fixed, which object moves, and what sign or ranking is claimed.
- `[BLOCKING]` Reused symbols keep the same meaning throughout the task; notation changes carry an explicit old-to-new mapping.
- `[BLOCKING]` Claims of existence, uniqueness, monotonicity, or concavity carry a stated argument, not assertion by inspection.
- `[BLOCKING]` New equations, named statements (lemmas, propositions, definitions, corollaries), and derivation steps face the same necessity lens as ledger entries: removal leaving the reasoning intact means remove it. They need no individual ledger entries — the one-move-per-step and reason-per-move items above enforce the lens.

### Gate 4 — Verification & Rendering

A derivation is complete only after surviving at least one independent check and reading cleanly for a human audience.

**Artifact: verification work + rendered output.** Report symbolic checks in the human-readable markdown / LaTeX shipping in `## Results`. Run numerical checks when needed to verify algebra; keep their parameters, evaluations, and outcomes internal.

**Checklist:**

- `[BLOCKING]` Every headline symbolic result checked against at least one independent verification mode: substitute back into the original conditions, test a limiting or special case, or evaluate a simple numerical example.
- `[BLOCKING]` Numerical verification, when needed, uses explicit parameter values and a pass condition: residual near zero, sign, monotonicity, feasibility, branch selection, or fixed-point convergence. It is not reported.
- `[BLOCKING]` Special and limiting cases interpreted economically, not just numerically confirmed ("at $\beta \to 0$ the policy reduces to the myopic rule, matching the one-period benchmark"), and compared against intuition and any hypotheses stated in the task objective; divergences flagged before proceeding.
- `[BLOCKING]` Results checked back against the assumption map. A step quietly needing a stronger sign, domain, or regularity restriction than the map states: update the map before using the result.
- `[BLOCKING]` With code, CAS output, or a solver, the human-readable result matches the computed object exactly. No manual transcription drift.
- `[ADVISORY]` Numerically delicate objects: verify more than one parameter set, or a small perturbation around the baseline.

### Implementation standards

- `[BLOCKING]` Evidence showing an extra lemma, case split, derivation step, or verification pass is required to trust the result: add it inside the current task and rewrite the step text to match.
- `[BLOCKING]` Solver scripts, symbolic code, and model notes organized so a reviewer can trace the chain from primitives and assumptions to the reported result.
- `[BLOCKING]` Major modeling decisions (normalization, timing, equilibrium selection, parameter baseline, approximation point) carry a markdown explanation or nearby comment.

### Documentation and handoff

Beyond the per-symbol / per-assumption ledgers:

- `[BLOCKING]` The canonical Notation Conventions table is **user-gated** — implementers do NOT inline-edit it. A symbol is promoted from the task-level ledger only when the user confirms it should become canonical project-wide; until then the ledger entry is that task's source of truth.
- `[BLOCKING]` Definitions, assumptions, and the reason for major derivation choices written alongside the math or code, not left only in chat.
- `[BLOCKING]` Human-readable equations, tables, and figures routed through `superRA:communicate`.
- `[BLOCKING]` Rendered math, prose, and supporting code use consistent notation for the same object.

## Common Rationalizations

Excuses the gate checklists alone do not catch.

| Excuse | Reality |
|---|---|
| "A/B/C is temporary; I will rename it later." | Placeholder notation spreads. Whatever the proof gets written under becomes the model. |
| "This new symbol makes the derivation read better." | Not the bar. An inlined expression carrying the same meaning makes the symbol redundant — inline it. |
| "The numerical check is only illustrative." | Even toy checks need explicit parameters and a stated pass condition. |
| "The CAS says it simplifies to zero." | CAS output is not the verification. State what was checked, under which assumptions, with what pass condition. |
| "I'll update the Notation Conventions table after the derivation is clean." | The table is user-gated. Log new symbols to the per-task `## Results` ledger; the user confirms promotion. |
| "It came from the derivation note, so it's already vetted." | Inherited notation is on trial again in the new proof. Legacy legitimacy does not beat a cleaner upstream name available now. |
| "These are local proof-only objects." | Cluster framings dodge per-symbol scrutiny by reframing the unit of evaluation. Each symbol walks Gate 1 on its own — one entry per object. |

## See also

- `superRA:communicate` — format discipline for equations, tables, figures, and LaTeX in Markdown.
