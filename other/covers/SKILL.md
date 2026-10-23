---
name: covers
description: >-
  Work on album artwork — reading an image's dimensions, and embedding a
  folder's cover file into the tags of its tracks. Use this whenever a task
  touches `services/artwork.py`, the cover half of `services/tags.py`, or
  `scripts/embed_covers.py` / `embed_covers_cron.sh`. Covers why Lyrion shows
  the embedded artwork and never the folder file, how covers are compared, why
  images are never re-encoded, and what embedding costs in rewritten files.
---

# Album artwork: measuring it, embedding it

Three cooperating pieces, none of which talk to Lyrion:

- `services/artwork.py` — dimensions from an image's **header bytes**. Dependency-free, so it works on a byte string from anywhere: a file, a tag, a streamed HTTP response.
- `services/tags.py` — `read_cover` / `write_cover`, next to the lyrics functions. Framework-free, mutagen-based.
- `scripts/embed_covers.py` + `embed_covers_cron.sh` — the batch job, same shape as the lyrics pair.

## The fact that motivates all of it

**Lyrion serves the artwork embedded in the file's tags, and never the `folder.jpg` sitting beside it.** A library can therefore hold a 3000 px sleeve on disk while every player shows the 500 px one buried in the tags, with nothing in the UI hinting at the gap. `albums.artwork` in `library.db` is a coverid pointing at a *track*, not at a file on disk.

That is what `embed_covers.py` fixes: it copies the folder's file into the tags so the good image becomes the one Lyrion actually shows.

## Measuring: header bytes only

`image_size(data)` returns `(format, width, height)` for JPEG, PNG, GIF, BMP and WebP, or `None`.

```python
from services import artwork

artwork.image_size(data)      # ("jpeg", 1400, 1400)
```

`None` is deliberately ambiguous: it means *not known from these bytes*, covering both "not an image" and "the header hasn't arrived yet". A caller streaming a file can keep reading and ask again. Don't tighten that contract — a JPEG carrying a large colour profile can push its SOF marker hundreds of kilobytes in, so a fixed-size sniff is not enough.

Dimensions are read for reporting and for refusing a file that is not an image at all — **not** to decide whether to embed. That decision is a byte comparison, see below.

## Writing: never re-encode

`write_cover(path, data)` stores the bytes it is handed, as they are. It drops any existing picture first, so a file ends up with exactly one. Formats: MP3/AIFF/WAVE (`APIC`), MP4/M4A (`covr`), FLAC (picture block); anything else raises `CoverTagError`.

**Never re-encode an image to make it fit.** Every write in this codebase is a byte copy, which is why the tag and the folder file can be compared byte for byte afterwards — the cheapest possible verification that a batch did what it claimed.

Embedding **rewrites the whole audio file**: artwork rarely fits the padding a smaller cover left behind. That is why `embed_covers.py` reports how much the files grow, and why the cron wrapper exists at all — re-tagging an album the day it arrives is free, because a new album is synced and backed up in full anyway; re-tagging it six months later means resyncing a file everyone thought was stable.

## The rule: the folder decides

`embed_covers.py` compares each track's embedded bytes against the folder's file and rewrites the ones that differ. Nothing else enters the decision — not dimensions, not file size, not which looks better.

That makes the folder's file the single source of truth, and it is what lets a cover be **replaced by a smaller one**: capping an absurd 7000 px sleeve at 2000 px is a legitimate edit, and a rule of "only if bigger" would silently refuse it while leaving the huge image in every track. The protection it offered against a bad cover was accidental, never designed; review happens before the file lands in the folder.

Two properties follow, and both matter when a cron runs this nightly: only the tracks that actually differ are touched, so an interrupted run resumes cheaply; and a second pass writes nothing, so the job is idempotent.

## The batch job

```bash
python scripts/embed_covers.py /path/to/music --dry-run
python scripts/embed_covers.py "/path/to/music/A*"      # globs, even quoted
```

An album folder is any folder holding music files, which leaves `Scans/` and `Artwork/` subfolders alone. Files starting with a dot are skipped: macOS leaves AppleDouble stubs (`._track.mp3`) that carry the extension but none of the content, and reading one instead of the real track makes a fully tagged album look empty.

Every track is read, since players pick artwork per file and a half-applied album must be finishable.

`embed_covers_cron.sh` mirrors `embed_lyrics_cron.sh` — marker stamped at the start, advanced only on success, untouched by `--dry-run` — with one difference: `find -cnewer` lists changed *files*, and it is their **folders** that get passed on. A replaced `folder.jpg` therefore queues its album exactly like a new track does.

## Rules

- Read dimensions through `services/artwork.py`; never add an imaging dependency for a job the header already answers.
- Never re-encode, never resize: the bytes in the folder are the bytes that go into the tags.
- Decide on bytes, never on dimensions — the folder's file wins even when it is smaller.
- Writes go to every track of the album, not just the first.
- Lyrion is never contacted: the files are the interface, and Lyrion re-scans on its own.
