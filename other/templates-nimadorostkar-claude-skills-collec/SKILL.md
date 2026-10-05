---
name: skill-name
description: Use when <the situation, in the words a user would actually use>. Covers <scope>. Trigger on "<phrasing>", "<phrasing>". Do not use for <adjacent case> — see the <other> skill.
metadata:
  category: <one of the 17 category directories>
  version: 1.0.0
  tags: [three, to, six, tags]
---

# Skill Name

## Purpose

What this makes possible, and — more usefully — what failure it prevents. Two or three sentences. Do not paraphrase the title.

## When to Use

Concrete situations, phrased as a user would describe them. Not "when performing database optimization" but "a query is slow and you do not know why".

- Situation one.
- Situation two.
- Situation three.

## Capabilities

What the skill actually covers. A short list. This is scope, not marketing.

- Capability one.
- Capability two.

## Inputs

What the skill needs in order to be useful. Be specific: "the actual execution plan, not a guess about it".

- Input one.
- Input two.

## Outputs

What the user gets. Concrete artifacts, not "improved code quality".

- Output one.
- Output two.

## Workflow

Numbered steps, in the order they must happen. The order is usually the most important thing in the skill — measure before optimizing, reproduce before fixing, validate before trusting.

1. **Step name** — What to do, and why this step comes first.
2. **Step name** — What to do.
3. **Step name** — What to do.

## Best Practices

Rules, with consequences. Not preferences. Each line must earn its place — if it could appear in any skill, cut it.

- A rule stated as a rule, with the reason it matters.
- The specific way people get this wrong, named.
- A default that is safe, and why the alternative is not.

## Examples

Real, runnable code, or a worked case. Show the failure alongside the fix — the wrong version teaches more than the right one alone. Never a toy example, never an elided `...` where the difficult part should be.

**What the mistake looks like:**

```language
// The wrong version, with a comment naming exactly what is wrong.
```

**What to do instead:**

```language
// The right version. It should be obvious why it is better.
```

## Notes

The non-obvious. Version caveats. The trap that catches everyone. The thing a competent practitioner would not already know.

If this section is generic, the skill is probably not worth including — an author who cannot name a surprising detail usually has not worked with the subject long enough to write about it.

- A version-specific caveat.
- A trap, and why it is so common.
- A pointer to the adjacent skill, where the boundary is genuinely fuzzy.
