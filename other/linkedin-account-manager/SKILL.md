---
name: linkedin-account-manager
description: Review, prepare, and manage approved changes across a LinkedIn member profile or company page. Use for headline, About, Experience, Featured, skills, page details, content, comments, inbox, connections, and account housekeeping.
license: MIT
metadata:
  version: "2.2.0"
  copyright: "VINCENZO PICCIUOLO (C) 2026 HRN INNOVATION TECHNOLOGIES LTD"
---

# Manage a LinkedIn account

Read `../../references/session-and-safety.md`,
`../../references/automation-modes.md`, and
`../../references/profile-rubric.md`.

1. Confirm the target account or company page, selected mode, granted scope,
   and the requested outcome.
2. Read the current state before proposing edits. In manual mode, ask for only
   the relevant section. In automatic or API mode, access only fields allowed
   by the current session or scopes.
3. Build a change set with `current`, `proposed`, `reason`, `evidence`,
   `reversibility`, and `approval status` for every item.
4. Use the focused skills for copy quality, content, comments, replies, direct
   messages, analytics, or campaigns when needed.
5. Never invent credentials, roles, dates, employers, results, recommendations,
   or endorsements. Use `{{NEEDS INPUT: ...}}` and block that edit.
6. Queue actions in a safe order. Low-risk reversible edits come before
   publishing, sending, connection changes, or deletion.
7. Show the exact final value and target immediately before each live change.
   Obtain explicit approval for that action.
8. Execute through the selected mode, verify the visible result, and save a
   receipt without sensitive data.
9. For unsupported API operations, explain the scope gap and offer manual mode.
   Offer automatic mode only after its required warning and acknowledgement.

Inventory the relevant surface rather than assuming "profile" means headline
and About only:

- identity, profile photo, banner, name pronunciation, headline, location,
  contact information, and public URL;
- About, Featured, Experience, Education, certifications, projects,
  publications, languages, volunteering, services, skills, recommendations,
  and creator settings visible to the account;
- posts, newsletters, events, comments, replies, reactions, saved drafts, and
  scheduled content visible to the account;
- notifications, inbox triage, connection requests, follows, and account
  housekeeping;
- company-page identity, description, buttons, locations, admins, content,
  moderation, and analytics when the user has the necessary page role.

Availability depends on the selected mode and LinkedIn UI or API permissions.
Do not change legal names, employment records, contact information, admin
roles, security settings, or visibility settings without naming the consequence
and obtaining an especially clear approval.

This skill is independently usable. It may draft and sequence a complete change
set even when no live adapter is connected.
