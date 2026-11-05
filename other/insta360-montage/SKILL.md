---
name: insta360-montage
description: Edit a video montage straight from raw Insta360 .insv recordings with ffmpeg, no Insta360 Studio, proposed by default as a vertical Instagram Reel (1080x1920, 30 fps, <= 40 s). Claude calibrates the camera mount, reviews the whole session from the .lrv proxies, finds every action with a motion analysis, lets the user pick from numbered candidate clips, then renders the chosen ones from the full-res .insv with a rider-locked horizon. Use when the user has Insta360 (X-series) footage on the camera or SD card and wants a reel, a highlight, a montage or "the jumps" from a session.
---

# Video montage from raw Insta360 footage

Everything runs locally with `ffmpeg`/`ffprobe` (Homebrew) and `python3` (stdlib only). Scripts live in
the `scripts/` folder of this skill's base directory (`~/.claude/skills/insta360-montage/` when installed
by install.sh; `$SK` below is that `scripts/` folder). Work in the session scratchpad (`$S`).
Read the card **read-only**: never write to or delete anything on the camera.

The flow: brief → calibrate the mount → find every action → the user picks clips from a numbered
candidate reel → assemble once → approval → save and cleanup. Iterate on the clip selection, never
on full renders.

## 0. Brief — ask before touching the footage (one message)

1. **Camera folder** (e.g. `/Volumes/Untitled/DCIM/Camera01`) and camera model. Check the card is mounted.
2. **What to show**: jumps, flying (foil up, no spray), tacks/gybes, a specific moment they remember
   ("my wing was flipped and filming another rider"), a session opener/ending?
3. **What to exclude**: crashes, pumping/waiting/standing, faces, other riders, and for a brand or
   sponsor reel, other brands' gear (a rider with a competitor's wing must not appear, even in the
   background).
4. **Length** (Instagram: <= 40 s is a safe target), **slow motion** on jumps (yes by default), music (none: natural sound, add a track in the app).
5. Can the card stay plugged in? The proxies (~2.4 GB per 30 min) can be copied locally for the
   review; the **final render needs the .insv on the card**. Ask to plug it back in when it's time.
   Read the card through the camera **one file at a time**: parallel reads over USB stalled at
   ~0.1 MB/s. If copying is slow, ask the user to copy the proxies in Finder (that was faster).
6. Cover: offer to export the best frame as a 1080x1920 JPG (Instagram: Edit cover > Add from camera roll).
7. **Where the approved reel goes**: a folder, or the Photos library on macOS (section 8).

Defaults that held up on review (wingfoil session, X6 mounted on the wing looking at the rider):
- Action only unless the brief says otherwise: flying, jumps, tacks. Pumping (board slapping the
  water, spray), waiting on the wing, walking on the beach and faces to the camera get cut.
- Slow motion starts at the **loading before the pop** and returns to real time **right after
  the landing**; the flight itself is short (0.5-1.5 s), so 0.5x on ~1.5-2 s of source is right.
- **Wider** on the rider (sg 140x190), **tighter** on distant subjects (sg 55x90 with a pan).
- Verify every cut against the exclusions frame by frame (2 fps sheet): an excluded wing or rider
  can enter the background in the last frames of a shot.

## 1. Probe the files

```zsh
zsh $SK/probe.sh <camera dir>
```

- `.insv` (X6): **two separate 1920x1920 HEVC fisheye streams** at 60 fps + AAC, ffmpeg reads it directly.
- `.lrv` proxy: **both lenses side by side** (2048x1024, 30 fps, 1 s keyframes) — not stitched. Same
  audio. Use it for every review step; keyframe-only decoding makes 1 fps passes I/O bound (~1 min/file).
- **The .insv and .lrv timelines are offset** (0 to ~0.55 s, constant within a file, different per file).
  Measure it from the audio; the renderer applies it in full mode:
  `python3 $SK/sync_offset.py --write $S/sync.txt <camera dir> $PROXY_DIR` (needs the card; ~1 min per
  file; it warns if the offset is not constant).
- New camera model: run `zsh $SK/check_layout.sh <insv> <lrv> 600 $S/layout.jpg` and read it; the
  `.insv` stream holding the rider lens goes in `INSV_FRONT` in `lens.sh`. Then calibrate the lens FOV on a
  frame with a distant textured background: `zsh $SK/stitch_cal.sh <insv> <t> 186 190 193 196 200` and put
  the minimum in `lens.sh` (193 on the X6, also verified visually).

Copy the proxies locally if the user wants to unplug (`~/Movies/insta360_proxies_tmp/`), verify one
checksum. They go in the cleanup (section 8).

## 2. Calibrate the mount — before any other review

The camera barely moves during a session, so its position and angle are measured once and used for every
clip. It usually sits on the wing's central strut, looking at the rider; it may one day be on the central
batten, at an extreme position, so never assume: measure.

```zsh
zsh $SK/mount_check.sh $PROXY_DIR $S/mount.jpg     # 3 equirect frames per recording, 45-degree grid
```

Read it and find the rider on every frame: x → yaw = (x/W − 0.5)·360, y → pitch = (0.5 − y/H)·180, the
centre is yaw 0 pitch 0. Then confirm the framing with `frame.sh` (sg, roll 180) and adjust until body,
board and wing fill the frame. Write `$S/mount.env`:

```
RIDER_YAW=0       # 0 = rider in the right half of the proxy, 180 = left half (camera turned round)
RIDER_PITCH=30    # 30 on the usual mount; 50 worked with the camera turned round
RIDER_ROLL=180    # static roll that shows the rider upright on review views
```

Pass `MOUNT=$S/mount.env` to every script below (`lens.sh` loads it) and use the same yaw and pitch in
`frame.sh`, `vstrip.sh` and the shot lists. If the rider is not at the same place on every frame, the
camera moved: use one mount file per recording. On a new mount position, check that `auto_roll.py` still
finds the rider (section 5).

## 3. Map the session (coarse pass)

```zsh
zsh $SK/coarse_sheets.sh $PROXY_DIR $S/coarse 15
```

Read every sheet. Note: setup, riding stretches, falls (green underwater frames), long swims, the wing
flipped on the water (sky + horizon, camera at water level), other riders, the ending. Rider upside down
in the equirect is normal (camera looks down from the wing).

## 4. Find every action (motion analysis, then sort)

Eyeballing 1 fps thumbnails misses 2-second jumps. Instead:

```zsh
MOUNT=$S/mount.env zsh $SK/motion.sh $PROXY_DIR $S/motion     # background, ~14 min per 30 min file
python3 $SK/peaks.py $S/motion/m003.txt                         # every peak above mean + 1 std, >= 4 s apart
MOUNT=$S/mount.env zsh $SK/peak_strips.sh $PROXY_DIR $S/peaks 003 <t1> <t2> ...   # 8-frame rows, 5 per sheet
```

Review **all** the peaks of every recording, not a top N: on one test session every jump sat beyond
the 40 strongest peaks.

Sorting the peaks: tacks/gybes = horizon sweeps around, rider passes under the wing; crash = splash then
green; **jump** = crouch/load, board lifts toward the camera, rider tucked right under the wing with the
board out of frame, landing splash. Pumping also peaks (spray, crouch) but the board stays on the water.
Confirm each candidate in the final framing at 5-10 fps (yaw and pitch from `mount.env`):

```zsh
zsh $SK/vstrip.sh $PROXY_DIR $S/vstrips 003 921 6 5 0 30 120 jump1
```

Clean **flying** stretches are the calm 1 fps runs between peaks (board steady, no white water).
A flipped wing filming another rider: locate the rider on the equirect sheet (x -> yaw: `(x/W-0.5)*360`),
it moves fast, so use a pan.

## 5. Framing: the rider lens, stereographic, rider-locked

- The rider is at the calibrated `RIDER_YAW` / `RIDER_PITCH` (section 2).
- Projection `sg` (stereographic) 140x190 for the rider: whole body, board and wing without stretching.
  55x90 (+ pan) for a distant rider. Test with `frame.sh`, compare several with `hstack`.
- **Roll changes with every tack and with how the wing is held** — do not hand-tune it. `roll = auto`
  measures the rider's orientation on the proxy every 0.5 s (`auto_roll.py`: the rider is the only large
  dark region and always hangs away from the handle) and counter-rotates the frame, so the rider stays
  upright while the world turns. This made tacks and jumps usable. Check
  `MOUNT=$S/mount.env python3 $SK/auto_roll.py <lrv> <t>` prints `dark_px` > 1500: it relies on a
  dark wetsuit and deck pad, so check it first with light-coloured gear.
- Pans use an equirect horizontal shift (v360 `sendcmd` was unreliable). Rotations use a 2720 px square
  render at `SQ_FOV` (calibrated so scale matches the static framing) then a centred 1080x1920 crop.
- **Stitching**: the renderer never uses v360's `dfisheye` input for output — with a 193° lens it overlaps
  both lenses, which duplicates anything near the seam (legs, board tail) and draws an arc across the sky.
  Each lens is projected to equirect on its own, the back lens gets a per-shot RGB gain measured in the
  overlap (`stitch_gain.py`), and the two are blended with a 13° feather mask (`lens.sh: stitch_graph`).
  Not optical-flow stitching like Studio, but the seam is invisible on water/sky and soft on close objects.
  The review tools (`frame.sh`, `vstrip.sh`, `peak_strips.sh`) still use the fast `dfisheye` path, so
  duplicated limbs on a review sheet are a review artefact, not a reason to drop a shot.
  Cost: ~15 s of render per second of source at full res (~10 min for a 40 s reel).
  Known limitation: a slight geometric offset and colour difference can remain at the seam (parallax,
  one shared FOV for both lenses, a single RGB gain). Next steps if the user wants better: calibrate each
  lens's centre and FOV separately, match colour with a curve instead of a gain.

## 6. Candidate clips: the user picks, nothing is assembled yet

Turn the best moments found in section 4 into numbered candidates: every jump, the cleanest tacks and
flying stretches, anything the brief asked for. Write them in `$S/candidates.txt` in the shot-list format
of `render_reel.sh` (times are **proxy** seconds), each line ending with a `# <n> <type> <seconds>s`
label. A slow-mo jump is three lines (real / 0.5x / real) sharing one label.

```
# file start dur yaw pitch roll speed [pan_to] [h_fov] [v_fov]
003 922.0 0.6 0 30 auto 1          # 1 jump 5.4s
003 922.6 3.8 0 30 auto 0.5        # 1 jump 5.4s
003 924.5 1.0 0 30 auto 1          # 1 jump 5.4s
004 310.0 3.5 0 30 auto 1          # 2 flying 3.5s
004 469.5 4.5 -130 3 0 1 -22 55 90 # 3 rider 4.5s
```

```zsh
LABEL=1 MOUNT=$S/mount.env MODE=proxy PROXY_DIR=... zsh $SK/render_reel.sh $S/candidates.txt $S/candidates.mp4
zsh $SK/sheet.sh $S/candidates.mp4 $S/candidates_sheet.jpg     # read it: exclusions, upright
zsh $SK/preview.sh $S/candidates.mp4 $S/candidates_preview.mp4  # < 30 MB, send with SendUserFile
```

Send the preview with the list (number, type, duration), say which clips you'd keep and in what order,
and ask which to keep. Every answer is a new selection, not a new render: reply with the clips kept, the
order and the total length, and repeat until the user says the selection is good. If a pick goes against
what works (a weak hook, past 40 s, a shot that shows an exclusion), say so plainly; the user decides. Render a new candidate reel only when the user asks for
moments that are not in it.

Order that worked: best jump first (hook), 3.5 s flying shots, tacks 5 s, alternate, end on a clean
flying shot, <= 40 s total.

## 7. Assemble once, cover, deliver

Copy the chosen candidates' lines into `$S/shots.txt` in the agreed order. With the card plugged in and
`sync.txt` written, render at full res:

```zsh
MOUNT=$S/mount.env MODE=full PROXY_DIR=... CAM_DIR=<camera dir> zsh $SK/render_reel.sh $S/shots.txt $S/reel_final.mp4   # ~10 min, run in the background
zsh $SK/sheet.sh $S/reel_final.mp4 $S/final_sheet.jpg    # read it: exclusions, upright, cut points
```

Cover: pick the apex frame (proxy time), then
`MOUNT=$S/mount.env PROXY_DIR=... CAM_DIR=... zsh $SK/cover.sh $S 003 923.85 0 30 auto $S/cover.jpg`
(blended stitch, rider upright, 1080x1920). Keep the subject centred (Instagram crops the grid preview
to 4:5).

Deliver: `~/Movies/reel_<subject>_final.mp4` (over 30 MB: give the path, send a `preview.sh` copy),
`~/Movies/reel_<subject>_cover.jpg`, the shot list in words with timings, the sync offsets used. A change
to a cut (trim, slow-mo window) edits `shots.txt` and renders again.

## 8. Once the user approves: save, clean up

Only once the user says the **final** reel is good (not the selection, and not while asking for
another version):

1. **Save it where the brief said.** For the Photos library (macOS, needs the `video-montage` skill):
   `zsh <video-montage skill folder>/to_photos.sh <final.mp4> <cover.jpg>` (the folder is
   `~/.claude/skills/video-montage/`, or the video-montage plugin's folder). It saves with "Add
   Photos Only" access and deletes the local copies once Photos confirms. Then tell the user both are in
   Recents: no script can write to a shared album, so adding them to one is theirs to do.
   Never read, list or export anything from the Photos library; the skill only asks for write access.
2. **Offer to delete the working files:** the local proxies (`~/Movies/insta360_proxies_tmp/` or
   wherever they were copied), and the scratchpad sheets, strips, motion data, candidate reels and
   renders. Delete them after a yes, or straight away if the user said they never need to be asked.

Look at each target before deleting it, never touch the camera card, and report what was deleted and
how much space it freed.

If the session taught something this skill should know (a fix, a camera quirk, a user correction),
propose the exact change to the user and edit the skill only after they say yes.
