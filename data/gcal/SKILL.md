---
name: gcal
description: Google Calendar CLI for listing calendars, managing events, and checking availability. Use when you need to view, create, update, or delete calendar events, check free/busy status, or list calendars.
---

# Google Calendar CLI (gccli)

You have access to `gccli` - a minimal Google Calendar CLI. All commands use the format:

```bash
gccli <email> <command> [options]
```

## Available Accounts

- ben.tossell@gmail.com
- ben@bensbites.com  
- ben@factory.ai

## Commands

### List Calendars

```bash
gccli <email> calendars
```

Returns: ID, name, access role.

### List Events

```bash
gccli <email> events <calendarId> [options]
```

Options:
- `--from <datetime>` - Start time (ISO 8601, default: now)
- `--to <datetime>` - End time (ISO 8601, default: 1 week from now)
- `--max <n>` - Max results (default: 10)
- `--query <q>` - Free text search

Examples:
```bash
gccli ben@factory.ai events primary
gccli ben@factory.ai events primary --from 2024-01-01T00:00:00Z --max 50
gccli ben@factory.ai events primary --query "meeting"
```

### Get Event Details

```bash
gccli <email> event <calendarId> <eventId>
```

### Create Event

```bash
gccli <email> create <calendarId> --summary <s> --start <dt> --end <dt> [options]
```

Options:
- `--summary <s>` - Event title (required)
- `--start <datetime>` - Start time (required, ISO 8601)
- `--end <datetime>` - End time (required, ISO 8601)
- `--description <d>` - Event description
- `--location <l>` - Event location
- `--attendees <emails>` - Attendees (comma-separated)
- `--all-day` - Create all-day event (use YYYY-MM-DD for start/end)

Examples:
```bash
gccli ben@factory.ai create primary --summary "Meeting" --start 2024-01-15T10:00:00 --end 2024-01-15T11:00:00
gccli ben@factory.ai create primary --summary "Vacation" --start 2024-01-20 --end 2024-01-25 --all-day
gccli ben@factory.ai create primary --summary "Team Sync" --start 2024-01-15T14:00:00 --end 2024-01-15T15:00:00 --attendees a@x.com,b@x.com
```

### Update Event

```bash
gccli <email> update <calendarId> <eventId> [options]
```

Options: same as create (all optional).

### Delete Event

```bash
gccli <email> delete <calendarId> <eventId>
```

### Check Free/Busy

```bash
gccli <email> freebusy <calendarIds> --from <dt> --to <dt>
```

Calendar IDs are comma-separated.

Example:
```bash
gccli ben@factory.ai freebusy primary,work@group.calendar.google.com --from 2024-01-15T00:00:00Z --to 2024-01-16T00:00:00Z
```

### List Access Control Rules

```bash
gccli <email> acl <calendarId>
```

Returns: scope type, scope value, role.

## Notes

- Use `primary` as calendarId to reference the main calendar
- Date/times should be ISO 8601 format (e.g., 2024-01-15T10:00:00 or 2024-01-15T10:00:00Z)
- For all-day events, use date format YYYY-MM-DD
