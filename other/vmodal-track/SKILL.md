---
name: vmodal-track
description: >-
  Track a subject through VModal video collections: find every verified appearance of it and return a trail (where, when, for how long, in what order). Works for a description ("red taxis in Kyoto") or for one specific subject ("this taxi", "the same woman", "the one at 1:57"). Use when the user asks to track, follow, trace, or find everywhere / every time something appears, e.g. "Track red cars. Collection: city". For a single good match use vmodal-find instead. Requires the vmodal MCP (dev branch) and the vmodal-find skill.
---

# vmodal-track

Find **every** appearance of a subject, not just the best one. Each appearance is
checked on a real frame before it goes on the trail.

This skill builds on **vmodal-find**. Read `<skill_dir>/../vmodal-find/SKILL.md` for its
spec checklist (step 2), scene grouping (step 4), frame verification (steps 5–6) and
PASS / PARTIAL / FAIL verdicts (step 7). Follow those rules exactly; this file only
adds what tracking needs. `<skill_dir>` means the folder this SKILL.md is in.
Budgets, labels and a worked example are in [reference.md](reference.md).

## 1. Scope

- **One collection** per run by default; sub-collection is an optional filter, as in
  vmodal-find step 1.
- **Across all collections** only when the user asks ("everywhere", "all collections").
  Then call `collection_list`, pick the collections that plausibly contain the subject,
  and say which ones you picked and why.

## 2. Pick the mode

- **Description mode**: any subject matching the description counts.
  "Track red taxis", "every woman in a yellow coat".
- **Identity mode**: it must be the *same* subject.
  "Track this taxi", "the same man", "follow the one at 1:57", "plate 50-20".

If unclear, use description mode and offer identity mode at the end.

In both modes, build the spec checklist and show it to the user before searching
(vmodal-find step 2).

## 3. Anchor and signature (identity mode)

1. Find the anchor: the sighting the user points to, or the best PASS from a first search.
2. View its frame (vmodal-find step 5) and write a **signature**: 2–5 details that tell
   this subject apart from look-alikes. Examples: plate number, logo, pattern, accessory,
   damage, hair, a bag. Prefer details visible from several angles.
3. Show the user the anchor frame path and the signature before tracking.

## 4. Search wide

Run these in parallel, all with the same collection and sub-collection:

- `find` with the **full description**.
- `find` with the **core subject + its most distinctive attribute** (e.g. "red taxi").
- `find` with **one rephrasing** that adds nothing new (e.g. "taxi painted red with a
  white top"). Don't add a place, era or style the user didn't say: "Japanese taxi"
  pulls the results toward Kyoto and hides other matches.
- **Identity mode only: one image search.** Crop the subject out of the anchor frame and
  encode it:
  `bash <skill_dir>/scripts/anchor_b64.sh <anchor.png> <x> <y> <w> <h>`
  (x, y, w, h in the frame's pixel coordinates; estimate them from the frame you viewed.)
  Then call `search_video(group_name=<collection>, image_query=<the base64>, limit=20)`
  (add `stream_name` if a sub-collection is set). `find` has no image input. A cropped
  subject finds the subject across scenes; a whole frame mostly finds the same place.
  At most 2 image searches per run: each base64 costs about 2–3k tokens.

**The MCP returns at most 20 rows per call** (unless `verbose=true`, which is much
larger), whatever `limit` says. Use `limit=20` and page with `offset` = 20, 40, 60, 80.

**Page lazily.** Start with page 1 of every query plus page 2 of the full description.
Fetch the next page of each text query only when every appearance found so far has been
viewed and the stop rule (step 7) hasn't ended the search. At most 5 pages per query.
Deeper pages are mostly unrelated: in testing, all PASSes came from pages 1–2.

**Merge order:** take results page by page, and within a page in the order the queries
are listed above (full, core + attribute, rephrasing, image), keeping each list's
returned order. De-duplicate on (`stream_name`, `filename`, `ts_unix_13digits`); the
first occurrence keeps its place.

## 5. Group: scenes → appearances

1. Group hits into **scenes** exactly as vmodal-find step 4 (same video, ≤ 3 s apart).
2. Merge scenes of the same video that are ≤ **10 s** apart into one **appearance**: the
   subject was briefly hidden, not gone. An appearance keeps its full time range, its
   best-ranked hit as representative frame, and its hit count.
3. Rank appearances by their best hit's rank.

## 6. Verify in batches of 10

For each batch, fetch the representative frames in one bulk call and view them
(vmodal-find step 5, converter at `<skill_dir>/../vmodal-find/scripts/frames_to_png.sh`).
`saved_paths[i]` belongs to the i-th record you sent, so keep that order to map frames
back to appearances (the saved file names don't say which frame they are).

- **Description mode**: give each appearance PASS / PARTIAL / FAIL (vmodal-find step 7).
- **Second frames**, fetched together in one extra bulk call after viewing the batch:
  - a PARTIAL that is only `unclear` gets vmodal-find's second look;
  - **an appearance spanning ≥ 5 s that FAILs gets its last hit checked too.** A subject
    can enter late: in testing, a red taxi was missing at 6:14 but in view at 6:20 of
    the same appearance. Keep the better verdict.
- **Identity mode**: for each appearance whose description verdict is PASS, also compare
  it with the signature and label it:

  | Label | When |
  |---|---|
  | SAME | the signature details you can see all match, and at least one is clearly visible |
  | LIKELY SAME | nothing contradicts the signature, but the key details are hidden |
  | DIFFERENT | any signature detail contradicts (other plate, other logo) |
  | DESCRIPTION ONLY | matches the description, but nothing visible can tell it apart |

  Never call something SAME on description alone. The same street, the same video or a
  nearby time is supporting evidence, not proof.

## 7. When to stop

Keep verifying batches until either:

- **two batches in a row add no new PASS** (identity mode: no new SAME or LIKELY SAME), or
- **50 appearances** have been viewed, or the appearances run out.

Always say which rule ended the search, so a short trail isn't mistaken for a complete one.

## 8. Report the trail

```markdown
**Checking:** red (attribute) · taxi (core) · white roof (attribute)
**Tracking:** red taxi with a white roof · identity mode
**Signature:** plate 50-20 · white roof light · green sticker on rear window   ← identity mode only
**Anchor:** Exploring Downtown Kyoto…, 1:57 → /abs/path/anchor.png             ← identity mode only

### Summary by video
| Video | Sub-collection | Appearances | Search span | First seen | Last seen |
|---|---|---|---|---|---|

### Trail
| # | Video | Time range | Verdict / label | Evidence | Frame |
|---|---|---|---|---|---|

### Close, but not matching          ← description mode only
| Reason | Count | Example (video, time) | Frame |
|---|---|---|---|

Viewed 30 appearances in 3 batches; stopped: two batches with no new SAME.
Description mode: 4 PASS, 10 PARTIAL, 16 FAIL. Identity mode: 3 SAME, 1 LIKELY SAME,
4 DIFFERENT, 6 DESCRIPTION ONLY, 3 PARTIAL. Not verifiable: none. Index version: v0.
```

- Trail rows in time order within each video; videos ordered by first appearance.
- **Search span** = sum of appearance ranges in that video. It comes from search hits,
  and usually only one or two frames per appearance were viewed, so label it
  "≈ … (search span)", not screen time.
- If timestamps are epoch times (≥ 1e12, see vmodal-find reference), sort the trail as
  one timeline across videos and show dates.
- Description mode: the trail holds PASS appearances. Group PARTIAL ones by reason
  ("white taxi, not red" × 8) in the "Close, but not matching" table, at most 5 rows.
- Identity mode: the trail holds SAME and LIKELY SAME (marked); give the counts of
  DIFFERENT and DESCRIPTION ONLY in the footer, and list them only if the user asks.
- An empty trail is a valid answer. Say what was searched and why it stopped.
