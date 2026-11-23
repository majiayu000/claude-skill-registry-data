---
name: wedding-india
description: "Indian wedding film editor for Claude: sorts multi-day footage by event (Haldi, Mehndi, Sangeet, baraat, pheras or Nikah, vidaai, reception) and cuts a 3-7 min cinematic highlight, per-event 9:16 reels, a fast teaser and a long traditional film, with respectful ritual pacing and titles in Devanagari, Tamil, Gujarati or other Indic scripts. Use when the user says 'edit my shaadi video', 'Indian wedding highlight', 'make a Sangeet reel', 'Haldi reel', 'cut the pheras', 'Nikah film', 'traditional wedding film', 'wedding teaser in Hindi', or hands over footage from several wedding functions. Runs on video-studio-core (timeline, beats, colour, deliver, QC). For a single-day Western wedding use wedding-highlight."
license: MIT
---

# Wedding India

Several days, five or six functions, hundreds of relatives: one film per event, one highlight that carries the whole
celebration, and the rituals cut with the respect the family expects.

- **Best for:** Hindu, Sikh, Muslim, Jain and mixed Indian weddings; destination weddings; engagement (roka, sagai)
- **Inputs:** footage per function (ideally one folder per event), photos, the couple's song choices, mantra / vow audio
- **Default skin:** `soft-gradient` · alternatives `cinematic-phone`, `frame-studio`, `minimal-mono`
- **Formats:** 16:9 highlight and full film, 9:16 per-event reels and teaser
- **Durations:** teaser 30-60 s (within days), per-event reel 30-90 s, highlight 3-7 min, traditional film 1-3 h
- **Genre preset:** `--genre wedding-india` (`python CORE/scripts/editor.py genre wedding-india`)

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = that folder, `SKILLS` = the skills folder.
- First run on a machine: `python CORE/scripts/check_env.py`.
- Ask the family first and write it down: couple's names in English **and** in the script they want (Hindi, Gujarati,
  Tamil, Punjabi, Urdu...), event names and dates, the list of elders who must appear (grandparents, both sets of
  parents, mama/mami, bua...), the order they want, songs (licensed), and anything that must not be shown.
- **Consent and privacy:** many guests, women in purdah, children. Deliver privately; public posting only with the
  couple's approval; drop anyone who asked not to be filmed.
- Sort footage into one folder per event **before** editing (`haldi/`, `mehndi/`, `sangeet/`, `baraat/`, `pheras/`,
  `vidaai/`, `reception/`) and give each event its own work folder. Never mix events in one assembly.

## How a pro cuts this

**Highlight structure (% of length)**

| beat | % | what goes here |
| --- | --- | --- |
| haldi | 12 | turmeric close-ups, laughter, water / flowers thrown |
| mehndi | 12 | henna detail macros, the groom's name hidden in the design, dholki |
| sangeet | 18 | family performances, the couple's dance, peak energy on the drop |
| baraat / arrival | 12 | horse or car, dhol, dancing relatives, the varmala |
| pheras / nikah | 26 | the ritual heart: agni, mantras, the seven rounds, sindoor, mangalsutra; or qubool hai and the nikahnama |
| vidaai / reception | 20 | the emotional goodbye, then the stage, cake, the last dance |

Per-event reel: open on the strongest image of that event, 3-4 beats of build, end on a family moment. Same skin and
grade for every event so the set looks like one wedding.

**Ritual pacing.** Ceremonies are repetitive but sacred. Never cut the seven pheras into seven 1-second flashes: show
the first round in full (or most of it), dissolve through the middle rounds, hold the last round and the reaction.
Let a mantra or the qubool hai play with the music dipped right down, or none. Hold the sindoor and mangalsutra moments 3-5 s. Cut the
celebrations on the beat (ASL 1.5-3.5 s), the rituals on the phrase (4-8 s holds).

**Cut rules.** No jump cuts inside a ritual; cover with a different angle or a detail (hands, fire, flowers). Never
place a laughing face over a crying vidaai moment (Kuleshov). Never reorder a ritual: the family knows the order.
Every elder on the list appears at least once, ideally in a clean close-up.

**Transition grammar.** Cuts on the beat for haldi, mehndi, sangeet, baraat; slow dissolves (0.8-1.2 s) inside pheras
and vidaai; dip to black between events in the long film. Whip only in sangeet / baraat.

**Music and sound.** A different licensed song per event is normal; the highlight can carry two songs joined on a
downbeat. Song leads (bed ~-6 dB) and dips fully for mantras, vows and the vidaai. Keep natural dhol and crowd sound.

**Colour.** `indian-wedding` (warm gold, rich reds, skin kept natural) at 0.6-0.75; never push reds so far the bridal
lehenga clips. Haldi yellow should look yellow, not orange skin.

**Titles and captions.** Event names as titles in the family's script (हल्दी, मेहंदी, संगीत, फेरे; or Tamil, Gujarati...).
No creator captions in the highlight. Mantra translation subtitles only if the family asks.

**What the client judges.** Every elder present, ritual respect, colour of the outfits, the sangeet energy, the teaser
arriving within days.

**Common mistakes.** One assembly for all events; pheras rushed; a missing grandparent; orange skin from haldi; music
over the mantras; misspelled names in the regional script; boxes instead of letters (font without that script).

## Make the edit

One work folder per event. Montage orders clips by file modification time and bakes the song into the assembled audio,
so dry-run first and fix the order in the spec.

```bash
# per event, e.g. sangeet (beat-cut montage, 60 s reel in 9:16)
python CORE/scripts/timeline.py auto sangeet/ --work ev-sangeet --mode montage --music sangeet_song.wav --duration 60 --format 9:16 --dry-run
#   edit ev-sangeet/timeline_spec.json: order, drop shots, transitions
python CORE/scripts/run.py - --timeline ev-sangeet/timeline_spec.json --style SKILLS/soft-gradient --genre wedding-india --format 9:16 --no-cut --model base --work ev-sangeet --stop-after plan
python CORE/scripts/render.py ev-sangeet/plan.json --frames 1,10,25,45,58
python CORE/scripts/render.py ev-sangeet/plan.json
python CORE/scripts/finish.py ev-sangeet/plan.json --platform reels
```

**Pheras / Nikah (ritual sound kept).** Use a hand spec (or `timeline.py auto pheras/ --mode story --model base --dry-run`)
with the ritual clips `"audio": "keep"`, dissolves between rounds, and no song baked in. Transcribe in the spoken language:

```bash
python CORE/scripts/timeline.py auto pheras/ --work ev-pheras --mode story --format 16:9 --model base --dry-run
python CORE/scripts/run.py - --timeline ev-pheras/timeline_spec.json --style SKILLS/soft-gradient --genre wedding-india --format 16:9 --no-cut --model base --music pheras_bed.wav --work ev-pheras --stop-after plan
# run.py does not pass --language to the timeline transcription; redo it in the spoken language, then re-plan:
python CORE/scripts/transcribe.py --work ev-pheras --model small --language hi
python CORE/scripts/autocut.py --work ev-pheras --keep-all
python CORE/scripts/make_plan.py --work ev-pheras --style SKILLS/soft-gradient --genre wedding-india --format 16:9
```

Re-planning drops the `--music` that run.py added, so put the `music` block back in the plan by hand.

**Highlight:** build the spec from the best shots of every event in ritual order (haldi to reception), then
`run.py - --timeline highlight_spec.json ... --format 16:9 --no-cut --work hl`. **Traditional film:** the same per event
with `--mode story`, long holds and dip-to-black between events.

## Refine the plan

- **Remove creator captions** (delete the `captions` element the skin adds) and clear `words` in montage reels.
- **Montage audio is music:** `"audio": {"platform": "youtube", "voice": false}`.
- **Ritual sections:** `"music": {"src": "pheras_bed.wav", "under": 22, "duck": "speech-aware", "duckDepth": 20}` keeps
  a soft bed that drops away under the mantras. Limit: plan music runs under the whole video (`start` is an offset
  into the song, not a timeline position) and there is no per-section mute. When a mantra must stand completely
  alone, leave music out of the pheras film and keep it for the celebration reels.
- **Colour:** `"color": {"look": "indian-wedding", "intensity": 0.7}`; mixed cameras `"match": "hero.png"`.
  `"finish": {"grain": 3, "vignette": 0.25}`.
- **Indic-script titles:** load a font that has the script, in the plan theme:
  `"theme": {"fontsUrl": "https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@600&display=swap", "vars": {"--font-display": "'Noto Sans Devanagari', sans-serif"}}`
  (Tamil: `Noto Sans Tamil`, Gujarati: `Noto Sans Gujarati`, Gurmukhi: `Noto Sans Gurmukhi`, Urdu: `Noto Nastaliq Urdu`).
  Keep the skin's `fontsUrl` too if you need its Latin face (one URL can load several `family=` entries).
  Title: `{"type": "titlecard", "kicker": "16.02.2026", "title": "संगीत", "subtitle": "Riya & Arjun", "start": 0, "end": 3}`.
- **Event lower third for elders (optional):** `{"type": "lowerthird", "name": "Dadi ji", "role": "Grandmother", ...}`, only with names
  the family approved.
- Freeze or slow the varmala / sindoor moment in the spec: `"speedRamp": [{"at": 12.0, "rate": 0.5, "ramp": 0.4}]`.
- `python CORE/scripts/editor.py review ev-sangeet/plan.json --genre wedding-india`.
- **Footage clean-up (video, before the spec):** handheld baraat shots, dark sangeet halls and LED-lit stages: `python CORE/scripts/prep.py baraat03.mp4 --work fix/baraat03 --stabilize --denoise light`, then use `fix/baraat03/source.mp4` in the spec. `--stabilize` = vidstab (crops ~6% at the edges), `--denoise light|strong` = video noise, `--deflicker` = mains-light flicker. Only on clips that need it. `--deflicker` under tube/LED lights that pulse on camera.

## Deliver

```bash
python CORE/scripts/deliver.py hl/plan.json --to youtube,prores-422hq --out-dir hl/deliver --burn no
python CORE/scripts/deliver.py ev-sangeet/plan.json --to reels,whatsapp-status --out-dir ev-sangeet/deliver --burn no
python CORE/scripts/qc.py hl/deliver/final_youtube.mp4 --plan hl/plan.json --platform youtube --strict
python CORE/scripts/qc.py ev-sangeet/deliver/final_reels.mp4 --plan ev-sangeet/plan.json --platform reels --strict
```

`whatsapp-status` makes a <=16 MB, 60 s version families forward. Sidecar `captions.srt` files are UTF-8 and keep the
regional script; check they open correctly. Name files `riya-arjun_sangeet_v001_9x16.mp4`.

## Check before delivering

- Contact sheet: the regional script renders with correct conjuncts and matras (no boxes, no broken ि placement).
  If it is wrong, the font lacks the script: fix `fontsUrl`.
- Every elder on the family's list ticked off; names in both scripts spelled as the family wrote them.
- Pheras / Nikah: rituals in the correct order, mantras audible, no music over them, no rushed rounds.
- Skin natural under haldi yellow and stage lights; reds not clipping. `qc.py` passes loudness and flash checks.
- Tell the family what each file is, which events are done, and how many correction rounds remain (often 2).

## Example requests

- "Make a 60-second Sangeet reel and a Haldi reel from these folders, Bollywood song for each."
- "Cut a 5-minute highlight of the whole wedding with the event names in Hindi."
- "Edit the pheras properly, keep the mantras, don't rush the rounds."
