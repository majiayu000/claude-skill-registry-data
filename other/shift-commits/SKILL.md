---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: shift-commits
description: >
  Rewrite git commit timestamps to shift weekday before-5PM commits to after 5 PM.
  Use when the user wants to shift, rewrite, or adjust commit times so they appear
  to be made after working hours. Supports dry-run preview, date range filtering,
  and deterministic per-commit hour assignment.
---

# shift-commits

Rewrites git history so weekday commits appear after working hours.

**How it works:** groups commits by day. Finds the earliest commit on each weekday.
If it's before the target hour (default 17:00), computes `delta = target - earliest`
and shifts ALL commits on that day by the same delta. This preserves relative ordering
within each day.

Commits before the day boundary (default 6 AM) are treated as belonging to the
previous calendar day. A 00:56 commit is a late-night session, not an early morning
one, so it gets grouped with yesterday and doesn't inflate today's delta.

Weekend commits and days where all commits are already after the target hour are untouched.

```bash
# Preview what would change (default is dry-run)
bun ~/.config/opencode/skills/shift-commits/shift-commits.ts --after 2026-07-06

# Actually rewrite history
bun ~/.config/opencode/skills/shift-commits/shift-commits.ts --after 2026-07-06 --run

# Custom target hour (default 17)
bun ~/.config/opencode/skills/shift-commits/shift-commits.ts --after 2026-07-06 --target-hour 18 --run

# Custom day boundary (commits before this hour count as previous day, default 6)
bun ~/.config/opencode/skills/shift-commits/shift-commits.ts --after 2026-07-06 --day-boundary 5 --run
```

After rewriting, verify with `git log` and force push with `git push --force`.

A backup ref is saved automatically so you can recover if anything goes wrong.

## Important

- This rewrites history. Every commit from the start date onward gets a new SHA.
- You must force push afterward.
- Open PRs referencing old SHAs will break.
- Always preview first (default behavior without `--run`).
