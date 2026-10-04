---
name: youtube-packaging
description: Generates click-optimized YouTube packaging — 3 thumbnail bets under one fixed title, engineered for YouTube's built-in A/B/C thumbnail test, plus a value-forward description, then renders the thumbnails as real images. Use this whenever you want to package a long-form video or turn a video idea into titles and thumbnails. Triggers include how would you package this, title ideas for, thumbnail concept, package this video, A/B variations, and make this clickable. Calibrates to your channel's own CTR data if you have it. Long-form only, never Shorts. Not for non-YouTube copywriting.
---

# YouTube Packaging (Title + Thumbnail)

Turns a video idea into **one locked title + 3 distinct thumbnail bets** built for YouTube's native
A/B/C thumbnail test, plus one value-forward description — then **renders the three thumbnails as
real images** with Nano Banana Pro.

The whole skill optimizes for one number: **CTR** (click-through rate). It's the metric YouTube
Studio reports per thumbnail, and the only one that isolates *packaging* from topic and algorithm.

## Where these rules come from, and what to do about it

The rules below are not generic YouTube advice — they were derived from Studio CTR data across 20
long-form videos on a real ~1M-subscriber beginner/AI channel, read in CTR order. That dataset isn't
shipped (it's another channel's numbers, and its absolutes wouldn't transfer). The **patterns** do
transfer, and they're a much better prior than guessing.

**But an inherited rule is a bet, not a fact — about YOUR audience.** So:

- **Cold start (no channel data yet).** Use these rules as-is. **Say so when you package**: "these
  are uncalibrated defaults — your own CTR data will beat them." Then tell the creator to start
  logging CTR from video 1.
- **Calibrated (~10+ long-form videos with CTR).** Run `references/channel-calibration.md` first,
  then follow *that* file's numbers wherever it disagrees with this one. **Their data wins over
  anything written here.**

Ask which mode you're in if it isn't obvious. Never quote a target CTR the creator hasn't measured.

## The core model — read this first

**Views = Reach × CTR. Two different levers, driven by two different things.**

- **Reach** (how many people YouTube serves it to) comes from the **topic** and from riding **known
  discovery waves** — a tool everyone's searching, a real news moment, a broad money/free promise.
  **Packaging cannot fix a low-ceiling topic.**
- **CTR** comes from **packaging craft** — concrete promise, magnet word, barrier-drop, one bold
  thumbnail hook. **This is the only lever this skill controls.**

Good packaging on a narrow topic produces good CTR and low views. **That is correct behavior, not a
packaging failure.** Never blame a title when CTR is healthy and views are small — and never expect a
title to rescue a topic nobody wants.

**The one guardrail that stops this becoming hollow clickbait:** the promise must be one the video
actually keeps. Overpromise → the viewer bounces in 30 seconds → retention craters → YouTube chokes
the exact reach you were chasing. **The widest promise that also holds** is what makes YouTube widen
distribution. Reality beats expectations.

## The flow

Run it in order. Stages 1–2 are fast; the value is getting the *promise* right before generating,
because a wrong promise wastes all three bets.

---

### Stage 1 — Intake

Ask in one message:

1. **Core idea** — what's the video about / the rabbit hole.
2. **The concrete takeaway** — the *one clear thing* the viewer walks away with. This becomes the
   promise. If you can't say it in a sentence, the packaging will be vague — push to name it.
3. **Audience** — who clicks this: beginners, practitioners, or a mixed/wide audience? This sets how
   much jargon a title can carry. (A wide/beginner channel should package for the widest clickable
   promise and do its segmentation *inside* the video, never by narrowing the title.)
4. **Locked angle or term?** — any angle already committed to, especially a coined/branded phrase.
5. **Conversion target** — what the video pitches (a course, a tool, a repo, a newsletter, nothing).
   Needed for the description. "Nothing" is a valid answer.
6. **Channel data?** — do they have ~10+ long-form videos with Studio CTR? Sets calibrated vs cold
   start. If calibrated and `references/channel-calibration.md` is still empty, offer to run it first.

---

### Stage 2 — Ceiling + promise (checkpoint before generating)

**Gate 1 — Topic ceiling.** Classify honestly:

- **HIGH** = broad demand riding a known wave (money / save-money, a broadly useful free capability, a
  major tool everyone knows).
- **NARROW** = niche format, niche tool, or an insider flex.

If narrow, **say so plainly and reset the view expectation** *before* generating: packaging will
still maximize CTR, but views are capped by demand. Then decide whether the topic is worth making
*for conversion* even if reach is low. That's a real strategy, but it should be a choice.

**Gate 2 — The promise.** Draft the core promise as the **clearest concrete takeaway, stated
plainly** — NOT a withheld-drama curiosity gap.

- Spell out the takeaway: name the number, the tool, the saving, the outcome.
- Don't withhold or moralize. "X Can Do More Than You Think" and "X Is Dead" are the classic floor.
- **If the video is built on a mechanism** — an experiment, a build-off, a comparison — **the lesson
  is the headline; the mechanism is only how the lesson surfaces.** Never lead with the mechanism.

**CHECKPOINT:** State the ceiling classification and the one-line promise. Confirm or fix the promise
before generating. Do not skip — three bets off a wrong promise is wasted work.

---

### Stage 3 — Generate the packaging

**Structure this correctly, it's the thing people get wrong:** YouTube's Test & Compare is
**thumbnail-only. The title is FIXED across all three variants.** So the deliverable is **ONE primary
title × 3 thumbnail bets**, not 3 independent title+thumbnail pairs.

**First, lock ONE title.** It must pass most of the Title Checklist below. Output with it:

- **Implied expectation** — one line: what the viewer expects walking in. The intro must pay this off.
  Carry it into the script.

**Then 3 thumbnail bets** under that fixed title. Each pulls a **different lever**, so YouTube
compares real alternatives rather than three flavors of one idea. For each:

- **Thumbnail concept** — composition per the Thumbnail Checklist: face + expression, the *one*
  dominant hook (word or number), color pop, any object.
- **Thumbnail text** — a **1–3 word fragment that combines with the title, never repeats it.**
- **Lever** — which lever it tests, one line on the bet.
- **Honesty check** — does this frame stay true under the fixed title, and does the video keep it? A
  thumbnail promising a beat the video doesn't have must be pulled or the beat must be built.

**Lever menu — pick 3 different ones:**

- **Magnet-word lead** — Free / Unlimited / 100% / $0
- **Number/$ lead** — a specific figure as the hook
- **Barrier-drop lead** — for beginners / no coding / without [skill]
- **Object / curiosity-anchored lead** — a tangible thing + a value contrast, or a named valuable
  thing the viewer wants ("the one skill")
- **News / "Now" lead** — only if something genuinely changed
- **Own-term / brand-fit lead** — a coined term. Lower reach (rides no wave) but strong identity —
  good as *one* of three, rarely all three.

Then close Stage 3 with:

- **One description** (one per video). Save to `videos/<project>/packaging/description.txt`:
  1. **2-line value hook** — the concrete payoff in plain words; name the *specific* things they'll
     learn (the real number, the free tool, the exact capability). The title sells the takeaway;
     these two lines make it specific and undeniable.
  2. **CTAs** — lead with the one matching the Stage 1 conversion target, then any others (repo,
     free resources, newsletter). If something is free, say so plainly.
  3. **Timestamps / chapters** — first chapter at `0:00`, keyword-rich labels. Derive from the edit
     plan / final cut; re-confirm if the cut length changed.
  4. Short like/subscribe nudge.
- **Self-check** — run the title and each thumbnail against both checklists; flag any rule bent and
  why it's worth it.
- **Baseline note** — if calibrated, restate their measured median + stretch target. If cold start,
  say plainly that there's no baseline yet and this is the first data point. You may predict which
  bet lands highest and why — **but the test decides. Never crown a winner**; the deliverable is 3
  worth shipping.

---

### Stage 4 — Refine

Iterate — tighten the title, swap a lever, adjust a hook. All 3 run live in the A/B/C test, so the
goal is **3 you're willing to ship**, not one.

---

### Stage 5 — Render the thumbnails (Nano Banana Pro)

Turn the 3 locked concepts into actual images. **The dedicated `/thumbnail` skill is the
interactive render engine for this stage** — it interviews for style elements (environment,
text budget, extras) with the creator's calibrated defaults (minimal text) and owns the
verify/iterate loop; use it whenever the creator is in the loop. Mechanics, prompt template,
and model details live in **`references/thumbnail-generation.md`** — load it before
generating. The flow:

1. **Build a prompt per concept** from its Stage 3 fields using the template in the reference doc.
   Nano Banana Pro **renders the hook word itself** (deliberate), so state the exact word, spell it
   letter-by-letter, and forbid all other text.
2. **Generate** into `videos/<project>/packaging/thumbs/A|B|C.png` with `tools/gen_thumbnail.py`,
   passing the `media/library/faces/` kit as reference so the face stays consistent. (You supply that
   kit — see its README. No face kit, no face renders.)
3. **Verify every render before showing it** — run the verify checklist in the reference doc (text
   spelled right + legible, face reads as the creator, one dominant hook, bright/saturated/positive,
   sane hands, 16:9 <2MB). Regenerate any that fail; only surface passes. This catches the one real
   risk of model-rendered text: a garbled word.
4. **Iterate** — review A/B/C together; change one thing at a time, holding `--seed` to keep
   composition steady. Keep each prompt in `thumbs/A.txt` so refinements are diffs.
5. **Deliver** the 3 finals to YouTube spec (`--jpg`, ≤2MB) plus prompts/seeds, so any winner is
   re-renderable later.

Remember the **loud-vs-calm rule**: the thumbnail is intentionally louder than the calm in-video
brand (`brand.md`) — never tone it down to match. See the reference doc.

---

## Title Checklist

A strong title passes most of these. Use as a generator *and* a filter.

1. **Concrete promise** — quantified ($ / count) or absolute (Unlimited / 100% / Free)? Vague = dead.
2. **At least one magnet word** — Free, Unlimited, 100%, Money, Easiest.
3. **Outcome-framed**, not feature-framed — the viewer's *gain*, not what the tool *does*. Selling a
   tool's capability instead of the viewer's outcome is a reliable floor.
4. **Zero unknown / own-product names** — see the self-brand rule below.
5. **Barrier-drop or authenticity rider** where the topic invites skepticism — "for beginners," "no
   coding," "without [skill]," "(No BS)."
6. **News / "Now / New" hook** if something genuinely changed — borrows the discovery wave.
7. **A specific noun**, not vague curiosity — "the one skill," never "WAY more" / "you won't believe."
8. **No hot-take / "DEAD" / negative framing** — make/save/build outperforms opinions. (Test this
   against your own data; it's one of the most channel-dependent rules here.)
9. **Leads with the takeaway, not the mechanism.**

## Thumbnail Checklist

Ranked by signal strength. Re-rank against your own data once calibrated.

1. **One dominant hook — never a busy frame.** One magnet word OR one big number as the focal
   element. This is the top-tier device. The multi-logo "kill the competitors" graveyard splits
   attention and reliably lands only mid-tier — even when the enemy-kill works in the *title*, render
   the *thumbnail* as one clean hook.
2. **Lead with a number/$ when the topic has one** — huge, bright. Strong but not sufficient: a
   number in a busy frame on a narrow topic still sinks.
3. **Big, high-energy *positive* face. Kill negative emotion.** Wide-eyed / excited / shocked,
   looking at camera, large in frame. Facepalms and flat smiles are the floor.
4. **Bright saturated color pop** — green (money), yellow (highlight), red (FREE). Dark and muted
   frames underperform.
5. **Tangible object in hand for curiosity**, especially a value contrast (a small price pointing at
   something that looks expensive, or vice versa).
6. **No DEAD / negative framing visually** — mirrors title rule 8.
7. **Thumbnail text ≠ title** — a 1–3 word fragment that *combines* with the title, never repeats it.
   Title and thumbnail are two halves of one message.

## Hard rules

- **Long-form only.** If asked to package a Short, decline and note this skill is long-form; Shorts
  are a different packaging game.
- **One title, three thumbnails.** Test & Compare is thumbnail-only. Never ship "3 title+thumbnail
  pairs" — the test can't measure that.
- **Clear takeaway over withheld drama — always.** Curiosity is allowed *only* when anchored to a
  named, valuable thing ("the one skill you need"), never pure mystery.
- **The self-brand rule:** unknown / own-product names stay OUT of titles. They don't kill clicks —
  they kill *reach*, because an unknown name rides no discovery wave, so YouTube serves it less.
  Known brands help and are fine. Own products belong in the thumbnail and the video, never the title.
- **No hot-take / "DEAD" / negative framing.**
- **3 distinct bets, never 3 flavors of one frame.**
- **Never quote a CTR target the creator hasn't measured.** Their median or nothing.
- **The creator's data beats this file.** When `references/channel-calibration.md` has real numbers
  that contradict a rule here, the rule is wrong for that channel. Update it.

## References

- `references/channel-calibration.md` — how to pull your own CTR from Studio (it is **not** in the
  API), build the dataset, derive your baseline and your real levers, and reconcile them back into
  this file. Run it once you have ~10+ long-form videos.
- `references/thumbnail-generation.md` — Stage 5 render engine: the Nano Banana Pro model/tool
  (`tools/gen_thumbnail.py`), the `media/library/faces/` reference kit, the prompt template, the
  per-render verify loop, the loud-vs-calm brand rule, and failure-mode fixes. Load before rendering.
