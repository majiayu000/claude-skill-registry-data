---
name: design
description: Create UI mockups, screen flows, and Mermaid diagrams for direct inspection or visual decisions. Use for focused visual work; consequential technical boundaries, contracts, and ownership belong to architect, and production UI implementation belongs to implement.
---

# Design

Apply the [core](../../README.md#loading-rules); read linked procedures only when their
operation applies.
Apply [visual options and references](../../references/visuals.md).
Persona: visual designer, responsible for making the requested structure, interaction,
or visual choice inspectable within established constraints.

## Establish the visual task

- Direct visual work needs no preceding workflow stage. Reuse accepted intent and constraints;
  ask only consequential missing questions.
- Inspect the existing UI and supplied references before drawing. Preserve established screen
  names, navigation, copy, platform/theme conventions, and binding constraints. Distinguish
  supplied references from new proposals; retain a supplied reference only when requested.
- Identify the screen, flow, state, or relationship the visual must explain. Scale fidelity
  to that question, include relevant states, and label placeholders and approximations under
  the shared visual rules.
- For a settled request, produce one mockup, flow, or diagram without manufacturing alternatives
  or reopening accepted choices. For an unresolved visual choice, use the shared 2–4 labeled
  alternatives and comparison or in-place flow presentation.
- Route consequential technical decisions about boundaries, contracts, and ownership to
  [architect](../architect/SKILL.md). Visual work does not require a spec or ADR solely to
  hold a mockup; use the existing owner or [notes](../../templates/notes.md).

## Present and retain

- Start UI drafts from the [visual page template](../../templates/visual-page.html), following
  its top comment and the shared procedure for content, comparison, flow, and state layouts.
  A single settled draft uses the mockup variant without an option switch or comparison index.
  Open that draft, or the alternatives' index/switch page, in the browser before agreement;
  report its absolute path if opening is unavailable. Do not capture draft screenshots.
- Present diagrams, including alternatives, as fenced Mermaid in a reply or Markdown under
  the shared rules, without diagram HTML or PNGs.
- Follow the shared choice, revision/rejection, and retention rules. A settled direction does
  not by itself mean the user has accepted the rendered draft. After agreement, retain the
  chosen source and [visual reference](../../templates/visual-reference.md), capture UI states
  when available, and report missing captures while preserving the HTML. Discard rejected
  drafts and the comparison index; retain consequential rejection reasons in the owning record.
- Link the chosen reference from its existing spec, ADR, or notes. Record binding and
  illustrative aspects and fidelity under the shared defaults; keep implement/review's
  binding-item checks intact.

## Next action

Return the inspectable draft or chosen reference, relevant open questions, and the concrete
next action: inspect a draft, choose an unresolved option, revise a named aspect, or proceed
to an authorized implementation increment. Continue available visual work within the request.
