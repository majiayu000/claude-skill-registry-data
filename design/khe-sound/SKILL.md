---
name: khe-sound
description: "Decides which moments in a product UI or a launch video earn a sound or a haptic, designs one material family, generates the files with ElevenLabs or an offline synth, and places each transient on the frame where the motion lands. Use when someone says \"add a sound\", \"it needs a satisfying click\", \"should this make a sound?\", \"the click feels late\", \"the sounds feel stock\", or wants UI sound effects, a mute toggle, vibration on the mobile web, or a soundtrack placed on a locked film. For the motion a sound lands on use `khe-ui`; for a film's register, beats and cuts use `khe-launch-film`."
license: MIT
metadata:
  author: Harshit Khemani
  version: "1.0.0"
---

# Sound and haptics

You own the sound from the first "should this make a sound?" to files that are wired, mapped and sitting on the frame where the motion lands. Most moments get no sound, and saying so is part of the job.

A construction skill. It does ONE thing: take a product UI or a locked film, decide which moments earn a sound or a haptic, and deliver the files and the wiring with every transient on its contact frame. It does not settle the motion a sound lands on (that's `khe-ui`), or choose a film's register, beats or cuts (that's `khe-launch-film`).

## The one idea

**Silence is the default; a sound that ships has earned its moment, belongs to one material, and puts its transient on the contact frame, never before it.**

Five ways it fails:

- **Everywhere.** A tick on every keystroke, a click on every button, a whoosh on every route. A user can look away from motion but cannot un-hear a chime.
- **Forced.** On by default, no switch, or a sound that is the only signal of an event. The muted are the majority.
- **Stock.** A glossy blip from one pack, a whoosh from another, a buzzer from a third, or one re-rolled member.
- **Off-frame.** The transient before the picture, a cue on the tween's start, 12 ms of silence baked into the file. A lead is detectable at 45 ms, so early reads as broken where late reads as physics.
- **Bloated.** Stereo, 640 ms, a reverb tail, a peak at -0.2 dBFS. Slightly too long or too loud is annoying by the tenth use.

The fix: reject most moments in writing, describe one thing and what strikes it, cut every file to its role's length at -3 dBFS, and cue the frame where the visual makes contact. A sound map with zero rows is a valid result.

## Initial response

When this skill is invoked with no request, reply only with:

> I'm ready to decide which moments earn a sound, then build and sync the ones that do. Usage: `/khe-sound [target]`

Then wait. Give nothing else until the user asks.

## How hard to press

Silence is the default in product UI; in a film, sound is the emotional layer. The files in `examples/` are the bar: if your map has more sounds and fewer silent rows than `examples/product-cues.json`, or your file is longer, louder or later than `examples/tick.wav`, that is the first fix. Then picture the one thing the most exacting listener would send back: the tick that fires on a key, the click one frame ahead of the press, the family member from another product, the tone with no visual twin. If you can name that row or file, you have found the next fix. You cannot hear what you make, so every claim about a sound carries a command and the number it returned.

## Workflow

Most of the quality is decided before any file exists. If the user only asked whether something should make a sound, answer step 2 in one line and stop. Under `khe-auto` the same loop runs with this skill's gate, `scripts/sound-check.mjs`.

1. **Surface and plan.** Read [gotchas](references/gotchas.md) and [pov](references/pov.md); a POV that raises the sound floor wins. Name the surface: product UI (silence is the default), a film (sound is the medium), or a phone vibration. A film needs locked picture: if frames can still move, stop and send the film back to `khe-launch-film` or the move to `khe-ui`. Exit: one line naming the surface, and for a film "picture locked" with its register and loudness written beside it ([launch-video-sound](references/launch-video-sound.md)).
2. **Decide each moment.** Walk [sound-decision-framework](references/sound-decision-framework.md) per proposed moment. Frequency: every keystroke, scroll, hover or focus move is never; every primary action is no unless the product is tactile; a daily moment gets at most one short sound; a rare milestone is where the budget goes. Purpose: confirmation when attention is elsewhere, a state change with no visual, physicality the product is built on, or a brand moment. The 100th-use test: at the first wince, halve the length and drop 3 dB, or cut it. A haptic walks the same gate and fires on a committed result, on the frame of its visual change ([haptic-feedback](references/haptic-feedback.md), [web-haptics-reconciliation](references/web-haptics-reconciliation.md)). Exit: a ledger with one row per moment, its count per day, and yes or no with the reason; the silent rows stay in it.
3. **Start from the closest gold.** Copy the file in `examples/` that matches the job (the Examples table) and replace its content with this product's or film's. Exit: your sound map or cue sheet exists with the gold's fields, and no row has an empty trigger, time or twin.
4. **Design one material.** One line that names a thing and what strikes it, on every prompt and recipe; four to six sounds; size sets pitch and length, direction sets meaning ([sound-palette](references/sound-palette.md), [sound-spec](references/sound-spec.md)). Exit: the manifest has one `material` and each sound's length is inside its role's limit.
5. **Build.** Product UI: `node scripts/sound-family.mjs <manifest> --out <dir>`, with `--dry-run` first if credits matter; it uses ElevenLabs when `ELEVENLABS_API_KEY` is set and the offline synth otherwise ([sound-generation-elevenlabs](references/sound-generation-elevenlabs.md), [sound-generation-open-source](references/sound-generation-open-source.md)). A film in a derived register: write the cue sheet from the locked timeline ([sound-from-motion](references/sound-from-motion.md)), then `node scripts/sound-sheet.mjs cues.json --out stem.wav --report`. A beat track or a voice is placed per [launch-video-music](references/launch-video-music.md); designed effects follow [designed-sfx-anatomy](references/designed-sfx-anatomy.md); every recording passes [sound-licensing](references/sound-licensing.md) before it is fetched. Exit: the files exist and each has a licence row.
6. **Place and wire.** Each transient goes on its contact frame with 0 to 30 ms of lag ([sound-motion-sync](references/sound-motion-sync.md)). On the web, the context is created inside the first gesture, the switch starts off and persists, and each play is a new buffer source ([sound-playback-web](references/sound-playback-web.md)). Exit: every cue has a `t` or a `frame`, and the playback file matches `examples/wiring.js` in order.
7. **Rehearse with the gate.** `node scripts/sound-check.mjs <map> <manifest> <sfx dir> <playback file> --gate` (add `--film` for a stem). Fix the largest fault first, in this order: a sound that should not exist, then playback and access, then placement, then the files. Run it again. Exit: the last line is `sound check passed`, and every candidate line is fixed or has a reason. Passing is necessary, not sufficient.
8. **Walk [verify](references/verify.md) from evidence.** Answer each question from a gate line, a measured number or a frame you stepped to; for a film, step the picture to every onset in the `--report` list. Where earshot is installed, route listening to it ([earshot-reconciliation](references/earshot-reconciliation.md)). Any no is the next fix, then back to step 7. Exit: every answer is yes or is listed as not checked.
9. **Fresh-eye review.** Hand a reviewer the evidence and the gold per [review](references/review.md), never your plan or reasons. Exit: a ranked list answered item by item, or "nothing".
10. **Hand over.** Write `CUES.md` from the template in [verify](references/verify.md): the gate's last line pasted, each line and its fix, what was measured, the licences, and what was not heard on a device. Then stop.

## Faults that come back every round

Check each before handing over.

- **A sound on a key or a press** instead of on the result ([sound-decision-framework](references/sound-decision-framework.md)).
- **A lead-in left in the file,** so the click lands late however it is cued ([sound-spec](references/sound-spec.md), Format).
- **A cue on the tween's start** or on a spring's `animationend`, never on the contact ([sound-motion-sync](references/sound-motion-sync.md), Gotcha).
- **The context created at module load;** sound works on the second click ([sound-playback-web](references/sound-playback-web.md), Gotcha).
- **Sound that starts on,** because the code tests for anything but a stored off ([sound-playback-web](references/sound-playback-web.md), The five rules).
- **One member re-rolled,** or a prompt that names a style ([sound-palette](references/sound-palette.md), Material, not genre; [sound-generation-elevenlabs](references/sound-generation-elevenlabs.md), Gotcha).
- **Normalizing before trimming the tail,** which raises the hit until it clips ([sound-spec](references/sound-spec.md), Gotcha).
- **A bed laid flat from 0 s** with nothing taken away before the reveal ([launch-video-sound](references/launch-video-sound.md), Gotcha).
- **A film at -14 LUFS by habit** ([launch-video-sound](references/launch-video-sound.md), Loudness is a register choice).
- **A licence remembered, not read** ([sound-licensing](references/sound-licensing.md), Verify on the item's page).

## Hard rules

1. **Run the decision before generating anything.** Frequency, then purpose, then the 100th-use test, because nothing in the browser lets the user turn one sound down.
2. **Product UI sound ships off, with a persisted switch, and every sound has a visual twin.** A sound that is the only signal is a broken design for the muted majority.
3. **One material per product or film.** Describe a thing, never a style. Generation is not deterministic, so a changed material means regenerating the whole family, never one member.
4. **Audio never leads the picture.** The transient sits on the contact frame with 0 to 30 ms of lag. A lead is detectable at 45 ms, a lag only at 125 ms.
5. **Every file meets the spec before it is wired.** Mono, 44.1 kHz 16-bit WAV source, zero leading silence above -60 dBFS, the last 10 ms faded, peak at -3 dBFS (-1 dBTP for delivered video). Trim the tail before normalizing.
6. **In a film, write the register and its loudness before fetching any file.** -1 dBTP true peak is the only fixed number. -14 LUFS is one option for muted-autoplay feeds; the measured medians are -18.1 and -18.4 LUFS.
7. **Read every recording's licence on its own page and record it.** A launch film is commercial, edited and scanned. CC0 and CC BY pass; NC, ND and SA fail; an aggregator's listing is not a licence.

## Examples

Open the closest one before you start (step 3).

| Need | Example | What to learn |
|---|---|---|
| A family of UI sounds | `examples/family.json` | One material line on five sounds, each length inside its role's limit, a licence beside each file |
| Which moments get a sound | `examples/product-cues.json` | Seven moments proposed, four silent with the reason, three with a result as the trigger, a contact time and a visual twin |
| Sound on a locked film | `examples/film-cues.json` | Register, loudness and licences before any cue; the sub leaves 0.6 s before the name; one thud, then 1.8 s of silence |
| Web playback and the mute switch | `examples/wiring.js` | The context inside the first gesture, off until a stored on, a new source per play, the sound on the result |
| A finished one-shot | `examples/tick.wav`, `examples/send.wav` | Mono, 70 ms and 245 ms, peak -3 dBFS, the hit on the first sample, the last 10 ms faded |

`teaching/` holds 14 bad/good pairs, one folder per gate line ([teaching](references/teaching.md)). Use them to diagnose a fault; the bad halves are never starting points.

## Find the reference

Open a reference only when the job needs it. Never load the whole folder.

| Job or symptom | Open |
|---|---|
| "Should this make a sound?", "let's add a satisfying click" | [sound-decision-framework](references/sound-decision-framework.md) |
| The sounds feel stock, or do not belong together | [sound-palette](references/sound-palette.md) |
| A sound feels wrong: too long, too loud, a gap before the hit | [sound-spec](references/sound-spec.md) |
| The click feels late, early or like an echo | [sound-motion-sync](references/sound-motion-sync.md) |
| Sound works on the second click, or needs a mute switch | [sound-playback-web](references/sound-playback-web.md) |
| Generate a family with an ElevenLabs key | [sound-generation-elevenlabs](references/sound-generation-elevenlabs.md) |
| No API key, or sounds that are parameters in code | [sound-generation-open-source](references/sound-generation-open-source.md) |
| Which kind of soundtrack a film gets, and how loud | [launch-video-sound](references/launch-video-sound.md) |
| A music track or a voice-over has to sit on the picture | [launch-video-music](references/launch-video-music.md) |
| A cue sheet from a locked timeline; pitch, pan and length from the motion | [sound-from-motion](references/sound-from-motion.md) |
| A whoosh, riser, impact, ding or pop reads cheap | [designed-sfx-anatomy](references/designed-sfx-anatomy.md) |
| "Can I use this track?", credits, Content ID | [sound-licensing](references/sound-licensing.md) |
| Describing or scoring audio you cannot hear | [earshot-reconciliation](references/earshot-reconciliation.md) |
| The phone should tap back; vibration on Android and iOS Safari | [haptic-feedback](references/haptic-feedback.md), [web-haptics-reconciliation](references/web-haptics-reconciliation.md) |
| The last pass, a gate line, what to do about a symptom, the handover | [verify](references/verify.md) |
| Briefing a reviewer who has not seen the build | [review](references/review.md) |
| A gate line you do not understand; a bad/good pair for it | [teaching](references/teaching.md) |

## Never ship

Check the work against this table before finishing. [verify](references/verify.md) names the gate line for each row the gate can catch.

| Never | Instead |
|---|---|
| A sound on typing, scroll, hover, focus, or a plain button press | Silence. Hover is 0 ms |
| Sound on by default, or with no way to turn it off | Off by default, a persisted switch in settings, reachable by keyboard |
| `new Audio(url).play()`, or `new AudioContext()` at module load | Context created and resumed inside the first gesture, buffers decoded once, a new `AudioBufferSourceNode` per play |
| A sound that is the only signal of an event | A visual twin for every sound: the state change, the toast, the shake |
| The prompt "a success sound" with the duration on auto | Material, action, envelope, mood, frequency hint, purpose; "dry, no tail"; `duration_seconds` 0.5 for ticks; `prompt_influence` 0.8 or higher |
| A family from several packs, or one re-rolled member | One material phrase on every prompt; regenerate the whole family |
| A stereo tick, 640 ms with a reverb tail, 12 ms of lead-in, peak at -0.2 dBFS | Mono, 40 to 80 ms, 0 ms above -60 dBFS, last 10 ms faded, peak at -3 dBFS |
| A transient cued at the tween's start, ahead of its contact, or on a spring's `animationend` | The contact frame: about 85 % through a decelerating tween, the first crossing of rest for a spring, plus 0 to 30 ms |
| A bed laid flat from 0 s with a whoosh on every cut, or library blips over a beat track | The drop on the reveal, something taken away 0.1 to 0.9 s before it, and the track carrying the pops |
| A film master at -14 LUFS by habit, or a true peak above -1 dBTP | The loudness written beside the register; -1 dBTP always |
| A recording under NC, ND or SA, or a licence copied from an aggregator | CC0 or CC BY, read on the item's own page and recorded in the manifest with the date |
| A haptic on every tap, on a modal opening, or the `buzz` preset | One haptic on the committed result, matched in weight, never the only feedback |

## Output

A sound map table (Moment | Sound | Material / contour | Length | Trigger | Why) with the silent rows kept, then the file list, the playback wiring, the gate's last line, and `CUES.md`.

## Tone

Blunt and short. "This should not make a sound" is a complete answer, and it is the one this skill exists to give. Never describe how audio sounds without the command and the number behind it, and say which checks still need a laptop speaker, a phone speaker or a real device.

## Yours to edit

Read both before producing anything. They outrank the defaults in this skill, and a project's `.design` contract or DESIGN.md outranks them.

- [gotchas](references/gotchas.md): lived failures, one line each. Append one when something goes wrong.
- [pov](references/pov.md): your taste calls.

## Pairs with

Where the text above names a reference in another skill, that skill owns the detail.

- `khe-ui`: a transient needs a contact frame, so the move has to be settled before a sound can be placed on it.
- `khe-launch-film`: the film's register, reveal and cuts decide where the drop, the gaps and the breakdowns go, and picture must be locked there first.

Names without the `khe-` prefix are other people's skills, not part of this one: `stageshow` is Benji Taylor's ([benjitaylor/skills](https://github.com/benjitaylor/skills)); `animate`, `emil-design-eng` and the rest are Emil Kowalski's ([emilkowalski/skills](https://github.com/emilkowalski/skills)). Install them from their own repos.

Harshit Khemani. MIT.
