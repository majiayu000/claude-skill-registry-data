---
name: motion-director
description: Use when a motion video is longer than about 90 seconds, needs several agents, is expected to run over an hour, or is resuming after a usage limit or crash.
---

# Motion director

ENGINE is `../../engine/`. The film is `<slug>/`. The parent session is the director: it owns shared files and never builds a clip itself.

## production.json (the director's state; create it first)
```json
{"slug": "...", "style": "...", "step": "brief",
 "steps": ["brief", "capture", "stills", "animatic", "clips", "film", "checks", "formats", "export"],
 "clips": {"hook": {"owner": "agent-1", "state": "todo", "file": "clips/hook/"}},
 "budget": {"maxRenders": 20, "renders": 0},
 "decisions": []}
```
- Advance `step` only when its gate passes. Append every user decision verbatim to `decisions`, with the date.
- On resume (new session, after a usage limit, after a crash): read production.json and `review_log.md`, re-run the current step's check, continue. Never restart a passed step.

## Steps and gates
| Step | Who | Gate |
|---|---|---|
| brief | director, via motion-brief | user OK on BRIEF.md + shotlist.md |
| capture | director, via motion-capture | every shot captured and looked at; facts.md complete |
| stills | director | user OK on 4-6 stills |
| animatic | director | `film.py render --animatic` + contact sheet; pacing notes fixed |
| clips | one motion-scene-builder per clip, all launched in one message | each clip passes two reviews in order (below) |
| film | director joins clips | lint clean; seams check looked at |
| checks | motion-critic | every measured check passes; every critique axis 8+, or 3 rounds logged |
| formats | director | each SIZE rendered and checked |
| export | director | `film.py export`; `film.py replay` IDENTICAL |

## Subagent playbook
- Before launching builders, write `ANIMATION_GUIDE.md` (motion.js helpers used, spring presets, type sizes, colour meaning, the handoff shape between each pair of clips) and a **seams table** in production.json: for each cut, the outgoing and incoming shape and its beat.
- Each builder gets one folder and a self-contained brief (scene prompt filled in, the seams it owns, facts it shows). Builders never edit shared files (timeline.js of the film, ANIMATION_GUIDE.md, facts.md): they report what they need changed and the director changes it.
- Builders write code in parallel, but only one renders at a time: parallel renders saturate the machine and slow every film. Record each one's result in production.json.
- Review every clip twice, in this order, and loop until both pass (a fix goes back to the same builder, then the same review runs again):
  1. **Spec review** (director): does the clip show exactly its shotlist beats, captured UI and facts.md rows, hand off through its seam shapes, and add nothing unasked? Checked against shotlist.md, facts.md and the seams table, not against taste.
  2. **Quality review** (motion-critic): `lint.py`, `film.py check`, and the scored critique.
  Never run quality review on a clip that fails spec review: polish on the wrong content is wasted renders.

## Effort and budget
- Medium effort for plans, stills and notes; xhigh for clips; max only for the hook and the payoff scenes.
- Every full render increments `budget.renders`. At the cap, stop and ask. Preview fixes with `--from/--to` (writes `part_F-T.mp4`, never `film.mp4`), `film.py mux` for sound-only changes, and animatics for pacing.

## Done when
`step` is `export`, every gate in the table is recorded as passed, and the director's report lists what was fixed, what it would still change, and what a human must listen for.
