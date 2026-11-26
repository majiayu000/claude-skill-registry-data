---
name: hard-problem-contract
description: "Write a contract-style prompt for a hard, precisely decidable problem: an open conjecture, a prove-or-disprove task, or a beat-the-frontier optimization. Use when ordinary prompting returns hedged partial results, special cases, surveys, \"this reduces to another open problem\", or early give-ups on long autonomous runs."
---

# Chnacknuss (hard-problem-contract)

## Overview

Turn the problem into a contract, not a request. The prompts that actually broke research-math frontiers in 2025–2026 (OpenAI's Cycle-Double-Cover prompt; Shouqiao Wang's six Erdős-problem solves, github.com/ShouqiaoW/erdos) are ultra-structured legal-contract style, not clever chain-of-thought: exact definitions, a forced binary settlement condition, an explicit ban list of results that do NOT count, multi-agent rules with adversarial auditors, and no early exit until the settlement condition is met. The model is forced to treat the proof like on-chain verification, not a vibe-check.

**Core principle:** everything a solver could use to soften the deliverable (undefined terms, "partial progress", "reduces to X", "verified up to n=12", returning early) must be closed off in writing before the run starts.

## When to use

- Open conjectures / prove-or-disprove tasks handed to a frontier model for a long autonomous run
- Research questions with an exact, checkable success criterion
- Beat-SOTA optimization where only an externally-verified score counts
- A previous long run came back with hedged partials, special cases, or "conditional on open problem X"

**When NOT to use:** problems without a precisely decidable success criterion: write the criterion first (what exact statement, verified how, counts as done?), then apply this skill. Not for routine engineering tasks.

## The seven clauses

Every contract has all seven. The master fill-in template is in [master-contract.md](master-contract.md).

| # | Clause | What it does |
|---|--------|--------------|
| 1 | **Definitions** | Every term defined exactly, including degenerate/edge cases (parallel edges, disconnected graphs, empty family). Removes "under my interpretation" escapes. |
| 2 | **Forced resolution** | Exactly one of two (or N exhaustive) outcomes, each with the exact statement that counts. A counterexample requires the explicit object plus full verification. |
| 3 | **Working posture** | "Assume, for purposes of the search, that a complete resolution exists and is findable." Kills the "this is famously open, so I'll survey" reflex. Posture governs search effort ONLY — never the verdict (see clause 7). |
| 4 | **Ban list** | Named weaker results that do NOT count: special classes, partial/approximate versions, fixed-size computation, reductions to any other open problem of comparable strength, counterexample candidates without full verification. |
| 5 | **Traps** | Problem-specific known failure modes: barrier theorems, false strengthenings, tempting circular reductions, exact-multiplicity errors. |
| 6 | **Multi-agent rules** | Up to N concurrent agents; start genuinely diverse approach families; keep incompatible routes alive; maintain a registry (ALIVE/BLOCKED/KILLED with refutations); dedicated adversarial agents that hunt the clause-5 failure modes plus circular reasoning; no route audits itself. |
| 7 | **Exit condition** | Effort floor (e.g. "spend at least 8 hours before even considering returning"). Only return a result that survives an adversarial audit panel instructed to REFUTE, plus an external verification gate (Lean compile, independent checker programs, a fresh benchmark-harness run). Nothing self-reported settles the contract. If the floor is hit without settlement, return the route ledger explicitly labeled NOT A RESOLUTION — never a softened "partial win". |

## Generating a problem-specific contract

1. Take [master-contract.md](master-contract.md) as the master template.
2. Feed it plus the target problem to the strongest available reasoning model; ask for a problem-specific version that preserves the exact statement, settlement criteria, ban list, and multi-agent rules.
3. Review the instantiation before running: the ban list must name **this problem's** tempting weaker results (the ones the literature is full of), and the traps clause must name its known barriers. A generic ban list is the #1 instantiation failure.
4. Run on the strongest model in long autonomous agentic mode; verify with Lean / independent checkers / the official harness, plus an adversarial pass.

## Executing in Claude Code

Map clause 6–7 onto the Workflow tool: diverse approach families as a parallel fan-out with per-family prompts; the registry as returned structured state; adversarial audit as a refute-by-default verify panel (majority-refute kills); loop-until-dry instead of fixed rounds; the external verification gate as the only code path that can return a settlement. For benchmark problems, "external gate" means a fresh run on the official harness on a clean state: a self-reported number never settles the contract (same discipline as ecdsafail-oracle-loop).

## Common mistakes

| Mistake | Fix |
|---------|-----|
| No posture clause — solver surveys the literature instead of attacking | Add clause 3 verbatim; it is a search posture, not permission to overclaim |
| Ban list omitted or generic — run returns "reduced to open problem X" or "holds for the planar case" | Enumerate this problem's specific non-counting results and forbidden reductions |
| Comfortable PARTIAL verdict offered — solver exits early into it | Partial output is allowed only after the effort floor, and must be labeled NOT A RESOLUTION |
| Auditors told to "check" or "review" | Auditors must be told to REFUTE, with the specific clause-5 failure modes to hunt |
| Accepting a mid-run summary or self-reported score as the result | Only the external verification gate settles; everything else is ledger material |
| Definitions skipped because "the problem is famous" | Famous problems have famous edge cases (multigraphs, loops, the empty family); define them anyway |

## Honesty invariant

Clause 3 is aggressive; clause 7 is what keeps it honest. "Assume a resolution exists" may never leak into the verdict: every claim in the final artifact is tagged verified-by-gate or it does not support settlement. If your project has an honest-admission protocol, the contract's exit clause must cite it.
