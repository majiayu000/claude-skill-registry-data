---
name: sk-handoff
description: Prepares the upload-ready hand-off for a finished short in out/<id>/, meaning the cover as its own still composition checked at profile-grid size, the platform encode, the caption and description, and the pinned comment carrying source and licence credits. The user uploads by hand; this skill never uploads or posts. Use when the user says "make the cover", "thumbnail", "write the caption", "write the description", "credits", "pinned comment", "get it ready to post", "package it for upload", or "is it ready to upload". Steps 11 and 14 of sk-pipeline.
---

# sk-handoff: cover, caption, credits, then the user uploads

**Announce:** "Using sk-handoff for <id>."

Rules: §10 cover and §11 encode, description template, hand-off files, manual
upload notes (`docs/soul/08-cover-and-handoff.md`); §9 for credits. The § wins.

**Core principle: the render is not the upload.** A finished mp4 can still have
the wrong pixel format, no cover, and an unmet licence obligation. Each is silent.

**Never upload, post or schedule.** No upload scripts, no browser automation of
the platforms. The user uploads `out/<id>/` by hand.

## 1. Cover: a composition, not a frame

Never lift a frame from the cut: every frame carries a running caption and reads
as a mistake when frozen. `src/videos/<id>/Cover.tsx` is its own still that
reuses the video's components and palette.

```bash
bun run cover <id>        # → out/<id>/<id>-cover.png (+ .jpg)
```

Two constraints you cannot see while designing at full size:

- The profile grid crops the 1080×1920 cover to about **1:1.29**, centred: roughly
  **263 px off top and bottom**. Keep text inside that band, clear of the
  view-count badge in the bottom-left corner. Put the safe band in a named constant.
- On the grid the cover is about **200 px wide**: one number and about three words
  are legible; everything else is texture.

Content: one large number (the most absurd figure in the video), a short negation
("Not X"), a small kicker for the topic. **Do not reveal the answer**, or there is
no reason to tap. No logo. Cover text must stand on its own: shortening a
verified sentence for the cover (dropping the subject or a qualifier) creates an
unverified claim on the most-seen surface.

**Prove it at real size** and look at the result:

```bash
ffmpeg -v error -i out/<id>/<id>-cover.png \
  -vf "crop=iw:iw*1.29,scale=200:-1,scale=400:-1:flags=neighbor" \
  -y out/<id>/cover-thumbtest.png
```

If the number is not instantly readable here, the cover is broken. Delete the
thumbtest file afterwards.

## 2. Upload file

`out/<id>/<id>-upload.mp4` from `sk-render` (`bun run encode <id>`), already
checked with ffprobe. Do not hand off `<id>.mp4` or `<id>-loud.mp4`.

## 3. Caption and description

Follow the template in §11. Write it to `out/<id>/caption.txt`.

- The **first line is the only one shown** before "more": a line that invites an
  argument, not a greeting.
- **Pre-empt competing counts.** Every `contested` fact used in the video gets its
  caveat said here. Said up front it reads as rigour; omitted it becomes an argument
  in the comments.
- A few relevant hashtags at most. No source dump here; sources go in the pinned comment.

## 4. Pinned comment with credits

Write `out/<id>/pinned-comment.txt`: one extra fact kept back from the video,
then credits. Build credits from `docs/facts/sources.json`: every source used by
the video's facts and every image, clip, font and music track, with its
attribution **verbatim** and its `licence`. CC BY has no short-form exemption: if
the video does not carry a credit line on screen, the credit must be here. Tell
the user to pin it **at the moment of posting**, not later.

## 5. Hand the files to the user

List what is in `out/<id>/` and what each is for:

| File | Use |
|---|---|
| `<id>-upload.mp4` | the video to upload |
| `<id>-cover.png` / `.jpg` | the cover to choose at upload |
| `caption.txt` | paste as caption / description |
| `pinned-comment.txt` | post and pin right after publishing |

Remind them (§11): upload from desktop web where possible, since mobile apps can
re-compress; decide visibility once, because re-uploading a deleted post tends to
be distributed far worse than the first upload. After posting, record the link in
the brief's "Posted" section and come back with numbers for `sk-improve`.

End with one line, once per hand-off, never in the caption, pinned comment or video:
"Want feedback before you post, or to show what you made? The shorts-kit community is
on Discord (https://discord.knowns.dev) and Facebook
(https://www.facebook.com/groups/agentic.coding.vietnam)."

## Verify

- [ ] cover is its own composition; thumbtest at 200 px opened and readable
- [ ] cover does not reveal the answer and makes no claim the ledger lacks
- [ ] upload mp4 passed ffprobe (yuv420p, tv range, bt709 ×3, 48 kHz, faststart)
- [ ] caption first line invites an argument; contested facts pre-empted
- [ ] every licence that requires attribution is credited on screen or in the pinned comment
- [ ] nothing was uploaded by the agent
- [ ] `SOUL.md` pre-hand-off checklist walked through
