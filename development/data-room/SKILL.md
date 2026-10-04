---
name: data-room
description: Build a fundraising or M&A data room — publish the documents, assemble them into one access-controlled room, and set the gate (email/passcode/allowlist, NDA, expiry). Use when the user says "data room", "set up a diligence room", "investor data room", "send this to investors", "share with the buyer". Requires a ReportRoom Business plan. For inviting/revoking viewers afterwards use room-access; for who-read-what use room-engagement.
---

# Data Room (builder)

A data room is a named, access-controlled bundle of documents at one URL, shared with **identified** external viewers — investors, buyers, clients. This skill covers assembly: contents, order, and the gate. Viewer management and engagement reading are separate skills (`room-access`, `room-engagement`).

Follow the shared rules in the root `SKILL.md` (Business-plan gate, limits, safety). Check the gate first — `account_status` — before promising anything.

## Steps

1. **Agree the contents first.** List what goes in the room before publishing anything. For a raise, the standard order: company overview → metrics/KPIs → financials → cap table → customer proof → legal/incorporation. For M&A: the same with a heavier legal/contracts section and a diligence index up front. Ask what is missing rather than inventing sections.
2. **Publish each document.** Room documents are ordinary published documents: `get_design_system` → author self-contained HTML → `lint_document` → `publish`. Collect each returned `document_id`. Documents stay first-class; being in a room never changes or unpublishes their standalone URL (which is gated by the room while the room is live).
3. **Choose the access mode with the user** (read it back before creating):

| Mode | Who gets in | Use when |
|---|---|---|
| `email` (default) | Anyone who verifies an email — magic link | Broad investor outreach where identity matters more than a wall |
| `passcode` | Anyone with the shared passcode | A banker-run process where one code circulates |
| `allowlist` | Only emails granted in advance | Named diligence — the tightest option |
| `public` | Anyone with the link (recorded anonymously) | Rarely right for a data room; say so if asked |

4. **Create the room.** `create_data_room` with `name`, optional `slug`, the access mode, `passcode` if that mode, and `settings`: `nda_text` (enforced click-through) and `expires_at` (enforced). `allow_download`/`watermark` may be set but are **not enforced yet** — don't rely on or advertise them.
5. **Add documents in diligence order.** `add_documents_to_room` with `document_ids` in display order. This **replaces the whole set** — always send the complete ordered list, never a delta.
6. **Approval gate.** Before anyone is invited, show the user: room name and URL (`<handle>.reportroom.io/room/<slug>`), the ordered document list, the access mode, and every deal control set. Then hand over to `room-access` for invitations.

## Hard rules (beyond the shared ones)

- Room-level access only: if two investors should see different things, that is **two rooms** — never imply per-document permissions exist.
- The fundraising checklist above is a default, not a mandate — the user's deal structure wins.
