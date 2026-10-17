---
name: handoff
description: Write ~/.claude/custom-handoff.md to hand off current work to the next session
disable-model-invocation: true
argument-hint:
  [focus, e.g. "the auth refactor" or "only what's left on the migration"]
allowed-tools: Write, Bash(trash-put:*), Bash(mv:*), Bash(git status:*), Bash(git log:*), Bash(git diff:*)
---

Write `~/.claude/custom-handoff.md` (resolve `~` to the user's home directory) summarizing current work so the next Claude session can pick up where this one left off.

## Focus argument

`$ARGUMENTS`, when present, is the user's steer for what the handoff should emphasize. Let it bias every section — `GOAL`, `RECENT CONCLUSIONS`, and `NEXT` especially — toward that thread of the work. Trim or drop details unrelated to the focus, and let `NEXT` lead with the focused action. Still keep `# ORIGINAL PROMPT` verbatim; the focus reshapes emphasis, not the recorded intent. When `$ARGUMENTS` is empty, weight sections as the rules below describe.

## Steps

1. Move any prior handoff out of the way (ignore errors if the file is absent; `trash-put` isn't installed everywhere, hence the fallback): `trash-put ~/.claude/custom-handoff.md 2>/dev/null || mv ~/.claude/custom-handoff.md "${TMPDIR:-/tmp}/custom-handoff.md.old" 2>/dev/null || true`
2. Write fresh content per template. No merge, no preserve.

## Template

```markdown
# ORIGINAL PROMPT

<the user's opening prompt from this conversation, verbatim if short; otherwise a one-to-two-sentence summary that preserves the ask>

# GOAL

<one line: what we're doing now>

# DONE

- <thing done>
- <thing done>

# RECENT CONCLUSIONS

- <decision, agreement, or insight from last few turns — what shifted the plan>
- <open question raised at end, still unanswered>

# NEXT

<concrete next action — derived from RECENT CONCLUSIONS, not stale earlier intent>

# WATCH OUT

<gotchas; omit section if none>

# SUGGESTED SKILLS

- `/plugin:skill` — <why the next session should invoke it>
```

## Rules

- Terse, scannable, under 250 words total.
- `# ORIGINAL PROMPT` anchors intent across sessions — do not drop it even if the work has drifted.
- **Weight the final turns heaviest.** Conclusions, decisions, course corrections, and open questions from the last few messages drive `NEXT`. Early-conversation context is backdrop, not the lead.
- `# RECENT CONCLUSIONS` captures what was just decided or learned — not a re-summary of DONE. If the last turns only restated earlier work, leave it empty rather than padding.
- If user and assistant disagreed or pivoted near the end, record the resolution (or that it's unresolved).
- Use file paths, not descriptions (e.g. `src/auth.ts:42`, not "the auth file").
- No prose narration ("we decided to...").
- **Redact secrets.** API keys, tokens, passwords, connection strings, and personal data never land in the file. Name where a value lives (`.env:DATABASE_URL`) instead of the value itself.
- **Point, don't copy.** Anything already captured in a spec, ticket, ADR, commit, or diff gets referenced by path or id — never re-summarized here.
- `# SUGGESTED SKILLS` names the skills the next session should invoke for this work, with a few words on why each. Omit the section when nothing specific applies.
- Omit `# WATCH OUT` when there are no gotchas.
