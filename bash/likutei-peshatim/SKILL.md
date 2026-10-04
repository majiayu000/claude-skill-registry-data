---
name: likutei-peshatim
description: Parse a Likutei Peshatim (HTC weekly Torah newsletter) email into calendar events and publish them to /calendars. Use when the user says /likutei-peshatim, "parse this week's Likutei Peshatim", or names a specific email/message ID to process.
---

# Likutei Peshatim — newsletter to calendar

Every week HTC emails "Likutei Peshatim: <Parsha> - <Year>" to matthewjmiller07@gmail.com.
It's a dense community bulletin (Torah insights, shul announcements, job postings, yahrzeits,
event listings) mixed together in one wall of text. This skill extracts the calendar-worthy
events and appends them to `src/data/likutei-peshatim/events.json`, which
`scripts/likutei-peshatim/generate-ics.mjs` turns into `public/calendar/likutei_peshatim.ics`,
served from the `/calendars` page.

## 1. Get the raw email

Automated runs pass a scratch text file path (written by
`scripts/likutei-peshatim/fetch-new-emails.mjs`, which uses the local `gws` CLI — read-only
Gmail OAuth scope, no API billing). For an ad hoc run on a specific message, fetch it directly:

```bash
gws gmail users messages get --params '{"userId":"me","id":"<messageId>","format":"full"}'
```

The plaintext body is at `payload.parts[].body.data` (or nested deeper for
multipart/mixed) — base64url-decode it.

**First check `src/data/likutei-peshatim/processed-emails.json`** — if this message ID is
already there, stop; it's already been parsed. Never reprocess.

## 2. What counts as an event

Include anything with a resolvable date: shiurim, drashos, screenings, races, fast-day
schedules, fundraising campaigns with a date window, Scholar-in-Residence talks, and
**yahrzeits** (as all-day events — Matthew has explicitly asked for these to be included).

Skip: job postings, open-ended asks ("join our waitlist", "seeking a...for hire"), and
anything with no date at all.

Granularity: prefer one event per distinct time/session rather than collapsing a whole
schedule into one block (e.g. a Tisha B'Av schedule with 4 service times → 4 events, not 1).
When several locations share one time (e.g. "NILI Shabbat shiurim, all at 5:30 PM" across
3 homes), one event with all locations/speakers in the description is fine.

## 3. Resolving dates

The email header always anchors a Hebrew date to a Gregorian one, e.g.
`2 Av 5786 | July 16, 2026`. Most events already give an explicit Gregorian date in the
body ("Monday evening, July 20th") — use that directly.

For Hebrew-only dates (yahrzeits are almost always given only as "7 Av", "כ״ח תמוז", etc.):
**never hand-compute the Gregorian date from month-length knowledge or day-offset arithmetic
— always resolve it with the Hebcal converter API.** The Hebrew year comes from the email
header (e.g. `5786`). Call:

```
https://www.hebcal.com/converter?cfg=json&hy=<hebrew_year>&hm=<hebrew_month>&hd=<hebrew_day>&h2g=1
```

`hm` takes standard English transliterations (`Tamuz`, `Av`, `Elul`, `Tishrei`, `Cheshvan`,
`Kislev`, `Teves`, `Shvat`, `Adar`, `Adar1`/`Adar2` in a leap year, etc. — not the Hebrew
glyphs from the email). The response's `gy`/`gm`/`gd` is the Gregorian date. Example:

```bash
curl -s "https://www.hebcal.com/converter?cfg=json&hy=5786&hm=Av&hd=2&h2g=1"
# {"gy":2026,"gm":7,"gd":16,...}  →  2026-07-16
```

For Hebrew-only dates written in Hebrew glyphs (e.g. "כ״ח תמוז"), transliterate the month
and convert the gematria day number before calling the API — don't guess the Gregorian date
from the glyphs directly.

**Still sanity-check the result** against known fixed points stated elsewhere in the same
email (e.g. Tisha B'Av) and against day-of-week where given ("Wednesday 8/22/26" that
doesn't match the API's date is very likely a copy-paste typo in the newsletter itself —
trust the API, note the correction in the event's description, don't blindly transcribe an
inconsistent date).

Times are America/Chicago local time — store as plain `"HH:MM"` (24h), not with an offset;
`generate-ics.mjs` handles the UTC/DST conversion.

## 4. Event schema

Append to `src/data/likutei-peshatim/events.json` (array), each entry:

```json
{
  "id": "lp-YYYYMMDD-short-slug",
  "title": "string",
  "date": "YYYY-MM-DD",
  "time": "HH:MM",            // omit or set allDay:true for all-day (yahrzeits, etc.)
  "endTime": "HH:MM",         // optional; else durationMinutes (default 60) is used
  "durationMinutes": 60,      // optional
  "endDate": "YYYY-MM-DD",    // optional, for multi-day all-day spans
  "allDay": false,
  "location": "string or null",
  "description": "string",
  "sourceExcerpt": "verbatim quote from the email this event was parsed from",
  "category": "shiur|drasha|screening|race|fast|campaign|event|yahrzeit",
  "sourceMessageId": "<gmail message id>",
  "sourceSubject": "<email subject>",
  "sourceDate": "YYYY-MM-DD"  // date the email was sent
}
```

`id` must be unique and stable — dedupe against existing entries in events.json (same
title+date already present from a prior week means don't re-add).

## 5. Finish: mark processed, rebuild, ship

1. Append `{id, subject, date, eventCount}` to `src/data/likutei-peshatim/processed-emails.json`
   for this message — **even if eventCount is 0** (e.g. an addendum with no dated content),
   so it's never reprocessed.
2. Run `node scripts/likutei-peshatim/generate-ics.mjs` to rebuild the ICS file.
3. `git add` only the 3 files touched (events.json, processed-emails.json,
   public/calendar/likutei_peshatim.ics) plus calendars.astro if the event count line needs
   no edit (it's computed from events.json automatically — don't touch calendars.astro for
   routine runs).
4. Commit (`Add Likutei Peshatim events: <Parsha> - <date>`) and push to origin main.
