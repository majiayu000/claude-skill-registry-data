---
name: reverse-lamport
description: Audit an existing mathematical, logical, algorithmic, or technical proof from its stated conclusion backward as a bounded AND/OR graph of exact obligations. Use to reconstruct conclusion dependencies, determine whether a proof-supplied route establishes the conclusion, or expose hidden assumptions, unmet side conditions, cycles, overly strong steps, or silent route switches. For a source-mapped Lamport rendering use convert-lamport, and for forward hierarchy, construct, and scope conformance use forward-lamport before this skill. This does not decide full theorem-level entailment by searching for a different proof; do not turn the audit into a linear reversed proof, exhaustive proof search, or replacement proof.
---

# Audit Proofs with Reverse Lamport

Start at the stated conclusion and ask what must be true for each major claim to follow by the route the proof actually uses. Build a bounded dependency graph, not a reversed paraphrase of the proof. Audit the given proof without silently repairing it.

## Related skill and combined use

Choose the audit by its direction and object:

- Use this skill when the requested product is a conclusion-first bounded AND/OR obligation graph or the main question is what the submitted proof's conclusion-reachable dependencies support.
- Use `$convert-lamport` when an existing ordinary or loosely organized proof first needs a source-mapped Lamport-style rendering. Conversion is optional when this conclusion-first audit is requested directly.
- Use `$forward-lamport` when the submitted proof's forward hierarchy, local scopes, and Lamport constructs are part of the contract.

When both audits are requested:

1. Freeze one exact theorem contract, source boundary, and set of accepted primitives. If `$convert-lamport` was used, freeze its exact rendering, source-to-step ledger, and issue register; mapping annotations establish provenance only and are not proof premises.
2. Run `$forward-lamport` first to establish the forward step ledger and legal visibility of assertions.
3. Run this skill second from the exact conclusion. Use the forward ledger as evidence, but recheck the exact proposition and scope at every dependency edge.
4. Report both verdicts under separate headings; do not convert one verdict mechanically into the other.

When consuming a forward step ledger, an `OK` or `MINOR` step may support an edge only after its exact proposition and visibility are rechecked. A `CONDITIONAL` step leaves the corresponding reverse obligation `open`. A `MAJOR` or `CRITICAL` step is failing support and cannot introduce a witness or discharge an edge. These step-status rules govern the handoff; do not mechanically derive a reverse verdict from the overall forward verdict.

The forward verdict is the **proof-establishment axis**: whether the submitted hierarchical proof discharges the theorem with valid construct and scope use. This skill's verdict is the **proof-route support axis**: whether a conclusion-reachable route supplied by the proof closes, merely fails to establish the conclusion, or supports a non-entailment verdict by counterexample or decisive non-entailment argument. `NOT ESTABLISHED BY THIS PROOF` does not by itself show that the conclusion is false or that no different proof exists.

## 1. Fix the audit boundary

Extract exactly:

- the conclusion, including quantifiers, domains, and parameter dependencies;
- the stated hypotheses and definitions;
- the proof's major intermediate claims;
- the accepted background primitives;
- the text or source locations in scope.

Treat a claim as major when it carries a substantive inference: a named intermediate result, case conclusion, induction step, theorem application, construction guarantee, or transition on which the final conclusion depends. Do not create nodes for purely expository sentences.

State the accepted primitives before expanding the graph. Accept explicit hypotheses, definitions, agreed axioms, independently proved earlier results, named theorems whose exact applicability conditions are checked, and elementary algebraic or logical rules whose side conditions are satisfied. Do not accept the desired conclusion, an equivalent reformulation of it, or an unnamed "standard fact" merely because the proof treats it as obvious.

If the supplied proof is incomplete, audit the supplied route and mark unavailable support explicitly. Do not invent assumptions or infer missing text.

## 2. Build a bounded AND/OR obligation graph

Model each claim as an OR node over sufficient justification routes and each route as an AND node over its exact obligations. Because the audit is bounded, represent proof-supplied routes only, plus a diagnostic route when it is needed to expose a silent switch. Normally the proof supplies one primary route.

Assign the conclusion an identifier such as `C0`. For every reachable major claim:

1. Identify the **primary route** the proof actually uses and label it `R0`, `R1`, and so on. Describe the route by its rule, construction, theorem, contradiction, induction, or case argument.
2. State every exact obligation required by that route. Include theorem premises, inference premises, domain restrictions, well-definedness, exhaustiveness, induction hypotheses, boundary cases, regularity conditions, and claimed bridges.
3. Connect the claim to those obligations as an **AND group**: every member must be discharged for that route to work.
4. Use an **OR group** only when the supplied proof genuinely develops alternative sufficient routes. Label each as `primary` or `supplied alternative`. A route mentioned only to expose a hidden assumption or unstated bridge behind a route switch is `diagnostic only` and cannot discharge the claim.
5. Recurse from each nonprimitive obligation until reaching an accepted primitive or a failing/open leaf.

Use dependency notation such as:

```text
C0 <- R0 (AND: O1, O2, C1)
C1 <- R1 (AND: O3, O4)
C0 <- Ralt (OR alternative; diagnostic only because it exposes O5)
```

Do not confuse cases with alternative routes. A proof by cases normally requires an AND group containing case exhaustiveness and a successful argument for every case, even though the cases themselves are disjunctive.

Do not force the graph into the proof's sentence order. Branch when one claim has several obligations, reuse a node when several claims need the same obligation, and preserve cycles so circularity remains visible.

## 3. Classify every obligation

Assign each obligation exactly one primary classification and a separate status.

| Classification | Use when |
| --- | --- |
| `hypothesis` | The obligation is exactly a stated assumption, with matching scope and strength. |
| `proved earlier` | An independent earlier result in the audited material proves the obligation. Link its claim node. |
| `definition` | The step is a direct unfolding, expansion, or use of a stated definition. |
| `named theorem` | A specifically identified theorem supplies the inference. List and check every applicability condition. |
| `unavailable support` | The proof identifies a particular internal derivation, admitted step, or omitted proof text that could discharge the obligation, but its content is not available for checking. Use status `open`; do not use this when the support is demonstrated false or absent. |
| `algebraic/logical step` | A local algebraic, order-theoretic, or logical inference is valid once its premises and side conditions are explicit. |
| `side condition` | The obligation controls applicability or well-definedness, such as nonzeroness, domain membership, regularity, convergence, measurability, exhaustiveness, or freshness. |
| `missing` | No stated hypothesis, earlier proof, definition, accepted theorem, or valid elementary step supplies the required proposition. |
| `circular` | The support path returns to the same claim or an equivalent unproved claim without independent grounding. |
| `too strong` | The obligation or intermediate claim asserts more than its cited support establishes or applies a result beyond its justified scope. Record the weaker supported statement. |
| `route switch` | The proof silently changes theorem, definition, representation, case, invariant, or argumentative route and omits the bridge needed to carry prior obligations across. |

Use statuses `discharged`, `open`, `failing`, or `diagnostic only`. Treat `missing`, `circular`, `too strong`, and an unbridged `route switch` as failing on a proof-supplied route. A `side condition` may be discharged or may depend on a separate `missing` node; do not hide an unsupported side condition in prose or give one node two classifications. A diagnostic-only route never counts as support.

Do not classify a named theorem by name alone. When its statement is available, record the exact implication being invoked and every premise. When the proof identifies a theorem but its exact statement or applicability is unavailable, state the exact meta-obligation—obtain that theorem statement and verify that its hypotheses and conclusion supply the target edge—without inventing its content. Classify the invoked support as `named theorem` with status `open` unless the supplied material independently demonstrates failure. Unavailability alone is not `missing` and must not force a failing route. Reserve `missing` for an exact required proposition for which the supplied route identifies no potentially discharging source, or for support shown to be absent rather than merely unavailable.

## 4. Bound, merge, and check the graph

Stop expanding at accepted primitives. Do not reprove axioms, definitions, named background theorems, or routine elementary rules after their exact preconditions have been checked. Do not search for every possible proof of the conclusion.

Follow these bounds:

- include nodes reachable from the stated conclusion through every route the proof actually supplies, expanding the primary route first;
- include a nonprimary route when the supplied proof actually develops it, or diagnostically when it exposes a hidden assumption such as a missing bridge behind a route switch;
- do not use an alternative route to rescue a broken primary route unless the supplied proof explicitly completes that route;
- stop an ambiguous branch at the first exact unavailable obligation and mark it;
- omit claims that do not affect the conclusion.

Merge repeated obligations when their propositions, quantifier scopes, domains, and parameter contexts are the same. Give the merged node one identifier and list every parent in `Needed by`. Do not merge merely similar obligations whose contexts differ.

Evaluate the graph structurally:

- discharge an AND route only if every child is discharged;
- discharge an OR claim only if at least one non-diagnostic, proof-supplied sufficient route is discharged;
- treat every reachable unsupported leaf as visible evidence against the specific route or routes that depend on it;
- detect direct and indirect cycles, including cycles hidden by renaming or equivalent reformulation;
- verify that every nonprimitive major claim has a primary route and every leaf has a classification and status.

Propagate discharge from accepted leaves upward. Do not let an ungrounded cycle discharge itself merely because every node in the cycle cites another node in that cycle.

Read `references/worked-audit.md` in full when calibrating the graph format, distinguishing a broken proof from a false conclusion, or handling a hidden domain or connectedness assumption.

## 5. Report the audit

Present the result in this order:

1. **Audit boundary:** quote or precisely restate the conclusion, hypotheses, scope, and accepted primitives.
2. **Obligation graph:** list each major claim and every route the proof supplies, primary first, with each route's AND obligations. Label any diagnostic-only comparison separately under the alternative-route rule.
3. **Critical findings:** explain missing, circular, too-strong, side-condition, and route-switch nodes without burying them in a narrative.
4. **Dependency table:** end the analysis with one row per unique node. Use at least these columns:

   | ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
   | --- | --- | --- | --- | --- | --- | --- |

   Use `root` or `major claim` in place of a classification only for claim nodes; every obligation node must use one of the eleven required classifications.
5. **Verdict:** place the verdict after the table and make it the final section.

Choose the verdict carefully:

- **FOLLOWS:** every obligation on at least one non-diagnostic route actually supplied by the proof is discharged, with no hidden assumption, circular dependency, overreach, or unbridged route switch on that discharged route.
- **NOT ESTABLISHED BY THIS PROOF:** no proof-supplied sufficient route closes, and every such route is blocked by at least one demonstrated failing obligation. State that this does not by itself show the conclusion is false or rule out a different proof.
- **DOES NOT FOLLOW FROM THE STATED ASSUMPTIONS:** provide a counterexample, countermodel, or decisive non-entailment argument; do not infer this verdict merely from a defective proof.
- **INDETERMINATE FROM THE PROVIDED MATERIAL:** no route closes, but at least one proof-supplied route remains merely open because unavailable proof text or invoked background could still discharge it. Prefer this over `NOT ESTABLISHED BY THIS PROOF` unless every proof-supplied route has a demonstrated failing obligation.

Name the decisive node identifiers in the verdict. Keep the audit bounded and explicit enough that another reader can verify every dependency without reconstructing a different proof.

If the user asks whether the theorem follows by some route not present in the submitted proof, report that theorem-level question as outside this bounded audit unless a decisive counterexample or countermodel settles it. If the user separately supplies another proof, audit that proof as a separate bounded graph against the same theorem contract and give it its own verdict; do not merge it silently into the first proof. Do not relabel `NOT ESTABLISHED BY THIS PROOF` as semantic non-entailment.
