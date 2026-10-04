---
name: cineops-screenplay-diagnostics
description: Diagnose screenplays and scenes for causality, character intention, value change, visual action, rhythm, and AI-production feasibility. Use before shot planning, when a scene feels flat or confusing, or when revising a script without losing its intended voice.
---

# CineOps Screenplay Diagnostics

## Purpose

Find the few defects that most affect audience comprehension and downstream production. Diagnose before rewriting. Preserve the author's premise, tone, and approved facts unless asked to develop alternatives.

Read `references/diagnostic-rubric.md` for scoring definitions. Use `assets/diagnostic-report.template.md` for a formal review.

## Diagnose

1. Establish scope, format, target runtime, audience, and the author's stated intention.
2. Summarize the causal chain using observable events: because A happens, the character does B, which causes C.
3. For each scene, identify entry value, character objective, obstacle, tactic, turning action, exit value, and new question.
4. Mark information that is spoken but should be dramatized, action that cannot be seen, motivation inferred without evidence, and spectacle without consequence.
5. Test producibility: stable identities, manageable locations, readable staging, feasible transformation beats, and shots that a generation system can distinguish.
6. Rank findings by downstream cost.

## Severity

- `blocker`: the scene cannot be understood or planned reliably.
- `major`: the scene works in outline but likely produces weak performance, pacing, or continuity.
- `minor`: a localized improvement that does not invalidate later work.
- `note`: an option, not a defect.

Every finding must cite a scene, line, beat, or concrete symptom. Explain the consequence. Avoid generic advice such as "raise the stakes" without naming the action that should change.

## Revise Safely

When revision is requested:

1. State the diagnosis being addressed.
2. Offer the minimum viable change first.
3. Preserve unaffected dialogue and beats.
4. Mark any new canon as proposed, not approved.
5. Re-run the causal chain and runtime estimate after editing.

## Exit Criteria

A scene is ready for shot planning when its objective and obstacle are playable, the turn is visible, the exit state differs meaningfully from the entry state, required exposition has a dramatic carrier, and no blocker remains.

Return a compact verdict, prioritized findings, protected strengths, revision plan, and unresolved decisions. Do not create a shot list unless explicitly asked; hand that stage to `$cineops-shot-planning`.
