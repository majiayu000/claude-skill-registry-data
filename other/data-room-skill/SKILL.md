---
name: data-room-skill
description: Shared rules for the data-room-skill bundle (data-room, room-access, room-engagement). Loaded by the individual skills for the common ReportRoom gate, limits, and safety rules. Not invoked directly — pick the specific skill for the job.
---

# Data Room Skills — shared rules

All three skills operate ReportRoom data rooms through the ReportRoom MCP server. This file holds what they share; each skill's SKILL.md holds only what differs.

## The gate (check before any room operation)

Call `account_status`. Data-room tools require **both**:

- the **Business plan** (not Free, Pro, or Team), and
- the caller to be the org **owner or an admin**.

If either is missing, say so plainly and offer the alternative (publishing documents normally, or a tracked proposal) rather than retrying. Never imply a room exists or a change was made when the entitlement check failed.

Limits: **10 live rooms per org, 200 viewers per room.** Deleting a room is an archive (its URL stops serving); there is no hard delete.

## Facts that hold everywhere (verified against the serving code)

- Access modes: `public` | `email` (magic link, default) | `passcode` | `allowlist`. Enforced at serve time.
- `nda_text` (accept-before-entry) and `expires_at` (room returns 410 after) are **enforced**.
- `watermark` and `allow_download` are stored but **not enforced yet** (Phase 2) — never tell the user a room is watermarked or download-locked.
- Access is **room-level**: every granted viewer sees every document in the room. Different audiences → different rooms.
- While a document is in a live room, its standalone URL is gated too — the room cannot be bypassed by opening the doc directly.
- Rooms are served `noindex`; regular published documents are public, indexable pages.
- Invite links from `grant_room_access` are shown **once**, never emailed by ReportRoom, and unrecoverable (re-grant to reissue).
- `get_room_analytics` is per-viewer, per-document (opens, events, dwell). Email/allowlist viewers are identified; passcode/public viewers appear as anonymous session ids.

## Safety rules (all three skills)

- Never fabricate or estimate diligence material — metrics, financials, cap-table figures go in exactly as the user supplies them; ask for missing numbers.
- Scan every document for secrets, keys, unredacted personal data, and third-party confidential material before it goes into a room.
- Never send an invite link to a recipient yourself unless the user explicitly asks; hand it to the user.
- Confirm access-mode and viewer changes back to the user before applying them — a wrong grant leaks a confidential room.

## Which skill for which job

| The user wants | Use |
|---|---|
| Build a new room (fundraise, M&A, board pack) | `data-room` |
| Invite, revoke, rotate a passcode, change NDA/expiry | `room-access` |
| Know who opened what, and what to do about it | `room-engagement` |
