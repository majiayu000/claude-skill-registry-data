---
name: feedback-checkpoint
description: >-
  Status checkpoint to unstick a run: detect loops and stuck states, report
  Done / Next / Blocking, and recover one step at a time. Use when the user
  asks for a status update, says "checkpoint", or when you suspect you are
  looping or stuck.
---

# Feedback Checkpoint

Run this to take stock and unstick a session.

1. **Check for a loop.**
   Have you done 3+ similar actions in a row, repeated the same failing step, or kept re-reading/re-editing the same area without progress? If yes, treat as loop.

2. **Check for stuck.**
   Are you blocked (error, missing type, unclear requirement) or have you spent more than 2–3 turns on the same task without finishing? If yes, treat as possibly stuck.

3. **Respond in one of these ways:**

   **If in a loop:**
   - Say you may be in a loop, what you were trying to do, and the **single next step** you will take.
   - Do only that one step, then stop and wait for user feedback.
   - Keep the task list up to date.

   **If stuck:**
   - Output a 3-bullet status: **Done**, **Next**, **Blocking**.
   - Stop and wait for user direction (e.g. "Proceed", "Simplify scope", or clarification). Do not start another round of tool calls until the user responds.

   **If neither:**
   - Give a short 3-bullet status anyway (Done / Next / Blocking) so there is a clear checkpoint.

4. **Rule:** one task at a time when recovering. Complete one step, then rely on the next turn or user confirmation before continuing.
