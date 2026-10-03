---
name: retro
description: Guided pass over recent Bigweld conversations to surface repeated patterns and propose memory or CLAUDE.md updates after Alex explicitly asks for them.
allowed-tools:
  - "Bash(ls:*)"
  - "Bash(cat:*)"
  - "Bash(find:*)"
  - "Bash(grep:*)"
  - "Read"
---

# /retro [<duration>|since:<YYYY-MM-DD>]

Use `/retro` when Alex explicitly asks Bigweld to look back across past conversations for repeated patterns, missed preferences, clarified terms, or rules worth promoting into memory. This is guided and interactive: no autonomous writes, no scheduled pass, no background autonomy.

## Trigger

- `/retro` — default to the past 7 days.
- `/retro <duration>` — use a simple duration such as `14d`, `3d`, or `1h`.
- `/retro since:<YYYY-MM-DD>` — include conversations modified on or after that date.

## Workflow

1. Resolve the time window. No arg means 7 days. `<number>d` means days, `<number>h` means hours, and `since:<YYYY-MM-DD>` means that date forward. If ambiguous, ask Alex for `7d`, `14d`, or `since:<YYYY-MM-DD>`.
2. Enumerate `/datapool/bigweld-portal/conversations/<YYYY-MM>/*.json` files modified within the window. Use `find` with `-mtime` for duration windows or `-newermt` for since windows when available. Skip `.lock` and `.tmp`.
3. Build a working list sorted by mtime descending. Keep each row compact: conversation id or filename, modified timestamp, summary sidecar path if present, one-line gist, and tool count.
4. Read each conversation. If `<conv-id>.summary.md` exists beside the JSON file, read that first. Otherwise read the raw JSONL and extract the first user turn, the last assistant turn's first text block, and tool count.
5. Truncate raw fallback snippets to about 300 characters. Do not over-parse; the goal is pattern recognition, not perfect reconstruction.
6. Keep private scratch notes terse: candidate pattern, evidence count, target memory file, possible diff.

Useful commands:

```bash
find /datapool/bigweld-portal/conversations -type f -name '*.json' -mtime -7 ! -name '*.lock' ! -name '*.tmp'
find /datapool/bigweld-portal/conversations -type f -name '*.json' -newermt '2026-04-20' ! -name '*.lock' ! -name '*.tmp'
grep -c 'tool' /datapool/bigweld-portal/conversations/<YYYY-MM>/<conv-id>.json
```

## Walkthrough

Open with scope:

```text
Walking the last <N> days, <K> conversations.
```

Then walk Alex through chunks of 3-5 conversations:

```text
Conversations 1-5 of 12:
- <date> <short id> — <gist>
- <date> <short id> — <gist>
```

After each chunk, pause and ask:

```text
anything noteworthy in those?
```

If Alex points at a pattern, capture it as a candidate. If he says to keep going, continue to the next chunk. Do not dump the whole corpus at once.

## Synthesis

At the end of the walk, identify recurring signals across multiple conversations. Good candidates:

- The same correction happened at least twice.
- Alex explicitly corrected you once with finality.
- A term, scope boundary, or relationship was clarified in more than one place.
- A workflow repeated enough times that Bigweld should remember the operating rule.

Examples:

- "I corrected my own approach 3 times across these 5 convos to match X. Should I add 'prefer X' to `working-with-alex.md`?"
- "Two conversations clarified that Scope A and Scope B differ on dimension Y. Should I add this to `world-model.md`?"
- "Alex pushed back on overly-eager summarization 4 times. Strong signal for `never-list.md`."

Frame the close like this:

```text
Patterns I noticed:
- <pattern> (<evidence count>, target file)
- <pattern> (<evidence count>, target file)

Memory updates worth considering:
```

## Diff-then-nod

Every proposal follows the Memory hygiene gate in `CLAUDE.md`:

1. Announce the observation and target file in plain language.
2. Show a fenced diff. For feedback entries, include **Why:** and **How to apply:**.
3. Wait for Alex's nod: "yes", "do it", "go", or equivalent.
4. Write only after the nod.
5. Acknowledge with exactly one line: "captured."

## What not to do

- Do not propose updates from a single data point unless Alex explicitly corrected you.
- Do not duplicate existing memory. Read the target file before proposing a diff.
- Do not bury Alex in suggestions. Limit proposals to 3-5 per `/retro` session.
- Do not ask Alex to verify factual claims about his own work. That belongs in the original conversation, not retro.
- Do not summarize for summarization's sake. If there are no durable patterns, say so and stop.
