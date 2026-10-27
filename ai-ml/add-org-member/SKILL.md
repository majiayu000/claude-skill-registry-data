---
name: add-org-member
description: >
  Add a Dimagi teammate to a Connect organization by email so they can see ACE's programs there. Use for @dimagi.com staff only.
disable-model-invocation: false
---

# Add Org Member

Invite a human to a Connect **workspace** (Connect's term: *organization*) by
email. This is the "let me / let a teammate into ACE's workspace so they can
see what ACE is building" flow. "ACE's workspace" is the instance's configured
PM org (`connect_orgs.pm_org`, `lib/connect-orgs.ts`) — never a typed slug.

## What it does

1. Resolves inputs (see **Arguments**): `email`, `organization_slug`, `role`.
2. **Enforces the @dimagi.com guard** — refuses any email not ending in
   `@dimagi.com`. This is an internal-team tool; adding external addresses to
   a Dimagi workspace is out of scope. If the operator genuinely needs to add
   an external collaborator, that's a deliberate manual action in the Connect
   UI by an org admin, not this skill.
3. Calls `connect_add_org_member({ organization_slug, email, role })`.
4. Reports the result — including the two Connect-side preconditions if the
   add was rejected (see **Failure modes**).

## Arguments

| Input | Required | Default |
|---|---|---|
| `email` | no | the session's `git config user.email` (i.e. "add me") |
| `organization_slug` (`--org`) | no | the configured PM org — `connect_orgs.pm_org` (resolve with `bash bin/ace-doctor --preflight --no-live` → `connect_orgs.pm_org`) |
| `role` (`--role`) | no | `member` (one of `admin` \| `member` \| `viewer`) |

Resolve `email` when omitted by running `git config user.email`. If that is
empty or not a `@dimagi.com` address, ask the operator for the email rather
than guessing.

## Precondition (enforced by Connect — you cannot bypass it)

- **ACE must be an admin of the target workspace.** ACE acts as its own
  Connect identity (`ace@dimagi-ai.com`). Connect's `add_members` view is
  `@org_admin_required`; if ACE is not an admin of `organization_slug` the
  POST 403s. The atom surfaces this as an HTTP 403 error — if you see it, ask
  a current workspace admin to add `ace@dimagi-ai.com` as an admin first (or
  to add the user directly).

The invitee does **not** need a Connect account first. Connect records the add
as a **pending invite** and emails an accept-invite link; someone with no
account signs up from that link. The membership appears only once they accept
(ace#2503).

## Process

1. **Resolve + guard.** Resolve `email` (arg or `git config user.email`),
   `organization_slug` (arg, else `connect_orgs.pm_org` from
   `bash bin/ace-doctor --preflight --no-live`), `role` (arg or `member`).
   Report the resolved slug back so the operator sees which workspace it was.
   If `email` does not end in `@dimagi.com`, STOP and tell the operator this
   skill only adds Dimagi accounts; point them at the Connect UI for external
   collaborators.

2. **Add.** Call `connect_add_org_member({ organization_slug, email, role })`.
   The atom GETs the workspace home for a CSRF token, POSTs the membership
   form, then reads back BOTH the member table and the pending-invite table,
   before and after (Connect's view redirects identically on success and
   failure, so read-back is the only reliable signal — the atom handles this).

3. **Report** by the returned `status` — every one below except a throw is a
   success, and `role` is what Connect stored (read back), not what you asked:
   - `invited-pending` — the normal outcome. The invite was created and emailed;
     they appear under *Pending Invites* (`invited_on` / `expires_on` given)
     and become a member when they click the link.
   - `already-invited` — a pending invite already existed; Connect re-sends it
     unless it was sent a few minutes ago (reinvite cooldown).
   - `invited` — a membership was created directly.
   - `already-member` — nothing changed; they were already in the workspace.
   - `role_unchanged` present — the requested role did NOT land; relay its note.

   On a `ConnectValidationError` or HTTP 403, see **Failure modes**.

## Failure modes

- **`ConnectValidationError` ("recorded neither a membership nor a pending
  invite")** — the email is in neither table after the POST, so Connect
  recorded nothing. Likely an invalid address, or the reinvite cooldown on an
  invite that was just revoked/accepted. Check the workspace's Members tab.
  Do NOT tell the person to "sign in to Connect first" — that is not a cause.
- **HTTP 403** — ACE (`ace@dimagi-ai.com`) is not an admin of this workspace.
  A current admin must grant ACE admin, or add the user directly.
- **Non-@dimagi.com email** — refused by this skill before any Connect call.

## MCP tools used

- `connect_add_org_member` (ace-connect) — the only mutating call.

## Notes

- The atom is general (any workspace, any role); the @dimagi.com guard lives
  here in the skill, so the underlying capability stays reusable for future
  internal flows.
- This is not part of `/ace:run` — it's a standalone operator convenience,
  invoked via `/ace:add-org-member`.
