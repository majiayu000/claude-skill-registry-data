---
name: archdeck
description: >-
  Animated explainer slides for programming videos — turns one technical
  problem (backend, database, system design, frontend, infra) into a deck of
  1920×1080 HTML scenes that teach the mechanism: requests travel, scans
  crawl, races interleave, the bottleneck lights up. Picks a story arc,
  drafts a storyboard with one shared fact sheet (same data, consistent
  numbers on every slide) for your approval, then renders standalone
  per-slide HTML plus one single-file deck with step-by-step
  reveals, speaker notes, and a clean recording mode, to
  out/archdeck/<slug>/. No codebase needed. Use for "make slides explaining X
  for my video", "animated architecture slides for a tutorial", "turn this
  system design problem into a presentation" — e.g. "/archdeck keyset vs
  offset pagination". For docs and mermaid diagrams of a real codebase use
  blueprint; to be taught a topic interactively use learn.
---

# archdeck — architecture explained in scenes

`/archdeck <problem>` — new deck from a problem statement
`/archdeck <slug> edit <what to change>` — revise storyboard + affected slides, rebuild
`/archdeck <slug> build` — re-lint and rebuild `index.html` after hand edits

Answer one question: **what sequence of pictures makes a viewer *see* why
this design works — and where it stops working?** The failure mode of
generated tech slides is a bullet list with boxes: topics as titles, every
idea on screen at once, numbers that change between slides, motion as
decoration. The countermeasures are structural: a story arc chosen first, a
fact sheet every number comes from, one claim and one focal point per
slide, and steps that follow causality.

## Step 0 — Brief

Get the date with `date +%F`. Derive a short kebab-case `<slug>` from the
problem. If `out/archdeck/<slug>/` exists, read its `storyboard.md` and
resume (or run the requested `edit`/`build`) instead of starting over.

Infer from the request, defaulting sensibly:

- **Language** — the language the user wrote in (badges and copy follow it).
- **Audience** — mid-level developer unless stated.
- **Length** — 10–14 slides (~1 min each) unless stated.
- **Voices** — narrator only; a two-voice dialogue (learner `S`, presenter
  `J`) when the problem has a "why are we doing this" pivot.
- **Theme** — drafting paper (light, most legible after video compression);
  blueprint (dark) on request.

Ask at most one round of questions, and only for what would change the arc:
the scenario if the problem is too abstract to make concrete ("caching" →
caching *what*, for *whom*?), or the takeaway if the user clearly has one in
mind. Otherwise proceed and state your assumptions in the storyboard.

## Step 1 — Get the mechanism right

There is no codebase; correctness comes from you. Work out the mechanism
end to end before any slide: what reads what, in what order, at what cost.

Build the **fact sheet** (format in `references/storyboard-template.md`): one
concrete scenario, realistic scale with the arithmetic shown, sample
entities reused on every mock, and the engine/version for any behavior that
varies (InnoDB vs Postgres, HTTP/1.1 vs 2, React 18 vs 19). If web search is
available, verify version-specific claims and defaults; if not, mark them
under "Claims to double-check" so the user can verify before recording.
Wrong numbers in a tutorial are worse than none.

## Step 2 — Pick the arc

Read `references/narrative-arcs.md`. Choose one arc, then write the brief:
misconception, aha, decision rule. Map beats to slides. The arc is where
"better than a list of slides" happens — a pivot, predict-pauses every 3–4
slides, a side quest that comes back, an ending that says *when* to use
what.

## Step 3 — Storyboard → approval gate

Write `out/archdeck/<slug>/storyboard.md` per
`references/storyboard-template.md`: per slide the claim-title, archetype,
concrete on-screen content, numbered steps with their motion, focal point,
bottom line, narration per step, and the bridge to the next slide. Choose
archetypes from `references/archetypes.md` — at least five different ones
per deck.

Show the brief and the one-row-per-slide table in chat and **wait for a
yes**. Apply requested changes to the file and re-show only what changed.
Rewriting a storyboard line costs seconds; re-rendering a slide costs
minutes. If the user said not to ask ("just make it"), note that and go on.

## Step 4 — Render

Read `references/visual-language.md`, `references/archetypes.md`, and
`references/animations.md`. Then:

1. Copy this skill's `assets/deck.css` and `assets/deck.js` into
   `out/archdeck/<slug>/assets/` (reuse the copies already there on an edit —
   the user may have tuned them).
2. For each slide write `out/archdeck/<slug>/slides/NN-<slide-slug>.html`
   starting from this skill's `assets/slide-template.html`: same `lang`,
   `data-theme` and deck `data-title` in every file; the archetype markup;
   `data-step` reveals exactly as storyboarded; narration in `.notes` with
   matching `data-step`s.
3. Rules that keep slides honest:
   - Every name and number comes from the fact sheet.
   - Only `deck.css` classes and tokens — inline style only for coordinates
     and motion knobs (`--x`, `--y`, `--at`, `--v`, `--d`, `--t`…). New
     visual needs go into a `<style>` block scoped by `[data-slug="…"]`.
   - Diagrams: explicit px size, matching SVG `viewBox`, shared arrowheads
     (`url(#ad-arrow)`, `-problem`, `-fix`…) — no per-slide `<defs>`, and
     any `id` prefixed with the slide number.
   - Code and queries are valid for the named dialect/version.
   - Nothing loads from the network except the Google Fonts that
     `deck.css` already imports — no CDNs, remote images, or scripts.

## Step 5 — Build and lint

```bash
python3 <this skill>/scripts/build.py out/archdeck/<slug>
```

It lints every slide (one section, a title, contiguous steps, narration per
step, no external resources, no duplicate ids, word budget), stamps each
slide's sheet number for its title block, then writes `index.html` (all
slides, CSS and JS inlined) and `notes.md` (the narration script, per
slide and step). Fix every ERROR and re-run; fix WARNs unless
the slide genuinely needs the words. Use `python` if `python3` isn't on
PATH.

## Step 6 — Look at it

Text that fits in your head can still overflow at 1920×1080. If a browser
tool is available, open `index.html#/N/99` (slide N at its last step) at a
1920×1080 viewport for every slide, screenshot, and fix overflow, overlap,
misaligned wires, and unreadable contrast; `window.archdeck.go(i, step)`
drives it too. Check step 0 of busy slides as well — the opening frame
must not give away the answer. If no browser is available, say the deck
was not visually checked.

Report in chat: the slide table (number · title · steps), the paths
(`index.html`, `slides/`, `notes.md`, `storyboard.md`), the claims still
marked to double-check, a reminder to open the deck once online before
recording (fonts load from Google Fonts and are cached after that), and the
controls:

```
→ / Space  next step     ← previous      ↓ ↑  next/prev slide    12⏎  jump
R replay step   F fullscreen   N notes   C clean (recording) mode   T theme
index.html?clean → record without HUD   #/5/2 → slide 5, step 2
```

## Edit mode

`/archdeck <slug> edit …`: change `storyboard.md` first, show the diff of
affected rows, then re-render only those slide files and rebuild. If the
fact sheet changes, find every slide that uses the changed value
(`grep` the old value in `slides/`) and update them all — a number that
changes on one slide but not the next is the bug viewers notice first.
