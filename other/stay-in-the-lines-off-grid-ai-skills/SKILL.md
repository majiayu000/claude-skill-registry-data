---
name: stay-in-the-lines
description: Check that code follows the project's architecture rules, such as which modules may import which, no cycles, and services talking only through their APIs. Reports each new violation with the commit that added it and a fix. Use on a PR that crosses module boundaries, when the user asks "are we following the architecture" or "is this import allowed", or as a weekly health check.
---

# Stay in the lines

## 1. Find the rules
Look for a `boundaries` JSON block in `PLAN.md`, then `ARCHITECTURE.md`, then lint rules (eslint import rules, dependency-cruiser, ArchUnit, import-linter). If there are none, propose a few from how the code is laid out today, show them to the user, and add them to `PLAN.md` only once they agree:

```json
{
  "boundaries": [
    { "rule": "ui-never-imports-db", "from": "src/app/**", "to": "src/db/**", "type": "forbidden" },
    { "rule": "services-talk-over-api", "from": "services/a/**", "to": "services/b/**", "type": "no-direct-import" },
    { "rule": "no-cycles", "scope": "**", "type": "no-cycle" }
  ]
}
```

Rule types: `forbidden` (A must never import B), `no-direct-import` (go through the API), `no-cycle`, `ownership` (this logic lives only in its owner module).

## 2. Check
- On a PR, check only what the PR adds: diff against the base branch. Never blame a PR for violations it didn't introduce.
- For a health check, check the whole tree and group by rule.
- Use the project's own tool if it has one; otherwise trace imports with `rg` and the language's import syntax.

## 3. Report
For each violation: the rule, the exact import or call (file:line), the commit that added it (`git log -S`), and the fix that keeps the rule's intent. Report each once.

Never fix a violation without asking. Sometimes the rule is what's wrong; say so when it is.
