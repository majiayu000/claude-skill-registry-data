---
name: challenge-decision
description: Pressure-test a decision before it is made (red-team) or run the learning loop after one is reversed (postmortem), arguing from the vault's own history. Use when the user says "challenge this", "red team", "stress test", "I'm thinking of X", "before I decide", "postmortem", "what went wrong", or when a decision note flips to status reversed.
version: 4.2.1
author: fbureau
license: MIT
metadata:
  hermes:
    tags: [second-brain, decisions, critique]
    related_skills: [recall, knowledge-stub]
    requires_toolsets: [second_brain]
---

# Challenge decision (Hermes edition)

Two modes. Pick by whether the decision has already been made.

## Mode A — red-team (before)

1. `sb_decision_context(subject=<the decision in one or two sentences>)`.
2. Argue from what comes back, not from principles. Every objection cites a note path. If
   `similar_decisions` is empty, say the red-team is weak for lack of prior art — do not compensate
   by inventing generic risks.
3. Give at most five objections, strongest first. For each: the claim it attacks, the evidence,
   and what would have to be true for the objection to be wrong.
4. Always cover these three, because they are the ones people skip:
   - **What was reversed before** — from `reversed_precedents`, and what is different this time.
   - **Who is not in the room** — from `stakeholders`, whoever the plan affects but never consulted.
   - **How you would know you were wrong** — a falsifiable reversal condition with a date to check it.
5. End with a verdict in one line: proceed, proceed with changes (name them), or hold and find out X first.
6. Write nothing. If the user commits afterwards, offer to record it with
   `sb_create_note(type="decision", ...)` including the reversal conditions from step 4.

## Mode B — postmortem (after a reversal)

1. `sb_decision_postmortem(path="05-decisions/...")`.
2. Name the lesson in one sentence, in the user's own vocabulary. "We underestimated the migration"
   is a lesson; "communication could be improved" is not.
3. For each entry in `notes_resting_on_the_same_hypothesis`, `sb_read` it and propose — do not apply —
   a concrete update. Show the list, ask for a go, then apply the ones the user approves.
4. Record the reversal on the decision note with
   `sb_append_timeline(path, "Reversed — <lesson>", [...])`. 05-decisions/ is append-only:
   never edit the rationale, never rewrite history.
5. File the lesson: `sb_create_note(type="knowledge", fields={domain, confidence}, ...)` linking back
   to the decision, then `sb_curate(path)`.
6. `sb_commit("postmortem: <decision>")`. Report what was learned and which notes were updated.
