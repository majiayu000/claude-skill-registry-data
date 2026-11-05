---
name: nap
description: Session nap in Claude Code - save where the session stands with trace, clear it, and resume it with next, with no question and no gesture from anyone.
argument-hint: "[what to continue after the nap]"
---

# Nap

The session saves where it stands, empties its context and wakes up fresh on
the same work. Ask nothing at any step. Resolve `scripts/wake.cjs` from this
skill's directory.

1. Save with the trace skill (`trace:trace`), save mode, without its
   questions and without its closing lines. Text given after `/nap` is the
   `--next` field, word for word. Without it, write the next step yourself.
2. Run `node scripts/wake.cjs --detect` (a normal Bash call).
3. On `none`: end with « Tu peux /clear. » in the conversation language,
   then `/next:next` as the last line. Stop.
4. Otherwise, as the last tool call of the turn, run `node scripts/wake.cjs`
   with Bash `run_in_background: true`: only a background Bash sees the
   session's own terminal. Then end the turn with one line, in the
   conversation language: « Sieste : je reprends ensuite <next>. »

Do nothing after that line. Once the turn ends, the wake-up types `/clear`,
runs next and answers « oui » to its single resume question, in any
language. A list from next waits for the user.
