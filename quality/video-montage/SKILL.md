---
name: video-montage
description: Edit a short video montage from a folder of phone videos with ffmpeg, proposed by default as a vertical Instagram Reel (1080x1920, 30 fps, H.264). Claude reviews every clip visually, proposes numbered candidate clips for the user to pick, then assembles the montage once, verifies it frame by frame and delivers. Use when the user asks for a Reel, a short vertical edit, a highlight video, or a montage from several clips.
---

# Video montage from a folder of clips

Everything runs locally with `ffmpeg` / `ffprobe` (Homebrew). No plugin or MCP is needed. The scripts are in this
skill's base directory (`~/.claude/skills/video-montage/` when installed by install.sh; `$VM` below).

## Inputs to get from the user

1. **Folder path** of the exported videos.
2. **Brief**. Ask these before cutting, in one message, unless already answered:
   - Which Reels to make: **brand** (a sport, a sponsor, gear), **personal/chill**
     (friends, family, places), or both from the same footage ("two in one").
   - Who appears, who must not appear.
   - Falls and crashes: excluded by default, but the user sometimes wants them
     (a big jump that ends in a fall can be the hook). Ask.
   - Which moment they consider the best, if they already know it.
   - Target length per Reel.
   - Where the approved Reel goes: a folder, or the Photos library on macOS
     (step 7).
3. Optional music file. If none, leave natural sound and tell the user to add a
   track in the Instagram app (also avoids rights issues).

## Two-in-one pattern (default when both are wanted)

- **Brand Reel**: max 20 s. Viewers leave in the first seconds, so the single
  best shot goes FIRST, no scene-setting opener. Only the athlete, only clean or
  spectacular action, 4 to 6 s per shot, end on the second-best shot.
- **Chill Reel**: 30 to 45 s. Places, people, chilling, with two or three
  action shots as peaks. Falls allowed if the user says so; low-res family clips
  acceptable when they carry the moment.
- Both are built from separate shot-list files with the same `build.sh`.

If the user drags items from Photos, what arrives are JPEG thumbnails, not the
movies. Ask them to export: Photos > select > File > Export > **Export Unmodified
Original** into a folder. Videos from an **iCloud shared album** export at
640x360; only the phone that recorded them has full quality. Flag this and prefer
full-resolution clips.

## Workflow

### 1. Inventory

```zsh
cd <folder>
for f in *.MOV *.mp4(N); do
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  r=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=p=0 "$f" | head -1)
  rot=$(ffprobe -v error -select_streams v:0 -show_entries stream_side_data=rotation -of csv=p=0 "$f" | tr -d '\n')
  c=$(ffprobe -v error -show_entries format_tags=creation_time -of csv=p=0 "$f")
  printf "%s\t%.1fs\t%s\trot=%s\t%s\n" "$f" "$d" "$r" "$rot" "$c"
done | sort -t$'\t' -k5
```

Group clips by resolution. Report the split to the user if many are low-res.

### 2. Contact sheets (one per clip, timestamped)

```zsh
S=<scratchpad>; mkdir -p $S/sheets
for f in *.MOV; do n=${f%.MOV}
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  nf=$(python3 -c "import math;d=$d;print(min(12,max(6,math.ceil(d/3))))")
  ffmpeg -v error -y -i "$f" -vf "fps=$nf/$d,scale=-2:400,drawtext=text='%{pts\:hms}':fontsize=28:fontcolor=yellow:box=1:boxcolor=black@0.6:x=8:y=8,tile=4x3" -frames:v 1 "$S/sheets/$n.jpg"
done
```

Read every sheet with the Read tool, full-resolution clips first. Note per clip:
what it shows, who is in it, stable vs. wobbly sections, falls, spray on the
lens, usable in/out points.

### 3. Candidate clips: the user picks, nothing is assembled yet

Turn the best moments from step 2 into numbered candidates in
`$S/candidates.txt`, one per line, `clip start duration`, ending with a
`# <n> <what> <seconds>s` label. Then render them as one labelled reel:

```zsh
LABEL=1 SRC=<folder> zsh $VM/build.sh $S/candidates.txt $S/candidates.mp4
ffmpeg -v error -y -i $S/candidates.mp4 -vf scale=720:1280 -c:v libx264 -crf 24 -c:a aac -b:a 128k -movflags +faststart $S/candidates_preview.mp4
```

Check it for excluded moments (step 5 sheet), send the preview with
SendUserFile plus the list (number, what, duration), say which clips you'd
keep for each Reel and in what order, and ask which to keep. Every answer is a
new selection, not a new render: reply with the clips kept, the order and the
total length, and repeat until the user says the selection is good. If a pick
goes against what works (a slow opener on a brand Reel, past the target
length), say so plainly; the user decides. Render a new candidate reel only
when the user asks for moments that are not in it.

Editorial rules that worked well:

- Brand Reel: best shot first, no opener, 20 s max.
- Chill Reel: open with 2 to 3 short scene-setting shots (2 to 3 s each), then
  alternate life moments and action.
- Action shots 4 to 6 s each, cut where the subject is stable and in control.
- Prefer full-resolution clips; use a 360p clip only when nothing else shows a
  needed moment, and keep it short.
- Never include a moment the user excluded, even between sampled frames: verify
  in step 5.
- End on the strongest, cleanest shot. Trim before any spray hits the lens.
- Target 30 to 50 s unless told otherwise.

### 4. Build the Reel once the selection is approved

Copy the chosen candidates' lines into one shot-list file per Reel in the
scratchpad (`clip start duration`, clip name without extension), in the agreed
order. Then:

```zsh
SRC=<folder> zsh $VM/build.sh <scratch>/brand.txt <folder>/reel_brand.mp4
```

It renders each shot as its own normalised segment (crop to fill 1080x1920,
30 fps, stereo 48 kHz) then concatenates with fade in/out and loudness
normalisation. Rotation metadata is applied automatically by ffmpeg.

### 5. Verify the draft frame by frame

```zsh
ffmpeg -v error -y -i $S/reel_draft.mp4 -vf "fps=1,scale=-2:420,drawtext=text='%{pts\:hms}':fontsize=26:fontcolor=yellow:box=1:boxcolor=black@0.6:x=8:y=8,tile=8x6" -frames:v 1 $S/draft_sheet.jpg
```

Read it. Fix any shot that shows an excluded moment, then re-run the script.

### 6. Deliver

Copy the final to the source folder (for example `reel_<subject>.mp4`). Files
over 30 MB cannot be sent through SendUserFile; just give the path. Report the
shot list in words, the duration, and any quality caveat.

### 7. Once the user approves: save, clean up

Only once the user says the **final** reel is good (not the selection, and not
while asking for another version):

1. **Save it where the brief said.** For the Photos library (macOS):
   `zsh $VM/to_photos.sh <reel.mp4>...`. It
   saves with "Add Photos Only" access and deletes the local copies once Photos
   confirms. Then tell the user the reels are in Recents: no script can write
   to a shared album, so adding them to one is theirs to do. Never read, list
   or export anything from the Photos library; the skill only asks for write
   access.
2. **Offer to delete the working files:** contact sheets, `segs_*` folders,
   candidate reels, drafts and draft sheets in the scratchpad, plus the source
   clips in the folder **only if** they are copies exported from Photos (the
   originals stay in the library). Delete after a yes, or straight away if the
   user said they never need to be asked. If the clips may be the only copy
   (camera import, AirDrop, a drive), always ask first.

Look at each target before deleting it, then report what was deleted and how
much space it freed.

If the session taught something this skill should know (a fix, a user
correction), propose the exact change to the user and edit the skill only after
they say yes.

## Iterating

Changes to what is in the Reel ("no family", "more shots like the last one") go
through the candidate selection (step 3). Changes to a cut ("shorter", a trim,
the order) edit the shot-list file, re-run `build.sh` and re-verify (step 5).
