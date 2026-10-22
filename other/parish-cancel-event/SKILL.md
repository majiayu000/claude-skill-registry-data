---
name: parish-cancel-event
description: Cancel or postpone an event (an "aktualita") already on the new farakurim.cz site, or drop one meeting of a series, by setting its change or cancelledMeetings through a corrected record with pnpm replace-event, then publish. Use whenever the user says an event ("aktualita") is cancelled ("ruší se", "nekoná se", "zrušeno"), postponed or moved to another date ("přesouvá se", "odkládá se"), or a meeting of a series is dropped ("odpadá"), or such a change is withdrawn. Other corrections (text, time, place, files, poster) are made with parish-correct-event, a new event is added with parish-create-event.
---

# Cancel or postpone an event

The record stays, as people may have saved, shared or imported it (design/DESIGN.md §11.9): its `change` (or
`cancelledMeetings`) makes the site show the status itself, on the cards, the detail page, the calendars and in the
`.ics`. It goes in with `pnpm replace-event`, like every corrected record.

## 1. Find the event

Look for the event the user names (title, date, place) in `src/content/news/` and take its `id`. When the
description fits several events or none, list the candidates (id, title, dates) and ask.

The `id` never changes: it is the detail page's URL, in shared links and in the Události calendar. It holds the
start year, so an event cannot be moved to another year: tell the user so and stop.

A pinned event cannot be cancelled: unpin it first with **`parish-pin-event`** (`--none`), or pin another event
there.

## 2. Write the corrected record

Copy the record whole into `record.json` in the session's scratchpad (never in the repo), with its `poster`,
`attachments`, `published` and `pinned`, and add the change. Keep its title, `text` and `tags` as they are (no
"(zrušeno)", no "Zrušeno" tag).

- **"Zrušeno"**: add `"change": { "status": "cancelled", "announced": "<today>", "note": "<reason>" }`.
- **"Přesunuto"**: set `start`, `end`, `startTime` and `endTime` to the new date and add
  `"change": { "status": "moved", "previousStart": "<old start>", "announced": "<today>", "note": "<reason>" }`.
  Add `previousStartTime` (and `previousEndTime`) when the time changed too.
- **A dropped meeting** ("setkání") of a series: add `"cancelledMeetings": { "dates": ["<the meeting's date>"] }`,
  with an optional `note`; the series stays as it is. Another dropped meeting adds its date to `dates`.
- **Withdrawn**: remove `change` (for a move, put `start`, `end`, `startTime` and `endTime` back from
  `previousStart`, `previousStartTime` and `previousEndTime`), or the meeting's date from `cancelledMeetings` (the whole key when it was the last one).

`announced` is today's Prague date ("Oznámeno 12. 10. 2026" on the detail page). `note` is one sentence in Czech from
the source, word for word; leave it out when the source gives no reason. A move's `note` follows "Přesunuto ze soboty 17. 10." on the card, so it starts in lower case: `"kvůli předpovědi počasí."`.

## 3. Check

```sh
pnpm replace-event <scratchpad>/record.json --check
```

It prints the fields that change (`Changed: …`).

## 4. Confirm with the user

Show the user each changed field as old → new, and how the site will show it ("Zrušeno: <note>", "Přesunuto ze
<old date> <note>", "Změna: setkání <date> odpadá, ostatní termíny platí."). The `Changed:` line must list only
`change`, `cancelledMeetings` and, for a move, `start`, `end`, `startTime` and `endTime`: another field there means the record was not
copied whole.

Wait for the user's yes or corrections to these before replacing anything.

## 5. Replace

Run the step 3 command without `--check`. It then checks the Události calendar, whose Kalendář and "Tento týden"
entries take the cancelled status only from a "Zrušeno: " title prefix (§16.4), never from the record, a linked
event included. Show the user the Události lines it prints unless they end in `nothing to do`, and ask them to change
the event in the Události calendar:

- cancelled, or the cancellation withdrawn: rename the event as the lines say (`rename "…" to "Zrušeno: …"`, or back
  without the prefix), and never delete it; a dropped meeting is renamed on that occurrence only. Run
  `pnpm event-calendar <id>` after the user's edit: it says `nothing to do` once the titles match;
- moved: move the existing event to the new date and time, as the line `"…" is still on <old date>: move it to …`
  says, and never import an `.ics` for it, which would add a second event. The check writes one only when the event
  is on neither date. Run `pnpm event-calendar <id>` after the user's edit: it says `nothing to do` once the
  event is on the new date.

## 6. Publish

Follow **`parish-publish-content`**.

## Common mistakes

- Deleting a cancelled event, or marking it with a "Zrušeno" tag or "(zrušeno)" in the title instead of
  `change`.
- Moving an event without `previousStart`: the card cannot say where it moved from.
- Cancelling a whole series when only one meeting is dropped: use `cancelledMeetings`.
- Writing `record.json` from scratch or editing `src/content/news/` by hand instead of `pnpm replace-event`.
- Deleting a cancelled event from the Události calendar instead of adding "Zrušeno: " to its title, or importing the
  `.ics` after a move instead of moving the Události event.
