---
name: vmodal-find
description: >-
  Find moments in VModal video collections and verify every detail of the query on the actual frames before reporting a match. Use when the user asks to find, search, locate or show something (an object, scene, person, place, "a beautiful shot") in a VModal collection or sub-collection, e.g. "Find a red car. Collection: city" or "a beautiful scene in Kyoto". Requires the vmodal MCP (dev branch, with the `find` tool).
---

# vmodal-find

Search a VModal collection, group near-duplicate hits into scenes, look at a frame
from each scene, and check **every** detail of the query on it. A search score is a
similarity rank, not proof: never report a match you have not looked at.

Tool details, timestamp math and a worked example are in [reference.md](reference.md).
`<skill_dir>` below means the folder this SKILL.md is in.

## 1. Parse the request

- **Collection** (required). If missing or unclear, call `collection_list` and ask.
- **Sub-collection** (optional). A place or source name in the query ("in Kyoto",
  "Rome") may be a sub-collection. Call `collection_subcollections_list(collection_name=...)`
  and use an exact listed name only. If nothing matches, search all sub-collections
  and keep the place as a context spec.
- **Query**: what to find.

## 2. Build the spec checklist

Split the query into atomic specs and tag each one:

| Tag | Meaning | Example | Rule |
|---|---|---|---|
| core | the subject itself | car, taxi, lantern | must pass |
| attribute | color, state, count, action | red, parked, two, driving | must pass |
| context | setting, time of day, nearby thing | at night, near a shrine, FamilyMart | must pass |
| subjective | taste words | beautiful, best, nice | judged, never a hard fail |
| unverifiable | can't be seen in a still frame | someone says X, music, smell | reported, never guessed |

- Keep specs small: "red taxi with a white roof" → `red` · `taxi` · `white roof`.
- For subjective specs, judge on stated criteria: lighting, composition, a clear view
  of the subject, nothing blocking it (people, poles), no burned-in subtitles.
- Search is image-only (`search_sources` is fixed to `["image"]`), so speech and audio
  specs are always **unverifiable**. On-screen text can be read off the frame if visible.

Show the checklist to the user in one line before searching, e.g.
`Checking: red (attribute) · taxi (core) · parked (attribute) · night (context)`.

## 3. Search for recall

Run two `find` calls (in parallel), both with the same collection and sub-collection:

1. the full query, `limit=20`
2. the core spec alone (e.g. "a taxi"), `limit=20`

The MCP returns at most 20 rows per call, whatever `limit` says. Also fetch the full
query's next page (`offset=20`) in the same parallel batch; when widening (step 8),
fetch further pages (`offset=40`, `60`, …) as needed.

Do not pass `version_id` or `mode`; `find` picks a working index (newest first, falling back to an older one; the result reports `version_lancedb`). Do not use
`save_images` here (it saves top hits, which are mostly duplicates of one scene).

Merge the two result lists: full-query hits first in their returned order, then
core-only hits not already present. De-duplicate on (`stream_name`, `filename`,
`ts_unix_13digits`). Use the returned order as the rank; don't reason about what the
score number means.

## 4. Group hits into scenes

Hits with the same `stream_name` + `filename` whose timestamps are within **3 s** of the
previous hit in that group form one scene. Frames are sampled about once a second, so a
car passing by usually yields 5–10 hits.

For each scene keep: video, sub-collection, time range (first–last hit), the
best-ranked hit as its representative frame, and the hit count. Rank scenes by their
best hit's rank.

## 5. Verify the top 8 scenes

1. `image_get_url_bulk(records=[...representative hits...])`. Search rows can be passed
   as-is.
2. `image_get_bulk_from_urls(urls=[...url_pre_signed...], collection_name=...)`.
3. Convert the saved frames for viewing:
   `bash <skill_dir>/scripts/frames_to_png.sh ${TMPDIR:-/tmp}/vmodal-find/<collection> <saved_path>...`
   It prints one PNG path per input (or `FAIL <path>`). Saved paths may be relative
   to the MCP server's working directory, which is the folder Claude Code was started
   in. The script looks in `$VMODAL_MCP_CWD`, the current directory, then `$HOME`, so
   run it from that folder (shell working directories can reset between calls) or
   prefix the call with `VMODAL_MCP_CWD=<that folder>`. Don't browse `ztmp/` yourself.
4. Read each PNG and mark every spec **pass**, **fail** or **unclear**, with a few words
   of visual evidence ("white roof visible", "sky dark, street lights on").

Be strict. Dusk is not night. Maroon is not red unless the user would call it red.
A car partly cut off by the frame edge still passes `car`, but its color may be unclear.

## 6. Second look

For a scene that is PARTIAL **only** because of `unclear` specs (blocked, blurred,
cut off, too small), fetch one more frame from inside its time range, preferably a
different hit from the scene, and re-check. Keep the better result. Don't re-look at
scenes with a clear `fail`.

## 7. Verdict

- **PASS**: every core, attribute and context spec is `pass`.
- **PARTIAL**: core passes; at least one attribute or context spec is `fail` or `unclear`.
- **FAIL**: a core spec fails.

Subjective specs never change the verdict; use them to order PASS scenes (best first).
Unverifiable specs never change the verdict; list them in the footer.

## 8. Widen if needed

If fewer than **3** scenes PASS, verify the next 8 scenes. Stop after **24** scenes
viewed in total, or when the scenes run out. If nothing passes, say so plainly:
"No verified match" is a correct answer. Don't relax the specs without telling the user.

## 9. Report

```markdown
**Checking:** red · taxi · parked · night

### Verified matches
| # | Video | Sub-collection | Time (best / range) | Checks | Frame |
|---|---|---|---|---|---|
| 1 | Exploring Downtown Kyoto… | Street_Visit_in_Kyoto | 1:57 (1:54–1:58) | red ✓ taxi ✓ parked ✓ night ✓ | /abs/path/frame.png |

### Close, but not matching
| # | Video | Sub-collection | Time (best / range) | Checks | Missed | Frame |
|---|---|---|---|---|---|---|

Viewed 8 scenes: 1 pass, 2 partial, 5 fail. Not verifiable: none. Index version: v0.
```

- Video titles: replace `_` with spaces and shorten long ones.
- Times use `m:ss` (or `h:mm:ss`); see reference.md for live-stream timestamps.
- Frame paths are absolute PNG paths so the user can open them.
- Give a one-sentence description of what is in each PASS frame under the table.
- Leave a table out if it is empty, but always keep the footer line.
