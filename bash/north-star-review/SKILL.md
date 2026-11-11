---
name: north-star-review
description: |
  Run the north-star review engine against every active thought in the
  project. The engine reads each thought's anti-patterns, greps the live
  codebase for hits, and emits a ranked list of suggested next-step
  contracts. Optionally updates the `Current gap` and `Suggested next steps`
  sections of each thought file in place.

  Use when: the user types `/north-star-review`, "what should we work on next",
  "review my goals", "show me how the codebase aligns with my aspirations",
  or wants a weekly/monthly check-in on long-horizon direction.
user_invocable: true
---

# /north-star-review — Read aspirations, compute gaps, emit suggestions

When invoked, run `.claude/scripts/north_star_review.py` and present the ranked output to the user.

## Step 1: Run the review

```bash
py -3 ".claude/scripts/north_star_review.py" --project <project-name>
```

Defaults: if no `--project` argument is provided, the script discovers every project under `.claude/north-stars/` and reviews them all. To review one project, pass the `project.name` slot of `.claude/project-profile.md` as the argument.

Optional flags the user may pass after `/north-star-review`:

- `--update` — rewrite the `Current gap` and `Suggested next steps` sections of each thought file in place. Without this flag, the script only prints; the files stay untouched.
- `--single <slug>` — review one thought only.
- `--repo-root <path>` — override the codebase root used for grep (defaults to the project's known location).
- `--json` — machine-readable JSON output.

## Step 2: Present the report

The script output already has the shape the user wants — pass it through verbatim. It lists, per active north-star:

- Title, slug, status
- Gap signals (count + concrete file paths from the anti-pattern grep)
- Suggested next steps (count + `/design-first` invocations to advance toward the aspiration)

## Step 3: Offer the update step

After presenting the dry-run, ask via `AskUserQuestion`:

> "Write these gap signals and suggested next steps into the thought files? (`--update` rewrites `Current gap` and `Suggested next steps` in each `.md`; the rest of each file stays verbatim.)"

If the user confirms, re-run with `--update` and confirm the writes landed.

## Step 4: Offer to act on top suggestions

For the ranked suggestion list, ask the user via `AskUserQuestion`:

> "Pick a suggested next step to draft now via `/design-first`, or skip."

Options should be the top 3 suggestions across all north-stars (one per north-star, prioritized by gap count). If the user picks one, invoke `/design-first` with the suggested task title — this hands off to the data-architect, which will then read the aspirations in its Step 0.5 and produce a contract that explicitly cites the north-star it advances.

## Step 5: If nothing actionable, say so

When all north-stars return zero gap signals (no anti-pattern hits in the codebase), tell the user:

> "All active north-stars are unblocked at the file-grep level. No anti-patterns currently in the codebase. Next move is to define richer anti-patterns OR to add feature work that ACTIVELY advances each aspiration — not remediation. Re-run after the next contract lands."

## Notes on the engine

The script is fail-soft: missing CodeGraph CLI, missing repo, parse errors — all degrade gracefully and emit warnings to stderr. The script never modifies anything without `--update`.

## What this skill does NOT do

- Does NOT create new north-stars — use `/north-star "<aspiration>"` for that.
- Does NOT promote a suggestion into a contract automatically — the user must invoke `/design-first` explicitly after picking from the suggestion list.
- Does NOT modify thought files without `--update`.

## Periodic auto-review

The user can schedule this skill via `/schedule` or a CronCreate-style routine for weekly runs. The recommended cadence: weekly on Monday morning, with `--update` enabled so the thought files accumulate a longitudinal gap-signal history.

```
/schedule "Weekly north-star review" --cron "0 9 * * 1" --command "/north-star-review --update"
```

Output of scheduled runs lands in stdout — pair with the existing notification pipeline to surface the gap-signal changes vs the previous week.
