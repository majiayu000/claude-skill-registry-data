---
name: apple-music
description: Use the local Apple Music MCP server to browse or manage the user's library and playlists, search the catalog, discover music, control playback, or edit the Up Next queue. Trigger whenever the user asks about their Apple Music account, listening history, playlists, library, playback, recommendations, or queue.
---

# Apple Music

Use the bundled `apple-music` MCP server. The user's account and authentication are local to their computer.

## Workflow

1. For reads, call the narrowest relevant Apple Music tool and return a concise result.
2. Before a write, resolve ambiguous songs, artists, albums, or playlists. Never silently guess between similarly named items.
3. For playlist additions, use a dry run when available and show ambiguous matches or duplicates before writing.
4. Ask for confirmation immediately before destructive or bulk actions, including deleting a playlist, clearing a queue, removing many tracks, or removing library items.
5. After a write, report exactly what changed and surface any skipped, duplicate, unmatched, or failed items.

## Prompt interpretation and defaults

Ask a concise clarification only when the missing choice would change the
target, meaning, or destructive effect of the request. Otherwise use these
defaults so ordinary prompts do not become an interview.

### References and catalog matches

- Resolve pronouns such as `it`, `this`, `those`, and `them` from the immediately
  preceding result only when the reference is unambiguous. Otherwise ask what
  the user means.
- Prefer an exact playlist-name match when a prompt such as `Play workout`
  could also name a song or album. If several plausible matches remain, ask.
- When a title has multiple plausible artists, recordings, remasters, or
  explicit/clean versions, ask the user to choose. Do not silently select a
  version.
- Allow explicit tracks unless the user requests clean music.

### Playlist creation and additions

- `Create a playlist called <name>` creates an empty playlist unless the prompt
  also states a music preference, seed, or tracks.
- When playlist creation includes a preference or seed but no track count,
  populate it with 25 tracks. An explicit count overrides this default.
- If the requested playlist name already exists, ask whether to use the
  existing playlist or create one with a different name. Never replace its
  contents automatically.
- A request to add recommendations uses the recommendation count rules below.
  If neither a seed, preference, nor source playlist is supplied, ask for one.
- If tracks are supplied but the destination playlist is missing, ask for the
  destination.
- Skip tracks already present in the destination playlist by default. After
  writing, report skipped duplicates.
- Use the immediately preceding recommendation result for phrases such as
  `add those recommendations` only when that result is unambiguous. Ask for the
  destination playlist if it is not stated or clear from context.

### Removal, deletion, and organization

- Interpret `the last N tracks` as the final N items in the playlist's current
  order. Preview their exact titles and artists before removal.
- If a requested track occurs more than once or has multiple versions in the
  playlist, ask whether to remove one specific entry or every matching entry.
- Treat `clear <playlist>` as ambiguous between emptying and deleting the
  playlist; ask which action the user wants.
- Before deleting a playlist, require confirmation that includes its exact
  name. Before emptying one, preview the number of tracks that will be removed.
- For automatic folder organization, propose a playlist-to-folder mapping and
  obtain approval before moving anything.
- If a rename lacks the new name, ask for it. If creating, copying, moving, or
  renaming would cause a name collision, ask instead of overwriting.
- When copying a playlist without a destination name, use `<name> Copy`; if
  that name exists, ask for another name.

### Playback and queue

- Resolve playback targets using the reference and catalog-match rules above.
- If the user says `shuffle` without a mode, use song shuffle.
- `Queue <track>` adds it to the end of Up Next. `Play <track> next` inserts it
  next without clearing the rest of the queue.
- Do not clear or replace Up Next unless the user explicitly requests it and
  confirms after seeing its current size.

### Ratings, history, charts, export, and backup

- Interpret `like` or `love` as Apple Music love, and `dislike` as dislike.
  Never translate either into a 1-to-5 star rating.
- A star-rating request must identify a track and a rating from 1 to 5. Ask for
  whichever is missing.
- For `What have I listened to lately?`, return the 20 most recently played
  items unless the user supplies a count.
- For an unspecified chart request, use the configured storefront, the songs
  chart, and 20 results.
- Interpret `my newest songs` as recently added library tracks. If ownership is
  not stated and the prompt could mean new catalog releases, ask which meaning
  is intended.
- `Export my library` defaults to the complete library in CSV with a unique,
  timestamped filename. Do not overwrite an existing export.
- Treat `Back up my library` as ambiguous between a portable export and a local
  Music.app snapshot; ask which one the user wants.

### Platform and ownership routing

- Before editing a playlist, inspect which available route can write to it. A
  playlist created in Music.app cannot be edited through the developer-token
  API or web player. On macOS, route that write through Music.app. Off macOS,
  explain the limitation concisely and offer to create an API-editable
  playlist; do not silently redirect the write.
- Star ratings, playlist folders and paths, library snapshots, and AirPlay
  require Music.app on macOS. If unavailable, state the limitation; do not
  substitute a different operation.
- Queue operations require a signed-in supported web-player session. If none
  is available, give one concise connection instruction and stop.
- For multi-action prompts, preserve the user's stated order. Report completed,
  skipped, and failed actions separately, and do not treat one successful
  action as proof that later actions succeeded.

## Taste analysis

Treat requests to `analyze` or `analyse` a playlist, listening history, library,
or music taste as a request for a reusable taste profile.

- If the user names one or more playlists, confirm each exact playlist and read
  each track list once in structured form. Do not infer taste from playlist
  titles alone.
- If no source is stated, ask one concise question: whether to analyze a named
  playlist or recent listening and heavy rotation. Do not scan the entire
  library unless the user explicitly requests a library-wide analysis.
- For recent-listening analysis, use recent plays and heavy rotation together
  so a short-lived listening session does not dominate the profile.
- Base every conclusion on observed artists, tracks, genres, eras, languages,
  tempo or energy, and recurring mood patterns. Label weak or mixed signals as
  tentative instead of presenting them as facts.
- Do not modify playlists, the library, ratings, playback, or the queue during
  analysis.

Return a structured analysis with these sections:

1. `Taste profile` — a concise summary of the user's core sound.
2. `Strong signals` — recurring genres, moods, energy, eras, languages,
   artists, and production styles supported by the source.
3. `Discovery directions` — adjacent sounds likely to fit, plus any boundaries
   or exclusions the user stated. Do not invent dislikes from missing genres.
4. `Coverage` — the source and number of tracks or listening items inspected,
   with any important limitations.
5. `Reusable scheduled-task prompt` — a self-contained, copyable prompt that
   includes the taste profile, source playlist when applicable, a default of 5
   recommendations when no count was requested, duplicate exclusion, no
   automatic playlist writes, and the official Apple Music result requirement.

Write the reusable prompt so a future scheduled task does not need the current
conversation for context. If the user asked for a particular cadence, time,
count, mood, or destination playlist, preserve it in the prompt. Generating the
prompt does not authorize creating a scheduled task; create one only when the
user explicitly asks.

## Recommendation cards

Interpret recommendation prompts before calling tools:

- Use the exact positive integer requested by the user. If no number is given,
  default to 5 songs. Treat vague quantities such as "some" or "a few" as the
  default of 5.
- A single official Apple Music result supports at most 25 songs. If the user
  requests more than 25, ask them to choose a number from 1 to 25. If the
  number is zero or negative, ask for a positive number.
- A recommendation source is either a named playlist or a stated preference,
  such as a genre, mood, activity, artist, era, language, or other song type.
- If the user gives neither a playlist nor a preference, ask one concise
  question requesting the kind of songs they like or the name of a playlist.
  Do not also ask how many songs they want; retain an explicit count or use the
  default of 5.
- If both a playlist and a preference are provided, use the playlist as the
  source and the preference as a filter.

Examples:

- `Suggest songs` -> ask for a preference or playlist; remember the default is 5.
- `Suggest 8 songs` -> ask for a preference or playlist; retain the count of 8.
- `Suggest chill songs` -> recommend 5 chill songs.
- `Suggest songs based on my "hello" playlist` -> recommend 5 songs.
- `Suggest 3 peaceful songs based on "hello"` -> recommend 3 songs using
  `hello` as the source and `peaceful` as a filter.

For a request based on a named playlist:

1. Confirm that the named playlist exists, then read its tracks once with the
   structured output format. Do not modify the playlist.
2. Select up to three distinct representative tracks, spaced across the
   playlist and with different artists where possible. Use their artists with
   the local `discover` tool to obtain official similar artists, then retrieve
   official top songs from those artists.
3. Keep the official discovery order. Exclude candidates already in the source
   playlist and duplicate title-and-artist pairs. Stop after the exact
   requested number of candidates; never invent or pad recommendations.
4. Use the official Apple Music app's batch track-details tool to match and
   render the selected songs. Set its collection title to `<playlist name>
   recommendations` and include the source playlist in its description.
5. Return only the official Apple Music result. Do not add an introduction,
   reasons, analysis, a Markdown list, or an automatic playlist write.

The official Apple Music app is required for this flow. If its batch
track-details tool is unavailable, return one concise instruction to connect
the official Apple Music app and stop; do not return a text-only recommendation
list. If the named playlist does not exist or
the official catalog yields fewer than the requested number after filtering,
return one concise error and stop.

For a preference-only request, use the local `catalog` and `discover` tools to
obtain official Apple Music candidates matching the preference. Deduplicate
title-and-artist pairs, preserve official discovery order, pass the exact
requested or defaulted count to the official Apple Music app's batch
track-details tool, and follow the same result-only and no-write rules above.

## Tool routing

- `playlist`: list/search playlists and folders; inspect tracks; create, add, copy, move, remove, rename, or delete.
- `library`: browse/search the library; view recent or favorite items; add, remove, rate, or snapshot.
- `catalog`: search or resolve songs; inspect albums, artists, genres, or suggestions.
- `discover`: recommendations, charts, heavy rotation, stations, top songs, and similar artists.
- `playback`: play and control audio; inspect now playing; manage shuffle, repeat, volume, or AirPlay when supported.
- `queue`: inspect or edit Up Next; confirm before clearing it.
- `config`: status and preferences. Use sign-in or logout only when the user explicitly asks.

## Safety and privacy

- Do not request or display Apple passwords, cookies, user tokens, developer tokens, `.p8` keys, or raw credential files.
- Never claim that `auth unsupported` in `/mcp` means login failed; this STDIO server authenticates through `applemusic-mcp login` outside MCP OAuth.
- Do not clear the audit log, reset configuration, or log out unless the user explicitly requests it and confirms.
- For large imports, resolve in batches and stop on throttling rather than repeatedly retrying.
