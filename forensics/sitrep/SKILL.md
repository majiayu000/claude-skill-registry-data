---
name: sitrep
description: Synthesise a status, standup, or situation-report from current work state. Trigger when a team member needs a concise summary of where things stand, what is blocked, and what is next.
---

# Sitrep

> **Situation reports are for the person who was not in the room.** Write for them.

A sitrep is not a diary of activity. It is a compressed, actionable picture of current state. Three questions: what is done, what is blocked, what is next. Anything that does not answer one of those three questions does not belong in the sitrep.

## When to use

- Daily standup synthesis from work logs, commits, or ticket state
- End-of-sprint summary for stakeholders
- Incident situation report during or after an active incident
- Handoff summary when switching context or handing work to another agent or person
- When a stakeholder asks "where are we?" and the honest answer is "it's complicated"

## Procedure

1. **Gather the current work state** — read from available sources:
   - Open and recently closed issues / tickets
   - Recent commits (last 24-48 hours for a standup; last sprint for a sprint summary)
   - Project status and roadmap documents (e.g. `docs/operating-model/PROJECT-OPERATING-PROFILE.md`, `docs/ROADMAP.md`, or equivalent per project structure)
   - Any blocking flags, risk register entries, or escalation notes

2. **Classify items** into three buckets:
   - **Done** — completed and verifiably closed (test passing, ticket closed, deployed)
   - **Blocked** — work that cannot progress without a specific unresolved dependency (name the blocker precisely)
   - **Next** — the highest-priority items that will be worked next (ordered by priority)

3. **Write the sitrep** — structure:
   ```
   ## Sitrep — <date> [<scope: sprint / incident / handoff>]

   **Done**
   - <item> — <one sentence on what was delivered and its evidence>

   **Blocked**
   - <item> — blocked on <specific dependency / owner / ETA if known>

   **Next**
   - <item> — <priority order, most important first>

   **Risks / flags** (optional — only if material)
   - <risk> — <impact if unresolved> — <owner>
   ```

4. **Apply the compression test** — for each line: if removing it changes nothing that the reader needs to act on, remove it.

5. **Name blockers precisely** — "blocked on backend" is not a blocker entry. "Blocked on API contract for `/v2/orders` — waiting on @owner, ETA unknown" is.

6. **Do not editorialise progress** — "made good progress" is noise. "Delivered X, which unblocks Y" is signal.

## Outputs

- A sitrep in the format above
- Optional: a one-paragraph executive summary for stakeholders who need even less

## Guardrails

- **No activity reporting.** "Worked on the auth module" is not a sitrep entry. "Auth module: JWT validation complete, token refresh failing under load — investigating" is.
- **Blocked means blocked.** If something is moving slowly but not actually blocked, it belongs in "Next" with a note, not "Blocked."
- **Done means done.** "95% done" is not done. If it is not verifiably complete, it is "Next."
- **Length is not quality.** A five-line sitrep that answers the three questions is better than a twenty-line one that does not.
