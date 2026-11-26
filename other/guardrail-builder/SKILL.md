---
name: guardrail-builder
version: 1.0.0
description: Find the mistakes agents keep repeating in a repo and make each one impossible, in order - architecture, types, a lint whose error names the fix, a test, docs last - and keep a rule-to-enforcer table in AGENTS.md. Use when the operator corrects you for the same thing twice, or asks to harden a repo against agent mistakes.
---

# Guardrail Builder

The operator keeps correcting agents in this repo for the same mistakes. Change the repo so the next agent can't make them.

Assume every contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. Design the repo so a change that looks right from one file is right for the whole repo.

## 1. Find the mistake classes

Read recent commits, reverts, review comments, agent instruction files, and comments that explain workarounds. Group the mistakes into classes. A class counts once it has happened twice.

## 2. Fix each class at the highest level that works

1. **Eliminate it with architecture.** Give each piece of state one owner and each task one supported way. Hide internals so the wrong import fails. Replace hand-synced lists with one source of truth. Delete old ways and dead code an agent would copy.
2. **Enforce it with types so the bad state can't be written.** If bad code still compiles, add a lint or CI check whose error names the file, type or function to use instead. If the pattern is already common, fail only when a change adds more.
3. **Test the behavior.** Fix or delete any test that still passes when the behavior it checks breaks, or that fails when only the internals change. See [`test-designer`](../../quality/test-designer/SKILL.md).
4. **Write docs or agent rules last, only for judgment calls.** Nothing fails when an agent skips them.

Configuration beats instructions: prefer a setting, then a hook, then a sentence. This is the same ordering [`token-economy`](../../meta/token-economy/SKILL.md) uses for instructions that load every session.

## 3. Fix and prove

Fix the most frequent classes now, one commit each. Prove each new check fails on a real past mistake. Run the same command locally and in CI. Exceptions go on the offending line with a reason, an expiry date and a human's approval.

## 4. Keep the rule table

Keep a table in the agent instruction file that pairs each rule with what enforces it. [`repo-tooling-architect`](../../tooling/repo-tooling-architect/SKILL.md) defines where `AGENTS.md` lives and how long it stays, so the table follows its rules: `AGENTS.md` is the single source, `CLAUDE.md` stays thin, and the table never duplicates content between them.

| Rule | Enforced by |
|---|---|
| Skill name matches its directory | `task skills:check` |
| Never import another module's internals | package visibility, lint error names the public entry point |

When the operator corrects you, fix the mistake and add the rule. If the rule was already there and nothing enforces it, that is a repeat, so fix it at the highest level in the same change. Drop a rule once its mistake can't happen.

**Reply:** each class with its evidence, the level you picked, and why a higher level didn't work.

---

_Adapted from [cursor/plugins pstack `correct`](https://github.com/cursor/plugins/tree/0b46ec399d55f2829e88822998f53b84944837d3/pstack/skills/correct) by Lauren Tan (MIT). Changed for this workspace._
