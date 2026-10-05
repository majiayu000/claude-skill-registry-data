---
name: flow-selector
description: Presents 2+ candidate flows from flow-detector and asks the user to pick one. Issues exactly one AskUserQuestion. Never activates when flow-detector returns a single candidate, and never asks cluster-by-cluster questions.
---

# Flow Selector

Present candidate flows produced by `flow-detector` and let the user pick one. Single decision point — no follow-up questions.

## Activation Triggers

This skill activates when:
- `flow-detector` has emitted **two or more** candidate flows.
- The caller (`/clarify` command or `@clarifier` agent) hands off the candidate list.

This skill does **not** activate when:
- `flow-detector` returned exactly one candidate. The caller proceeds straight to `execution-context-builder`. If this skill is invoked with a single-candidate list, no-op and log "single candidate; selector skipped".

## Hard Rules

1. Issue **exactly one** `AskUserQuestion` call. Never two. Never a follow-up.
2. The question's options are the candidate **titles**. The "Other" escape hatch is added automatically by `AskUserQuestion`.
3. Do not ask sub-questions about entity, trigger, channel, recipient, or failure handling. Those are encoded in each candidate's `full_context`.
4. Do not ask "are you sure?" after the user picks.
5. Pass the chosen candidate's `full_context` directly to `execution-context-builder`.

## Process

### 1. Print the framing

Output a brief framing block before the question:

```
This task has multiple possible flows:

1. <candidate[0].title>
   <candidate[0].one_line_diff>

2. <candidate[1].title>
   <candidate[1].one_line_diff>

…

Which flow would you like to proceed with?
```

The framing prints to the chat so the user can see all candidates at once. The `AskUserQuestion` tool then renders them as selectable options.

### 2. Issue the question

Call `AskUserQuestion` with one question:

```yaml
question: "Which flow describes the intended scope?"
header: "Flow"
multiSelect: false
options:
  - label: <candidate[0].title (truncate to ≤ 5 words if needed)>
    description: <candidate[0].one_line_diff>
  - label: <candidate[1].title>
    description: <candidate[1].one_line_diff>
  # … one entry per candidate, max 4 total
```

Notes:
- `AskUserQuestion` allows 2–4 options. `flow-detector` caps at 4 candidates, so this fits without truncation.
- The "Other" escape hatch is added automatically. Do **not** include an explicit "Other" option.

### 3. Handle the answer

- **User picked a numbered option** → look up the corresponding candidate and pass its `full_context` to `execution-context-builder`. Done.
- **User picked "Other"** → prompt once with a free-text request: "Describe the intended flow in your own words." Treat the answer as a synthesized candidate (`id: user-supplied`, `title: <user text>`, `full_context: <best-effort inference from the user's text + repo>`). Pass it to `execution-context-builder`. Do not loop back.

## Examples

### Two candidates, user picks #1

User runs `/clarify "Send message on sign-in"`.

Print:
```
This task has multiple possible flows:

1. User sign-in flow — in-app message to the signing-in user
   Recipient is the user who signed in; channel is in-app

2. Tenant audit flow — email to the tenant owner when a member signs in
   Recipient is the tenant owner; channel is email

Which flow would you like to proceed with?
```

Then issue one `AskUserQuestion`. User picks option 1 → hand `candidate[0].full_context` to `execution-context-builder` → done.

### User picks "Other"

User picks Other and types: "Slack message to #engineering when an admin signs in".

Synthesize a candidate:
- `entity: User` (admin role)
- `trigger: { event: "post-auth", timing: "after", preconditions: ["role=admin"] }`
- `action: { verb: "post", channel: "slack", recipient: "#engineering" }`
- `flow: { services: ["slack-webhook"], mode: "async", transport: "https" }`
- `failure_handling: { strategy: "retry", details: "3 attempts then log" }`

Hand to `execution-context-builder`. Do not ask any follow-ups — even if some fields had to be guessed. The artifact is the deliverable; the developer can edit it directly.

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Ask multiple questions in sequence | One `AskUserQuestion`, period |
| Ask "and which channel?" after the user picked a flow | Each candidate already encoded the channel |
| Add a manual "Other" option | `AskUserQuestion` adds it automatically |
| Ask "are you sure?" | Trust the user's pick; write the artifact |
| Drop the framing block and go straight to the question UI | The framing gives context the question chip can't fit |

## Success Criteria

- [ ] Exactly one `AskUserQuestion` call per invocation.
- [ ] The framing block is printed before the question.
- [ ] Each option's label and description map to one candidate's title and `one_line_diff`.
- [ ] On "Other", a single free-text follow-up is taken; no further questions.
- [ ] The chosen `full_context` is passed unchanged to `execution-context-builder`.
