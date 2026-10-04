---
name: tool-flow-stills
description: Generate, review and repair still images in Google Flow (Nano Banana 2) by browser automation — free unlimited image generation, batch prompting, per-image editing that preserves what you tell it to preserve, version-history revert, and asset renaming as the shot-mapping mechanism. Use when the user wants stills for an MV, article, slideshow or deck made in Flow, or says "use Flow", "use Nano Banana", "generate the stills", or points at a labs.google/fx/tools/flow project. NOT for local GPU generation (use tool-comfyui-image), NOT for the EmptyOS Music Studio staged pipeline (use creative-mv-generator), NOT for defining a film's visual language (use creative-mv-art-director first).
---

# Flow Stills Skill

For an MV, start at `creative-mv-director`: free Flow stills can fill living-master slots from v0 onward (after the treatment is approved); it swaps each reviewed still into the living master, and no paid video is made before the user approves v0.

Operating manual for Google Flow's image side, learned the expensive way on
无所住 (2026-08-07). Flow does **both** stills and video in one project, so
assets never leave the workspace between stages.

## The economics that shape everything

| | cost |
|---|---|
| **Nano Banana 2 image generation** | **0 credits — free, all tiers** |
| Image editing (same surface) | free |
| Omni Flash video, 10 s | 15 credits |
| Veo 3.1 Quality video | 100 credits |
| Veo 3.1 Fast video, 8 s x1, 720p (measured 2026-09-22) | 10 credits |
| Video download: 720p / 1080p upscale / 4K upscale (menu, 2026-09-22) | free / free / **50 credits** |

**Because stills are free, review-and-regenerate is the cheap half of the
pipeline.** Do not try to nail a perfect first pass — generate, look, and
regenerate the misses. Four rounds cost nothing.

## Hard-won mechanics

### Free generations skip the approval gate
With *Confirm before generating: Always* set, credit-spending generations
require an Approve click. **Free image generations bypass it entirely** — so a
long unattended stills run needs no settings change and no supervision. Video
does.

### ⚠ Confirmed on video: the once-per-session approval fails SILENTLY

Measured on Love Hate v6, 2026-08-08. A second video request in the same session
produced the agent's *"I will generate…"* text and then **nothing** — no approval widget,
no generation, no credits spent, and **no error**. It is indistinguishable from a request
still thinking.

**A page reload is NOT sufficient** — this cost four wasted attempts. Reloading does
produce a differently-named session, so it *looks* like a reset, but that session still
never draws the widget. The agent replies *"I will generate…"* and then stops, every
time.

**The only reliable reset is the explicit control: ☰ (top-left of the session panel) →
"Create a new session".** That gives an "Untitled session", and the widget renders on
its first request. So the working loop for a multi-clip run is:

> ☰ → Create a new session → request → **Approve** → wait → verify in `Videos`

**Budget one explicit new session per credit-spending generation.** Approving with
"Approve" (not *"Approve, do not ask again"*) keeps the gate for the next one.

One more trap on top: **the session panel does not re-open by itself once closed.** If
you dismiss it with ✕, later replies — including approvals — render into a panel you
cannot see, which is indistinguishable from nothing happening. Re-open it with the
expand control beside the create box.

Because the failure is silent, **verify against the `Videos` list, not against the
chat.** Counting clips is the only reliable signal that a generation actually happened —
and it is also how you confirm no credits were spent when it did not.

### The approval widget renders only ONCE per conversation session
A credit-spending request later in the same session states its plan and then
silently waits on a control Flow never draws. The agent will insist it is
"waiting for your permission approval in the interface" when there is nothing
to click. **Fix: start a new session per credit-spending generation** (☰ →
Create a new session). This cost ~15 minutes before it was diagnosed.

### A single conversation collapses composition
Flow's agent volunteers *"I'll use the first generated image as a style
reference to maintain consistency"*. It propagates **composition**, not just
palette, and the collapse grows with series length — 13 of 18 frames became the
same photograph (eave over rooftops, misty mountains, wet ledge).

**Fix, and it works decisively:**
1. **Fresh session** for each batch of 3–5.
2. **Name what must not recur**: "no dark eave across the top, no misty mountain
   backdrop, no white-walled village receding into fog, no wet stone ledge along
   the bottom — those have been overused."
3. **Force shot scale explicitly** — macro / overhead / sky-only / enclosed.
   Without this every frame converges on the establishing composition.

### Batch 3–5 per message
The agent handles multiple numbered descriptions in one message and generates
them in parallel (~50 s). Beyond ~5 the per-image direction gets diluted.

### ⚠ A newline in the project chat SENDS the message — compose as ONE line

Found on Love Hate v6, 2026-08-07. A multi-paragraph prompt **sends at the first
newline**: the opening paragraph goes off as a complete message and the rest sits
in the input box, unsent. The agent then works from a preamble containing none of
the actual shot descriptions.

It fails quietly, like the others in this file — the message looks sent, the agent
answers confidently, and it is answering a prompt you never meant to ask.

**Write every Flow chat prompt as a single line.** Separate items inline —
`IMAGE 1 — … IMAGE 2 — … IMAGE 3 — …` — never with line breaks. This applies to
the batch-edit template below too.

Recovery: click ■ to cancel the response, click the ✕ on the input box to clear the
leftover text, then retype as one line. Nothing is charged (images are free) and no
asset is created by the truncated request.

## 🔑 THE BIG ONE: the project chat is an AGENT — batch, don't hand-edit

**Read this before touching anything else.** Flow's right-hand project chat can
apply the *same edit to many existing images in one message*. It processed
**11 images in a single request**, correctly, in about a minute — after I had
spent hours opening frames one at a time.

Ask it plainly:

> I need a colour correction applied to MULTIPLE existing images in this
> project — please edit the existing images, do not generate new ones. Take
> every image whose name starts with a number and a middle dot (01 through 18)
> and apply this same correction to each: **⟨the edit⟩**. Keep each image's
> exact composition, framing, subject, brightness and contrast unchanged. Can
> you apply this across all of them in one go? If you can only do a few at a
> time, do as many as you can and tell me which ones you completed.

Why this phrasing matters:
- **"edit the existing images, do not generate new ones"** — without it the
  agent may generate fresh frames instead of editing.
- **Naming the selection by a filename pattern** (`NN ·`) is what lets it
  address a set. This is the payoff for renaming keepers — the names become a
  *queryable selector*, not just a label.
- **"tell me which ones you completed"** — you get an explicit manifest back
  instead of having to audit the grid. **But see the next section: the manifest is
  a claim, not evidence.**

### 🚨 Agent mode REWRITES your prompt — turn the Agent pill OFF for anything geometric

Measured on 說得太急, 2026-09-21. The project chat does not send what you typed. It
**paraphrases the prompt** and the paraphrase drops constraints — silently, with no
indication that the prompt which ran is not the prompt you wrote.

A blockout-reference prompt containing two geometry clauses —

> *"…reproduce exactly what is and is not visible from this camera"* and *"Do not add,
> move or remove any **wall, opening**, furniture or object that is not in the blockout,
> and **do not invent any view, room or background that the blockout does not show**"*

— reached the model as only:

> *"Do not add, move, or remove any **furniture or object** not in the blockout."*

The model then obeyed it exactly: it added no furniture and no object, and it added a
**window and a wall corner** into a flat wall. The defect reads as "the reference
doesn't control geometry" when the real cause is that the instruction never arrived.

**The pill is a toggle beside `+` in the composer.** Off, the bar shows the model chip
(`Nano Banana 2 · 16:9 · x3`) and your prompt goes to the model verbatim — and you get
x2/x3 variants free, which agent mode does not give. On, it shows `Agent`.

- Use **direct mode** whenever the prompt carries constraints that must survive
  literally: blockout/layout references, negative lists, "do not add X", exact framing.
- Keep **agent mode** for what it is genuinely good at — batch edits across many
  existing assets (the section above), and loose creative briefs.
- If you must use agent mode, **read the rewritten prompt back** from the asset's detail
  panel afterwards and check your constraints survived. That is where the rewrite is
  visible; nowhere else.

### ⚠ A featureless proxy figure in a blockout renders as a SCULPTURE

Same session, and it is the other half of making blockouts work. With the prompt
reaching the model verbatim the geometry came out right — and all three variants
rendered the grey stand-in **as a real object**: the sphere head became a bronze ball,
the torso boxes became a stone plinth, and the actual man was painted sitting behind
them.

Flow cannot distinguish "grey box standing in for a person" from "grey box". The
blockout's own docs may call the figure a placeholder; the model never reads those.
**Declare it in the prompt**, and name the objects it must not become:

> The grey blocky figure in the centre of IMAGE 1 is a PLACEHOLDER marking where the man
> sits — it marks his seat position, his body scale and his head height, and it is NOT an
> object in the room. Replace it entirely with the real man from IMAGE 2, seated in that
> exact position at that exact scale with his head at that exact height. There is no
> statue, no sculpture, no sphere, no ball, no plinth, no pedestal and no stone block
> anywhere in this photograph.

That one clause took the shot from unusable to gated-pass with nothing else changed.

### ⚠ A blockout constrains what it SHOWS, not what it CROPS

Third finding from the same session. A camera that cuts a wall feature off above the
frame edge leaves that feature unconstrained, and Flow fills it in from style — a framed
picture appeared in a corner where the blockout has bare wall, because the real picture
sits just above the top edge.

Harmless when the invention is scene-appropriate, and a continuity break when it is not.
**If a landmark has to be in the right place, frame it.** Verify what the blockout
actually shows by brightening a crop of the region rather than assuming from the model —
a dark render hides a lot.

### ⚠⚠ The completion manifest can be FABRICATED — always verify by search

Measured on Love Hate v6, 2026-08-07. Asked to rename 19 existing images, the
project chat replied with a per-item bulleted list of all 19 new names and the
sentence *"All items were successfully matched and updated. No files were left
unrenamed."*

**It had renamed exactly one of the 19.** Every other asset still carried its Flow
auto-caption ("Two men walking down street", "Hand resting on shoulder blade").

Renaming **is** an advertised capability — Flow's own onboarding tooltip lists
*"rename assets"* among what the agent can do. So this is not a missing feature. The
agent can do it, did one, and reported nineteen. Capability is not the issue;
**execution reporting is.**

This is the sharpest form of the proxy-signal trap in this file, because the
manifest is the thing recommended above as the fix for proxy signals. It is still
worth asking for — it tells you what the agent *believes* it did — but it is not
evidence.

**Open an asset and read its title bar** — that is the check that distinguishes a
rename from an auto-caption. A `·` search is a useful first pass but it did not
render reliably on a later attempt, so do not depend on it alone.

### Renaming by hand — the fast path

The **detail view title is editable inline**, which is much quicker than the grid's
`⋮ → Rename`:

1. **← / → arrow keys step through every asset deterministically.** Use these, not
   the filmstrip — the filmstrip reorders as you rename and coordinate-clicking
   lands on already-done frames.
2. The auto-caption in the title bar identifies the frame ("Two men sharing
   cigarette"), so one zoom on the title tells you which shot you are on. Where two
   shots could share a caption, look at the image before typing.
3. **Triple-click the title** to select it, then type the new name **with a trailing
   newline** — the newline commits. That is 4 actions per asset.

19 assets took roughly 80 actions this way.

Keep the authoritative shot→image mapping in a file on disk regardless. Flow names
are a convenience for the video stage, not the record.

Per-image editing (below) is now only for **one-off repairs** — a single frame's
composition, a continuity fix, a wrong subject. Never use it for anything
applied across the set.

Cost is unchanged: image work is free, so a batch re-run costs nothing.

## The editing surface (per-image repair)

Click an image → detail view with *"What do you want to change?"*.

**It honours "keep X exactly as it is."** Both successful edits on 无所住
preserved their stated invariants pixel-for-pixel and changed only what was
named:

> *"Keep the composition, the low camera height, the palette and the flower
> exactly as they are. Change only the setting: replace the European deciduous
> trees and tarmac with a wet stone lane and an out-of-focus Huizhou wall."*

**Narrow, explicitly-scoped edits are safe. Blanket style edits are not.**

### ⚠ A scoped edit can silently change the ASPECT RATIO

Found on Love Hate v6, 2026-08-08. An edit that only re-dressed a room's contents
returned the frame as **4:3 instead of 16:9**. Nothing in the prompt mentioned
framing, and the change is easy to miss because the detail view fits any ratio
neatly into its container.

It matters because assembly needs every clip at one ratio — a single 4:3 still
becomes a pillarboxed or cropped shot in the cut.

**Check the ratio after every edit**, and if it drifts, a follow-up edit naming
"wide 16:9 widescreen, extend the scene left and right" restores it while keeping
the content.

### The corollary: an edit changes ONLY what you name

The same session asked for a bed to be cleaned up and named the mattress, walls and
floor. The mattress, walls and floor came back clean — and the **pillows**, which
were never named, came back exactly as stained as before.

This is the same property that makes scoped edits trustworthy, seen from the other
side. **Enumerate every element that must change**, and expect anything unnamed to
survive untouched.

### ⚠ A near-black gradient is a LOADING PLACEHOLDER, not a failed render

**This wasted two edits and produced two wrong conclusions.** A colour/tone edit
renders progressively; mid-render the frame shows as a dark featureless
gradient that looks exactly like a destroyed image. Judging it there leads you
to revert a perfectly good result.

**Wait for the render to settle, and check the history panel before reverting**
— the finished version appears there even when the main canvas still shows the
placeholder.

Grade-type edits do work on this surface:

| Edit | Result |
|---|---|
| *"Shift the neutrals warm — stone as warm grey not blue-grey, tile as umber not blue-black, fog as ivory not blue-white."* | Worked. Only temperature moved. |
| *"Far too desaturated and near-monochrome — bring real colour back: living green moss, real slate and umber in tile, natural brown timber. Natural and filmic, not vivid."* | Worked. Real colour returned with composition and light intact. |

Both were briefly "black gradients" before finishing.

### 🚨 After a manual REVERT, a later edit does not take selection

Measured on Love Hate v6, 2026-08-08, and it is probably the real mechanism behind the
"I2V bound a stale version" observation below.

Five stills were edited in one pass. Checking them afterwards, **two carried the wrong
selected version** — the canvas and the asset's current state showed an *older* entry
while the newest render sat unselected further down the history panel.

The two were exactly the two where I had **manually reverted before editing**. The
sequence that breaks it:

1. click an older version in the history panel to revert → that version becomes selected
2. run a new edit → it renders and appends to the bottom of the history
3. **selection stays on the reverted-to version**, not the new one

Nothing announces this. The edit clearly succeeded, the new thumbnail is right there,
and the asset silently remains on the older frame. Anything downstream — a later edit,
an export, an image-to-video generation — takes the *selected* version, not the newest.

**So the check before animating is not "did my edit render" but "is my edit the selected
version".** Open each asset, look at which history entry carries the selection border,
and click the newest if it does not. On an asset you never reverted, the newest is
selected normally — the defect is specific to the revert-then-edit sequence.

**⚠ But fixing the selection does NOT fix the video binding.** Measured immediately
after, on the same asset: with the newest version correctly selected, and with the
agent stating in its own approval message *"I'll use the most recent, dimmer version"*,
the rendered clip came back from the **original, brightest** version anyway. Selection
is a separate defect from binding, and correcting one does not correct the other.
**Flattening (below) is mandatory, not a fallback.**

### 🚨 Image-to-video may bind a STALE VERSION of an edited still

Measured on Love Hate v6, 2026-08-08. A still that had been edited four times was
used as the start frame for an I2V clip, with the prompt explicitly asking for *"its
most recent version"*. **The clip rendered from an earlier version** — carrying two
defects that had already been fixed.

The consequence is severe and silent: every repair made to a still can be discarded
at the video stage, and nothing announces it. Only comparing the clip's first frame
against the intended still reveals it.

**Re-measured 2026-08-08 and CONFIRMED, with both obvious safeguards in place.** The
asset's newest version was correctly selected, and the agent's own approval message
said *"I'll use the most recent, dimmer version"*. The clip still rendered from the
**original**, several versions back. Neither the selection state nor the agent's stated
intent governs what I2V actually binds.

**Mitigation — flatten before animating. This is mandatory, not optional.** Tested and
**confirmed working** on Love Hate v6: the clip from a flattened source binds the correct
frame. There is no prompt wording that substitutes — that was tried and it failed.

The procedure, about two minutes per shot:

1. Open the asset and confirm the intended version is **selected**.
2. Download → **1K "Original size"**. Not 2K/4K — an upscale changes the pixels and adds
   a variable you did not ask for.
3. **Verify the file before re-uploading.** Mean luma via PIL is enough to tell a dim
   grade from a bright one; it costs seconds and catches a wrong download.
4. Re-upload through the page's file input (`find` the `type=file` element, then
   `file_upload` — never click the button, which opens a native picker you cannot
   drive). Flow files it under a new **Uploads** section.
5. **Name it distinctly** — `NN FLAT · <desc> · video source · <timing>` — so it can
   never be confused with the multi-version original.
6. Animate the FLAT asset by name.

**Always** compare frame zero of each clip against its source still before accepting
the clip, whether or not you flattened. Do this on the **first** clip of a run, before
committing credits to the rest: one wasted generation is the cheapest possible way to
discover this.

### Revert works
Version history is in the right-hand panel; clicking an earlier version
restores it. Always check the result of an edit — and revert immediately if it
degraded, before stacking another edit on top.

## ⚠ Rename by the IMAGE, never by the auto-caption

Measured on Love Hate v6, 2026-08-08. A shot was regenerated because the first
attempt broke its brief — an "empty street with nobody casting the shadows" came back
with two men walking in it. Both versions received near-identical auto-captions
("Empty street at night"). During the rename pass **the reject was named as the
keeper**, purely on its caption, and the correct version was left unnamed.

The result is the worst possible state: a wrong asset wearing the right name, which
every downstream step then trusts.

**Open the image and look at it before typing a name.** The caption describes the
*subject*, not the *outcome*, so a failed generation and its fix are usually
indistinguishable by caption alone. This matters most exactly where you regenerated
— i.e. where you already know one version is wrong.

Label rejects explicitly (`zz REJECT - <why>`) rather than leaving them unnamed;
"unnamed" is indistinguishable from "not yet processed".

### ⚠ A re-staged shot leaves its predecessor holding the slot name

Measured on Love Hate v6, 2026-08-08 — the sharper form of the trap above, and the
one that actually bit. Six shots were regenerated for blocking variety and renamed
into their slots. **Four of the frames they replaced were already named into those
same slots** from the previous round: `10 · a night doorway`, `09 · sharing a
cigarette`, `05 · the kiss`, `13 · the two falling onto a bed`.

So renaming the keeper does not resolve the ambiguity — it *creates* a duplicate.
Two assets now answer to shot 09, and the search filter returns both.

**Renaming a regenerated shot is a two-step operation.** Name the new keeper, then
immediately demote the frame it replaced. Doing only the first half is worse than
doing neither, because the collection now looks tidy.

The predecessors are easy to miss because they sit far away in the grid — they were
made in an earlier session, so they are separated from their replacements by every
asset generated since. Do not scan for them by scrolling; go to the shot list, and
for each slot you re-staged, open **every** asset that could plausibly be it.

### ⚠ A re-NUMBERING orphans names too — and the orphan proves the slot is TAKEN

Same session, worse variant. A revision that moves a shot between slots (rev3 gave
shot 04 to a new scene, shot 06 to another) leaves the *previous* occupants wearing
numbers that no longer describe them. Two frames were still named `04 · the two
dancing close` and `06 · two empty glasses on a wet bar` long after both slots had
been reassigned.

These are invisible to every cheap check, because the image is good and the name is
well-formed. Only opening the asset and reading **title against image** finds them.

**The trap: an orphaned name means its slot was taken, not that the slot is free.**
Seeing the dancefloor two-shot stranded on `04 ·`, I renamed it into `03 ·` — which
was already correctly held by a different frame. The fix created a duplicate. Those
two situations feel identical and are opposite.

So: **before moving a name into a slot, confirm the slot is empty.** Check the shot
list, then check the asset that should already be there.

The same renumbering also orphans **prompts**. A video prompt for shot 06 described
condensation on a drinking glass, which read as a random index error — until the
orphaned asset turned up. Under the old numbering, shot 06 *was* the glasses. One
cause, two symptoms, found hours apart. After a renumbering, re-read the prompts as
well as the names.

Two labels, and the difference is real:

| prefix | meaning |
|---|---|
| `zz REJECT (<slot>) - <why>` | the frame failed its own brief — the model ignored an instruction, or it duplicates blocking the film already has |
| `zz ALT (<slot>) - <what>` | the frame is good; the choice between it and the keeper is open and belongs to the director |

`zz` sorts both to the end of any listing while keeping them available. Never delete
— a wrong reference is a hazard, an unused asset is just inventory.

### The new asset panel makes this much easier

Flow's updated layout shows each asset's **full generation prompt**, creation date,
model and aspect ratio beside the thumbnail. That is the reliable discriminator
between a reject and its fix — their prompts differ even when their captions don't.
Use it in preference to captions for any audit.

## ⚠ In a silhouette shot, character references do nothing — identity must be in the OUTLINE

Measured on Love Hate v6, 2026-08-08. A shot specified as *"two men kissing, seen in
full profile as near-black silhouettes"* came back with both figures carrying the
same head: same hair volume, same jaw, same neck, same collar. It read as **one man
mirrored**, not as the film's two characters — even though both character reference
images were attached and every other shot in the film held them perfectly.

The cause is structural, not a bad roll. Flow's Characters feature carries identity in
**face and colouring**, and a silhouette discards both. With the faces unlit there is
nothing left for the reference to act on, so the model defaults to a generic head —
twice.

**A silhouette has only four carriers of identity**, and a prompt must name them
explicitly or the shot cannot hold its cast:

1. **Hair shape and volume** — tall and messy vs cropped tight to the skull
2. **Head and jaw profile** — narrow vs heavy and square
3. **Shoulder width and height** — the build, not the face
4. **Neckline** — a raised collar vs a bare shoulder and vest strap

Fixing it is one scoped edit that names all four per figure, with left/right stated so
the model cannot swap them, plus *"their two outlines must be immediately
distinguishable from shape alone"* and *"both faces still unlit and featureless"* so
the fix doesn't quietly light the faces to solve the problem.

**Generalises to any backlit, underlit, obscured, distant or rear-view shot.** Wherever
the face is not readable, the character reference is inert and the differentiation has
to be written into the prompt as silhouette geometry.

## ⚠ Tone-consolidate the OUTLIERS only, and change only the property that is wrong

Measured on Love Hate v6, 2026-08-08, over three attempts — the first two both wrong,
in different ways.

**Attempt 1 — a blanket grade.** Asked for a tone pass across 19 stills, the obvious
move is one grade instruction applied to every frame: lift the blacks, halate the
highlights, ease the contrast, add heavy grain. It reads as a careful plan and it
**makes the images worse**: *"the new filter makes it low quality."*

The mechanism is real and worth knowing. **An image edit re-renders the entire
frame**, so on a frame that is already right:

- "add heavy visible grain" lands as noise **on top of** the grain already baked in at
  generation — the result reads as compression artefact, not emulsion;
- "lower contrast, lift the blacks" flattens an exposure that was already correct;
- the re-render softens fine detail slightly, every time.

**But do not over-generalise from that**, which is the mistake I made next: I
concluded tone work could not be done in Flow at all and should be deferred to ffmpeg.
Two frames that *did not need the pass* say nothing about the frames that do. On a
genuinely off-look frame the same class of edit works cleanly.

**Attempt 2 — the wrong property.** Given the real list, I read "too clean" as missing
surface texture and added grain, mottling and dust. Also wrong: *"clean means the tone
not the stains."* The frames were never short of texture — their **colour** was
freshly white-balanced and digital, and they were the **brightest** frames in a film
that is otherwise night.

**What worked**, applied only to the named frames:

> **Do NOT add dust, specks, scratches, marks or dirt of any kind**, and do not change
> composition, framing or subject. **(1) The light is too bright** — bring the exposure
> down noticeably; the brightest areas should read as pale grey, not near-white.
> **(2) The colour is too clean** — expired-stock tone: no pure white and no neutral
> grey anywhere, highlights slightly off, a faint sallow yellow-green in the shadows,
> colours faded and muddied rather than fresh.

Plus a per-frame clause protecting whatever that shot cannot afford to lose — the one
warm shot must stay warm, face shots must keep faces natural and readable, and every
frame keeps its existing dominant colour so the film's colour arc survives.

Three rules that fall out of it:

- **A note about the look names a symptom, not a mechanism.** "Too clean" can mean
  texture, colour or exposure. Ask which before choosing an instruction.
- **Test on a frame the director named**, not one of your own choosing. Both failed
  passes were tested on frames that were never on the list.
- **A frame that already looks right needs nothing.** Grade outliers only, and confirm
  the outliers are outliers first.

A whole-film grade — matching every shot to every other — still belongs at assembly in
ffmpeg (`eq` / `curves` / `colorchannelmixer`), where it is arithmetic on pixels rather
than a re-render. Per-frame Flow edits are for fixing *specific* frames that are wrong.

## ⚠ Motion in an empty frame needs a stated CAUSE, or it reads as a presence

Measured on Love Hate v6, 2026-08-08, on the first rendered clip. A shot of an empty
unmade bed was given the motion *"one fold of the sheet releases and settles into the
hollow"*. The clip is technically exactly that — and it is **uncanny**: a sheet moving
by itself, in an empty room, with nobody there. It reads as a poltergeist, not as
absence.

The cause is a prompt error, not a model error. The *"name two observable motions per
shot"* discipline is right, but on an **absence** shot it pushes you into inventing
motion that nothing in frame could have produced. A body could move that sheet — and
the whole point of the shot is that the body is gone.

**Every motion in a people-free frame must have a visible or stated physical cause.**
Auditing the rest of the film found this was a pattern, not a one-off — three of five
people-free shots had it:

| motion | verdict |
|---|---|
| a colour field drifting, grain crawling | ✓ the medium itself is the cause |
| fog re-forming on cold glass, a droplet running | ✓ condensation, gravity |
| litter turning over in the wind, a lamp flickering, moths circling | ✓ wind, electrics, insects |
| **a coat swaying on its hook** indoors | ✗ no draught named |
| **a sheet folding itself** | ✗ nothing touches it |
| **shadows wavering where nobody stands** | ✗ **worst** — the premise is that nothing casts them, so movement puts someone there |

Two ways to fix, and prefer the first:

1. **Name the cause** — *"a draught under the front door stirs the hem of the coat"*.
   The detail survives and becomes motivated.
2. **Change what moves** — for the bed, the light creeping as the sun rises and dust
   motes turning in the beam, with *"the bedding does not move at all"* stated
   explicitly. The shot still has two motions; both have a source.

For shadows specifically: **intensity may change, shape may not.** A flickering lamp
legitimately makes a shadow's edges harden and blur. A shadow that *shifts position*
has a body behind it.

## 🚨 The VIDEO stage has a stricter content gate than the image stage

Measured on Love Hate v6, 2026-08-09, across three refusals. **Nano Banana will generate
stills that Omni Flash then refuses to animate**, failing with *"This generation might
violate our policies."*

On that film the boundary was **physical contact between two men** — not nudity, and not
the act:

| shot | both men | touching | clothing | result |
|---|---|---|---|---|
| eye contact across a room | yes | **no** | full | ✅ |
| side by side on a doorstep | yes | **no** | full | ✅ |
| bathhouse, bare back | yes | yes | bare | ❌ |
| a kiss, near-black silhouettes | yes | yes | full | ❌ |
| **pressed to a wall, fully clothed, both faces away** | yes | yes | **full** | ❌ |

The third refusal is the decisive one: the least explicit framing of the three still
refused, which rules out nudity and explicitness as the trigger. Two shots carrying both
characters *passed* — so it is not "two men in frame" either.

**The gate reads the START FRAME, not the prompt — so rewording cannot rescue a shot.**
Tested to exhaustion on one refused image:

| attempt | prompt | result |
|---|---|---|
| 1 | body language described (*"lowers his head closer to the neck"*) | ❌ |
| 2 | that clause removed, other body language kept | ❌ |
| 3 | **environment only** — a flickering tube, one water drip, and an explicit *"everything else in the frame stays completely still and unchanged"* | ❌ |

The third prompt described no bodies at all and still refused with the identical message.
**This matters because the error text says "Please try a different prompt", which points
at exactly the thing that does not work.** Do not spend credits iterating wording.

**Do not assume the still stage predicts the video stage.** If a film has an intimate
register, test **one contact shot early**, before generating the whole still set around
an assumption that it can be animated. 15 credits at the start is far cheaper than
discovering it after the stills are finished.

Since the image is the variable, the productive fallback is to **re-stage the still** —
same beat, figures near but not touching — and animate that. The still stage has never
refused any of this material.

Practical consequences:

- Budget for refusals. They cost credits and produce nothing.
- **Count the `Videos` list to know what actually succeeded.** A failed generation never
  appears there, so the count is the only honest signal — the chat shows an approval and
  a scheduled message either way.
- Fallbacks when a shot is refused: hold it as a **still** in the edit (a held frame
  among moving ones reads as deliberate), **re-stage** so the figures are near but not
  touching, or try a **different video model** — a different policy surface may apply.

## ⚠ A generation is evidence only when it has FINISHED

Corollary of the above, and it cost two wrong conclusions in one project. A clip sitting
at 23% is not a pass. I twice reported a diagnosis built on an in-progress render, and
twice the render subsequently failed — once producing a confident, wrong theory about
where a content boundary lay.

This is the same error as judging a still from a loading placeholder, and it is easier to
make on video because progress percentages *look* like evidence of success.

**Wait for terminal state, then count the `Videos` list.**

## ⚠ Image-to-video (Veo 3.1 Fast): what the start frame invites, the model does

Measured on 不可說, 2026-09-13/14: 59 video generations, 8 s 720p x1 at 10
credits on Ultra. Every row below cost at least one regeneration.

| Start frame / prompt | What Veo did | What worked |
|---|---|---|
| Casement window with an opening sash in frame + any camera move | Rotated the sash. A later version slid a timber post as a separate object; another invented a new frame bar crossing the image (3 shots) | Edit the still to fixed glazing with no hinge in frame. For "static except water", use the **same image as first and last frame** and describe water-only motion |
| Curtain asked to billow | Lifted high and revealed an invented gold multi-globe lamp | Cap the motion ("small hem sway, no lift") and clean ambiguous blur behind the curtain first |
| Quiet paper-on-desk shot | Flipped the page and the pencil vanished; another version added a finger | First+last frame lock; state "no page turn, no hands" |
| Single water drop | A second drop appeared mid-clip | First+last frame; or select the range before the second event |
| Dawn lake ending | A fishing rod entered frame | Regenerate; check frame edges through the whole clip, not samples |
| Moonlit sky, lateral move | Sky drifted green across the clip | Regenerate; grading could not clean a progressive colour drift |
| "Lateral truck" prompts | Often weak displacement, or rotation instead | Reliable here: tilt-up, push-in / dolly-back, rack focus, and lateral moves with a near foreground (reeds, branches) for parallax |

Rules:

- **The start frame is the prompt.** Remove anything you do not want animated
  (hinges, lamps, loose pages) from the still before spending credits. Rewording
  is the weaker lever, the same lesson as the content gate above.
- **Output was 1280×720, 24 fps, 192 frames.** Plan 1080p delivery as a post
  step: upscale a textless master and render text natively at 1080p.
- **A connection drop during *Start generation* may or may not have
  submitted.** Check the project's job list before resubmitting.
- **Real text never survives generation.** Clean fake glyphs in the still,
  composite the lyric afterwards (Blender, planar), and re-overlay the paper
  if animated reflections cross it.

## ⚠ Flow UI traps measured on 換班 (2026-09-15)

- **The frame picker's preview follows a CLICK, not a hover.** Hovering a
  second option left the preview on the first one (the previous start frame).
  Click the option, confirm the preview is the intended still, then press
  *Add to prompt*. Options sort by recent use, so reference images you just
  attached float above the new generation.
- **"Extension not connected" does not mean the JS did not run.** An ingredient
  attach + prompt fill reported a disconnect and had in fact completed. Read the
  prompt box (text length, attached thumbnails) before retrying, or the retry
  attaches everything twice.
- **Video mode reopens on Ingredients.** Switching Image → Video selected
  Ingredients; Frames had to be picked explicitly before the Start/End slots
  appeared. Confirm the quote reads 10 credits for Veo 3.1 Fast 8 s x1.
- **Downloaded zip names are the prompt truncated by words.** "The camera slowly
  pushes toward her…" arrived as `The_camera_slowly_pushes_toward_<timestamp>.mp4`;
  a prefix one word longer matched nothing. Match on a short word prefix, then
  bind by content hash.
- **A shared Downloads folder carries other sessions' zips.** Accept only files
  newer than your baseline whose inner name starts with your prompt.

## Direct-mode video, measured on 說得太急 (2026-09-22)

The agent-session approval traps above belong to **agent mode**. With the
Agent pill off, three Veo clips went out back to back with **no approval
widget at all**, ran concurrently (~1–2 min each), and the balance dropped by
exactly the quote (3 × 10).

> ⚠ **Direct mode has no credit gate.** Clicking `Start generation` spends the
> quote immediately — nothing asks. So the human approval has to happen
> *before* that click: get a yes from the user for the batch (shots, count,
> credits) in chat, and never send a paid generation the user has not approved.

The working loop:

1. Settings pill → **Video** → **Frames** → `Veo 3.1 - Fast` → 8s → x1; zoom the
   popup and confirm *"Generating will use 10 credits"*.
2. Clipboard-paste the start image into the composer: in Frames mode it lands
   in the **Start** slot (not as an ingredient). Wait until the slot shows the
   thumbnail, not a grey placeholder — pasting the prompt early is fine, but
   sending before the upload finishes is not.
3. Paste the prompt, zoom the composer (Start thumbnail + full text), send via
   the `Start generation` button — found by reference, since the composer
   moves when the popup or a long prompt resizes it.
4. Count the **Videos** tab. Open a clip: the detail view's download icon is at
   the top right beside the trash; choose **720p Original size** (free).
   1080p is an upscale; **4K costs 50 credits** — never click it by habit.
5. Downloads arrive as `<Flow title>_<timestamp>.mp4`, where the title is
   either the prompt truncated by words (換班) or a short caption Flow writes
   itself ("Two men sitting in cafe", 說得太急) — so neither is a key. Bind
   files by timestamp order to what you submitted, then by content hash.

Read the balance from the avatar menu (`N Google Flow credits`) after the batch
and reconcile it against the quotes before the next one.

**The start frame decides what gets animated** (see also the Veo table above). A
subject already at the end of his action made Veo invent a second man; a
painted shadow stayed painted; a lean became a bow. Stage the still for the
*beginning* of the motion — `tool-blender-scene-reference` § Staging a start
frame for video.

**Do not buy Veo for “almost nothing”.** On 說得太急 (2026-09-23), prompts
for a three-centimetre hand lift, a frozen raised hand and a tiny posture change
reliably escalated into lowering, clasping, reaching, drinking or visible
speech. Keep a clean segment if one exists; otherwise use controlled local
still drift. Reserve Veo for motion whose continuity matters (walking through
space, a bus crossing the window), and let bar-led reuse cover repeated chorus
material.

## Record every Flow submission in the MV library

`{vault}/10_Projects/YouTube-Music-Channel/library/` holds one row per
generation (format: its `SCHEMA.md`). For MV work in Flow:

1. **Before prompting**, read the matching `patterns/` notes — for edits
   `edit-keep-composition-one-change`, for new angles `reference-only-as-role`,
   for Veo `locked-off-camera`, `closed-lip-performance`,
   `single-motion-nothing-else-moves` — and their known failures.
2. **On each submission**, record a row with `verdict: "unreviewed"`: exact
   prompt, `platform: google-flow`, model and mode from the SCHEMA table, input
   hashes, quoted credits, `pattern_ids`. An x2 request is two rows sharing a
   `batch_id`, with distinct `attempt` numbers.
   From the EmptyOS repo root:
   `python scripts/mv_library.py record-attempt --file row.json`
3. **After download and review**, update the same `attempt_id` with `--update`:
   output path and sha256, `verdict`, `codes` from `failure-codes.md`,
   `reason`, `evidence.path` (a vault-relative file that exists). A tile that says *Failed* is
   `generation-failed` with `output: null` and the charge as shown. A stale
   version bound as start frame is code `stale_version_bound`.
4. Finish with `python scripts/check_mv_library.py`.

Flow output carries SynthID: approved stills recorded with `record-asset`
(required fields: SCHEMA §2) get `rights.watermark: "synthid"`. Never copy lyrics into a row.

## Review at full size, never from thumbnails

Two defects on 无所住 were **invisible in the grid and obvious full-screen**:

1. **Cultural fit** — a "roadside flower" frame rendered as an English country
   lane (bare deciduous trees, tarmac) in a film set in a Huizhou town. The only
   frame with no Chinese context at all.
2. **Continuity** — two consecutive shots of *the same flower* showed a white
   anemone and a daisy.

Open every frame individually before declaring a set done.

## Shot mapping lives on the assets

Flow has **Rename** in each image's ⋮ menu. Name keepers
`NN · description · motif/state · timing`, leave superseded versions with their
auto-names, then **search `·` to filter to exactly the keeper set**. This
survives sessions and puts the mapping where the video stage needs it.

## Cleanup

⋮ → **Move to trash** (recoverable; *Restore All* in the Trash view). Never
empty the trash.

**Verify by name before every removal.** The grid reflows after each deletion,
so coordinates go stale and blind clicking opens the wrong asset — one such
click opened a keeper's detail view instead of a menu. Read the label, then act.

## The failure mode that recurs — constant text overwriting variation

Four separate defects on 无所住 had one cause: **anything held constant across
shots silently overwrites anything meant to vary across shots.**

| Symptom | Constant that caused it |
|---|---|
| A kite appeared in a shot with no kite | a style contract listing per-shot literal anchors, appended verbatim to every prompt |
| Rain fell in all 18 shots, including the clearing sky and the final stillness | one shared material-behaviour string containing "rain visibly strikes surfaces" |
| 13 of 18 frames were the same photograph | one conversation + the agent's style reference |
| Every frame sat at one flat tone | an identical palette line in every prompt |

**Rule: a globally-appended string may contain only what is true of every
frame.** An object, a weather state, or a tonal key belongs in its own shot's
description. Any per-act arc — weather, tone, framing — must be written into
the per-shot prompt or it will not survive.

## Licensing

Nano Banana output carries Google's terms and a **SynthID watermark with no
opt-out**. Different position from local Apache-2.0 models. Check before
monetizing.

## Cross-references

- `creative-mv-art-director` — define the visual language first; this skill executes it
- `creative-mv-generator` — the EmptyOS Music Studio staged pipeline (local GPU)
- `tool-comfyui-image` — local FLUX generation, no watermark, commercial-safe presets
- `{vault}/10_Projects/YouTube-Music-Channel/songs/2026-02-23__无所住/` — the worked example: `art-direction.md` § Generation method, `stills-run-2026-08-07.md`
