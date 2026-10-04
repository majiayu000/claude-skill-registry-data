---
name: motion-check
description: Use when a motion video has been rendered, before showing it to anyone, or when asked to check, review, critique or QA a rendered film.
---

# Motion check

ENGINE is `../../engine/`; checks are defined in `../motion-video/checks.md`. `<slug>` is the film folder (index.html, timeline.js, film.mp4).

1. `PY ENGINE/film.py check <slug>` (with the same `SIZE=` the film was rendered at): every check that applies (the list is in checks.md; `lufs` is loudness). Keep its JSON.
2. For every shot with a move over 15 px a frame or a morph swap, `PY ENGINE/film.py strip <slug> <seconds>`.
3. Open contact.png, the strips, phone_01.png, first.png and poster.png. Look properly.
4. Score 1-10 on the eight axes of the scored critique in checks.md: hook · readability · composition · motion · variety · brand · sound · polish, each beside its measured check. Hunt for the banned defaults in CLAUDE.md, dead beats, blurry scaled text, overlapping swap text, loop stutter, invented UI or numbers.
5. Append to `<slug>/review_log.md`: date, scores, the 3 worst problems as `Problem: <what, shot + beat> / Wanted: <result>`.
6. Report: the check JSON's failures verbatim, the scores, the 3 problems, and what a human must listen to.

Review only: never edit index.html, timeline.js or clips. Fixing belongs to whoever built the film.
