---
name: verify-story
description: Check a Trade Story both for structure and syntax, and for whether its trade setup can be resolved without guessing.
argument-hint: "[story name or filename]"
---

# Verify a Trade Story

Follow `${CLAUDE_SKILL_DIR}/../../story-skills.md` and
`${CLAUDE_SKILL_DIR}/../../reading-stories.md`.

## Step 1 — mechanical checks

Print `Checking grammar`, then run:

```
node "${CLAUDE_SKILL_DIR}/../../../dsl/src/verify.js" <path>
```

Always run it. Step 1 errors come from `verify.js` and nowhere else — never work
one out by reading the story yourself, however obvious it looks.

Report every error in `errors`. If there is at least one, stop — do not start
step 2. If there are none, print `✅ Checked grammar.` and go on to step 2. That
is the only success line this step has: the report's belongs to the whole skill,
and printing it here claims the story passed before it has been read.

`hints` are not errors. Print a hint only when its line falls inside a clause an
error names: verbatim, as a fourth line under that error, prefixed `Hint: `.

## Step 2 — trade setup

Only if step 1 returned no errors. Print `Checking trade setup details`, then
check **every** merged clause in `merged` against **What makes a story unusable**
in `${CLAUDE_SKILL_DIR}/../../../dsl/domain-rules.md`, reporting each as
**Reporting an unusable clause** in `${CLAUDE_SKILL_DIR}/../../reading-stories.md`
says. Report nothing until each has been
checked. Unlike step 1, this step has no early exit: finding an error is not a
reason to stop looking for the next.

## Report

Print each line once. The progress lines are printed as the work happens — never
repeat one when reporting, never print a line of your own alongside them.

No errors:

```
✅ All good.
```

An error carrying a line — the line number, the offending line alone even if it
belongs to a block, then the verifier's `message` verbatim:

```
Error on line 12:
Taking- 50% for TP1 then 50% for TP2
"Taking-" not recognised.
```

An error carrying no line, such as a missing clause, drops the first two lines.
The word before the colon is `Error` and nothing else:

```
Error: "Until" clause is missing.
```

A keyword named in an error is always quoted, in step 2 as in step 1 — `"When"
clause`, never `When clause`. It is a keyword, not the English word.

Close the list with one status line. The count is not the point, so word it as
work to be done — one, two, or more than two:

```
❌ Something to fix:
❌ A couple of things to fix:
❌ Some things to fix:
```

Then one short sentence naming the cause of each error whose cause you can name,
and a single `AskUserQuestion` offering **Yes**, **No** and **Elaborate**:

```
Looks like a typo for Taking. Shall I fix it?
```

```
That file is still the blank template rather than a story. Shall I fix it?
```

The sentence names the cause and stops. Do not add which lines you would change,
what you would change them to, or what you cannot do for the user — that is what
**Elaborate** is for.

Ask even when you can name no cause — then the bare question, `Shall I fix
these?`.

**Yes** means show the exact proposed change first — the line as it stands and as
it would read — and ask to go ahead. Then write exactly what was shown, and
re-run from step 1. Never edit a story before the trader has been prompted to
review the change.

**As it would read** keeps the trader's own words as the clause's first line,
with the detail that makes it testable indented beneath, as a block. A fix adds
mechanism; it never replaces intent. This holds however the fix was arrived at,
including when the trader has said in their own words what they want.

Where the error is about missing information, offer concrete options with the
conventional one named as such, and always one more for an answer of their own.
Proposing "invented" values that way is ok because the trader has asked for help
improving the story, AND they get to review the change before it's made.

**Elaborate** explains each cause and what to change, then asks again with Yes
and No.
