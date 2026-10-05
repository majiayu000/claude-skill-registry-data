---
name: writing-beats
category: writing
description: >
  Shape an article as a journey of beats, choose-your-own-adventure style — write one beat,
  offer pivots, repeat until it ends. Use when the user has raw material and wants it
  assembled as a narrative rather than an argument.
codex-short-description: "Shape an article as a journey of beats, choose-your-own-adventure style"
related-skills:
  - writing-shape
  - writing-fragments
  - writing-humanize
loop-eligible: false

compatibility: claude-code codex opencode
---

<what-to-do>

The user has passed (or will pass) a markdown file of raw material.

If the user did not say where to save the article, ask once and remember the path.

Then run a beat-by-beat journey:

1. Write 2–3 candidate **starting beats**, drawn from the raw material. Each is a different entry point into the article. Show the user the beats before writing it to the article file. The user picks one.
2. Once the user picks a starting beat, write **only that beat** to the article file. A beat may be one sentence or several paragraphs — whatever that beat naturally is. Stop there.
3. Re-read the article file from disk. Then offer 2–3 candidate **next beats** — different directions the journey could pivot to from where the article now stands.
4. Loop steps 2–4 until the article reaches a natural end.

</what-to-do>

<supporting-info>

## What is a beat

A beat is one move in the journey. It does one thing — sets a scene, lands a point, asks a question, tells a small story, drops an aside, twists the angle. Then it stops, leaving the reader at a place where the next beat can pivot.

A beat is sized by what it needs:

- A single sentence if that's all the move is ("And then nothing happened for three weeks.").
- A short paragraph if the move needs setup.
- Multiple paragraphs if the beat is a self-contained vignette, argument, or example.

If a "beat" needs five paragraphs and three subheadings, it's not a beat — it's two beats glued together. Split it.

## Offering candidate beats

Each candidate should be genuinely different — different angle, different tone, different move. Not three flavours of the same paragraph. The user is choosing a _direction_, so the choices need to diverge.

Format the offer like a menu:

```
Where do you want to start?

1. **Open with the failure.** Drop the reader into the moment it broke —
   the bug, the silence, the wrong number on the dashboard. Hooks on shock.

2. **Open with the contradiction.** State the thing everyone believes,
   then state the thing that turns out to be true. Hooks on curiosity.

3. **Open with the small scene.** A specific morning, a specific
   conversation. Hooks on intimacy.
```

Sketch the move, not the prose. The user picks a direction; you write the prose afterward.

Always end the menu with your recommendation and a one-line reason. Don't sit on the fence — pick one. Example: "I'd go with **2** — the contradiction sets up the strongest through-line for what's in the pile." The user can override; they usually won't, but they need your read.

## Writing one beat

Once a beat is picked, write _that beat only_ to the article file. Do not write the next beat. Do not foreshadow the next beat. Do not write transitions out of the beat — the next beat will pivot, and pivots are written when their beat is written.

Pull material from the raw pile to populate the beat. You can paraphrase, split, recombine, or quote. The pile is a quarry.

If the beat needs something the pile doesn't have, name the gap before writing: "this beat wants a concrete example and the pile doesn't have one — give me one or pick a different beat."

## Pivoting to the next beat

After the user has edited, re-read the article file. The article may have changed in ways that change what the next beat should be. Then offer 2–3 candidates again.

The candidates should respect the article so far. Useful pivot moves:

- **Continue** — push further in the same direction, deepen what's there.
- **Contrast** — introduce the opposite, the counterexample, the doubt.
- **Zoom in** — narrow to a specific case, scene, or detail.
- **Zoom out** — widen to the broader implication or pattern.
- **Aside** — break the fourth wall, drop a tip, add a footnote-shaped paragraph.
- **Pivot hard** — deliberately change subject, trusting the connection will land later.

Mix the candidates. If you've offered three "continue" options in a row, force a contrast or zoom into the next menu.

## Ending the journey

The article ends when the journey is complete — not when the pile is empty. Most piles will have leftover fragments that don't make it in. That is fine; that is the point of having more raw material than you need.

When you sense an ending is near, say so: "we could end on the last beat, or add one more that lands the takeaway — which?" Let the user decide.

## Writing rhythm

- Append one beat at a time. Never write ahead.
- Re-read the article file from disk before every write. Preserve user edits absolutely.
- If the user edits a previous beat substantially, let it change what comes next. The journey is alive.
- If the user says "rewrite that beat" or "go back and try a different beat 3", do it — edit in place, leave the rest alone.

## Out of scope

- Outlining the whole article up front.
- Writing multiple beats in a single turn.
- Editing the raw material file.
- Imposing a fixed structure (intro/body/conclusion). The structure is whatever the journey turns out to be.

</supporting-info>

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/writing-beats.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
