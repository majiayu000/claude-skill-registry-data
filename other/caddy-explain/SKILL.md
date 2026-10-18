---
name: Caddy Explain
description: When a [CADDY] hint fires and the principal is confused why, /caddy-explain walks the scoring transparently — which trigger matched, what points it earned, what the threshold was, what other skills were close. Pairs with the legibility thesis. Caddy's decisions should be inspectable on demand.
---

# Caddy Explain

When Caddy surfaces a hint and you don't see why, run `/caddy-explain` to see the deterministic scoring. The scoring should never be a black box.

## When to use

- A [CADDY] hint fired and you're surprised by the choice
- A [CADDY] hint *didn't* fire when you expected it to
- You want to verify why a particular skill won (or lost) for a recent prompt
- Triggered by Caddy on prompts like: "/caddy-explain", "why did Caddy suggest", "explain that hint", "why no hint", "why this skill", "Caddy scoring", "Caddy why"

## How to execute

### Step 1 — Identify the prompt being explained

If the principal provides the prompt explicitly, use it. Otherwise:
- Use the immediately-preceding user prompt from the current session
- If there's ambiguity ("the one before the last hint"), ask one focused question

### Step 2 — Walk the scoring deterministically

For each skill in `.claude/skill-index.json`:

1. List its triggers
2. For each trigger, check whether it appears in the prompt:
   - Multi-word phrase match (case-insensitive substring) → 3 points
   - Single-word boundary match (`\bword\b` regex) → 1 point
   - No match → 0 points
3. Sum the per-skill score

### Step 3 — Show the result

Output format:

```
🔍 Caddy scoring for prompt:
   "{prompt text}"

Threshold: 2 (skills below this score are silent)
Max hints: 2 (top scorers above threshold are surfaced)

SURFACED:
   /skill-a — score 5 — matched: "phrase match" (3pts), "keyword" (1pt), "another" (1pt)
   /skill-b — score 3 — matched: "exact phrase" (3pts)

NEAR MISSES (below threshold):
   /skill-c — score 1 — matched: "word" (1pt)
   /skill-d — score 1 — matched: "another" (1pt)

SILENT (no triggers matched):
   /skill-e, /skill-f, /skill-g, /skill-h, ... (28 more)

Reasoning:
   Caddy chose /skill-a + /skill-b because their scores cleared the threshold
   of 2 AND they were the top 2 (max 2 hints per prompt).
   /skill-c and /skill-d had matches but didn't clear threshold.
```

### Step 4 — If the principal expected a different result

Ask: would they like to:
- **Adjust triggers** for a skill that should have matched but didn't (one trigger could be added)
- **Narrow triggers** for a skill that fired when it shouldn't have (a trigger could be removed)
- **Accept the result** and move on (sometimes the scoring is correct and the surprise was misremembered)

If they pick adjust/narrow, they can run `/caddy-enroll <skill-path>` to update the index, or edit `.claude/skill-index.json` directly.

## Output principles

- **Show the math.** Don't summarize "the skill matched well." Show the trigger, the points, the threshold.
- **Show the near-misses.** The skills that *almost* matched are often the most informative for tuning.
- **Don't apologize.** If the matcher chose correctly, say so plainly. Caddy is deterministic; surprise often means the principal's mental model needs updating, not the matcher's.
- **Don't auto-tune.** This skill explains; it doesn't change the index. Auto-tuning is a separate decision the principal makes after seeing the explanation.

## Why this skill exists

The legibility thesis says every layer of the framework must be inspectable. Caddy is one of the most-fired layers (every prompt). Without `/caddy-explain`, its decisions become a black box — which violates the thesis and erodes trust over time.

`/caddy-explain` makes Caddy's decisions auditable on demand. The scoring is deterministic; the explanation should match.

## Connects to

- [[Caddy]] — the doctrine note this skill makes inspectable
- [[Suggestion Credibility]] — the constraint Caddy operates under, including inspectability
- [[Legibility Thesis]] — the meta-doctrine this skill enforces at the Caddy layer
