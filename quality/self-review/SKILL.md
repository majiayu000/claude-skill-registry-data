---
name: Self-Review
description: Spawn a reviewer subagent with 4-6 specific verification questions before declaring non-trivial code work done. Triggers when changes are >30 LOC, multi-file, hot-path, prompt-affecting, or genuinely uncertain. Bad asks produce bad answers — this skill forces structured verification questions, not "is this good?"
---

# Self-Review

Run an explicit second-pair-of-eyes pass on non-trivial work before declaring done. Quality of review depends on quality of question.

## When to RUN self-review

- More than ~30 lines OR multi-file change
- Hot path (many requests flow through this code)
- Subtle interactions with code you might have missed
- Prompt or output affecting user-visible content
- Code not worked in recently (mental model might be stale)
- Any genuine uncertainty after writing the change

## When to SKIP self-review

- One-line edit, mechanical fix, obvious diff
- Pure rename or move with no logic change
- Code just written with full context, low blast radius
- Cost-benefit doesn't justify (review takes longer than the fix did)

If skipping, say so explicitly: "Skipping self-review — N-line trivial fix." Don't silently bypass.

## How to execute

### Step 1 — Set context (3-5 lines max)

State, in plain language:
- The bug / feature / what was asked
- The cause (what was actually wrong)
- The fix (what was actually changed)

### Step 2 — List specific changes

```
- path/to/file_one.ts:L123-L145 — replaced regex with structured parser
- path/to/file_two.ts:L56 — added null guard for empty corpus
- path/to/config.json — bumped diversity_threshold 0.6 → 0.75
```

### Step 3 — Ask 4-6 specific verification questions

**Bad asks (do not produce useful answers):**
- "Is this good?"
- "Does this look right?"
- "Any issues?"
- "Did I miss anything?"

**Good asks (concrete, falsifiable, named):**
- "Does the new keyword order ever cause a wrong branch in `routeRequest`?"
- "Does the diversity rule reach the model in the same prompt as the recent-titles list?"
- "Is the early return at line 47 still bypassing this check?"
- "If `recent_titles` is empty (first run), does the sort comparator return stable output?"
- "Does the schema migration handle the existing 12K `null` rows or only new inserts?"

Each question must:
- Reference a specific file:line or function name
- State the failure mode you're worried about
- Be answerable yes/no after a focused read

### Step 4 — Ask explicitly about edge cases, regressions, missed interactions

```
"Edge cases I'm uncertain about:
- What happens when input X is empty?
- Does this break callers Y and Z that I didn't read?
- Any regression on the prior fix from PR #N?"
```

### Step 5 — Request severity ratings + line references

```
"Please rate findings as HIGH / MEDIUM / LOW with concrete line references."
```

### Step 6 — Spawn the reviewer subagent

Use the Agent tool with a code-reviewer subagent_type (or equivalent). Pass the full context block (steps 1-5) as the prompt. Set model to whatever is appropriate for the review depth.

### Step 7 — Process findings

- **HIGH severity** → fix before declaring done
- **MEDIUM severity** → fix unless you have a specific reason not to. If skipping, document why.
- **LOW severity** → judgment call. Often fold into a follow-up note.
- **Reviewer misread** → trust your own reading, but re-verify before dismissing. A misread is a signal the code might need clarity.

The reviewer is a **second pair of eyes, not an authority.** Evaluate every suggestion. Blindly applying every note is as bad as ignoring them all.

## Output format

After review completes, append to your delivery message:

```
**Self-review:** {APPROVED — severity X} / {N findings applied} / {N deferred — listed below}
- {finding} → {fix applied OR reason deferred}
```
