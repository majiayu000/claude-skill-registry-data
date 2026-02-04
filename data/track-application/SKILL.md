---
name: track-application
description: Manages the application process, tracks statuses, and handles follow-up. Use after sending an application and for updates.
---

# Track Application

<workflow>

## Step 1: Initialization

1. Check if a tracker exists: `/02-Applications/YYYY-MM/Company-Name/Application-tracker.md`.
2. If new, create using the template in `references/templates.md`.
3. Log basic info: Company, Role, Date, Source.
   - **Initial Status:** Defaults to "Ready to Apply".
   - **Date:** Use "Pending" if not yet sent.

## Step 2: Confirmation Sweep

1. Scan all `Application-tracker.md` files.
2. Identify "Ready to Apply" or unchecked "Application Submitted" items.
3. Prompt user to confirm if these have been sent.

## Step 3: Status Updates

1. Update status (Applied, Screening, Interview, Offer, Rejected).
2. Log interactions in the "Communication Log".
3. Record interview details (Date, People, Questions).

## Step 4: Follow-up Management

1. Schedule reminders:
   - 1 week post-application.
   - 2 weeks post-interview.
2. Use templates from `references/templates.md` for emails.

## Step 5: Analytics

1. Generate weekly reports on active applications.
2. Analyze conversion rates and rejection patterns.

## Step 6: System Integration

1. Update the main application dashboard.
2. Sync dates with the calendar.

</workflow>
