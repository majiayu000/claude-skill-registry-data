---
name: real-estate-tour
description: "Real-estate tour editor for Claude: turns gimbal, drone and phone clips of a property into a 60-120 s walk-through ordered like a buyer's visit (exterior, entry, living, kitchen, bedrooms, amenities), with price/beds/baths cards, a branded version, an unbranded MLS version and a 20-30 s vertical reel. Use when the user says 'edit my listing video', 'property tour', 'real estate reel', 'MLS video', 'house tour for Instagram', 'Airbnb / rental walkthrough', 'make this home look bright', or hands over room-by-room clips. Runs on video-studio-core (timeline, colour, deliver, QC)."
license: MIT
---

# Real Estate Tour

A calm, bright walk through the home in the order a buyer would walk it, with the facts on screen and every version the agent needs.

- **Best for:** listings, rentals, holiday homes, new-build show homes, commercial spaces
- **Inputs:** one clip per room (gimbal glides, drone), optional photos, agent logo/contact, price + beds + baths + area, licensed music
- **Default skin:** `minimal-mono` · alternatives `frame-studio`, `product-spotlight`, `swiss-poster` (needs `--no-matte`)
- **Formats:** 16:9 branded master, 16:9 unbranded (MLS), 9:16 reel
- **Durations:** tour 60-120 s (MLS often 45-90 s), reel 20-30 s of 5-7 clips
- **Genre preset:** `--genre real-estate-tour`

## Before you start

- Needs **video-studio-core** in the same skills folder (`CORE`); `SKILLS` = the skills folder.
- First run on a machine: `python CORE/scripts/check_env.py`.
- Get the facts in writing: address, price, beds, baths, area, agent name, phone, brokerage, licence number if the
  market requires it. Every number on screen must match the listing.
- Ask whether the MLS allows branding (most need an **unbranded** version: no names, phones, logos, URLs).
- Check the footage for people, family photos, house numbers of neighbours, documents, and screens; leave them out.

## How a pro cuts this

**Structure (tour, % of length)**

| beat | % | shots |
| --- | --- | --- |
| exterior / drone | 15 | establishing drone or street approach, title card with address |
| entry | 10 | front door opening, hallway glide |
| living | 20 | widest angle first, then a detail (fireplace, view) |
| kitchen | 15 | wide, island, one appliance or finish detail |
| bedrooms | 20 | primary suite first, then the rest; bathrooms after their bedroom |
| amenities | 10 | garden, pool, garage, view, neighbourhood |
| outro + contact | 10 | hero exterior (dusk if you have it), agent card |

**Pacing.** ASL 2.5-5 s. Each room gets one wide (3-5 s) plus at most one detail. Total 60-120 s. Never more than 3
shots of one room.

**Cut rules.**
- **No jump cuts.** Each shot is a full glide with a clean start and end. Cut on the move, mid-glide, and let the next
  shot continue in the same direction (left-moving into left-moving).
- Speed-match glides: a slow push followed by a fast pan looks broken. Use `"speed"` in the spec to even them out.
- Straight verticals: walls must not lean. Reject tilted shots instead of using them.
- Order follows the walk; never jump back to a room you left.

**Transition grammar.** Short dissolves (0.4-0.6 s) between rooms, straight cuts inside a room, one dip to black before
the agent card. No whips, glitches or flashes.

**Music and sound.** Upbeat, light, licensed bed that leads (bed about -18 dB, no ducking unless there is a voice-over).
Cut to length on bars and end on a hit (`fitTo: "beats"`, `endButton: true`). Room sound muted. SFX none.

**Colour.** Accurate and bright: `real-estate-bright` at 0.5-0.7, or `clean-commercial`. Whites must look white, not
blue or yellow. Open the shadows; windows can clip a little but not the whole frame.

**Captions / text.** No creator captions. Facts as cards: address + price + beds/baths/area at the open, room chips
("Chef's kitchen") as a `chip` at the lower left for 2 s, agent `card` at the end. Text lives in the branded version only.

**What the client judges.** The space looks big and bright, the flow makes sense, the numbers are right, the MLS
version passes the board's rules, and they get a vertical for Instagram.

**Common mistakes.** Jump cuts inside rooms; tilted verticals; too many shots of one room; music that fades mid-phrase;
branding left in the MLS version; portrait video for YouTube; wrong price on screen.

## Make the edit

Write the tour as a timeline spec so the room order is yours (auto montage orders by file time and cuts on every beat,
which is too busy for a tour):

```json
{"format": "16:9", "fps": 30,
 "clips": [
  {"src": "rooms/exterior.mp4", "in": 0, "out": 5, "audio": "mute"},
  {"src": "rooms/entry.mp4", "in": 0.5, "out": 3.5, "audio": "mute", "transition": {"type": "fade", "dur": 0.5}},
  {"src": "rooms/living.mp4", "in": 0, "out": 4.5, "audio": "mute", "transition": {"type": "fade", "dur": 0.5}},
  {"src": "rooms/kitchen.mp4", "in": 0, "out": 4, "audio": "mute", "speed": 1.2, "transition": {"type": "fade", "dur": 0.5}},
  {"src": "rooms/bedroom.mp4", "in": 0, "out": 4, "audio": "mute", "transition": {"type": "fade", "dur": 0.5}},
  {"src": "photos/garden.jpg", "dur": 3, "transition": {"type": "fade", "dur": 0.5}}
 ],
 "music": {"src": "music.wav", "volume": 0.8, "duck": false, "fadeOut": 1.5}}
```

```bash
python CORE/scripts/run.py - --timeline rt/tour_spec.json --style SKILLS/minimal-mono --genre real-estate-tour --format 16:9 --model base --work rt --stop-after plan
python CORE/scripts/render.py rt/plan.json --frames 1,5,8,12,15,19
python CORE/scripts/render.py rt/plan.json
python CORE/scripts/finish.py rt/plan.json --platform youtube
```

A `--timeline` spec sets every in/out point, so autocut is skipped (and this genre's preset has autocut off anyway).
Photos in the spec get a slow push-in (`"kenburns": false` to stop it). Agent voice-over as the soundtrack: add
`"voiceover": true` to the spec's `music` block (with the VO as `src`) and timeline.py transcribes it for captions. For a tighter music edit run
`python CORE/scripts/music_fit.py music.wav --duration 62 --out rt/music_fit.wav` first and use that file in the spec.

**Reel (9:16, 25 s).** Make a second spec with the 5-7 best shots, `"format": "9:16"`, 3-4 s each, and run it into
`--work rr --format 9:16`. Vertical crops of 16:9 glides lose the room: choose shots where the subject is centred,
or shoot vertical.

## Refine the plan

- **Audio is music only:** `"audio": {"platform": "youtube", "voice": false}` so the dialogue chain does not compress the song.
- **Colour:** `"color": {"look": "real-estate-bright", "intensity": 0.6}` and `"finish": {"grain": 0, "vignette": false}`
  (the skin may add grain, vignette or letterbox; remove them: buyers want the real room).
- **Opening card:** `{"type": "card", "kicker": "FOR SALE", "title": "14 Orchard Lane", "body": "4 bed · 3 bath · 2,450 sq ft", "start": 0.5, "end": 4.5, "in": "fade", "out": "fade"}`
  over the drone shot. A `titlecard` also works but is opaque full frame and hides the exterior.
- **Room chips:** `{"type": "chip", "text": "Chef's kitchen", "x": 200, "y": 960, "anchor": "left", "start": 11.2, "end": 13.5, "in": "maskUp", "out": "fade"}`.
- **Agent card:** `{"type": "card", "kicker": "Listed by", "title": "Jane Doe, Realty Co", "body": "+1 555 0100", "start": 17, "end": 20.5}`; add `"image": "logo.png"` if the skin shows it.
- **Unbranded MLS version:** copy the plan to `plan_mls.json` in the same folder, delete the agent card and any logo,
  keep the facts the board allows, set `"outputFile": "final_mls.mp4"`, then `finish.py rt/plan_mls.json`.
  (Plans use paths relative to their folder, so keep the copy next to `plan.json`.)
- `editor.py review rt/plan.json --genre real-estate-tour` complains about "no hook text" if the first card is late:
  the address card at 0.5 s is the hook.
- **Footage clean-up (video, before the spec):** handheld walkthroughs and LED/fluorescent interiors: `python CORE/scripts/prep.py kitchen.mp4 --work fix/kitchen --stabilize --deflicker`, then use `fix/kitchen/source.mp4` in the spec. `--stabilize` = vidstab (crops ~6% at the edges), `--denoise light|strong` = video noise, `--deflicker` = mains-light flicker. Only on clips that need it. Gimbal and drone shots need nothing.
- **Privacy:** blur house numbers, number plates, family photos and documents with `"blurs": [{"x": 1320, "y": 410, "w": 160, "h": 120, "start": 21.0, "end": 24.5}]` (output pixels, top-left box; `"pixelate": true` for a mosaic). One box per shot.

## Deliver

```bash
python CORE/scripts/deliver.py rt/plan.json --to youtube --out-dir rt/deliver --burn no
python CORE/scripts/deliver.py rt/final_mls.mp4 --to youtube --out-dir rt/deliver_mls --burn no --no-post
python CORE/scripts/deliver.py rr/plan.json --to reels,tiktok --out-dir rr/deliver --burn no
python CORE/scripts/qc.py rt/deliver/final_youtube.mp4 --plan rt/plan.json --platform youtube --strict
python CORE/scripts/qc.py rr/deliver/final_reels.mp4 --plan rr/plan.json --platform reels --strict
```

Name them `14-orchard-lane_tour_branded_16x9.mp4`, `..._tour_unbranded_mls_16x9.mp4`, `..._reel_9x16.mp4`. If the
MLS has a file-size cap, check the size in `deliver_report.md` and use `--to web-h265` for a smaller file.

## Check before delivering

- Contact sheet: verticals straight, rooms bright, nothing personal in frame, chips readable and inside the safe area.
- Every number (price, beds, baths, area, phone) matches the listing sheet, letter by letter.
- The unbranded file contains no name, phone, logo or URL anywhere (watch it end to end).
- Music ends on a downbeat; `qc.py` passes loudness and has no black or flash frames.
- Report: lengths of each version, the music credit, and which file goes where (MLS, YouTube, Instagram).

## Example requests

- "Here are clips of every room, make a 90-second listing video with the price and beds on screen."
- "I need the same tour without my branding for the MLS."
- "Cut a 25-second vertical reel of the best shots for Instagram."
