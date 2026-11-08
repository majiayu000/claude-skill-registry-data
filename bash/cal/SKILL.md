---
name: cal
description: Cal.com integration for AI agents via ClawLink — browser login, no API key setup. Connect cal through ClawLink's hosted setup. Use this skill when the user wants to work with Cal.com (Events & Scheduling) — connect Cal.com, read or update Cal.com data, or take actions in Cal.com from chat instead of saying you cannot access it.
---

# Cal.com

Use **Cal.com** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Cal.com once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect cal   # opens browser → authorize Cal.com
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Cal.com

```bash
npx @useclawlink/cli actions cal "<what you want to do>"   # find an action
npx @useclawlink/cli describe cal <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run cal <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `cal_add_attendee` | Tool to create a new attendee for an existing booking in Cal.com. Use when you need to add an additional participant to a scheduled event. |
| `cal_add_member_to_team_using_org_and_team_id` | Adds a new member to a specified team within an organization by creating a team membership. |
| `cal_add_organization_attribute_option` | Adds a new option to an organization's SINGLE_SELECT or MULTI_SELECT attribute. Use this action to extend the available choices for an existing attribute. For example, adding a new department option like 'Marketing' to a 'Department' attribute. Prerequisites: - The organization must exist and the user must have admin access - The attribute must already exist and be of type SINGLE_SELECT or MULTI_SELECT Common use cases: - Adding new department options to a department selector - Expanding location choices for a location attribute - Creating new priority levels for a priority field Note: While it's recommended to use unique slugs for clarity, the API may allow duplicate slugs. |
| `cal_cancel_booking_via_uid` | Cancels an existing and active Cal.com booking using its unique identifier (UID). |
| `cal_check_calendar_version2` | Retrieves free/busy availability for a specified calendar to aid scheduling without revealing event details; requires an existing, accessible calendar, noting that data granularity can vary. |
| `cal_check_gcal_synchronization_status` | Call this read-only action to verify the connection and synchronization status of a user's Google Calendar integration with Cal. |
| `cal_check_ics_feed_calendar_endpoint` | Checks an ICS feed URL (expected as a query parameter) to verify its validity, accessibility, and iCalendar data integrity. |
| `cal_check_stripe_status` | Verifies if Stripe is correctly connected to the Cal scheduling system and functional for processing payments, reporting only on the integration's status. |
| `cal_check_team_stripe_integration_status` | Retrieves the Stripe integration status and related information for a team, primarily to verify account connection, subscription details, or payment setup; this is a read-only operation that does not modify Stripe settings. |
| `cal_confirm_booking_by_uid` | Confirms an existing booking by `bookingUid` if the booking exists and is in a state allowing confirmation (e.g., not already cancelled or confirmed); this finalizes the booking, does not modify its details, and should typically be performed once. |
| `cal_connect_to_calendar` | Initiates or checks the external connection status for a specified calendar, possibly returning a redirect URL for user authorization to complete integration, without altering calendar data. |
| `cal_create_membership_for_organization` | Creates a new membership for a user within a Cal.com organization. The caller must have admin/owner access to the organization, and the target user must already exist in the system. Use CAL_RETRIEVE_USERS_IN_ORGANIZATION to get valid user IDs. |

## Notes

- **No API key for Cal.com itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect cal`.
- The action list above is a snapshot; `npx @useclawlink/cli actions cal` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
