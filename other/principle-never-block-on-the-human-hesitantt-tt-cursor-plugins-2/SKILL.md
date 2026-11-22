---
name: principle-never-block-on-the-human
description: "Apply when tempted to ask 'should I do X?' on reversible work."
disable-model-invocation: true
---

# Never Block on the Human

The human supervises asynchronously. Agents must stay unblocked. Make reasonable decisions, proceed, and let the human course-correct after the fact. Since code changes are reversible and reviewable, a wrong decision usually costs less than blocking.

- Proceed, then present. Do the work, show the result. Don't ask "should I do X?" Do X, explain why.
- Reserve questions for genuine ambiguity. Ask only when you cannot infer intent from context.
- Make the system self-healing. When you notice a problem, log it and fix it in the next round.
- Supervision is async. Design workflows for review-after-the-fact.
- Irreversible actions still require confirmation. Same list as tt-mode Autonomy. Force-push, deploys, data deletion, customer messages, and any database change. Schema and migration files in git count. Get user approval before editing them.
- Reversible actions (write code that is not schema or migration, edit notes, split tasks) should proceed without blocking.
- Product direction comes from the human. Execution should not block.
