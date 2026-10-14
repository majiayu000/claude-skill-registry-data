---
name: usm
description: "Trigger: USM, user story map, story map, mapa de historias, MVP slice. Create journey-first story maps with MVP slicing and Mermaid output."
license: MIT
metadata:
  author: andresnator
  status: testing
  version: "2.0.0"
---

# User Story Mapping

## Activation Contract

Use this skill to interactively create a User Story Map for a raw idea, PRD, PRD Light, RFC, issue, notes, or other product context. Raw ideas are first-class input. Existing artifacts are initial context only; validate the story map structure through the interview.

Always read `assets/usm-template.md` at the start of the session and use it as the final artifact skeleton.

## Hard Rules

- Ask one focused question at a time, then stop and wait for the user's answer.
- Ask open-ended questions directly in normal chat; use the `question` tool only for a closed confirmation or enumerated choice.
- Add `Recommendation: ...` only when it helps the user respond. Do not add question headings, numbering, rationale blocks, or interview-length estimates.
- Use one adaptive-depth flow: ask more when context is thin, and move faster when strong PRD, RFC, issue, or notes are provided.
- With strong source input, summarize and confirm instead of re-asking already answered questions, but still validate every structural minimum in Closure Criteria.
- Show partial summaries at phase boundaries, not after every question.
- Do not produce the final Markdown or Mermaid until Closure Criteria are met, even if the user says "generate now".
- Block only on structural gaps; use clearly marked assumptions for minor unknowns.
- Build the story map journey-first, not feature-first; add the User Journey Map as discovery/context, not as a replacement for the story map.
- Treat phases/activities as high-level journey stages, not UI screens or implementation steps; capture actions as narrative user actions, not click-by-click logs.
- If the user gives features, ask where each feature lives in the user journey before accepting it into the map.
- Do not accept a flat feature list as the map structure.
- Map cards are concise user tasks, not full `As a/I want/so that` stories.
- Candidate stories are optional output only when explicitly useful or requested; they are never required for validation.
- Support multiple actors, but require one Primary Actor. Treat secondary actors as variants, constraints, or important perspectives.
- Use one point of view per User Journey Map: one Primary Actor in one scenario.
- Mark the User Journey Map as current-state, future-state, or hypothesis. If evidence is thin, label assumptions clearly.
- Require an MVP Slice as the first end-to-end walking skeleton. Later release slices are optional, but when present they must also be vertical journey slices, not scope buckets.
- Replace every visible template label before final output, including Mermaid labels like `{Activity 1}` or `{MVP task from Activity 1}`; structural node IDs may remain.
- Default to print-only output. Do not save files unless the user explicitly asks.
- If saving is requested, suggest `docs/usm/{product-or-feature-name}-usm.md` and wait for confirmation before writing.
- Use the conversation language for the final artifact unless the user explicitly asks for another language.

## Conversation Format

Use this minimal shape for open interview questions:

```markdown
[Direct question]

Recommendation: [short recommended/default answer when useful]
```

Omit the recommendation line when it adds no value.

## Decision Gates

| Situation | Action |
| --- | --- |
| Missing product or feature goal | Ask what outcome the story map should support. |
| Missing Primary Actor | Stop and ask which actor is the primary journey owner. |
| Multiple actors compete for priority | Ask which actor anchors the map; record others as secondary actors. |
| Missing scenario | Ask what scenario the Primary Actor is in. |
| Missing expectations after scenario is known | Ask what the Primary Actor expects to accomplish or experience. |
| Missing journey evidence or state | Ask whether the journey is current-state, future-state, or hypothesis, and what evidence or assumptions support it. |
| Input is a feature list | Ask where each feature belongs in the user journey before mapping tasks. |
| Journey has fewer than 3 activities | Ask for the before, during, and after high-level journey stages until at least 3 activities exist. |
| Activities have no user tasks | Ask what the Primary Actor does under each activity. |
| MVP Slice is missing | Stop and ask which tasks form the first end-to-end walking skeleton. |
| User asks to generate early | Explain that minimum structure is incomplete, ask the next blocking question, then wait. |
| Minor detail is unknown | Mark it as an assumption, risk, or open question and continue. |

## Execution Phases

1. Intake: identify the product or feature, available context, artifact language, and whether the user expects print-only output or explicitly wants a saved file; ask only one missing item at a time.
2. Goal and Actors: capture the goal, Primary Actor, and secondary actors or variants.
3. Scenario and Evidence: capture scenario first, then expectations only if still missing; then capture journey state, source evidence, and assumptions.
4. Journey Backbone: define at least 3 sequential high-level phases/activities from start to finish, not screens or implementation steps.
5. Journey Context: capture phase-level narrative actions, mindsets or emotions, pain points, and opportunities.
6. User Tasks: capture concise user tasks under each main activity.
7. Slice Planning: select the mandatory MVP Slice as the first end-to-end walking skeleton; add later vertical journey slices only when useful.
8. Review: walk the map left-to-right as the Primary Actor's story to find missing steps, then briefly review open questions, risks, assumptions, and structural completeness.
9. Closure: generate one final Markdown artifact using `assets/usm-template.md`, with Mermaid embedded inline.

At each phase boundary, provide a compact summary and ask the next phase's first question.

## Closure Criteria

- Goal is explicit and outcome-oriented.
- One Primary Actor is named.
- Secondary actors, if any, are marked as variants or constraints.
- User Journey Map is explicit and includes actor, scenario, expectations, journey state, high-level phases, narrative actions, mindsets or emotions, opportunities, and evidence or assumptions.
- Journey state is marked as current-state, future-state, or hypothesis.
- User Journey has at least 3 activities in sequence.
- Each main activity has user tasks beneath it.
- User tasks are concise actions, not full user stories or implementation tasks.
- MVP Slice includes at least one meaningful task from each critical part of the journey and can be understood as the first end-to-end walking skeleton.
- Open Questions, Risks, and Assumptions are briefly reviewed before final output.
- Final output includes Open Questions, Risks, Assumptions, and Next Steps sections.

## Output Contract

Return exactly one complete Markdown artifact in chat or CLI by default. Embed Mermaid inline in the artifact.

The primary diagram must be a Mermaid `flowchart LR` using subgraphs for activities. Stack tasks top-to-bottom inside each activity. Use class definitions or colors to distinguish MVP from later releases. Add an optional Mermaid `journey` diagram only when it is useful and enough phase/emotion data exists; never use it as the full User Journey Map because the table carries the required context.

For Later Release Slices, output either a table of vertical journey slices or `None planned yet; defer until MVP learning is reviewed.`

The final artifact must include:

- Title and metadata.
- Goal and context.
- Actors.
- User Journey Map.
- User Journey Backbone.
- User Tasks by Activity.
- Slice Plan with mandatory MVP Slice.
- Mermaid Story Map using `flowchart LR`.
- Open Questions.
- Risks.
- Assumptions.
- Next Steps that suggest converting the MVP Slice to issues without creating issues automatically.

Replace every `{...}` placeholder with artifact content before returning the final artifact. Never leave placeholder rows, unused optional sections, template guidance, or instructional notes in the final artifact. Use `TBD` only for intentionally skipped non-blocking details.

## References

- `assets/usm-template.md` — User Story Map output template.
