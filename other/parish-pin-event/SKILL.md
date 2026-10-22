---
name: parish-pin-event
description: Change the "Doporučujeme" (recommended, pinned) event on the Aktuality page of the new farakurim.cz site - pin an existing event (an "aktualita") or unpin it, then publish. Use whenever the user wants to pin, unpin, feature, recommend or change the Doporučujeme event, for an event already on the site. A new event is pinned with parish-create-event.
---

# Pin an event

"Doporučujeme" is the panel at the top of the Aktuality page (`design/DESIGN.md` §11): it shows the one pinned event
until it ends, and none when nothing is pinned. At most one record is pinned (`src/content/news/news.test.ts`),
so `pnpm pin-event` is the only way to change it: it unpins every other record itself. Never edit `pinned` in a
month file by hand.

## 1. Find the event

The records are in `src/content/news/<year>/<MM>.json`, in the file of their **start** month. Look for the event
the user names (title, date, place) and take its `id`. Only an event that has not ended (`end`, else `start`, is
today or later in Prague) can be pinned; the script refuses the others. When the user's description fits several
events or none, list the candidates (id, title, dates) and ask.

## 2. Check and confirm

```sh
pnpm pin-event <id> --check   # or --none --check to unpin every record
```

It prints `Would pin <id> (<title>)` and a `Would unpin …` line for each record that loses the pin, or
`<id> (<title>) is already the only pinned event` (nothing to do: say so and stop). Show the user
which event becomes "Doporučujeme" and which one stops being it (say so when that one has not ended yet: it leaves
the panel early).

Wait for the user's yes or corrections to these before pinning anything.

## 3. Pin

```sh
pnpm pin-event <id>   # or --none
```

It writes the changed month files, formats them and runs the news tests (`pnpm test src/content/news`). A failing
test stops it: fix the cause, do not edit `pinned` around it.

## 4. Publish

Follow **`parish-publish-content`**.

## Common mistakes

- Editing `"pinned": true` into a month file: a second pinned record fails the tests and the release.
- Pinning an event that has ended: the panel would not show it, so the script refuses it.
- Picking one of several matching events without asking.
