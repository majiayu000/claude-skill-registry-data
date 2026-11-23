---
name: redesign-in-claude
description: >
  End-to-end page redesign straight into Claude Design. Runs the
  draft-ui-redesign skill to audit a page and produce its self-contained
  generation prompt, then uses that prompt to build the redesign as a Claude
  Design artifact (the Artifact tool's Design type) — no copy-pasting between
  tools. Use when the user says "redesign this page in Claude Design", "take
  this screen through Claude Design", "draft and design the redesign", or runs
  /redesign-in-claude with a route or file. Claude-only: it targets Claude
  Design exclusively, never Stitch, v0, Lovable, or Figma Make.
license: MIT
compatibility: >
  Claude only (Claude Code or claude.ai). Requires the Artifact tool with the
  Design type, and the draft-ui-redesign skill installed alongside it.
metadata:
  author: mshindi-labs
  version: "1.0.0"
---

# Redesign in Claude Design

Two stages, run in order without stopping in between unless something blocks:

1. **Draft** — `draft-ui-redesign` writes the redesign document and its prompt.
2. **Design** — that prompt becomes a live Claude Design artifact, built with
   Anthropic's `frontend-design` skill when it is installed.

This skill adds no design rules of its own. The contract (nothing removed, no
logic changes, additive-only APIs, graceful degradation) and all the audit
rules belong to `draft-ui-redesign` — do not restate or loosen them here.

## Stage 1 — Draft the prompt

Invoke the skill with the Skill tool:

- `skill: "draft-ui-redesign"`
- `args`: the user's route or file, plus: `Target tool: Claude Design only.`

Follow it completely (locate → audit → benchmarks → gaps → write the doc). It
writes `docs/redesign/<page>-redesign.md`.

**Stop here and ask the user** if `draft-ui-redesign` could not find the real
response shape. A design built on guessed fields is worthless, and Stage 2
would only make it look polished.

## Stage 2 — Extract the prompt

Read the generated document and take the content of the fenced `text` block
under `## 3. Generation Prompt`, verbatim. That block is the only thing that
goes to Claude Design.

Before using it, check it is self-contained: no file paths, no "see the table
above", no raw field names without a description of what they hold. If it
fails the check, fix it in the document first so the doc and the design match.

## Stage 3 — Build it in Claude Design

1. Call `Artifact` with `action: "quickstart"`, `intent: "design"`. Always do
   this fresh; never hardcode the Design type's `type_url`.
2. Publish with the returned `type_url`, `title: "<Page Name> redesign"`, no
   files, and `auto_open: "after_first_write"`.
3. **Load Anthropic's `frontend-design` skill, if it is available** (see
   below), before filling the artifact.
4. Follow the instructions in the create result to fill the artifact. The
   extracted prompt is the brief. Design every state it lists (loading, empty,
   error, dense/overflowing) and every responsive breakpoint as its own
   artboard, not just the happy path.
5. If the user names a design system, use it. Otherwise carry on without one,
   as the quickstart result says.

Do not use `DesignSync` here. It syncs design-system component libraries and
cannot create designs.

### Using `frontend-design`

Check the available skills for Anthropic's official `frontend-design` (listed as
`frontend-design:frontend-design` when installed as a plugin, or
`frontend-design`). If it is there, invoke it with the Skill tool. If not, skip
this section and build without it. Do not substitute a community lookalike.

Use its process for the build: plan a compact token system (a palette of 4 to 6
named hex values, type with roles, layout, principles), review that plan against the brief for generic defaults,
build, then critique the rendered artboards and fix what fails. Also use its
quality floor (focus states, contrast, reduced motion, mobile) and its list of
generated-design tells to avoid.

It sits **below** the brief. Where they disagree, this order wins:

1. The `draft-ui-redesign` contract: every item in the content inventory
   appears, nothing is invented, behaviour is fixed.
2. The prompt's design direction and named benchmark mechanics. These pin down
   density, alignment and type. `frontend-design` defers to a brief that sets a
   direction, so follow the prompt exactly.
3. `frontend-design`, only on axes the prompt leaves open.

In practice:

- **No hero, no marketing composition.** This is an existing working screen.
  Open with its primary job, as the prompt's hierarchy says.
- **Keep existing labels verbatim.** Its copywriting guidance applies only to
  text the redesign adds, such as empty, error and loading states.
- **States you add get copy, never controls.** An empty, error or loading state you
  design may add text, but no button or link the page does not already have: no
  retry, create, reset or refresh unless the page already offers it.
- **Skip its "confirm the subject with the client" step.** The audit has
  already established the subject, audience and job.
- **Put boldness where the benchmarks allow it.** For dense tools that is
  usually one detail, such as the status treatment or a key figure, not the
  overall layout.

## Stage 4 — Hand back

Link the design doc and add the artifact's URL to its top, as
`Claude Design: <url>`, so the two stay connected. Then report briefly:

- Design artifact link
- Document path: `docs/redesign/<page>-redesign.md`
- API additions proposed (from section 4), or "none needed"
- Whether `frontend-design` was used
- Anything you had to guess or that the user should review

## If something fails

- **Artifact publish refused or the Design type is unavailable:** stop, say so
  plainly, and point the user at the prompt block in the doc so they can paste
  it into claude.ai/design by hand. Do not switch to another design tool.
- **The user wants changes to the design:** edit the same artifact by its
  `url`. If the change affects content (adds or removes a data point), update
  the doc's prompt and inventory first. The doc stays the source of truth.
