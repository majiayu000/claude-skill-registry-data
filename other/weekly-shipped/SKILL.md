---
name: weekly-shipped
description: >-
  Summarize what shipped to `main` over the last week as a concise, human-
  sounding end-user report. Use when the user wants "this week's shipped
  improvements", "top things that landed", or a weekly release-style recap from
  git history, especially when they want the answer framed around everyday user
  impact instead of commit mechanics.
---

# weekly-shipped

This skill turns a week's worth of shipped commits into a short report that reads like a person wrote
it, not like a release-note generator dumped a template.

## What this is for

- Weekly "what shipped" recaps from `main`
- "Top 3/5/10 improvements that landed"
- End-user framing: what changed, what got easier, what got safer, what got less annoying
- Founder/operator updates where commit detail matters less than practical impact

## What this is not for

- A raw commit log
- A PR-by-PR changelog
- A code review
- A roadmap or "what's next" memo unless the user asks for that separately

## Workflow

1. Pull the shipped window from `main`, not the current feature branch.
   Use exact dates when the user says "this week", "last week", or similar.
2. Cluster commits into improvements.
   A good report item usually maps to a fix/theme/outcome, not a single tiny commit.
3. Rank by user-facing consequence.
   Prefer reliability, safety, usability, cost, clarity, and time-saved over internal cleanup.
4. Write from the outside in.
   Start with what changed for a normal user, then explain why it matters.
5. Write the finished report to `PROJECT/3-COMPLETED/WEEKLY-YYYY-MM-DD.md`.
   The date in the filename is the date the report is generated, not the start of the shipped window.

## Sourcing

Default starting point:

```bash
git log main --first-parent --since="<start>" --until="<end>" --oneline
git log main --since="<start>" --until="<end>" --stat --format='%h %ad %s' --date=short
```

Use `--first-parent` when the question is about what actually landed on `main`. Drop to fuller history
only when you need extra detail to understand a merged theme.

Two gotchas that silently produce a truncated or stale window:

- **`--since`/`--until` can prune too early.** If the first-parent chain isn't perfectly
  date-monotonic (a merge pulling in an older branch), `git log --since=X` can stop walking before
  reaching commits that are actually in range, with no error or warning. If the returned list looks
  suspiciously short, cross-check with a plain `git log <ref> --first-parent -20 --format='%h|%ad|%s'
  --date=short` (no since/until) and pick the boundary commit by eye, then use a `<boundary>..<ref>`
  range instead of date flags.
- **A local `main` can be behind `origin/main`.** Check `git rev-list --count main..origin/main`
  (or `git log main..origin/main --oneline`) before trusting local history. If it's behind, fetch or
  read `origin/main` directly rather than reporting stale content as this week's ship list — don't
  push/reset local `main` to "fix" it.

If the repo maintains a human-authored `CHANGELOG.md` (or similar) with one entry per shipped change,
check it before falling back to raw commits — it's usually already clustered and written in plain
language, which is closer to the report's final shape than a commit log is.

## How to choose the top items

Prefer items that changed one of these:

- The default path got more reliable
- The tool became safer to trust
- Setup or usage got easier
- Output got easier to understand
- Cost or surprise went down

Skip items that are mostly:

- bookkeeping
- doc reshuffles with no user-visible effect
- tiny follow-ups unless they close a painful edge case

## Writing style

The report should sound natural even though the process is structured.

- Do not sound like a release-note template.
- Do not repeat the same sentence frame in every item.
- Do not open every second paragraph with the same stock phrase.
- Vary the rhythm: one item can lead with the pain removed, another with the new behavior, another with the downstream effect.
- Prefer concrete language over abstract praise.

Avoid robotic filler like:

- "Users should care because ..."
- "This improvement enhances ..."
- "This feature provides ..."
- "Net impact:"
- "Overall, this means ..."

Instead, write more directly:

- "The default path is less brittle now."
- "This cuts a common failure case."
- "The tool is less likely to surprise you here."
- "Reading the output takes less work."

## Output shape

Unless the user asks otherwise:

- Write the report to `PROJECT/3-COMPLETED/WEEKLY-YYYY-MM-DD.md`
- Use the current local date for `YYYY-MM-DD`
- Make the file Markdown
- Start with a short title that names the shipped window
- Use a numbered list
- One improvement per item
- Lead with the shipped improvement itself
- Keep each item short
- Frame it in everyday-user terms, not implementation trivia

Example output path on July 17, 2026:

`PROJECT/3-COMPLETED/WEEKLY-2026-07-17.md`

Good pattern:

1. **What shipped.** One or two sentences on the visible change.

   One short paragraph on why that change matters in normal use.

Bad pattern:

1. "Commit X changed Y and Z and then commit A updated B and then commit C..."

## Tone

- Crisp, not breathless
- Specific, not generic
- Calmly opinionated about why something matters
- No hype
- No canned "why you should care" wording unless it genuinely fits that one item

## Final check before writing

Before writing the file and returning its path, scan for repetition:

- repeated openers
- repeated "this means" constructions
- repeated "users" phrasing
- too many items with the exact same two-paragraph cadence

If it sounds patterned, rewrite for variation before sending.
