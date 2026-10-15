---
name: avoid-feature-creep
description: Prevent feature creep when building software, apps and AI products. Use when planning features, reviewing scope, building MVPs, managing backlogs, or when someone says "just one more feature".
---

# Avoid Feature Creep for Agents

Ship products that solve real problems without unnecessary complexity. Most successful products do fewer things well.

## Decision framework

Before adding ANY feature, answer each with evidence:

1. **Validate the problem.** Does it solve a real, validated user pain point? Have we talked to actual users? What evidence supports building it?
2. **Check alignment.** Does it support the core vision? Would it delay the current release? What are we NOT building if we build this?
3. **Measure impact.** How will we know it succeeds? Which KPIs change? Can we quantify the value?
4. **Assess complexity.** True cost (build, test, maintain, document)? New dependencies or debt? Can a simpler version ship first?
5. **Final check.** Would we delay launch a month for it? Differentiator or table stakes? Would removing it harm the core experience?

If questions 1 to 3 cannot be answered YES with evidence, do not build the feature.

## Scope rules

1. **Define and defend the MVP.** Write down what "done" means and what you are NOT building before you start, and reference it constantly. Template: `references/playbook.md`.
2. **Version-control scope.** Track it in `SCOPE.md`. Scope changes need an explicit commit naming the approver and the impact.
3. **48-hour rule.** Wait 48 hours before adding a requested feature to the backlog.
4. **Budget-based scoping.** When something comes in, something goes out: "Which of these three features should we cut to make room?"

## Working with AI agents

- State scope constraints at the start of every session: what you build, what is out of scope, when you stop.
- Agents are stakeholders. Log their suggestions with the agent as source and apply the same rigor. "The agent suggested it" is not a reason.
- Typical agent-driven creep: extra edge-case handling, unrequested refactors, extra tests, extra types. Each may be good, none is in scope unless you decide so.
- When an agent suggests out-of-scope work, add it to `DEFERRED.md` and stay on the current scope.
- Every 30 to 60 minutes ask: "Are we building the right thing today, or adding scope?" If adding scope, commit and restart.
- At session end compare built versus planned, note why scope expanded, list what to defer.

## AI product features

One AI feature at a time. Validate the use case with users first, measure actual usage. Before adding one answer: what task does it automate, how is it better than the non-AI alternative, what happens when it is wrong, can we ship without it.

## Backlog hygiene

Audit monthly. For each item older than 30 days: has anyone asked, does it still fit the vision, would anyone notice if it never shipped. Three "no" answers means delete. Use MoSCoW (Must, Should, Could, Won't) and be honest: most "Should" items are "Could".

## Already bloated

Audit features against usage data, categorize (core, supporting, peripheral, bloat), deprecate bloat with a warning period, move peripheral features behind advanced settings, then add creep checks to code review. Detail: `references/playbook.md`.

## Quick check for any request

1. What user problem does this solve?
2. What is the smallest version we could ship?
3. What are we NOT building to make room for it?
4. How will we measure success?
5. What happens if we never build it?

If these cannot be answered clearly, do not proceed.

## References

`references/playbook.md`: warning signs and costs, MVP scope document template, templates for saying no (stakeholders, executives, users, yourself, AI agents), AI feature red flags, backlog audit, AI session checks, scope decision log, recovery steps.

## Golden rule

Ship something small that works, then iterate on real usage data. Every feature you do not build is time back, bugs not fixed, and code not maintained.
