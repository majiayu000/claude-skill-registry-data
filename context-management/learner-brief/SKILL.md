---
name: learner-brief
description: Create a compact teaching brief with learning goal, approximate level, relevant prior knowledge, constraints, and preferred depth or mode.
---
# Learner Brief

Capture only what affects instruction: what the learner wants to be able to understand or do, their approximate starting point, relevant prior knowledge, time or tool constraints, and whether they want explanation, practice, review, or direct help.

Do not demand information that can be inferred safely from the conversation.

## Profile Learner Context Minimization

When the learner is a Hermes profile (e.g. `agency-backend-engineer`), the brief must contain only what the receiving faculty member needs:

**Include:**
- Learner profile name (identity)
- Learner role (one-line description of what the profile does)
- Requested objective (one clear learning goal)
- Relevant skill names or descriptions when they directly affect instruction

**Never include:**
- Full profile state or configuration
- Memory contents or conversation history
- Secrets, credentials, or API keys
- Internal tool schemas or implementation details
- Unrelated skills or capabilities

Use `routing.py` → `minimize_learner_context()` to build the minimized context object. The function accepts learner profile name, role, objective, and an optional list of relevant skill names, and returns a `LearnerContext` containing only those four fields.
