---
name: obsidian-workout-export
description: Export workout data to an Obsidian-formatted Markdown file. Always trigger immediately when the user types "owd". Also trigger on "export workout", "obsidian workout", "save workout to obsidian", or related requests to export workout data into Obsidian. Read the current conversation first before searching prior conversation history. Name the file after the date of the chat that contains the workout data.
version: 1.1.0
---

# Obsidian Workout Export Skill

## Intent

Convert workout session data into clean Obsidian-ready Markdown logs with body stats, session details, PRs, and notes.

## Use When

- The user explicitly asks for `obsidian-workout-export`.
- The request matches the triggers or workflow described below.
- The task benefits from a reusable, structured output instead of a one-off answer.

## Do Not Use When

- Do not use for programming future training blocks, diagnosing injuries, or inventing workout details missing from the source.
- Required context is missing and cannot be reasonably inferred.
- A more specific skill in this repo is a better match.

## Validation Checklist

- [ ] The output matches the skill's intended task and platform.
- [ ] Required inputs, assumptions, and uncertainty are explicit.
- [ ] Safety, scope, and source limits are respected.
- [ ] The response follows the requested format or the skill's default output format.
- [ ] The result is practical enough to use without another cleanup pass.

Export logged workout sessions into Markdown files for an Obsidian `WorkoutData/` folder.

## Primary Trigger

Use this skill immediately when the user types `owd` in a chat that contains workout data.

Other triggers:

- `export workout`
- `obsidian workout`
- `save workout to obsidian`
- `workout to obsidian`
- `log to obsidian`

## Workflow

### 1. Locate the workout data

Always check the current conversation first. If the current chat already contains logged workout data such as exercises, sets, reps, weights, or body stats, use it directly instead of searching older history.

If the current chat does not contain workout data, search the most recent prior session using workout-related terms such as:

- `workout log sets reps`
- `leg press chest press fitness`
- `Day 1 Day 2 upper lower workout`

Use the date of the chat that contains the workout data as the filename date.

### 2. Extract all available session data

Pull every logged data point that is actually present.

**Session info**

- workout date
- day number and focus, for example `Day 2: Lower A`

**Exercises**

- exercise name
- weight
- sets
- reps
- PR flag when present

**Body stats**

- bodyweight in pounds
- body fat percentage

**PRs hit**

- each PR with weight and reps when available

**Session notes and flags**

- regressions
- injuries
- missed exercises
- anything else explicitly flagged in the session

### 3. Build the Markdown file

Use the filename `YYYY-MM-DD.md` based on the date of the chat containing the workout data.

Recommended structure:

```markdown
# Workout Log - [DAY NAME AND FOCUS]
**Date:** YYYY-MM-DD
**Program:** 15 Percent Body Fat Project

## Body Stats
| Metric | Value |
| --- | --- |
| Bodyweight | XXX lbs |
| Body Fat | XX.X% |

## Session - [Day X: Focus]

| Exercise | Weight | Sets | Reps | PR? |
| --- | --- | --- | --- | --- |
| Exercise Name | XXX lbs | X | X | yes or no |

## PRs Hit
- Exercise: XXX lbs / X reps

## Notes and Flags
- factual session notes, regressions, or flags
```

Omit sections with no data. If there are no PRs, either omit the section or state `None this session`.

### Template variants

Match the template to the session type instead of forcing everything into the strength table:

- **Strength session**: the default structure above.
- **Ride**: replace the exercise table with distance, duration, average and max speed or power, elevation, and route name when logged.
- **Run**: distance, duration, pace, and surface or route when logged.
- **Combined day**: one section per activity in the order trained, sharing the same body stats block.

Keep column names consistent across files of the same type so Dataview queries work across the whole `WorkoutData/` folder.

### Frontmatter metadata

Add YAML frontmatter so notes are queryable:

```yaml
---
date: YYYY-MM-DD
type: strength | ride | run | combined
focus: [day focus, e.g. Lower A]
duration: [minutes, if logged]
effort: [easy | moderate | hard, only if stated or clearly implied]
tags: [workout, plus activity tags like strength or cycling]
prs: [count, 0 if none]
---
```

Only include fields the log supports. Add a one-line progression note at the end of the file when the session data shows a clear change from the last comparable session, and skip it otherwise.

### Duplicate protection

Before producing the file, check whether this session was already exported in the current conversation. If the same date and session were exported before:

- ask whether to overwrite or skip, unless the user explicitly asked for a re-export
- when re-exporting with corrections, produce one complete replacement file rather than a partial patch
- if two different sessions genuinely share a date, suffix the filename with the focus, such as `2026-06-10-lower-a.md`

### 4. Output expectations

Produce the Markdown content directly unless the user specifically asks for a file to be created in a local repo or folder.

When you finish, confirm:

- the filename
- the session date used
- that the file is intended for the Obsidian `WorkoutData/` folder

## Rules

- Never fabricate data. If a field was not logged, omit it or mark it as unlogged.
- If sets or reps are ambiguous, preserve exactly what was logged.
- If weight is missing for an exercise, note it as `bodyweight` or `unlogged` when appropriate.
- Keep the output factual. It is a data record, not a journal entry.
- Tables should stay Dataview-compatible for Obsidian use.

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- A workout log and the destination note style or vault context if relevant.

Example prompts:

- `Use obsidian-workout-export to turn this workout log into an Obsidian ready Markdown note.`
- `Export these strength and cycling notes into a clean workout entry for my Obsidian vault.`
- `Show me an example prompt for using this skill with a pasted workout session.`

