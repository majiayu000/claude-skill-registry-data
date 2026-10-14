---
name: content-performance-review
description: >
  Use this skill to analyze how one or more published content pieces performed and
  generate concrete iteration variants for the next piece. Invoke when the user says
  "review how this post performed", "analyze content performance", "what worked in
  these posts", "help me iterate on this based on the numbers", or pastes performance
  data (impressions, engagement rate, CTR, conversions) alongside a piece and asks
  what to do next. Works from whatever data the owner supplies — there is no
  analytics API integration. Do NOT use it to evaluate whether a positioning claim,
  channel allocation, or campaign goal was validated — that is a strategic-level
  question for strategy-performance-review, not this skill.
allowed-tools: Read, Write, Bash
argument-hint: "[optional: path to a file with performance notes]"
---

# Content Performance Review Skill

You are helping the owner understand why one or more content pieces performed the way
they did, and turn that understanding into concrete next-piece variants. This skill
looks at **structural and tonal patterns within and across individual content
pieces** — it is deliberately narrower than a strategic review: it never evaluates
whether a positioning claim or channel allocation was validated (that's
`strategy-performance-review`, a different plugin's skill, at a different altitude).

This skill reasons only over data the owner supplies — pasted metrics, notes, or
observations. There is no live analytics integration.

## Step 0: Recall learnings

If `.claude/learnings.md` exists, read it silently. Apply all entries relevant to
this run — both `[cc-content:*]`-tagged entries and entries from other plugins that
inform content quality or project constraints. Do not announce this step. If the
file is absent, continue normally.

## Step 1: Load context

Read the context table from all loaded CLAUDE.md files:

```bash
grep -A 200 '## Context files' CLAUDE.md 2>/dev/null || echo "(no context table)"
```

**If no context table is found**, ask once:

> "I don't see any context files registered. Would you like to:
> (a) Pause and run `/content-onboarding` to set up context
> (b) Continue without project context (iteration variants will use generic style choices)"

Stop if (a); note "generating without project context" and continue if (b).

**If a context table exists**, identify which file covers **brand voice** — the
**only** need this skill gates on, since Step 4's iteration variants need it to stay
on-voice. Organization background and audience are noted silently if present and
never block.

**Coverage gap — brand voice:**

If no loaded file plausibly covers brand voice, ask once:

> "I don't see any writing style or brand voice context. Is this intentional, or
> should I pause while you run `/content-onboarding`?"
>
> - **Intentional**: note the gap; label the output `⚠ DEGRADED OUTPUT — no brand voice context`.
> - **Pause**: direct the owner to onboarding and stop.

## Step 2: Gather the pieces and their data

For each piece under review, collect:

1. **The content itself** — pasted text, a file path, or (if unavailable) a brief
   summary the owner provides.
2. **Performance data** — whatever the owner has: impressions, engagement rate, CTR,
   conversions, or qualitative notes (e.g. "comments kept mentioning X").

If nothing is provided yet, ask:

> "Paste the piece(s) and whatever performance numbers or notes you have —
> impressions, engagement rate, CTR, conversions, or just qualitative observations."

If the owner has only numbers and no content, proceed with data-only analysis and
note that limitation in the output.

## Step 3: Identify patterns

Compare pieces against each other (if 2 or more are provided) or against stated
expectations (if only 1 is provided). For each piece, note which storytelling
framework (`../_shared/storytelling-frameworks.md`) and persuasion principles
(`../_shared/persuasion-principles.md`) it used, if identifiable.

Name the structural/tonal elements correlated with **stronger** results — e.g. "the
two top-performing posts both used PAS with a Loss-Aversion opener." Name the
elements correlated with **weaker** results the same way.

**Do not fabricate a pattern from a single data point.** If there isn't enough
evidence to generalize (e.g. only one piece with no comparison, or metrics too close
to distinguish), say so explicitly rather than naming a pattern anyway.

## Step 4: Generate iteration variants

Produce **2–3 short concept-level variants** (not full drafts) for the next piece.
Each variant:

- **Keeps** the winning elements identified in Step 3.
- **Changes exactly one thing** — a different hook trigger, a different framework, a
  different persuasion principle — so results stay attributable to that one change.

After presenting the variants, offer the next step:

> "Want me to turn one of these into a finished draft? Tell me the number and the
> format. If a dedicated skill fits the format (e.g. a blog article or LinkedIn
> post), I'll route you to it for a better result; otherwise I'll use the general
> text skill (`/long-tail-copy`)."

Do not auto-draft. Wait for the owner to choose.

## Step 5: Delimited output

```
─────────────────────────────────────────────
Performance review — <N> piece(s)
─────────────────────────────────────────────
Winning elements: <list, with evidence>
Weak elements: <list, with evidence>
Confidence: <note if evidence is too thin to generalize, or omit if solid>
─────────────────────────────────────────────
Iteration variants for next piece
─────────────────────────────────────────────
Variant 1: <what's kept> / <the one thing changed>
Variant 2: <what's kept> / <the one thing changed>
[Variant 3, if applicable]
─────────────────────────────────────────────
```

If the output is degraded (no brand voice context), prepend:

```
⚠ DEGRADED OUTPUT — generated without brand voice context
```

## Step 6: Feedback

**Auto-store phase.** Before asking for feedback, review this run. For each
qualifying observation, append one tagged line to `.claude/learnings.md` (create with
the standard header if missing):

```text
[cc-content:content-performance-review] <concise observation> — <YYYY-MM-DD>
```

Qualifies: performance patterns not already in any loaded context file or
`CLAUDE.md` (e.g. "audience consistently engages more with concrete numbers in the
hook"); corrections the owner made to the identified patterns; project-specific
facts that would change future reviews.

Does not qualify: standard behavior applied without deviation; facts already in
context files or `CLAUDE.md`; anything derivable by re-reading context files; facts
semantically equivalent to an existing `.claude/learnings.md` entry under any plugin
tag — when in doubt, skip; redundancy is worse than a missed entry.

Check for the file before appending:

```bash
ls .claude/learnings.md 2>/dev/null && echo "exists" || echo "missing"
```

Standard header when creating the file:

```markdown
# Learnings

Corrections and feedback collected during content sessions.
Entries are tagged by skill and dated.

---
```

**Explicit feedback.** After the auto-store phase, ask:

> "Does this analysis match your own read on why these pieces performed the way they
> did? Any corrections or notes for future reviews — or press Enter to finish."

- If the owner **provides a correction**: append it as a tagged entry using the same
  format and qualification criteria above. Confirm: "✓ N learning(s) saved to
  `.claude/learnings.md`."
- If the owner **confirms or skips**: if any entries were auto-stored, confirm
  "✓ N learning(s) auto-saved to `.claude/learnings.md`." Then exit. If nothing was
  stored, exit directly.
