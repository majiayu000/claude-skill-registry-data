---
name: apple-photos
description: Access your Photos.app library on a Mac via AppleScript — list albums, list/count what's in an album, export photos out to files (to view or edit them), or import a photo into an album with a specific date. Use when you reference a Photos album by name (e.g. "my Vacation album"), ask if the agent can see certain photos, or want an edited photo placed back into your library/album. Pairs with the `photo-touchup` skill for actually editing what comes out of here.
---

# Apple Photos (local, via AppleScript)

Photos.app exposes albums and media items to AppleScript — no API key, no iCloud calls, works
because Photos.app is signed in locally on the Mac. Everything goes through `scripts/photos.py`,
which wraps `osascript` calls consistently (escaping, indexing, error handling). Don't hand-roll
`osascript -e` inline for this — use the script so indexing stays consistent across calls.

```bash
python3 scripts/photos.py list-albums
python3 scripts/photos.py list --album Vacation                    # index, filename, date — tab-separated
python3 scripts/photos.py count --album Vacation
python3 scripts/photos.py export --album Vacation --out ~/Pictures/export --start 60 --end 76
python3 scripts/photos.py import --file ~/Pictures/edit.jpg --album Vacation --date "January 15, 2024 9:30:00 AM"
python3 scripts/photos.py set-date --album Vacation --filename edit.jpg --date "January 15, 2024 9:30:00 AM"
```

## Workflow for "do you see X in my [album] album"

1. `list-albums` if you don't already know the exact album name (case/spelling must match exactly).
2. `list --album NAME` to get every filename + date. **Filenames alone rarely tell you what's in
   the photo** — you have to actually look at the images. Don't guess content from filename/date.
3. `export --album NAME --out <scratchpad-dir>` — do this in batches (e.g. 15-20 at a time via
   `--start`/`--end`, using the 1-indexed position from `list`) rather than all at once if the
   album is large; it's easier to work through images in the Read tool that way.
4. Downscale before reading, then read: full-res photos from a modern iPhone are large and slow
   to load/reason over many at once.
   ```bash
   mkdir -p thumbs && for f in *.jpeg; do sips -Z 500 "$f" --out "thumbs/$f"; done
   ```
   Read the `thumbs/` versions to identify what's in each photo; go back to the full-res export
   only for the specific file(s) you end up editing or need detail from.

## What Photos will and won't let a script do

Verified by probe:

| verb | works? | |
|---|---|---|
| `delete media item` | **no** | compiles, then fails `-10000` at runtime |
| `delete album` | yes | the album only, not its photos |
| `make new album` | yes | |
| `add {items} to album` | yes | takes a list, one call |
| `remove … from album` | **no** | not a dictionary term at all |

**You cannot delete a photo from a script.** `delete` appears in the scripting
dictionary and `osacompile` accepts it, so it looks supported — but the handler
always raises `Photos got an error: AppleEvent handler failed. (-10000)`. Every
addressing form was tried (`media item id X`, `first media item whose id is X`,
`media item id X of album Y`); all three *read* fine, none delete. Apple
reserves deletion for the user in the UI. Don't burn a session working around
it, and never report that a script deleted anything.

The workaround that does work: `make new album` + `add {…} to album` to corral
the condemned, then the user opens it and does Cmd-A, Delete. Confirmed end-to-end.

**Address media items by `id`, never by album index, whenever the operation
could change the album.** Indices renumber the moment anything is deleted, so
an index-addressed batch operates on the wrong photos partway through. Get ids
with `id of m` while iterating `media items of album "X"`.

**Filenames are not unique within an album.** A large album can have
filenames appearing twice (re-imports months apart, pixel-identical). Exporting
a whole album into one flat folder lets Photos silently collide them — export in
per-batch subfolders and verify each batch's file count against the expected
names. Match a library item on `(filename, capture date)` when you need a
stable key across runs.

## Gotchas

- **`photos.py` needs Python 3.10+** — it uses PEP 604 unions (`int | None`), and
  `/usr/bin/python3` is 3.9, which dies at import with `unsupported operand
  type(s) for |: 'type' and 'NoneType'`. Call it with a Homebrew/pyenv `python3` (3.10+),
  or `shutil.which('python3')` from a script.
- **`export` requires the destination folder to already exist** — `mkdir -p` it first (the script
  does this for you if you go through `import_item`/`export_items`, but if you ever call
  `osascript` directly, Photos silently does nothing if the folder is missing rather than erroring
  loudly — you'll just get an empty directory and no error message).
- **HEIC/MOV get converted on export** — Photos exports HEIC as JPEG and leaves video as-is
  (`.mov`/`.mp4`); filter those out before batch-thumbnailing (`sips` can't convert video).
- **Index order from `list` is Photos' own internal media-item order for that album** — in
  practice this has matched chronological (oldest→newest) for every album checked so far, but
  it's not a documented guarantee. If exact chronological order matters, cross-check against the
  `date` column `list` prints rather than assuming index order.
- **Date strings are parsed by AppleScript's locale-aware `date "..."` coercion** — the format
  that reliably works on a US-English Mac is `"Month DD, YYYY H:MM:SS AM/PM"` (e.g.
  `"January 15, 2024 9:30:00 AM"`), which is also exactly the format `list`'s date column prints
  in (minus the weekday) — copy from there when you need to match an original photo's timestamp.
- **`import` needs an absolute POSIX path** — the script resolves `~` and relative paths for you;
  if you ever bypass it, Photos' `import` command will fail silently on a bad path rather than
  erroring.

## Common combined flow (touch up a photo, put it back in the same spot)

1. `export --album X --out <dir> --start N --end N` to pull one photo out (use `list` first to
   find its index, or match by filename after exporting a range).
2. Hand off to the `photo-touchup` skill.
3. `import --file <edited> --album X --date "<original's date from list>"` — this drops the edit
   into the album positioned/sorted right next to the original, which is usually what's wanted.
