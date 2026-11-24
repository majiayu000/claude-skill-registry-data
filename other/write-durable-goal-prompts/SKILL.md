---
name: write-durable-goal-prompts
description: Write or repair a durable goal prompt for Autorun, /goal, or another long-running agent. Use when asked for a "goal prompt", "goal paragraph", "durable goal", or when an autonomous goal became stale because it embedded a commit, count, phase, or temporary decision.
license: Apache-2.0
metadata:
  version: 1.0.0
---

# Write durable goal prompts

<purpose>

Write a compact objective that remains correct while implementation state changes. Keep durable
intent, authority boundaries, and completion criteria in the goal; point to living project state
instead of copying volatile facts into it.

</purpose>

<requirements>

1. State the user-visible outcome and why it matters.
2. Preserve the user's latest instructions over any plan, note, previous goal, or generated text.
3. Keep commits, test counts, phase numbers, current blockers, and temporary decisions out of the
   goal. Point to the living plan or status artifact that owns them when one exists.
4. Name authoritative project artifacts only after verifying they exist or explicitly saying they
   will be created. Prefer project-relative paths unless the target runtime requires absolute ones.
5. Include the boundaries that must remain stable: scope, permissions, destructive actions,
   external side effects, paid operations, live-system access, and release authority.
6. Define completion by observable outcomes and evidence, not effort, confidence, or a fixed number
   of iterations. Do not require endless polishing after the acceptance gate passes.
7. Keep the goal independent of one provider's tools. Put host-specific invocation syntax, length
   limits, task APIs, and resume behavior in the delivery note, not the portable goal, unless the
   named runtime makes them part of the requested artifact.
8. Do not mine private history by default. When prior user wording materially affects the contract
   and AI Session Search is available, use a bounded search, verify the human-authored messages,
   and record its limits. Otherwise use current user-provided and locally checkable evidence.
9. Never import another project's names, paths, corpus, examples, or preferences into a public or
   unrelated goal.

</requirements>

<workflow>

## 1. Establish the current contract

Read the current request, applicable project guidance, and any named plan or status artifact.
Separate durable requirements from current state. Resolve later corrections before drafting and
retain unresolved conflicts as explicit questions or blockers rather than silently choosing.

## 2. Discover the target interface

Identify the actual harness and goal mechanism. Check its current argument and length rules when
they matter; do not reuse a limit observed on another host. If no durable goal feature exists,
return a portable prompt the user can give to the long-running agent.

## 3. Draft the smallest sufficient goal

Use this order when applicable:

1. outcome and motivation;
2. authoritative living plan/status artifacts;
3. instruction precedence and change handling;
4. critical operating constraints and permissions;
5. evidence-backed definition of done.

Keep operational detail in the plan. Include a method rule only when omitting it would materially
change safety, correctness, or the requested outcome.

## 4. Audit durability

Reject or rewrite any sentence that:

- will become false after the next commit, phase, test run, or decision;
- grants authority the user did not grant;
- duplicates mutable plan content;
- assumes a tool or runtime capability not established for the target;
- contains unrelated private or project-specific material;
- cannot change the agent's decisions or completion gate.

Verify every named path and measure the final character count against the target's actual limit
when known. If the prompt is too long, move mutable detail into the living plan before removing a
durable constraint.

</workflow>

<output_contract>

Return:

- the goal as one copyable fenced block;
- the target harness and verified limit or `unknown`;
- the living artifacts it references;
- material assumptions, unresolved conflicts, and evidence limits;
- any detail deliberately kept in the plan rather than the goal.

Do not install, start, replace, or cancel a goal unless the user separately authorized that action.

</output_contract>
