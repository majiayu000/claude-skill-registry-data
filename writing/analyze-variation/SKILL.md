---
name: analyze-variation
description: Use when scheduling social copy or reviewing a batch of posts/drafts to measure sentence- and post-length variation — flags metronomic rhythm and same-size posts. For voice/tone rules, see your project's own style guide.
user-invocable: true
argument-hint: <markdown files/glob, or pipe text via stdin>
metadata:
  version: "1.0.0"
---

# Analyze Variation

Reports rhythm (within-post sentence-length variation) and length spread (across a
sequence of posts), and flags **monotone** posts and **too-similar neighbors**.

> **Why this is a skill with a script, not a prompt:** length and rhythm metrics
> must be deterministic. The numbers are computed by the bundled Node script —
> this skill just tells the agent to run it and how to read the output. Do not
> eyeball the counts; run the script.

## When to use

- Before scheduling a batch of social posts, to check the feed won't read as a
  same-length content machine.
- Reviewing journal/blog drafts or any prose for metronomic cadence.
- Whenever a house style asks to "vary sentence and post length" (the measurement
  is voice-agnostic; the style rules stay in the project's own voice doc).

## How to run

Always execute the bundled script — never compute the metrics yourself.

The script lives at `scripts/analyze-variation.mjs` **inside this skill's own
directory**. Resolve that directory however your harness exposes it, then run the
absolute path with Node:

- Claude Code: `$CLAUDE_PLUGIN_ROOT/skills/analyze-variation/scripts/analyze-variation.mjs`
- opencode / other Agent Skills hosts: use the absolute path to this `SKILL.md`'s
  directory + `/scripts/analyze-variation.mjs` (the env var above is Claude-Code-only).

```bash
# pick whichever resolves on your harness; SCRIPT points at the bundled .mjs
SCRIPT="$CLAUDE_PLUGIN_ROOT/skills/analyze-variation/scripts/analyze-variation.mjs"

# one post per file → sequence analysis with neighbor flags
node "$SCRIPT" posts/*.md

# a single post inline or piped
node "$SCRIPT" --text "Short. Then a noticeably longer sentence."
pbpaste | node "$SCRIPT"

# machine-readable, or write a version-tracked report
node "$SCRIPT" posts/*.md --json
REPORT_DATE=2026-06-07 node "$SCRIPT" posts/*.md --write report.md
```

Markdown frontmatter and JSX/HTML tags are stripped before analysis. The script is
CJK-aware (Chinese characters count as tokens; wide chars weighted ×2 for length),
so it works for English and mixed CJK copy alike. Dependency-free (Node built-ins).

## Reading the output

- **cv (per post)** = stdev/mean of sentence length. Higher = more varied rhythm.
  Below **0.35** with ≥3 sentences is flagged **monotone**.
- **spread(cv) (sequence)** = variation of post lengths across the batch. Target
  **≥ 0.35**; lower means the posts are all about the same size.
- **too-similar neighbors** = adjacent posts whose lengths are within **15%**.
- **wt** = X-weighted length; anything over 280 sits past the in-timeline
  "Show more" fold (informational, not a cap on Premium accounts).

## Fixing flags (the script measures; the writer fixes)

Mix short and long sentences within a post; let post length rise and fall across
the schedule. Apply the project's own voice rules for *how* to cut or expand —
this tool only tells you *where* the rhythm is flat.

## Thresholds (tunable)

Defined as named constants at the top of the script:

- `MONOTONE_CV_THRESHOLD = 0.35` — a post with ≥3 sentences and a lower
  sentence-length CV is flagged monotone.
- `NEIGHBOR_SIMILARITY_THRESHOLD = 0.15` — adjacent posts within this length
  fraction are flagged too-similar.

These are first-guess heuristics; tune them to your corpus.
