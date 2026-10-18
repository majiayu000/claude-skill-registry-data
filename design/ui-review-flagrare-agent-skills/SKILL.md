---
name: ui-review
description: "Full UI pass on one screen, dialog or flow: runs /flagrare:ux-audit, /flagrare:design-review and /flagrare:interaction-polish together, in that order, on the same browser session and the same screenshots, then ships ONE findings report (a single severity-ranked list, each finding tagged UX / Design / Interaction, overlaps merged) followed by the fixes it applied and the principle behind each. The first-time-user walk drives the real UI and gathers the evidence; the design lens diagnoses those screenshots (system coverage inventory, squint test, subtraction, ranked top 3); the interaction lens works on the interactions the walk found (press feedback, loading and transition states, frequency-gated motion, reduced motion). When a demo or before/after is part of the output it ships an MP4 recorded in real time with a visible cursor, never a GIF stitched from screenshots. Use when the user says 'UI review', 'review this screen', 'full pass on this page', 'audit and polish this', 'design and UX pass', 'make this screen good', 'run all three UI skills', or names one screen and asks for UX, design and feel in one go. Use a single source skill instead when only one lens is wanted."
---

# UI Review

One target, three lenses, one report. A first-time user walks the screen, a senior product designer reads what the walk captured, an interaction designer tunes how it feels, and the result is a single ranked list with the fixes applied.

> **No em-dashes.** Nothing this skill writes may contain an em-dash; use a comma, colon, or parentheses instead. Enforced by a repo hook. See `/flagrare:write-docs`.

This skill orchestrates three existing skills in sequence. It does not duplicate their logic: each one's rules still apply in full, and this file only says how they share evidence and how their findings merge.

---

## When to Use

- The user names one screen, dialog or flow (running locally, or a URL) and wants usability, visual design and feel reviewed together
- After building a non-trivial UI, before handing it to design or review
- "UI review", "review this screen", "full pass on X", "audit and polish this", "make this page good"

Use a single source skill when only one lens is wanted. For a whole app with many routes, run `/flagrare:ux-audit` alone first; this skill is for one target at a time.

---

## Rules carried from the source skills

Each of these governs its phase exactly as written in its own skill. Read the section there, do not paraphrase it away.

- **Coverage discipline** (`/flagrare:ux-audit`): the scoped area is walked exhaustively, every state and every visible affordance, no "seen enough". Scoped narrows *what* is covered, never *how thoroughly*.
- **First, respect the design system** and **remove, then demote, then quiet** (`/flagrare:design-review`): every fix uses the project's tokens and components, and quieting competitors comes before adding emphasis.
- **First, do no harm** and the **frequency gate** (`/flagrare:interaction-polish`): nothing on the user's path waits on motion, high-frequency actions get little or no animation, and every animation ships with its `prefers-reduced-motion` path.

---

## Workflow

### Step 0: Lock the goal (anti-stall)

**Hard requirement.** Before invoking any sub-skill, you (the executing model) MUST call `/goal` yourself. This is a three-skill chain with a long walk in the middle; without a durable goal the model stops after the walk. Phrase it so the evaluator can judge it from your output:

> The target `<target>` has been walked with `/flagrare:ux-audit` (every state and affordance in scope), diagnosed with `/flagrare:design-review` and `/flagrare:interaction-polish` on the same screenshots, merged into `.ui-review/REPORT.md` with one ranked, lens-tagged findings list, the in-scope fixes applied and re-verified by fresh screenshots, and the hand-off message sent. Stop after 40 turns if not met.

**One goal per session.** `/flagrare:ux-audit` normally sets its own goal; the `called by /flagrare:ui-review` argument in Step 2 tells it to skip that. Do not re-set the goal between steps. If `/goal` is unavailable, proceed without it.

Also create a Todo list with one item per step below, plus one item per state of the target once Step 2 enumerates them.

### Step 1: Pin the target and the session

1. **Name the target** in one line: the route or URL, the screen or dialog, and for a flow, its start and end. Find its source files (the route file, the components it renders, the styles and tokens they use). A URL with no source in the repo is a report-only run: say so up front, the fixes become recommendations.
2. **Open one browser session** following `/flagrare:ux-audit`'s Prerequisites and Step 3 (Chrome DevTools MCP, one dedicated tab the user can watch, mobile-first viewport unless the target is desktop-only). This tab is the only one the three lenses use.
3. **Create `.ui-review/`** for all output: numbered screenshots, the UX lens's table, the merged report, and any video.

### Step 2: Walk it with `/flagrare:ux-audit`

Invoke `/flagrare:ux-audit` with arguments starting `called by /flagrare:ui-review`, then the target, the output folder, and the extra captures the other two lenses need:

```
called by /flagrare:ui-review, scope: <target>, out: .ui-review/,
also capture: every data state (empty, partial, full, error), hover, focus and pressed
on each control, loading states under a throttled network, the target with
prefers-reduced-motion: reduce emulated, and an interaction inventory
(each interaction: trigger, what feedback it gives now, how often a real user hits it)
```

The walk is the one and only pass through the UI. Every screenshot the later lenses look at comes from it. If a later lens needs a state the walk missed, go back in the **same tab** and capture that one state, numbered after the last shot, then note it in coverage.

**Wait for the walk to finish.** It returns its findings table, its coverage list, the interaction inventory and the screenshot paths, without its own hand-off message.

### Step 3: Diagnose the design with `/flagrare:design-review`

Invoke `/flagrare:design-review` with: `called by /flagrare:ui-review, diagnose only, screenshots: .ui-review/, source: <files>`. It works from the screenshot set (and the source, when there is one), not from a fresh walk. It returns its diagnosis without editing:

- the screen's one job and the user's priority order
- the system coverage inventory (every visual group named to a recipe, unmapped groups and unspent personality called out)
- the squint test result and the subtraction pass
- the ranked top 3, then polish

When the target is a URL with no token source to read, the design system is whatever the product already renders: read computed styles in the same tab (`get_css_styles`, `evaluate_script`) to find its scales, and hold fixes to those.

### Step 4: Diagnose the interactions with `/flagrare:interaction-polish`

Invoke `/flagrare:interaction-polish` with: `called by /flagrare:ui-review, diagnose only, interactions: <the inventory from Step 2>, screenshots: .ui-review/, source: <files>`. For each interaction it returns the frequency band, what it does now, and the 1-3 changes that move the feel the most, including changes that remove motion. It covers press feedback, loading and transition states, and the reduced-motion path, and it checks the reduced-motion screenshots from Step 2 rather than guessing.

### Step 5: Merge into one report

Write `.ui-review/REPORT.md` **before touching any code**, so the findings survive even if the fixes go wrong.

**One ladder.** Every finding gets a `/flagrare:ux-audit` severity (High, Medium, Low, per its `references/severity-rubric.md`). Design and interaction findings map onto it by what they cost the user: a primary action the squint test cannot find, or motion that makes the user wait, is High; contrast under the legibility gate, an undesigned group, a missing reduced-motion path or a control with no feedback on a frequent action is usually Medium; spacing off the scale or a weak easing curve is Low. Within a band, order by design-review's lever order: hierarchy, then clutter, then whitespace, legibility, alignment, tokens; interaction findings sort after design findings of the same band, because motion sits on top of the layout.

**De-duplicate.** Same location and same symptom is one row. Tag it with every lens that caught it, keep the highest severity any lens gave it, and keep the most concrete fix. Different symptoms in the same place stay separate rows.

**Fix boundary.** A finding is **in scope** when its fix lives in the target's own code: copy, labels, an empty-state call to action, tap targets, hierarchy, spacing, contrast, press feedback, transitions, the reduced-motion path. A finding is **for triage** when the fix changes navigation, spans other screens, needs a new design-system pattern the team has not agreed, or is a product decision. Triage findings are reported, never applied.

```markdown
# <Target> UI review: YYYY-MM-DD

**Target:** <route or URL, screen or flow> · **Viewport:** <size> · **Method:** one Chrome DevTools session; ux-audit walk, then design-review and interaction-polish on the same screenshots

## Summary

**The screen's one job:** <one sentence, from design-review>
**Findings: N** (X High, Y Medium, Z Low) · UX a · Design b · Interaction c · merged across lenses d

1. **<Top finding>** (<id>, <lenses>), one line on what is wrong and why it matters
2. ...
3. ...

## Findings

| # | Severity | Lens | Location | Issue | Why it matters | Fix | Status |
|---|----------|------|----------|-------|----------------|-----|--------|
| 01 | High | UX, Design | `/checkout` pay button | ... | ... | ... | Applied |

## Applied fixes

| # | What changed | Principle | Where |
|---|--------------|-----------|-------|
| 01 | Demoted the two secondary buttons to text links | Emphasize by de-emphasizing (design-review) | `CheckoutFooter.tsx` |

## For triage (not applied)

- <id>: <finding>, and why it is outside this target's code

## Coverage

- States covered: ...
- Not tested: ...

## Evidence

Screenshots in `.ui-review/`, before/after video `.ui-review/before-after.mp4` (when recorded)
```

### Step 6: Record the "before", when a demo is part of the output

If the user asked for a demo or a before/after, or the main fixes are interactions that a still image cannot show, record the **before** now, while the code is untouched. Follow `references/demo-video.md`: a short Playwright script replays the interaction with `recordVideo` and a visible cursor, in real time, and ffmpeg converts it to MP4. This is a replay of one scripted path, not a second walk.

Never assemble a GIF from screenshots. A stitched GIF drops the timing, which is exactly what an interaction fix changes, and reads as a slideshow.

### Step 7: Apply the in-scope fixes

Apply in this order, because each layer depends on the one before it:

1. **Content and structure** from the UX lens: copy, labels, missing calls to action, dead ends inside the target. Hierarchy cannot be judged on copy that is about to change.
2. **Design** in design-review's lever order: hierarchy, subtract and de-clutter, whitespace and rhythm, legibility, alignment, tokens.
3. **Interaction** last, per interaction-polish's workflow: CSS-first, `transform` and `opacity` only, named properties, reduced-motion variant, hover gated behind `(hover: hover)`.

Explain each change in a line, naming the principle (the source skills do this as they go), and fill the Applied fixes table as you go. If a fix turns out to need something outside the target, stop, move the finding to triage, and say why.

### Step 8: Verify in the same session

Re-capture every state that a fix touched, in the same tab, numbered after the walk's shots (`NN-after-<state>.png`). Re-run the squint test on the after shots. Re-check the reduced-motion state. Press every control whose feedback changed. A fix that did not show up on screen is not applied: fix it or mark it so in the report.

If Step 6 recorded a before, record the **after** with the same script, then combine both into one side-by-side MP4 (`references/demo-video.md`). Watch it once end to end before shipping it.

### Step 9: Hand off

End with one short message:

- Path to `.ui-review/REPORT.md`, and the video when there is one
- Count by severity, and how many were applied versus left for triage
- The top 3 findings, one line each
- An explicit "I did not test: ..." list

---

## Anti-patterns

- **Walking the UI three times.** One session, one screenshot set. The design and interaction lenses read what the walk captured; a missing state is captured once, in the same tab.
- **Letting `/flagrare:ux-audit` set its own goal.** It would replace this skill's goal and the chain would stop after the walk.
- **Three reports stapled together.** The deliverable is one list with one severity ladder. Separate per-lens sections bury the overlaps the merge exists to find.
- **Fixing before the report is written.** The report goes to disk first; the fixes are measured against it.
- **Applying triage findings.** A navigation change or a new pattern needs the team, not a drive-by edit inside one screen.
- **A GIF of screenshots as the demo.** Real-time MP4 with a visible cursor, or no demo.
- **Animating the high-frequency path because a lens found it "stiff".** The frequency gate decides, not the finding.

---

## Flow position

```
/flagrare:ui-review <target>
     |
     v
[Step 0: /goal locked, spans the chain]
     |
     v
[Step 1: one Chrome DevTools tab, .ui-review/]
     |
     v
/flagrare:ux-audit (called by ui-review)    <- the one walk: screenshots, states,
     |                                         interaction inventory, UX findings
     v
/flagrare:design-review (diagnose only)     <- same screenshots: inventory, squint,
     |                                         subtraction, top 3
     v
/flagrare:interaction-polish (diagnose only) <- the inventory: frequency gate, press,
     |                                          loading, reduced motion
     v
[Step 5: REPORT.md, one ranked list, lens-tagged]
     |
     v
[Step 6: before MP4, if a demo is wanted]
     |
     v
[Step 7: apply in-scope fixes: content → design → interaction]
     |
     v
[Step 8: re-capture in the same tab, after MP4]
     |
     v
[Step 9: hand off]
```
