---
name: entry-point-audit
description: Use when adding any cross-cutting change - a new gate, limit, permission check, or rule that must apply everywhere.
---

## The rule

When a change has to hold everywhere, the bug is the path you forgot. Before you add it to the handler in front of you, search the whole codebase for every entry point that reaches the same action, and apply it to all of them.

## Fires when

Adding a limit or quota, an auth or permission check, a feature flag or gate, input validation, or logging that must always fire for some action.

## How to apply

Grep the codebase for the action itself, not just the caller you're looking at: the function, the event, the command. Assume two or three entry points exist, not one. Apply the change to every one of them. Then search again to confirm none are left.

## Worked example

You add a rate limit to the REST endpoint that sends invites. Shipped. Users still spam invites, because the same send-invite function is also called from a CLI command and a nightly cron job, and neither is rate-limited.

The limit had to live at every entry point, or below all of them. Not just the HTTP door you happened to be standing at.

## Red flags

| Thought | Reality |
|---|---|
| "I'll add it to this handler" | Which handler? Find all of them first. |
| "There's only one place this happens" | Assume three until you've checked. |
| "It works from the UI" | The UI is one door. Count the others. |
