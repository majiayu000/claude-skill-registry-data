---
name: recipe-video
description: "Recipe and food video editor for Claude: turns cooking footage (overhead steps, pours, sizzles, the finished dish) into a 30-60 s vertical recipe reel that opens on the money shot, shows ingredients with readable quantities, speeds through the process and ends on the taste, plus a longer YouTube version. Use when the user says 'edit my recipe video', 'cooking reel', 'food short', 'Tasty-style video', 'make my dish look delicious', or hands over kitchen footage. Runs on video-studio-core (timeline, speed ramps, captions, warm grade, sizzle audio, deliver, QC)."
license: MIT
---

# Recipe Video

Make them hungry in the first second, then make the recipe impossible to get wrong.

- **Best for:** recipe reels, food creators, restaurant dishes, meal prep, cocktail videos
- **Inputs:** overhead/step clips (one per step ideally), the finished-dish shot, optional voice or talking head, ingredient list with quantities
- **Default skin:** `tutorial-steps` · alternatives `sticker-pop`, `countdown-list`, `paper-cut`
- **Formats:** 9:16 master, 4:5 and 1:1 feed, 16:9 long-form
- **Durations:** reel 30-60 s, long-form 5-12 min
- **Genre preset:** `--genre recipe-video`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = that folder, `SKILLS` = the skills folder.
- First run: `python CORE/scripts/check_env.py`.
- Ask for: the exact ingredient list with quantities and units, oven temperature and times, allergens, the dish name.
  Quantities, temperatures and allergens on screen are checked against that list, never guessed from the audio.
- Sponsored ingredient or brand: add a disclosure (`chip` "Paid partnership") and say it in the caption text.

## How a pro cuts this

**Structure (reel, % of length)**

| beat | % | what goes here |
| --- | --- | --- |
| money shot | 10 | the finished dish: cheese pull, cut-through, pour, steam, in the first second |
| ingredients | 15 | quick cuts or a flat-lay with a checklist of quantities |
| steps | 55 | one step per shot, fast-forward the waiting, verbs on screen |
| final reveal / taste | 15 | plating, the bite, the reaction |
| CTA | 5 | "save this", recipe link |

**Pacing.** ASL 1-2.5 s; visual change every 2 s. Speed process shots 2-4x (stirring, kneading, simmering), keep
pours and sizzles at real speed or slow (0.5x) for appetite.

**Cut rules.**
- Cut on action: hand enters, ingredient drops, pan tilts. Match cut bowl-to-bowl between steps.
- Hold each quantity on screen >= 1.5 s; never cover the food with text.
- Jump cuts are native here; keep one camera angle per step so the viewer stays oriented.

**Transition grammar.** Cuts on the beat, whip between big phases, flash only at the reveal. No dissolves.

**Music and sound.** Upbeat bed ~-20 dB, ducked under voice. Food sound is the star: keep sizzle, crunch, pour and
chop audible (`audio: "keep"` on those clips, music dips). SFX medium (~10/min): `pop` on ingredient cards,
`whoosh-short` on whips, `ding` when it comes out of the oven.

**Colour.** `food-pop` (rich warm reds, oranges, yellows) at 0.6-0.8, or `warm`; keep greens fresh, never neon.

**Captions.** Word-pop 1-3 words, uppercase, <= 17 cps (`"preset": "hormozi"` or the skin's), ingredient names as
`keywords`. Quantities go in cards, not in fast captions.

**What the client judges.** Appetite appeal and readable quantities.

**Common mistakes.** Opening on raw ingredients; text over the food; quantities too fast to read; cold grey grade;
music drowning the sizzle; missing an allergen; oven temperature wrong.

## Make the edit

Clips without speech (most recipe footage): assemble in step order with a hand-written spec.

```bash
python CORE/scripts/timeline.py auto steps/ --work rv --mode montage --music bed.wav --duration 45 --format 9:16 --dry-run
#   edit rv/timeline_spec.json: money shot first, steps in order, "speed": 3 on waits,
#   "speedRamp" into the pour, "audio": "keep" on sizzle clips (montage mutes everything by default)
python CORE/scripts/run.py - --timeline rv/timeline_spec.json --style SKILLS/tutorial-steps --genre recipe-video --format 9:16 --no-cut --work rv --stop-after plan
python CORE/scripts/render.py rv/plan.json --frames 0.5,5,15,30,42
python CORE/scripts/render.py rv/plan.json
python CORE/scripts/finish.py rv/plan.json --platform reels
```

Talking-head recipe (voice explains): `python CORE/scripts/run.py cook.mp4 --style SKILLS/tutorial-steps --genre recipe-video --format 9:16 --smart-cuts --retakes --broll steps/ --work rv2 --stop-after broll`
(name step clips after what they show: `garlic-chopping.mp4`). Long-form: same footage, `--format 16:9`, a calmer
`--max-gap 0.45`, and keep the full method.

## Refine the plan

- **Money-shot hook:** first clip is the dish; a `text` hook in the first 1.5 s ("15-minute garlic noodles").
- **Ingredients:** `{"type": "checklist", "title": "You need", "items": [{"text": "200 g noodles", "at": 4.2}, {"text": "6 cloves garlic", "at": 5.0}]}`
  with every quantity from the user's list.
- **Step labels:** `{"type": "tile", "text": "Step 2: Fry the garlic", "start": 11, "end": 14, "in": "pop"}`; temperatures as `chip`s.
- **Timer for waits:** `{"type": "timer", "from": 10, "label": "minutes", "start": 20, "end": 22}` (it counts seconds of
  screen time; label it as the real wait).
- **Captions:** keep one `captions` element (delete it for music-only footage, and clear `words` if Whisper heard lyrics).
- **Audio:** music-only assembly: `"audio": {"platform": "reels", "voice": false}`. With voice:
  `"music": {"src": "bed.wav", "under": 18, "duck": "speech-aware", "fitTo": "beats", "endButton": true}`.
- **SFX:** `"sfx": [{"t": 4.1, "kind": "pop", "gain": 0.35}, {"t": 30.2, "kind": "ding", "gain": 0.4}]`.
- **Colour:** `"color": {"look": "food-pop", "intensity": 0.7}`, `"finish": {"sharpen": 0.3}`.
- Check every auto `counter` (value and label match what is said); delete ones that make no sense.
- Check B-roll `cutaways` land on the right step in the `--frames` stills.
- **Footage clean-up (video, before the spec):** handheld close-ups and kitchens under LED/fluorescent light: `python CORE/scripts/prep.py step03.mp4 --work fix/step03 --stabilize --deflicker`, then use `fix/step03/source.mp4` in the spec. `--stabilize` = vidstab (crops ~6% at the edges), `--denoise light|strong` = video noise, `--deflicker` = mains-light flicker. Only on clips that need it. An overhead rig is already stable. Talking-head run: the same flags work on `run.py`.

## Deliver

```bash
python CORE/scripts/deliver.py rv/plan.json --to reels,tiktok,shorts,pinterest,facebook --out-dir rv/deliver
python CORE/scripts/qc.py rv/deliver/final_reels.mp4 --plan rv/plan.json --platform reels --strict
```

Also hand over a clean (no captions) version, a cover frame (`thumb_cover_1080x1920.png`) on the money shot, and the
full written recipe for the post text.

## Check before delivering

- Every quantity, temperature, time and allergen matches the user's recipe list.
- Money shot by 1 s; no text over the food; quantities on screen >= 1.5 s.
- Sizzle and crunch audible over the music; `qc.py` passes (-14 LUFS, -1 dBTP, safe zones).
- Colour looks appetising but true (no orange skin, no neon greens).

## Example requests

- "Make a 45-second recipe reel from these clips, start with the cheese pull."
- "Add the ingredients with quantities on screen and speed up the simmering."
- "Cut a long YouTube version and a vertical one from the same cook."
