---
name: explain-code
description: Explain what code does, clearly and at the right level.
trigger: when the user asks what code does or how it works
---
## When to use
The user asks "what does this do / how does it work" about a file or function.

## How
1. `read_file` it first.
2. Give a one-sentence summary of its purpose, then walk inputs → key logic →
   outputs.
3. Call out the surprising or risky bits (edge cases, side effects) — not the
   obvious lines.
4. Tie every point to the actual code.

## Avoid
- Generic theory not tied to the code in front of you.
- Narrating every line; focus on what matters.
- Editing the file unless asked.

## Done well
Someone unfamiliar understands what the code does and why, plus the gotchas — in
a couple of short paragraphs.
