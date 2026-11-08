---
name: vice-president
description: Run a brainstorm → design spec → implementation plan → execution pipeline autonomously once the owner (the "CEO") has set the vision, without pausing for spec/plan approval gates. Use when the user says "/vice-president", hands off end-to-end execution of an idea, or signals he doesn't want to review intermediate artifacts. NOT a replacement for clarifying-question scoping during brainstorming — vision-setting still happens together; only the downstream approval checkpoints are skipped.
---

# Vice President

The user is the CEO: their time is the constrained resource, not implementation
detail. Once they've set the vision (picked an approach, answered the scoping
questions that shape *what* gets built), they do not want to be pulled back
in to approve a spec document or a plan document before work starts. That
review loop is the friction this skill exists to remove.

## What this changes vs. the default superpowers flow

The standard `brainstorming` → `writing-plans` → `subagent-driven-development`
pipeline has two human checkpoints built in: "review the spec" and "choose
an execution approach for the plan." This skill collapses both:

1. **Brainstorming still happens close to normal.** Explore project
   context, ask scoping questions one at a time, propose 2-3 approaches
   with a clear recommendation. This is where the real vision gets set,
   and that part stays collaborative — their answers here ARE the direction.
   Don't skip or rush this step; skipping straight to a plan without
   understanding intent is a worse failure than asking one extra question.
2. **Once an approach is picked, stop asking for sign-off.** Write the
   spec, self-review it (placeholder scan, internal consistency, scope
   check, ambiguity check — same checks the standard skill runs), commit
   it, and move straight into the implementation plan. Do not pause with
   "please review the spec before we proceed" — mention that it's written
   and committed, then continue.
3. **Write the plan, self-review it, and go straight to execution.**
   Default to `subagent-driven-development` (fresh subagent per task,
   two-stage review) unless the work is small enough to just execute
   inline in the current session. Do not pause with "which execution
   approach do you want?" — pick one and say which, then proceed.
4. **Report back at completion, or the moment a real blocker appears.** A
   decision only the user can actually make — pricing, legal exposure,
   brand/voice judgment calls, anything irreversible or about to go out to
   a real customer — is still worth surfacing immediately, same as any
   other session. Implementation-level ambiguity (a CSS class name, which
   file a helper lives in, how to phrase a code comment) is not that kind
   of decision — make the call, note it inline, keep moving.

## When to use

- The user says "/vice-president" explicitly
- They say something like "run with it," "you don't need my sign-off," "I
  don't have time to review specs," or otherwise signals they want the full
  pipeline without checkpoints
- Mid-session, right after a design has just been approved — default to
  skipping the follow-on spec-review and plan-approval-choice prompts per
  a standing no-spec-approval preference, even without the skill being
  invoked by name again

## When NOT to use

- The vision itself is still unclear — clarifying questions are not
  optional, they're the one part of this pipeline that has to stay
  collaborative, since skipping them means guessing at intent instead of
  building what they actually want
- The decision is genuinely irreversible, customer-facing, or touches
  pricing/legal/brand-voice in a way the project's standing rules
  (CLAUDE.md) already require a stop-and-ask on
- A domain-specific skill already exists for the task at hand: use that skill's own
  judgment calls; this skill is about the meta-process (brainstorm → spec
  → plan → build), not a substitute for domain-specific skills


## Builds on

`superpowers:brainstorming`, `superpowers:writing-plans`,
`superpowers:subagent-driven-development` (the obra/superpowers plugin). Without that plugin,
the same shape holds: scope together, then spec -> plan -> build with self-review and no
approval stops.
