---
name: lyrics
description: >-
  Work on lyrics — the web fallback (LRCLIB, Musixmatch, NetEase, Genius), the in-memory
  cache, verification, and embedding lyrics into audio file tags. Use this
  whenever a task touches `services/lyrics.py`, `services/tags.py`, the
  `/lyrics.json` route, or `scripts/embed_lyrics.py` / `embed_lyrics_cron.sh` —
  adding or fixing a provider, changing caching/verification, or the batch
  tagger. Covers the provider contract, the synced-vs-plain rule, the read-only
  cache, and why writes only ever store plain text.
---

# Lyrics: web fallback + tag embedding

Two cooperating pieces:

- `services/lyrics.py` — fetch lyrics from the web (used by the `/lyrics.json` route and the CLI). **Read-only** with respect to Lyrion.
- `services/tags.py` — write lyrics into an audio file's tags via mutagen (used by `scripts/embed_lyrics.py`). Framework-free, no Flask/Lyrion import.

Lyrion's `library.db` is **read-only**, so web lyrics can never be stored back there — they live in a process-local cache (web app) or get written straight into the files' tags (CLI), which Lyrion then re-scans.

## Provider contract

Each provider is a function `(artist, title, album, duration) -> result | None`. A hit is a dict:

```python
{"lyrics": str | None,   # plain text
 "synced": str | None,   # LRC with timestamps, when the provider offers it
 "meta":   {"artist", "title", "album", "duration"} | None,  # for verification
 "versions": [{"lyrics", "synced", "album", "duration"}]}    # optional, winner first
```

`versions` is how a provider that found the song several times offers the others: the page cycles through them so a listener can weigh a take against the one it picked. Only LRCLIB fills it — Musixmatch answers with one subtitle, NetEase with one LRC and Genius with one page — and the winner is always its first entry, so `lyrics`/`synced` stay the answer for any caller that ignores the list (the batch CLI does). It is capped at `MAX_VERSIONS`, because every entry carries a full lyrics body into a cache entry that lives for `TTL_HIT`.

**The order is the priority, because it is also the order a cap eats from the back.** The synced uploads come first, then the plain ones of that same length: a plain upload is still a second reading of the words, worth reaching when the tags are wrong, but it is what a full budget can afford to lose. `MAX_VERSIONS` counts the library's own text too, even though no provider can see it — the page holds that one, so a response may legitimately fill the whole budget and the page trims its tail when it has a local text to put first.

Providers live in `services/lyrics.py`: `_provider_lrclib`, `_provider_musixmatch`, `_provider_netease`, `_provider_genius`, registered in the `PROVIDERS` map. Order comes from the `LYRICS_PROVIDERS` env var (`_enabled_providers`); **synced-capable providers first** (LRCLIB, Musixmatch, NetEase) because display always prefers synced (karaoke) over plain — Genius is plain-only, so it comes last. Unknown names in the env list are silently ignored, so an operator can disable a flaky provider by dropping it.

**A provider that can return either form must prefer the synced one, inside itself.** LRCLIB stores lyrics per upload: the record `/get` matches on the exact artist/title/album/duration signature may be plain-only while another upload of the same track carries an LRC, so `_provider_lrclib` keeps a `/get` hit with no synced record of this length — plain-only, or an LRC whose length `_duration_close` refuses — as a fallback and still runs `/search`, scanning the candidates for one with `syncedLyrics` instead of taking `results[0]`. The chain above it only settles across providers: `_search_providers` holds the first plain-only answer and keeps asking the later providers for a synced one, skipping those in `PLAIN_ONLY_PROVIDERS` (Genius), whose answer could only be plain again; the held answer stands when none syncs, and a later outage does not cost it (`tests/test_lyrics_lrclib.py`, `tests/test_lyrics_chain.py`). With `verify` the first plain answer ends the chain, since the CLI stores plain text only.

`_lrclib_search` returns that winner **and the set it came from**, ranked by `_by_length`: the length-matching synced uploads, then the length-matching plain ones behind them (or those alone when nothing is synced). The `/get` hit joins the tail when the search that found the LRC never returned it — it matched the exact artist/title/album/duration signature, so it is the one plain reading that is certainly this recording's. The `get` hit normally comes back from `/search` too, under the very signature that found it, so it is dropped from the others by `id` — the one duplicate with an exact criterion. Nothing is de-duplicated on the text: two uploads of a song differ by a mistranscribed line or a missing verse, which is precisely what someone comparing them is looking for, so any similarity threshold would remove the signal along with the noise.

**A name the two sides spell differently finds nothing.** LRCLIB matches names as it stores them, so `_lrclib_attempts` builds the `/search` queries in two passes: each name album-filtered first for precision then without it, then the whole set again with the leading articles dropped — the one word a library and a catalogue routinely disagree on (`Les Fatals Picards` tagged as `Fatals Picards`).

**But a synced record only counts if it is the same recording.** An LRC's timestamps belong to the upload they were made for, so a live or extended version scrolls against the wrong timeline — the karaoke sits idle, then jumps. `_duration_close` (the same tolerance `_matches_request` verifies with) filters the `/search` candidates before the synced preference applies, and a record of another length still serves its `plainLyrics`: right words with no karaoke beat a karaoke that's wrong. Several uploads routinely fit that tolerance, so `_closest_in_length` takes the one nearest this track's length rather than the first LRCLIB listed. Both lengths keep their fraction (`_float_duration`, where `/get`'s signature parameter and the logs still want whole seconds): a dozen uploads sit on the same second, and the one matching to the millisecond is the same rip, hence the same timeline. `min` is stable, so candidates the length still cannot separate keep the catalogue's own order.

**A fuzzy matcher's own answer has to be checked inside the provider.** Musixmatch's `matcher.track.get` always returns its nearest hit, so a track absent from its catalogue comes back as a different song — often in another language, since that is what "nearest" reaches for once the title stops matching. `_provider_musixmatch` runs the matched track through `_matches_request` and returns `None` when it doesn't line up, whatever the caller's `verify` setting: unlike LRCLIB's signature `/get`, there is no upstream "no match" to fall back on. It also picks the subtitle by language (`_mxm_subtitle`) rather than taking `subtitle_list[0]`, since a translation among the subtitles would swap out the words; when only translations are on offer the plain lyrics stand alone.

**NetEase Cloud Music's search is free text too**, so `_provider_netease` holds its hits to the same rule: `_netease_pick` keeps those that pass `_matches_request` against any of their credited artists (a duet lists both) and takes the nearest in length. Its LRC opens with the song credits as timed lines in Chinese (`作词 : …`), which `_NETEASE_CREDIT_RE` drops so they don't scroll as lyrics; a text with no timestamp at all comes back as plain lyrics. Only `/cloudsearch/pc` still answers anonymously: `/search/get/web` encrypts its `result` and `/search/pc` demands a phone-verified account, both behind an HTTP 200, so a `result` that is not an object is logged at INFO as a blocked search. Its hits carry `ar`/`al`/`dt`, durations in milliseconds, and it wants a browser UA with a `music.163.com` referer.

The search's `INFO` line counts one set narrowing three times — candidates returned, those of this length, those of them synced — so the last number is what the page can actually offer. Counting synced records over the whole result set instead, as it once did, reports versions that the length filter has already discarded.

**Adding a provider:** write `_provider_<name>(artist, title, album, duration)` returning the dict above (set the `meta` fields you can, leave the rest `None`), add it to `PROVIDERS`, and — since a provider must never break the chain — catch its own network/parse exceptions and return `None` on failure. `fetch_lyrics` already wraps each call in a `try/except`, but keep provider-internal failures from raising too. Use a browser-like UA where a service blocks default agents (see `BROWSER_UA`).

## fetch_lyrics: the orchestrator

`fetch_lyrics(track_id, artist, title, album, duration, force, verify)`:

- Tries each enabled provider in order, keeps the **first synced** result, else the first plain one (see above).
- Returns `{"lyrics", "synced", "source"}`, plus `versions` when the provider offered several. `source` is the winning provider name (preserved across cache hits so the UI can show the origin), `"none"` when nothing was found, or `"rejected"` when a candidate came back but failed verification.
- **Caching:** an `OrderedDict` LRU behind a lock, bounded to `CACHE_MAX_ENTRIES`, with hits kept `TTL_HIT` (24h) and misses `TTL_MISS` (1h) — a track with no lyrics online isn't re-queried on every click, but a transient failure recovers sooner. The cache key is `track_id|artist|title|verify`, **not** track_id alone: streamed "flow"/mix sources reuse one playlist track_id while the song changes underneath, which would otherwise serve the first song's lyrics for all of them.

## Diagnosing a track without lyrics

The chain logs its own reasoning (see `logsetup.py`), so `docker logs` answers "why no lyrics" without a debugger:

- `INFO` — the whole story of one track: the library miss from `get_track_lyrics` (which separates "the library has no lyrics" from "the web fallback found nothing"), each provider's verdict (`has no match`, unreachable, rejected-with-the-candidate), the closing `lyrics: <title> by <artist> -> <source> (synced=…, plain=…) in N ms`, a cache hit served instead of a search, and throttling. A provider whose own shortlist explains the verdict says so here too: each LRCLIB `/search` attempt reports the artist name and album filter it used, how many candidates came back, how many carry an LRC and how many are of this track's length — which separates "nothing on LRCLIB" from "a synced upload exists but for another recording". Two LRCLIB lines carry a browsable URL so the catalogue can be checked by hand: a lookup that found no record at all logs the site's search page for the same artist and title (`_lrclib_search_url`), and a synced record dropped for its length logs `lrclib.net/tracks/<id>` with both durations. That search does not filter on duration the way `_duration_close` does, so it lists records the app refuses — the gap is the diagnosis.
- `DEBUG` — the HTTP detail behind those verdicts, the lookups that succeeded, the search inputs (album, duration, verify), and the LRCLIB record finally chosen, which opens at `lrclib.net/tracks/<id>`.

A new provider raises `ProviderUnavailable` for unreachability — `_search_providers` logs the warning with the cause, so don't log it twice — and keeps its own dead ends at DEBUG, except a non-200 that is not part of a normal fallback (LRCLIB's `/get` 404s routinely before `/search`, so that one stays DEBUG).

## Verification (`verify=True`)

The batch CLI writes lyrics **permanently** into tags, so it opts into verification: `_matches_request` requires the candidate's normalized title and artist to equal the request's, and — when both durations are known — to fall within `VERIFY_DURATION_TOLERANCE` seconds (the surest way to tell the real recording from a live/remix/cover). `_fold_name` does the comparing: `_normalize` (accents, case, parenthetical qualifiers, "feat." credits; letters of every script survive, so a Chinese or Cyrillic name is compared rather than folded to nothing), then the leading article dropped and plural words trimmed, so a library tagged "Fatal Picards" still matches the catalogue's "Les Fatals Picards". It folds both sides, so distinct acts stay apart, and the duration is what tells two recordings of one song apart. The web route does **not** verify (lenient recall); the CLI does (precision — a wrong tag is worse than none). The flag governs the chain in `_search_providers`; `_provider_musixmatch` applies the same rule to itself unconditionally (see above), so the lenient path still never shows another song's lyrics.

## Writing tags (`services/tags.py`)

- Handles mp3/aiff/wav (`USLT`), mp4/m4a (`\xa9lyr`), flac/ogg/opus (`LYRICS`).
- **Only plain text is ever stored** — `lrc_to_plain` strips LRC line/word timestamps and metadata lines first, for maximum player compatibility. Even when a synced result is fetched, the embedded tag is plain.
- `read_metadata`, `has_lyrics`, `write_lyrics`, `clear_lyrics`; failures raise `LyricsTagError`.

## The batch CLI (`scripts/embed_lyrics.py`)

Runs outside the web app with `requirements-cli.txt` (no Flask/Lyrion). Walks files/dirs, fetches with `verify=True`, writes tags; Lyrion picks changes up on its next scan. Auto-loads the repo-root `.env` (via python-dotenv, **before** importing `services.lyrics` since its timeout is read at import). Flags: `--force`, `--clear`, `--no-verify`, `--dry-run`, `--delay`, `--verbose`. `embed_lyrics_cron.sh` wraps it to only re-tag files whose `ctime` changed (marker + `find -cnewer`), advancing the marker only on success.

## Checklist

1. New provider → `(artist, title, album, duration)` → result dict; register in `PROVIDERS`; swallow its own errors; put synced-capable ones before plain-only, and list a plain-only one in `PLAIN_ONLY_PROVIDERS`.
2. Preserve the cache-key shape and TTL split; don't key on track_id alone.
3. Tag writes store plain text only (run through `lrc_to_plain`).
4. Keep `services/tags.py` free of Flask/Lyrion imports (the CLI reuses it).
5. Add/extend tests: `test_lyrics_cache.py`, `test_lyrics_verify.py`, `test_lyrics_musixmatch.py`, `test_lyrics_netease.py`, `test_lyrics_route.py`, `test_get_track_lyrics.py`. See the `testing` skill.
