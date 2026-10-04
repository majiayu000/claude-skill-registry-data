---
name: forward-lamport
description: Audit an existing Lamport-style hierarchical mathematical proof forward for validity and whether its hierarchy, scope, dependencies, side conditions, and proof constructs discharge the stated theorem. Use when the central question concerns a top-down proof with numbered levels, subproofs, ASSUME/PROVE, SUFFICES, PICK, CASE, DEFINE, Q.E.D., or prose equivalents. For an ordinary proof that first needs source-preserving hierarchy, use convert-lamport; for conclusion-first AND/OR obligation reconstruction, use reverse-lamport. Do not use to generate or replace a proof, or to audit Lean, Coq, Isabelle, or other proof-assistant source.
---

# Audit a Lamport-Style Proof Forward

## Mission

Audit an already written **standard Lamport-style hierarchical proof**. Treat the proof as a tree of claims and subproofs, reconstruct the active goal and scope at every step, and challenge every inference that is not fully supported.

Preserve the proof's forward, top-down organization. Do not turn it into a reverse proof, a backward-chaining derivation, or a different proof. The task is to decide whether the submitted proof establishes the submitted theorem and to identify the smallest repairs needed when it does not.

Be adversarial but precise. A plausible sentence is not evidence. A named theorem is not applicable until all of its hypotheses have been matched. An omitted side condition is a proof obligation, not an invitation to assume it.

## Boundaries

Do not:

- construct a proof from scratch;
- work backward from the conclusion as a reverse proof;
- replace the submitted proof with a more elegant proof;
- claim machine-checked certainty without an actual proof checker;
- treat Lean, Coq, Isabelle, or other proof-assistant source as a Lamport-style proof; use proof-assistant-specific auditing instead.

## Related skill and combined use

Choose the audit by its direction and object:

- Use this skill when the submitted proof's hierarchy, local scopes, and Lamport constructs are part of the contract.
- Use `$convert-lamport` first when an existing ordinary or loosely organized proof needs a source-mapped hierarchy. Conversion preserves gaps and is not evidence of validity.
- Use `$reverse-lamport` when the requested product is a conclusion-first bounded AND/OR obligation graph or the main question is what the submitted proof's conclusion-reachable dependencies support, independent of Lamport formatting.

When both audits are requested:

1. Freeze one exact theorem contract, source boundary, and set of accepted primitives. If `$convert-lamport` was used, also freeze its exact rendering, source-to-step ledger, and issue register; mapping annotations establish provenance only and are not proof premises.
2. Run this forward audit first. Its step ledger records which assertions are established and legally visible.
3. Run `$reverse-lamport` second from the exact conclusion. Use the forward ledger as evidence, but recheck the exact proposition and scope at every dependency edge.
4. Report both verdicts under separate headings; do not convert one verdict mechanically into the other.

The forward verdict is the **proof-establishment axis**: whether this submitted hierarchical proof discharges the theorem with valid construct and scope use. The reverse verdict is the **proof-route support axis**: whether a proof-supplied conclusion-reachable route closes, merely fails to establish the conclusion, or supports a non-entailment verdict by counterexample or decisive non-entailment argument. A forward `FAIL` alone never licenses `DOES NOT FOLLOW FROM THE STATED ASSUMPTIONS` or rules out a different proof.

## Required input

For a complete audit, require:

1. the exact theorem statement;
2. the complete structured proof;
3. definitions or conventions that are not standard in the stated domain.

External lemmas and citations may be supplied separately. If a cited result is unavailable, continue the audit conditionally and record the exact meta-obligation to obtain its statement and verify that its hypotheses and conclusion justify the affected step. Do not reconstruct unknown theorem content or silently accept “well known,” “standard,” or “by a theorem” when the missing statement could contain relevant hypotheses.

If a partial proof is structurally readable, audit the supplied portion, mark omitted or admitted dependencies `CONDITIONAL`, and use `INCOMPLETE` unless a separately demonstrated defect requires `FAIL`. Ask for clarification only when the theorem or proof is missing or unreadable, or when an essential nonstandard definition prevents a conservative interpretation. Otherwise make explicit, conservative assumptions and label them.

## Semantic model

A Lamport proof is a hierarchy of proof obligations.

- The statement being proved by a subproof is its **current goal**.
- A step at one level may itself have a lower-level proof.
- The lower-level proof must establish the step's statement.
- The final step of every completed level is `Q.E.D.` or an explicit assertion of that level's current goal.
- `Q.E.D.` means the current goal, not merely “the preceding discussion is finished.”

At a step, the normally available facts are:

- assumptions and definitions of the theorem;
- active assumptions introduced by enclosing proof constructs;
- statements of earlier siblings at every open level;
- statements of earlier ancestor-level siblings;
- definitions and witnesses whose scopes are still active;
- explicitly cited external results.

The normally unavailable facts are:

- later siblings or other forward references;
- the conclusion of the current step before it has been proved;
- lower-level substeps of a completed sibling;
- assumptions local to a closed sibling or closed case;
- witnesses or definitions that have left scope;
- claims from an abandoned, refuted, or admitted branch unless the dependence is explicit.

A useful visibility test is this: inside the proof of a step, one may cite earlier steps on the path's open levels, but not reach sideways into the internal proof of another step. For example, a proof of `⟨3⟩4` may use earlier visible level-1, level-2, and level-3 statements, but not a private level-4 substep belonging to a different branch.

## Normalize the proof before judging it

Do not change mathematical content. Build an internal ledger with one row per labeled or construct-bearing proof step; omit only purely expository unlabeled text:

- step label;
- parent step;
- construct type;
- statement;
- current goal before the step;
- current goal after the step, if changed;
- assumptions, definitions, and witnesses in scope;
- cited dependencies;
- proof text or child steps.

Recognize prose equivalents. For example, “It is enough to show...” is usually `SUFFICES`; “choose an element...” is usually `PICK`; and “suppose for this case...” is usually `CASE` or `ASSUME/PROVE`.

Preserve the author's labels. Accept canonical Lamport labels and decimal tree labels, but audit their semantics rather than their typography.

## Audit procedure

### 1. Freeze the theorem contract

Rewrite the theorem in a compact logical form without strengthening or weakening it. Record:

- all quantified variables and their domains;
- every hypothesis;
- the exact conclusion;
- definitions and ambient conventions;
- implicit type, existence, finiteness, non-emptiness, sign, regularity, or choice assumptions.

Check that the proof is proving this theorem, not a nearby statement. Watch for changed quantifier order, omitted boundary cases, stronger hypotheses introduced without discharge, or a conclusion weakened during the argument.

### 2. Validate the proof tree

Check that:

- step labels are unambiguous and nesting is well formed;
- every nontrivial assertion has a proof or explicit child subproof;
- every child subproof proves its parent statement;
- every completed level ends by proving its current goal;
- references obey hierarchy and scope;
- there is no circular dependency, direct or indirect;
- no step depends on a later step;
- closed local assumptions do not leak into later branches.

Treat poor formatting as a style issue unless it creates real ambiguity. Treat an ambiguous scope or dependency as a logical issue.

### 3. Check each proof construct by its actual obligation

| Construct | Audit obligation | Scope effect | Frequent failure |
|---|---|---|---|
| Simple assertion `F` | `F` follows from currently available facts | None beyond making `F` available to later visible steps | Missing premise, invalid inference, hidden side condition |
| `ASSUME A PROVE B` | Prove `B` under local assumption `A` | `A` and any `NEW` identifiers are local to this step's subproof; after closure, only the whole discharged assertion is exported | Using `A` after the subproof closes; failing to discharge `A` |
| `SUFFICES F` | Prove that `F` implies the old current goal | In the reduction proof, use `F` only as the temporary antecedent of that implication; after closure, the current goal becomes `F` | Merely proving `F`; never proving `F → old goal` |
| `SUFFICES ASSUME A PROVE B` | Prove that the whole displayed assume/prove assertion implies the old goal | The whole proposed assertion may support the reduction, but its internal assumptions and `NEW` identifiers are unavailable individually; after closure, they become active and the current goal is `B` | Using newly introduced assumptions or identifiers to justify the reduction |
| `PICK x ∈ S : P(x)` | Prove `∃x ∈ S : P(x)` without treating `x` as declared in this proof | Only after successful proof does fresh `x`, together with `x ∈ S` and `P(x)`, enter the containing scope | Using `x` in its own existence proof; no existence proof; non-fresh variable; witness escapes its scope |
| `CASE C` | Under local assumption `C`, prove the current goal | `C` is local to that case | Using `C` in another case; proving only a weaker case conclusion |
| Final case `Q.E.D.` | Show the cases cover all possibilities and therefore yield the current goal | Closes the case split | Missing or overlapping cases are acceptable only if coverage is still proved; non-exhaustive cases are not |
| `DEFINE d ≜ E` | Check that the definition is well formed, non-capturing, and used consistently; do not demand a subproof merely because it is a step | Normally active for the rest of the current level | Definition used before introduction or outside its level |
| `Q.E.D.` | Prove the exact current goal from visible earlier steps | Closes the current proof level | Restating an intermediate fact instead of discharging the goal |
| Equational or relational chain | Justify every relation and ensure the chain's directions compose to the required endpoint relation | Intermediate expressions remain local to the chain unless named | Reversed inequality, illegal cancellation, incompatible transitivity |

### 4. Audit every local inference

For each step, explicitly answer:

1. **What is the claim?** State it exactly, with domains and quantifiers.
2. **What facts are legally available?** List only visible facts.
3. **What rule or theorem is being used?** Name the inference, identity, definition, or cited result.
4. **Do all hypotheses match?** Map each required hypothesis to an available fact.
5. **Are side conditions proved?** Check nonzero denominators, sign before multiplying inequalities, convergence before exchanging limits or sums, measurability, compactness, freshness, and analogous domain-specific conditions.
6. **Does the conclusion follow exactly?** Do not accept “morally,” “essentially,” or “up to a harmless detail.”

Treat validity and citation specificity as separate checks. If a rule has a side condition that is already legally available, then that condition is not an unresolved validity obligation. However, when the written justification names the rule but does not identify the active fact that supplies its nontrivial side condition, mark the step `MINOR`, not `OK`; for example, “by cancellation” should cite the active nonzero assumption. This yields `PASS WITH MINOR ISSUES` when no major or critical defect remains. Do not upgrade the omission to a validity failure, and do not silently repair the written citation in the ledger.

When a step cites several earlier steps, verify that their conjunction really implies the claim. When it cites a theorem, reconstruct the substitution from the theorem's variables to the proof's objects.

A step may be left atomic only when the inference is genuinely routine for the intended audience and has no plausible hidden side condition. When uncertain, demand a lower-level expansion rather than guessing.

### 5. Check global proof patterns

Apply the relevant checks in addition to local inference checking.

**Direct proof:** The final `Q.E.D.` must derive the original current goal, not merely a useful intermediate result.

**Contradiction:** Confirm that the negation assumed is exactly the negation needed, that `FALSE` is actually derived, and that no consequence of the contradiction is used before the contradiction is established.

**Cases:** Audit each case under only its local assumption, then audit exhaustiveness separately. Do not let a true conclusion in each listed case conceal a missing case.

**Induction:** Identify the induction predicate, domain, base case, induction hypothesis, and induction step. The induction hypothesis is available only in the step case and only at the permitted predecessor or smaller objects. Check well-foundedness for nonstandard induction.

**Existence:** Distinguish proving that a witness exists from naming a witness. A `PICK` step requires an existence argument in which the proposed witness is not yet in scope; use it only after that proof succeeds.

**Uniqueness:** Check both existence and at-most-one. Do not accept “the construction gives the unique object” without the second implication.

**Set or function equality:** Check both inclusions or invoke a valid extensionality principle with its hypotheses.

**Optimization or extremal claims:** Check feasibility, attainment when claimed, and both the bound and a matching example or equality case.

### 6. Attack the proof

For every doubtful step, try at least one adversarial test:

- instantiate the claim on a smallest or boundary example;
- remove a suspected hidden hypothesis and look for a counterexample;
- test empty, singleton, zero, negative, infinite, degenerate, or non-generic cases as appropriate;
- independently recompute algebra, indices, signs, and quantifier order;
- trace dependencies backward to detect circularity;
- negate the step and see whether the cited premises can still hold;
- verify an external theorem from a primary source when available.

A found counterexample is decisive. Failure to find one is not proof of validity.

### 7. Classify findings

Use these severities consistently:

- **CRITICAL** — The theorem as stated is false, a counterexample exists, the proof is circular, or a central inference is invalid in a way that defeats the result.
- **MAJOR** — A nontrivial proof obligation is missing; a theorem is misapplied; a scope leak, missing case, unjustified existence claim, or hidden domain restriction affects validity.
- **MINOR** — No validity obligation remains unresolved, but a locally correct step needs a clearer citation, scope marker, side calculation, or statement.
- **NOTE** — Readability, notation, decomposition, or presentation advice with no identified effect on validity.

Do not downgrade a logical gap because the intended theorem is probably true. Do not upgrade a stylistic preference into a logical defect.

## Verdicts

Use exactly one overall verdict:

- **PASS** — Every step is supported, every local assumption is discharged, all external results used have been checked or were supplied exactly, and the final `Q.E.D.` proves the theorem as stated.
- **PASS WITH MINOR ISSUES** — No critical or major issue and no unresolved validity obligation remains; only minor or note-level improvements are needed.
- **INCOMPLETE** — Unavailable external lemmas, explicitly admitted steps, or omitted material prevent closure, but the supplied material contains no demonstrated defect that independently requires `FAIL`.
- **FAIL** — A demonstrated critical defect or unresolved internal major obligation prevents the submitted proof from establishing the theorem. Prefer `FAIL` over `INCOMPLETE` when both conditions occur.
- **NOT AUDITABLE** — The theorem or proof is missing, unreadable, or too incomplete to reconstruct a proof tree.

Use `INCOMPLETE` only when the proof identifies particular external, admitted, or deliberately omitted support that could still discharge the affected steps if supplied. A silently unsupported internal assertion or construct obligation with no identified potentially discharging source—such as an unproved `PICK` existence claim, case coverage claim, or scope bridge—is a `MAJOR` internal defect and requires `FAIL`. Do not turn every absent argument into “omitted material”; prefer `FAIL` whenever the submitted route itself asserts or uses an unsupported internal obligation.

A converter-created `OPEN` or `GAP-*` record does not by itself mean “omitted material” in the `INCOMPLETE` sense. Reclassify the rendered step from its proof role and source support: when the source presents an internal assertion as part of its route but supplies no proof, the exposed gap remains a `MAJOR` internal defect and requires `FAIL`. Use `CONDITIONAL` for a frozen dependency only when the source identifies it as external unavailable, admitted, or deliberately omitted. Preserve every `AMB-*` reading boundary while making this classification; do not choose the reading that makes the proof succeed, and do not let ambiguity conceal a separately recorded unsupported inference.

Never call an informal audit “machine verified.” State the confidence boundary: the result is a structured mathematical audit, not a kernel-checked proof.

## Output format

Produce the audit in this order.

### 1. Verdict

State the verdict in one sentence and name the highest-severity issue.

### 2. Theorem contract

Give the normalized theorem, including domains, hypotheses, conclusion, and any assumptions you had to infer.

### 3. Proof-structure summary

Report the number of steps and levels, the principal proof pattern, and whether scope and dependency structure are well formed.

### 4. Findings

List findings from highest to lowest severity. Use this form:

```text
[LMP-001] MAJOR — Step ⟨2⟩3 — Scope leak
Claim: ...
Available facts: ...
Problem: ...
Why it matters: ...
Required repair: ...
```

Reference the author's original step labels. Quote only the minimum text needed to identify a problem.

### 5. Step ledger

Include one row for every labeled or construct-bearing proof step; omit only purely expository unlabeled text:

| Step | Current goal | Legal dependencies | Justification checked | Status |
|---|---|---|---|---|

Statuses are `OK`, `MINOR`, `MAJOR`, `CRITICAL`, or `CONDITIONAL`. Use `CONDITIONAL` only when a step depends on unavailable external, admitted, or omitted material and has no independently demonstrated defect.

For a very large proof, group the ledger by top-level step if helpful, but do not omit any labeled or construct-bearing step.

### 6. Unresolved obligations

State each missing calculation, case, scope clarification, or known lemma as an exact proposition to be proved or supplied. When a cited result's content is unavailable, state instead the exact meta-obligation to obtain its statement and check that it supplies the target under the visible hypotheses. Say what downstream steps depend on every unresolved item.

### 7. Minimal repair plan

Propose local repairs in dependency order. Do not rewrite the entire proof unless the user asks. If a step is false, say whether it should be weakened, split into cases, given an added hypothesis, or replaced.

## Two canonical audit traps

### Illegal descent into another branch

```text
⟨1⟩1. ASSUME A PROVE B
  ⟨2⟩1. C
  ⟨2⟩2. Q.E.D.
⟨1⟩2. D
Proof: By ⟨2⟩1.
```

Reject the justification of `⟨1⟩2`. The visible result is the whole statement `⟨1⟩1`, not its private substep `⟨2⟩1`, which may depend on local assumption `A`.

### Misused `SUFFICES`

```text
⟨1⟩1. SUFFICES ASSUME A PROVE B
Proof: By A.
```

Reject the proof. The newly introduced `A` is available after the `SUFFICES` step while proving the new goal `B`; it is not available to prove that the reduction itself is valid.

## Operating principles

- Audit the submitted proof, not the author's reputation or likely intention.
- Prefer exact local objections to vague skepticism.
- Expose hidden assumptions rather than silently adding them.
- Preserve a distinction between a false step, an unproved step, and a poorly explained true step.
- A proof can be mathematically correct and still fail the requested standard Lamport structure; report logic and structure separately.
- Stop calling a step “obvious” as soon as its truth depends on a side condition, a scope fact, or a theorem not already in view.

## Source basis

This skill follows the ordinary, forward hierarchical proof method described by Leslie Lamport in *How to Write a Proof* and *How to Write a 21st Century Proof*: named hierarchical assertions, explicit proofs, scoped assumptions, restricted cross-level references, and a final `Q.E.D.` that asserts the current goal.
