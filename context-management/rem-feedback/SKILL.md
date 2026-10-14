---
name: rem-feedback
description: 'Capture typed feedback about skill mistakes so skills can learn and improve over time. Writes structured entries to `~/.claude/skill-feedback.jsonl` tagged with one of six mistake types — misrouted (wrong skill fired / should have fired), wrong-output (false claim, bad advice), missed (skill didn''t flag an issue it should have), over-flagged (skill flagged a non-issue), context-ignored (skill ignored CLAUDE.md / memory / project conventions), stale (advice references deleted files / old APIs / outdated facts). Links each feedback entry back to the originating invocation in `~/.claude/skill-usage.jsonl` by session_id + timestamp. Auto-promotes to `/rem-skill analyze [name]` when 3+ same-type flags accumulate for one skill. Distinct from rem-learn (which captures project-level lessons, not skill-system lessons) and rem-handoff (session state, not feedback). Use for "flag a skill mistake", "this skill got it wrong", "the skill should have X", "rem-copy misrouted", "rem-review missed the bug", "skill feedback", "rate the skill", "this wasn''t helpful", after any skill-assisted session where output disappointed.'
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
argument-hint: '''[skill-name] [optional: mistake-type] — or leave empty for interactive'''
---

# Skill Feedback Capture

You are a feedback curator for the skill ecosystem. Your job: turn a user's "that was wrong" observation into a **typed, structured, analyzable record** so the skill that misfired can be improved deterministically — not by vibes.

## Output voice

This skill follows the shared output-voice contract at `_references/output-voice.md`. Narration is plain-language and purposeful (5 moments only); CTAs are invitational, not declarative; banned vocabulary translates per the table in that file.

## Philosophy

Skills are code. Code improves through measurement. Without a feedback loop, every skill drifts: routing gets fuzzier, anti-patterns decay, the description gets stale relative to reality. This skill is the write side of that loop. `/rem-skill analyze` is the read side.

Good feedback entries are:
- **Typed** — one of six canonical mistake types (not free-form sentiment)
- **Specific** — literal skill name, literal mistake, not "the AI was bad"
- **Actionable** — contains enough detail that a future `/rem-skill improve` can derive a concrete edit (description tweak, new anti-pattern, clarified handoff)
- **Linked** — points back to the originating `skill-usage.jsonl` entry when possible
- **Dated** — YYYY-MM-DDTHH:MM:SSZ; so staleness can be detected when the skill is later rewritten

**Bad feedback**: "rem-copy output wasn't great"
**Good feedback**: `{skill: "rem-copy", type: "context-ignored", what_happened: "Generated em-dash heavy copy despite feedback_em_dash.md in memory", what_should_have: "Loaded memory, used plain hyphens", severity: "high"}`

## The Six Mistake Types

| Type | Signal | Fix target in skill |
|---|---|---|
| **misrouted** | Wrong skill fired, or right skill didn't fire | Description trigger phrases, confusion-pair matrix |
| **wrong-output** | Output contained a false claim or bad advice | Body rules, anti-patterns, verification steps |
| **missed** | Skill should have flagged X but didn't | Checklist gap, detection heuristic, new anti-pattern |
| **over-flagged** | Skill flagged X as problem but it wasn't | Calibration, severity rubric, confidence gate |
| **context-ignored** | Skill didn't read CLAUDE.md / memory / conventions | Missing "Step 0: load context" phase |
| **stale** | Advice referenced deleted files / old APIs / outdated facts | Date-based pruning, freshness check in skill |

Full type taxonomy + 12 worked before/after examples: **`_references/mistake-types.md`**.

---

## Input

`$ARGUMENTS` parses as `[skill-name] [optional: mistake-type]`:
- Both provided → skip Step 1, start at Step 2
- Only skill-name → start at Step 1 type selection
- Empty → start at Step 0 skill selection

---

## Step 0: Identify the Skill (if not provided)

Ask: "Which skill misfired?" — offer recent invocations from `~/.claude/skill-usage.jsonl`:

```bash
tail -20 ~/.claude/skill-usage.jsonl | jq -r '.skill' 2>/dev/null | sort -u
```

If user names a skill not in recent log, proceed anyway — feedback doesn't require prior invocation (user may be flagging from memory).

---

## Step 1: Classify the Mistake Type

Present the six types as a picker. For each, a one-line prompt helps the user self-classify:

- **misrouted** — "Did the wrong skill fire, or should a skill have fired but didn't?"
- **wrong-output** — "Did the skill produce a factually wrong claim or bad advice?"
- **missed** — "Did the skill fail to catch something it was supposed to catch?"
- **over-flagged** — "Did the skill flag something that wasn't actually a problem?"
- **context-ignored** — "Did the skill ignore project conventions, CLAUDE.md, or saved memory?"
- **stale** — "Did the skill reference outdated information (deleted files, old versions, obsolete APIs)?"

If the user's answer spans multiple types, pick the **primary leverage point** — the type whose fix would prevent the most similar failures. Don't split into multiple entries unless the mistakes are genuinely independent (e.g., misrouted AND wrong-output once routing went wrong).

Tie-breaker rules + worked multi-type examples: `_references/mistake-types.md` § Primary Leverage.

---

## Step 2: Gather the Facts

Collect four fields:

| Field | Content | Length |
|---|---|---|
| `what_happened` | Literal description of the mistake — include exact quotes, file paths, commands | 1-3 sentences |
| `what_should_have` | What the correct behavior would have been — be concrete, not aspirational | 1-2 sentences |
| `severity` | low / medium / high — see severity rubric below | one value |
| `context` | Optional: project name, CLAUDE.md section, user prompt text that triggered it | 1 sentence or skip |

### Severity Rubric

| Level | Signal | Examples |
|---|---|---|
| **low** | Annoying but correctable in one edit | Typo in output, missed secondary trigger phrase |
| **medium** | Caused user to re-prompt or correct | Wrong verdict that user had to override |
| **high** | Would ship wrong work if unchecked | Missed security issue, ignored saved preference |

**Don't inflate severity.** A `high` flag on every entry dilutes the signal. Most feedback is `medium`.

---

## Step 3: Link to Originating Invocation

Find the most recent matching entry in `~/.claude/skill-usage.jsonl`:

```bash
grep "\"skill\":\"<skill-name>\"" ~/.claude/skill-usage.jsonl | tail -5
```

If exactly one entry in the current session (`session_id` match) → link it by `ts` + `session_id`.
If multiple recent entries → ask the user which, or pick the latest.
If none (user is flagging from memory) → set `linked_usage: null`.

---

## Step 4: Write the Feedback Entry

Append a single JSON line to `~/.claude/skill-feedback.jsonl`:

```json
{
  "ts": "2026-04-18T21:59:00Z",
  "skill": "rem-copy",
  "mistake_type": "context-ignored",
  "severity": "high",
  "what_happened": "Produced em-dash heavy copy despite feedback_em_dash.md in auto-memory",
  "what_should_have": "Loaded auto-memory before generation; used plain hyphens throughout",
  "context": "a production project project, landing page hero section",
  "linked_usage": {"ts": "2026-04-18T21:45:12Z", "session_id": "abc123"},
  "status": "open"
}
```

Use Bash + `jq` to build the JSON safely (no manual string concatenation — escapes will bite). One-liner:

```bash
jq -n --arg ts "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
  --arg skill "rem-copy" \
  --arg type "context-ignored" \
  --arg sev "high" \
  --arg what "..." \
  --arg should "..." \
  '{ts:$ts, skill:$skill, mistake_type:$type, severity:$sev, what_happened:$what, what_should_have:$should, status:"open"}' \
  >> ~/.claude/skill-feedback.jsonl
```

Full jq template for every field combination: `_references/write-format.md`.

---

## Step 5: Check for Patterns & Escalate

After writing, count existing open entries for this (skill, mistake_type) pair:

```bash
jq -c 'select(.skill == "<name>" and .mistake_type == "<type>" and .status == "open")' \
  ~/.claude/skill-feedback.jsonl | wc -l
```

| Count | Action |
|---|---|
| 1-2 | Report the new entry; no escalation |
| **3+** | **Escalate**: "This is the Nth `<type>` flag for `<skill>`. Run `/rem-skill analyze <skill>` to see aggregated signal and propose improvements?" |
| 5+ | Escalate harder: "`<skill>` has accumulated 5+ `<type>` flags — strongly recommend running `/rem-skill improve <skill>` now" |

Escalation is a **recommendation, not an auto-trigger** — the user decides whether to run `/rem-skill analyze` or `/rem-skill improve`. Don't act on their behalf.

---

## Step 6: Report

Emit a 4-line summary:

```
Feedback captured: rem-copy / context-ignored / high
Linked to invocation: 2026-04-18T21:45:12Z (session abc123)
Entry count for this pattern: 3 (was 2)
Recommendation: Run /rem-skill analyze rem-copy — pattern threshold reached
```

If no escalation triggered, omit the Recommendation line.

---

## Rules

1. **Feedback must be typed.** Free-form "this wasn't good" entries cannot be analyzed. If the user can't classify, walk them through the six types; don't default to a generic bucket. Anti-pattern: writing `mistake_type: "other"` — kills aggregation. Fix: if none of the six fit, that's a signal the taxonomy needs extension; propose a new type and discuss with user before using it.

2. **Link to skill-usage.jsonl when possible.** The link enables join queries in `/rem-skill analyze` (e.g., "what args were passed when rem-copy misrouted?"). Anti-pattern: skipping the link because it's "extra work". Fix: Step 3 is ~3 seconds; do it unless the invocation is genuinely unrecoverable.

3. **Don't auto-trigger rem-skill improve.** Escalation presents a recommendation; the user runs the improve step. Reason: improvements to a skill's description can change its routing — that's a decision the user should make, not a side effect of flagging feedback.

4. **Severity discipline.** If >50% of entries are `high`, severity has become meaningless. Use `medium` as the default. `high` means "would have shipped wrong work." Anti-pattern: tagging every annoyance as `high` because it felt frustrating in the moment. Fix: re-read the severity rubric; rewrite if inflated.

5. **One mistake type per entry.** When a single failure spans multiple types, pick the primary leverage point. Anti-pattern: writing 3 entries for one failure — pollutes counts, causes false escalation. Fix: pick the root type; mention secondary types in `what_happened`.

6. **Write to JSONL only.** Never write feedback into project `learnings.md`, `MEMORY.md`, or CLAUDE.md directly. The analyze mode reads the JSONL; other locations fragment the signal. Anti-pattern: "while I'm here I'll also add a CLAUDE.md note" — now there are two sources of truth. Fix: if the feedback truly generalizes beyond one skill, flag it — the user may want `/rem-learn` as a follow-up, but that's a separate action.

7. **Never edit existing entries to "close" them.** Closing happens when `/rem-skill improve` runs and marks entries as addressed (status transitions `open` → `addressed`). Anti-pattern: manually flipping `status` to clean up the file. Fix: let the improve cycle do it; that's how the feedback loop learns.

8. **Feedback is not criticism.** Tone of `what_happened` should be factual, not punitive. Future-you reads these to improve skills, not to relitigate a frustration. Anti-pattern: `what_happened: "the skill was stupid and ignored me"` — zero signal. Fix: reframe as "skill did X; expected Y".

---

## Handoffs

**← Upstream** (who hands work here)
- Any skill produced disappointing output — user invokes `/rem-feedback [name]`
- `rem-review-plan` / `rem-audit` / `rem-qa` — when the review skill itself misfired (missed issue, over-flagged)
- `rem-skill evaluate` — if evaluation revealed a pattern worth capturing as feedback
- Direct user invocation after any skill-assisted session

**→ Downstream** (conditional)
- **Pattern ≥ 3** → recommend `/rem-skill analyze <name>` to aggregate signal
- **Pattern ≥ 5** → recommend `/rem-skill improve <name>` to apply improvements
- **Mistake type = misrouted** → may warrant edit to `_references/skill-routing.md` confusion pair matrix
- **Mistake type = stale AND project-scoped** → may warrant `/rem-sync` run to refresh project docs

**∥ Parallel** (runs alongside)
- None — feedback capture is a single-purpose write step

**✗ Abort signals**
- IF user's description is not concrete enough to classify into one of six types → push back; ask for specifics before writing
- IF user is describing a general frustration with AI rather than a specific skill mistake → skip the skill; suggest they talk through it instead
- IF the "mistake" is actually expected skill behavior that the user disagrees with philosophically → don't write feedback; the right channel is a discussion about redesigning the skill, not flagging an invocation

See `_references/skill-routing.md` for full workflow chains.
