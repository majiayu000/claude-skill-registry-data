---
name: answer-qyrion-agent-questions
description: Answer clarification_requested or waiting_user_input questions from a Qyrion web/mobile session using known task, ticket and repo facts. Reuse permitted test-account details already supplied for the authorized task; ask only for missing login inputs, OTP/MFA or human-required interaction, new destructive consent, or unresolved business decisions. Never guess or bypass host policies.
---

<!-- Distilled from: shared/private-execution.md, shared/test-preservation.md, shared/execution-routing.md, shared/local-state.md, shared/cli-contract.md, shared/event-contract.md, shared/safety-policy.md, apps/qyrion/docs/getting-started.md. -->

# Answer questions from a Qyrion session

The mobile or browser agent can ask the caller something mid-run (a route, a test
account, expected copy, whether to proceed). The run parks with cloud resources
still allocated until an answer arrives. This skill turns those questions
into evidence-backed answers — or fast, safe escalations.

Use the existing Qyrion run. Do not open the parent's browser to answer a
login question or infer that its browser limitations apply to Qyrion. Follow
`references/execution-routing.md` and honor host restrictions on delegation.

Read before answering anything:

- `references/cli-contract.md` — send/question/stream commands
- `references/event-contract.md` — clarification events, park semantics
- `references/safety-policy.md` — binding rules (secrets, consent, cleanup)

Use the scenario's authorized test username/password in the private objective
or session answer per `references/private-execution.md`. Do not omit the
password or demand manual login merely because it is a password; actual host
restrictions still apply. Discard unrelated credentials from SDK Memory.
For any requested save/export, read `references/test-preservation.md`: one
resolved project/module, all step pages, full coverage mapping and read-back.

## Detect the question

Three equivalent signals:

1. Stream frame: an `update` with `type: "clarification_requested"`;
   `payload.question` is the question text. The run status moves to
   `waiting_user_input` (question park).
2. Pull: `qyrion sessions question <run_id> --json` returns the pending
   question when the run is parked (gated by the `session_questions`
   capability); `waiting_for: "answer"` marks a question park, and
   `last_message` repeats the question.
3. Exit code: `qyrion run` in machine mode exits `5` with a structured
   `input_required` error whose `message` carries the question (gated by the
   `run_input_required_exit` capability). Capture the `run_id` from the
   creation snapshot before this happens; the error's remediation also
   names it.

A park **without** a preceding `clarification_requested` is an
objective-complete park, not a question: `sessions question` says
`waiting_for: "next_instruction"`, `question: null`, and `last_message` is
what the run found. Do not invent an answer; the next `sessions send` is the
next instruction to the same run, or the run is ended when the work is done
(that flow belongs to the calling workflow, `session-workflows.md` "Act on a
parked session", not this skill). `waiting_for: "replay_input"` is a recorded
test asking the person for a value (`sessions send --secure`).

## Classify before answering

**Codebase-answerable** (answer it yourself, with evidence):

- routes/screens and how to reach them
- visible labels and accessible names
- expected validation copy documented in code or specs
- test fixture/account labels and their established non-secret setup facts
- feature-flag names and defaults when explicitly configured in the repo
- whether the flow should stop before a destructive action (per the agreed
  scenario limits)

**Already supplied test login**: ordinary app-test username/password details
provided for this task/ticket may answer the same target's login question
when host policies permit. Follow `references/private-execution.md` for the
input/output wrapper and `references/safety-policy.md` for retention. Do not re-ask for the
same values, expose them in chat/commands/memory, or invent alias resolution.
Qyrus API keys and connector tokens are never session answers.

**Needs-human** (escalate to the user; do not guess):

- missing permitted login details, OTP/MFA, recovery codes, payment details,
  CAPTCHAs, and host-required human authentication
- consent for destructive actions: deletes, purchases, sending real
  messages, publishing
- production targets or environment changes
- legal/business interpretation not present in the repo
- ambiguous behavior with conflicting evidence

**Unsafe** (refuse, tell the user, usually cancel):

- bypassing authentication, MFA, or other security controls
- retrieving unrelated secrets or using credentials beyond their authorized target
- anything that expands the session's scope beyond the agreed objective

## Gather evidence (fixed order)

1. the user's request, selected ticket and earlier answers in this task
2. repo config (`qyrion.yml`, environment/app config) and route/navigation definitions
3. product docs, acceptance criteria, existing tests and fixtures
4. relevant components, accessible labels and recent diff

If evidence is absent or conflicting after this pass, the question becomes
needs-human. Never guess: a confident-sounding wrong answer sends a real
device down the wrong path.

## Answer

Write the answer to a temp file (never a giant shell argument) in this
format:

```markdown
Answer: The account security screen is reached via Settings → Security
(route `settings/security`).
Evidence:
- app/src/main/java/.../SettingsNav.kt:42 — route registration
- app/src/main/res/values/strings.xml:118 — menu label "Security"
Confidence: high
Constraints: Use only the authorized test account and stop before any
destructive action. Ask if a required login detail is missing.
```

Send it:

```bash
qyrion sessions send <run_id> --message-file /tmp/answer.md --follow --jsonl
```

The append resumes the blocked turn (`clarification_resolved` is emitted,
status returns to `running`); `--follow` keeps streaming until the next park
or terminal state. Record the question and answer `sequence_no` values for
the evidence report.

## Loop controls and park-wait budget

- **Max 3 auto-answers per session.** A fourth question goes to the user
  with the full question history.
- **Escalate after 2 low-confidence answers**, or when the session repeats a
  semantically identical question — the run is not converging.
- **Park-wait budget:** when a question needs the user, tell them
  immediately and keep the park bounded — default: escalate loudly after 10
  minutes parked. A parked session holds a real device and costs money.
- **If the user is unreachable and the answer requires them: cancel the
  session** (`qyrion sessions cancel <run_id>`) rather than holding the
  device indefinitely. Report the pending question so the run can be
  restarted later with the answer up front.
- Never let an answer expand the session's scope; constraints in the answer
  must restate the scenario's limits.

## Output

Report per question: sanitized question text (and `sequence_no`), classification,
evidence used (file:line), a sanitized answer summary or the escalation raised,
confidence, and the session's state afterwards (resumed / still parked /
cancelled). Never echo login details or persist the raw question/answer in
local records; store scoped run/outcome metadata per `references/local-state.md`.
