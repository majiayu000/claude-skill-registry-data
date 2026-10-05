---
name: cardstock-diorama-myth-animation
description: >-
  Produce a complete narrated MYTHIC SHORT FILM end-to-end on Unsora MCP in the
  layered cut-paper diorama style — stacked matte cardstock worlds, a strict three-colour
  palette, exposure that swings, paper wipes hiding every seam, landing on a face.
  Animation-movie storytelling, not an explainer: gods, monsters, heroes, folklore, origin
  myths and transformations, told in ten-second story beats with a mythic narrator, native
  paper foley, and one assembled MP4. Use whenever the user wants a myth, legend, fable,
  folktale or fairy-tale short, a cut-paper or papercraft animated story, "tell the story
  of X" as a video, a stop-motion-look mythic film, or says "run the cardstock diorama
  myth animation" or "run the diorama myth pipeline" — even with no story given, since the skill proposes myths itself. NOT for
  fact-driven explainers with charts and statistics (that is vox-motion-graphics).
---

# Cardstock Diorama Myth Animation (Unsora MCP)

One request — a myth, a premise, or nothing at all — becomes a finished narrated
mythic short film in the layered cut-paper diorama style: stacked matte cardstock
worlds, three colours and no others, a storyteller's voice, one final MP4. This is
**animation-movie storytelling** — gods, monsters, thresholds, transformations —
not a data explainer.

**The style, in one line:** flat matte cardstock worlds — visible cut edges, soft
contact shadows, a strict **three-colour palette and no others** — a tiny figure
dead-centre of a huge symmetrical set, **rendered in 3D, not real stop-motion**,
scenes packed with incident and joined by **paper wipes**, native impact SFX and
paper foley, landing on a face.

**The look is a specification, not a vibe.** Palette, exposure and pacing are
numbers, and every failure is a number drifting off target. State targets as
numbers in the prompt, then measure the output (`scripts/qc.py`). Adjectives don't
survive the trip to the model; percentages do.

**The failure this skill exists to prevent** is not an ugly clip — it's a **boring**
one: one slow scene per block, one camera drift, half the runtime doing nothing. It
looks correct and feels dead. **Density is the deliverable.** The second failure,
specific to story work, is a film that *narrates* instead of *showing*: if the voice
is describing what the picture already says, the picture isn't working hard enough.

**The tool split (read this — it is the point of the pipeline):**

- **Everything generated runs on Unsora.** `create_image` (`nano-banana-pro`) for
  the style key, the reference sheets and any hero frame → `create_video`
  (`seedance-2.0`) for every block → `create_voiceover` (ElevenLabs Eleven v3) for
  the narration → `create_music` (`mureka-7.5`) only if a bed is wanted. Each
  `create_*` is async: poll its matching `wait_for_*`.
- **Assembly is ffmpeg, locally.** Unsora has no assembler, so the cut, the
  narration placement inside each block window, and the mix are ffmpeg commands you
  run yourself. This is an upgrade over any server-side assembler: block windows,
  VO centring and wordless blocks are all under your control instead of a server's.

## Hard preconditions

- **Unsora MCP connected and authenticated.** Needs `create_image`,
  `create_video`, `create_voiceover`, `list_voiceover_voices`, and the matching
  `wait_for_image` / `wait_for_video` / `wait_for_voiceover`; `create_music` +
  `wait_for_music` only if a score is requested. If they're missing, stop and say
  so — do not substitute another generator.
- **Local `ffmpeg` and `ffprobe`.** Not optional here — they *are* the assembler.
  Without them you can generate clips but cannot deliver a film.
- **Web search** for the lore pass, whenever the story is a real tradition.
- **Recommended:** `python3` with `numpy`, `pillow`, `scikit-learn` plus `curl` for
  the QC pass. If unavailable, run the eyeball checklist in
  `references/style-dna.md` and say QC was visual only.

## Operating mode

Hands-off. The user delegates story choice, palette, script, voice, casting and
assembly.

- Honour anything they specified — the myth, the tradition, the length, the
  palette, the voice, the orientation. Decide everything else yourself.
- Right before the first **paid** generation, post one short plan message (the story
  and which variant, palette, block count, the beat sheet in one line each, voice,
  rough credit estimate) so the user can interrupt — then **proceed immediately
  without waiting for approval**, unless they asked to be consulted. Note that the
  story shortlist below is a separate, earlier stop: by the time this plan message
  goes out, the myth is already settled.
- Never stop mid-pipeline to ask what a default answers. Delivering loose clips
  instead of one assembled MP4 is a failure.
- **One exception: which myth.** If the user gave no story, present a shortlist and
  wait for their pick (Phase S). Everything downstream — palette, voice, framing,
  casting, beats — you still decide. A topical explainer works with any trending
  subject, so picking one unasked is fine; a myth is the whole creative premise, and
  guessing it wastes the entire run. This is one stop at the front door, not a habit
  of asking.

Two style names collide, so be exact: this is the **three-colour cardstock**
diorama, *not* the sepia-newsprint censor-bar diorama documentary. Do not use its
letterpress prop text, and do not use any Mixed Media collage preset. This skill
generates its own style key in Phase 1.

## Defaults

| Setting | Default | Override when… |
|---|---|---|
| Style key | Generated in Phase 1 from the cardstock style-key prompt (`references/style-dna.md`), at the run's aspect ratio | user supplies their own reference image |
| Palette | Auto-picked to fit the myth's world and mood (`references/palette.md`) | user names one, or the tradition has a strong colour identity |
| Aspect | **16:9** — the concentric top-down hero shot needs the width, and this is a film | user says shorts/TikTok/Reels → 9:16, and warn the ring beat loses power |
| Length | 1 minute → N = 6 blocks (N = minutes × 6, each block one 10s beat). A myth with a real arc wants **8–12 blocks**; recommend 90s–2min if the user is open | user gives a length (1–10 min) |
| Engine | `create_video`, `model: "seedance-2.0"`, `resolution: "720p"`, `duration: 10`, `generateAudio: true` | — |
| Character sheet | **Mandatory** for the protagonist, and for any creature or place in 2+ blocks | a single-location fable with one figure still gets the figure |
| Language | English narration (prompts stay English regardless) | user asks otherwise |
| Voice | Auto-pick a **storyteller** from the twenty Eleven v3 voices: deep, unhurried, warm, formal — a voice reading a legend aloud, not a news anchor and not an ad read. `stability: 0.6` | user wants to choose → `list_voiceover_voices` renders the picker; show it and wait |
| Subtitles | **OFF** — this style is image-led and a myth plays better uncaptioned | headed for silent-autoplay social → ON, burned from an ASS file in the ffmpeg pass |
| Music | None — seedance's native paper foley and impact SFX carry it | user wants a score → `create_music` (`mureka-7.5`), ducked under the VO in the mix |

## Story engine

Four things carry a mythic film:

- **Every block delivers one nameable event.** *"What does the viewer see happen
  that they didn't a second ago?"* — a blade is drawn, a wave swallows a boat, a
  body becomes a tree, the sky splits. If you can't name the event in one clause,
  the block is a postcard: pack it, fold it, or cut it.
- **A 10s block needs two internal paper wipes.** A wipe every 3–4 seconds is what
  keeps this style dense, so each block runs roughly: event → wipe → event → wipe →
  event, plus its join bookends. Never let a 10-second block ride one slow camera
  move.
- **One talisman travels the whole film.** A single physical object carried through
  every block and escalating — a thread, a feather, a cracked mask, a lantern, a
  seed. In myth this is the story's memory: it enters in the first beat, changes
  hands or changes state at the crisis, and pays off in the last frame. Design it
  before writing block 1.
- **The arc, mapped to blocks.** For N = 6 use the short column; for N = 8–12
  expand the ordeal.

| Beat | Story job | Visual job |
|---|---|---|
| 1 | **Cold open in the middle of something.** An omen, a rupture, the world already breaking. No "long ago there was a…" | cold open on motion, no leading wipe; deliver the establishing geometry *while* something violent is underway |
| 2 | **The world and the lack.** Who this is, where, and what is wrong or missing | the tiny figure dead centre of the huge symmetrical set — the format's signature shot |
| 3 | **The threshold.** The choice is made, the door opened, the pact struck | the talisman enters or is claimed; the palette swings to its dark end |
| 4 … N−2 | **The ordeal, escalating.** One trial per block, each costlier than the last. Never repeat a beat's shape | the build — packed, wipe-joined, whiplash the scale: giant face → ant-sized figure → colossal creature |
| N−2 | **The crisis.** The lowest point, or the transformation itself | the biggest impact of the film; flat shards, punched confetti, a full ground-flood or a full void-flood |
| N−1 | **The confrontation.** The reckoning, inside the ring | **the ring hero shot** — crane straight up, the world resolving into concentric rings around the figure at dead centre |
| N | **The cost, and what remains.** What was paid, what changed. End on the image, not a moral | **land on a face** — push into an extreme close-up, flat paper features, accent across the eyes, lit as bright as the opening. Ends on the image; no trailing wipe |

**Find the ring.** The top-down concentric beat needs a circular geometry to fall
into — an arena, a whirlpool, a coiled serpent, a ring of standing stones, a crater,
a spiral stair, a circle of mourners, a labyrinth. Myth is full of them. If the story
seems to have none, find the ring hiding in it (a duel becomes a ring of onlookers; a
funeral becomes a ring of fire). A ring you only look at is a postcard; one something
happens inside is a film.

## Narration — sparser than an explainer, and that is the point

**~12–18 words per block** (an explainer runs 20–24). Mythic register: concrete
nouns, plain verbs, no hedging, no modern idiom, no jokes. Present or simple past,
held consistently. The voice names what cannot be seen — a lineage, a bargain, a
consequence — and stays silent about what the picture already shows.

You centre each take inside its fixed 10s window in the ffmpeg pass, and **for a
myth that is a feature, not the bug it is in an explainer**: a 16-word line runs
~6.5s and centres with ~1.75s of pure paper foley at each end — the film breathes,
and the impacts land in silence. So aim short deliberately. The **ceiling is ≈9.5s**
per block; past that there is no air left, and you have to speed-fit the take
(`atempo` ≤ 1.15) and the storyteller starts to sound rushed. Reshape long lines into
one flowing sentence or cut a clause; narrator voices pause ~0.7s at every period, so
two short sentences cost more time than one longer one.

**One or two blocks should carry no narration at all** — the crisis and often the
ring shot play stronger silent, on SFX alone. On this pipeline a wordless block is
trivial: generate no voiceover for it and lay nothing over it in the mix. No
workaround, no test needed.

## Joins — paper-wipe bookends

- **Tail of block N** — the final 0.4s: the camera rushes into a blank sheet of the
  join colour filling the frame; the clip ends on flat paper, no detail.
- **Head of block N+1** — opens on ~0.25s of the same flat colour, then pulls back
  into its tableau.

Concatenated, the cut lands between two flat identical-colour frames, so the seam is
invisible; the halves read as one continuous ~0.5s wipe. **Ground/light wipes into
bright beats, accent wipes into dark ones** — the colour previews the beat it opens,
which in a myth means the wipe carries dread or relief before the image does. The
join colour is a property of the join and must be written into both sides. Never
chain `image` → `lastImage` across blocks; the bookends are the join. Wording:
`references/style-dna.md` §The paper wipe.

This trick is battle-tested against exactly the assembler used here — a local ffmpeg
concat — so there is no uncertainty about how the seam lands. Still inspect the
seams after the concat and report what you see.

## Pipeline

| Phase | What happens | Tools |
|---|---|---|
| S Story | use the given myth, or propose 4–6 and **wait for a pick** | reasoning + web search |
| L Lore | read the actual tradition: variants, names, iconography, the ending | web search |
| P Palette | lock one palette for the whole film | `references/palette.md` (free) |
| 1 Style key | generate the cardstock style key at the run's aspect ratio | `create_image` (`nano-banana-pro`) |
| 1b Casting | sheets for the protagonist, every creature, every recurring place, the talisman | `create_image` (`nano-banana-pro`, 16:9) |
| 2 Beat sheet + narration | N beats on the arc, ~12–18 words each, 1–2 wordless | reasoning (free) |
| 3 Block prompts | N prompts in the diorama language, wipe-bookended, sheets bound | reasoning (free) — templates in `references/style-dna.md` |
| 4 Clips | N × 10s clips, style key + sheets on every one | `create_video` (`seedance-2.0`) |
| 5 Voice | one storyteller, one take per voiced block | `list_voiceover_voices` + `create_voiceover` |
| 6 Assemble | concat clips, place + mix the takes, deliver one MP4 | ffmpeg (local) |

Read `references/style-dna.md` before Phase 1 and `references/unsora.md` before
Phase 4. Phases S, L, P, 2, 3 and 6 are free; 1, 1b, 4, 5 cost credits.

**Job model:** every `create_*` returns a `generation.id`. Poll the matching
`wait_for_*`; a completed job carries a **result URL**. That URL — not the id — is
what you pass onward: as `image` and inside `referenceImages` on `create_video`, and
to `curl` for the local copy. Everything from Phase 6 on works on local files. Check
`get_credits` once before Phase 4 if you want a balance for the plan message.

## Phase S — Story

**Story given** → use it, go to L.

**No story** → **propose 4–6 myths, show them, and wait for a pick.** Do not choose
one yourself and start generating; this is the one front-door stop. If the user
answers with a vibe rather than a title ("something with a sea monster"), that counts
as a pick — take the closest candidate and go.

Bias hard toward **action-dense spectacle**: monsters, sieges, floods, descents into
the underworld, shapeshifting, oaths and bargains with something older than the hero.
What makes a myth work in *this* style:

- **A physical world to build in card** — a mountain, a sea, a forge, a maze, a
  storm. Abstract theology needs a physical proxy.
- **A creature or force with a silhouette** — cut paper lives or dies on silhouette,
  so a serpent, a wolf, a giant, a wave read beautifully; an unseen dread does not.
- **A transformation** — this style does metamorphosis better than anything, because
  a body becoming a tree is literally one stack of card replaced by another.
- **A circular geometry** somewhere, for the ring beat.
- **An ending that lands on a face** — a cost paid, a change worn.

**Scope each candidate to the runtime.** One myth, or one episode of a larger cycle —
not a whole epic. "The binding of the wolf" is a film; "the Norse myths" is not. If a
tradition only offers an epic, propose the single strongest episode and say which.

**Spread the shortlist.** Vary the tradition, the scale and the tone — not five Greek
myths, not five monster fights. Include one lighter or stranger option; the trickster
tale is often the one people pick. Lesser-known myths outperform the famous ones: the
audience doesn't know where it's going, and there's no animated-film version in their
head to compete with.

**Proposal format** — one entry each, so a pick takes seconds:

```
**[Title] — [tradition]**
[One-line logline: who, the turn, and what it costs.]
Ring: [the circular geometry] · Creature: [the silhouette] ·
Transformation: [what becomes what] · Talisman: [the travelling object]
```

If a candidate is missing one of those four, say so rather than inventing it — a myth
with no transformation can still be the best pick, and knowing what it lacks tells the
user what the film will lean on instead.

**Calibrated seeds** (a spread that works; don't just recycle these, but match this
level of concreteness):

| Myth | Ring | Creature | Transformation | Talisman |
|---|---|---|---|---|
| The binding of Fenrir (Norse) | the gods ringed around the wolf | the wolf, growing each attempt | — (the cost is a hand) | the silk-thin chain |
| Arachne's contest (Greek) | the circle of judges at the loom | — | woman → spider, on screen | the tapestry |
| Vasilisa and Baba Yaga (Slavic) | the fence of skulls around the hut | the hut on chicken legs | — | the skull lantern with fire in it |
| Marduk and Tiamat (Babylonian) | the coil of the sea itself | the salt-water serpent | her body → the sky | the net of the four winds |
| Nüwa mends the sky (Chinese) | the hole burned in heaven | the black turtle | stone → molten patch | the five stones |
| Cú Chulainn's warp-spasm (Irish) | the ford, fighters ringed on both banks | the man himself, deformed | hero → monster → hero | the ford's single stone |
| Anansi buys the stories (West African) | the ring of animals bearing witness | the hornets, the python | — (a trick, not a change) | the calabash of stories |
| Icarus (Greek) | the spiral of the labyrinth below | the sun as a flat disc | wax → nothing | the feathered wing |

**One caution.** Some stories are living sacred tradition rather than public folklore —
especially Indigenous and closed-practice material. Prefer widely published,
public-domain myth; if the user asks for something that reads as sacred or closed, say
so plainly once, offer a near neighbour, and follow their call. Don't lecture, and
don't refuse a myth just because it is religious.

## Phase L — Lore

Never write a myth from vibes. Search the tradition and collect: **which variant**
you're telling (most myths have several irreconcilable versions — pick one and say
which), the **names** as commonly transliterated, the **iconography** the tradition
itself uses (what the creature actually looks like in its own art, what the hero
carries, what the place is described as), the **ending** as the source gives it, and
any **detail specific enough to be worth stealing** — a number of doors, a colour of
a horse, the thing said at the threshold. Specifics are what make a mythic film feel
found rather than generated.

Then decide what you are changing and own it. Compression is fine; contradicting the
tradition's ending is a choice to make deliberately and mention in the delivery
message.

**Do not** describe characters as they appear in copyrighted animated films. Render
from the tradition's own iconography. See the moderation and IP notes in
`references/unsora.md`.

## Phase P — Palette

Pick one of the five tested palettes and hold it for the whole film: **Reference**
(cream/vermilion/navy), **Sable** (lilac/violet/moss), **Cobalt**
(cream/vermilion/teal), **Iris** (cream/violet/forest), **Glacier**
(ice/vermilion/bitumen). Match the myth's world — the mapping is in
`references/palette.md` §Picking a palette for a myth. State the choice and the three
hexes in the plan message. The maths, the full prompt-ready ranges, and the rule that
**something must oppose the accent by ~140°** are in the same file.

## Phase 1 — Style key

`create_image`, `model: "nano-banana-pro"`, `aspectRatio` = the run's ratio, with the
STYLE KEY prompt from `references/style-dna.md` §Style key, palette hexes
substituted. `wait_for_image`, then keep the **result URL** — that URL is the style
key, and it goes in `referenceImages` on **every** clip. QC it before spending on
clips: a bad key poisons the run and re-rolling costs one image.

## Phase 1b — Casting (do not skip this)

A myth follows the same figure for its whole runtime, so **character drift is the
single biggest technical risk in this skill** — a bigger one than palette drift. In
the explainer version sheets were optional; here they are the job.

Generate, before any clip: a **character sheet for the protagonist**, one for **every
creature**, and a **location sheet for every place appearing in 2+ blocks**. Formats
in `references/style-dna.md` §Reference-sheet formats — always 16:9. The talisman
gets its own sheet too, at 1:1, from the format in §The talisman / prop sheet: it
must stay recognisable at every scale, and a second sheet if it changes state at the
crisis.

Then pass each sheet's URL in `referenceImages` on every block that uses it, alongside
the style key, and refer to it in the prompt by slot — "the same figure from
@Image2". Mind the slot maths: on `create_video`, `image` is @Image1, so the first
`referenceImages` entry is @Image2. Pass only the sheets that block actually uses; a
dangling reference invites drift, and Seedance caps `referenceImages` at 9. QC every
sheet and show them in the plan message: a flawed sheet propagates into every block
that references it, and this is the cheapest moment to re-roll.

## Phase 2 — Beat sheet + narration

N beats on the arc table above, labelled `Block 1 … Block N`. For each: the event in
one clause, the wipe-in colour, which sheets it uses, and its narration line
(~12–18 words, or **none**). Plain spoken text only — no stage directions, no
parentheticals, numbers spelled out. Read the whole narration start to finish aloud:
it should sound like one voice telling one story, not N captions. Cut every line that
describes what the picture already shows.

## Phase 3 — Block prompts

One video prompt per block. Each block is a 10-second `create_video` call that takes
the style key and this block's sheets in `referenceImages`. Write all N with the
block template in `references/style-dna.md`, then run the per-block checklist there.
(For the ring block and the final face block, consider the optional **hero-frame
lock** in `style-dna.md`: generate that block's opening frame with `create_image`
first and pass it as `image`, which buys precision on the two shots that carry the
film.) Non-negotiable in every prompt:

- The medium sentence (stacked matte cardstock, visible cut edges, soft contact
  shadows, rendered in 3D) **and** the AI-default negative.
- The palette stated **three ways** — hexes with ranges, percentages, and the
  exclusion naming the colour you removed.
- The exposure block. **Never a global exposure lock** — the swing is the style.
- Paper logic named for every element, especially anything entering mid-block, and
  for every creature, flame, wave and wound.
- Every camera move pinned to a timecode and forbidden to pause.
- Both wipe bookends with colour and duration (except block 1's head, block N's
  tail).
- Sheet binding by slot for every figure, creature, place and the talisman.
- **Never the word "hold"** — the model freezes on a full-detail frame. Named
  micro-motion instead.
- The audio block: native paper foley and impact SFX, `No music. No voice.` The
  narration is a separate track; a voice inside the clip fights it.

## Phase 4 — Clips

Submit N `create_video` jobs — `model: "seedance-2.0"`, `duration: 10`,
`resolution: "720p"`, `generateAudio: true`, `aspectRatio` identical across the run,
style key plus that block's sheets in `referenceImages`. Exact call template and the
moderation and IP map are in `references/unsora.md`. Poll each with `wait_for_video`,
`curl` the result to `clips/block_NN.mp4`, and record every generation id against its
block in the manifest; re-submit only failures.

**Violence, the way this style does it.** Myth is violent and the style handles it
natively *because* it is abstract: a wound is a vermilion paper shard, a beheading is
a silhouette and a scatter of punched confetti, a flood is stacked wavy card. Describe
the paper event, never the gore — that keeps the film true to the style and clears
moderation at the same time. Explicit blood and viscera will flag and are off-style
anyway.

QC each clip if the local pass is available:
`python scripts/qc.py video clips/block_NN.mp4 --ground '#…' --accent '#…' --void
'#…'`. Report numbers honestly, failures included — luma swing (target ~150, under
~80 is a dead clip), ground share near 45%, no fourth hue, and the flat head/tail
runs that prove the bookends landed. Re-roll only on a fail; never re-roll a good
block "for consistency" — a re-roll comes back different and breaks the bookend match
with its neighbour.

## Phase 5 — Voice

1. `list_voiceover_voices` → auto-pick a **storyteller** from the twenty Eleven v3
   voices: deep, unhurried, warm, slightly formal, comfortable with silence. Read the
   register off the myth — a Norse saga and a trickster tale don't want the same
   voice. Note the exact `voice_id` and reuse it on every block. If the user wants to
   pick, the tool renders a picker with previews: show it and wait, and don't repeat
   the voices as a list in your reply.
2. One `create_voiceover` call per **voiced** block. `stability: 0.6` for a steady
   narrator (lower gets theatrical, higher gets flat); leave `similarity` at its
   default. Generate nothing for a wordless block. Poll `wait_for_voiceover`, `curl`
   each mp3 to `vo/vo_NN.mp3`.
3. `ffprobe` every take for its real duration and record it. A 12–18 word line
   landing at **5–8s is correct** — the block is 10s and the assembler centres the
   take so it opens and closes on foley. Over **≈9.5s** there is no air left: cut a
   clause or merge two sentences and re-voice that block only, or speed-fit it in the
   mix (`atempo` ≤ 1.15, pitch-safe).

`<#0.5#>` between words inserts a half-second pause and is worth using at a
threshold line — but a pause spends the same window the silence at each end does, so
check the take still lands under the ceiling.

## Phase 6 — Assemble (automatic, mandatory)

The moment all clips and takes are done, assemble in the same run without being
asked. `ffprobe` the finished clips' real `width`/`height` and encode to **those** —
if the clips rendered in a different aspect than planned, the assembly matches the
clips, not the plan.

1. **Concat** the clips in manifest order. Every join is wipe-bookended, so the cut
   lands between two flat identical frames and needs no crossfade.
2. **Place each take** at its block's window: `offset_ms = block_start_ms +
   (10000 − vo_duration_ms) / 2`. That centring is what gives the myth its air, and
   on this pipeline it is your arithmetic, not a server's. Wordless blocks get
   nothing.
3. **Mix** VO over the clips' native SFX (kept low so impacts read), plus the music
   bed ducked under the VO if there is one.
4. **Verify** duration, dimensions and audio streams before presenting.

Exact commands — concat, loudnorm, the centring offsets, the sidechain duck,
verification and resume — are in `references/unsora.md` §Assembly. Then present
`final.mp4` with the host's native file delivery.

## Delivery

Final message: the video, the myth and which variant you told in one sentence, the
talisman and what it paid off into, the locked palette (name + three hexes), the full
narration so the user can reuse it, the QC numbers if measured, anything you
deliberately changed from the source, and where you read the tradition. Then offer —
never run unasked — social posting (Unsora `create_post`, its own explicit yes) or a
titles pass.

## Failure handling

| Symptom | Cause | Fix |
|---|---|---|
| The protagonist looks like a different person each block | No sheet, or sheet not passed | Sheet first, always; its URL in `referenceImages` of every block that uses it; describe only pose and action in the prompt, never re-describe the design |
| The creature changes anatomy between blocks | Same, plus over-description | One creature sheet, bound everywhere; in the prompt say "the creature from @Image2", then only what it does |
| Film feels like N tableaux, not one story | No talisman, or the arc wasn't mapped | Put the object in every block and change its state at the crisis; check each block against the arc table |
| Narration describes what the image shows | Explainer instinct | Cut the line to its unseeable half — lineage, bargain, consequence — or drop it and let the block play silent |
| Reads like a scene from an animated feature | A film's character design leaked into the prompt | Render from the tradition's own iconography; never name or describe a copyrighted character version |
| Clip is boring — one slow move, half the block dead | Only one event in a 10s window | Two internal wipes, three events; purge every "hold" and name micro-motion |
| Renders glossy CGI / photoreal, or grows smoke and volumetrics | AI-default leaked | Medium sentence + full negative every time: stacked matte cardstock, visible cut edges, flat shards not smoke, no gloss/specular/lens-flare/DoF |
| Renders as flat vector illustration | Cut edges and contact shadows not stated | Name both explicitly; they are the signature |
| Clip drifts dark (interiors, caves, night, close-ups) | No exposure block, or a global lock | Exposure block from attempt one; pin close-ups "as bright as the opening"; never "hold the balance every frame" |
| Palette drifts / a fourth colour / accent floods | Ground collapsed, or nothing opposes the accent | State the palette three ways; name the removed colour; check something opposes the accent ~140° |
| Camera move never happens or arrives late | Move unpinned | Pin to a timecode and forbid pausing |
| Visible hard cut at a seam | Bookends missing or colours mismatched | Same flat join colour on outgoing tail and incoming head; verify flat runs with `qc.py video` |
| A low continuous drone under the biggest move | Seedance adds it unasked | Ban the sustain, not the frequency: "no sustained tone, no cinematic drone, no continuous hum"; keep "heavy card dropped flat" so impacts keep body |
| Clip contains a voice | Narration leaked into the video prompt | `No voice.` in every prompt; the voice exists only in the mix |
| Video job `FAILED` with no error text | Moderation, not luck | Usually violence described as gore rather than as paper — rewrite it as shards and silhouette. See the map in `unsora.md` |
| Storyteller sounds rushed | Take over ~9.5s, so it was speed-fitted | Cut a clause or merge two sentences into one; re-voice that block only |
| Assembled film is short | A clip failed and got skipped by the concat | Check the manifest, regenerate the missing block, re-concat — a concat that drops a clip still yields a valid file |
| Clips won't stream-copy concat | A clip came back a different size | Every clip must be 720p at the same ratio; regenerate the odd one and re-verify |
| The mix is 6 dB quiet | `amix` without `normalize=0` | `normalize=0` on every `amix` — it is not optional |

## Reference files

- `references/style-dna.md` — the full cardstock visual system: locked slots, paper
  logic (including creatures, water, fire and wounds), exposure swing, camera,
  motion, audio vocabulary, the AI-default negative, the wipe wording, the
  **style-key prompt**, the **block-prompt template** with a worked mythic example,
  sheet formats, and the per-block checklist. **Read before writing any prompt.**
- `references/palette.md` — the palette maths, the five tested palettes plus one
  documented failure, prompt-ready ranges for all five, how to state a palette three
  ways, palette-by-myth-world, and how to build a sixth with `scripts/palette.py`.
- `references/unsora.md` — exact Unsora call templates for every phase, the job and
  polling model, the manifest schema, the moderation and IP map, cost arithmetic,
  every ffmpeg command for the assembly, verification, resume-after-failure, and the
  optional posting flow.
- `scripts/qc.py` — measures frames (`frame`) and clips (`video`) against the
  palette, exposure and wipe targets. `python scripts/qc.py --help`.
- `scripts/palette.py` — solves a new three-colour palette at the right luma values.
