---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree one decision at a time. Use when a task is under-specified, a design needs stress-testing, or the user asks to be grilled.
---

# grill-me

Use this as the optional discovery / pre-planning phase inside the atelier workflow.

Interview the user relentlessly about every material aspect of the plan, design, or requested change until the decision tree is resolved enough for `plan-task` to write a strong execution contract.

## Read first

- `../references/task-packet-contract.md`
- `../references/persistent-artifacts-contract.md`
- `../references/compatibility-policy.md`
- `../references/ownership-and-reuse-policy.md`
- `../references/final-state-authoring-policy.md`
- relevant tracked `AGENTS.md` chain
- applicable `AGENTS.override.md` only if local execution constraints matter

## Role

This skill owns clarification, not execution.

Keep the main interview context lean and decision-oriented. If clarification requires repo/codebase exploration, spawn or reuse a sidecar teammate named `researcher` instead of doing the digging yourself. Use model `openai-codex/gpt-5.4` by default and choose `thinking` to match task complexity.

It is for:

- resolving ambiguity before planning
- surfacing hidden constraints
- narrowing decision branches
- testing whether the proposed direction actually makes sense against the codebase
- producing a crisp enough brief that `plan-task` can write a self-sufficient `PLAN.md`

It is not for:

- writing implementation code
- doing final plan review
- inventing speculative scope the user did not ask for
- preserving compatibility by default

## Interview workflow

1. Understand the current ask.
   - Restate the current design/problem in your own head.
   - Identify what is still ambiguous, missing, or risky.
2. Explore before asking when possible.
   - If the answer is in code, architecture, existing artifacts, tracked `AGENTS.md`, or nearby boundaries, investigate first.
   - Route non-trivial exploration through a sidecar teammate named `researcher`; do not load the main interview context with raw repo details.
   - `researcher` defaults to model `openai-codex/gpt-5.4`; choose `thinking` by complexity: minimal/low for quick lookups, medium for bounded multi-file tracing, high/xhigh for ambiguous or cross-cutting investigation.
   - Pull back only the distilled findings needed for the next interview question or brief update.
   - Use questioning only for information that is genuinely missing, preference-driven, or decision-driven.
3. Ask exactly one question at a time.
   - Never batch multiple unrelated questions into one message.
   - Resolve the current branch before moving to the next one.
4. Use multiple-choice format by default.
   - Offer 2–5 concrete answer options.
   - Include `Other` when the space is open-ended.
   - Make the options mutually exclusive when possible.
5. Mark a recommended option only when confidence is high.
   - Format clearly, e.g. `Recommended: B`.
   - Include one short explanation of why it is recommended.
   - If confidence is not high, do not force a recommendation.
6. Walk the decision tree top-down.
   - Resolve goals before mechanics.
   - Resolve boundaries before implementation details.
   - Resolve ownership/reuse before new abstractions.
   - Resolve compatibility only if a real external boundary is involved.
7. Stop once the plan can be written cleanly.
   - When the major branches are resolved, summarize the clarified brief or update `BRIEF.md` if a task packet is already in play.
   - Write the brief as the current clarified model, not as a chronology of how the conversation wandered there.

## Question format

Default shape:

- short context sentence
- one explicit question
- answer options labeled `A`, `B`, `C`, ...
- optional `Recommended: X`
- short `Why:` only for the recommendation

Example shape:

```text
Question: What should own the new retry policy?
A. Keep it in the existing session owner
B. Introduce a dedicated retry coordinator
C. Split between ingress and reducer
D. Other

Recommended: A
Why: one owner, lower coordination cost, and likely smallest tidy-first path.
```

## Conversation mode

Track a persistent conversation channel mode while this skill is active.

Modes:

- `local` = ask and continue in the current chat thread
- `remote` = ask via `send_notification` and treat notification replies as normal authoritative human input

Defaults and switching:

- default to `local` unless the human explicitly asks for `remote`
- the human may switch modes at any time in natural language
- interpret requests like `switch to remote mode`, `switch to local mode`, `I am back lets proceed locally`, `I need to go, switch to remote`, and close variants as immediate mode switches
- do not ask for confirmation before switching
- once switched, stay in that mode until the human explicitly switches again
- a reply arriving through the non-primary channel does not by itself switch modes; it is still valid human input, but the active mode remains unchanged
- treat a mode-switch request as control input, not as an answer to the current product/design question; switch first, then continue the same decision branch in the new mode

When in `remote` mode:

- keep the multiple-choice format the same
- ask the active question via `send_notification`
- if you have high confidence, include `Recommended: X` on its own line exactly in that shape
- explicit text replies from the human override any inferred meaning from reactions
- if a reply arrives as:
  - `reply to notification <messageId>`
  - `reaction: 👍`
  - or `reaction: ❤️`
  then treat that as confirmation of the recommended option for that notification
- only infer that confirmation when the question for that notification included a clear `Recommended: X`
- if no recommendation was present, do not infer a choice from reaction alone; ask the next clarifying question in text if needed

When in `local` mode:

- continue in the chat normally
- stop using `send_notification` for new questions unless the human explicitly switches back to `remote`

## What to optimize for

- one question at a time
- lean interviewer context
- concrete options over vague open prompts
- recommendations only when confidence is genuinely high
- tidy-first reuse over parallel same-purpose entities
- explicit ownership and invariants
- no backward compatibility by default
- minimal future ambiguity for `plan-task`
- early detection that the work is too large or too cross-cutting for one healthy task packet

## Artifact responsibility

If a task packet already exists, this skill may:

- create or update `BRIEF.md`
- update `INDEX.md` notes

It should not:

- write `PLAN.md`
- write review artifacts
- write tracked `AGENTS.md`
- write `AGENTS.override.md`

## Do not

- do non-trivial codebase exploration in the main interview context
- ask broad multi-part questionnaires
- ask about things the codebase or `researcher` can answer
- recommend compatibility for internal-only changes
- recommend a new same-purpose entity before considering tidy-first reuse
- continue asking once the decision tree is already resolved enough for planning

## Initiative-mode trigger
If discovery starts producing a giant shared-context blob, many child-worthy workstreams, or cross-repo coordination needs:
- stop aiming straight at one giant `PLAN.md`
- steer toward `frame-initiative` first
- use the interview to clarify initiative scope, shared invariants, terminology, and likely split boundaries

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
