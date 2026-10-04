---
name: simple-debug
description: Find serious bugs before ship, or trace a reported bug to its root cause. Use when the user asks to debug, hunt bugs, or find why something breaks. Reports only, does not fix unless asked.
metadata:
  author: denniemok
  version: "1.0.0"
license: MIT
---

# Simple Debug

Scan for high impact issues only. Scope is the whole codebase unless the user names files, a feature, or a symptom. If a symptom is given, trace it to the root cause first.

## Look for problems that

1. Break core logic or core workflows
2. Cause crashes or runtime failures
3. Corrupt data or produce invalid states
4. Block user actions or ruin the user experience
5. Introduce security risks or unsafe behavior

Ignore style issues, harmless edge cases, and personal preferences.

## Rules

- Read the code paths involved before claiming a bug. Trace real inputs through the logic.
- Report only what you can explain with a concrete failure scenario. Drop guesses.
- Separate real bugs from engineering tradeoffs. Mention a tradeoff briefly, never as a bug.
- Report only. Do not change code unless the user asks.

## Output

For each bug:

- `file:line`
- What breaks, and the input or state that triggers it
- A one line suggested fix

End with a verdict: safe to ship, or not, and the blockers. If nothing serious is found, say so plainly.
