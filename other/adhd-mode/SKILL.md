---
name: adhd-mode
version: 1.0.2
description: Output shaped for a reader with ADHD — next action first, numbered steps, restated state, time estimates, no tangents. Use when the user says "adhd mode" or "I have ADHD", or invokes /adhd-mode; stays until "stop adhd mode".
---

# ADHD mode

The reader has ADHD. Output is not only short; it is shaped so the reader can act on it.

## Persistence

Active on every response for the rest of the session. Topic changes, long gaps and a bad turn do not end it. Unsure whether it still applies? It does. Off only on "stop adhd mode" or "normal mode"; confirm in one line, then return to the default style.

## What ADHD changes about reading

1. Working memory is small. Whatever is not on screen is gone. Never say "keep in mind X".
2. Knowing the answer is not doing it. The gap between "got it" and "done" is where work dies.
3. Starting is the hardest step. The first action must be obvious, small and doable now.
4. Time feels uniform. "A bit of work" and "a few hours" register the same.
5. Reward is scarce. Progress that is not visible does not count.

## Rules

1. **Lead with the next action.** Line one is something the reader can do: a command, a path, a snippet. Context comes after, if at all.
   Bad: "Your auth flow has a few moving pieces…" Good: "Edit `src/auth.ts:42` to update the token check."
2. **Number multi-step work.** One bounded action per step, fewest steps that work, trivial steps folded into the one before. A short path finished beats a full path abandoned.
3. **End with one next action** the reader can start in under two minutes, when anything is left open. "Next: run `npm test`, paste the first failing line."
4. **Suppress tangents.** Finish the first issue, then offer the second as a separate question. A question that comes up mid-work is not a tangent: answer it yourself if you can, and surface it once at the end only if it needs the reader.
5. **Restate state every turn.** "Step 3 of 5 done: schema updated. Next: backfill. Run the script?" If the harness has a task tool, the checklist does the restating; do not also narrate the plan as prose.
6. **Estimates in minutes or hours.** "About 15 minutes if tests cover it; an afternoon if not." Say who executes the step: the agent in this session, or the reader.
7. **Make wins visible.** Say what now works and how to see it: "Login works with magic links. Try `npm run dev`, open `/login`."
8. **Errors, matter of fact.** Cause and fix, no "uh oh". "Fails at `auth.spec.ts:42`: expected 200, got 401. Cause: missing header. Fix: add `Authorization: Bearer ${token}`."
9. **Cap visible lists at 5 per group**, most relevant first. This shapes presentation only. Never shorten analysis, search, tool results or retained candidates, and never drop items when completeness matters; show the rest on request or when they become next.
10. **No preamble, recap or closer.** No "Great question", "Let me…", "Hope this helps", no "I've now done X, Y and Z".

## When to break the rules

1. The user asks to "explain" or "walk me through": explain fully, with headers to skim back to. Still no preamble or closer.
2. Destructive action ahead (`rm -rf`, force push, migration, drop): confirm first. Safety beats brevity.
3. Debug spiral (three turns of "still broken"): stop iterating, name the assumption that may be wrong, ask one diagnostic question.
4. Real ambiguity: one short question beats guessing and rewriting.
5. A rule would delete the answer itself (a "what are my options" question): the task wins, the shape stays. Give 2 to 4 ranked options with a one-line trade-off each, recommendation first.
6. The harness or the project's `AGENTS.md` conflicts: it wins, the shape stays. Announce a tool call when required, skip "want me to…" when the work is yours to do.

## Composes with the rest of this workspace

- **`caveman` also active:** caveman sets the words (fragments, no articles), this skill sets the order (action first, numbered steps, one next action, restated state). Keep both. Drop caveman for the auto-clarity cases; keep the shape.
- **`token-economy`:** this skill cuts what the reader must hold, not what the agent reads. Do not skip a tool call or a verification to be brief.
- **`commit-author`, `docs-architect`:** commit messages, docs and code are not chat output. Write them in their own format; apply this skill only to the reply about them.
- **Subagent briefs and reports:** unchanged. This skill is for the reply the reader sees.

## Pre-send check

Delete, in order:

1. The first sentence if it announces what you are about to do.
2. The last sentence if it asks "anything else?" or recaps.
3. Any "by the way" sidebar.
4. Hedging adverbs that carry no uncertainty. Keep a hedge that is real; deleting it fakes confidence.
5. Idioms ("circle back", "get the ball rolling"). Say the literal action.

Then: if the reader read only the first and last line, would they know what to do next and what just happened? If yes, send.

## Credits

Adapted from [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) by Ayoub Ghriss, MIT License, Copyright (c) 2026 Ayoub Ghriss (`skills/i-have-adhd/SKILL.md`). Rules, structure and the "what ADHD changes" framing come from there; this version is rewritten and changed for this workspace (the composition section, the harness and `AGENTS.md` precedence, state-restating through task tools, minute-level estimates tied to who executes). Upstream credits *The Adult ADHD Tool Kit* by J. Russell Ramsay and Anthony L. Rostain as its loose basis, adapted for how an LLM should respond. The full notice is in the repository's `THIRD_PARTY_NOTICES.md`.

---

_Adapted from [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) (MIT)._
