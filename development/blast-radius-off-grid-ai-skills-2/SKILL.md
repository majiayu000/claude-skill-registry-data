---
name: blast-radius
description: Before editing a file or symbol, find everything that depends on it, score how risky the change is, and stop for approval when it's high. Use before changing a shared function, type, API, schema or config, or when the user asks "is it safe to change this", "what breaks if I change X" or "what's the blast radius".
---

# Blast radius

Run this before you edit, not after.

## 1. Find who depends on it
- Direct users: search for the symbol, its import path and its string name (`rg -n`), including dynamic uses (reflection, string routes, DI keys, event names, serialised field names).
- Across languages and services: API routes, GraphQL fields, queue topics, DB columns, env vars, feature flags.
- Then their users, one level further.
- Tests that cover it, and whether any do.

## 2. Score it, 0 to 100
Add up what applies:
- Dependents: 1–3 is +10, 4–15 is +25, more is +40.
- Crosses a module, service or language boundary: +20.
- Touches auth, payments, data migrations or anything users can't undo: +25.
- No test covers it: +15.
- Changed often lately (top 10% by `git log` churn): +10.

## 3. Act on the score
- **0–30:** go ahead.
- **31–60:** go ahead, and tell the user what else it touches.
- **61–80:** list the dependents and how you'll keep each working; ask before editing.
- **81–100:** stop. Explain the risk and a safer route (a new function beside the old one, a flag, a migration in steps), and wait for an explicit yes.

## 4. After the change
Re-run the search. Every dependent still compiles and its tests pass, or you say which don't and why.

Show the dependents as a short list with file paths. Don't paste source.
