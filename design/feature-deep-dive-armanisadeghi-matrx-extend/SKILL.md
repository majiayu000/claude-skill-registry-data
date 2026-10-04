---
name: feature-deep-dive
type: Skill
title: "feature-deep-dive — exhaustive audit, target vision, approved plan, complete build"
description: "Doctrine for auditing an ENTIRE feature and building it to its ideal state. Use on 'deep dive on X', 'audit the X feature', 'figure out everything X does', 'take over X and finish it', 'bring X up to best practices', or when a whole feature needs overhauling, unifying, or finishing, not patching. NOT for one small addition (use build-sub-feature)."
tags: [execution, features, audit, planning, doctrine]
timestamp: 2026-09-10T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/feature-deep-dive/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# Feature Deep-Dive: Audit, Plan & Build

Fully understand a feature, define what it should ideally become, get that plan approved, then build it — in full. No code changes before the plan is approved: enter plan mode at the start (if not already active), work Phases 1–5 to full depth, present the plan deliverable for approval, and begin Phase 6 only after approval. Your focus is: gather everything, decide what it should be, and make it real, completely. "Done" means every part implemented, tested, and confirmed working — never partially done.

Primary focus: frontend + backend. The database matters insofar as code reads and writes it — verify the code's assumptions about the schema are actually true.

**Out of scope, entirely:** authentication, authorization, and access scoping. A single application-layer model already handles this; never investigate, analyze, test, or report on it.

**Not this skill:** quick bug fixes, single-file edits, diff/PR reviews, or one small addition to an otherwise-untouched feature (that is `build-sub-feature`).

## Method: small, specialized subagents

Use MANY small, highly specialized subagents rather than a few broad ones — they're cheap. One subagent = one narrow question against named files. "Review the backend" is useless; "verify every error path in `uploadHandler.ts` returns a status the frontend handles" is useful.

Mechanics:
- Dispatch with the Agent tool. Use read-only `Explore` agents for fact-finding; use general-purpose agents only when a question needs full tooling.
- Launch independent subagents in parallel — multiple Agent calls in a single message.
- Give each subagent: the named files/directories, the one narrow question, and the required report shape — findings, severity, exact file/line refs, and a confidence label ("verified" / "strongly suspected" / "needs runtime verification").
- Spawn follow-ups recursively until the questions stop.

Work the phases in order. Each is completed with full depth before the next.

---

## Phase 1 — Fact-finding: what exists

Understand the real codebase before anything else, and dig through ALL of it — not just the obvious core. Scattered pieces live everywhere: scripts, demos, tests, prototypes, and artifacts from every era of the project. Some are *better* than the current main implementation. Everything found is in scope and must be understood.

Map it:
- Every UI entry point: pages, components, modals, buttons, shortcuts, context menus, background triggers.
- Each flow end to end: component → state → hook/service → network → handler → logic → db/storage/external → response → state → render.
- Every endpoint touched — real request/response shapes, not what the types claim.
- All state (client / server / cached / persisted / URL) and anywhere the same data lives twice.
- All side effects: writes, uploads, queues, webhooks, websocket events, jobs, cache invalidation.
- Capability catalog — including capabilities built but not surfaced or adopted.
- Suspected domain fragments elsewhere in the codebase (see Phase 4 → Feature Boundary).

Analyze it — dispatch subagents across these lenses:
- **Correctness & data integrity:** flows match what the UI promises; type/response/schema mismatches; lossy or mutating transforms; multi-step ops where step 2 fails after step 1 commits (rollback/retry/detection?).
- **Errors & failure modes:** silently swallowed errors; network/timeout/slow/offline behavior; each non-success status handled distinctly vs. a generic "error"; missing `await`s and fire-and-forget calls whose failures vanish.
- **Concurrency & state:** double-submit; stale closures/cache; out-of-order responses; same record edited from two sessions; optimistic updates that don't roll back; effect cleanup, listener/subscription leaks; server-side non-atomic read-modify-write, missing transactions/locks.
- **Edge cases:** empty / one / thousands of items; large/empty/whitespace/unicode/RTL/special chars; pagination off-by-ones; timezone/DST/serialization; new user vs. messy long-lived data; malformed data handled gracefully vs. corrupting state or crashing.
- **Performance & scale:** N+1s, missing indexes, unbounded queries; over-fetching, request waterfalls, missing parallelism; needless re-renders, missing virtualization, bundle weight; resource leaks; behavior at 100× data.
- **Code quality:** duplication (feeds canonicalization); convention violations; every TODO/FIXME/HACK; type holes (`any`, unsafe casts, ignored errors); stale or wrong comments/docs.
- **UX completeness:** loading/empty/error/success states; action feedback, disabled states, undo on destructive actions, confirmations; accessibility basics (keyboard, focus, labels, contrast); small-viewport behavior; consistency with sibling features.
- **Observability:** are failures logged with enough context to debug in production; are cost/usage/quota operations tracked; can a reported "it didn't work" be diagnosed from logs alone.

## Phase 2 — Intent: what it was meant to be

The original vision is usually bigger, more powerful, and more ambitious than what was built. Hunt for the evidence: docs left in the codebase, unfinished tasks, half-built flows, and structural hints — unused DB columns, dormant params, scaffolding with nothing behind it — that reveal a larger plan never carried out. These unfulfilled intentions are not out of scope; they are the richest source of meaningful improvement. **Wherever intended > built, that gap is a primary target.**

## Phase 3 — Best practices: the bar

Treat this as critical — not secondary, never underplayed. The standard is the discipline's world champion (`common-docs/policies/champions.md`: name it before you build, match it before you ship, beat it before you call it done). Research and apply best practices specific to the platform, language, architecture, and every relevant technical dimension. Find what's currently done well but not as well as it could be, and build toward the best achievable implementation. Never water an ambitious goal down to fit a mediocre template.

## Phase 4 — Synthesize & gap analysis: what it should be

Combine what exists, what was intended, and what best practices demand into one concrete target vision for the feature. Then run a gap analysis: where things stand vs. that vision, and what it takes to close the distance. The vision must resolve all of the following:

- **Feature boundary (among the highest-value work you can do).** A feature is a product/domain boundary — not a screen, workflow, or tool. It owns the canonical concepts, types, state, services, and reusable UI for its domain; surfaces (extractors, studios, viewers, editors, dashboards) consume and extend it. A top-level feature answers "what domain is this?" — never "which screen needed it first?" Teams routinely spin up a new "feature" per mode of interacting with one domain, fragmenting it into drifting siblings; assume that has happened here. Find every fragment, map each to its true domain, and form a unification plan: one canonical home, surfaces reorganized beneath or beside it as use-case layers. Move anything misplaced to its rightful owner and consume it from there. **Default to unification** — keep fragments separate only with explicit owner approval, or if the owner confirms the feature legitimately spans multiple domains.
- **Canonicalization.** One implementation of any unit — component, hook, utility, service, script, type, query — that everything else uses. Fix it once and the fix flows everywhere; a bug in it surfaces loudly, while a bug in a duplicate hides. Flag every duplicate or re-creation across every layer (frontend, Python, shared) and name which becomes canonical.
- **Integration, two-sided (encapsulation via a public facade).** Each module exposes a controlled public surface — a facade — that others consume, never reaching into its internals or hand-rolling their own integration. *Outward:* provide the interface other modules need, written and owned by this feature. *Inward:* stop doing the hard way what another module already exposes canonically.
- **Underexposed vs. legacy.** Under-used code is usually an unsurfaced opportunity, not legacy — treat it as an asset to surface, finish, or promote. Apply "legacy / dead / deprecated" ONLY when (a) the owner says so, or (b) Git history proves it was once active, then deliberately reduced under human direction, and is genuinely old. Otherwise call it "underexposed" or "status unclear — confirm with owner."

## Phase 5 — Ask vs. decide

Prune and ask per the `grilling` skill. Facts and best-practice-decidable forks never reach the owner: decide them and list them as "Decided — override by number". Only genuine gray areas enter the tree — pure preference, no established best practice, or app-specific knowledge you cannot derive from the code. Ask frontier rounds until the tree is empty. The plan's **Open Questions** section holds only what remains unasked, each item with the default that ships if skipped.

## Phase 5b — Attack the plan

Before presenting the plan deliverable, run `plan-attack` (REGRET + BUILDABILITY in parallel) and adjudicate. OWNER-ONLY findings join Open Questions. The plan carries the one-line attack record.

## Phase 6 — Implementation

Execute the approved plan completely. The task is not done when parts are done — it is done when every aspect is implemented, tested, and confirmed functional. Nothing is marked complete while any piece remains non-functional or untested.

## Phase 7 — Testing

Test everything you can yourself. For anything you cannot test independently, produce a dead-simple checklist for the project manager — each item stating: where to go, what to click or do, what is being tested, and what a passing result looks like. Simple enough to follow without interpretation. The PM reports pass/fail; you iterate as many times as needed. You own the entire process end to end, and the work is complete only when the final product is fully delivered, tested, and conforming to best practices.

---

## The plan deliverable (produced before Phase 6)

A complete, prioritized, exhaustive plan. Every finding appears — minor items drop to lower tiers, never to the trash. This is what goes for approval at the end of plan mode.

**Priority tiers:**
- **P0 — Broken:** bugs, data-integrity risks.
- **P1 — Significant:** failure modes, race conditions, missing error handling users will hit.
- **P2 — Improvements:** performance, UX gaps, canonicalization, feature-boundary unification, integration surfaces, surfacing underexposed capabilities, vision-gap features, risk-reducing refactors.
- **P3 — Polish:** code quality, true dead code, docs, consistency.

**Each item:** what's wrong/missing, exact file/line refs, why it matters, the fix (concrete: "add error handling" is not a fix), complexity (S/M/L), dependencies, confidence label.

ALWAYS use this structure:

```
# <Feature> — Deep-Dive Plan
## What's Working Well              ← preserve it
## Target Vision & Gap Analysis
## Feature Boundary & Unification   ← the domain · fragments found · the single bounded feature they collapse into · misplaced ownership to relocate
## Canonicalization & Integration   ← duplication to unify · facades to expose · canonical interfaces to consume
## Underexposed Capabilities        ← assets to surface, finish, or promote
## Findings
### P0 — Broken
### P1 — Significant
### P2 — Improvements
### P3 — Polish
## Open Questions                   ← only genuine gray areas, each with a best-guess default
## Recommended Sequencing           ← respects dependencies
```

## Ground rules

- Read the actual code. Names, comments, and types lie — verify against implementation.
- Code/schema disagreements and client/server disagreements ARE findings.
- Label each finding "verified," "strongly suspected," or "needs runtime verification."
- Don't stop at the first issue in a file; files with one bug usually have more.
- Don't call anything "legacy/dead/deprecated" unless it meets the strict two-condition test (Phase 4).
- Prefer one canonical implementation; treat duplication as a finding and a module's facade as the way others consume it.
- The same domain appearing as several "features" is a defect — default to a unification plan.
- Authentication, authorization, and access scoping are fully handled elsewhere and must not appear anywhere in your work.
