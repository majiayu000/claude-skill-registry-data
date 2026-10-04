---
name: room-access
description: Manage who can enter an existing ReportRoom data room — grant viewers by email (single-use invite links), revoke access instantly, rotate or clear the passcode, switch access mode, update the NDA text or expiry. Use when the user says "invite X to the data room", "add the buyer's counsel", "revoke their access", "rotate the passcode", "change the NDA", "extend the room". Requires a ReportRoom Business plan. For building a new room use data-room; for who-read-what use room-engagement.
---

# Room Access

Viewer and gate management for a live data room. Every operation here changes who can see confidential material — confirm each change back to the user before applying it, per the shared rules in the root `SKILL.md`.

## Operations

**Grant a viewer** — `grant_room_access` with `room_id` + `email`.
- Returns a **single-use invite link once**. ReportRoom does not email it. Hand the link to the user to deliver; never send it to the recipient yourself unless explicitly asked.
- The link is unrecoverable after display (only a hash is stored). Lost link → re-grant the same email to reissue a fresh one.
- Invite links expire after 48 hours if unused; re-grant to refresh.

**Revoke a viewer** — `revoke_room_access` with `room_id` + `viewer_id` (find the id via `list_room_viewers`).
- Takes effect **immediately**: live sessions end, not just future entries. Confirm with the user first — a revoked investor notices.

**See the roster** — `list_room_viewers`: each viewer's email, verification state, NDA acceptance, and revocation state. Never exposes invite tokens.

**Change the gate** — `set_room_access` with `room_id`:
- `access_mode` — switch between `public` / `email` / `passcode` / `allowlist`. Mode changes invalidate live viewer sessions (viewers re-enter through the new gate).
- `passcode` — a string sets/rotates it, `null` clears it, omitting leaves it unchanged. Rotating ends sessions opened under the old code.
- `settings.nda_text` — editing re-prompts **all** viewers (including those who accepted the old text) on next entry; tell the user this.
- `settings.expires_at` — set, extend, or clear the hard deadline; past it the room serves 410 to everyone.
- `settings.allow_download` / `settings.watermark` — storable but **not enforced yet**; if the user asks for them, say so plainly instead of pretending.

## Judgment rules

- **Match the change to the intent.** "Remove them" usually means revoke one viewer, not rotate the passcode for everyone; "the code leaked" means rotate the passcode *and* review the roster. Reflect the plan back before acting.
- **Allowlist + grant go together.** In `allowlist` mode, a granted email is the only way in — granting is not optional onboarding, it *is* the gate.
- **Report state after every change** — re-run `list_room_viewers` and summarize who currently has access, so the user always knows the live blast radius.
