---
name: discovery-map-journey
description: >
  Map the customer journey and opportunity landscape for a discovery theme as a
  diagram, exposing pains and opportunities before any solutioning. Use when the
  work needs a visual of the experience: phrasings like "map the customer
  journey", "draw a journey map", "where do users feel pain in this flow",
  "lay out the opportunity landscape", "visualise the as-is experience", "what
  are the stages and pain points", or when a Discovery/Spike needs its journey
  made navigable. Do NOT use to run or synthesise the research itself (that is
  discovery-synthesize-research), to frame the riskiest assumptions (that is
  discovery-upsert-hypothesis-canvas), to turn opportunities into stories or create
  tickets (that is elaboration-upsert-user-story), or to add links to an existing
  issue (that is governance-enrich-ticket).
---

# Discovery journey map

Owned by the **Analyst** persona (the journey/opportunity-mapping step). Invoked as `/discovery-map-journey`.

Map a discovery theme's customer journey, or its opportunity landscape, as a diagram so the
stages, actions, pains, and opportunities are visible **before** anyone proposes a solution. The
map is exploratory: it surfaces where the experience hurts and where value could be created, and
hands those findings to assumption-framing and upsert-user-story. It does not decide the fix.

## The anchor model (read before writing)

The diagram lives in a diagramming tool or board (drawio or a mermaid block in the repo). The
**local Spike work item under `docs/discovery/spikes/` is the authoritative anchor**: it holds
the link to the diagram and a one-line description of what the map shows. If you also write a
repo doc, it carries the inbound `story:` and a `relates.design` edge pointing at the diagram.
See `docs/ai-sdlc/artifact-graph.md`. Do not create work items here; that is
elaboration-upsert-user-story.

## Workflow

1. **Identify the persona and scenario.** Name whose journey this is and the scenario being
   mapped. A map with no clear actor or scope is not actionable.
2. **Lay out the experience.** Walk the scenario as stages; under each, capture actions, pains,
   and opportunities. Keep pains evidence-backed; mark assumptions as such.
3. **Produce the diagram.** Use mermaid or drawio. Save it to the repo.
4. **Optionally write a short discovery doc** carrying graph front-matter:

   ```yaml
   ---
   story: MN-5              # the Spike key, the anchor
   phase: discovery
   step: map-journey
   relates:
     design: <repo path to the diagram>
   ---
   ```

5. **Confirm before writing.** Present the diagram and any doc for confirmation.

## Guardrails

- **Map before you solve.** The output is pains and opportunities, not a chosen solution.
- **Anchor on the Spike file, not the board.** The link must live on the work item file.
- **Evidence over opinion.** Pains trace to research; mark unknowns as assumptions.
- **No em-dashes, no source line numbers.**

## Next steps

- `/discovery-upsert-hypothesis-canvas` (Analyst/PM) - frame the riskiest assumptions the map surfaced.
- `/elaboration-upsert-user-story` (PM) - when opportunities become stories.
- `/governance-enrich-ticket` (any) - link the map to the work item file.
