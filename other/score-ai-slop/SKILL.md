---
name: score-ai-slop
description: Use when the user wants a slop quality-pass rather than a rewrite or a located list. Triggers include "score this for slop", "how sloppy is this", "give me a slop breakdown", "rate this writing for AI tells", "is this ready to publish", or "slop report by category". Returns a per-category breakdown (deterministic counts plus judged notes) and a publish-readiness read, deliberately without a single 0-10 headline number, because one number invites gaming. For located findings use detect-ai-slop; to rewrite the text use remove-ai-slop.
---

# Score AI Slop

Give the author a quality-pass read: how much slop is here, by category, and is it ready
to publish. This is the aggregate view over the same engine that `detect-ai-slop` and
`remove-ai-slop` use. It does not rewrite, and it does not return a single 0-10 number;
a headline score becomes a thing people optimize against, so the output stays a
breakdown plus a plain-language readiness call.

Rules, categories, severity, and the override-merge order live in
[`../../shared/spec.md`](../../shared/spec.md). Read it before scoring.

## How to score

**Deterministic tier (preferred).** Run the bundled script and use its `summary` (the
per-category counts) plus its `findings` for the breakdown:

```bash
python3 shared/slop_count.py --file <path> \
  [--allow-list ~/.claude/config/remove-ai-slop/user-allow-list.md] \
  [--allow-list .claude/skills/remove-ai-slop/overrides/user-allow-list.md] \
  [--extra-vocab ~/.claude/config/remove-ai-slop/user-vocabulary.md] \
  [--extra-vocab .claude/skills/remove-ai-slop/overrides/user-vocabulary.md]
```

Pipe text on stdin instead of `--file` when the user pasted it. Pass whichever override
files exist. The script is the sole override parser; consume its output, do not
re-parse the override tables.

**Judged tier (you).** The script cannot see meaning. Add a short note per
meaning-dependent category from the spec (`padding-and-filler`, `elegant-variation`, and
contextual cases). Mark these `judged`.

## Fallback — when `python3` is absent

If `python3` is unavailable, do the read yourself from the spec and references, read the
allow-list files directly, and tag the result **unstable**: say "No python3 found; this
is an LLM-only pass and the counts are not byte-stable."

## Output

A per-category breakdown, then a one-line readiness call. No 0-10 number.

```
Slop breakdown (deterministic + judged):

| Category                 | Count | Severity | Notes                         |
|--------------------------|-------|----------|-------------------------------|
| overused-vocabulary      | 9     | low      | clustered in para 1           |
| formulaic-constructions  | 1     | high     | "not just X, it's Y" (para 2) |
| formatting-tells         | 2     | med      | em-dash run in para 2         |
| padding-and-filler       | 1     | med      | judged: hedging in para 3     |

Readiness: heavy slop — run remove-ai-slop for a rewrite pass.
```

Readiness is plain language tied to the spec threshold, not a number:
- **No findings** → `Clean — reads as written by a human, publish as-is.`
- **A few isolated tells, none clustered** → `Light — a couple of edits, no rewrite needed.`
- **Any paragraph over the co-occurrence threshold** → `Heavy — run remove-ai-slop.`

Rules:
- Never emit a single 0-10 number. The per-category counts are the signal.
- If the script ran, note the counts are stable. On fallback, tag the read unstable.
- Respect the allow-list: an allow-listed word is never counted.
- If there are no findings, say so plainly and stop.

## Scope

Aggregate read only. To see exactly where each tell is, that is `detect-ai-slop`. To
rewrite the text, that is `remove-ai-slop`. Do not rewrite from this skill.
