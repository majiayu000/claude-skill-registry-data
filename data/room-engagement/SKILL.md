---
name: room-engagement
description: Read per-viewer engagement from a ReportRoom data room — who opened which documents, how long they spent — and turn it into next actions for the deal. Use when the user says "did they look at the data room?", "who opened the financials?", "what did the investor read?", "any activity in the room?". Requires a ReportRoom Business plan. For building a room use data-room; for inviting/revoking use room-access.
---

# Room Engagement

The read side of a data room: `get_room_analytics` returns per-viewer, per-document opens, event counts, and dwell time. The job is not to dump numbers — it is to translate them into what the user should do next in the deal.

Follow the shared rules in the root `SKILL.md`. This skill is read-only: it never changes access (that's `room-access`).

## Steps

1. **Pull the data.** `get_room_analytics` with `room_id`. If the result is empty/unconfigured, say so plainly — no activity data is different from no activity.
2. **Join with the roster.** `list_room_viewers` maps viewer ids to emails and NDA state. Note the identity limits: **email/allowlist viewers are identified; passcode/public viewers appear as anonymous session ids** — for a passcode room you can say "someone spent 9 minutes on the financials", not who.
3. **Report by viewer, then by document.** The useful shape: "a.chen opened 4 of 6 documents; 9m on financials, 2m on the deck; never opened legal." Dwell is time-on-page from a browser beacon — treat it as an engagement signal, not a verified read-through.
4. **Translate into next actions.** Patterns worth naming:
   - **Deep on financials/pricing, silent on reply** → they're evaluating; a targeted follow-up on the numbers beats a generic nudge.
   - **Opened once, bounced fast** → the room order or the first document may not land; suggest reordering or a shorter overview doc (via `data-room`).
   - **Never entered** — check the roster first: unaccepted invite (link may have expired after 48h → suggest re-granting via `room-access`) is a delivery problem, not disinterest.
   - **NDA not accepted** → they hit the gate and stopped; worth a personal note, not a re-send.
5. **Offer the loop.** Recurring check-ins ("I'll check the room again in two days") are the value; offer, don't spam.

## Hard rules

- **Engagement data is for the user, never for the viewer.** Don't draft messages that reveal surveillance detail ("I saw you spent 9 minutes on pricing") — translate the signal into a natural follow-up instead.
- Don't over-interpret: dwell ≠ comprehension, an open ≠ a read, and one anonymous session ≠ one person. State confidence honestly.
- Never fabricate activity. Empty analytics get reported as empty.
