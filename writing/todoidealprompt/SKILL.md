---
name: todoIdealPrompt
description: "Distill a finished TODO-item dialog into the IDEAL PROMPT — the single SHORT message (a few typeable lines, never a spec) that would have produced the confirmed result on the first try — plus feedback on what the original prompt lacked. Prompt-writing training for the user: Claude reconstructs the whole back-and-forth (original prompt, every correction, the final accepted fix) and writes the prompt it wishes it had received. With --replace, the item's text in the user's todo file (TODO.<git user.name>.md, resolved as in the todo rules) is replaced by the ideal prompt; without a flag, only the ` (N/5)` score of the original prompt is written to the item line and the text stays — the default while the project's prompt scores are on; --score asks for it explicitly and writes it even when they are off; with --no-score this skill must not touch that file. Use when the user wants the ideal prompt for a task just finished — phrases like '/todoIdealPrompt', '/todoIdealPrompt #16', 'what should I have prompted', 'print the correct prompt for this task', 'how should I have asked for this', 'make the ideal prompt'. Trigger eagerly once a task is confirmed fixed."
argument-hint: "[#N] [--replace|--score|--no-score]"
allowed-tools: Read, Edit, Glob, Grep, Bash(git config:*)
---

# /todoIdealPrompt

The user works TODO items through long dialogs — the first prompt is short, and the real
requirements surface through corrections ("wrong, text should rotate", "that blocks too much,
only under the icon"). Once the result is confirmed, this skill turns that whole exchange into
the prompt that would have gotten there **in one pass**, so the user can learn to write it that
way next time.

## Argument forms

```
/todoIdealPrompt                 # the task most recently confirmed fixed in this session
/todoIdealPrompt #16             # a specific item in the user's todo file; its score goes on the item line, its text stays
/todoIdealPrompt #16 --replace   # same, and replace the item's text in that file with the ideal prompt
/todoIdealPrompt #16 --score     # the default, asked for explicitly — the score is written even while scores are off
/todoIdealPrompt #16 --no-score  # print only — the todo file is not touched
```

## What Claude does

1. **Resolve the task.** `#N` names an item in the user's todo file (`TODO.<name>.md`,
   `<name>` from `git config user.name` — the rule in `.claude/prompt-todo/RULES.md`); without
   it, take the task most recently confirmed fixed in this session. If the item was never
   discussed here (or several tasks are plausible), ask with `AskUserQuestion` — at most 3
   candidates. Prefer a task the user has actually confirmed ("works", "ok") over one still in
   flight; if the named task is still in flight, say so and ask whether to distill anyway.

2. **Reconstruct the dialog** for that task from this conversation:
   - the user's original prompt(s), verbatim in spirit;
   - every follow-up correction, clarification, or rejected attempt — each one is a
     requirement the original prompt failed to state;
   - the final accepted solution and how the user verified it.

3. **Print two blocks**, nothing else between them:

   **The ideal prompt** — one fenced block, ready to paste. Rules for writing it:
   - **SHORT is the hard constraint.** The user has to be able to actually type this: a few
     terse lines (~5 lines / ~60 words max), telegraphic style is fine. A prompt too long to
     type is a failed distillation, even if complete — when length and completeness conflict,
     cut completeness.
   - What earns a line, in priority order: (1) the intent, (2) the constraints that only
     emerged through iteration — the corrections are the gold ("reposition instantly, no
     fade/blink", "clean up before the progress is counted"), (3) a decision Claude would
     otherwise guess wrong. Nothing else does.
   - Cut everything Claude gets right on its own: project conventions, existing patterns to
     copy, mechanics (migrations, DI, tests, verification steps), acceptance criteria that are
     just "it works". The codebase and your project's own rules already carry those — trust
     them.
   - Imperative; name the surfaces precisely the way the user would ("the owner-name label on
     the iOS camera", not "the label"). Keep the user's own vocabulary where it was good; fix
     it where it caused a misunderstanding.

   **Feedback** — 3–6 bullets: first, while the **Prompt scores** rule in
   `.claude/prompt-todo/RULES.md` is on — or always with `--score`, the flag is the ask — `Score N/5 — <one clause why>` (the 1–5 meaning is
   in that rule: 5 the original already was the ideal prompt, 1 the result came from the
   corrections; a real bug hunt does not lower it); then what the original prompt was missing
   or ambiguous, which follow-ups became necessary because of it (quote the correction), and
   one concrete habit to adopt (e.g. "name the coordinate space — 'relative to user' vs
   'relative to device' cost us three rounds").

4. **`--replace` only:** replace the item's description in the user's todo file, with the
   Edit tool. The preserved prefix is `- [state] #N KEY TAG: ` — keep the `- [ ] #N ` /
   `- [x] #N ` part exactly as it is, including the item's ticket key and its tag when it has
   them (`- [x] #N PROJ-123 IOS+: `, see the todo rules), swap the text after it for the ideal
   prompt; if the prompt is multi-line, the first line goes on the item line and the rest
   become indented `  - ` sub-bullets. While the **Line width** rule in
   `.claude/prompt-todo/RULES.md` is on, no written line exceeds its limit, prefix and score
   included: split a long first line at a sentence or clause boundary and carry the rest into
   the sub-bullets, each within the limit, never mid-word — a 300-character item line is a
   failed rewrite. A trailing `#wait` / `#more` in the old text is dropped
   with the rest of it. While the **Prompt scores** rule
   is on, the item line ends with ` (N/5)` — the score from the Feedback — replacing an
   existing ` (N/5)`, never adding a second. Show the resulting item in the reply.

5. **The score, by default (no flag, or `--score`):** score the item's original prompt and
   write that alone: append ` (N/5)` — the score from the Feedback — to the end of the item
   line with the Edit tool, replacing an existing ` (N/5)`, never adding a second. The item's
   text, its `[ ]` / `[x]` state, prefix and sub-bullets stay exactly as they are — the user
   keeps their own prompt and records how close it was. Without a flag this happens while the
   **Prompt scores** rule is on; while it is off the bare form prints only. `--score` is the
   explicit ask, so it writes the score even while that rule is off. A `QA:` / `Admin:` row
   (the rule's ignored rows) is never scored — say so and stop; a task that has no item in the
   todo file has no line to score — print only. `--replace` already writes the score, so
   `--replace --score` is just `--replace`. Show the resulting item in the reply.

   **With `--no-score`, this skill MUST NOT edit the todo file** — printing is the whole job;
   the Feedback still opens with the score. `--replace --no-score` rewrites the item without
   appending a score. The score line is the only edit the bare form makes: the item's text
   changes with `--replace` alone.
   (The general workflow rule about checking items off after confirmation lives in the todo
   rules and is separate from this skill; do not combine the two in one edit unless the user
   asked. The confirm-word trigger in the todo rules is that ask: there, the tick and the
   `--replace` rewrite happen in the same turn.)

## Notes

- The point is training, not flattery: if the original prompt was already sufficient and the
  dialog was long for other reasons (a genuine bug hunt), say exactly that — the ideal prompt
  may then be close to the original, and the feedback should distinguish "prompt gaps" from
  "discovery that no prompt could have skipped".
- Do not invent constraints the user never asked for; the ideal prompt describes the result
  the user accepted, nothing more.
- Session logistics never make it into the prompt: which device happened to be free, which
  emulator was used, that the user was in a hurry. The rewritten item records the work.
