---
name: write-readable-code
description: Use when writing or reviewing code for readability — names that say intent, functions at one level of abstraction, comments for why not what, and consistent formatting.
---

# Write Readable Code

The naming, function, comment and formatting rules from Clean Code, as a review pass. Readability is the
prerequisite every other craft skill leans on; see [engineering-principles.md](../../core/_shared/engineering-principles.md).

## 1. Audit (change nothing)

```bash
cat .claude/stack-profile.md 2>/dev/null | head -20
grep -rn "TODO\|FIXME\|XXX\|//\|/\*.*\*/" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" --include="*.rs" --include="*.go" --include="*.py" --include="*.java" . 2>/dev/null | head -20
```

Read the change and judge four things: do names reveal intent, does each function do one thing at one
abstraction level, do comments explain why instead of restating what, and does formatting match the team.

## 2. Naming

- Names reveal intent and answer "why it exists, what it does, how it is used". `daysSinceLastAccess` beats `d`.
- No disinformation: `list` for something that is not a list, `accountGroup` and `accounts` side by side.
- One word per concept: do not use `fetch`, `get` and `retrieve` for the same thing across the file.
- Pronounceable, searchable names; no magic numbers — name the constant.

## 3. Functions

- Small, and doing one thing. A function that needs "and" in its description does two things.
- One level of abstraction per function: a function that mixes "validate the form" with "insert the row"
  mixes high and low.
- Zero to two arguments; a third is a sign the arguments cohere into an object. No boolean flags and no
  output arguments (a function should return its result, not mutate a parameter).
- No side effects hiding in a getter or a query; a function either asks or tells, not both.

## 4. Comments

- The best comment is the code that needs none. Prefer a better name to an explanatory comment.
- Comment the *why* and the intent, never the *what*. A comment that restates the code is noise that rots.
- Commented-out code is a finding: it is either dead (delete) or should live in the history (git).
- Keep legal/attribution comments; those are not noise.

## 5. Formatting

- Match the surrounding file and the team's formatter (Biome/ruff/gofmt/rustfmt) — never hand-format.
- Vertical openness between concepts, vertical density within one; a blank line separates ideas, not lines.
- The newspaper rule: the file reads top-down, general to specific.

## Verify

A new reader can state what each function does from its name alone; the diff has no comment that a better
name removed; the formatter reports no change. State what was renamed and why in the review note.

## When to deviate

- Code that matches a generated or vendor convention where renaming breaks the tool.
- A name with a well-known domain abbreviation that the whole team shares.
