---
name: verify-outcome
description: Verify the user-facing outcome, and verify that your metric can even see the defect class you care about.
---

# Verify the outcome

A passing test or a point-wise statistic can be blind to the failure that matters. Point stats miss structure; presence gates miss absences.

**Why:** "the check passed" is worthless if the check cannot perceive the bug. You confirm the wrong thing and call it done.

**How to apply:** confirm the actual end-to-end result a user would experience. Separately, ask what defect class your metric is structurally unable to detect, then add a check that can see it.
