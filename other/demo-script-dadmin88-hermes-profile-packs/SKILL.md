---
name: demo-script
description: Write a product demo script that proves one or more capabilities through a realistic user goal, exact setup, visible actions, narration, proof points, transitions, and recovery from likely live-demo failure.
---
# Demo Script

Use when a live or recorded demonstration needs a reliable narrative and operational sequence.

## Procedure
1. Define the audience, user goal, capabilities to prove, time limit, environment, and what the audience should believe or do afterward.
2. Choose a realistic starting state and remove setup steps that do not teach or prove anything while preserving limitations the audience needs to understand.
3. Script visible actions in the exact order they will be performed and pair narration only with context or meaning the screen cannot show itself.
4. Identify proof moments where the result should be allowed to sit on screen long enough for the audience to see it.
5. Prepare data, accounts, files, network, permissions, device state, and dependencies and record the exact build or version used.
6. Add transitions between capabilities so the demo remains one user journey rather than a sequence of disconnected features.
7. Define fallback or recovery for slow network, failed dependency, stale state, or accidental navigation when a live demo cannot simply be restarted.
8. Rehearse at real speed, trim unnecessary narration, and validate every claimed result immediately before the presentation or recording.

## Decision rules
- Demonstrate outcomes rather than describing features while the screen is idle.
- The demo environment is part of the deliverable.
- Do not fake a result that the product cannot currently produce.
- A fallback should preserve truth, not conceal failure.

## Quality gate
The script is ready when the demo can be rehearsed end to end in the allotted time, setup is reproducible, actions visibly prove the claims, narration adds rather than duplicates information, and likely failure states have honest recovery paths.