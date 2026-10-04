---
name: interaction-design
description: Use when designing interface states, feedback, hover/focus/press, gestures, direct manipulation, navigation transitions, loading/error/empty behavior, or deciding where interaction should carry the design concept.
metadata:
  short-description: Design states, feedback, gestures and signature interactions
---

# Interaction Design

## Start with state, not animation

For every interactive element define:
- trigger/input;
- state before;
- state after;
- feedback latency;
- reversal/cancel path;
- keyboard/touch alternative;
- loading/error/empty behavior if applicable.

## Motion-purpose taxonomy

Animation is justified when it improves at least one:
- feedback;
- orientation;
- continuity;
- hierarchy/attention;
- storytelling;
- brand personality.

If none apply, remove it.

## Motion budget

Per viewport, prefer:
- at most one dominant narrative motion moment;
- a small number of supporting transitions;
- micro-feedback where interaction occurs.

Do not animate every section entrance. Repetition destroys salience.

## Signature interaction

Design one interaction that expresses the brand or product concept. Make it optional to task completion and give it a reduced-motion equivalent.

## Accessibility

Never make hover the only way to discover essential content. Drag-only functionality requires a non-drag single-pointer alternative where required by the accessibility baseline.

For product flows, read `references/product-edge-cases.md` before release and cover the states that apply; a polished happy path is not a complete interaction model.
