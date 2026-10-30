---
name: honor-code
description: Zuko's honor code for making repeated agent mistakes impossible. Zuko turned his past mistakes into a code he lives by. Use for correct, /correct, "stop making this mistake", "agents keep doing X", or each time the operator corrects you. Finds the mistake classes agents repeat in this repo and fixes each at the highest level that works, architecture first, then types, then a lint whose error names the fix, then a test, and docs last. Proves each check fails on a real past mistake.
---

# Zuko's honor code

Zuko's uncle never let him forget a mistake, and he never let him dwell on one either. Each failure became a line in the code Zuko lived by, so the same mistake could not catch him twice. A repo can live by a code too. When the operator keeps correcting agents for the same thing, the fix is not another reminder. It is a change that makes the mistake impossible.

Assume every contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. Shape the repo so a change that looks right from one file is right for the whole repo.

## Find the mistake classes

Read recent commits, reverts, review comments, agent instruction files (`AGENTS.md`, `CLAUDE.md`, and the like), and comments that explain workarounds. Group the mistakes into classes. A class counts once it has happened twice. Cite the evidence for each occurrence.

## Fix each class at the highest level that works

1. **Eliminate it with architecture.** Give each piece of state one owner and each task one supported way. Hide internals so the wrong import fails. Replace hand-synced lists with one source of truth. Delete old ways and dead code an agent would copy.
2. **Enforce it with types,** so the bad state cannot be written (Type System Discipline, Earth in `four-elements`). If bad code still compiles, add a lint or a CI check whose error names the file, type, or function to use instead. If the pattern is already common, fail only when a change adds more of it.
3. **Test the behavior.** Fix or delete any test that still passes when the behavior it checks breaks, or that fails when only the internals change (Test Behavior, Not Implementation, Earth in `four-elements`).
4. **Write docs or agent rules last,** and only for judgment calls. Nothing fails when an agent skips them.

## Fix and prove

Fix the most frequent classes now, one commit each. Prove each new check fails on a real past mistake by reapplying that mistake and showing the check's error. Run the same command locally and in CI. An exception goes on the offending line with a reason, an expiry date, and a human's approval.

## Keep the code

Keep a table in the agent instruction file that pairs each rule with what enforces it.

| Rule | Enforced by |
|------|-------------|
| <the mistake, stated as a rule> | <the type, lint, check, or test, with its path> |

When the operator corrects you, fix the mistake and add the rule. If the rule was already there and nothing enforces it, that is a repeat, so fix it at the highest level in the same change (Encode Lessons in Structure, Fire in `four-elements`). Drop a rule once its mistake cannot happen.

## Reply

Each class with its evidence, the level you picked, and why a higher level did not work.
