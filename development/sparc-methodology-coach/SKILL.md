---
name: sparc-methodology-coach
description: >-
  Guide structured development through 5 phases — Specification, Pseudocode,
  Architecture, Refinement (TDD), and Completion — with explicit time budgets per
  phase and a mandatory 6-persona staff-level audit loop at Completion that evaluates
  systemic risk, blast radius, and architectural coherence before any ship gate.
  Use whenever someone asks to build a feature, module, or system that benefits from
  structured thinking before coding. Triggers on: build this properly, spec this out,
  SPARC, TDD, test-driven, write tests first, spec before code, pseudocode this,
  architecture before coding, structured development, I keep rewriting this, this got
  messy, acceptance criteria, Given When Then, Red Green Refactor, time budget,
  phase-gated, completion checklist. Works standalone or activates inside
  staff-engineer-v4 Implement phase for STANDARD or FULL scope tasks.
  Do NOT trigger on quick fixes, patches, single-function tweaks, or LITE-scope tasks.
metadata:
  version: "1.0.0"
---

# SPARC Methodology Coach

<essential_principles>

1. **Coding before thinking is the most expensive mistake in software.** SPARC enforces structured phases that catch 80% of bugs before production and eliminate rework from unclear requirements or premature architecture.

2. **The 5 phases nest inside staff-engineer-v4.** Staff-engineer-v4 decides *what* to build (scope, stack, file plan). SPARC decides *how to build each piece* (spec → algorithm → structure → tests → ship). They layer naturally: staff-engineer-v4 Step 4 (Implement) → SPARC activates per feature.

3. **Time budgets are guardrails, not rituals.** S: 20% / P: 15% / A: 20% / R: 35% / C: 10%. They prevent two failure modes: over-planning (60%+ in S/P/A, 30% left for code) and under-specifying (80%+ in R/C, making it up as you go).

4. **The audit loop at Completion is a ship gate.** P0 findings block the feature. No exceptions. The audit runs even when the user says "just build it" — they opted out of ceremony, not out of quality.

5. **"Just build it" is valid.** Compress S and P into a brief internal plan (don't show it). Proceed to Architecture → TDD → Completion + Audit. Respect the request, preserve the quality.

</essential_principles>

<intake>

**Activate when:**
- New feature, module, API endpoint, or system component
- Anything >30 minutes to build
- Explicit TDD / spec-first / structured development request
- Inside staff-engineer-v4 STANDARD or FULL scope Implement phase
- User says "I keep rewriting this" or "this got messy"

**Do NOT activate when:**
- LITE scope / quick fix / patch
- Single function under 30 lines with no novel logic
- Bug fix where the problem is already identified
- Refactoring without design change (rename, extract, simplify)
- User says "just do it" or "skip the ceremony" — still run, but compress S and P

**Time budget by task estimate:**

| Estimate | S (20%) | P (15%) | A (20%) | R (35%) | C (10%) |
|---|---|---|---|---|---|
| 2 hours | 25 min | 18 min | 25 min | 42 min | 12 min |
| 8 hours | 1.6h | 1.2h | 1.6h | 2.8h | 0.8h |
| 1 day | 1.6h | 1.2h | 1.6h | 2.8h | 0.8h |

</intake>

<routing>

Route to the appropriate workflow for each phase:

| Phase | Workflow | When to Load |
|---|---|---|
| S: Specification | `workflows/specification.md` | Start of every SPARC activation |
| P: Pseudocode | `workflows/pseudocode.md` | After Spec approved |
| A: Architecture | `workflows/architecture.md` | After Pseudocode complete |
| R: Refinement (TDD) | `workflows/refinement-tdd.md` | After Architecture locked |
| C: Completion + Audit | `workflows/completion-audit.md` | After all tests pass |

**Load each workflow file as you enter that phase. Do not pre-load all phases.**

</routing>

<reference_index>

| Reference | Purpose |
|-----------|---------|
| `references/patterns.md` | Pseudocode examples, TDD cycle patterns, decisions log format, SPARC + staff-engineer-v4 integration map |

</reference_index>

<workflows_index>

| Workflow | Purpose |
|----------|---------|
| `workflows/specification.md` | Phase S — testable requirements, acceptance criteria, unknowns |
| `workflows/pseudocode.md` | Phase P — algorithm design in structured English before any syntax |
| `workflows/architecture.md` | Phase A — components, data flow, integration points, security |
| `workflows/refinement-tdd.md` | Phase R — Red → Green → Refactor TDD cycle |
| `workflows/completion-audit.md` | Phase C — completion checklist + 6-persona staff audit loop |

</workflows_index>
