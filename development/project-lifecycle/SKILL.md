---
name: project-lifecycle
description: "Run a software project across its full lifecycle — define, design, build, verify, operate, maintain. Use whenever someone is starting or scaffolding a new codebase, deciding how it will be structured and run, laying a foundation, maintaining a shipped one, tightening or cleaning one up, deciding which files stay or go, taking over an unfamiliar codebase, or planning how the work should run start to finish — even if no phase is named. Built on the Expert Standard Development Methodology: every recommendation traces to the named standard that governs its phase, every factual claim about a codebase is verified against that codebase before it drives a decision, and every phase produces evidence — not just a process that ran. Not generic project-management folklore."
---

# Project Lifecycle

## What this is

A working guide for running a software project across its whole life, organized around a six-phase lifecycle. It applies the **Expert Standard Development Methodology** — which adapts ISO/IEC/IEEE 12207's software life cycle processes for execution against named standards — and holds every decision to that methodology's two standards of proof.

This SKILL.md is deliberately light. The depth lives in `references/`, one file per phase plus the cross-cutting concerns and the hard situations. **Don't read all of them.** Read the index below, find the phase or situation the current work belongs to, and open the one or two references that match. Each reference names the standards that govern its phase and gives the concrete moves.

The word "project" here means *the codebase you are working on* — the thing being defined, built, or maintained. It never means this skill or the library it ships in.

## Starting points — two ways in

Two situations bring you here, and they begin differently. Figure out which one you're in before anything else.

**A new codebase, from nothing (greenfield).** Enter at Define and move forward. The spec constrains the design, the design constrains the build, each handoff passes its gate. Open `references/phase-define.md` and go.

**An existing repo you want to bring into conformance (brownfield).** The common case — and it does *not* mean retroactively running six phases or rewriting anything. In short: survey the repo from current source, map its gaps against the six phases, prioritize those gaps by risk, and backfill them one slice at a time without breaking what works. That is its own path with its own standards and procedure — open `references/adopting-on-an-existing-repo.md` and start there, not in the phase files.

The phase references below are what each step in either path actually does.

## The framework: six phases

The lifecycle runs in six phases. Each names the standards that govern it, produces an output contract, and passes a binary quality gate at its handoff:

1. **Define** — problem → requirements. Governed by ISO/IEC/IEEE 29148 (requirements quality) and a source test on every requirement.
2. **Design** — requirements → architecture. Governed by SOLID, REST conventions (RFC 7231 / 7232 / 7807), OWASP ASVS and Threat Modeling, and ISO/IEC 25010 quality characteristics.
3. **Build** — architecture → implementation. "Correct" means against the standards the design was built on, with verification evidence for the libraries and contracts the code depends on.
4. **Verify** — confirm the build is right (against the architecture) *and* is the right thing (against the spec). Governed by structured standards-based review, OWASP ASVS, and the performance requirements from the spec.
5. **Operate** — transition to and run in production. Governed by SRE principles, operational-readiness standards, and the four golden signals.
6. **Maintain** — evolve a running system safely. Governed by change management, dependency management (SemVer, security advisories), Fowler's refactoring discipline, documentation currency, and the architecture document as the governing contract.

Five **cross-cutting concerns** run across all six phases rather than being phases themselves: memory and continuity across sessions, project tracking, quality gates, standards compliance, and how tools compose.

A practical task rarely sits in one phase. Standing up a new codebase spans Define, Design, Build, and the continuity and tracking concerns; a cleanup lives mostly in Maintain. The index maps the task to the phase or phases that govern it.

## The two axes — the core discipline

Everything below rests on two axes. They apply in every phase, in every reference.

**Frame each decision against the named standard, not against what's familiar.** Before choosing a structure, a branching model, a documentation layout, a cleanup action — name the standard that governs that decision and decide against *it*. The nearest available reference (the last repo, a layout that "looks clean," what the existing code already does) is the default comparison target, which is exactly why it's dangerous: it may be wrong, or wrong here. If you can't name the standard or the genuine constraint behind a choice, you're pattern-matching — say so rather than presenting the guess as grounded.

**Verify each claim about the codebase against the codebase, before the claim drives an action.** "This file is unused," "nothing imports this," "the tests pass," "this is already documented," "this dependency isn't needed" — each is a factual claim, and each is routinely wrong when stated from memory or impression. Verifying it means reading the actual code and reasoning about what it does, running the actual test, or reproducing the actual behavior — before it justifies an action, *especially* a deletion or a merge. A search (grep, a dependency graph) is a lead that tells you where to look; it is not the verification, and a clean result is evidence, not proof. A claim carried in from a prior session or an earlier read is a candidate to re-verify, not an established fact.

A note on the tools, because they are easy to mistake for verification. Search (grep) and structure tools (a dependency or call graph) produce *leads and evidence* — they tell you where to look and narrow the space. Neither proves anything by itself, and absence is the trap: a clean grep and an empty importer list are both evidence that nothing references X, never proof, because neither can see dynamic dispatch, reflection, string-keyed lookups, config and DI wiring, generated code, or callers outside the repo. Getting from that evidence to a verified claim means reading the candidate sites, reasoning explicitly about each of those non-static paths, and — for any claim about behavior — running or reproducing it. "Appears unused" is a hypothesis to check by reading, not a fact a search can establish.

## How decisions get proven — output contracts and gates

The methodology's defining requirement is that rigor is **visible in the output**, not merely performed in your head — the failure it exists to prevent is a process that ran without leaving proof it ran soundly. So:

- Each phase produces **evidence** as part of its deliverable: the standards it named, the source tracing on each significant decision, the verification behind each factual claim (a read of `file:line` with the reasoning, a run or reproduction for a behavioral claim, a documentation source with version — a search result is a lead toward this, not the verification itself — or an explicit "tentative — unverified" marker), the judgment calls made, and the gaps left open.
- Each phase transition passes a **binary quality gate**: does the output *contain* the evidence its contract requires? Not "does it look done." A gate that passes despite missing evidence is the hole that lets bad work ship downstream, where it costs more to fix.

Each reference states what its phase's output contract requires.

## The four ways this goes wrong

Four failure signals. Watch for them in your own work:

- **Unnamed approvals** — "clean structure," "well-organized repo," "solid plan," with no standard behind the judgment. If the approval would read identically regardless of quality, it isn't an assessment.
- **Silent pattern replication** — scaffolding a new codebase by copying another repo's layout because it's there; adopting a branching model because the last codebase used it; importing a claim from a handoff without re-deriving it. The pattern may be right — adopt it because it's *justified here*, not because it's *present*.
- **Unverified premises** — acting on "dead / unused / covered / passing" without checking. This is the failure that turns a cleanup into an outage.
- **Assessment gaps** — declaring a codebase "cleaned up," "production-ready," or "done" when a real check (a deep review, a security review, an actual readiness gate) would still find problems. If a readiness claim matters, run the real check instead of asserting it.

## Index — which reference to open

| You are… | Phase(s) that govern it | Open |
|---|---|---|
| Starting / scaffolding a new codebase, laying its foundation, deciding how it will be run | Define + Design + Build, plus continuity and tracking | `references/phase-define.md`, `references/phase-design.md`, `references/phase-build.md`, `references/cross-cutting-concerns.md` |
| Turning a problem or idea into requirements; writing the charter or spec | Define | `references/phase-define.md` |
| Deciding architecture, structure, technology, API surface | Design | `references/phase-design.md` |
| Implementing, integrating, standing up tests and CI | Build | `references/phase-build.md` |
| Reviewing, auditing, or verifying that work is correct and complete | Verify | `references/phase-verify.md` |
| Deploying, monitoring, writing runbooks, handling incidents | Operate | `references/phase-operate.md` |
| Maintaining a shipped codebase; dependency upkeep; tightening, cleaning up, deciding what stays or goes; deprecating or disposing | Maintain | `references/phase-maintain.md` |
| Setting up a roadmap, decision log, tracking, or cross-session continuity; git and documentation conventions; how tools compose | Cross-cutting | `references/cross-cutting-concerns.md` |
| Adopting this on an existing repo; taking over an unfamiliar or broken codebase; working out of phase order | Survey and gap-map first, then the governing phase | `references/adopting-on-an-existing-repo.md` |

More than one row applies often. Standing up a new codebase pulls in the first four; a cleanup pulls in Maintain and the cross-cutting concerns.

## When the ask is "just set it up, skip the process"

Work gets started under pressure, and sometimes the ask is "just scaffold it" or "just clean it up, don't make a project of it." That's a legitimate call, and it's the user's to make. The discipline is to flag once and comply: name in a single sentence what's being skipped and what it risks, then proceed — and don't repeat the flag. Skipping the spec is fine for a throwaway; the risk it carries is that scope creep has nothing to check against later. Make the trade visible, then move.
