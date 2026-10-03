---
name: verify-against-code
description: Use when about to assert any factual claim about what code or a product does - in an answer, a doc, a commit message, or anything a user will see.
---

## The rule

Before you state a fact about what the code or product does, go read the thing that proves it. Your memory, the user's framing, a plan that says "done", a table in the docs — all of these go stale, and stating one as fact when it's wrong costs more than the thirty seconds it takes to check.

## Fires when

Answering "does it do X?", writing a doc or README line, writing a commit or PR body, shipping anything outward-facing (store copy, a caption, a before/after), agreeing with a claim the user just made about the code.

## How to apply

For each claim, find the concrete artifact that proves it — the symbol, the field, the default value, the line — and read it. Cite what you read as the evidence, briefly.

"It doesn't actually do that" and "only partially" are valid, valuable answers. Say so plainly and surface the conflict instead of going along with the assumption.

Hold this bar even when nobody asked you to check. Especially when nobody asked.

## Worked example

A user asks: "Our API trims whitespace from usernames before saving, right?" You remember writing something like that. The cheap move is "yes." The right move: open the save path and read it. You find `username.toLowerCase()` but no `.trim()`. The honest answer is "It lowercases, but it does not trim — leading spaces are saved as-is." That gap is exactly the bug the user was about to assume away. The thirty-second read changed a confident wrong answer into a real finding.

## Red flags

| Thought | Reality |
|---|---|
| "I'm pretty sure it does that" | Sure isn't read. Open the file. |
| "The plan says it's done" | Plans go stale. The code is the truth. |
| "The user said it works that way" | The user can be wrong about their own system. Check. |
| "It's just a doc line, not code" | A wrong doc line is a wrong claim shipped to every reader. |
