---
name: decision-record-writer
description: Use when Codex should capture a durable decision record from a discussion, plan, code/design change, workflow choice, research direction, tool selection, policy, or project tradeoff. Use for ADRs, decision logs, "record this decision", "why did we choose this?", "write a decision note", post-plan decision capture, and preserving rationale, alternatives, consequences, review triggers, and verification evidence.
---

# Decision Record Writer

Turn a decision into a short record future work can trust. This skill records decisions; it does not reopen the full debate unless required information is missing.

## Workflow

1. Identify the decision.
   - Name the concrete choice that was made or needs to be recorded.
   - Separate the decision from implementation steps, preferences, and background discussion.

2. Gather evidence from current context.
   - Use existing discussion, local docs, plans, diffs, tests, source links, or user statements.
   - Do not invent rationale. Mark unknown rationale as "not recorded" or ask if it changes the record.

3. Capture alternatives.
   - Include the chosen option.
   - Include viable rejected options when they were considered or are likely to recur.
   - Keep rejection reasons short and falsifiable.

4. Record consequences.
   - Benefits expected.
   - Costs, risks, maintenance burden, migration needs, compatibility constraints, or user-facing effects.
   - Verification evidence already available and evidence still needed.

5. Choose durability.
   - If the user names a target file, write or update it.
   - If the repo has a decision-log convention, follow it.
   - If no durable artifact is requested, provide a copyable Markdown decision note in the response.
   - Avoid storing secrets, credentials, or sensitive personal details.

6. Route when needed.
   - Use `$codex-consensus-plan` before this skill if the decision is not actually settled.
   - Use `$assumption-auditor` when the record rests on unverified premises.
   - Use `$scope-negotiator` when the decision is mostly about current-turn scope.

## Output Shape

Use this Markdown template by default:

```markdown
# Decision: <short title>

- Status: proposed | accepted | superseded
- Date: YYYY-MM-DD
- Context:
- Decision:
- Rationale:
- Alternatives Considered:
- Consequences:
- Verification / Evidence:
- Review Trigger:
```

For lightweight chat-only decisions, compress to:

- Decision
- Why
- Alternatives rejected
- Consequences
- Revisit when

## Stop Conditions

- Do not continue debating a settled decision unless the user asks.
- Do not mark a decision `accepted` unless the user clearly accepted it or the surrounding work already committed to it.
- Do not create or update files unless the user requested a durable artifact or the repo convention clearly calls for one.
