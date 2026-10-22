---
name: generate-ux-design
description: Phase 2.5 of the SPEAKMAN.AI pipeline — run MCP_UX_DESIGN_V1 to map architecture and requirements into a UI screen inventory, then produce a proposed design direction and clickable HTML mockups for human review before Phase 3 code generation
---

# generate-ux-design — SPEAKMAN.AI Phase 2.5 UX & Interface Design

You are running Phase 2.5 of the SPEAKMAN.AI pipeline: mapping a solution's architecture and
requirements into a UI screen inventory, then generating a proposed design direction and
self-contained HTML mockups for the human to actually react to before Phase 3 writes real code.

This phase sits between Phase 1 (Architecture) and Phase 3 (Code Generation) — it can run
right after Phase 1 alone, or after Phase 2 (Requirements) if that's been run for richer use
case detail. It is optional: skip it and Phase 3 will infer UI decisions on its own instead of
building toward a reviewed target.

---

## Step 0 — Collect Inputs

Ask the user:

> "Where is the Phase 1 (Solution Architecture) output?
>  - **On disk** → the SAD output directory containing a `raw/` folder
>  - **A SPEAKMAN.AI session** → the Phase 1 session ID, fetched via `get_output` (public API only)
>  - **Neither** → paste a business description and I'll run this from that alone (lower quality — Phase 1's component/requirement detail is strongly recommended)"

> "Do you have Phase 2 (Requirements Engineering) output too? Same options — on disk, a
> session ID, or skip. Adds richer use-case and field detail; not required."

> "Do you have an existing brand to design toward — a live website, a style guide file, or
> brand text? Optional — paste it, point me at a file/URL, or press Enter and I'll propose a
> direction from the business context instead."

> "Where should the output go? Provide the parent directory — I'll create
> `outputs/YYYY-MM-DD_{slug}/` under it."

Store: **PHASE1_SOURCE**, **PHASE2_SOURCE** (optional), **BRAND_SOURCE** (optional, stored as a
raw reference — do not parse it yet, the delegate step in the workflow itself fetches it),
**OUTPUT_PARENT**.

> **Handoff rule (do not violate):** session IDs are read only via `get_output` — never bridge
> internal DB records server-side. Same rule as every other phase skill in this pipeline.

---

## Step 1 — Load Context

**Phase 1** (required or a business-text fallback, same three branches `generate-requirements`
uses):
- On-disk `raw/` dir → read `business_analyst.txt` (personas, functional requirements,
  key data entities) and `business_application_architect.txt` (logical components).
- Session ID → `get_outputs` then `get_output` for `MCP_BUSINESS_ANALYST_V1` and
  `MCP_BUSINESS_APPLICATION_ARCHITECT_V1`.
- Business text only → use as-is; warn that component/requirement mapping quality will be lower.

**Phase 2** (optional): if provided, read/fetch `use_case_catalog.txt` and
`database_schema.txt`/`api_schema.txt` for richer flow and field detail than Phase 1 alone provides.

---

## Step 2 — Build the Seed Description

Compose a description (10,000-char limit, same headroom rule as every other phase skill — use
it, don't over-condense) containing, in this order:

1. Business goal (one paragraph)
2. Personas with their primary goals
3. Functional requirements — ID + category + description for each (do not drop any; this is
   what the needs analyst traces coverage against)
4. Key data entities and their fields
5. Logical architecture components — ID, name, type, responsibility for each (the needs analyst
   determines which are real UI surfaces; give it everything, don't pre-filter)
6. If **BRAND_SOURCE** was provided: state it verbatim as the last line, e.g. "Existing brand
   source: {url or reference}." If not provided: state "No existing brand source is available
   for this project — propose a design direction grounded in this business context."

Show the assembled description to the user and confirm before submitting.

---

## Step 3 — Run the SPEAKMAN.AI Session

### 3a — Start

`start_session(workflow_id="MCP_UX_DESIGN_V1", title=<short project title>, description=<Step 2 output>)`.

Poll every 20-30s.

### 3b — Handle each AWAITING_INPUT gate

This workflow has one delegate step and one human review gate, in sequence:

- **`agent_type: "MCP_LLM_DELEGATE"` (origin `UX_MOCKUP_DESIGNER_V1`)** — this is you. Read
  `input_required.prompt` (your operating instructions) and `input_required.context` (the
  validated screen inventory + flow diagrams). Do the actual design work yourself: propose a
  direction (or fetch the real brand source if one was referenced) and produce self-contained
  HTML mockups for the 3-5 highest-priority screens, per the prompt's own instructions. Submit
  the exact JSON shape it asks for via `submit_response`. On every `submit_response` in this skill, also pass `executed_by`: the name of your tool and your model, for example `Claude Code, claude-opus-5-5` (say what you actually are and do not guess; it is recorded with the output).

- **`agent_type: "HITL_VALIDATOR"` (origin `UX_MOCKUP_DESIGNER_V1`)** — this is the real human
  review gate. **Do not self-approve.** Save each mockup from the prior step's own submission to
  a local `.html` file (see Step 4 — do this now, before asking, so you can show real files) and
  publish each as an Artifact for the user to actually look at, one per mockup, not a compressed
  summary — this is a Claude Code-specific capability, appropriate here because this skill (not
  the underlying workflow) is allowed to be client-specific; a different connected client would
  show these some other way. Surface the design direction (palette, typography, layout concept)
  and ask the user to approve or describe changes. Submit their real answer via
  `submit_response({"status": "Approved"|"Update", "feedback": "..."})` — never invent approval
  on their behalf.

Continue polling until `COMPLETED`.

---

## Step 4 — Download and Save Outputs

`get_outputs(session_id)` for the manifest, then `get_output` for each agent. Create
`OUTPUT_PARENT/outputs/YYYY-MM-DD_{slug}/` (slug = lowercase-hyphenated title, date = today)
with this layout:

| Source | Save as |
|---|---|
| `UX_NEEDS_ANALYST_V1` (full JSON) | `raw/screen_inventory.json` |
| `UX_FLOW_VISUALIZER_V1` (Mermaid text) | `raw/flow_diagrams.md` |
| `UX_MOCKUP_DESIGNER_V1`'s `design_system` field | `raw/design_system.json` |
| Each entry in `UX_MOCKUP_DESIGNER_V1`'s `mockups` array | `mockups/{screen-name-slug}.html` — the `html` field's content, saved as a real standalone file, not embedded in another document |

Save every mockup as its own real `.html` file — these need to open directly in a browser, not
live only as JSON strings inside a bigger output.

---

## Step 5 — Report

```
Phase 2.5 — UX & Interface Design
Session ID   : {session_id}
Credits used : {session_cost}   (only if a tool reported a cost; leave this line out otherwise)
Design review: {approved on first pass | approved after N revision(s)}
Outputs      : outputs/YYYY-MM-DD_{slug}/
  raw/screen_inventory.json
  raw/flow_diagrams.md
  raw/design_system.json
  mockups/{screen}.html   (one per mockup produced)
```

Report any requirement the needs analyst flagged as `unmapped_requirements` (these are usually
legitimate backend-only requirements, but confirm rather than assume) and any screen the
mockup step explicitly skipped, with its stated reason — don't let either go unmentioned.

Then say: "Phase 2.5 complete. These mockups are reference targets for Phase 3
(`/generate-speakmanai-code`), not production code — no real data binding, no framework, no
routing. Open any `.html` file directly in a browser to review."

---

## Rules

- **Phase 1 is strongly recommended, never fabricated.** If truly absent, run from business
  text alone and say so plainly in the final report.
- **The brand source, if given, is passed through as a raw reference in the seed description —
  never parsed by this skill.** The workflow's own delegate step fetches and reads it directly;
  parsing it here first would duplicate that work and risk stripping detail the delegate step
  needs.
- **Never self-approve the HITL gate.** The whole point of this phase is a real human reaction
  to a real proposal — surface every mockup individually, not a summary, and submit only the
  user's actual answer.
- **Mockups are saved as real, standalone `.html` files.** They must open and render correctly
  on their own — verify each one is complete (starts with `<!doctype html>`, ends with
  `</html>`) before reporting success.
- **These are throwaway reference mockups, not code Phase 3 should copy verbatim.** Say this
  explicitly in the final report so it's never mistaken for a deliverable to wire up as-is.
