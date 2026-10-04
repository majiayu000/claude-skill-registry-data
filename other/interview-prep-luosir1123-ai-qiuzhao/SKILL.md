---
name: interview-prep
description: Use when a user wants interview preparation based on a target JD and resume, including likely technical and behavioral questions, evidence-backed answer outlines, project deep dives, gap repair, or mock-interview follow-ups.
---

# Interview Prep

Turn the JD and verified resume evidence into a role-specific interview pack.

## Inputs

Obtain the JD, resume/profile, interview stage, and available preparation time when known. Read the shared [candidate contract](../../shared/references/candidate-profile-schema.md), [claim ledger](../../shared/references/claim-ledger-schema.md), [role families](../../shared/references/role-families.md), and [output contract](../../shared/references/output-contracts.md).

## Workflow

1. Map JD requirements to candidate evidence, weak evidence, gaps, and unknowns.
2. Predict questions across motivation, project architecture, technical depth, engineering tradeoffs, metrics, failures, collaboration, and role-specific fundamentals.
3. Build answer outlines from facts. Use Situation, Task, Action, Result for behavioral evidence, but keep technical explanations architecture-first.
4. Generate adversarial follow-ups for every major resume metric and design claim.
5. For gaps, provide an honest bridge answer and a concrete study or experiment plan rather than a bluff.
6. Add questions the candidate should ask the interviewer.
7. Prioritize by probability and consequence using [interview-pack.md](references/interview-pack.md).
8. Prioritize `user_attested`, `inferred`, and high-scope claims for adversarial follow-up. Answers must preserve the ownership boundary and metric definition in the claim ledger.

## Integrity

Never invent implementation details, ownership, benchmark conditions, users, production scale, or business outcomes. Explicitly label suggested future work.
