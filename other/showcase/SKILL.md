---
name: showcase
description: Compose and publish a visual explanation of how something works — captures, diagrams, and prose on one page.
argument-hint: "[subject]"
disable-model-invocation: true
---

The deliverable is a **narrative**: a sequence of points, each in the medium that proves it — a text shape for _how it's built_, a diagram for _how it flows_, a capture for _what you see_. Every visual is a **proof**: the smallest view that makes its point, and nothing else. Pitch it at product and architecture; descend into code only when code is the subject.

This skill decides what goes on the page. `/to-artifact` composes and publishes it, and the **brief** of step 4 is the handover. A medium the user asked for by name wins over every default below.

## 1. Fix the subject

Take it from the first source that has one: what the invocation names; the subject under discussion this session; a PR or issue the user linked. If every source is empty, ask.

Done when the subject is one written line.

## 2. Scope the points

Derive the list of points the page will cover, and the **ordering** that carries them. The ordering follows the subject. These recur often enough to start from:

**Feature walkthrough** — lead with what the feature does, and descend toward how it's built only at the end, if at all. What it is, as the job it does for whom. The journey, step by step, one capture per step. How it flows, as one diagram naming the real screens and states. Where it lives, as the entry points in file references.

**Architecture overview** — the shape, naming the parts and the job of the whole. The flow, as a data-flow or sequence diagram of the main path. Part by part: each part's job, inputs, outputs, and entry point. The edges, where the system touches the outside, and what crosses each one.

**Bug anatomy** — past tense for the bug, present tense for the fix. The symptom the user saw, as a repro storyboard when the bug is visible on screen. The mechanism: the failing path, its real states, and the branch where behaviour diverged. The fix, as prose with linked code references. The proof: the same flow, after.

When more than one ordering fits the subject, ask once (`AskUserQuestion`, multiSelect) with concrete candidates drawn from the subject. When one is obvious, skip the ask. Either way this is the last question about what to cover.

Done when you hold the points in order.

## 3. Gather the media

**Shapes** — pick the one that proves each point. Pseudocode for logic where the branches matter and the syntax doesn't. A call tree for runtime control flow, what calls what in order. A component tree for UI structure, carrying the state and module boundaries that matter. A file tree for file responsibility or the shape of a broad refactor, one line of purpose per entry. A diff for what changes when the surrounding shape already exists, matching the diff's shape to the topic — a component tree for a UI change, a call tree for a call-order change. A diagram for component interaction, data flow, and state machines, drawn per `/artifact-diagramming`: real states, real names, real branch conditions, arrows labeled with what moves.

**Captures** — when the subject renders, captures carry the journey. A diagram standing in for screens the app could have shown is a defect.

Invoke `/run` to get the app serving, then drive the flow from that URL, preferring a sub-agent per flow: flows run in parallel and the logs stay out of your context. Take one capture per step, in sequence, and note for each what the user just did and what changed on screen. Captures land as files on disk and reach the page as supporting files, so the pixels stay out of your context too. Resize and compress each one before it ships.

When a planned capture can't be produced — the app won't launch, or the flow won't drive — stop and ask, offering the page without captures as one option.

**Research** — this session's own context is the first source. Past it, the scope decides: invoke `/how` for a point that needs mechanism, `/why` for a point that needs motivation. A UI journey usually needs neither. Both run wide (`/how` dispatches an explorer per angle, `/why` an investigator per source and then a synthesizer), so fire them for a point that needs them.

Done when every point has its medium in hand.

## 4. Brief and publish

Write the **brief** to the scratchpad, as the one document that settles what `/to-artifact` builds:

```md
# Brief: <subject>

The subject, points, and media below are settled. Take them as given, and start at framing the reader's job.

## Subject

<one line>

## Points

1. <what this point proves> — capture — `shots/01-signin.png`
2. <what this point proves> — sequence diagram
3. <what this point proves> — prose with file references

## Media

Publish these as supporting files:

- `shots/01-signin.png` — <what it shows, and what the reader just did>
```

Dispatch a fresh agent to invoke `/to-artifact` with the brief's path. The brief is the whole of its context.

Done when the user holds the link.
