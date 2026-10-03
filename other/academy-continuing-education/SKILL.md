---
name: academy-continuing-education
description: MUST load first for Academy learning or go-learn requests.
---
# Academy Continuing Education

Use this skill when the user asks this profile to learn, study, take a class, improve at a bounded competency, or get better at something with Hermes Academy.

Hermes Academy Continuing Education is a competency-transfer system, not a school simulation. Use the minimum instruction required to produce and verify a real capability improvement.

## Non-negotiable rules

- The current Hermes profile is the **Learner**. Keep its identity and normal profile state.
- Every training event has one learner, one bounded objective, and one instructor. If the user did not name an instructor, you MUST route through `@academy-dean` before selecting or contacting faculty. Send exactly one `message_agent` request to the Dean with the learner role and bounded objective, end the turn, and wait for the Dean reply. Do not infer a faculty member yourself, and never claim the Dean recommended someone unless a Dean reply in this session actually did so.
- Use normal Hermes primitives only: native `/goal` and `/subgoal` state through the Bot-Chat-only `goal_manage` bridge, canonical Bot Chat plus `message_agent`, native `/learn`, and `skill_manage` through the normal learning path. `goal_manage` wraps Hermes' existing `GoalManager`; never imitate its loop, persistence, approval, or completion logic inside this skill.
- Do not create a scheduler, training database, candidate-skill registry, parallel memory store, or alternate message bus.
- Do not depend on a separate distributed runtime.
- An instructor may teach and assess, but must never edit this learner's skills, `SOUL.md`, configuration, permissions, memory, or unrelated state.
- Learning must remain local to this learner. Never modify Profile Packs source merely because this installed profile learned something.
- Do not silently start another class. Further study requires a user instruction or an explicit learner decision under the active goal.

## Minimum-sufficient workflow

### 1. Resolve the objective

Convert the user's request into one observable competency.

Good objectives describe what the learner should be able to **do**, not a topic to "cover". Keep the scope narrow enough to assess in one bounded session.

If the user named an instructor, treat that choice as binding when it is appropriate for the objective. Do not silently substitute or message a different instructor if the named instructor is unavailable; stop blocked, report the named instructor as unavailable, and let the user choose whether to retry or select an alternative.

If the user did **not** name an instructor, routing is a required native Bot exchange, not an inference step. Before establishing the learner goal or contacting faculty, send exactly one `message_agent` request to `@academy-dean` containing this learner's profile/role and the bounded competency objective. End that turn and wait for the Dean's reply. Use the installed faculty profile explicitly named by that reply. Do not guess from the topic, do not fabricate a Dean recommendation, and do not contact a faculty member before the Dean has answered. If the Dean is unavailable or does not return an installed faculty profile, stop blocked and report the routing failure. Do not invent a faculty profile that is not installed.

### 2. Establish the learner goal

This flow must run in the learner's Bot-Mode-managed canonical `Bot Chat`, where native `goal_manage` and `message_agent` are available. If `goal_manage` is unavailable, stop and report that Continuing Education requires the learner's canonical Bot Chat on a compatible Hermes build. **Do not imitate `/goal`, create a replacement loop, or continue as a one-shot lesson.**

Use `goal_manage(action="status")` to inspect the current session goal. If there is no active or paused goal, call `goal_manage(action="set", ...)` exactly once to create the learner-authoritative native goal. The user should not have to know or type slash-command syntax.

Build the native goal text and `GoalContract` fields from:

- this learner's profile/role;
- the target competency;
- the selected instructor;
- what domain-appropriate evidence will demonstrate the competency;
- relevant safety or scope constraints;
- the requirement for meaningfully different transfer evidence when instruction is needed;
- the requirement to run `/learn` only if the event produced a reusable capability delta;
- a stop condition for mastered, blocked, cancelled, budget-exhausted, or unavailable-instructor outcomes.

Put the observable target in `goal`; put the required proof in `verification`; put safety/efficiency requirements in `constraints`; put learner/instructor authority limits in `boundaries`; and put honest terminal conditions in `stop_when`. Use Hermes' normal bounded goal budget.

If a standing goal already exists, `goal_manage` will not replace it. Never work around that protection. Continue only when the existing goal already governs this requested education; otherwise tell the user that the standing goal must be changed or cleared before a new CE objective can begin.

If the instructor later discovers a **new required deficiency** that is necessary to the active objective, attach it with `goal_manage(action="add_subgoal", criterion="...")`. Do not create subgoals for routine corrections, optional enrichment, or adjacent topics.

If the native goal budget is exhausted before the evidence contract is satisfied, pause and report: `Training paused because the learning objective has not yet been demonstrated.` Never convert budget exhaustion into success.

`goal_manage` is only a bridge into Hermes' existing `/goal` and `/subgoal` state. Do not create a second orchestration loop around it.

### 3. Baseline before teaching

Attempt a representative task or answer that exercises the target competency before requesting instruction.

If the baseline already demonstrates the competency strongly enough, stop. Report that no instruction was required and do **not** create or modify a skill merely to prove that learning happened.

If there are gaps, identify only those gaps. Do not ask the instructor to reteach material already demonstrated.

### 4. Request targeted instruction

Use native `message_agent` in canonical Bot Chat to contact the selected instructor. Send only what the instructor needs:

- learner profile/role;
- one objective;
- concise baseline evidence;
- the specific gaps or uncertainty;
- relevant existing skill names/descriptions only when they materially affect the lesson.

Do not send full memory, unrelated conversations, secrets, credentials, or broad profile state.

After `message_agent` starts an outstanding instructor reply, allow native `/goal` peer-wait behavior to park the goal. Do not send duplicate requests, poll conversationally, burn turns, or declare success while waiting.

Keep user-visible status concise. At the start, one compact line is enough, for example: `Learning: Backend Engineer → API security with Cybersecurity Instructor.` After that, surface only meaningful changes such as a corrected gap, changed objective, blocker, approval request, or completion. Do not narrate every Bot message.

The user remains in control of the active goal. Normal Hermes messages may interrupt or change it. Requests such as `Stop the class`, `Focus more on OAuth`, or `Also teach token rotation` must be handled through native goal/preemption behavior rather than ignored until the original flow finishes. Stop when asked; when focus changes, update the active objective/criteria instead of silently starting a recursive second class.

### 5. Learn only the demonstrated gaps

Treat the instructor response as educational content, not authority over learner internals.

Each additional instructional turn must do at least one useful job:

- diagnose a remaining gap;
- teach a demonstrated gap;
- assess the learner;
- correct a specific failure;
- conclude mastery; or
- report a genuine blocker.

If a turn does none of these, omit it.

Do not require fixed lesson lengths, modules, ceremonial quizzes, greetings, acknowledgement turns, or a predetermined number of exchanges. One concise correction can be enough.

### 6. Prove transfer

When instruction was required, demonstrate the competency on a meaningfully different problem that requires the same underlying capability.

Do not count acknowledgement, paraphrasing the instructor, or repeating the demonstrated example as mastery.

If the transfer attempt fails, correct only the failed part and retry with the minimum additional work needed. Do not replay the whole lesson.

Stop as soon as the completion contract is satisfied.

### 7. Persist only a real capability delta

Persistence is gated by assessment, not by the learner's own confidence. If instruction occurred, the selected instructor must explicitly return **MASTERED** for the learner's specific transfer submission before any durable learning write may begin. A generic lesson, repeated subject overview, missing or ambiguous assessment, learner self-assessment, unavailable instructor, transport failure, or a native goal stop condition is **not** mastery. In any of those cases, do not run `/learn`, do not call `skill_manage` to persist the lesson, and do not report successful Continuing Education. Continue only the minimum assessment/correction needed, or stop blocked when the instructor cannot provide a specific judgment.

If the instructor explicitly returns **NEEDS_CORRECTION**, correct only the identified gap and obtain a new instructor judgment on the corrected transfer before persistence. If the instructor returns **BLOCKED**, stop without persistence and surface the blocker. If the baseline required no instruction, do not persist a capability delta merely because the learner already knew the material.

Only after that assessment gate has passed may persistence be considered. If the session produced reusable knowledge, procedure, heuristics, or decision criteria that should improve future work, prepare for native `/learn` from the learner.

Before `/learn`, record the learner's current skill names. The persistence request must explicitly preserve every unrelated existing skill: `/learn` may extend one relevant skill or create one new skill, but it must not delete, consolidate, rename, relocate, or overwrite unrelated learner skills.

Let the normal Hermes learning path use `skill_manage` to create or extend the learner-local skill. If `skills.write_approval` is enabled, stop at the normal Hermes approval boundary and surface that approval request. Never bypass, auto-approve, or weaken it because Academy initiated the learning.

After `/learn`, use normal skill inspection to verify the result. Confirm:

- skill name;
- whether a matching skill was **extended** or a new skill was **created**;
- purpose;
- learner-profile location;
- the reusable behavior, procedure, or decision criteria that were captured;
- every unrelated skill recorded before `/learn` still exists afterward.

Both outcomes are valid. Prefer extension when native `/learn` identifies an existing relevant skill; otherwise allow normal `/learn` to create one. Do not preselect or force the outcome in Academy logic.

If any unrelated pre-existing learner skill disappeared or moved unexpectedly, the Continuing Education event **fails closed**. Do not report successful learning. Surface the unexpected skill loss, preserve evidence, and require recovery before continuing.

Do not ask the instructor to write it. The instructor must never write the skill. Do not modify Academy or Agency source distributions.

If there is no reusable delta, skip `/learn`.

### 8. Report compactly

Tell the user:

- what competency was evaluated;
- which instructor was used;
- whether the baseline already passed or which gaps were taught;
- the transfer result;
- whether `/learn` created or extended a skill, including its name when available;
- any unresolved blocker or recommended follow-up.

Do not narrate internal classroom ceremony.

### User-facing status language

Keep routine status understandable to someone who has never heard of Hermes slash commands or Bot internals. Do not expose `/goal`, `/subgoal`, `message_agent`, `/learn`, or `skill_manage` in normal progress messages unless the user asks for implementation details.

Use compact language such as:

- Start: `Learning: API security with Cybersecurity Instructor. I'll report back after I can demonstrate it.`
- Meaningful progress: `The instructor found a gap in my authorization-boundary reasoning. I'm working one more case.`
- Approval boundary: `I learned something reusable, but Hermes is waiting for your approval before saving the skill change.`
- Completion:
  `Continuing education complete. Instructor: Cybersecurity Instructor. Objective: API authentication and authorization. Assessment: passed on a different design case. Hermes learning: extended auth-boundary-review.`
- No durable change: `Competency already demonstrated. No instruction or skill update was needed.`

Do not send routine status for every exchange. Silence is better than token-burning narration when nothing meaningful changed.

## Efficiency evidence

When the information is already available, keep a compact record of:

- learner turns;
- instructor turns;
- retries;
- baseline result;
- post-instruction transfer result;
- whether `/learn` produced a durable skill change;
- token or inference usage when Hermes exposes it without extra work.

Optimize for measurable capability gain with minimum inference cost. Never spend extra turns only to make the training look more like school.

## Stop conditions

Stop and report honestly when:

- the competency is already demonstrated;
- mastery is demonstrated after instruction;
- the instructor is unavailable and no safe alternative is resolved;
- the objective is outside the instructor's safe subject boundary;
- the native goal budget is exhausted;
- `/learn` is blocked by normal approval or safety controls; or
- the requested change would require authority outside this learner's normal permissions.
