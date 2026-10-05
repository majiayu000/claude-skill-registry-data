---
name: feature-development
description: Use when implementing a new feature or extending existing functionality. Covers understanding the request, proposing a short plan, getting approval, implementing with tests, and recording the work.
---

# Feature Development

Goal: build what was actually asked for, keep the user in control, leave a
record.

## Steps

1. **Understand the request.**
   Read the parts of the codebase the feature touches. If the requirement is
   ambiguous, ask ONE short question with 2-3 concrete options — do not start
   coding on a guess.

2. **Classify the risk (L0-L3).**
   Check the automatic escalation triggers in the constitution. State the
   level in your Plan message.

3. **Propose.**
   Send the Problem / Plan / Risk / Question message. Plain language,
   2-3 sentences of plan. For L2/L3: wait for approval (and consult the
   advisor first, if available). For L1: proceed unless the user objects.

4. **Implement in the smallest coherent slice.**
   - Match the existing code style and structure.
   - Write tests alongside the code, not as an afterthought. Test the
     behavior the user asked for, including the failure paths — not just the
     happy path.
   - No speculative abstractions. Build for the requirement you have.

5. **Verify.**
   Run the `verify-work` skill before claiming anything is done.

6. **Record.**
   - Journal entry: `docs/agent-journal/YYYY-MM-DD-feature-<slug>.md`
     (format: What was asked / Plan / What was done / How verified).
   - If the feature changed an API surface other people integrate with,
     write an integration brief (see `integration-brief` skill).

7. **Close the loop.**
   Report Done / Verified / Recorded, and ask the user — briefly — if they
   want anything changed. The user's answer, not your report, ends the task.

## Do not

- Do not dump implementation details into chat. They belong in the journal.
- Do not silently change existing behavior "while you're there". Separate
  concern, separate proposal.
- Do not add config options, hooks, or extension points nobody asked for.
