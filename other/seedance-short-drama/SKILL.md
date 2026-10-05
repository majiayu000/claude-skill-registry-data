---
name: seedance-short-drama
description: Requires OFOX_API_KEY — create one at https://app.ofox.ai. Generate a realistic-human, dialogue-driven short-drama clip — one shot, or a few hard-cut shots inside one job — from a script or scene description using the Ofox video API (Seedance 2.5). Runs a short creative brief when the input leaves beat, aspect ratio, emotional arc or camera register open (one held take, a travelling take, or a multi-shot cut list) ("Let the AI decide" is offered on the taste questions, never on a must-ask one, and never as the default), writes a structured prompt (header manifest, timestamped shots, quoted dialogue with delivery notes, consistency lock), shows a cost estimate, then calls ofox-video-core to submit, poll, download, and report the real cost. Use when a user asks to turn a script beat into video, e.g. "generate scene 3 of this script, two characters talking, 15 seconds", "make a vertical short-drama clip of these two arguing in a kitchen", "turn this dialogue into a 12-second video", or "give me a realistic short-drama shot of a couple breaking up at a train station". Do not use for silent product/brand shots (see seedance-ad-creative), for anime- or manga-styled scenes (see seedance-anime-drama), for one person addressing the viewer rather than another character — a script read from a supplied portrait is talking-head, an idea pulled out of an article is explainer — or for anything not involving people/dialogue.
license: MIT
version: "2.0.1"
homepage: https://github.com/ofoxai/skills/tree/main/skills/seedance-short-drama
metadata:
  author: ofoxai
  version: "2.0.1"
  openclaw:
    requires:
      env: [OFOX_API_KEY]
      bins: [curl, jq]
    primaryEnv: OFOX_API_KEY
    envVars:
      - name: OFOX_API_KEY
        required: true
        description: Ofox API key. Create one at https://app.ofox.ai (Settings -> API Keys). The same key works across every Ofox skill.
    emoji: "🎭"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/seedance-short-drama
---

# seedance-short-drama: dialogue-driven short-drama shots

Turns one beat of a script into a realistic-human video clip — one shot, or a
few hard-cut shots inside a single job. A short creative brief settles what
the script leaves open; a structured prompt (character block, timestamped
shots, quoted dialogue with delivery notes, consistency lock) goes to
Seedance 2.5; this skill submits, polls, downloads and reports the cost.

This skill is a thin, scenario-specific layer over
[`ofox-video-core`](../ofox-video-core/SKILL.md). It owns the short-drama
prompt craft, the pre-generation brief, recommended defaults, and this
scenario's rows in the approval table; `ofox-video-core` owns talking to the
Ofox API correctly and safely (the `OFOX_API_KEY` handling, the no-resubmit
rule, error-code mapping, download/verification). **Read that skill's safety
contract before using this one** — it is not restated here.

Three shared references from `ofox-video-core` are load-bearing here and are
linked, not copied:

- [`../ofox-video-core/references/creative-brief.md`](../ofox-video-core/references/creative-brief.md)
  — what to ask the user before a prompt exists: the three tiers, one round of
  at most four questions, the "Let the AI decide" discipline, the skip rows,
  and the anti-patterns. Read it before the brief section below, which adds
  only this scenario's question set.
- [`../ofox-video-core/references/prompt-structure.md`](../ofox-video-core/references/prompt-structure.md)
  — the vendor's formula, the header-manifest → timeline → closing-block
  skeleton, timestamp formats and segment lengths, transition and camera
  vocabularies, consistency locks and negative lists, dialogue density,
  reference-image semantics, endings. Load it before writing a prompt; this
  file adds only what is specific to short drama.
- [`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md)
  — never spend before an approved cost table.

## Where the core skill lives

Resolve once, before the first call:

```bash
for d in ../ofox-video-core \
         ../ofoxai-skills-ofox-video-core \
         ~/.agents/skills/ofox-video-core \
         ~/.agents/skills/ofoxai-skills-ofox-video-core \
         ~/.claude/skills/ofox-video-core; do
  [ -f "$d/references/ofox-video.sh" ] && echo "$d" && break
done
```

Examples below are written as `../ofox-video-core/...` (the skills.sh /
ClawHub / `npx ofox-skills` layout, where a skill's directory is named after
the skill). If the probe found a different directory — LobeHub unpacks each
skill as `ofoxai-skills-<name>`, so the sibling there is
`ofoxai-skills-ofox-video-core` — substitute it, in the `ofox-video.sh`
commands and in the `references/*.md` links alike.

Nothing found → the core skill isn't installed; see "If the script isn't
found".

**This skill needs `ofox-video-core` 2.0.0 or newer.** From that version the
billable subcommands refuse to run without `--approved`, and every real-run
command below passes it. An older core does not know the flag and stops with
`unknown option '--approved'` before any request — nothing is submitted and
nothing is billed, so the fix is to update the core, never to drop the flag.

## Before generating: the availability check

Run this once per session (not on every request):

```bash
bash ../ofox-video-core/references/ofox-video.sh check
```

If it fails, follow `ofox-video-core`'s guidance (install `curl`/`jq`, or get
an `OFOX_API_KEY` at `https://app.ofox.ai`) — don't dead-end the
conversation, and don't re-run this check on every subsequent request once
it has passed.

## Shots, cuts and jobs

One job is one clip of 4–30 seconds, and a clip **can hold several shots
joined by hard cuts**. Write the timestamps as cut boundaries — `SHOT 2
(3-6s): … HARD CUT.` — and on the runs measured so far Seedance 2.5 cuts
there. Default to **2–5 seconds per shot**.

The measured envelope, as of 2026-09-04, is **up to 10 shots in 30 seconds**,
and separately **up to 6 hard cuts** among one job's boundaries — the two
maxima are from different jobs — at 480p and 720p, on
`bytedance/seedance-2.5` pinned to `byteplus`. Four of those jobs are short
drama with the audio on and lines in it (`844c9145`, `4e5c9581`, `41f87ac7`,
`036ac3a8`), which closes the caveat this section used to carry — the first
two measured runs were silent, and speech turned out not to disturb the cut
structure: `036ac3a8` carried five lines across seven shots and rendered all
seven in order. Cuts land within about ±1.5 seconds of their stamps, and a
character described once in a manifest survives every shot on text alone,
with no image attached. The job ids and the frame-by-frame readings are
under "Several shots in one job" in
`../ofox-video-core/references/prompt-structure.md`.

**Still outside the envelope**: more than 10 shots or more than 6 hard cuts
in one job, 1080p, the `volcengine` upstream, and a single line of dialogue
split across a cut — the tooling used here cannot hear audio, so no run
above has had its words checked, only their presence and timing. A first
attempt outside that envelope is an experiment — say so, and price it as
one. And inside it, a written `HARD CUT` is still not self-guaranteeing;
see "Choosing a transition, not defaulting to a cut" below.

If you mean beats inside one held shot rather than cuts, declare `one
continuous shot` in the first sentence; without it a timestamped list reads
as a cut list ("Two things a timestamp can mean" in the shared file).

### Where separate jobs and `chain` fit

- **Separate `generate` calls** when each shot needs its own approval, seed,
  resolution or duration, or when the sequence runs past 30 seconds. Each is
  a separately billed job; this skill does not stitch clips.
- **`ofox-video-core`'s `chain`** carries one job's closing frame into the
  next. **It does not work in this scenario** — the carried frame holds a
  photoreal person, which Seedance 2.5 refuses ("Reference images and real
  people"). Say so up front rather than letting the user discover it
  mid-sequence. Consecutive short-drama jobs are generated independently;
  continuity across them is text — the same character block word for word
  plus the `CONSISTENCY` line of the template.

A script that spans several scenes is still not one job. Which beat gets the
clip is the brief's first question; do not compress a chapter into 30
seconds.

## Prompt language follows the audio

Audio is generated on by default, and the model speaks **whatever language the
quoted lines are written in**. So keep dialogue in the user's own language —
if they give you Chinese lines, put Chinese in the prompt. Translating them to
match the English examples in this file produces an English-dubbed clip, and
the user only finds out after paying for it.

The rest of the prompt (setting, camera, lighting) can be English regardless;
it is the quoted speech that determines the spoken language. The dialogue
budget is in two tiers, below; for Chinese and Japanese count characters
rather than words.

## Before writing the prompt: the creative brief

The shared rules are in
[`../ofox-video-core/references/creative-brief.md`](../ofox-video-core/references/creative-brief.md)
— the three tiers, the one-round limit, the shape of a question, the "Let the
AI decide" discipline, the generic skip rows, the order with the approval
gate, the fallback for a runtime without `AskUserQuestion`, and the
anti-patterns. Read it before writing a prompt. This section adds only what
is specific to short drama.

Read the user's message and attachments first, and mark every axis of the
clip **settled** or **open**. Zero questions is common here: a beat pasted
with its stage directions plus "15 seconds, vertical, for Reels" has settled
every axis — write the prompt.

| Tier | Short-drama axes |
|---|---|
| **must-ask** | which beat of a multi-scene script to render; whether an asset the request implies actually exists |
| **ask-if-open** | aspect ratio, emotional arc, the camera register — which also fixes the shot count; a draft batch versus one final, but only when the user is already exploring; on a published deliverable, a second round adds the duration split and whether a slow-motion or freeze-frame beat belongs in the clip at all — see "Pacing questions belong in round two" in `creative-brief.md` |
| **never-ask** | resolution, model, provider, audio on/off, duration once stated. "Never-ask" means the agent never raises this proactively — it does **not** mean ignoring an explicit choice: if the user names a model (an id, or a shorthand like "wan"/"hailuo"), that model is used instead of the `seedance-2.5` default. See "Choosing a video model" below. |

### The short-drama questions

| # | Tier | Header | Question | Options — first is recommended; "Let the AI decide" comes last wherever it appears, and never on a must-ask row | Ask when |
|---|---|---|---|---|---|
| 1 | must-ask | `Beat` | Which beat gets this clip? One job holds 4–30 seconds. | Two or three beats extracted from the script, each named by its turning line or action (`Kitchen confrontation — "Where were you last night?"`, `She walks out — no lines`); recommended = the one with the clearest reversal. **No "Let the AI decide" here** — a must-ask axis never gets one, and no model can tell which beat the user meant. If they answer "you pick" in free text, choose the strongest beat, name it in the recap, and let the gate be the check | The script spans more than one scene or more than about 30s of action. A single beat: skip. |
| 2 | ask-if-open | `Aspect` | Where will it be watched? Vertical and landscape are different framings, not a crop. | `9:16 vertical (recommended)` — mobile short-drama feeds, the default below / `16:9 landscape` — web and YouTube; the gallery's own short-drama sample is mostly landscape (5 of the 6 cases that state a ratio) / `Let the AI decide` | No platform word and no ratio in the input. |
| 3 | ask-if-open | `Arc` | How does the feeling move across the clip? It decides the shots. | Two or three arrow chains built from the script (`braced → hears him → wavers → wry smile → "We're done." → steps back`, adapted from case 3; `calm → the lie lands → silence → she leaves`); recommended = the one the lines support most directly / `Let the AI decide` | Lines with no stage directions and no tone word. Stage directions present: skip. |
| 4 | ask-if-open | `Camera` | How is the beat shot? This one answer decides what the camera does **and** how many shots there are. | Put the register that fits the beat first and mark it `(recommended)` — the travelling take when the beat has somewhere to go (two rooms, a corridor, a doorway, a street), the cut list when it jumps between faces, hands and details, the held take when everything happens on one face. `Travelling one take` — no cuts; the camera **crosses space** and each new view arrives from behind an occlusion or through a gap; 3–5 phases of 5–8s (cases 2, 6, 8). Only offer it when the beat has somewhere to go — a take that closes distance in place comes back static (job `16023efe`, below) / `Multi-shot cut list` — a new shot size and camera position at every timestamp, 2–5s a shot, so 4–10 shots in 20–30s (cases 1, 11, 14) / `Held take` — locked, or a breathing handheld, on one or two faces; the reframing comes from an actor moving rather than the lens (cases 3, 22) / `Let the AI decide` | No camera word in the input. |
| 5 | follow-up | `Lines` | The lines overrun this duration's budget (tiers below). | `Extend to <N> seconds (recommended)` — keeps every line; state N / `Trim to budget` — the cut lines are shown before the cost table / `Let the AI decide` | Only when the dialogue exceeds its tier for the chosen duration. |
| 6 | ask-if-open | `Drafts` | Several takes to choose from, or one final? | `One 720p final on seedance-2.5 (recommended)` / `Four 480p drafts on seedance-2.0-mini, then the final` — a different model is a different look, not only a different price; see "Several takes to choose from" / `Let the AI decide` | Only when the user asks for versions, or says they are unsure what they want. |
| 7 | ask-if-open (round two) | `Pacing` | Where do the seconds go? The payoff decides it — a fight's payoff is the middle of the clip, a dialogue beat's can be the last line. | `Weight the core (recommended)` — setup and close stay near the "Action / spectacle" row of "Duration budget" below; most of the runtime goes to the fight or the exchange itself / `Weight the close` — the payoff is the last line or action, so the close gets real time, near the "Dialogue / slice-of-life" row / `Let the AI decide` | Only in round two (a published deliverable — see `creative-brief.md`), and only when the beat has a clear "main event" whose share of the runtime the request leaves open. |
| 8 | ask-if-open (round two) | `Effects` | Slow motion or a freeze frame on the best beat, or full speed throughout? | `One insert, capped near 2–3s (recommended)` — on the single decisive hit or reveal only, per "Duration budget" below / `None — full speed throughout` — plainer, and nothing to check on the draft / `Let the AI decide` | Only in round two, and only when the beat has an obvious climactic hit, reveal or gesture where either device is a plausible choice. |

Handheld or locked is a **texture inside** the register, not a fourth
option: the realistic short-drama convention is a breathing handheld (cases
1, 4, 6), and it applies to a travelling take (case 6) as readily as to a
held one. Until 1.8.0 this question offered `Handheld documentary`, `Steady
cinematic` and `Static over-the-shoulder` — three labels for the camera
staying roughly where it is, which is exactly what `creative-brief.md`'s "The
shape of a question" forbids ("visibly different pictures, not synonyms").
A user who wanted the camera to travel could not pick it.

If more than four are open in round one, ask in this order: `Beat`,
`Aspect`, `Arc`, `Camera`; `Lines` is the follow-up. `Drafts` folds into the
cost table as a second row rather than taking a question slot. On a
published deliverable (`creative-brief.md`'s two-round rule), round two adds
`Pacing` and `Effects` — in that order, since the duration split has to be
settled before a slow-motion budget can be carved out of it. Never asked:
the language of the lines (follows the script), resolution, model, provider,
audio on/off — all rows in the table.

### Skip rows specific to short drama

On top of the generic rows in `creative-brief.md`:

| Signal in the input | Axis | Value |
|---|---|---|
| The language the quoted lines are written in | spoken language | that language — **never asked**; see "Prompt language follows the audio" |
| Stage directions in the script ("crying", "slams the door", "deadpan") | emotional arc | build the arc from them |
| A tone adjective ("tense", "tender", "bitter") | emotional arc | build the arc from it |
| A camera word ("handheld", "locked off", "slow push", "over the shoulder") | camera register | held take, with that word as the movement value |
| A traversal word ("walks with her", "follows him through", "one take", "no cuts", "out onto the street") | camera register | travelling one take |
| A cutting word ("cut between", "intercut", "shot list"), or a numbered storyboard in the input | camera register | multi-shot cut list, at the count the input implies |
| An image attached to the request | asset question | settled; see "Reference images and real people" for the route it takes and the real-person refusal |
| The request names where the runtime should go ("mostly the fight", "linger on the ending", "keep it snappy") | duration split | as stated; see "Duration budget" below |
| The request rules slow motion or a freeze frame in or out ("no slow-mo", "give me a freeze on the hit", "keep it at full speed") | slow motion / freeze | as stated |

### Every answer lands somewhere

| Answer | Where it goes |
|---|---|
| Beat | which lines and actions the timeline covers; the `--name` |
| Aspect | `--aspect-ratio` |
| Arc | the `ARC` arrow chain in the header and the 1–3 signals in each shot |
| Camera register | how many `SHOT` blocks there are and how long each runs, which kinds appear on the `TRANSITION` lines, the movement field of the `CAMERA` line, and each shot's size / position / movement |
| Lines over budget | `--duration`, or the trimmed lines shown in the recap |
| Drafts | `batch` on `bytedance/seedance-2.0-mini` at 480p, or a single `generate` |
| Pacing | the per-shot lengths and the `SHOT` count given to setup, core and close, per "Duration budget" below |
| Effects | whether a shot's action line or `TRANSITION` carries a speed ramp or a freeze frame, and how many seconds it spends |

### The recap for this scenario

```
Brief
- Beat: the kitchen confrontation — "Where were you last night?" (your choice)
- Aspect: 9:16 (inferred from "for Reels")
- Arc: composed → hears the excuse → wavers → wry smile → "We're done." → steps back (AI's pick)
- Camera: multi-shot cut list — six shots of about 2.5s, breathing handheld; occlusion into shot 4, hard cuts elsewhere (your choice)
- Pacing: most of the runtime goes to the confrontation itself; setup and close stay brief (your choice)
- Effects: one slow-motion beat on the final line, capped at about 2s (AI's pick)
- 720p, 15s, byteplus, audio on (defaults — rows in the table below)
```

Then the full prompt, then the table `approval-gate.md` specifies, all in one
message.

## Prompt template

Load these sections of `../ofox-video-core/references/prompt-structure.md`
first: "Prompt skeleton: header manifest, timeline, closing block",
"Segmenting the timeline", "Camera language", "Consistency locks and the
negative list", "Dialogue and sound", "Endings". The vocabulary — shot sizes,
movements, transition phrases, negative-list items — lives there and is not
repeated. What follows is the short-drama shape laid over that skeleton.

Gallery evidence for the shape: the eight short-drama prompts (cases 1–8) are
the only category timestamped 8 of 8. Of the 11 short-drama and talking-head
prompts, 8 carry a capture-medium style anchor and 8 carry a negative list —
two overlapping sets of eight, not the same eight. 6 of the 8 prompts with
dialogue attach a delivery note. Chinese-language cases are quoted in
translation.

### 15–30 seconds: one or several shots

Slots in `<angle brackets>`; optional lines in `[square brackets]`. Two to
five seconds per shot; most shots carry no line.

```
[FORMAT: <ratio>, <T> seconds, <N shots, hard cuts on the timestamps | N shots, transitions named on the timeline | one continuous shot, no cuts>]      — optional; must match the flags
STYLE: live-action, <colour 35mm film grain | phone or mirrorless realism, slight sensor noise>, <light: soft cool key from front-left, warm rim from behind | tungsten practicals>, <palette or grade>.
<TAG A>: <age range, build>, <hair>, <clothing item by item, colour + material — "grey turtleneck knit top, small gold hoops, thin chain">, <one bearing word>. Referred to as "<tag A>".
<TAG B>: <same fields> — or: heard only, never shown | seen only as a dark, heavily out-of-focus shoulder at frame right.
SCENE: <place, time of day, light direction and colour temperature, one foreground element, weather or room tone>.
ARC: <state 1> → <what she hears or sees> → <wavering> → <the cover: wry smile, looks down> → <the line that turns it> → <the exit action>.

SHOT 1 (0–<a>s): <shot size, camera position, movement>. <tag A> <one action — at most 1–3 visible signals: eyes, hands, breath>. [<Tag B> (off-screen, <tone>): "<line>".] <sound for this beat>
<TRANSITION — name a kind on purpose; a hard cut is one of nine, not the default: HARD CUT. | Without cutting, <the swinging door / his shoulder / a passing body> sweeps across the lens and the camera comes out of the occlusion on <the next view>. | Without cutting, the camera pushes through <the doorway / the beaded curtain / the gap between the machines> into <the next space>. | Without cutting, <what changes the framing: she steps back; the camera drifts>. | <nothing here — one continuous shot, declared in the first sentence instead>>
SHOT 2 (<a>–<b>s): … [<Tag A> (<tone>): "<line>" — <delivery: quiet, no anger; on "<word>" the eyes steady>.]
SHOT <N> (<x>–<T>s): … <ending state: hold on her face for one second | hard cut to black at the peak | the camera settles and the clip runs on a moment>.

CAMERA: <movement — not optional, and `static` is one of its values rather than the absence of one: locked with a breathing sway | close handheld follow just behind and beside her | slow push from the two-shot into a close-up | a half-turn orbit | travels with her from <space 1> through <space 2>; state it per shot when it changes>, <lens: 70–100mm medium telephoto | 24mm wide>, <depth of field>, focus stays on <tag A>'s eyes; <axis rule: one eye-line axis, never crossed>.
SOUND: <room tone>, <two diegetic sounds tied to actions: door click, fabric>; music <none — the default here, since asking this model for a scored cue has failed output moderation on audio copyright (unbilled); see "Asking for music can fail output moderation on copyright" in the shared file | enters at <t> | drops out at <t>, only if the user accepts that same risk>. Dialogue in <language>, mouths matched to it.
CONSISTENCY: <tag A>'s face, hairstyle, <accessory>, <clothing items> identical in every shot; <tag B>'s <items>; positions and light direction do not change.
AVOID: subtitles, on-screen text, watermarks; extra or warped limbs; CGI look, plastic skin, skin smoothing; <the cuts you forbid: jump cuts, dissolves | shot/reverse-shot when one continuous shot>; theatrical over-acting, sudden tears.
```

What each short-drama slot is for, and where it comes from:

| Slot | Why it is here | Cases |
|---|---|---|
| `ARC` arrow chain | Five or six states in a row give the model a path rather than a mood; each shot then owns one step of it | 3 (`tense preparation → hears the familiar greeting → brief wavering → wry smile as cover → resolute declaration → restrained exit`), 8 |
| 1–3 visible signals per shot | More reads as over-acting; the gallery's most controlled performance prompt caps it and bans the tear | 3, 20 |
| Delivery note on every line | Volume, tone, accent, and what the face does on which word — present in 6 of the 8 dialogue prompts | 3, 7 (`controlled and intimate, not theatrical`), 22 (`confident Australian accent`), 5 |
| Off-screen or unseen partner | A voice without a face, or a silhouette kept out of focus, is cheaper to keep consistent and stronger dramatically | 3 (the man is heard off-screen and seen only as an out-of-focus shoulder), 21 (`cut to the voice only … as a voiceover`) |
| Two people told apart by wardrobe colour blocks | Case 7's four characters are `cobalt trench / rust knit polo / faded green workwear / pale gray suit` and nothing else, and stay distinguishable | 7, 1 |
| Ending state | Stated in 6 of the 11: freeze, black, `End on …`, the camera settling | 4 (`hard cut to black at the peak of suspense`), 5 (`the frame freezes`), 7, 8 |
| Separate `SOUND` block | Room tone plus two or three sounds keyed to actions; music in and out points | 3, 4, 7, 6 |
| `TRANSITION` line between shots | Nine kinds exist and only one of them is a cut; naming a kind is what stops a timeline from becoming a list of held frames spliced together | 2 (the back-flags sweep past the lens and the camera comes out on the other actor), 3 (she is revealed from behind his out-of-focus silhouette), 8 (an ice crevice and a roof each carry one transition), 7 (`Cut to` / `Cut back inside`) |
| `CAMERA` movement field | The camera has to be doing something specific, even when that something is holding still; without the field the prompt tends to come back as "locked, no push, no zoom" in every shot | 6 (`close handheld follow shot, staying just behind and slightly beside her`), 8 (a movement phase per segment), 2 (orbit into the next actor), 3 (locked, deliberately) |
| `AVOID` — the short-drama items | subtitles / text / watermarks (6 of 11); CGI or plastic skin (1, 4, 20); over-acting (3, 20); the transitions you are not making (3, 8). **Its text items are a backstop, not a defence** — a period or festival setting (a neon street, a courtyard at New Year, a shopfront) needs the lettered surfaces composed out of the shots themselves, per "Unwanted text is designed out of the set, not forbidden in the list" in the shared file; jobs `41f87ac7` and `036ac3a8` are the two sides of that | 4, 5, 20 |
| Clothing with colour and material | The one appearance field every gallery prompt that describes a character writes; age, build, hair, eyes appear as needed | 1, 3, 4, 5, 7, 8 |

Camera choices that recur in this category, all in the shared "Camera
language" tables: over-the-shoulder at the partner's eye height, held (case
3); a fixed close-up where the reframing comes from an actor stepping back,
not a zoom (3); a close handheld follow that stays just behind and beside (6);
a frontal medium two-shot with a slow push into a close-up (1, 22); `do not
cut to shot/reverse-shot` when the point is one held take (3). The travelling
end of the same tables: a slow orbit of the upper body that carries into the
next actor (2); a close handheld follow that struggles through the same crowd
she does, then releases and settles at her level (6); one movement phase per
segment, written out as its own block — `low-altitude rear FPV pursuit`,
`smooth three-quarter rear tracking`, `continuous rise into a high-angle
wide` (8).

### Choosing a transition, not defaulting to a cut

The shared "Transitions" section holds **nine** kinds with the exact phrasing
to copy for each: hard cut; one continuous shot with cuts forbidden;
occlusion; pass-through; morph; flash; match cut; speed ramp; narrative
ordering words. Load it and pick one per boundary. Four of the nine have
short-drama instances among the 63 prompts:

| Kind | Short-drama cases |
|---|---|
| Hard cut | 1 (nine numbered shots), 4, 5, 7 |
| One continuous shot, cuts forbidden | 2, 3, 6, 8 |
| Occlusion | 2, 3, 8 |
| Pass-through | 8 |

The other five — morph, flash, match cut, speed ramp, narrative ordering
words — appear only outside this category (ads, fashion, fight and
music-video prompts). Borrowing one is a deliberate choice, not a documented
short-drama convention; say so in the recap if you do.

A boundary with no transition kind named is not neutral. It renders as a
hard cut, so a timeline of `SHOT 1 … SHOT 2 … SHOT 3` with nothing between
them is a cut list whether or not that was the intent — the same mistake as
leaving the `CAMERA` movement field empty, one line further down.

**Naming a `HARD CUT` is not a guarantee it renders as one, and the reason is
the rest of the timeline, not that boundary alone.** Six
`bytedance/seedance-2.5` jobs now bear on this, four of them short drama.
Ordered by how large a share of the boundaries were written as hard cuts:

| Hard-cut share | Job | Hard cuts that rendered as cuts |
|---|---|---|
| 3 of 9 | `4e5c9581-d462-443b-9663-b1aa6d72f527` (30s) | **0 of 3** — the whole clip read as one continuous flow |
| 3 of 8 | `844c9145-9b10-4335-9fdc-ec4937793a2f` (30s) | 3 of 3, within about 1.5s of their stamps |
| 3 of 6 | `036ac3a8-6f68-47ad-a553-86a29aa3e5b8` (20s) | 3 of 3, all seven shots in the written order |
| 5 of 7 | `41f87ac7-d7a6-4c8c-8efd-feb7bdc4818d` (20s) | 5 of 5 |

The two commerce jobs at 4-of-4 and 6-of-6 kept every cut as well. So the
direction is settled even though the threshold is not: **a boundary's
rendering is not decided independently of the rest of the timeline, and
weighting the mix toward hard cuts is what buys a cutting rhythm.** Five
consistent samples against one is enough to act on; the gap between 3-of-8
(held all three) and 3-of-9 (held none) is a single boundary, so nobody knows
where the line is, and the trigger could still be the boundary count, the
resolution or the particular transition kinds. The full reading is under
"Several shots in one job" in
`../ofox-video-core/references/prompt-structure.md`.

Two working rules follow. **Write hard cuts as at least half the boundaries
when the beat needs a cutting rhythm**; if the brief's `Camera` answer was
the cut list, that is what it asked for. And **check the draft by reading
frames, not by counting a scene detector's hits** — at threshold 0.3 the
detector misses a cut between two shots in the same place under the same
light, which is exactly what shot/reverse-shot is. It missed the single most
important cut in each of two accepted clips: `41f87ac7` at 9.5s (his
close-up to hers) and `036ac3a8` at 9s (the mother's close-up to the son's),
both plainly visible frame by frame. "Checking the cuts: read frames, never
a detector count alone" in the shared file has the method.

What none of this establishes: whether the softened cuts are what made the
30-second clip above read, in the repository owner's words, as not well
connected — that is a plausible follow-on hypothesis, not a tested finding,
and this repo has no measurement of viewer-perceived coherence to test it
against.

### Shot density — pick a register, then count

The register comes from the brief's `Camera` answer; the shot count follows
from the register and the duration. Per-case measurements behind this table
are in "Shot density, measured per case" in the shared file; these are the
short-drama targets read off them.

| Register | Per shot | 20s | 30s | Measured on |
|---|---|---|---|---|
| **Held take** — one or two faces, the camera stays put | performance beats of 1–3s inside one frame, no cuts | 1 shot | 1 shot | case 3: eight beats in 15s |
| **Travelling one take** — no cuts; the camera moves through the space and an occlusion or a pass-through carries each new view | 5–8s a phase, each phase arriving somewhere the previous one could not see | 3–4 phases | 4–5 phases | case 2: 3 phases in 20s; case 6: 4 phases and three spaces in 30s; case 8: 5 phases and four locations in 30s |
| **Multi-shot cut list** — a new size and position at every stamp | 3–5s | 4–6 shots | 6–9 shots | case 1: 9 shots in 30s; case 18: 8 in 30s; case 22: 6 in 30s |
| **Spectacle, beat-driven** — cuts on the action, the line or the music | 2–3s | 7–10 shots | 10–13 shots | case 11: 10 shots in 24s; case 34: 13 cuts in 30s |

Frequency is not effect: these are counts from prompts good enough to be
collected, not a measured relationship between shot count and how good a
clip is. What they do settle is the floor. **Four 5-second shots in a
20-second clip is the slowest point on this table** — and if each of those
shots also holds the camera still, the result is a slideshow of held frames
that renders exactly as written. Measured here on 2026-09-03, job
`38ca8311-5b2d-47d5-a45d-e8ebea0e6312` (20s, 480p, four static shots, cuts
landing on 5/10/15s as written, consistent characters, clean Mandarin
delivery): technically correct on every axis and discarded for being plain.
That run is why this subsection and the `Camera` register question exist.

**The one-take rows have a floor of their own, and it is about movement, not
shot count.** A single 20–30 second take needs the camera to *travel* — cases
2, 6 and 8 cross a stage, three club rooms and four locations respectively.
Measured against that on 2026-09-04: job
`16023efe-48d6-45fe-8fd8-f5c6fbfe6519` (20s, 720p, one continuous shot, zero
detected cuts, characters stable throughout) was rejected as too static,
because its whole movement plan was one very slow push while the actors held
a standing position. So when writing this register:

- give each 5–8s phase **a view the previous phase could not see** — through a
  doorway, past an occlusion, around a corner, from the other side of a room;
- write the movement as travel (`the camera walks with her out of the kitchen
  and into the corridor`), not as distance-closing (`a very slow push`). A
  push is a beat inside a phase, never the plan for the take;
- if the beat genuinely happens in one place on one face, the register you
  want is the **held take** with performance beats — that is what case 3 is,
  at 15 seconds, and it does not pretend to travel.

Cut counts here are inside the measured envelope: 10 shots in 30 seconds, and
up to 6 hard cuts in one job, have both been run on Ofox ("Shots, cuts and
jobs" above). The `spectacle` row's 10–13 cuts in 30s is still gallery practice —
price a first attempt as an experiment — and on every register, check where
the cuts actually landed on a 480p draft, **by reading frames rather than a
detector count**, before paying for the final.

### Duration budget — spend the seconds where the beat is

Shot density says how many shots and how long each one runs; it says nothing
about which shots the story actually needs seconds for, and a clip can obey
every row of that table while still spending more than a third of its
runtime on the parts nobody came to watch. Measured on job
`4e5c9581-d462-443b-9663-b1aa6d72f527` (30s, 720p, ten shots, 3.0s each,
$7.20, accepted but flagged): a 2.5s stand-off, six shots of close-quarters
combat, one 4.5s decisive-strike shot carrying a speed ramp and a freeze
frame, then 7 seconds — close to a quarter of the clip — spent recovering
breath and settling into a stand-down that mirrors the opening shot. The
repository owner's own words on it: "why is 20 to 30 seconds so plain? Don't
compress the best part just to make room for the ending — the ending took
10 seconds, most of it should be the fight." The uniform 3.0s-per-shot
average that produced this — every shot the same length, none longer or
shorter than any other — is itself part of the problem: it is the same
flattening shape "Shot density" already warns against for a static camera,
just spread across duration instead of across shot count.

**Budget by function, not by shot count**, and check the numbers add up to
the duration before writing a single shot:

| Register | 20s | 24s | 30s |
|---|---|---|---|
| **Action / spectacle** — a fight, a chase, a stunt; the beat's payoff is the middle of the clip, not the last shot | setup ~1.5s, core ~15s, close ~3.5s | setup ~2s, core ~19s, close ~3s | setup ~2s, core ~24s, close ~3–4s |
| **Dialogue / slice-of-life** — an exchange that lands on a line or an action; the beat's payoff can legitimately be the last shot | setup ~3s, build ~12s, close ~5s | setup ~3.5s, build ~15s, close ~5.5s | setup ~4–5s, build ~17–18s, close ~6–8s |

The two rows are not the same rule with different numbers — they encode
where the payoff sits. An action beat's payoff is the fight itself, so the
close is a stand-down after it rather than the destination, and stays the
smaller number. A dialogue beat's payoff is often the final line or gesture,
so its close is allowed real weight: job
`844c9145-9b10-4335-9fdc-ec4937793a2f` gives its last shot the
sitting-down-and-eating beat the whole scene has been building to, and that
is the close doing its job, not padding. Pick the row that matches the
beat's `Arc`, not the clip's genre label — a dialogue scene that resolves
mid-clip and coasts to a static hold behaves like the action row.

**Slow motion, speed ramps and freeze frames spend real seconds and have to
come out of this budget, not sit outside it.** The 4.5s decisive-strike shot
above stacked an extreme speed ramp into a flash-freeze into a resume — three
effects on one action — to cover what a single clean strike needed about
half that time for. Cap it: **no more than about 2–3 seconds of
slow-motion/freeze/speed-ramp effect, total, across a 30-second clip**
(scale down for shorter clips — roughly 1.5–2s at 20s, 2–2.5s at 24s), and
default to using the device **once**, on the single best beat, not on every
hit. A second use is defensible only when each instance stays under about
1.5s.

**A symmetrical bookend — the last shot mirroring the first — is a
deliberate flourish, not the default shape of a close.** It reads well (the
`ARC` line and the shared file's `Endings` section both support it), but it
is not free: in the job above it cost the close roughly half its budget on
two static, held shots that do nothing but face each other. If you use it,
its seconds come **out of** the close row above, not on top of it — a
mirrored bookend in a 30s action clip should still leave the close at 3–4s
total, split between the two bookend shots, not 3–4s each.

**"The best part gets more shots and more description" is an instruction
about density, not just enthusiasm — apply it unevenly on purpose.** The
counter-example is exactly what produced the flagged clip: ten shots
averaging 3.0s each, uniformly, so the six-shot melee in the middle got the
same per-shot allowance as the stand-off that opened it and the stand-down
that closed it. The fix is not more shots overall — it is fewer, longer
shots outside the core and more, shorter, more specifically described shots
inside it: one shot for the setup, one or two for the close, and the core
written at the dense end of "Shot density" (2–2.5s a shot, one distinct
action verb per shot) while the shots around it sit at the loose end
(4–6s). A prompt where every shot is the same length is easy to write and
hard to notice is flat until the clip is already paid for.

### Dialogue budget — two tiers

| Tier | Budget | What the gallery measured |
|---|---|---|
| **Dialogue drama** — two people, an exchange | **0.4–1.7 words/s over the clip**; one 2–4s beat may peak at 3.5–5. Treat 2–3 words/s as a ceiling, never a target — most seconds carry no line | case 3: 6 words in 15s; case 1: 51 words in 30s; case 7: 43 words in 30s |
| **Monologue / talking head** — one person to camera | **3.5 words/s English; 5 characters/s Chinese or Japanese** | case 22: 103 words in 30s; case 20: 50 characters in 10s |

A script that overruns its tier is the brief's `Lines` question: extend the
duration (within 30s) or trim and show the trimmed lines in the recap.
Compressing the delivery is what produces rushed, garbled speech.

### Two worked examples, two registers

Both are legitimate short drama and the brief's `Camera` answer picks between
them. The first is the restrained end: one held take, one face, six spoken
words in fifteen seconds. The second is the dense end: nine shots in
twenty-four seconds, a space the camera travels through, and something other
than a hard cut at three of its eight boundaries. Writing the first when the beat
wanted the second is this skill's most likely failure, because it fails
quietly — every rule obeyed, nothing to look at.

### Worked example 1 — adapted from case 3 (translated): 15 seconds, one continuous shot

The original attached a photo of the actress; on Ofox that is refused (real
person), so this version carries her in text. Six spoken words in fifteen
seconds — this is what the drama tier looks like in practice.

```
STYLE: live-action, natural light, soft cool-white key from about 45 degrees front-left, a little warm gold rim from behind; real skin texture, no smoothing; nothing theatrical in the lighting.
HER: woman around 30, slim, dark hair in a low knot, small silver hoops and a thin chain, grey turtleneck knit top; composed, tired. Referred to as "her".
HIM: heard off-screen; seen only as a dark, heavily out-of-focus shoulder and jaw at frame right, never in focus, never turning to camera.
SCENE: an apartment doorway at dusk; she is inside, he has just opened the door; quiet street tone outside.
ARC: braced → hears the familiar greeting → a flicker of the old warmth → wry smile as cover → "We're done." → one step back.

One continuous shot, 15 seconds, no cuts, no shot/reverse-shot.
0.0–0.8s: The door opens toward camera; the frame is mostly his dark blurred shoulder; she is revealed behind it, chest-up, centred slightly left, eyes down.
0.8–3.2s: Him (off-screen, casual, a smile in it): "Hey, what's up, baby?" Her eyes lift to his; one slow blink. Sound: door click, fabric.
3.2–6.0s: A half-breath. The corner of her mouth moves — the start of a smile that does not arrive. Nothing else moves.
6.0–9.5s: Her (very quiet, very clear, no anger): "We're done." A short intake of breath before it; "We're" still carries warmth, on "done" the eyes steady.
9.5–13.0s: Lips close. She holds his look a full second, then one step back; the framing loosens from close to medium close-up because she moved, not the lens.
13.0–15.0s: She turns her head a few degrees away. Hold. Room tone only; no music.

CAMERA: over-the-shoulder from behind his right shoulder at her eye height, 70–100mm equivalent, shallow depth of field, focus locked on her eyes throughout; his outline stays out of focus at frame right; one eye-line axis, never crossed; no push, no zoom, at most a faint breathing sway.
SOUND: door hinge, knit fabric, distant street; no score. Dialogue in English.
CONSISTENCY: her face, hair knot, hoops, chain, grey turtleneck and apparent age identical throughout; his position and the light direction do not change.
AVOID: subtitles, on-screen text, watermarks; tears rolling, hysterics, exaggerated frowning; shot/reverse-shot, fast push-ins, orbits, sudden zooms, multi-camera switching; plastic skin, beauty filter.
```

### Worked example 2 — adapted from case 1 (translated): 24 seconds, nine shots, four kinds of transition

Case 1 is the official nine-shot storyboard: 30 seconds, a shot every 3.3
seconds, a new size and camera position at every stamp, a line in almost every
shot. This version keeps that ladder, writes the manifest in the `Uppercase
labels` style this skill's template uses (case 1's own is bracketed section
headings), moves the beat into a space the camera can travel through, and
varies the transition instead of cutting eight times — occlusion once,
pass-through once, a no-cut drift once, hard cuts for the rest. The original
attached one appearance image per character; on Ofox an attached photoreal
person is refused unless the caller asserts the rights to that likeness (see
"Reference images and real people"), so both are carried in text. Eleven
spoken words in twenty-four seconds is 0.46 words/s, the quiet end of the
drama tier — density here is in the shots, not the lines.

**Nine shots in one job is three times the count verified on Ofox** (three
shots in eight seconds). Price a first run at this density as an experiment
and read the cuts off a 480p draft.

```
FORMAT: 16:9, 24 seconds, 9 shots, transitions named on the timeline.
STYLE: live-action, colour 35mm film grain, slight exposure fluctuation; the only light is a phone torch, a green emergency sign and city glow through the stairwell windows — cold white close in, sodium orange far off; deep black shadow, real skin texture, no smoothing.
HER: woman around 30, tall, black hair pushed back and damp at the temples, a grey hooded sweatshirt over pyjama trousers, trainers with the laces loose, a phone held torch-down in her right hand; braced, moving fast. Referred to as "her".
HIM: boy about 12, small for his age, cropped hair, a red school tracksuit top zipped to the chin, one trainer untied, a folded paper kite under one arm; still, watchful. Referred to as "him".
SCENE: an old eight-storey apartment block during a night power cut — a tiled ground-floor lobby with a dead lift, a concrete stairwell with a window at every landing, a top landing whose steel door stands open, and a flat roof with the dark city and one lit crane behind it; warm summer night, no wind at ground level, wind on the roof.
ARC: she comes in already looking → the lift is dead → she starts up → the torch finds one untied trainer on a step → she climbs faster → the roof door is open → she sees him at the parapet → she does not shout → she sits down beside him.

SHOT 1 (0-2.5s): Wide, low, from just inside the lobby door, camera locked. She comes in fast from frame left, presses the dead lift button twice, turns to the stairwell without waiting. No line. Sound: the door swinging, the fly-buzz of the emergency sign, no lift motor.
Without cutting, the swinging lobby door sweeps across the lens and the camera comes out of the occlusion on the first flight of stairs.
SHOT 2 (2.5-5s): Medium from behind, close handheld follow just behind and beside her on the first flight; the torch beam jumps across the wall and the handrail. No line. Sound: two sets of steps doubling in the shaft, her breath.
HARD CUT.
SHOT 3 (5-7.5s): Extreme close-up, torch-lit: one untied trainer lying on a step. Her hand enters frame and lifts it. Her (quiet, not calling out): "Bo?" Sound: the shoe leaving the concrete, nothing answering.
HARD CUT.
SHOT 4 (7.5-10s): Low angle straight up the stairwell shaft, three flights receding into the dark; she climbs past the lens fast, the torch swinging. No line. Sound: steps accelerating, a handrail knock.
Without cutting, the camera pushes through the open steel door into the night.
SHOT 5 (10-13s): Wide on the roof, the dark city behind, the one lit crane at frame right; he stands at the parapet with the kite under his arm, back to us, small in the frame. No line. Sound: the wind arrives, the shaft noise stops.
HARD CUT.
SHOT 6 (13-15.5s): Medium single on her in the doorway, chest-up, locked, breathing hard; she does not shout. Her (very quiet): "I am not angry." Sound: wind, her breath.
HARD CUT.
SHOT 7 (15.5-18s): Close-up single on him, three-quarter, the crane light along one cheek; he keeps looking out, not at her, and his grip on the kite tightens. No line. Sound: wind, paper flexing.
HARD CUT.
SHOT 8 (18-21s): Two-shot from behind at parapet height; she enters frame and stops beside him without touching him, both looking out. Him (small, flat): "You could have knocked." Her: "I know." Sound: wind, fabric, one far siren.
Without cutting, the camera drifts back and down to the roof surface.
SHOT 9 (21-24s): Wide, low, from the roof floor: the two of them in silhouette against the crane light; she sits down first, he sits a second later, the kite across his knees. Hold the silhouettes for the last second. Sound: wind only; no music.

CAMERA: movement per shot, and `locked` is a value here rather than a default — locked in 1, close handheld follow in 2 and 4, locked singles in 6 and 7, a slow drift back and down in 8 into the low wide of 9; 28mm in the stairwell and on the roof, 70mm for the singles; shallow depth of field on the singles, deep on the wides; the torch is the only key below the roof; the eye-line axis between the two of them is set in shot 5 and never crossed.
SOUND: a dead lift, a buzzing emergency sign, two sets of footsteps in a concrete shaft, a shoe lifted off concrete, roof wind arriving at 10s, fabric, paper, one far siren; no music at any point. Dialogue in English, mouths matched to it.
CONSISTENCY: her face, pushed-back black hair, grey hooded sweatshirt, pyjama trousers and loose trainers identical in every shot; his face, cropped hair, red zipped tracksuit top, one untied trainer and the folded paper kite identical in every shot; the power stays off, the torch stays in her right hand, the crane light stays at frame right on the roof.
AVOID: subtitles, captions, on-screen text, watermarks, logos; extra or warped limbs, warped hands; CGI look, plastic skin, skin smoothing; dissolves, jump cuts, shot/reverse-shot, sudden zooms, whip pans, crossing the eye-line axis; the lights coming back on, anyone climbing onto the parapet, anyone falling, shouting, tears rolling, hugging.
```

### 10 seconds or less: one shot, no manifest

No header — the vendor's formula order in three or four sentences (no gallery
prompt of 10s or less carries a manifest). The micro-beats are performance
beats inside the one shot, so say `fixed camera` or `one shot` to keep them
from reading as cuts.

```
<Tag>, <appearance in one clause — hair, top with colour>, <place and light>. <Shot size — chest-up medium close-up>, <fixed camera | faint handheld>, <background softness>; <capture medium: real phone or mirrorless texture, slight sensor noise>.
<Tag> faces <the camera | someone off-screen> and says, <tone>: "<line — talking-head tier: up to 3.5 words/s English or 5 characters/s Chinese; drama tier: far fewer>".
0–<a>s: <eye contact, a blink>. <a>–<b>s: on "<word>", <one gesture: a small head shake>. <b>–<c>s: <second gesture>. <c>–<T>s: after "<last word>", <ending: lips close, half-second pause | the smallest nod>.
Natural blinks, breath, micro-expressions, real skin texture; mouth matched to <language>. No presenter cadence, no over-acting, no smoothing, no filters, no camera movement, no subtitles, no on-screen text.
```

Adapted from case 20 (translated), 10 seconds, 9:16 — 19 words in ten
seconds, inside the talking-head tier:

```
A woman in her late 20s, straight dark hair past the shoulders, plain oatmeal knit sweater, in a bright home study; soft window light from front-left, a bookshelf softly blurred behind her. Chest-up medium close-up, fixed camera, no movement; real mirrorless texture with slight sensor noise, like a knowledge creator filming herself.
She faces the camera and says, conversational, unhurried: "People think AI understands you. It doesn't. It predicts the next word — and that turns out to be enough."
0–2s: she looks straight into the lens, one natural blink. 2–5s: on "It doesn't" a single light head shake. 5–8s: one hand enters low in frame for a small open-palm gesture on "predicts". 8–10s: after "enough" her lips close and she gives the smallest nod.
Natural blinks and breath, real skin texture, mouth matched to English. No presenter cadence, restrained hands, no smoothing, no influencer filter, no dramatic lighting, no camera movement, no subtitles, no watermark, no on-screen text.
```

### Reference images and real people

Both meanings of an attached image ("Reference assets as visual anchors" in
the shared file) run into the same check in this scenario:

- `--frame-first-image` / `--frame-last-image` with a photoreal person is
  refused by `bytedance/seedance-2.5` at submission
  (`input_moderation_failed`; verified 2026-08-30; nothing billed).
- The identity-reference route (`input_references` through `--extra-json`)
  has **not been tested with a real person in this repo either way** — do not
  assume it passes.
- `--real-person true` **does lift that refusal on 2.5** — measured
  2026-09-16. It is Ofox's privacy-preserving preprocessing path for
  real-person references the caller is **authorised** to use: an
  authorisation route, never a way past the check. Offer it only when the
  user holds the right to that person's likeness and has said so, never as a
  retry after a refusal, and never set it on their behalf. Evidence and every
  limit on it:
  [`../ofox-video-core/references/api-params.md`](../ofox-video-core/references/api-params.md)
  → "`--real-person true` lifts that refusal on 2.5".

For fictional characters, props, storyboards, or environments supplied as
several images, use the shared
[`Identity-reference recipe — the authoritative copy`](../ofox-video-core/references/prompt-structure.md#identity-reference-recipe--the-authoritative-copy).
It covers the gallery shape behind cases 1 and 2 without pretending that
their four-image and non-character combinations were tested here: only two
images have been exercised, while the API ceiling is nine. Keep the JSON
array and canonical `@image1`, `@image2` labels in the same order, and state
what each asset supplies and what the model must ignore.

**That opens a door this scenario has not walked through.** What was measured
is a single 4-second 480p image-to-video job on one first frame, with a
*synthetic* portrait, on `byteplus`. A short drama is the opposite shape:
several shots, minutes of screen time, the same face required in every one of
them, and — if the user brings a photograph — a real person rather than a
generated one. Nothing here has measured a face holding across two jobs, so
the default stands.

A short-drama character's consistency across jobs is text: the same
appearance block word for word, plus the `CONSISTENCY` line. If a user
attaches a photo of a real person anyway, say what will happen before
spending anything, and confirm they have rights to the likeness — which is
the same precondition the flag asserts, and the reason it is a conversation
rather than a setting.

### Continuing a scene across jobs, when no frame can be attached

The refusal above closes the frame route for this scenario in practice: the
rest of the repo continues a clip by attaching its last frame, and a frame
holding a photoreal person is refused unless the caller asserts the rights to
that likeness — which is a claim about a real person, not something an agent
makes on a user's behalf, and which no measurement here has taken past one
4-second clip. So when scene 3 has to open where scene 2 closed, the
instrument to reach for is **the words route** — case 44's
continuity block, described and measured under "Continuing a previous clip:
the frame route and the words route" in
`../ofox-video-core/references/prompt-structure.md`. Load that subsection; the
measurement is not repeated here.

Its shape, adapted to a dialogue scene:

```
CONTINUITY: this is part <N>, continuing directly from part <N-1>. Part <N-1>'s
final image, restated: <who is where in the frame — foreground/background, near/far>,
<what each is wearing, itemised>, <the objects that must still be there and where>,
<the light and the time of day>, <the emotional state each was left in>.
No re-staging, no re-introduction, no settling in — <the tag> is already <the action
in progress> on the first frame.
```

Two things follow from the measurement, and they change how you write the cut
rather than how you write the block:

- **Staging, wardrobe, props and palette come back; an exact pose and the
  camera's distance do not.** So write the continuation so it does not depend
  on matching a pose — pick up on a line, a prop or a position in the room,
  not on the tilt of someone's head. If the two clips genuinely must match on
  a pose, the honest answer is that this route will not deliver it.
- **The "no re-staging" half is a prohibition on a tempo, and those are soft.**
  The measured run still opened with about two seconds of near-static
  preparation. Give the first beat its own timestamp and write it as an action
  already underway (`[0–3s] mid-sentence, she is already turning away from
  him…`) — that does more than the prohibition does.

One limit worth stating to the user before they pay: the run behind those
findings (`c2eb32e1-3b54-4a56-8d78-86e63bc355c7`) was an **anime** continuation,
not a live-action one. The mechanism is the prompt, not the art style, and
nothing suggests it would differ — but no live-action continuation has been
measured in this repo, so a first one is an experiment and worth pricing as
one.

## Recommended defaults

| Parameter | Default | Why |
|---|---|---|
| `--model` | `bytedance/seedance-2.5` (script default, no flag needed) — **unless the user named a different model**, which always wins | current-generation model; see "Choosing a video model" for the other two options |
| `--duration` | `10`; match the user's stated length; when the brief settles on several shots, sum 2–5s per shot | enough room for a short exchange; Seedance 2.5 accepts 4–30 |
| `--resolution` | `720p` — a `seedance-2.5`/`wan-3.0-prime` value. On `minimax/hailuo-3` use `768p`: that model has no `720p` tier | realistic detail on faces and lip movement at a reasonable cost; `1080p` only for a hero shot the user will publish |
| `--aspect-ratio` | whatever the brief's `Aspect` answer was; `9:16` when that question was skipped, delegated or never asked | short drama is consumed vertically on mobile feeds. Note the gallery's own short-drama sample skews landscape — 5 of the 6 cases that state a ratio are 16:9 (1, 2, 3, 7, 8) — so the default is about the audience, not about what the gallery did |
| `--generate-audio` | `true` (server default, no flag needed) | dialogue needs an audio track — never set this `false` for a scene with spoken lines |
| `--real-person` | leave unset (`false`) | see "Reference images and real people". A text-described character never needs it, and this skill's answer to a user who brings a photograph is `talking-head`, not this flag. `true` is Ofox's privacy-preserving preprocessing path for **authorised** real-person references, measured lifting 2.5's refusal on 2026-09-16 — an authorisation route, never a way past the check, and never set on a user's behalf. What was measured is one 4s 480p first-frame job on a synthetic portrait; a multi-shot drama carrying a real face is outside it. See [`api-params.md`](../ofox-video-core/references/api-params.md) → "`--real-person true` lifts that refusal on 2.5" |

Always confirm the actual duration/aspect ratio with the user's request first
(e.g. "15 seconds" in the trigger example overrides the 10s default).

## Choosing a video model

`model` stays **never-ask** — the agent does not raise this as a question of
its own. But never-ask is not "never listen": `bytedance/seedance-2.5` is
only the default because nobody asked for something else. If the user names
a model — an id (`alibaba/wan-3.0-prime`, `minimax/hailuo-3`), or a shorthand
like "wan" or "hailuo" — use that model, not the default. Never silently
substitute `seedance-2.5` for a model the user actually asked for.

| Model | Cheapest tier (catalog) | Max resolution | Duration | Aspect ratios | Real moderation data point |
|---|---|---|---|---|---|
| `bytedance/seedance-2.5` (default) | 480p, 11 cents/s | 1080p | 4–30s | 7, incl. 21:9 | **Rejected** a photoreal-portrait i2v reference (`input_moderation_failed`) and a Re:Zero/Rem-styled anime t2v prompt after it had already generated (`output_moderation_failed`, copyright) — both free, nothing billed. See `.trellis/spec/skills/external-api-integration.md`, "Gotcha: moderation policy is per-model, not a platform-wide constant". |
| `alibaba/wan-3.0-prime` ("wan") | 480p, 6.4 cents/s | 1080p | 2–30s — the shortest minimum of the three, handy for a cheap draft | 6 — no 21:9/9:21 | **Accepted** both of the clips seedance-2.5 rejected above, 12.8 cents each (2s/480p, its minimum). Only these two content classes have been tested — not a general "no moderation" guarantee for this model. |
| `minimax/hailuo-3` ("hailuo") | 768p, 8 cents/s — no 480p tier | 2k, uniquely among the three, at 13 cents/s | 4–15s — the shortest **maximum** of the three, so it's out for anything past 15s | 7, incl. 21:9 | **Accepted** the same two clips, 32 cents each (4s/768p, its minimum). Same caveat: two content classes tested, not a blanket clearance. |

Price, max resolution, duration and aspect-ratio counts are catalog facts —
`GET https://api.ofox.ai/v1/models/catalog`, no API key needed, publicly
re-checkable any time — not results from a real generation. The moderation
column is the one column in this table that came from a real, paid API
call; read it as evidence about exactly those two tested content classes on
that date, not as a blanket policy for either model. One more catalog fact
worth knowing since it bears on moderation: `wan-3.0-prime` runs on two
upstreams (`alicloud`, `aliyun`) and `hailuo-3` on two (`minimax`, `novita`),
neither of which `ofox-video-core` currently pins the way Seedance's
`byteplus`/`volcengine` pin works below. So a job on either of those two
models routes by weight, and a moderation result on one run is not
guaranteed to repeat on the next.

### What changes when the model changes

The defaults table above was written for `seedance-2.5`. Two entries do not
carry over unchanged:

- **`--resolution 720p` does not exist on `minimax/hailuo-3`.** That model
  offers `768p` and `2k` only, so pass `--resolution 768p` there. Sending
  `720p` is rejected by the script locally, before submission, for free — a
  wasted turn rather than a wasted dollar, but avoidable.
- **`--duration`**: `hailuo-3` caps at **15s**, well under this skill's 4–30s
  room on the other two. Re-check the duration the brief settled on against
  the table above before submitting.

`--aspect-ratio` needs no adjustment: it is validated per model, and if a
frame image is ever attached, `ofox-video-core` 1.22.0+ handles the frame's
shape per model and prints a `NOTE:` saying what it did.

## Which upstream renders it

Jobs are pinned to the `byteplus` upstream (ByteDance's platform for markets
outside mainland China). Ofox otherwise picks between it and Volcengine Ark by
weight, and the two moderate differently, so pinning keeps results consistent.
Pass `--provider volcengine` for the mainland platform, or `--provider auto` to
let Ofox choose. Pricing is identical either way. See
`ofox-video-core/references/api-params.md` for the detail.

## Before you spend: the approval gate

**Never submit a paid job until the user has seen a cost table and said yes.**
The rule, the table's required columns, where the numbers must come from, how
to itemise a batch and what to do when no estimate is possible are written
down once, for every Ofox skill in this repo:
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md).
Follow it rather than improvising; everything below is only what this scenario
adds to it.

The numbers come from `--dry-run`, per "Where the numbers come from" in the
shared spec:

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --dry-run \
  --prompt "..." --duration 15 --resolution 720p --out-dir ./out
```

After the yes, re-run the identical command with `--dry-run` swapped for
`--approved` — same prompt, same flags. A prompt edited between the quote and
the run is a new table.

`--approved` is where that yes gets typed out. Since `ofox-video-core` 2.0.0
the four billable subcommands — `generate`, `create`, `batch`, `chain` —
refuse to run without it, while `--dry-run` never needs it, so the quote above
is still free and still works with no API key. Be exact about what the flag
does: it records a stance, it cannot prove one. Nothing in a shell script can
observe the conversation you had, and it can be typed without showing anyone a
price. What it changes is that spending without quoting is no longer the
default — it has to be written into the command, where a transcript shows it.
The rule above is still the rule, and it is still yours to follow.

What this scenario's message needs beyond the table: the **brief recap** (the
block shown above, with `(AI's pick)` and `(inferred …)` marked) and the
**quoted dialogue in full** inside the prompt, since a line silently
rewritten or translated is the most expensive thing that can go wrong here
(see the audio/language note above). One row for the clip at the duration and
resolution you settled on; a second row when the brief's `Drafts` answer adds
a draft batch.

## Several takes to choose from

Video generation is a slot machine — most takes go in the bin. When the user
wants options rather than one clip, use `batch` instead of running `generate`
repeatedly:

```bash
bash ../ofox-video-core/references/ofox-video.sh batch --dry-run \
  --prompt "..." --takes 4 --duration 8 --resolution 480p --out-dir ./out
```

It prices the whole batch up front, stops on the first failure instead of
burning the remaining takes, and produces a contact sheet — three frames per
take, one row each — so the user picks from one image instead of opening N
files. Price it the way the shared gate's "Batches get an itemised table, not
one total" requires: a row per take and `BATCH_COST_TOTAL`.

Hand the user the `CONTACT_SHEET` path on its own line, the same way you hand
over a video — in this flow it is the artifact they actually look at first,
since it is how they pick. Then list the individual take paths beneath it.

Each `TAKE` line carries `seed=N`. That seed is how "take 3 was the good one"
gets written down at all: re-running the same prompt with that seed on a
better model or higher resolution **aims at** that take. It does not return
it — measured 2026-09-15, three submissions of one byte-identical request on a
fixed seed came back as two visibly different clips and one refusal, so this
API is not reproducible even with nothing changed. Say that before the user
pays for the re-render; a promotion is another roll at the same shot.

A single `generate` prints a `SEED` line too, and records it in the clip's
`.json` sidecar along with the resolution and aspect ratio. So "that one was
good, give me it at 1080p" works off one clip — you do not need a batch to
get a handle worth re-submitting.

Worth offering when the user is exploring (the brief's `Drafts` question):
draft cheap on `bytedance/seedance-2.0-mini` at 480p, then render the winner
on `bytedance/seedance-2.5`. Four 8-second drafts cost about 64 cents on mini
versus $7.68 on 2.5 at 720p. But **don't switch models on their behalf** — a
different model is a different look, not just a different price.

## Pricing a job with no API key

**No API key needed** to find out what something costs. All three of these
work with `OFOX_API_KEY` unset:

```bash
bash ../ofox-video-core/references/ofox-video.sh models      # models and rates
bash ../ofox-video-core/references/ofox-video.sh providers   # full price matrix
bash ../ofox-video-core/references/ofox-video.sh generate --dry-run \
  --prompt "..." --duration 15 --resolution 720p             # a real quote
```

So when a user hasn't signed up yet, **quote the job first and let them decide
whether it's worth registering.** Don't open by sending them to a signup form
— price it, show them the number, then point at
[app.ofox.ai](https://app.ofox.ai) if they want to proceed.

## If the script isn't found

```
bash: ../ofox-video-core/references/ofox-video.sh: No such file or directory
```

Nothing is broken — this skill delegates all execution to `ofox-video-core`
and reaches it by relative path, and that path just missed. Two different
situations wear this same message, so run the probe in "Where the core skill
lives" before deciding which one it is:

- **The probe printed a directory** — the core is installed and only the
  directory *name* was wrong, which is the normal LobeHub case
  (`ofoxai-skills-ofox-video-core`). Re-run the command against what the
  probe printed. Nothing needs installing.
- **The probe printed nothing** — `ofox-video-core` really is absent, and
  installing it is the user's call to make, not yours: an install writes
  outside this working directory, so hand over the command and let them run
  it rather than running it for them. Which command depends on the installer
  they already have — skills.sh is
  `npx skills add ofoxai/skills --skill ofox-video-core`, which asks for that
  one skill and answers none of the agent, scope or confirmation questions on
  the user's behalf; this repo's own wrapper is
  `npx ofox-skills ofox-video-core`, the same install with all three answered
  in advance (every agent, user-level, no prompts); on LobeHub or ClawHub,
  install `ofox-video-core` from the same publisher. Ask for the one skill
  that is missing rather than the whole repo, and give all three routes —
  pointing a LobeHub user at the skills.sh line alone reads as "abandon your
  installer", which isn't the advice.

Either way, say which skill is missing and where it is expected rather than
relaying the raw path error, which names neither.

The shared reference files this skill links to go the same way for the same
reason — `prompt-structure.md`, `creative-brief.md`, `approval-gate.md` and
`api-params.md` ship with `ofox-video-core`, not with this skill (a scenario
skill packages only its `SKILL.md` and `CHANGELOG.md`). When the probe found
a core but a link still doesn't resolve, the link is pointing at the wrong
directory name and wants the same substitution; when it found nothing, they
come back with the core. Until then this skill still stands on its own: the
prompt templates, the brief's question table and the defaults are all in this
file. What is out of reach is the detail behind the general rules they point
at — the full vocabulary lists, the wider question-flow rules, and the exact
wording of the spend gate, which stays mandatory either way.

## Exit codes worth knowing

Full table in [`../ofox-video-core/SKILL.md`](../ofox-video-core/SKILL.md) —
the ones that come up:

| Code | Meaning | What to do |
|---|---|---|
| `1` | Parameter rejected locally, no network call, nothing billed | Fix the flag and retry freely |
| `2` | Environment problem — `curl`/`jq` missing, or no `OFOX_API_KEY` | Ask the user to fix it; `check` reports the same |
| `3` | API rejected it, or the job ended failed/cancelled/expired | Read the mapped message; a rejected create was not billed |
| `4` | Timed out waiting — **the job is still running and billable** | `poll JOB_ID`, never re-run `generate` |
| `5` | Ambiguous network failure on create | Do not retry blindly; check https://app.ofox.ai first |
| `6` | `--out-dir` unusable | Fix the path; if it happened after a create, `poll JOB_ID` instead of regenerating |

## How long to tell the user it will take

`generate` blocks while it polls, up to `--max-wait` (default 540s). A short
480p draft is usually one to three minutes; longer or higher-resolution jobs
take longer. Say so before starting, so the wait isn't silent.

If your tool call can't stay open that long, use `create` (submits and returns
a job id in seconds) followed by `poll`, instead of `generate`. That way a
timeout can never strand a job whose id you never saw. For `batch`, the worst
case is `takes x max-wait` — lower `--max-wait` for drafts, or create and poll
each take yourself.

## Where the file lands

Always pass `--out-dir`. Without it the script writes to the current working
directory, which is usually the user's project root. Pick something sensible
(`./out`, or wherever the user asked) and relay the absolute `VIDEO_PATH` the
script prints, on its own line.

Pass `--name` too. You know what the shot is — you just wrote the prompt for
it — so name the file after the beat rather than leaving the script to guess
from the prompt's opening words, which describe the style and the lighting.
The clip lands as `<name>-<short job id>.mp4` with a `.json` sidecar beside
it holding the full job id, the prompt and the real cost.

## Running the script

Paths in the examples above are written relative to **this skill's own
directory**, and they assume the core sits beside it under its own name —
the skills.sh / ClawHub / `npx ofox-skills` layout. "Where the core skill
lives" at the top of this file has the probe for the other layouts;
substitute whatever it printed for `../ofox-video-core`. If you are running
from somewhere else entirely, adjust accordingly — from a clone's repo root
it is `skills/ofox-video-core/references/ofox-video.sh`.

## Generating

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --approved \
  --prompt "<the short-drama prompt built from the template above>" \
  --name "<short beat name, e.g. doorway breakup>" \
  --duration 15 \
  --resolution 720p \
  --aspect-ratio 9:16 \
  --out-dir ./out
```

`--approved` is not decoration: without it the script refuses, submits
nothing, and prints the quote-first steps instead. Add it only once the cost
table has actually gone in front of the user and come back with a yes — the
flag cannot check that for you.

This one call validates the parameters, submits the job, polls to
completion, downloads the mp4, and prints `STATUS`, `JOB_ID`, `VIDEO_PATH`,
`VIDEO_SECONDS`, and `VIDEO_COST`. Report the **actual** values from that
output to the user — never the estimate, and never a path/cost you didn't
see the script print. Do not re-implement any of the request/poll/download
logic here; always call into `ofox-video.sh`.

## Common failure modes and fixes

These are `ofox-video-core`'s documented exit codes and error codes
(full table: [`../ofox-video-core/references/api-params.md`](../ofox-video-core/references/api-params.md)),
plus the short-drama-specific ones:

| Symptom | Cause | Fix |
|---|---|---|
| Exit `1`, no network call made | Bad `--duration`/`--resolution`/`--aspect-ratio`, or missing `--prompt` | Fix the flag per the error message and re-run `generate` — free to retry, nothing was submitted |
| Exit `2` | `curl`/`jq` missing, or `OFOX_API_KEY` not set | Re-run `ofox-video-core`'s `check` and follow its install/signup guidance |
| Exit `3`, `error.code: insufficient_credits` | Ofox balance too low | No charge was made; the user needs to add credits at `https://app.ofox.ai` before retrying |
| Exit `3`, `error.code: input_moderation_failed` on create | An attached frame contains a real person — refused at submission, nothing billed | Drop the image and carry the character in text (see "Reference images and real people"). Do **not** reach for `--real-person true` as the retry: it lifts this refusal on 2.5, but it is how a caller asserts they hold the rights to that likeness, so it belongs to a conversation with the user, never to error recovery |
| Exit `3`, job ends `failed`, or `invalid_request` on create, with no other error code hint | Likely a moderation rejection: prompts describing real/identifiable public figures, sexual content, or graphic violence are commonly rejected before or during generation | Rewrite the prompt: use a generic character description instead of naming a real person, tone down graphic detail, then call `generate` again — this is a **new** request with a new prompt, not a resubmission of the failed one, so it's safe to retry immediately |
| The clip renders exactly as written and still looks like nothing — held frames spliced together, no reason to keep watching | Every shot 5s or longer, every `CAMERA` movement static, and every boundary a bare hard cut: the slowest point of "Shot density — pick a register, then count", reached by writing the template's defaults instead of choosing a register | Re-ask the brief's `Camera` question, take the register the beat actually wants, then rewrite: more shots at 2–3s, or one travelling take, and a named transition kind at each boundary. This is a new prompt, so it is a new cost table |
| Generated speech sounds rushed, garbled, or cut off | Too many words for the clip's tier — see "Dialogue budget — two tiers" | Extend `--duration` (within 4–30s) or trim the lines; never compress the delivery |
| A cut lands up to a second off its timestamp | Expected: the measured runs placed cuts within about ±1.5s of the written stamps, and the deviation does not accumulate along the timeline (`844c9145`: late at the second boundary, back on time at the third) | Give each shot 2s or more of slack around a line; if a cut must be frame-exact, generate the shots as separate jobs |
| The written `HARD CUT`s did not happen at all — the clip reads as one flowing take | The transition mix: the one measured job that lost every hard cut had them at only 3 of 9 boundaries (`4e5c9581`), while five jobs at 3-of-8 or better kept all of theirs | Rewrite with hard cuts as at least half the boundaries, then re-check. This is a new prompt, so a new cost table |
| A scene detector reports fewer cuts than were written, and the clip looks fine | Not a defect in the clip — detection at threshold 0.3 cannot see a cut between two shots in the same place under the same light, i.e. exactly shot/reverse-shot. Missed the pivotal cut in both `41f87ac7` and `036ac3a8` | Read frames either side of every written stamp instead of trusting the count — "Checking the cuts: read frames, never a detector count alone" in the shared file |
| A one-take clip renders perfectly and still feels inert | The take closes distance in place instead of crossing space — measured on `16023efe` (20s, one very slow push, rejected) | Rewrite the phases so each one arrives somewhere the last could not see, or switch register to a held take with performance beats. New prompt, new cost table |
| Garbled or invented lettering on signs, couplets or shopfronts | The `AVOID` list was relied on; on Ofox it is only partly obeyed even at its strongest (`41f87ac7`) | Compose the lettered surfaces out — edge of frame, out of frame, occluded, or a background with no text-bearing surface at all, which is how `036ac3a8` kept five couplet shots clean |
| Character's appearance drifts between two clips of the "same" script | Each `generate` call is stateless — no persistent character memory | Reuse the exact same character block word for word and keep the `CONSISTENCY` line in every prompt for that script |
| Exit `4`, timed out waiting for completion | Job is still running upstream, not failed | Do **not** re-run `generate`; run `bash ../ofox-video-core/references/ofox-video.sh poll JOB_ID` using the job id printed before the timeout |
| Exit `5`, ambiguous network failure on create | No HTTP response received at all — can't tell if a job was created | Do not guess or retry `generate`; tell the user to check `https://app.ofox.ai` for a job that may already be running, per `ofox-video-core`'s no-resubmit rule |

## When NOT to use

- Silent product/brand footage with no characters or dialogue — use
  `seedance-ad-creative` instead.
- **One person addressing the viewer**, rather than a scene between
  characters. The boundary is who is being spoken *to*: a beat where
  characters talk to each other is this skill, a single speaker facing the
  audience is not. `talking-head` covers a script read from a portrait the
  user supplies — and runs a different model, because `bytedance/seedance-2.5`
  refuses a real person's photo at submission — while `explainer` covers the
  case where the words still have to be chosen out of an article, doc or
  release note.
- The user wants to animate an existing photo of a real person (a specific
  actor/likeness) rather than a described fictional character — Seedance 2.5
  refuses real-person frames unless `--real-person true` asserts the rights to
  the likeness, and what that has been measured doing is one short
  single-frame clip, not a drama's worth of shots holding one face.
  `talking-head` owns the portrait route. Say all of this before anything is
  spent, and settle the rights question with the user rather than around it.
- Stitching several generated clips into one file — this skill produces
  individual jobs (each of which may hold a few hard-cut shots); joining
  jobs is an external editing step.
- Anime- or manga-style scenes, especially ones needing the same character
  to look identical across multiple shots — use `seedance-anime-drama`
  instead: it starts every shot on a generated image of the character (not
  just repeated text), which Seedance permits for non-photoreal characters.
