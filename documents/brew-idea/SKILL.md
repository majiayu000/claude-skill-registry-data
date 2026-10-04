---
name: brew-idea
description: Runs a multi-agent debate over a project idea. Four angle agents (product, engineering, skeptic, market research) propose and rebut, one judge ranks features keep / improve / add / cut with a phased plan, one designer turns the verdict into flows, screens, data and architecture, and the result becomes a markdown spec plus a design artifact like jump-start's. Use when the developer runs /opm:brew-idea <brief>, says "brew this idea", asks to brainstorm a project with several agents, or wants a project idea improved before designing it.
argument-hint: <project brief>
disable-model-invocation: true
---

# Brew-idea

One brief in, an argued-over design and plan out. The debate decides; the
page shows the product it decided on, not the argument. The developer is
involved at two points: the brief, and approving the result. Everything in
between runs without questions.

**Announce at start:** "Using opm:brew-idea; four angles will argue, one judge decides."

Invocation text is in `$ARGUMENTS`. The workflow script lives next to this
file: `${CLAUDE_PLUGIN_ROOT}/skills/brew-idea/scripts/brew.workflow.js`.
Template: `templates/spec.md`.

This skill needs the Workflow tool. If it is not in the tool list, stop and
say: "brew-idea needs the Workflow tool, which is not available in this
session." Do not imitate the run with Agent calls.

## Gates

| Gate | Passes only when |
|---|---|
| G1 Brief | A brief of about 15 words or more, or the one allowed question was answered |
| G2 Result | The workflow returned `completed: true` |
| G3 Approval | The developer chose "Approve" on the latest revision, not an earlier one |

## Phase 0: parse

1. The brief is all of `$ARGUMENTS`. If it is shorter than about 15 words, ask
   one question: "What should it do, for whom, and on which platform (web,
   mobile, API)?" Append the answer to the brief. No other questions.
2. `projectRoot` is the current directory, absolute.
3. `hasCode` is true when the directory contains source files outside
   `node_modules`, `.git` and `docs` (check for a package manifest or any
   `.ts`, `.js`, `.py`, `.dart`, `.go` file). Say which mode the run is in.
4. `slug`: the directory name when `hasCode`, otherwise the first three
   meaningful words of the brief (skip articles and "app", "for", "with") in
   kebab-case. `date` is today as `YYYY-MM-DD`.
5. Tell the developer: the four angles, that the run asks nothing, that it
   takes roughly ten to twenty minutes, and that the result comes back as a
   design page to approve.

## Phase 1: launch

Invoking this skill is the opt-in the Workflow tool requires; do not ask again.

```
Workflow({
  scriptPath: "<plugin root>/skills/brew-idea/scripts/brew.workflow.js",
  args: { projectRoot: "<abs path>", brief: "<brief>", hasCode: <bool> }
})
```

Record the runId. Wait for the task notification; do not poll.

Result shape: `{ completed, reason?, facts, proposals, rebuttals, verdict, design, missingAngles, silentAngles }`
with `verdict = { vision, features: [{ title, decision, reason, votesFor, votesAgainst, impact, effort }], plan: [{ phase, goal, features, risks }], cut: [{ title, reason }], openQuestions, assumptions }`
and `design = { pitch, goals, nonGoals, successSignal, personas: [{ name, need, flow }], surfaces: [{ name, kind, purpose, delivers, layout, states }], navigation: [{ from, to, via }], dataModel: [{ entity, fields, relations }], architecture: [{ part, runsOn, role }], stack: [{ choice, reason }], assumptions }`.

`completed: false` fails G2. Report `reason` in one line and offer to
relaunch with `resumeFromRunId` (finished phases replay from cache). Do not write a spec or a page.

Read the returned object only. Never open a subagent transcript.

## Phase 2: write the spec

Write `docs/specs/<date>-<slug>-brew.md` from `templates/spec.md`:

- Vision and Design from `design`: one block per surface with its `layout`
  lines in a code fence, in the order a user meets them.
- Features in the judge's order, one row each, with `votesFor` and
  `votesAgainst` as comma-separated angle names.
- One plan section per phase.
- Every entry in `verdict.cut`.
- `missingAngles` and `silentAngles` become an assumption line each
  (returned nothing, or proposed but never rebutted).
- Assumptions: `verdict.assumptions` then `design.assumptions`.
- Why these choices: one or two sentences per angle from its proposal and
  rebuttal: its position and the argument that changed the result. An angle
  in `missingAngles` gets "returned nothing".
- Run: angles present, count of ideas with `unverified: true`, revision count.

Keep it tight. The renderer reads it next, and implementers read it later.

## Phase 3: render

Dispatch one renderer and record its agent id, revisions resume it:

```
Agent (subagent_type: general-purpose, model: opus)
description: "Render brew-idea design page"
prompt: |
  Render <abs spec path> into <abs projectRoot>/docs/brew/<slug>.html as a
  design artifact in the style of
  <plugin root>/skills/jump-start/templates/design-outline.md: one
  self-contained page, inline CSS and inline SVG only, no external scripts
  or stylesheets, readable at 400px width, title "<slug> brew". Plain
  language a non-engineer can follow; the wireframes and diagrams carry the
  weight, text stays short. Sections in this order:
  1. Overview: vision, pitch, goals, not doing, success signal.
  2. Who uses it: one card per persona with its flow as numbered steps.
  3. Screens: one low-fidelity wireframe per surface, drawn from its layout
     lines as bordered boxes top to bottom (a terminal box for a command, a
     request/response box for an endpoint), with purpose, the features it
     delivers and its states underneath.
  4. How screens connect: an SVG navigation map from the navigation table.
  5. Data: entity boxes with fields and relation lines.
  6. Architecture: an SVG diagram of the parts and where they run.
  7. Stack: choice and reason.
  8. Plan: phases in order as a horizontal timeline, each with goal,
     features and risks.
  9. Decisions: one compact table of features with decision, impact and
     effort; then Cut and why.
  10. Open questions and assumptions, in a box headed "Challenge these
      before approving".
  11. Why these choices: collapsed in <details>, one line per angle.
  Mark unverified market claims "not checked online". Invent nothing: if the
  markdown does not say it, the page does not show it. Do not commit, do not
  dispatch subagents. Report in at most three lines: sections rendered and
  anything you could not render and why.
```

If the renderer fails, the spec still exists. Say so and offer to retry.

Publish:
- Artifact tool available: load the `artifact-design` skill, publish
  `docs/brew/<slug>.html` with the title "<slug> brew", and republish the same
  file on every revision so the link never changes.
- No Artifact tool: `open` the file (macOS) or `xdg-open` (Linux).

## Phase 4: approve

Repeat until approved:

1. Share the link and three lines, nothing more: the vision; "N features,
   M plan phases, K cut"; the first plan phase. Everything else lives on the
   page. Do not paste the verdict, the design or the debate into the chat.
2. Ask with AskUserQuestion: "Approve" or "Request changes" (free text).
3. On changes: relaunch with the same `scriptPath`, `resumeFromRunId`, and the
   same `args` plus `feedback: "<the developer's text>"`. Scout, propose and
   debate replay from cache; only the judge and the designer rerun. Rewrite the spec from the
   new verdict, SendMessage the renderer ("The markdown at <path> changed:
   <what>. Re-render and report."), republish, list what changed in three
   bullets, ask again. Every revision gets its own question.
4. On approval: commit the spec and the page:
   `docs(brew): <slug> brew-idea result`.

## Phase 5: finish

Tell the developer the next step:

- `opm:writing-plans` with the spec path when the project exists and the plan
  fits in a week.
- `opm:milestone-planning` when the plan has several phases.
- `opm:jump-start <name> <brief>` when the project does not exist yet; paste
  the vision and the add features into the brief.
- Optional: `/opm:explainer-video <path>` turns this into a narrated explainer.

## Errors

| Situation | Do |
|---|---|
| Workflow tool missing | Stop and say so. No Agent-call imitation |
| `completed: false` | Report `reason`, offer to relaunch with `resumeFromRunId`. No spec, no page |
| `missingAngles` not empty | Continue; note the angle in Assumptions and in the page |
| `silentAngles` not empty | Continue; the judge is told, note it in Assumptions |
| Market angle reports `webSearchUsed: false` | Note in Run that market claims were not checked online |
| Renderer fails | Keep the spec, say so, offer to retry the render |
| Developer interrupts the run | On the next invocation in the same directory, if a runId is known, relaunch with `resumeFromRunId` |

## Red flags

| Thought | Reality |
|---|---|
| "I'll run the angles with Agent calls, Workflow is overhead" | The workflow is the contract: fixed rounds, resume on change requests. Stop if it is missing. |
| "The skeptic only says no, the judge can skip it" | Every high-severity attack gets a mitigation or the feature is cut. That is the point of the skeptic. |
| "The debate is the interesting part, put it up front" | The developer approves a product, not an argument. Debate stays collapsed. |
| "I'll render the HTML myself" | Dispatch the renderer on opus. The main thread writes markdown, not SVG. |
| "They approved the last version, this tweak is fine" | Every revision gets its own approval question. |
| "The market claims sound right, no need to flag" | Unverified stays unverified in the spec and on the page. |
| "One quick question to the developer mid-run" | The run asks nothing. The judge lists open questions instead. |

## Safety

- Read-only against the project: the run creates nothing outside `docs/specs/`
  and `docs/brew/`, and commits only on approval.
- Nothing leaves the machine except the market angle's web searches and the
  artifact publish, which is private by default.
