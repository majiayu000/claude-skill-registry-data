---
name: run-sdlc
description: >
  Navigate the AI-SDLC workflow for a given work item or artifact: report where it is in
  the lifecycle and what to do next. Use when the user asks "where are we on MN-42",
  "what is the next step for this story", "run the sdlc on <key or path>", "what is missing
  before this can ship", "which phase is this in", or hands over an artifact (a work item key, a
  spec, a doc, an ADR) and asks how to proceed. It is READ-ONLY for navigation: it resolves the anchor,
  traverses the artifact graph, and reports the current phase plus the next /<phase>-<step>
  and the persona who owns it. It does NOT create, edit, link, or transition anything, and it
  never writes directly; on explicit request it can dispatch the next step by handing off to the
  owning phase-step skill (which writes behind its own confirmation gates), per
  docs/ai-sdlc/orchestration.md. Do NOT use to
  author artifacts or to write work items.
---

# Run SDLC (navigator)

Owned by the **Orchestrator** (cross-cutting). Invoked as `/run-sdlc <artifact>`.

Given any work item or artifact, work out where it sits in the lifecycle and what comes next,
then report it. This is a **guide, not an autopilot**: it reads and reports; it never writes,
and by default does not execute the next step - the human decides whether to run it. On explicit
request it dispatches the next step per `docs/ai-sdlc/orchestration.md`, handing off to the owning
step-skill (which writes behind its own gates) and running genuinely independent steps in parallel
on Claude. It still does not author anything itself; it routes.

The phase/step/persona map this navigates is in `docs/ai-sdlc/plan.md`; the graph it traverses
(front-matter edges in local work item files and repo artifacts) is defined in `docs/ai-sdlc/artifact-graph.md`.
Read those for the authoritative map and schema rather than trusting a copy here.

## The lifecycle it reports against

Phases in order, with the governance track running across all of them:

- **discovery** - synthesize-research, map-journey, upsert-hypothesis-canvas (Analyst)
- **elaboration** - upsert-user-story, upsert-prd-document, upsert-user-story-acceptance-criteria, architecture, upsert-api-contract (PM / Architect)
- **create** - sprint-planning, code-generation, refactoring, verify-test-coverage, upsert-documentation (Scrum Master / Developer / QA / Tech Writer)
- **mature** - collect-release-feedback, analyze-ticket, resolve-ticket (PM / Developer)
- **governance** (cross-cutting) - constitution, author-adr, enrich-ticket, check-graph (Lead / Architect / any)

## Input

One of:
- a **local work-item key** (e.g. `MN-42`), the usual anchor;
- a **repo artifact path** (a doc, spec, or ADR) that declares `story:` front-matter;
- a free description, in which case resolve it to a key first (search `docs/discovery/`) or ask.

## Workflow (read-only)

1. **Resolve the anchor.**
   - Given a key (e.g. `MN-42`): find the matching work item file under `docs/discovery/` by scanning front-matter `key:` fields. Read its content (title, status, type, points, relates).
   - Given a repo path: read its front-matter (`story`, `phase`, `step`, `relates`) and take `story` as the anchor. If it has no front-matter, treat the file as not yet in the graph and say so.
2. **Traverse the graph (repo side).**
   - Find artifacts that declare `story: <key>` in a YAML front-matter block (the `story:` line between the leading `---` fences). Search `docs/`, `docs-functional/`, and `specs/`. Ignore the illustrative examples in `docs/ai-sdlc/*` (they show the schema, they are not real artifacts). Collect each artifact's `phase`, `step`, and `relates` edges (spec, adr, design, research, docs).
   - Read the work item file itself for `relates:` entries pointing to other work items (story-to-story edges), and for artifact links in its body sections (Decisions and ADRs, Artifacts and references).
3. **Place it in the lifecycle.** From the anchor's phase (front-matter, or inferred from status/type) and which artifacts exist, determine the current phase and which expected edges are present vs missing. Use the "intended required edges" in `docs/ai-sdlc/artifact-graph.md` as the checklist.
4. **Report (do not act).** Cover:
   - **Where it is:** the current phase and what exists (story, ACs, spec, ADRs, code/tests, docs), each with its path.
   - **What's missing:** the expected edges or artifacts not yet present. Mark an expected edge **N/A (reason)** rather than missing when the work plainly does not need it.
   - **Options:** a numbered list of the viable next `/<phase>-<step>` moves from here, each with the **persona** who owns it and a short why.
   - **Recommendation:** end with one recommended option and a short, concrete why it is the best move now.
   - **Thin ticket -> sharpen before build.** If the anchor is under-specced, recommend sharpening first.
   - **Entering build starts with a plan, not code.** When the next step is `/create-code-generation`, say so explicitly.
   - **Caveat:** the graph is incremental, so artifacts without front-matter are invisible here; say the report is "based on what is linked".
5. **Offer to dispatch.** By default, stop here. If the user asks you to run the next step, dispatch it per `docs/ai-sdlc/orchestration.md`.

## Output shape

A short report, for example:

```
MN-42  -  "Compare two cloud configuration versions"
Phase:   elaboration  (story exists, acceptance criteria present)
Linked:  story (docs/discovery/stories/cloud-config/compare-versions.md), ADR 0007 (docs/adrs/0007-...md)
Missing: machine-readable spec (relates.spec) before it can enter create

Options:
  1. /elaboration-upsert-api-contract          (Architect) - add the OpenAPI spec the build will consume
  2. /elaboration-upsert-user-story-acceptance-criteria (PM/QA)     - tighten the ACs first if any are still thin
  3. /governance-enrich-ticket        (any)       - link the spec/ADR onto the work item once they exist

Recommendation: 1, /elaboration-upsert-api-contract. The story is AC-complete but has no spec, and the spec is the gate into create.

(Based on linked artifacts; the graph is incremental, so unlinked work is not shown.)
```

## Guardrails

- **Read-only navigation.** The navigator never creates, edits, links, or transitions anything itself.
- **A guide, not an autopilot.** Do not run the next step automatically - surface it and let the human choose.
- **Be honest about coverage.** The graph is incremental; state that the report reflects only artifacts that have opted in (front-matter). Do not assert a phase is "done" from absence of evidence.
- **No direct writes.** No file creation, front-matter edits, or work item writes from the navigator itself. When the user wants to act, dispatch to the owning skill.

## Next steps

- Run the `/<phase>-<step>` this report identified, owned by the named persona.
- To run several genuinely independent next steps at once, dispatch them per `docs/ai-sdlc/orchestration.md`.
- If an expected edge is missing because it was never linked (not because the work is undone), fix the link with `/governance-enrich-ticket`, then re-run this navigator.
- `/governance-check-graph` (Lead) - validate that the repo-side `relates:` links actually resolve.
