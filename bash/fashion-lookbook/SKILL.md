---
name: fashion-lookbook
description: "Fashion lookbook and outfit-reel editor for Claude: cuts runway, studio or street-style footage on the beat into a 15-60 s lookbook with outfit-change transitions, product tags and prices, true-to-garment colour, in 9:16, 4:5 and 16:9. Use when the user says 'make a lookbook video', 'outfit transition reel', 'new collection video', 'fashion reel for my brand', 'GRWM outfits on the beat', 'product tags on each look', or hands over model / outfit footage and a track. Runs on video-studio-core (timeline montage, beats, colour, deliver, QC)."
license: MIT
---

# Fashion Lookbook

Every look on the beat, every garment its true colour, every tag readable: a collection that sells.

- **Best for:** brand collection drops, boutique and D2C catalogue reels, stylists, outfit-transition creators, runway recaps
- **Inputs:** clips per look (walks, turns, details), product names / prices / SKUs, logo, licensed track
- **Default skin:** `soft-gradient` · alternatives `y2k-chrome` (add `--no-matte`), `swiss-poster` (add `--no-matte`), `minimal-mono`
- **Formats:** 9:16 master, 4:5 feed, 16:9 for the website / YouTube
- **Durations:** 15-60 s (3-8 looks)
- **Genre preset:** `--genre fashion-lookbook` (`python CORE/scripts/editor.py genre fashion-lookbook`)

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = that folder, `SKILLS` = the skills folder.
- First run: `python CORE/scripts/check_env.py`.
- Ask for: the look order, product names and prices (exact, with currency), the hero look, logo, the track (licensed),
  a reference photo of each garment under neutral light (for colour checks), and model release / consent.
- One folder of clips per look, named `look1-...`, `look2-...`; montage orders by file modification time, so check the
  order in the dry-run spec.

## How a pro cuts this

**Structure (% of length, 4 looks)**

| beat | % | what goes here |
| --- | --- | --- |
| look 1 | 25 | strongest silhouette first: full body, then 1-2 details, tag |
| look 2 | 25 | full body, movement (turn, walk), detail, tag |
| look 3 | 25 | same grammar, different energy |
| hero look + tag | 25 | the look the brand pushes most, held longer, logo + CTA ("Shop the drop") |

**Pacing.** ASL 0.8-2 s on the beat; full-body shots 1.5-2.5 s (the customer must see the fit), details 0.5-1 s. Change
outfit on a downbeat or a phrase change; inside a look cut every beat or every 2nd beat.

**Cut rules.** The outfit change is the event: hide it in a motivated transition (spin, hand over the lens, jump, walk
past the camera), cut on the action a third of the way in. Keep the model's position matched across an outfit change
(same framing, same spot) so the swap reads as magic.

**Transition grammar.** Cuts on the beat; one outfit-change transition family (match cut, whip or speed ramp) used
consistently; a dip to black only before the logo.

**Music and sound.** The track leads (no duck), cut on bar lines, ending on a hit. Optional fabric / heel foley, one
whoosh per whip.

**Colour.** Garment colour accuracy matters more than mood: e-commerce returns come from wrong colour. Use
`clean-commercial` or `high-key` lightly (0.3-0.5) or no look at all; correct white balance first. The preset's
`pastel` look is for editorial / brand-mood versions only, never the shop version.

**Captions.** None. Product tags (name, price) per look, small and inside the safe zone.

**What the client judges.** Garment colour accuracy, fit visible, rhythm, tags correct.

**Common mistakes.** A stylised grade shifting a red dress to orange; tags with wrong prices; outfit changes off the
beat; details only and no full body; text under the platform buttons.

## Make the edit

```bash
python CORE/scripts/timeline.py auto looks/ --work fl --mode montage --music track.wav --duration 30 --format 9:16 --dry-run
#   edit fl/timeline_spec.json: group shots by look, outfit changes on downbeats, add transitions
python CORE/scripts/run.py - --timeline fl/timeline_spec.json --style SKILLS/soft-gradient --genre fashion-lookbook --format 9:16 --no-cut --model base --work fl --stop-after plan
python CORE/scripts/render.py fl/plan.json --frames 1,7,14,21,28
python CORE/scripts/render.py fl/plan.json
python CORE/scripts/finish.py fl/plan.json --platform reels
```

Find the downbeats for outfit changes with `python CORE/scripts/beats.py track.wav --out fl/beats.json` (the montage
already cuts on beats; use `downbeats` to place the look changes and the tags). Outfit-change move in the spec:
`{"src": "look2-spin.mp4", "in": 1.2, "out": 2.4, "audio": "mute", "transition": {"type": "whip", "dur": 0.25}}` or a ramp
`"speedRamp": [{"at": 1.8, "rate": 0.4, "ramp": 0.3}]` on the spin.

## Refine the plan

- **Delete the `captions` element**, clear `words`, set `"audio": {"platform": "reels", "voice": false}`.
- **Colour (shop version):** `"color": {"auto": true, "wb_strength": 1.0, "look": "clean-commercial", "intensity": 0.35}`;
  editorial version `"look": "pastel"` or `"cross-process"`. Compare against the garment reference photo with
  `python CORE/scripts/color.py preview fl/cut.mp4 --look clean-commercial --intensity 0.35 --correct --t 4 --out fl/check.png`.
- **Product tags:** `{"type": "tile", "text": "Linen Shirt Dress · ₹2,499", "x": 540, "y": 1380, "start": 3.2, "end": 6.4, "in": "maskUp", "out": "fade"}`,
  one per look, timed from the look's first downbeat to its last frame. Keep y between 10% and 80% of the height and
  clear of the right 12%. Use `callout` with `point` to tag a single item (bag, shoes).
- **Hero end:** logo `image` element and a `chip` "Shop the drop · link in bio" for the last 2-3 s.
- **SFX:** `{"t": 6.2, "kind": "whoosh-short", "gain": 0.35}` before each whip, nothing else.
- `python CORE/scripts/editor.py review fl/plan.json --genre fashion-lookbook`.

## Deliver

```bash
python CORE/scripts/deliver.py fl/plan.json --to reels,tiktok,pinterest,facebook --out-dir fl/deliver --burn no
python CORE/scripts/qc.py fl/deliver/final_reels.mp4 --plan fl/plan.json --platform reels --strict
```

`facebook` gives the 4:5 feed crop: check no tag is cut off. For the 16:9 website version build its own montage with
`--format 16:9` (a vertical master would get a blurred fill). Name files `brand_ss26_lookbook_v001_9x16.mp4`.

## Check before delivering

- Colour: every garment matches its reference photo (hold them side by side); whites are white.
- Tags: names, prices and currency exactly as the client wrote them; each tag on screen >= 1.5 s; safe zones respected
  in 9:16 and 4:5.
- Outfit changes on downbeats; each look shows the full body at least once.
- `qc.py` passes loudness and flash checks; the track ends on a hit.
- Tell the client the look order, the track credit and which version is the colour-accurate shop version.

## Example requests

- "Make a 30-second lookbook reel of our new 5 looks with name and price on each."
- "Outfit transition video on the beat, spin to change."
- "Same lookbook as a 16:9 for our website, keep the colours true."
