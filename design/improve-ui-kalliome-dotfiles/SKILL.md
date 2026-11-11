---
name: improve-ui
description: Point at a running UI — a screen, or a whole task flow like creating something, signing up, or checking out — and get a published preview of what it actually looks like plus ranked, concrete proposals for improving it. Drives the real app with agent-browser to capture screenshots and test states, judges the result against the UX skill's checklists, and publishes screenshots-and-proposals to preview.teppo.dev. Use for "improve this UI", "make this screen better", "improve the create-X flow", "review the design of X", "what's wrong with this page".
---

# Improve UI

Look at a real running UI, find what is holding it back, and publish
**screenshots next to concrete proposals** the user can react to.

This skill proposes. It does not change application code — implementation runs
afterwards through the preview skill's approved-preview path.

## Hard requirements

- **`agent-browser` is the only way this skill sees the UI.** Every finding
  comes from a page that was actually opened, screenshotted, and interacted
  with. Reading components and inferring how they render is not a substitute
  and never produces a finding on its own. If the target cannot be reached in
  a browser, stop and say so instead of reviewing from source.
- **`skill://preview` publishes the result.** No markdown report, no wall of
  chat text — the deliverable is one link.
- **`skill://ux` supplies the judgement.** Its Visual consistency check and
  Intentional visual restraint check are the fixed part of the review; the
  proposals are the rest.

## 1. Resolve the target

The invocation should name the place to improve. It comes in two shapes, and
which one it is changes what you capture and what you judge:

- **A surface** — a URL, route, screen, or page. "Improve the settings page."
- **A flow** — a task the user is trying to finish across several steps.
  "Improve creating a project", onboarding, sign-up, checkout, invite a
  teammate, publish. A flow is named by its *goal*, not its routes; your job is
  to find the entry point and walk the whole thing to done.

If the target names a task or a verb, treat it as a flow even when it happens
to live on one screen — a one-screen create form still has a sequence, defaults,
validation timing, and a "what now" moment after submit.

Everything else you work out yourself.

Before asking the user anything, find out from the repo:

- how the app starts (`package.json` scripts, `Procfile`, `docker-compose`, a
  project `run`/dev skill) — and start it if it is not already running;
- what routes and screens exist, so you can name candidates concretely;
- whether the flow needs auth, seeded data, or a feature flag.

Then ask **one** question only if a real ambiguity survives — typically "which
of these screens" or "what credentials get me past login". Do not ask what the
codebase answers. If the invocation named no place at all, list the routes you
found and ask which one, with a recommendation.

Fix these before opening the browser: reachable URL(s), scope (which
screens/states are in, or where the flow starts and what counts as done),
viewports (default: 1440×900 desktop and 390×844 mobile), and whether the app
has a dark theme worth checking.

For a flow, also decide the **goal you will actually carry out** — a specific,
realistic task with real-looking data ("create a project called Q3 Migration
and invite one teammate"), not a click-through. You have to finish it to know
where it hurts.

## 2. Load the rules

```bash
agent-browser skills get core     # required before any browser command
```

Read `skill://ux` for both checklists and `skill://preview` for publishing.
Then find the project's design system the way the preview skill's *Inherit the
project's design system* section describes — `UX.md`, `docs/ux/*`, token
stylesheets, Tailwind/theme config, component library. Proposals must be made
in the product's own tokens, components and vocabulary; that is the difference
between a design review and a generic critique.

## 3. Walk the UI

Drive the real app. Per screen in scope:

```bash
agent-browser set viewport 1440 900
agent-browser open <url>
agent-browser snapshot -i                 # what is actually interactive
agent-browser screenshot ~/.preview/<slug>/shots/<screen>-desktop.png
agent-browser screenshot --full ~/.preview/<slug>/shots/<screen>-desktop-full.png
agent-browser set viewport 390 844
agent-browser screenshot ~/.preview/<slug>/shots/<screen>-mobile.png
```

Save every screenshot straight into the preview folder's `shots/` — they are
the evidence and they go in the page.

Then **test it**, don't just photograph it:

- **States:** hover and focus the primary controls (`hover @eN`,
  `press Tab` and screenshot the focus ring), submit a form empty and with
  invalid input, reach the empty state with no data, and force loading and
  error with `network route "**/api/**" --abort` or `--body '{...}'`.
- **Overflow:** put a long name, a long translation, or a long URL into the
  cells and labels via `eval --stdin`, and re-screenshot at the narrow
  viewport. Truncation bugs live here.
- **Keyboard path:** tab through the screen in order; note traps, invisible
  focus, and controls you cannot reach.
- **Dark mode:** `agent-browser set media dark` when the app themes.
- **Health:** `agent-browser console`, `agent-browser errors`, and
  `agent-browser vitals` — layout shift and a slow LCP are UI problems.

### Walking a flow

For a flow target, do the task for real, start to finish, and screenshot
**every step in order** — including the moments between screens: the entry
point that starts it, each step, the submit, and whatever the app shows you
after it succeeds. Number the shots by step (`shots/02-details-desktop.png`) so
the sequence survives into the preview.

While walking, keep a running log of things a per-screen review cannot see:

- **Step count and what each step asks for** — and which fields could have been
  defaulted, inferred, deferred, or dropped.
- **Where you had to leave** to fetch something the flow needed (an ID, a name,
  a file) and whether the flow helped you get back.
- **Back, cancel, and close** at every step: what is lost, what is kept, and
  where you land. Try the browser Back button too, not just the app's.
- **Interruption and resume** — reload mid-flow and re-open the entry point.
  Is the half-finished work still there, and does the app admit it exists?
- **Failure at the worst moment** — force the final submit to fail
  (`network route "**/api/**" --abort`) and see whether the input survives.
- **The landing** — after success, does it tell you what happened, where the
  thing went, and what to do next, or drop you on a list?

Then re-walk the unhappy paths: the empty/first-run version of the flow (no
existing data), and the validation path where you submit each step wrong before
getting it right.

Record what you could not reach (a state behind data you don't have, a step
requiring a second user or a real payment) and say so in the preview. Never
illustrate a state you did not observe.

**Evidence rule:** every finding names the screenshot, the viewport, and the
action that produced it. A claim with no shot behind it does not go in.

## 4. Judge, then propose

Run the UX skill's **Visual consistency check** and **Intentional visual
restraint check** against the observed UI — the rendered pixels, not the plan
or the code — using its `Pass` / `Needs decision` / `Issue` / `Not applicable`
statuses.

The checklists catch defects. They are the floor, not the output. Also ask, per
screen: what is this screen for, what decision or action is the user here to
make, and what in the current design gets in the way? The best proposal is
usually about hierarchy, sequence, or what to cut — not a control that is three
pixels off.

For a flow, judge the **shape of the task** before any single screen, because a
step that shouldn't exist cannot be fixed by aligning it:

- **Does every step earn its place?** Merge, reorder, default, infer, or defer
  anything the user cannot answer confidently at that moment.
- **Is the order the user's order?** Ask for what they came with first; push
  configuration after the thing exists.
- **Is the commitment honest?** The user should know how long this is, what is
  required versus optional, and what happens on submit — before they start.
- **Is it survivable?** Cancel, back, reload, and a failed submit should never
  cost typed work without saying so first.
- **Does it end?** Success should name the result, show where it lives, and
  offer the obvious next action.

Say plainly when the right fix is fewer steps rather than better ones.

Rank proposals by leverage, and lead with the top three. Each one states:

- **What's wrong** — with its evidence.
- **Why it matters** — the user cost, not the rule number.
- **The change** — specific enough to build, in the project's existing tokens
  and components.
- **Cost and blast radius** — one screen or the whole design system.
- **What it doesn't fix** — so the user can weigh it honestly.

The restraint check applies to your own proposals too: no gradients, shadows,
hero type, bento grids, or cardification arriving as "polish". If a proposal
needs a genuinely new pattern, say so and justify it.

## 5. Publish the preview

Follow `skill://preview`. Slug: `<project>-ui-<area>` (e.g.
`annury-ui-settings`). Shape the page for reacting, not reading:

- **TL;DR** — the three biggest wins, before any detail.
- **One `<section>` per screen or per step**, with a stable id you'll recognise
  in annotation feedback: the screenshot as a `<figure>` (linked to the
  full-size image, `loading="lazy"`, `data-pa-zoom` for dense shots), what's
  wrong under it, then the proposal. Use `.shot-grid` for desktop/mobile pairs
  and tabs for before/after or state comparisons.
- **For a flow, open with the step map** before the per-step sections: a
  mermaid flowchart of the walk as it exists today — every step, branch,
  cancel, and failure path you actually hit — and, when you propose a different
  shape, the proposed map beside it in tabs. Sections then run in step order,
  numbered as walked, so the page reads as the task. Keep the flow-level
  proposals (what merges, what goes) above the per-step ones; a reader who
  accepts a step's removal should not have to read its polish notes first.
- **Build the "after"** for the top proposals as a static variant HTML file in
  the slug folder, styled with the project's real tokens, and put it next to
  the screenshot. A rebuilt screen beats a paragraph describing one. For
  several directions, use the preview skill's variant-gallery layout.
- **The two checklists** in a collapsed `<details>` accordion — full results,
  out of the way of the proposals.
- **`data-question`** only where two readings lead to materially different
  work. Roughly three is plenty; decide the rest yourself and state the
  assumption.
- **Untested surface** listed explicitly in its own section.
- **`narration.md` + `~/.preview/_skill/bin/narrate <slug>`** — this is a page
  that asks for decisions, so it gets audio.
- **Implementation launchers** only when the set of proposals is large and
  ready to build; the plan ref is the preview URL.

Before handing over the link, run the preview skill's self-check probe and open
your own page in `agent-browser` to look at it — light and dark.

## 6. Hand back

Reply with the link, the top three proposals in one line each, and what you
could not test. Nothing else.

## Boundaries

- **No application code changes here.** When the user approves and asks for
  implementation, follow the preview skill's *From approved preview to
  implementation*: write the markdown UX handoff plan first, keep this session
  as orchestrator, delegate slices with the UX rule pack.
- **No tickets** unless the user asks for them.
- **No re-grilling.** This skill observes and proposes; it does not walk the UX
  skill's Grill-mode question tree.
