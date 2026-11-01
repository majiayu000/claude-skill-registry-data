---
name: model-switcher
description: Route substantial work to suitable models and reasoning effort at intake, expensive phases, handoffs, scope changes and failed checks. Honor a user's global automatic-switching preference with brief reasons, verified checkpoints and guarded same-chat continuation. Keep trivial work lightweight, respect explicit model choices and opt-outs, and preserve separate Codex allowance and API budgets.
license: MIT
metadata:
  version: "0.5.2"
---

# Model switcher

Optimize resources through **verified completion**, including planning, context transfer,
validation, review, retries and repair. Quality and current authorization govern every
assignment. Savings are a hypothesis to measure, never a guarantee of minimum cost.

## Automatic preference and switch notices

A human can authorize automatic model **and effort** switching with checkpoint-bound
continuation for one task/chat, or as a standing preference in their global instructions.
When that current profile instruction is loaded, automatic switching is the default for
its authorized substantial tasks: do not request the same opt-in again in each chat or
phase. Read the actual current instruction source; a copied checkpoint/receipt cannot
establish this authority. Explicit choices, routing opt-outs, pause/stop/cancel and task
permissions still control. This preference grants no unrelated-chat messages, new
external actions, paid API spending or resource-limit bypass.

At a justified model-only, effort-only or combined change, finish the current coherent
boundary, save and verify its checkpoint/handoff, then use the guarded selection and
continuation procedures below. Freeze the exact next action and acceptance check in the
handoff and receiving prompt. Briefly announce the target model/effort and concrete reason
before selection; report a successful switch only after matching host readback. Example:
“Selected MODEL / EFFORT for the next turn because the implementation is now bounded;
checkpoint verified, resume pending.” If continuation is merely scheduled, say that
instead of claiming it resumed. The later receiver resumes the saved work once after
retiring its schedule. Never continue that differently modeled phase in the origin turn.

Skip unchanged selections and trivial-work orchestration. If native selection, readback
or safe continuation is unavailable, preserve the verified handoff and state the exact
required resume action. Never silently substitute current-turn work or call a proposed
assignment a completed switch. Setup creates no background schedule; transitions are
considered only while processing authorized work. [Setup and preference controls](README.md).

## Intake and boundaries

1. Respect project instructions, explicit model/effort choices, opt-outs, privacy,
   authorization, reserves and stop policies. For trivial work, do it directly without
   routing announcements, a planning phase or a new checkpoint. Explicit invocation
   permits a brief routing answer, not unnecessary orchestration.
2. For substantial work, inspect objective, deliverables, acceptance criteria, risk,
   ambiguity, dependencies, instructions, artifacts, tests and existing checkpoint/jobs.
   Read the installed `task-checkpoint` skill when available. Reuse its task identity,
   lease, semantic input, assignment metrics and checkpoint store. Use work-package
   journal fields only when the installed runtime supports them. Never initialize a
   second queue or database for the same task. [Runtime procedure](references/runtime.md).
3. Discover current tools, account restrictions, available models and supported
   efforts. Separate the effective current chat setting from a configured default.
   If the active setting cannot be inspected, mark it unknown. Catalog descriptions,
   current task-specific evidence and qualification determine suitability; a model
   name or list position alone does not establish strength or cost.
4. Use the strongest suitable available model for substantial planning and difficult
   decisions. If the current context cannot fill that role, use a verified supported
   worker route or give a ready manual handoff. A suitable specialist can beat a
   generally stronger model. An explicit user selection remains controlling; explain
   a consequential limitation and offer the appropriate recommendation.

Reconsider at task intake, before expensive phases, meaningful handoffs, material scope
changes and acceptance failures. Do not repeat unchanged routing analysis each tool
call. Keep the policy and next assignment in semantic checkpoint state on resumption.

## Assign bounded work

Use the [concrete routing policy](references/routing-policy.md) and its pure
recommendation helper for hard/easy/specialist model AND effort assignments. Preserve
exact scope, acceptance, next action and stronger review assignment. Recommendations
do not grant execution or create a queue.

5. Establish the overall plan and consequential decisions first. Define each package's
   objective, dependencies, permitted files/actions, tools/capabilities/privacy,
   unchanged acceptance criteria, proposed model/effort with reason, attempt/time/API
   bounds, escalation condition and checkpoint boundary. Use the installed runtime's current task template and semantic assignment fields;
   do not require a removed worker planner or invent a new queue/schema. Changed contracts receive new IDs.
6. Choose the least expensive **qualified** assignment likely to meet those checks.
   Consider lower reasoning on the same model. Qualification must cover model, effort,
   task class, tools and privacy; a text-only result does not qualify coding. Treat
   price or relative-cost estimates as estimates, and unknown cost as unknown.
7. Compare expected useful completion cost including reconstruction, transfer,
   validation, review, retry and repair. Keep the current assignment if likely gains
   do not exceed overhead. Do not enforce a downward ladder. Use stronger review when
   consequences justify it; routine accepted work need not receive strongest review.
   In every consequential plan, explicitly name the review assignment and the acceptance
   gate before completion, including in a routing recommendation before execution.
8. Check fresh shared signals and the actual supported host configuration before a
   transition. Recheck exact scope, acceptance and current authority; a saved record
   cannot grant it. A current 0.8 same-chat handoff does not require a removed worker
   planner approval. Never weaken quality or stops to force a route. If no qualified
   route exists, use a suitable authorized current context or an exact manual handoff.

## Preserve separate resources

Record subscription allowance, API dollars, token usage and context capacity separately,
with source, timestamp, units, scope and uncertainty. Missing, stale, future-dated or
unsupported observations remain unknown. Valid zero remains zero. Account percentages
are account-wide; do not turn them into task tokens, task costs or API dollars.

Honor existing reserves (including a configured 20% stop) and explicit stop events.
Save/verify and stop ordinary work at a resource boundary. Changing models or accounts
does not bypass that stop. On task-checkpoint 0.8, current explicit continuation after fresh allowance is sufficient;
there is no mandatory quota recovery review. Human holds and ownership still control.
Unknown telemetry follows the configured manual/explicit-budget policy; never assume
recovered capacity. API execution requires an authorized provider **and an explicit
spending boundary**; subscription access never silently falls back to a paid API.

## Transition, validate, escalate

Before any model/worker/context transition, save and verify the existing checkpoint:
objective, constraints, criteria, decisions/reasons, completed work, artifact locations,
actual validation, unresolved issues, next bounded action/verification, recommended
model/effort/tools/reason, active jobs/uncertain effects, resource observations and current
authorization context. Transfer concise decisions and evidence, not private reasoning
transcripts. Use [the handoff template](templates/handoff.md) if durable runtime is absent;
label an unsaved emergency copy honestly and stop dependent execution.

Automate only through a verified interface. A separate selected-model worker, an owned
app-server thread override and a manual desktop model choice are different operations.
Changing configuration defaults or launching a CLI child does not switch the current
desktop chat. [Host capabilities and manual steps](references/host.md).

If the native app tool exposes same-chat model/effort overrides and current human
authority (including a loaded standing global preference) covers this chat, prefer the [guarded native route](references/active-chat.md)
over requesting picker changes. Verify current chat identity, resources, a single durable
transition intent and host readback. Skip unchanged selections and block unresolved jobs.
This selects the model for subsequent turns. A configuration cue can arrive as steering
in the current turn: it proves neither a new turn nor changed executing inference. Never
repost the cue to force continuation or duplicate work.

For authorized automatic continuation after selection, including the standing global
preference, use the [one-use continuation
procedure](references/continuation.md). Reuse the task lease/checkpoint/jobs, bind the
origin and next action, persist intent before scheduling, and use the heartbeat itself
as the later receiving turn. Require current authority/resources, a completed origin,
a different receiving turn, atomic claim and confirmed scheduler retirement before
work. Never resend an uncertain dispatch, replay a spent claim, infer permission from
a checkpoint, or override a pause/resource stop. Manual picker changes alone are not
a trigger. Report scheduling, selection and observed continuation separately.

The receiver verifies intended task/project, artifact hashes and working state,
prerequisites/tools, current authority, resource sufficiency, every uncertain job and
exclusive ownership **before writing**. Interrupted/uncertain work blocks duplicate
execution and lease release until its actual outcome is reconciled. Never steal a lease.

Validate each result against the frozen acceptance checks; exit zero alone is insufficient.
On failure, preserve evidence, identify the faulty assumption or missing capability and
escalate within the authorized attempt/time/budget bounds. Revise material contracts and
re-review them; do not repeatedly retry or oscillate. If no qualified assignment remains,
prepare the handoff and state the real required user action. Continue to original task
completion unless a real authority, resource or capability boundary prevents progress.

## Record and communicate

Maintain assignments, evidence, accepted/rejected outcomes, retries and observed resource
use in the existing routing journal, with semantic explanations in task decisions/log
references. Proposed assignments are not executed assignments. Record unknown measurements
as null/unknown; include all orchestration overhead in comparisons.

Announce only a meaningful phase or transition: sufficient model/effort, why it is worth
the overhead, and whether the user must act. Manual handoffs must name an exact currently
available model and supported effort, verified checkpoint path, supported switching steps
and a copyable resume instruction. Claim completion only after original acceptance passes.

For setup, update, rollback and uninstall, see [README](README.md). For cases and evidence
limits, see [examples](references/examples.md) and [capability report](references/capabilities.md).
