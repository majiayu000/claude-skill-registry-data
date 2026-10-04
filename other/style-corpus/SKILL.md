---
name: style-corpus
description: The offline LEARN phase of the style-replication loop. `learn <url|file>...` downloads each Group C exemplar short (yt-dlp, media into gitignored work/_style/<id>/), profiles it sidecar-free via profile-clip (vision ON), and stores the small JSON Style Profile in references/profiles/ (checked in); `distill` aggregates every profile into references/targets.json — per-field robust distribution targets (median + MAD-derived sigma, floored at 10% of the median) with each levered field carrying its code lever, so the style-gate can compare our span 0 against a DISTRIBUTION of good shorts instead of overfitting one exemplar; `show` prints the targets. Deterministic distill, non-fatal per exemplar, idempotent (profile-clip's .ppmeta makes re-learn a no-op on unchanged media).
---

# style-corpus

```bash
bash .claude/skills/style-corpus/style-corpus.sh learn <urlC1> <urlC2> ...
bash .claude/skills/style-corpus/style-corpus.sh distill
bash .claude/skills/style-corpus/style-corpus.sh show
```

`references/targets.json`: `{style_profile_version, n, clips[], fields:{"cuts.cuts_per_min": {median, sigma, n, lever, invert} | {median, sigma, n, diagnostic:true}}}`.
Only levered fields participate in the style-gate match; diagnostic fields are
reported but can never fail the gate (the unreachable-target protection —
production facts like multicam/staged are measured, not chased).

The gate self-arms: `style-gate` no-ops until `targets.json` exists with
`n >= SG_MIN_REFS` (default 3). Env: `STYLE_REFS` (corpus dir, default
`references/`).
