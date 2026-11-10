---
name: open-design-critique
description: Get a second opinion on an Open Design artifact from a design critic, judged from its latest check screenshots, the brief and the design system against a fixed rubric, with one verdict (ship, polish or rework) and at most five fixes — use before telling the user a design is done (the open-design skill's check step), and whenever the user asks for a second opinion, another opinion, a critique or a review of an Open Design artifact, or asks "is this good?"
---

<!-- generated:open-design-agent-kit -->

Get a design critic's second opinion on one Open Design artifact.

Request: the rest of the user's message (if there is none, ask the user: "Which design should get a second opinion?")

**How to talk to the user.** Many people using Open Design don't write code, so:
- Use the user's own words. If they say "artifact", "design tokens" or give a file path, use those terms back; otherwise use the plain words below.
- Keep the machinery out of replies: no tool names, no ids like `od:prototype:poster-hero`, no internal files (`.artifact.json`, `.comments.json`, `config.json`), and not the words "register", "manifest", "sidecar", "entry" or "surface", unless the user used them first.
- Explain a print term the first time it comes up, in one short clause, and not again.
- Say where a file is the way the user would find it ("in your Open Design folder, under seed-swap-flyer"). Give a raw path only where the user can click it (Claude Code, Claude Desktop's Code tab, VS Code) or asks for it.
- End each reply that finishes a step with one line on what they can do next, with at most two options ("Want it in Instagram sizes too, or is it ready to print?").

| Instead of | Say |
|---|---|
| artifact, entry, registered | your design, saved |
| design system, active design system | your style (the first time: "a saved style: colours, fonts and spacing") |
| surface, skill, template, recipe | kind of design, starting layout, or nothing |
| workspace, output directory | your folder, your Open Design folder |
| bleed | print edge ("a few millimetres extra that the printer trims off") |
| trim size | final size |
| preflight findings, errors | "I checked it and fixed…", "one thing to look at:" |
| export | save as PDF, save as an image |
| inline preview, MCP App | the preview above |

## 1. Find the artifact

Use the artifact the request names; if it names none, use the one you made or changed most recently in this conversation. Registered artifacts are the files under the Open Design output folder (default `.open-design/`) that have a `.artifact.json` file next to them. If it isn't registered yet, register it first with `register_open_design_artifact`.

## 2. Gather what the critic sees

Call `get_open_design_artifact` with its `entryPath` and `critique: true`. The result's `critiqueInput` holds the recorded brief (or, when there is none, the title and skill id), the design system's `DESIGN.md`, the latest saved check run's findings (including any taste and state findings) and its screenshot paths, and the last critique. The run's screenshots are attached.

If it says there is no saved check run, call `check_open_design_artifact` for the artifact first, fix any **error** it reports, then ask for the critique input again.

## 3. Get the critique

The critic judges only what is in `critiqueInput` and the screenshots, never what the builder meant. Pick the first of these your host has:

- **The `design-critic` agent** (Claude Code with the Open Design plugin; it may be listed as `open-design:design-critic`). Start it with the entry path, the `critiqueInput` JSON exactly as returned, and the screenshot and entry file paths written as full paths your own file tools can read. Add nothing about what you intended or what the user said beyond the recorded brief. It reads, it never edits.
- **A general subagent tool** (the Agent tool in Claude Code, `runSubagent` in VS Code). Give it the same material plus the rubric and output format below, and tell it not to edit any file.
- **Neither: run it yourself, inline.** Judge the attached screenshots against the rubric as if you had never seen the design before: look for what is on the screen, not for what you meant to put there. In your reply, call it a self-review ("I looked it over again myself"), since it is weaker than a fresh critic.

<!-- rubric:start -->
**Rubric.** Judge the screenshots first and the entry file only to confirm copy and states. Every finding names one of these areas:

| `area` | Looks for |
|---|---|
| `purpose-hierarchy` | Can you tell in five seconds what this is and what to do? One clear first read. |
| `typography` | The display scale actually used, comfortable line length, not too many sizes or weights. |
| `colour-contrast` | The accent used for meaning, not decoration; contrast findings from the check. |
| `layout-rhythm` | Spacing on the design system's steps, alignment, crowded or dead areas. |
| `copy` | Filler, invented numbers, vague buttons ("Submit", "Learn more"). |
| `states` | Empty, loading and error states present where the design shows data. When a screenshot is labelled `states: …` (the states board), judge every frame on it: each says why it is in that state and offers a next action, and none is a blank panel or a near-copy of the default. |
| `task` | When `critiqueInput.tasks` lists tasks: each can be finished on these screens (see the walkthrough below). |
| `fit` | Matches the design system's `DESIGN.md` and the brief, not a generic look. |

**Walk each task.** For every task in `critiqueInput.tasks`, go through its `path` screen by screen on the screenshots (for a single screen, find the action that completes it). On each screen ask: is the control for the next step (its `triggers` label) visible on the first screen, is it the most prominent action there rather than a secondary link under a bigger button, does its label say where it leads, and is there a way back? Report what fails under `task`, naming the task and the screen in `where`. A task marked `unreachable`, or one you can't walk on the screenshots, makes the verdict at least `polish`.

**Respect steering edits.** When `critiqueInput.edits` lists recent steering edits ("bolder on the pricing section"), the user asked for those directions: don't propose a fix that reverses one (making that section quieter again). Judge whether each edit worked and fits the rest of the page.

**Check a redesign's fixes.** When `critiqueInput.auditFixes` lists problems found on the old site, look for each one in the screenshots of the new design (a booking button below the fold on the phone, text too faint to read, tap targets too small). Report any that is still there under `task`, with its id and title in `where`. One still there makes the verdict at least `polish`.

**Judge `fit` against the person's own brand.** When `critiqueInput.brand` is present the design is on their own brand. Open `brand.reference` (their site) beside the screenshots. Compare the buttons, inputs and cards with `brand.components` (height, radius, weight, case), and the headlines and calls to action with `brand.voice` (heading case, sentence length, person, exclamation marks, the sample lines). Name each mismatch in the `fit` note with the brand's value, for example "headline in upper case with exclamation marks; the brand writes sentence case and uses none".

**The brief wins.** When the brief or the design system asks for the look a finding objects to (all caps, one colour, a dense layout), drop the finding. Don't flag what the check already reported as an error unless it is still visible in the screenshots.

**Verdict:** one of
- `ship`: nothing worth another round.
- `polish`: one round of the listed fixes makes it right.
- `rework`: the direction is wrong (wrong audience, wrong kind of design, unreadable), and fixes won't save it.

**Findings:** at most five, most important first, each with `area`, `where` (the section, element, slide or viewport), `problem` (what is wrong, in one sentence) and `fix` (the change to make, specific enough to do without asking). Fewer is better than padding: a `ship` verdict usually has none.

**Output:** only this JSON, nothing before or after it:

```json
{ "verdict": "polish", "findings": [{ "area": "copy", "where": "hero button", "problem": "\"Learn more\" doesn't say what happens.", "fix": "Say \"Start your free trial\"." }] }
```
<!-- rubric:end -->

## 4. Act on the verdict

- **`ship`:** the design is done. Record the critique (step 5) and tell the user.
- **`polish`:** apply every finding once with your own file-editing tools, register the artifact again (with the critique, step 5), run `check_open_design_artifact`, and fix any new **error**. Then report it done: don't ask for a second critique unless the user wants one.
- **`rework`:** don't rebuild yet. Record the critique, tell the user in a sentence or two what is wrong and what you would change, and ask whether to rebuild that way. Rebuilding is their call.

When the user asked for this opinion themselves, show them the verdict and findings and ask which to apply, instead of applying them straight away.

## 5. Record it

Pass the critique as `critique` (`verdict` and `findings`, as returned) on your next `register_open_design_artifact` call for the artifact, with the same other arguments as its last registration (kind, title, skill id, design system, format, supporting files). Only the latest critique is kept; it shows in the browser preview's Checks panel as "Second look". `checkRunId` and `at` are filled in for you. If registration rejects it as over 4 KB, shorten the findings and register again.

## 6. Tell the user

Keep it short and in everyday words: "I had a second look: …", then the top one or two things you improved (or, for `rework`, what's wrong), and nothing about rubric areas, verdict codes, file paths or tools. In Claude Desktop Chat and Cowork, say at most two findings and nothing more technical than that. Elsewhere, list every finding only if the user asks.

If the user says they don't want a second look on their designs, respect it for the rest of the conversation and skip this skill in the check step.
