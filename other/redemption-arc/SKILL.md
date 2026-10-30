---
name: redemption-arc
description: Zuko's redemption arc for incidents and postmortems. Use for an outage, a bad deploy, data loss, a production incident, "what went wrong", "write the postmortem", or owning a mistake. Stabilizes first, then builds a blameless timeline, finds the root cause, and turns the lesson into structure.
---

# Zuko's redemption arc

Zuko's honor did not come back when he caught the Avatar. It came back when he owned what he had done and changed how he acted. An incident is the same. The goal is not blame. It is a system that cannot fail the same way twice.

## During an incident

1. **Stabilize first.** Stop the bleeding with the fastest reversible action: roll back, disable the flag, scale up, fail over. Diagnosis waits until users are safe.
2. **Pause for anything irreversible.** Data deletion, schema changes, and customer messages need a human decision.
3. **Keep a running log.** Timestamps, what was observed, what was tried, and what changed. You will need it for the timeline.

## After it is stable

1. **Build the timeline.** From logs, deploys, alerts, and chat: when it started, when it was detected, when it was mitigated, when it was resolved. Every entry cites its source.
2. **Measure the impact.** Who was affected, for how long, and what they lost. Use real numbers or label them *estimated*.
3. **Find the root cause.** Use `healing-water` to reproduce and name the mechanism. When the evidence is a live process or a captured profile, use `ember-trace` to read it first. Then ask why the mechanism was possible, and why it was not caught. Stop at causes you can change.
4. **Ask what helped and what hurt.** Which alert fired, which dashboard lied, which runbook was missing, which step took longest.
5. **Turn lessons into structure.** For each lesson, pick the strongest fix that exists: a test, a type, a lint, a check in CI, an alert, a guard in the deploy, before a document or a reminder. A lesson that lives only in prose will be forgotten. When the incident repeats a mistake class agents keep making, run `honor-code`.
6. **Write the postmortem** with `tea-time`.

## Postmortem shape

```markdown
# <Date>: <What broke, in user terms>

Summary: <two sentences>
Impact: <who, how long, how much>
Timeline: <timestamped, each line with its source>
Root cause: <mechanism, and why it was possible>
What went well: <short list>
What went poorly: <short list>
Actions: <owner, structural fix, tracking link>
```

## Rules

- Blameless. Name systems and decisions, never a person as the cause.
- No action item without an owner and a tracking link.
- Every action prefers structure over prose (Encode Lessons in Structure, Fire in `four-elements`).
