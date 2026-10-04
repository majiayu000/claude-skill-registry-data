---
name: dota-architecture
description: >
  Governs the system architecture of the Dota AI Coach project — layering,
  module boundaries, and dependency rules across GSI, computer vision,
  MatchState, feature engineering, recommendation engines, ML/ONNX
  training, and the WPF/WinUI overlay/voice UI. Use whenever adding a new
  project/module, wiring a new dependency between existing modules,
  deciding where a piece of logic belongs, reviewing whether a change
  crosses a layer boundary it shouldn't, or setting up a new .NET project
  in the solution. This is a structural gate, not a style guide — consult
  it before code ends up in the wrong layer, since that's expensive to
  undo later.
---

# Dota AI Coach Architecture

This project pulls from many different worlds — a live game feed, screen
pixels, ML models, historical match APIs, and a desktop UI — that all want
to bleed into each other if boundaries aren't enforced deliberately. This
skill exists because the failure mode isn't a crash, it's a slow one:
strategy logic creeping into the GSI layer, UI code reaching past the
recommendation layer straight into an external API, ML code accidentally
depending on WPF. Each individual instance looks harmless; the accumulation
makes the system untestable and impossible to reason about.

## System architecture

```
Dota GSI  ─┐
           ├─→ State Merger → MatchState → Feature Engine → Recommendation Engines
Computer   ─┘                                                        │
Vision                                                                ↓
                                                          Recommendation Orchestrator
                                                                       │
                                                                       ↓
                                                          Overlay / Voice (UI)

Historical APIs → Data Platform → Training → ONNX models
                                                  │
                                                  └──→ (consumed by) Recommendation Engines
```

Two source pipelines feed the live path (GSI and Computer Vision both
produce raw observations that the **State Merger** reconciles into one
canonical `MatchState`). A separate **offline pipeline** (Historical APIs
→ Data Platform → Training → ONNX models) produces trained models that
the live Recommendation Engines consume as an artifact — it does not run
live and does not call back into the live path.

See `references/layers.md` for what each stage owns and doesn't own, in
detail.

## The rules

These are the load-bearing constraints. Read `references/dependency-rules.md`
for the full reasoning and how to enforce each mechanically (project
references, analyzers, tests) — this is the summary:

1. **Domain must not depend on infrastructure.** Domain types
   (`MatchState`, features, recommendation logic) must not reference GSI
   transport types, CV/vision libraries, ONNX runtime specifics, or UI
   frameworks. Infrastructure adapts *to* the domain, never the reverse.
2. **GSI must not contain recommendation logic.** The GSI layer's job
   ends at producing normalized state/events. It must never rank items,
   suggest plays, or contain any Dota strategy judgment — see `dota-gsi`
   and `dota-domain` for the layering this enforces.
3. **Computer Vision must not contain Dota strategy.** CV's job is pixels
   → structured observations (e.g. "this HUD region shows item icon X").
   It must not decide whether that item is good, itemize a recommendation,
   or otherwise reason about the game — that's the Feature
   Engine/Recommendation Engines' job, using CV's output as an input.
4. **ML must not depend on WPF/WinUI.** Training code, feature
   extraction, and ONNX inference must be usable headless (console app,
   test project, CI) with zero reference to any UI framework assembly.
5. **UI must not call OpenDota (or any external API) directly.** All
   external data access goes through the Data Platform layer. UI consumes
   only the Recommendation Orchestrator's output.
6. **Recommendation engines consume normalized features, not raw state.**
   A recommendation engine's input is the Feature Engine's output, never
   `MatchState` directly and never raw GSI/CV data — see
   `references/layers.md` for why skipping the Feature Engine is a
   recurring temptation worth resisting.

## Using this skill

- **Adding a new module/project?** Work through
  `references/new-module-checklist.md` before writing code — it walks
  through which layer the module belongs in, what it may/may not
  reference, and what test coverage proves the boundary holds.
- **Not sure where a piece of logic belongs?** `references/layers.md`
  describes each stage's responsibility in enough detail to place most
  code confidently. If it still doesn't fit cleanly into one stage,
  that's a signal the logic may need to be split, not a signal to just
  pick the closest stage.
- **Reviewing a change that adds a new dependency between projects?**
  `references/dependency-rules.md` has the allowed dependency graph and
  how to check a proposed reference against it.
- **.NET project structure questions?** `references/dotnet-solution-structure.md`
  covers how this maps onto actual `.csproj`/solution layout for a
  local-first Windows application (WPF/WinUI shell, class-library layers,
  ONNX Runtime for inference, no ASP.NET/server dependency implied by
  "Data Platform").

## Relationship to other skills

This skill governs structural boundaries; it doesn't replace the
domain-specific skills that own the substance within each layer:
- `dota-gsi` — the GSI layer's internal design (payload parsing,
  MatchState normalization, fixtures).
- `dota-domain` — Dota strategic knowledge used by the Feature
  Engine/Recommendation Engines.
- `dota-fairplay` — what data may legitimately be used at all; a
  stricter, cross-cutting constraint that applies independent of which
  architectural layer a feature sits in.

A change can be architecturally correct (right layer, right
dependencies) and still be a FairPlay violation, or vice versa — check
both when relevant.
