---
name: audit-arch
description: >-
  Macro-scale architectural audit. Finds structural conflicts — patterns whose replacement would simplify the whole system — judged against the language, the runtime environment, and the project's OWN stated ambitions, never against ambitions it doesn't have. Optional argument shifts the auditor's archetype (e.g. "scaling up" → scale-invested architect).
  <triggers>
    /audit-arch, architecture audit, structural audit, macro audit, audit the architecture, big-picture review, architectural conflicts
  </triggers>
---

# Architecture Audit

```
/audit-arch                      # whole repo, fitness judged from evidence
/audit-arch src/engine           # scoped target
/audit-arch scaling up           # adopt the scale-invested archetype
/audit-arch soft-realtime game   # adopt the frame-budget archetype
```

## Contract

One sentence you must be able to complete for every finding you report:

> "Replacing **{current structure}** with **{simpler structure}** would let us **delete {concrete things}**, because in **{language/runtime}** the idiomatic shape for this problem is **{pattern}**."

If you cannot fill every slot with evidence (file:line), the finding does not exist.

## Prohibitions — read before auditing, these are where audits go wrong

1. **Never audit against an unsignaled quality dimension — any dimension.** Every quality axis a criterion could invoke (scalability, portability, extensibility, multi-tenancy, i18n, security hardening beyond the threat model, performance beyond observed need, configurability, cross-platform, offline mode, …) is in scope ONLY if the project signaled it — in docs, the skill argument, config, dependencies, or the user's words. This list is illustrative, not exhaustive: the rule is that the *dimension itself* needs a signal before any finding on it exists. Before writing a finding, name the dimension it judges against and cite its signal; no signal → the finding is deleted, not softened. Absence of every signal means one bar remains: fitness and simplicity for what the code demonstrably does today.
2. **Never report micro findings.** Naming, single-function complexity, missing null checks, one file's style — out of scope. If the fix touches fewer than ~3 modules or deletes nothing, it belongs to a code review, not this audit.
3. **Never propose an abstraction that adds a layer without deleting two.** Every recommendation must net-reduce: fewer moving parts, fewer places a change lands, fewer facts a new contributor must learn.
4. **Never infer architecture from names.** `EventBus.cs` is not evidence of pub/sub; `Cache` is not evidence of caching. Read the call sites. A finding cites how data/control actually flows, with file:line.
5. **Never bundle.** One structural conflict per finding, findings independent, ranked by leverage × centrality (Step 1c), not by severity theater.
6. **Never let "bad" outrank "unimportant-but-bad."** Importance comes from the project's ethos, not from how wrong the code is. A textbook-poor pattern in a subsystem the project barely cares about (e.g. clumsy multiplayer plumbing in a primarily single-player game) is at most a footnote; the audit's headline findings live where the project's point lives.

## Step 1 — Establish fitness scope

Before reading code, fix the yardstick. Two inputs:

**a. Declared intent** (overrides everything): the skill argument, plus `README`/`docs/`/`CLAUDE.md`/ADRs. If the arg names an ambition ("scaling up", "plugin ecosystem", "mobile port"), adopt the matching archetype:

| Argument signals… | Audit as… | Which adds criteria like… |
|---|---|---|
| scale / load / users | Scale-invested architect | contention points, O(n) fan-outs, sync-over-async seams |
| realtime / game / frame | Frame-budget architect | per-frame allocation, poll-vs-event, update-order coupling |
| team growth / onboarding | Legibility architect | module count a newcomer must hold, hidden coupling |
| plugins / extensibility | Seam architect | closed enums vs registries, hardcoded dispatch |
| (no argument) | Resident senior engineer | idiomatic fitness for what the code demonstrably does today |

**b. Demonstrated intent**: what the code is actually shaped to do — a single-process desktop game, a CLI, a service. The demonstrated shape sets the default bar.

**c. Ethos — the importance modifier.** Beyond what the project *does*, articulate what it *cares about*: the philosophy, the point, the thing that would make its author say "this is why the project exists" (e.g. a single-player systemic sim cares about simulation fidelity and feel; a data pipeline cares about correctness and replayability; a prototyping tool cares about iteration speed). Every subsystem then has a **centrality**: core (embodies the ethos), supporting (serves it), peripheral (incidental to it). Centrality scales importance for the rest of the audit — a genuinely poor architecture in a peripheral subsystem is still poor, but it is not *important*, and this audit reports what's important. A moderate conflict in the core loop outranks a severe one in a corner the ethos doesn't care about; if the top-5 cut must drop something, peripheral findings go first, noted in one line under "Explicitly not flagged."

State the scope in one line before proceeding:

> Auditing as: {archetype}. Fitness bar: {what this system is for}. Ethos: {what it cares about most} — core subsystems: {list}.

## Step 2 — Map the macro structure (dispatch, don't wander)

First tool call is an Explore/investigate dispatch, not direct reads. The brief:

- Identify the top ~10 modules by fan-in/fan-out and the direction of every major dependency between them.
- Trace the three dominant flows end to end (e.g. input→state→render; request→domain→persistence; tick→simulation→UI).
- For each flow, record the *coordination mechanism* at every hop: direct call, poll, shared mutable state, event, message, callback, singleton reach-around.
- Note where the same fact is stored/derived in more than one place.

The coordination-mechanism list is the raw material: most macro conflicts are a mechanism mismatched to its hop.

## Step 3 — Detect structural conflicts

For each hop/cluster, ask the conflict questions. These are shape-level, and each carries its own don't-flag guard:

| Conflict | Flag when | Do NOT flag when |
|---|---|---|
| **Poll where push belongs** | N consumers re-derive/re-check state every tick that changes rarely, and producers know when it changes | the poll IS the domain (a game update loop), or N=1 and it's cheap |
| **Push where poll belongs** | event cascades re-implement "current state" via replay/flags | events genuinely model one-shot facts |
| **Shared mutable state as API** | modules communicate by writing fields other modules read on a timer | it's a deliberate blackboard/ECS with a single owner |
| **Layer inversion** | low-level module knows high-level types (engine imports UI, domain imports transport) | the "layer" is aspirational, not declared or needed |
| **Duplicated source of truth** | the same fact is computed/stored in ≥2 places that can disagree | one is a documented cache with an owner and invalidation |
| **God orchestrator** | one module's edit-frequency and fan-out dwarf all others; every feature lands there | it's a thin composition root that only wires |
| **Framework fought, not used** | hand-rolled machinery duplicating what the runtime/framework provides idiomatically (e.g. manual change-detection beside an ECS; hand-rolled async beside Tasks) | the hand-rolled version exists for a measured, documented reason |
| **Config/flag switchboard** | booleans threaded through many layers select behavior that a seam (interface + two adapters) would isolate | two flags, one consumer — leave it |
| **Ambition mismatch** *(archetype-gated)* | declared ambition (Step 1a) is structurally blocked — e.g. "scaling up" + in-memory singletons holding session state | no such ambition was declared |

Verify each suspect with the **deletion test** (from /improve-codebase-architecture): imagine the current mechanism gone, replaced by the simpler shape. List what concretely gets deleted. Nothing deletable → not a finding.

## Step 4 — Report

Rank by **leverage × centrality**: how much of the system simplifies, scaled by how close the finding sits to the project's ethos (Step 1c). Severity alone never promotes a peripheral finding over a core one. Maximum 5 findings — a macro audit that reports 20 things has reported nothing. Format each exactly like this:

```
### {n}. {Current shape} → {Proposed shape}

**Where:** {files/modules, with the 2–3 most load-bearing file:line cites}
**Current flow:** {2–3 sentences: how data/control moves today, mechanism named}
**Conflict:** {which conflict from Step 3, and why the guard column doesn't save it}
**Simpler architecture:** {the target shape in plain language — no interfaces, no code; name the idiomatic pattern for this language/runtime}
**Deletion test:** {the concrete list of code/concepts/sync-points that disappear}
**Cost honesty:** {what the migration touches; what new risk it introduces}
```

Close with:

```
**Fitness bar used:** {restated from Step 1}
**Explicitly not flagged:** {1–3 things a generic audit would flag that this fitness bar excuses — and why. This line is mandatory; it proves the bar was applied.}
```

Findings only. Do not implement anything. If the user picks a finding to pursue, hand off to /improve-codebase-architecture for the grilling loop and interface design — this skill decides *what* conflicts exist, that one decides *how* the replacement gets shaped.
