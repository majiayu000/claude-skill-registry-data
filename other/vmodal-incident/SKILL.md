---
name: vmodal-incident
description: >-
  Find road incidents in VModal dashcam footage (near-miss, collision, red-light running, pedestrian or cyclist conflict, unsafe lane change), rebuild each one second by second from the real frames, and write an incident report with a timeline, a contact sheet and a confidence level per step. Use when the user asks what happened, asks for incidents, near-misses, crashes or dangerous moments, or wants an incident report, e.g. "Find near-misses with pedestrians. Collection: dashcam_v1" or "What incidents are in dashcam_v1?". Requires the vmodal MCP (dev branch) and the vmodal-find skill.
---

# vmodal-incident

Find **events**, not objects: something that happens over a few seconds. Each candidate
is rebuilt as a timeline of frames around its peak and every step is checked on a real
frame before it goes in the report. Wording stays observational: say what is seen,
never who is at fault.

This skill builds on **vmodal-find**. Read `<skill_dir>/../vmodal-find/SKILL.md` for the
spec checklist (step 2), scene grouping (step 4) and frame conversion (step 5). Follow
those rules; this file adds what incidents need. `<skill_dir>` means the folder this
SKILL.md is in. The incident catalog, frame facts and a worked example are in
[reference.md](reference.md).

## 1. Parse the request

- **Collection** (required). If missing, call `collection_list` and ask; dashcam footage
  is usually in `dashcam_v1`. Sub-collection as in vmodal-find step 1.
- **Mode**:
  - **Targeted**: the user names a type. Map it with the catalog's "Request words"
    column. A word that fits several types ("near-miss") takes all of them; say which.
  - **Scan**: "what incidents are in …", "anything dangerous". Use every catalog type.
- **Time window** (optional): "around 5:20", "in the first two minutes". Only keep hits
  inside it, plus 10 s on each side.

Show the checklist line of each type in scope (catalog "Checklist" column) before
searching. If the type covers more than the user said (cyclists for "pedestrians"),
keep it and label such incidents in the report.

## 2. Search

Run the catalog's search phrases for each type in scope in parallel (`find`, same
collection and sub-collection), `limit=50`, no `version_id` or `mode`. If a result has
no `requested_limit` field and returns 20 rows (older MCP, capped at 20), also fetch
`offset=20` of each phrase.

Merge: page 1 of every phrase first, then page 2, each in catalog order and keeping
its returned order. De-duplicate on (`stream_name`, `filename`, `ts_unix_13digits`); the
first occurrence keeps its place. That position is the hit's rank.

Search finds "eventful-looking" clips but doesn't separate types well: in testing,
"pedestrian", "red light" and "crash" phrases returned mostly the same moments. Decide
the type from the frames, not from which phrase found it.

## 3. Candidate events

1. Group hits into scenes (vmodal-find step 4: same video, ≤ 3 s apart).
2. Merge scenes of the same video ≤ **10 s** apart into one **candidate**, but a candidate
   is at most **15 s** long: when a merge would exceed that, start a new candidate.
   (Compilations otherwise chain unrelated clips into 30–45 s candidates.)
3. Keep each candidate's time range, best-ranked hit (the provisional peak) and hit
   count. Rank candidates by their best hit's rank.

## 4. Triage in batches of 10

1. **Download** the best hit of each of the next 10 candidates (see "Downloading frames").
2. **One sheet per batch**: `frames_strip.sh` with the 10 frames in candidate order
   (tile n = candidate n of the batch). Read the sheet once. Tiles are 320 px: enough to
   triage. View a frame full size only when its tile is ambiguous.
3. Judge each tile against the catalog's "PASS in triage" rule for the types in scope:
   - **PASS**: the rule is met in this frame.
   - **PARTIAL**: the participants are there but the conflict isn't visible in this one
     frame (e.g. a cyclist far ahead in our lane, a car angled toward our lane).
   - **FAIL**: ordinary traffic (queued at a red, parked, empty road) or no participants.
4. Stop triage after **two batches in a row with no new PASS**, **30 candidates**, or when
   candidates run out. Say which rule ended it.

**Rebuild** (step 5) every PASS, then PARTIALs in rank order, **at most 6 rebuilds** in a
run. One PARTIAL in testing turned out to be the only real incident, so don't skip them
when the cap allows.

## 5. Rebuild the timeline

For each candidate to rebuild:

1. **Fetch the window.** One record per second from peak − 4 s to peak + 4 s: copy the
   best hit's row and change only `ts_unix_13digits` (± 1000 ms steps). Any indexed
   second can be fetched, not only search hits. Windows of several candidates can go in
   one call (≤ 20 records per call). Many seconds are not indexed (`found: false`, "image
   not found"; up to 10 s in a row in testing): keep them as gaps.
2. **Make the contact sheet** in time order, `-` for each gap:
   `bash <skill_dir>/scripts/frames_strip.sh ${TMPDIR:-/tmp}/vmodal-incident/<short-title>_<m>m<ss>.png <path|->...`
   (`<short-title>`: 1–2 words of the video title.) It prints `TILE <n> <input>` lines,
   then the sheet path. If fewer than 3 seconds were found, skip the sheet and view
   those frames directly.
3. **Cut the clip.** Compilations jump between clips, often. A tile showing a different
   road, light, camera or overlay style, an end card or a montage, or a jump in the
   overlay clock or GPS, is a cut: drop it and everything on that side of it. If the peak
   is within 2 s of a cut, say so.
4. **Find the real peak**: the tile where the conflict is closest (smallest gap, contact,
   a person nearest the car's path).
5. **Extend once if needed.** If the peak is an edge tile of the window, **or** the
   seconds right after the peak are all gaps, fetch peak + 5 … + 8 s (or − 5 … − 8 s on
   the other side) once. Use found frames only if the overlay clock (or the scene) shows
   the same clip. If nothing usable comes back, write "after the peak: not indexed".
   At most 2 extra fetches per candidate.
6. **Merge split candidates.** If the extension reaches another candidate of the same
   clip (continuous overlay clock), treat them as one incident.
7. **View the peak frame full size** (plates, signals, lane lines and overlay text need
   the full frame), and the trigger frame too when a signal or lane line decides the type.
8. **Label each kept second** with a phase:
   - `setup`: normal traffic before;
   - `trigger`: the hazard appears (a car starts to cross, a person steps out, the light
     is red while a vehicle moves on);
   - `peak`: closest approach or contact;
   - `outcome`: what follows (stopped, swerved, drove on, debris, people on the road).

   Several seconds can share a phase; not every phase has to be seen.

### Downloading frames

- **Preferred** (dev MCP from `b0ace5b`): `image_download_from_records(records=[...])`,
  ≤ 20 records per call. It keeps input order, reports each failure, and names files
  `<asset>_<timestamp>.jpg`, so frames map back by name. No signed URLs to copy.
- **Fallback** (older MCP): `image_get_url_bulk(records)`, then
  `image_get_bulk_from_urls(urls)` with the **found** records' URLs, ≤ 20 per call.
  `saved_paths[i]` is the i-th URL sent, not the i-th record. If the result's `skipped`
  is > 0 or there are fewer paths than URLs, the mapping is lost: re-send the missing
  ones in a separate call, never guess.

### Dashcam overlay

Many dashcams burn in speed, GPS and a clock (e.g. `063KM/H S:33.9602 E:150.8759 …
23/03/2026 03:14:37`). Read them from full-size frames.

- **Speed**: report it as "overlay speed". Never estimate speed from the picture; with
  no overlay, speed is not determinable. A falling overlay speed is "speed falls", not
  "braked".
- **Clock**: real date and time. Continuous seconds = same clip, even across index gaps;
  a jump = a cut.

## 6. Confidence per step

| Level | Rule |
|---|---|
| High | seen clearly in **two or more consecutive** frames |
| Medium | seen in one frame, or partly hidden, small, or at night |
| Low | not seen; inferred from the frames before and after ("contact likely between 5:21 and 5:22") |

Frames are at most one per second, so a fast moment can fall between two frames. Say
"between frames" rather than guessing. Never state fault, intent, braking (unless brake
lights are visible), horn or other sound.

## 7. Verdict per incident

- **CONFIRMED**: the trigger and the peak are each High or Medium.
- **POSSIBLE**: the trigger is seen, but the peak is Low or hidden (cut, gap, blocked).
- **NOT AN INCIDENT**: the timeline shows ordinary traffic. Count it in the footer; name
  a rebuilt one in a few words so the user sees why it was dropped.

The catalog's type rules can cap a verdict (e.g. red-light running needs the red signal
and the vehicle entering the junction in frames).

**Who is involved**: say whether the dashcam car is a participant ("dashcam car") or only
a witness ("third parties; dashcam car not involved"). Both count as incidents.

## 8. Report

```markdown
<!-- illustrative values, not a real finding -->
**Checking:** pedestrian or cyclist (core) · in the roadway (attribute) · in or entering the car's path (attribute)
**Collection:** dashcam_v1 · mode: targeted (pedestrian / cyclist conflict)

### Incidents
| # | Type | Video | Time | Verdict | Confidence |
|---|---|---|---|---|---|
| 1 | Pedestrian conflict | Example dashcam video | 2:23–2:31 (peak 2:27) | CONFIRMED | High |

### 1 · Pedestrian conflict, 2:23–2:31
| Time | Phase | What is seen | Confidence | Frame |
|---|---|---|---|---|
| 2:24 | setup | two-lane road, person on the kerb on the left | High | tile 2 |
| 2:26 | trigger | person steps into our lane | Medium | /abs/.../trigger.png |
| 2:27 | peak | person about one car length ahead, centre of lane | High | /abs/.../peak.png |
| 2:28 | outcome | person reaches the far side, car still moving | High | tile 6 |

Involved: dashcam car and one pedestrian.
Contact sheet: /abs/path/sheet.png (tiles 2:23–2:31; 2:30 not indexed)
Overlay: 41 km/h at 2:27 · 2025-03-14 08:12:09
Not determinable from video: fault · whether the driver braked · sound

Viewed 14 candidates in 2 batches; stopped: two batches with no new PASS. Rebuilt 4.
1 CONFIRMED, 0 POSSIBLE, 13 not an incident (rebuilt and dropped: 4:02 traffic queued at a red).
Frames at most 1 per second, with gaps. Index version: v0.
```

- Video titles: `_` → spaces, shorten long ones. Times `m:ss` (or `h:mm:ss`).
- "Confidence" in the summary is the lower of the trigger's and the peak's.
- Frame column: an absolute PNG path for frames viewed full size, otherwise
  `tile <n>` of the contact sheet.
- Order incidents by verdict (CONFIRMED first), then by time.
- If triage saw a clear incident of a type **not** in scope, mention it in one line
  under the footer ("Also seen: collision at 8:12, not a red-light event").
- No incident found is a valid answer: "No confirmed incident", with what was searched
  and which stop rule ended it. Don't relax the catalog rules without telling the user.
