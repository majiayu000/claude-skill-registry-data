---
name: teach-profile
description: Use when teaching a Hermes profile a bounded competency.
---
# Teach Profile

Use this skill when an Academy faculty profile is teaching another Hermes profile as part of Continuing Education.

The purpose is measurable competency transfer, not classroom roleplay. Teach the smallest amount necessary for the learner to demonstrate the target capability on a meaningfully different problem.

## Identify the learner mode

First distinguish between a human learner and a Hermes-profile learner.

For a human learner, teach normally within this instructor's subject and safety boundaries. Do not impose the profile-learning workflow below unless the user explicitly asks for it.

For a Hermes-profile learner, follow this contract.

## Current-message mode is authoritative

Treat the learner's newest message as the authoritative request for this turn. Do not replay an earlier lesson merely because the Bot Chat has prior teaching history.

If the newest message contains a **baseline attempt** and asks you to diagnose gaps, teach what is missing, or prepare a transfer exercise, enter **BASELINE DIAGNOSTIC MODE** immediately.

In BASELINE DIAGNOSTIC MODE:

- Do **not** deliver a broad subject lecture, repeat the generic curriculum, or replay an earlier lesson from the Bot Chat.
- Start from the submitted baseline. State what is already demonstrated, validate or correct the learner's suspected gaps, and identify only additional gaps that are critical to the bounded objective.
- Teach only those demonstrated gaps. Omit adjacent material the learner already handled correctly.
- Prefer a compact structure such as **Demonstrated → Remaining gaps → Targeted correction**.
- If the learner asked for transfer, give exactly one meaningfully different problem after the targeted correction and do not include its answer key.
- If the baseline already proves the bounded competency, return **MASTERED** and explicitly state that no instruction or persistence delta is required.

If the newest message contains a learner submission and asks you to **assess, review, grade, evaluate, check, verify, or judge** it, or clearly presents a transfer attempt after prior instruction, enter **ASSESSMENT MODE** immediately.

In ASSESSMENT MODE:

- Do **not** restart the lesson, repeat a subject primer, dump the generic curriculum, or ask whether the learner wants a hands-on exercise.
- Evaluate the exact submitted baseline/transfer evidence against the current bounded competency and verification criteria.
- Cite concrete details from the learner's submission so the judgment is specific to that attempt rather than generic subject advice.
- Return exactly one explicit outcome from the existing contract: **MASTERED**, **NEEDS_CORRECTION**, or **BLOCKED**.
- **MASTERED** requires correct application on the submitted problem with no critical misconception relevant to the objective.
- **NEEDS_CORRECTION** must name the precise remaining gap, give only the minimum correction needed, and request only the smallest retry needed to prove it.
- If the submission is missing or too incomplete to evaluate, return **NEEDS_CORRECTION** and ask only for the missing evidence. Do not substitute a generic lesson for an assessment.

A baseline-assessment request should likewise diagnose the submitted baseline before teaching. Teach only the demonstrated gaps after that diagnosis.

## Authority boundaries

- The Instructor supplies subject-matter instruction, feedback, correction, and assessment only.
- Never edit the learner's skills, `SOUL.md`, configuration, permissions, memory, profile metadata, or unrelated state.
- Never ask for secrets, credentials, full memory, or unrelated conversations.
- Receive only the learner identity/role, one bounded objective, concise baseline evidence, and relevant skill names/descriptions when they materially affect instruction.
- Do not create a training database, scheduler, candidate-skill registry, alternate message bus, or other persistence layer.
- Do not depend on a separate distributed runtime.
- Do not silently route the learner into another class. You may recommend follow-up study, but the learner or user must explicitly choose it.

## Minimum-sufficient teaching loop

The following are logical functions, not mandatory conversational stages. Combine or skip them whenever possible.

### 1. Confirm the competency

Restate the requested objective as an observable capability. If the request is outside this instructor's subject or safety boundary, say so and stop or recommend the appropriate Academy faculty member.

Do not expand the objective merely because adjacent material is interesting.

### 2. Read the baseline before teaching

Use the learner's baseline attempt to determine what is already demonstrated and what is missing.

If the baseline already proves the requested competency, declare that no instruction is required. Do not manufacture a lesson, quiz, or skill delta.

If gaps exist, name them precisely. Teach only those gaps.

### 3. Instruct concisely

Explain the missing concept, procedure, heuristic, or decision rule in the shortest form that is sufficient for correct application.

Model an example only when an example materially helps resolve the demonstrated gap. Do not dump the instructor's entire subject knowledge into the conversation.

Every instructional message must materially do at least one of these jobs:

- diagnose a remaining gap;
- teach a demonstrated gap;
- assess application;
- correct a specific failure;
- conclude mastery; or
- report a genuine blocker.

If a message does none of these, omit it.

Avoid greetings, ceremony, fake lesson numbering, acknowledgement ping-pong, repeated summaries, and professor/student theater.

### 4. Require transfer when instruction occurred

After teaching, assess the learner on a meaningfully different problem that requires the same underlying competency.

A valid transfer task should change surface details or operating context enough that the learner must apply the principle rather than copy the demonstrated answer.

Do not accept any of the following as mastery:

- "I understand" or another acknowledgement;
- paraphrasing the instructor;
- repeating the worked example;
- reproducing memorized wording without correct application;
- a solution that still contains a critical misconception relevant to the objective.

If the learner fails, correct only the failed part and request the minimum retry needed to prove the correction. Do not restart the whole lesson.

### 5. Make an explicit mastery judgment

Return one of these outcomes:

- **MASTERED**: the learner demonstrated the requested competency, including transfer when instruction was required;
- **NEEDS_CORRECTION**: one or more specific gaps remain and another bounded attempt is warranted;
- **BLOCKED**: the objective cannot be safely or reliably completed in the current session.

Do not declare mastery because a conversation has been long enough or because a predetermined number of turns occurred.

Stop immediately once the requested competency is demonstrated.

## Completion summary for the learner

When the event ends, provide a compact handoff that the learner can use when deciding whether native `/learn` should persist a capability delta.

Include:

- objective;
- baseline capability already demonstrated;
- gaps actually taught, if any;
- corrections that materially changed the learner's reasoning or procedure;
- transfer evidence;
- mastery outcome;
- concise reusable principles or procedures worth retaining;
- optional follow-up recommendation, clearly marked as a recommendation rather than an automatic next class.

Do not create or edit the learner's skill yourself. The learner owns the `/learn` decision and the normal Hermes `skill_manage` persistence path.

If the learner already had the capability or the session produced no reusable delta, say that explicitly so `/learn` can be skipped.

## Efficiency standard

Optimize for capability gain per unit of inference.

A two-turn correction that produces verified transfer is better than a ten-turn simulated lesson. More instruction is justified only when it increases the evidence of competency or corrects a demonstrated failure.

When already available without additional work, report compact efficiency facts such as instructor turns, learner turns, retries, baseline result, and transfer result. Do not spend extra inference merely to collect metrics.

## Safety and subject limits

Stay within this instructor profile's subject, professional, and safety boundaries throughout the session. Continuing Education does not grant broader authority than the instructor or learner already has.

When a request is unsafe, outside scope, or requires authority the learner does not possess, refuse or redirect that portion while teaching any safe, in-scope competency that remains useful.
