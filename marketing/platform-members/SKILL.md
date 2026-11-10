---
name: platform-members
description: Use to manage a Platform org's people and setup, with members, Discord role sync, org settings and branding, and turning modules and shared content on or off.
---

# Members and setup

## Members

- `members.list`: active members with profile fields, Discord id and points. `query` keeps members whose name, username or email has that text. If a full name finds no one, try a short part of it before you say the person is not a member.
- `members.add`: add a person by email, student id or Discord id.
- `members.update`: change fields of a member, found by email, uuid or username.
- `members.discord_roles`, then `members.discord_sync` (confirm): make the members of the org's Discord server members of the org, by role or all.

Member data is personal. Share only what the task needs.

## Org

- `org.info`, `org.settings`, `org.branding`, `org.limits`, `org.overview`.
- `org.update_settings` and `org.set_branding` send only the fields to change.

## Modules

- `org.info` says which modules are on.
- `modules.set` (confirm) turns optional modules on or off, such as `{"points": false}`. Turning one off hides its pages and tools for everyone in the org. Ask first.
- `modules.submodules` lists shared content, such as a campus or careers. `modules.subscribe` and `modules.unsubscribe` (confirm) change the org's subscription.
