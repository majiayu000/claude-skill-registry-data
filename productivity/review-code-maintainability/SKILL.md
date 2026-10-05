---
name: review-code-maintainability
description: Review implementation for maintainability, evolvability, anti-slop, and human complexity; emit `M#` findings and durable residue candidates when needed.
---

# review-code-maintainability

Phase 2 code review. Judge whether the change is easy to evolve safely, easy for a human to navigate, and free of avoidable slop.

This is not a style pass. Look for real future-change pressure.

## Read first

- `../references/task-packet-contract.md`
- `../references/persistent-artifacts-contract.md`
- `../references/review-phases-contract.md`
- `../references/compatibility-policy.md`
- `../references/ownership-and-reuse-policy.md`
- `../references/final-state-authoring-policy.md`
- `../references/initiative-workflow-contract.md` when reviewing an initiative child packet
- `../../references/communication-mode.md`
- relevant tracked `AGENTS.md` chain
- applicable `AGENTS.override.md` only if local execution constraints matter
- current task packet: `CODE_REVIEW.md`, `AMENDMENTS.md`, `PLAN.md`, optional `PLAN_SATISFACTION_REVIEW.md` for unresolved `PS#` detail

## Core scope

Check:

- maintainability
- evolvability
- anti-slop
- human complexity
- ownership clarity
- change amplification
- hidden coupling
- speculative abstractions
- needless indirection
- navigation cost for the next human/agent
- final-state coherence in canonical code/docs/contracts

Allowed fallback:

- raise a correctness/regression finding if you encounter one while doing this pass

## Core workflow

1. Establish review scope.
   - Read the thin handoff from phase 1: `CODE_REVIEW.md` as the primary rollup source, `AMENDMENTS.md` as required companion, and `PLAN.md` for original intent / owner-boundary context.
   - Read `PLAN_SATISFACTION_REVIEW.md` only when an unresolved `PS#` needs more detail.
   - Identify the exact implementation commit under review, the exact diff from that commit, changed boundaries, and the modules that now own the behavior.
   - If the lead did not provide the commit hash and the workspace is dirty, stop and ask which commit is the review target instead of guessing from a floating workspace.
   - If the workspace has drift beyond the named commit, review the named commit and call out the drift explicitly so the lead can re-anchor the review.
2. Run a maintainability pass.
   - Look for duplication, hidden coupling, scattered sources of truth, and logic that will drift if changed in more than one place.
   - Call out design debt only when it creates a realistic future bug surface or makes the new behavior harder to evolve safely.
3. Run a human maintainability pass.
   - Judge how quickly a human can find the owner code, rebuild the mental model, and make a safe edit without holding too much hidden context in working memory.
   - Treat high navigation cost, scattered logic, and heavy cross-file recall as maintainability problems.
4. Run an architecture-drift pass.
   - Check whether the change weakens module boundaries, introduces a second source of truth, leaks internal invariants across APIs, or increases change amplification.
   - Prefer findings that explain future breakage pressure: `this works, but every future change now has to update three places`.
5. Run an ownership-and-reuse pass.
   - Flag parallel same-purpose entities unless the new boundary is explicit and materially non-overlapping.
6. Run a final-state-authoring pass.
   - Flag dual vocabularies, dual status models, or dual owner semantics that survive inside canonical code/docs/contracts.
   - Flag files that read like migration notes, patch notes, or append-only overlays when one current model should be obvious.
   - Flag implementations that keep old/new same-purpose paths alive when no real external boundary requires that residue.
   - Flag changes that should have reused the current owner after a small tidy-first refactor.
   - Flag designs where one invariant or behavior now has multiple owners.
   - Flag implementations that require coordinated edits across same-purpose modules to keep one behavior correct.
7. Run an anti-slop pass.
   - Flag generic abstractions without leverage.
   - Flag speculative extensibility that is not earning its complexity today.
   - Flag helper or adapter sprawl that makes ownership harder to see.
   - Flag AI-shaped indirection, duplicated glue, or ceremonial wrappers that do not reduce real risk.
   - Flag prose/config/code duplication pressure that nudges the system toward multiple sources of truth.
   - Flag internal-only backward-compatibility scaffolding as unnecessary complexity unless the human explicitly required it for a real external boundary.
8. Check tests as maintenance evidence when relevant.
   - If the new structure makes correctness harder to prove or leaves fragile behavior weakly tested, treat that as a maintainability finding.
9. Write or update `MAINTAINABILITY_REVIEW.md`.
   - Emit only concrete `M#` findings with real future-change pressure.
10. Update `CODE_REVIEW.md` with the fixed rollup fields this phase owns.
   - `Maintainability verdict:` `strong`, `acceptable`, or `fragile`
   - unresolved `M#`
   - rerun notes
   - latest rolled-up status if the phase-2 verdict or follow-up status changed
   - keep key dispositions already decided in `AMENDMENTS.md` current when new review dispositions were resolved after phase 1
11. If the review exposes durable semantic/navigation residue, append it to `ARTIFACT_CANDIDATES.md`.
12. Update `INDEX.md` if packet status changes.

## How to inspect changes

- Start from the named implementation commit.
- Prefer `git show --stat <commit>`, then targeted diff reads, then final-code reads.
- Use workspace diff only to detect drift beyond the named review commit, not to silently move the review target.

## Maintainability heuristics

Look for:

- one behavior split across many files without a strong reason
- readers and writers of the same state no longer agreeing on one model
- logic duplicated across provider, adapter, and UI layers
- local edits that now require synchronized changes elsewhere
- ownership that is obvious only if you already know the backstory
- tests that prove the happy path but not the risky maintenance path
- compatibility aliases, wrappers, or dual-support paths that exist only for internal callers
- a new helper/service/adapter/store/module whose purpose substantially overlaps an existing owner
- old and new same-purpose implementations kept alive together after the change

## Human maintainability rule

Good code lets a person quickly:

- find the owner logic
- understand the contract
- identify likely change points
- make a safe edit without holding half the system in mind
- know which single owner to modify for one behavior

If the patch raises time-to-confidence or navigation cost materially, that is review-worthy.

## Findings bar

Only emit an `M#` finding when all are true:

- it is actionable
- it has credible future-change or maintenance impact
- you can point to the concrete structure or code path causing the trap

Do not report:

- purely hypothetical concerns with no credible trigger path
- generic `consider refactoring` advice
- style nits that do not affect future safety

## Requester-response rule

Always report the review result back to the requesting side.

- If the lead/orchestrator requested the review, reply back to the lead/orchestrator.
- If a human directly requested the review in this pane, reply back in this pane.
- Local pane output without an explicit reply to the requester does not count as review completion.

## Output shape

Default output should include:

- findings first, highest severity first
- exact `M#` findings
- short maintainability verdict: `strong`, `acceptable`, or `fragile`
- residual risks or rerun notes when useful

## Rerun rule

Rerun only when fixes materially change structure, ownership, complexity, or future change surface.

## Do not

- turn this into generic style commentary
- duplicate phase-1 plan-fidelity work unless a new issue depends on it
- inflate minor polish into maintainability findings
- write tracked `AGENTS.md`
- write `AGENTS.override.md`
- excuse internal-only compatibility scaffolding as harmless future-proofing
- excuse parallel same-purpose entities as harmless decomposition when they raise future change cost
- accept canonical owner docs or code that still teach superseded vocabulary or state models

## Initiative child packets
When the reviewed packet belongs to a parent initiative, keep parent/child vocabulary straight:
- parent initiative owns shared context and cross-task contracts
- child packet owns the executable plan and local implementation evidence
- flag duplication or drift that blurs those responsibilities
- flag parent/child state mutations performed by the wrong owner even when behavior still appears to work

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
