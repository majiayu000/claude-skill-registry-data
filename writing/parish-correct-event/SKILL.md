---
name: parish-correct-event
description: Correct an event (an "aktualita") already on the new farakurim.cz site - fix its text, date, time, place, programme or links through a corrected record with pnpm replace-event, or stage a corrected or added poster or attachment with --corrected, or make another attachment its poster (or remove it) with pnpm event-poster, then publish. Use whenever the user says an event ("aktualita") is wrong or has changed (new time or place), brings a corrected poster or invitation ("plakát", "pozvánka"), wants to add a file to an event already there, or says its poster is the wrong file or should go. A cancelled or postponed event, or a dropped meeting of a series, is handled by parish-cancel-event, a new event is added with parish-create-event, the pin is moved with parish-pin-event.
---

# Correct an event

A corrected record goes in with `pnpm replace-event`, a corrected or added file with
`pnpm stage event --corrected`, and another poster with `pnpm event-poster`.

## 1. Find the event

Look for the event the user names (title, date, place) in `src/content/news/` and take its `id`. When the
description fits several events or none, list the candidates (id, title, dates) and ask.

The `id` never changes: it is the detail page's URL, in shared links and in the Události calendar. It holds the
start year, so a start in another year cannot be corrected: tell the user so and stop.

## 2. Write the corrected record

Copy the record whole into `record.json` in the session's scratchpad (never in the repo), with its `poster`,
`attachments`, `published` and `pinned`, and change only what is wrong:

- a corrected poster or invitation: read it as **`parish-create-event`** step 1 reads a source, compare it
  with the record and take over every difference;
- a correction the user describes: change those fields;
- a cancellation, a postponement or a dropped meeting: stop and follow **`parish-cancel-event`** instead.

The fields follow **`parish-create-event`** step 2.

## 3. Check

Only the record changes:

```sh
pnpm replace-event <scratchpad>/record.json --check
```

Corrected or added files, only those (the record on the site is used without `--record`):

```sh
pnpm stage event <id> "<source>" "<label>" ["<source>" "<label>" …] --corrected [--record <scratchpad>/record.json] --check
```

A file replaces the attachment with the same `label`, so take the label from `attachments`; another label adds a
file at the end. The other attachments stay. The poster is rendered again when the file it was made from is
corrected; otherwise it changes only as below.

Another attachment (an image or PDF) as the poster, or no poster:

```sh
pnpm event-poster <id> "<label>" --check   # or: pnpm event-poster <id> --none --check
```

When it says the attachment's file is not here, run `pnpm pull-uploads` first.

They all print the fields that change (`Changed: …`); the stage command also the files it would stage, the poster
command the poster it would render.

## 4. Confirm with the user

Show the user each changed field as old → new, and each file with whether it changes the poster. The
`Changed:` line must list only the fields you meant to change: another field there means the record was not copied
whole.

Wait for the user's yes or corrections to these before replacing or staging anything.

## 5. Replace

Run the step 3 command without `--check`. Show the Události calendar lines it prints unless they say `linked`.
After a change of date, time, title or place, ask the user to change the event in the Události calendar too: after
a new date the check reports it `missing` and writes an `.ics`, but importing it would add a second event, so the
existing one is moved instead.

## 6. Publish

Follow **`parish-publish-content`**.

## Common mistakes

- Editing a record in `src/content/news/` by hand instead of `pnpm replace-event`.
- Writing `record.json` from scratch: the poster, attachments or `published` get lost (see `Changed:`).
- Changing the `id`: shared links and the calendar link break.
- Changing `pinned` in `record.json`: it is refused; pin with **`parish-pin-event`**.
- Staging a corrected file under another label: the old attachment stays next to the new one.
- Changing `poster` in `record.json` by hand instead of `pnpm event-poster`: its WebP would not exist.
- Removing or reordering attachments with the stage command: change `attachments` in `record.json` and run
  `pnpm replace-event`.
- Importing the `.ics` after a date change instead of moving the Události event.
- Moving a postponed event to its new date as a plain correction: a postponement needs its `change`, with
  **`parish-cancel-event`**.
