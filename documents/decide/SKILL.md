---
name: design-decide
description: Facilitates the Decide movement of a Tutti design session. Use after the Domain movement to record the alternatives considered, the chosen shape and why it beat them, the risks it carries, and the open questions still live (the core of a design doc or ADR). Asks one question at a time, may invoke the sequence diagram skill when the chosen flow reads better as a picture, and emits the movement artifact section once the alternatives, the choice, the risks, and the open questions are covered.
---

# Decide movement

Make the call and record why. The guiding question is: what are we building, and why this shape
over the alternatives? This is the core of a design doc or ADR: a choice is only as good as the
alternatives it was weighed against, so a decision with no rejected options is a red flag.

## What to cover

- **Alternatives considered**: the real options, including the one you rejected and why.
- **Choice made**: the shape you are committing to, stated plainly.
- **Risks named**: what could go wrong with the chosen shape, not with the rejected ones.
- **Open questions listed**: what is still unresolved and who or what will resolve it.

## How to facilitate

Ask ONE question at a time. Draw out the alternatives first (a choice with only one option is
not a decision), then the reason this one wins, then press on the risks the chosen shape brings,
then capture the open questions. Go deeper on a trade-off the human is waving away.

## Diagrams

When the chosen shape's flow of calls or messages reads better as a picture, invoke the
`sequence` diagram skill and embed its inline SVG in the artifact section.

## When you are done

Once the alternatives, the choice, the risks, and the open questions are covered, emit the
tagged complete reply with the artifact section as markdown: a `## Decide` heading, the
alternatives considered, the choice and its rationale, the risks, and the open questions.
