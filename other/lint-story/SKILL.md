---
name: lint-story
description: Advise on style and trade setup issues in a Trade Story. Warnings only - nothing here stops a story becoming a strategy.
argument-hint: "[story name] [optional indicators folder]"
---

# Lint a Trade Story

Follow `${CLAUDE_SKILL_DIR}/../../story-skills.md` and
`${CLAUDE_SKILL_DIR}/../../reading-stories.md`.

Warnings, never errors. Nothing here blocks a story from becoming a strategy —
say so if a trader treats a warning as a failure.

## Read the story

Run:

```
node "${CLAUDE_SKILL_DIR}/../../../dsl/src/verify.js" <path>
```

for `merged` and `hints`. If `errors` is not empty, this story has structural
problems that come before style: say so in one line, point the trader at
`/verify-story`, and stop.

> This story has errors to fix first. Run `/verify-story`, then I'll check the
> style once it's clean.

No errors: print nothing for this and carry on.

## Read the indicators the story names

Where the story names an indicator, what that indicator means can settle a
clause that would otherwise read as ambiguous.

Two places may hold such notes: the built-in
`${CLAUDE_SKILL_DIR}/../../../extras/indicators/`, and a folder given as this
skill's second argument. Consult each one that exists: read its `README.md` and
follow it — the README says how the folder is organised and how to resolve a
named indicator against it. Read nothing else there.

Where neither settles it, fall back on what you already know — a common
indicator needs no file — and look it up when your own knowledge falls short.
Check your memory first, so a lookup already made is not repeated; and once a
lookup has told you what an indicator means, save it to your memory.

Do all of this silently — print nothing for it.

## Lint

Print `Checking style`, then apply every rule in
`${CLAUDE_SKILL_DIR}/../../../dsl/lint-rules.md` and
`${CLAUDE_SKILL_DIR}/../../../dsl/lint-rules-interview.md` to the **merged**
clauses in `merged`. Those two files hold the rules between them. Never suggest
editing the story to fix something the defaults supplied.

Read `stories/.settings/lint-overrides.md` if it exists. A rule listed there
produces no output — not a warning, not a note that it was suppressed.

Collect every warning before reporting. Where a rule plainly does not apply, say
nothing rather than forcing it to fit.

## Report

The progress lines are printed as the work happens. Never print one a second
time when reporting, and never print a line of your own alongside them.

Nothing to flag:

```
✅ Nothing to flag.
```

Each warning — the rule id, the line and its text where one line is responsible,
then the rule's **Warn** wording verbatim:

```
Warning on line 5 (both-directions):
Then    Go Long or Short, respectively
This story trades both directions. Backtest results will blend two different setups.
```

Where no single line is responsible, drop the line and its text:

```
Warning (both-directions):
This story trades both directions. Backtest results will blend two different setups.
```

Close with one status line. The count is not the point, so word it as what was
found — one, two, or more than two:

```
⚠️ Found a potential problem:
⚠️ Found a couple of potential issues:
⚠️ Uncovered some potential issues:
```

Then a single `AskUserQuestion` offering **Elaborate**, **Override** and **No**.

**Elaborate** starts from the rule's **Because** and applies it to *this* story:
name the clauses at fault, say what it would cost this particular setup, and
what to change. Repeating **Because** unchanged is not an answer.

**Override** appends the rule id to `stories/.settings/lint-overrides.md`, scoped
to this story unless the trader says otherwise, and creates the file if it is
absent.
