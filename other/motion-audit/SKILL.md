---
name: motion-audit
description: Use when asked to audit the studio or workspace, what is out of date, what can be cleaned up, or the state of all films at once.
---

motion-review, workspace-wide, plus what only shows across films. Rank findings: blocking first, then by size.

## Run first
`python3 ENGINE/audit.py <workspace>` (ENGINE is `../../engine/`). It walks every folder with index.html + timeline.js, lints each, and adds the workspace findings. Keep every line. Then run motion-review's judgement on the one or two films with the most blocking findings, and read kit/AUDIO.md yourself.

## Tags
Blocking:
- `rule:` a film with motion-review blocking findings. Name the tags.
- `stale:` film.mp4 older than its index.html, timeline.js, motion.js, mix or shots: what ships isn't what the code says.
- `unchecked:` a render with no checks since, or with failing checks. Quote the failures.
- `license:` a kit file with no row or no licence link in kit/AUDIO.md.

Polish:
- `drift:` a film's motion.js differs from the engine's: engine fixes don't reach it. Update deliberately, then re-render and re-check.
- `legacy:` a film with its own inline engine. Leave it if it ships; never copy it into new work.
- `critique:` rendered with no review_log.md: nobody scored it.
- `orphan:` screenshots nothing references. Give the count and size.
- `clean:` build/ leftovers. Give the size; render recreates them.
- `recipe:` a render with no recipe.json: nobody can prove it rebuilds. Re-render with the current engine, then `film.py replay`.

Verify:
- `unrendered:` a film with no film.mp4 yet.
- `unused:` kit sounds no film uses. Fine to keep.

## Output
One line per finding, ranked: `<tag> <what>. <fix>. [path]`.
End with `films: <N> · blocking: <B> · polish: <P> · verify: <V>` (sizes are on the orphan and clean lines). Nothing found: `films: <N>. Studio clean. Ship.`

## Boundaries
Scope: rule compliance, freshness, provenance and housekeeping across the workspace. How a film looks is motion-check's job. Never deletes, re-renders or edits: it lists. One-shot.
