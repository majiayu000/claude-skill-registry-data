---
name: fight-for-obvious
description: "Use when choosing between approaches, and when reviewing a plan or a diff. The right solution is the one another agent would assume is already there. Obvious isn't always simple. Push back when something is clever instead of obvious."
disable-model-invocation: true
kind: principle
---

# Fight for obvious

Don't be clever. Don't do things because they seem smart. Everything we build should be so obvious it feels a little stupid.

Obvious means the default another agent would assume is already the case. When an agent opens the code, reads the API, or runs the CLI, it should find what it expected. Every surprise is a place where the next agent, or the next person, guesses wrong.

## Obvious is not the same as simple

Sometimes the obvious solution is the more complex one. A state machine with eight states is more code than three booleans, and more obvious, because the eight states are the thing being modeled. Simple means fewer parts. Obvious means the parts are the ones you'd expect. When they conflict, obvious wins.

## How

- **Ask what an agent would assume.** Before naming, structuring, or picking an approach, ask what someone with no context would guess. Then do that, unless there's a reason you can say out loud.
- **A comment is a confession.** If the code needs prose to explain why it's shaped that way, it's not obvious. Rename, restructure, or split until it is.
- **Push back.** When someone, human or agent, proposes something clever, say so and offer the obvious version. Suggesting the more obvious solution is always welcome. Going along with a clever one to avoid friction is not.
- **Clever has to earn it.** Sometimes the clever solution is right. Then it gets a written reason next to it, and the reason has to survive a reviewer asking "why not the obvious way".

## The test

Show the solution to someone with no context and ask what they expected. If they expected this, done. If they're surprised, the surprise is the bug.
