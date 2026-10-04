---
name: context-tax
description:
  Retrospectively analyze the current Claude Code session and estimate how
  much time and tokens were spent on context work (explaining the codebase,
  style guide, conventions, correcting Claude when it reinvented existing
  utilities) vs. actual feature work. Use this skill whenever the user wants
  to audit session efficiency, measure how much time they lost to
  re-explaining context, or decide whether to invest in persistent project
  docs. Trigger on "/context-tax", or phrases like "calculate my context
  tax", "how much did I waste on context this session", "audit this
  session", "session breakdown", "was this session efficient", even if the
  user doesn't explicitly say "context tax".
---

# Context Tax Calculator

Retrospectively classifies every turn in the current Claude Code session
into five categories — four flavors of "context work" plus actual feature
work — then estimates the time and tokens spent on each. The output is a
breakdown report that helps the user see exactly what a session cost them
beyond building the feature they sat down to build.

## Why this matters

Every new Claude Code session starts cold. The user carries context in
their head, retypes it, paraphrases it, and corrects Claude when it
misremembers or reinvents things. That work is invisible in the moment —
it just feels like "coding" — but it's a tax on the session. Measuring
it once gives the user the number they need to decide whether persistent
project documentation is worth the setup cost.

Numbers from this skill are approximations, not exact measurements.
Classification is heuristic and will occasionally miscategorize borderline
turns. That's fine — the goal is a roughly accurate breakdown that reveals
which category dominates, not a precise audit.

## When to Use

- User invokes `/context-tax` at the end of a coding session
- User asks to "calculate the context tax", "show me my context tax",
  "how much did I spend on context this session", "audit this session",
  or similar phrasings about session efficiency
- User is about to close the terminal and wants a post-mortem of the
  session they just completed

Run this skill BEFORE the session ends — once the transcript is closed,
the in-context conversation disappears and only the JSONL file remains.

## Procedure

### Step 1: Locate the session transcript

Primary source: the JSONL file at
`~/.claude/projects/<slug>/<session-id>.jsonl` where `<slug>` is the
current working directory with `/` replaced by `-` (e.g.,
`/home/alice/projects/myapp` becomes `-home-alice-projects-myapp`).

```bash
# Find the most recent session file for this project
ls -t ~/.claude/projects/"$(pwd | sed 's|/|-|g')"/*.jsonl 2>/dev/null | head -1
```

If the JSONL isn't readable (permissions, not yet flushed, or the user is
not in Claude Code), fall back to analyzing the conversation visible in
the current context window. The JSONL is preferred because it contains
precise token counts and timestamps per turn.

### Step 2: Classify each turn

For each USER turn, pick exactly one category based on the dominant
content. When a turn mixes categories, pick the one the user spent the
most words on.

| Category               | What to look for                                                                                                                         |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `codebase_explanation` | Pointing Claude at files/folders/modules/architecture. "Look at src/auth", "we have a utils/ dir", "the config lives in lib/env.ts"      |
| `style_guide`          | Rules, conventions, naming, linting, formatting. "Follow the style guide", "we use camelCase", "see CLAUDE.md", "wrap at 80 chars"       |
| `ways_of_doing_things` | Approach corrections, pattern preferences. "No, do it like this", "use our pattern", "don't use X, use Y", "we always do it this way"    |
| `reinvented_wheel_fix` | Claude built something that already existed; user redirects. "We already have this in lib/foo", "don't rewrite, use the existing helper" |
| `feature_work`         | Actual implementation dialogue — new logic, bug fixes, refactors, tests, questions about the feature being built                         |

For each ASSISTANT turn, classify by dominant activity:

- Re-reading `CLAUDE.md`, rule files, or style guide references → `style_guide`
- Searching for existing utilities, reading the project structure, exploring files for orientation → `codebase_explanation`
- Writing new feature code, fixing bugs, running tests, debugging → `feature_work`
- Re-explaining an approach or walking the user through an alternative because the prior approach was rejected → `ways_of_doing_things`
- Rewriting code that duplicated an existing utility, after being corrected → `reinvented_wheel_fix`

When a turn is ambiguous, classify as `feature_work` — we want a
conservative tax estimate, not an inflated one.

### Step 3: Estimate time and tokens per turn

**Tokens (preferred — from JSONL):**

Each JSONL entry has `message.usage.input_tokens` and
`message.usage.output_tokens`. Sum both for the turn's token cost.

**Tokens (fallback — from in-context conversation):**

Estimate at ~4 characters per token. Count total characters in the turn
(user message or assistant response) and divide by 4. When using this
fallback, prefix the Tokens column in the final report with `~` to
signal approximation.

**Time (preferred — from JSONL timestamps):**

Each JSONL entry has a `timestamp` field. Compute the time between
consecutive turns and attribute it to the earlier turn (this captures
user thinking time + assistant response time).

**Time (fallback — when timestamps are unavailable):**

- Assistant turns: assume 200 tokens/second output rate
- User turns: assume 40 words/minute typing rate

### Step 4: Identify the top 3 costliest context moments

Across all non-`feature_work` turns, rank by individual-turn time spent
and pick the top 3. For each, capture a short quote (first 12 words) or
a summary of what the turn was about. Skip this section entirely if the
session has fewer than 5 turns — the sample is too small to be
meaningful.

### Step 5: Render the report

Output this exact markdown structure, filling in the bracketed values:

```markdown
# Context Tax Report — [YYYY-MM-DD HH:MM]

**Total session**: [X] minutes · [Y] tokens

## Breakdown

| Category               | Time    | Tokens  | % of session |
| ---------------------- | ------- | ------- | ------------ |
| Codebase explanation   | [X] min | [Y] tok | [Z]%         |
| Style guide            | [X] min | [Y] tok | [Z]%         |
| Ways of doing things   | [X] min | [Y] tok | [Z]%         |
| Reinvented-wheel fixes | [X] min | [Y] tok | [Z]%         |
| **Feature work**       | [X] min | [Y] tok | [Z]%         |

**Context tax**: [100 minus feature_work %]% of this session went to
context, not features.

## Top 3 costliest context moments

1. **[Category]** — [X] min — "[short quote or summary]"
2. **[Category]** — [X] min — "[short quote or summary]"
3. **[Category]** — [X] min — "[short quote or summary]"

## The fix

If your context tax is above 20%, persist this context so you don't pay
it again next session. Create three files in your project root:

- `PROJECT.md` — the "why" (stack decisions, constraints, non-goals)
- `ROADMAP.md` — the "what" (phases, current status)
- `STATE.md` — the "where" (cursor: which phase/task you stopped on)

Then add a Session Protocol to your `CLAUDE.md` that reads all three
files on session start and updates STATE.md on session end. The first
run of `/context-tax` after adopting persistent context usually drops
by 20-40 percentage points.
```

## Output Conventions

- Always fill in real numbers — never leave `[X]` placeholders in the
  final output
- Round time to the nearest minute; if a category is under 1 minute,
  show `<1 min`
- Round token counts to the nearest 100 if above 1000 (e.g., `12.3k tok`)
- Round percentages to whole numbers
- When `feature_work` is above 80%, add a closing line: "Most of this
  session went to features — nice work." Skip the "fix" section in that
  case since the tax is already low
- Skip the "Top 3" section if the session has fewer than 5 turns
- When falling back to character-based token estimation, prefix the
  Tokens column header with `~` (e.g., `~Tokens`) and add a single-line
  note at the bottom: "_Tokens estimated from character counts — add the
  `--jsonl` flag or ensure session transcript access for precise
  numbers._"

## Examples

**Input scenario (session has 18 turns, 45 minutes):**

The user spent the first 10 minutes explaining their project structure,
then 5 minutes correcting Claude's assumption about their style guide,
then 25 minutes pair-programming a feature, then 5 minutes at the end
because Claude built a duplicate of an existing helper.

**Expected report:**

```markdown
# Context Tax Report — 2026-04-15 21:34

**Total session**: 45 minutes · 38.2k tokens

## Breakdown

| Category               | Time   | Tokens    | % of session |
| ---------------------- | ------ | --------- | ------------ |
| Codebase explanation   | 10 min | 8.5k tok  | 22%          |
| Style guide            | 5 min  | 4.1k tok  | 11%          |
| Ways of doing things   | <1 min | 0.3k tok  | 1%           |
| Reinvented-wheel fixes | 5 min  | 3.8k tok  | 11%          |
| **Feature work**       | 25 min | 21.5k tok | 55%          |

**Context tax**: 45% of this session went to context, not features.

## Top 3 costliest context moments

1. **codebase_explanation** — 6 min — "ok so the project structure is a
   monorepo with apps/ and packages/, and..."
2. **reinvented_wheel_fix** — 5 min — "no we already have formatDate in
   lib/utils/date.ts, please don't..."
3. **style_guide** — 3 min — "we don't use semicolons, check CLAUDE.md,
   also we prefer const over let..."

## The fix

If your context tax is above 20%, persist this context so you don't
pay it again next session. Create three files in your project root:

- `PROJECT.md` — the "why" (stack decisions, constraints, non-goals)
- `ROADMAP.md` — the "what" (phases, current status)
- `STATE.md` — the "where" (cursor: which phase/task you stopped on)

Then add a Session Protocol to your `CLAUDE.md` that reads all three
files on session start and updates STATE.md on session end. The first
run of `/context-tax` after adopting persistent context usually drops
by 20-40 percentage points.
```

## Notes

- Classification is heuristic — borderline turns may be miscategorized,
  but the aggregate breakdown will still be directionally accurate
- The skill is designed for a single session at a time; don't attempt
  to aggregate across sessions unless the user explicitly asks
- If the user runs the skill twice in the same session, the second run
  will include the first run's output in the transcript; that's fine,
  it usually classifies as `feature_work` and doesn't skew results
