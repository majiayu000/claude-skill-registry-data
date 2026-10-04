---
name: omni-ugc-ad-factory
description: Produce a UGC-style talking-head video ad end to end on the MaxFusion MCP — research the product with user-supplied competitor leads, tear down 5 competitor Meta ads and 5 organic TikToks, write a pain-driven script that sounds like a person talking (never like an ad), reverse-prompt a rights-clean photoreal actor from a user-supplied reference photo, generate two chained 10-second Gemini Omni clips that play as one continuous take, and ship a single seamless 9:16 MP4. Use whenever the user wants a UGC ad, a talking-head ad, an ad for an app or product, mentions Omni or Gemini Omni Flash, drops an actor photo and asks for a video ad, or says anything like "make me some UGC", "let's make ads for X", or "another variation". Built for Claude Code (local ffmpeg); degrades to Claude app with documented fallbacks.
---

# Omni UGC Ad Factory

Turns a product + an actor reference photo into **one finished ~20-second UGC ad**: two
chained 10-second Omni clips stitched into a single seamless **9:16 vertical MP4**. That file
is the deliverable — no composites, no extra formats. The user does what they want with it.

**Model:** `gemini-omni-flash`, locked. The only model that produces synchronized speech AND
10-second clips. Casting stills: `gpt-image-2`, locked (see `references/actor-image.md` —
nanobanana produced plastic skin through four rounds of tuning; the model is the first
variable to change, not the last).

---

## How this skill is enforced — read this first

**You never hand-write a prompt for a paid generation call.** Every prompt is *assembled* by
a gate script from structured JSON you write. If the gate fails, you fix the JSON and re-run
it. The generation call uses the approved file's content **verbatim**:

```
casting.json  → scripts/gate_casting.py →  ad1/approved_casting.txt  → gpt-image-2
clip1.json    → scripts/gate_omni.py    →  ad1/approved_clip1.txt    → gemini-omni-flash
clip2.json    → scripts/gate_omni.py    →  ad1/approved_clip2.txt    → gemini-omni-flash
```

The gates encode every production failure this pipeline has ever had: age-drifted casting,
device words rendering into frame, robot voices, choreographed disfluencies, "same girl"
identity shorthand, ad-copy closers, re-described seed frames, negated visual instructions,
missing camera landings. **A prompt that skipped its gate does not exist.**

Data files the gates read (edit these to improve the system, not the prose rules):
`data/age_lexicon.json` · `data/delivery_glossary.json` · `data/voice_spec.json` ·
`data/color_grading_glossary.json`

---

## The chaining mechanism

Omni holds its reference image for the first ~8–10 frames before dissolving into the
generated scene. Seed clip 2 with clip 1's trimmed final frame and that hold becomes an
invisible join. The order cannot be rearranged:

```
generate clip 1 → TRIM clip 1's dead-air tail → extract the trimmed clip's last frame
              → seed clip 2 with it → generate clip 2 → seam-check → trim tail → stitch
```

**Trim clip 1 before extracting the seed** — trim after, and clip 2 chains to a frame that no
longer exists in the final cut. `scripts/adkit.py` enforces this.

**Corollary:** the hold also puts the casting still's *lighting* on screen for the first
third of a second of every clip. Prompt the scene the still is already lit for, or the
dissolve IS a visible mid-clip light change.

---

## 0 — Setup: one round of questions, then stop asking

Ask all of these in **one** message, then infer everything else:

1. **Actor age bracket** — 20s / 40s / 50s (drives the casting lexicon, mechanically).
2. **Delivery tone** — yapping & fast / agitated & fed up / excited & hyped / calm, honest & direct.
3. **Visual lane** — lane zero (no graphics — the default and usually the best) /
   hand-drawn illustration / bold color + arrows / motion graphics / environment & light.
4. **Research leads (open question):** "To make research fastest — do you know your
   competitors? Paste their Meta Ads Library URLs if you have them, or just give me the
   keywords that best fit the product. Otherwise I'll search from scratch."
5. **Actor reference image:** ask the user to supply one (Pinterest or anywhere).
   Recommend: *a natural, uneven, real photo — ordinary light, imperfect framing, no studio
   polish. The more accidental the photo, the better the actor.*

If the user already answered any of these, don't re-ask. If they say "you pick", pick, state
the pick in one line, move on.

## 1 — Research the product

Web-search it. Establish what it does, its **mechanism** (the specific thing it does that
solves the problem), and the real pain in users' own words (reviews, Reddit, App Store).
"Reduces screen time" is a category. "Makes you take a breath before the app opens" is a
mechanism. The mechanism is what the ad turns on.

## 2 — Pull reference: 5 paid + 5 organic

**Use the user's leads first.** Competitor page URLs → pull those advertisers directly.
User keywords → use them verbatim before inventing your own. Only fall back to your own
queries if theirs return nothing — and then follow the keyword-hygiene rules in
`references/pitfalls.md` §4 (query the advertiser's copy-words, 2–3 words, check hit rate,
dedupe by `page_id`, `days_running` is age not runtime).

**Meta** — `maxfusion_search_meta_ads`: `media_type: "video"`, `limit: 10`, select 5.
**TikTok** — `maxfusion_search_tik_tok`: `sort: "most_liked"`, `count: 10` (enum floor), select 5.
Rank organic by **save rate** (saves/views), not views. Import via `maxfusion_import_meta_ads`
/ `maxfusion_import_tik_tok`.

## 3 — Tear them down on the canvas

One flow, two `flowGroup`s (paid: adItem ×5; organic: tiktokItem ×5), each into a
`contentAnalyzer` (`gemini-3.1-pro-preview`, master prompts left `""` — the backend hydrates
forensic transcribers; don't rewrite them). Validate (free) → run → read
`runtime_state.node_outputs[node][0].items[].analysis_text` via `maxfusion_get_flow`.

> ### HARD GATE — no analyzer text, no scripts
> Metadata is not research. Ad copy, page names and engagement counts assemble a confident,
> plausible, **wrong** thesis — this happened on a real run and had to be retracted in full.
> If the user asks for scripts before the teardown has run, say you can't write them yet.

Mine: **hooks separately from pitches** (first-3-seconds VO verbatim), **CAST across all
ten** (the uncast role is usually the ad), and the pain nobody is saying out loud.

## 4 — Write the script

**PROBLEM (pain) → TWIST THE KNIFE → SOLUTION.** ~25–28 words per 10s clip (drop to ~22–25
with heavy disfluency). Clip 1 = problem + twist; clip 2 = solution. Two **distinct**
candidate scripts, presented in **one** approval gate; the user approves one.

**The not-an-ad law.** This is a person talking, just sharing what's up — never copy:
- The product name gets the **smallest** event, thrown away mid-sentence, unstressed.
  Bury the endorsement in a subordinate clause she isn't paying attention to.
- The strongest structure: **complaint-as-endorsement** — she's annoyed she needs it, or
  humiliated that it worked. She's already on the viewer's side against the ad.
- Real speech ends on something unimportant. One line of pure waste. One line unresolved.
  No em dashes (Omni performs them). No antithesis pairs. No closers.
- The `gate_omni` script enforces the mechanical tells (dashes, ad-copy closers, word
  budget); **the ear test is yours**: read it aloud — if a copywriter would be proud, rewrite.

**Then the humanizer — forced, not inferred.** Read `references/humanizer.md` **in full**
and apply it to the approved script. If that file is a placeholder, STOP and tell the
operator. Never substitute your own idea of "humanize".

## 5 — Compile the Omni prompts (beat tagging → glossary → gate)

For each clip, write `ad1/clipN.json`:

1. **Beat-tag** every script line with the speaker's internal state, from the glossary's
   state list (venting, ashamed, resigned, thinking, deciding, confiding, …).
2. **Pick behaviors per beat** from `data/delivery_glossary.json` — only behaviors valid for
   that beat's state, within budget (3–6 per clip, ≥2 categories, throat-clear once per ad).
   Weave each behavior's phrasing into the `delivery` prose (the gate verifies it's there).
3. **Write the voice block once** — all six categories: pitch placement, texture, pacing,
   volume dynamics, terminal pitch, accent mechanics (a **city**, rhoticity, vowel shape).
   Paste it **byte-identical** into clip 2 (the gate hashes it).
4. **Delivery = states, never choreography.** "She runs out of air so her voice sags into a
   creak on its own" — never "creak on the word 'day'". No emotion words anywhere.
5. **Clip 2:** `style` must be `""` and nothing may re-describe face/hair/wall/light/crop —
   the gate injects the seed-premise line itself and fails you on any visual re-description.
6. **Closing:** the speech may trail off; the camera never does. Land the shot: still, eyes
   open, mouth closed, camera locked (clip 1's closing IS the seed frame).
7. **`framing_hold` (clip 1, when the casting still has a hard angle):** Omni's prior is a
   centred level talking head and it will quietly straighten a canted/low/off-centre shot.
   State positively what STAYS true for all ten seconds ("the frame stays canted, she keeps
   the phone where it is…"). The gate rejects prohibitions. Expect partial obedience — the
   model resists hard angles; production practice is to also trim clip 1's head past the
   hold-then-dissolve jump (step 8) so the ad opens on the model's settled frame.

Run `python3 scripts/gate_omni.py --input ad1/clip1.json --workdir ad1/` until PASS.

## 6 — Cast the actor (reverse-prompt, never invent)

**Casting is reverse-prompting the user's reference photo.** We do not compose an image of
our own, and we do NOT pass the photo in `references` (that clones a real person — rights
problem; text-to-image only). The photo is read with your eyes, exhaustively:

1. **LOOK at the photo with a tool** — crop, enlarge, view. Never assert from memory; when
   corrected, re-open the image, don't re-reason.
2. Write `ad1/casting.json`, reverse-prompting every field from the photo: `subject`
   (mechanics, not emotions — and include **eye color**; omit it and the model picks its
   own), `framing_angle`, `shoot_style`, `lighting` (direction + source + hardness + how it
   sits on the skin), `color_grade` (terms from `data/color_grading_glossary.json`),
   `background`, `composition_accidents` (a real photo is badly made — canted, off-centre,
   clipped, missed focus).
3. `physiology` comes from the **age bracket lexicon**, not from taste: the gate requires
   ≥4 right-age terms and zero wrong-age terms (`data/age_lexicon.json`). Never write
   "young" — write the physiology and let age fall out.
4. **Device words never appear** — iphone/phone/tripod/ring light render INTO the image.
   Describe the *look* of the capture, not the equipment. The gate enforces this.
5. The still's lighting must match the scene the clips will prompt (see Corollary above).

Run `python3 scripts/gate_casting.py --input ad1/casting.json --workdir ad1/` until PASS.
Generate: `maxfusion_generate_image`, `model: "gpt-image-2"`, `aspect_ratio: "9_16"`,
`quality: "high"`, `image_count: 2`, prompt = `approved_casting.txt` verbatim. User picks.
Check the pick against the bracket — a mis-aged actor is baked into every clip downstream.
Change ONE variable per correction round.

## 7 — Generate clip 1

Upload the chosen still (`maxfusion_upload_asset`: filename, size_bytes,
`purpose: "image_reference"`, content_type), then:

```
maxfusion_generate_video:
  video_model:        "gemini-omni-flash"
  aspect_ratio:       "9_16"
  duration:           10
  resolution:         "720p"
  ref_image_mode:     "ingredients"
  ref_image_file_ids: [<still file_id>]
  prompt:             <ad1/approved_clip1.txt, verbatim>
```

Omni has **no `frames` mode** — `start_frame_file_id` fails validation. Chaining is step 8.

## 8 — Trim, extract the seed, chain clip 2

**Claude Code (primary):** download the clip from its asset URL, then
`python3 scripts/adkit.py seed --clip1 clip1.mp4 --workdir ad1/` — measures speech, trims
the dead-air tail, extracts the trimmed clip's last frame. **Also trim clip 1's head**: the
hold-then-dissolve leaves ~5–10 reference frames then a hard jump (interframe delta spike
>15/255) — measure it, cut clip 1's start at the spike (speech starts later; nothing is
lost), and update `state.json`'s clip1 path/duration. Clip 1's head is safe to trim; only
clip 2's head is sacred. **Look at the seed frame** (one
view call): clean, still, eyes open — a mid-blink frame chains badly. Upload it, generate
clip 2 same params, `ref_image_file_ids: [<seed frame file_id>]`,
prompt = `approved_clip2.txt` verbatim.

**Claude app (fallback):** no local ffmpeg / S3 blocked → measure the tail by watching the
clip, use `maxfusion_extract_video_frame` (video_id + timestamp just before dead air) for
the seed, and ask the user to attach MP4s when a measurement is needed. Say this up front.

## 9 — Seam-check, stitch, deliver

`python3 scripts/adkit.py finish --clip2 clip2.mp4 --workdir ad1/` — verifies the seam
(mean abs diff of clip 1's end vs clip 2's frame 0 must be **< 5/255**; FAIL = clip 2 wasn't
seeded right → regenerate, never paper over), trims clip 2's tail (never its head — the held
frames ARE the seam), and stitches both trimmed clips into one **9:16 MP4**.

**Deliver that file. It is the whole deliverable.**

Then recommend (don't do): *"Omni's audio is studio-clean; a room-tone bed ~15dB under the
voice makes it sound recorded. Send me a room-tone/ambience file and I'll mix it in."* Mix
only if the user provides a REAL recorded bed — a synthesized noise bed was tried in
production and rejected by ear; do not synthesize one. Measure, never fix the gain:
bed_gain = (voice_mean − 15) − bed_mean, mixed with `amix normalize=0`; a quiet stretch
should lift ~8–14 dB and the voice mean must stay within 0.2 dB (commands in
`references/pitfalls.md`).

Variations: if the user wants another ad, repeat 4–9 with a different pain/angle (lane zero:
the diversity axis is the angle and the pain, not decoration).

---

## References & files

- `references/pitfalls.md` — every production failure: symptom → cause → fix. **Read before
  the first generation call.**
- `references/omni-prompting.md` — beat structure, visual lanes, positive-language rules.
- `references/actor-image.md` — Raw Camera Casting Realism (condensed) + age-texture
  decoupling + the casting rules that each cost a wasted generation.
- `references/raw-camera-casting-realism-master-prompt.md` — the full master realism prompt
  (canonical source for the style; the age lexicon modulates it per bracket).
- `references/delivery.md` — how a real person actually talks: invariants, register
  transposition, state-not-choreography.
- `references/humanizer.md` — the operator's humanizer. **Forced read at step 4.**
- `scripts/gate_casting.py`, `scripts/gate_omni.py` — the gates. `scripts/adkit.py` — trim,
  seed, seam, stitch.
- `data/*.json` — the four glossaries the gates enforce.
