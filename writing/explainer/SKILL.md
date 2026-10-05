---
name: explainer
description: Requires OFOX_API_KEY — create one at https://app.ofox.ai. Turn an article, doc or release note into a short explainer clip — one person to camera, or a voiceover over illustrative footage. The user supplies the source text and the model generates the speech; audio cannot be uploaded, measured. A 30-second clip holds about eighty spoken words in eight sentences — measured, and well under a tenth of a 1,200-word post — so this skill does not summarise an article, it picks the single idea worth saying and helps choose which one. Use when a user asks to turn writing into a short spoken video, e.g. "make a 30-second explainer from this blog post", "explain this feature in a short video", "turn our changelog into a clip", "a quick video explaining what this paper found". Do not use for a scene between people (see seedance-short-drama), a brand or product ad (see seedance-ad-creative), a handheld creator clip (see ugc-ads), or when the user already has both a portrait and the finished words (see talking-head). Budget sentences as well as words — each sentence boundary costs about 0.7 seconds of silence, so a script with more sentences runs longer at the same word count.
license: MIT
version: "2.0.0"
homepage: https://github.com/ofoxai/skills/tree/main/skills/explainer
metadata:
  author: ofoxai
  version: "2.0.0"
  openclaw:
    requires:
      env: [OFOX_API_KEY]
      bins: [curl, jq]
    primaryEnv: OFOX_API_KEY
    envVars:
      - name: OFOX_API_KEY
        required: true
        description: Ofox API key. Create one at https://app.ofox.ai (Settings -> API Keys). The same key works across every Ofox skill.
    emoji: "💡"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/explainer
---

# explainer: one idea from the writing, said once

Takes something written — an article, a README, a release note, a paper — and
produces a short clip of it being said out loud. The user supplies the source;
this skill picks the one idea that fits, writes it as spoken words, and sends
it to be generated.

This skill is a thin, scenario-specific layer over
[`ofox-video-core`](../ofox-video-core/SKILL.md). It owns the idea selection,
the explainer prompt craft, the brief, the defaults and the pre-generation
cost estimate; `ofox-video-core` owns talking to the Ofox API correctly and
safely (the `OFOX_API_KEY` handling, the no-resubmit rule, error-code mapping,
download/verification, and reporting the downloaded file's absolute
`VIDEO_PATH`). **Read that skill's safety contract before using this one** —
it is not restated here.

Shared prose is linked rather than copied: the prompt formula, camera and
delivery vocabulary, the word-rate tiers and the negative-list items are in
[`../ofox-video-core/references/prompt-structure.md`](../ofox-video-core/references/prompt-structure.md);
the pre-prompt question rules in
[`../ofox-video-core/references/creative-brief.md`](../ofox-video-core/references/creative-brief.md);
the spend rule in
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md).

## The request this skill almost always receives is not the one it can fill

People ask for "a 30-second video of this article". The arithmetic says no,
and it says no by a wide enough margin that the honest move is to say it in
the first reply rather than after the bill.

### Sentences cost seconds too — the budget is not words per second alone

🚨 **This section used to be headed "a thirty-second clip holds about ninety
spoken words". A 30-second run disproved it.** The old number came from
multiplying a 20-second clip's rate by 30, and the thing that multiplication
misses is that **every sentence boundary costs about 0.7 seconds of silence**.
A script with more sentences takes longer at the same word count.

The two word-rate tiers and the gallery cases behind them live in the shared
file —
[`prompt-structure.md`](../ofox-video-core/references/prompt-structure.md) →
"Dialogue and sound" → "Density — two tiers, not one" — and are not restated
here; what this skill has measured on this API is below. **The tier that
applies to an explainer is monologue / talking head** — one person speaking
continuously. The other tier, dialogue drama at 0.4–1.7 words/s, measures a
different shape: two people, with silence between their lines. It is a *floor*
here rather than a budget.

**The budget formula, from the 30-second run:**

```
speech span (seconds) ≈ words / 3.56 + 0.7 x (sentences − 1)
```

3.56 words a second is the measured rate **while actually speaking**; the
second term is the pauses between sentences. Checked against its own run: 80
words in 8 sentences predicts 27.4s, and the delivered speech span was
**28.13s**. Then leave room at both ends — that clip started speaking at
0.567s and finished 1.39s before the last frame.

| Clip | A safe script | Which is | Share of a 1,200-word article |
|---|---|---|---|
| 10s | ~25 words, 2–3 sentences | one thought | 2% |
| 15s | ~40 words, 3–4 sentences | a short paragraph | 3.3% |
| 20s | ~55 words, 5 sentences | a paragraph | 4.6% |
| 30s | **~80 words, 8 sentences** — **measured, fits with 1.39s to spare** | a claim, its reason, and what to do about it | 6.7% |

Only the 30-second row is measured. The others apply the same formula with
the same headroom and have not been run.

**Ninety words in thirty seconds does not fit.** By the formula, 90 words
across 8 sentences needs `90/3.56 + 4.9 = 30.2s` of speech span — longer than
the clip, before any opening or closing beat. The failure mode is the
expensive one: overrunning comes back rushed, garbled or cut off, which costs
the whole clip, while under-filling costs a pause at the end. Round down.

**Count the sentences, not just the words.** Two 80-word scripts can differ by
several seconds — short punchy sentences are *slower* on this model than the
same words in fewer, longer ones. That is the opposite of how most people
estimate, and it is the practical half of this section: a script that fails
the budget can often be fixed by **joining sentences** rather than cutting
words.

**What kind of evidence this is.** Both tiers started as counts of *gallery
prompt text* against clip length: real prompts and published clips, but
unrecorded platforms and parameters, and no measurement of what this API
delivers. That is still what the **3.5 / 5 ceiling** is, and the CJK figures
are still exactly that and nothing more. The English budget is now this
model's own, measured twice:

| Run | Script | Speech span | Overall rate | Rate while speaking |
|---|---|---|---|---|
| `edef379e` (20s) | 59 words | 19.33s | **3.05 w/s** | not separated |
| `42d8b5c3` (30s) | 80 words, 8 sentences | 28.13s | **2.84 w/s** | **3.56 w/s** |

**The two overall rates differ, and the second run explains why.** Splitting
speech from silence showed 22.49 seconds of actual speaking and 5.64 seconds
of internal silence — **7 pauses, matching the script's 7 sentence boundaries
exactly**, about 0.7s each. So the overall rate is not a property of the
model; it falls out of how many sentences the script has. A denser-sentence
script scores a lower "words per second" while speaking at the same speed.

That is why the budget above is a formula rather than a rate, and why the old
90-word row could not survive: it multiplied a 20-second observation by 1.5
and carried no term for the pauses.

**Until that run this was an extrapolation across tiers, and that is a mistake
this repo has already made once.** Every word rate measured here before today
came from *two-person dialogue*, and handing the dialogue band to a continuous
speaker is a category error rather than a conservative estimate — the dialogue
tier's low floor is not somebody talking slowly, it is words spread across a
clip where most seconds have nobody speaking at all. `talking-head` shipped
that error and had to correct it. The monologue tier now has measurements of
its own instead.

**A third observation, on another model, and that is still not a law.**
`talking-head`'s first paid run measured **3.16 words a second** overall on
`alibaba/wan-3.0-prime` (2026-09-16). It is close to this skill's two, which
is the reassuring direction — but its speech and silence were never separated,
so it cannot be compared against the 3.56 figure, and the sentence-boundary
term has been measured on **one** run only. Nothing has been measured in
another language or at another resolution. Two data points on one model,
agreeing about *why* they differ, is exactly as much as this file claims.

⚠️ **Thirty seconds is now measured; the rest of the table is not.** The
30-second row comes from a real 30-second clip. The 10, 15 and 20-second rows
apply the same formula with the same headroom and have not been run at those
lengths — the closest evidence is the 20-second clip, whose script was written
against the older, looser budget and still fitted.

### So the product is one idea, said once

Eighty words is not a summary of a 1,200-word article — it is well under a
tenth of it. It is a claim, its consequence, and one concrete detail. That is
not a degraded explainer — it is what a short explainer has always been — but
it has to be said out loud before a user pays for something they thought was a
summary:

> A 30-second clip holds about **eighty spoken words** — roughly one paragraph
> and under a tenth of your article, and that is measured rather than
> estimated. It will not summarise the piece. What it can do well is land
> **one** idea from it — so the useful question is which idea, and the next
> section is how to pick.

**Never quietly compress the article into eighty words instead.** A summary
squeezed to that length becomes a string of abstractions that means nothing to
someone who has not read the source — the worst of both products. One concrete
idea, fully said, beats five ideas gestured at.

If the user genuinely needs the whole article covered, the honest answers are:
a series of clips (priced below, and it has a real continuity problem), a
narrated slide deck, or written text. Say which you think fits before quoting.

## Picking the idea

This is the work. Everything after it is mechanics.

### The procedure

1. **Read the source and list its candidate ideas** — usually three to five.
   A candidate is a claim, not a section heading: "the migration is automatic"
   is a candidate; "Migration" is not.
2. **Write each one as the sentence that would actually be spoken.** Not a
   label, the words. This is the step that kills most candidates: an idea that
   cannot be said in one or two plain sentences will not survive the clip
   either.
3. **Score each against four tests**, all four of which have to pass:

   | Test | Fails when |
   |---|---|
   | **Stands alone** — does it make sense to someone who has not read the article? | It depends on a definition, a number, or a previous paragraph |
   | **Concrete** — is there a specific thing, number or action in it? | It is a category ("improved performance", "better developer experience") |
   | **Fits the budget** — does the spoken form come in under the clip's word count? | It needs a subordinate clause to be true |
   | **Worth 30 seconds of someone's attention** — is it the thing the reader should remember or do? | It is true and nobody's decision changes because of it |

4. **Offer the two or three survivors to the user, as the actual sentences**,
   and let them choose. This is a must-ask axis — it is their article, and no
   model can tell which idea they meant. If they say "you pick", pick the most
   concrete one, name it in the recap, and let the approval gate be the check.

### Where the good candidate usually is

Not in the introduction. In practice the sentence worth saying is:

- the **one number** in the piece that changes a decision;
- the **thing that is now true that was not true before** — a release note's
  actual change, a paper's actual finding;
- the **counter-intuitive** line, the one a reader would not have guessed;
- the **action** the article is asking for.

A title is usually a bad candidate: it was written to be clicked, so it is
vague on purpose, and vague is what one paragraph of speech cannot afford.

### Worked selection — a 1,100-word release post

Source: a post announcing a database client release. Candidates, each written
as it would be spoken, with the verdict:

| Candidate | Spoken form | Verdict |
|---|---|---|
| The release is out | "Version 4 of the client is out today, with a lot of improvements." | **Fails** concrete and worth-it. Nobody's decision changes |
| Connection pooling was rewritten | "We rewrote connection pooling on top of a new scheduler with backpressure." | **Fails** stands-alone. Means nothing without the article |
| Reconnects no longer drop queries | "Version 4 stops dropping queries when the connection blips. If you wrapped every query in a retry, you can delete that now." — 22 words | **Passes all four.** Concrete, a reader acts on it |
| Old versions stop getting fixes in March | "Version 2 stops getting security fixes in March, so upgrading is now a date rather than a preference." — 18 words | **Passes all four.** A number, a decision |

Two survivors go to the user. The recap names which one they picked and says
the clip carries that one and not the post.

## Before anyone pays: what is measured here, and what is not

**This skill has two paid runs of its own, and the second one overturned the
number the whole file used to be built on.** Both `bytedance/seedance-2.5` on
`byteplus`, 480p, text-to-video with nothing attached, `--generate-audio` left
at the server default so the speech came back on the track, and both read
afterwards — audio measured and transcribed, frames extracted — rather than
called done at `STATUS completed`.

| Run | Shape | Cost |
|---|---|---|
| `edef379e-9ac0-41c9-ab59-6378d030239e` (2026-09-16), seed `623333235` | **20s**, presenter-to-camera, 59 words | $2.20 |
| `42d8b5c3-31f4-41d2-90eb-b07a3181b465` (2026-09-17), seed `1021654967` | **30s**, 16:9, the **Voiceover** template, 80 words in 8 sentences | $3.30 |

### The first run — 2026-09-16

| Question | Measured | How |
|---|---|---|
| **Speech rate** | **3.05 words a second** overall | 59 words across a 19.33s speech span. `silencedetect` at -30dB puts the first word at 0.399s and the last at 19.729s, with 7 internal pauses |
| **Truncation** | **None** | A `whisper tiny.en` transcription returns all 59 words, in order, with nothing added or dropped |
| **The closing beat** | **It fitted** | 0.335s of silence between the last word and the last frame. The template asks for that beat and the clip had room for it — under-filling by a hair is what bought it |
| **Whether a 30-second clip behaves the same** | ❌ **It does not** | This row used to say "not measured" and carried the 90-word extrapolation. See the second run |

⚠️ **One measurement here was nearly reported backwards, which is worth
knowing before repeating it.** A first pass with `silencedetect` at a 0.35s
minimum found no trailing silence, and the tempting reading was "a script at 3
words a second squeezes the closing beat out". Wrong: the beat is plainly
there in the frames — mouth closed, expression held — and the pause is 0.335s,
sitting just under the threshold that was looking for it. A tool not reporting
something is not the thing not happening. Check that the threshold can see the
size of the thing you are asking about before concluding from its silence.

**What that run does not establish:** one run, one script, English, 480p, 20
seconds, presenter-to-camera. A faster or slower script, another language and
another resolution are all still unmeasured here.

### The second run — 2026-09-17, and it cost this file its headline number

Job `42d8b5c3`, **30 seconds**, the **Voiceover** template (no visible
speaker), 80 words in 8 sentences, $3.30. It closed this skill's two largest
gaps at once: the duration it is named for, and the shape it had never
generated.

| Question | Measured | How |
|---|---|---|
| 🚨 **Does "about ninety words" hold at 30 seconds?** | ❌ **No** | Speech span 0.567s → 28.695s = **28.13s** for 80 words. Split into speech and silence: **22.49s speaking, 5.64s of internal silence in 7 pauses — exactly the script's 7 sentence boundaries**, about 0.7s each. Speaking rate **3.56 w/s**; overall **2.84 w/s**. By that model 90 words in 8 sentences needs 30.2s of span, which does not fit in a 30s clip |
| **The budget formula** | `span ≈ words/3.56 + 0.7 x (sentences − 1)` | Predicts 27.4s for this script; delivered 28.13s |
| **Truncation** | **None** | 1.39s of tail left over. The script fitted with room |
| **The voiceover shape itself** | ✅ **It works** | No person anywhere in 30 seconds; a slow continuous push with no cut; **no on-screen text at all**; and the ending holds — the frames at 22s and 29.5s are nearly identical, on a recessed button, exactly as the template asks |
| **Whether the 20s and 30s rates conflict** | **They don't** | 3.05 and 2.84 are the *overall* rates of scripts with different sentence densities. The underlying speaking rate is the thing that is stable, and only the 30s run separated it |

**What this run does not establish:** one run, one script, English, 480p, 30
seconds, voiceover. The 0.7s sentence-boundary cost is measured **once**, on
one script's 7 boundaries — it is the most load-bearing number in this file
and the least replicated. A faster or slower script, another language, another
resolution, and any duration past 30 seconds remain unmeasured.

The rest of what this file rests on:

| Claim | Strength |
|---|---|
| The English budget formula — **3.56 words a second while speaking, plus ~0.7s per sentence boundary** | **Measured** on this model, once, at 30 seconds (`42d8b5c3`). The 20-second run agrees on the overall figure it can supply (3.05 w/s across a script with 7 pauses of its own) but never separated speech from silence, so it corroborates rather than replicates. `talking-head`'s 3.16 w/s on `alibaba/wan-3.0-prime` is a third overall rate on a different model, also unseparated |
| A supplied audio track does not become the clip's audio | **Measured**, job `d8561509-dcc6-4f2c-8864-a193cd239b14`, 55 cents, 2026-09-15 — the input was near-continuous speech, the delivered track was sparse, correlation 0.41. The model generates its own voice |
| The model renders a photoreal person speaking, from text alone | **Measured**, six `bytedance/seedance-2.5` text-to-video jobs of 20–30 seconds built entirely around photoreal people, all completed, five of them carrying spoken lines. On five of the six only the picture and the timing were checked; the sixth is this file's own run above, where the audio was transcribed against the script |
| A photoreal person in an *attached* image is refused at submission on `bytedance/seedance-2.5` | **Measured** 2026-08-30, `input_moderation_failed`, nothing billed. It decides the continuity limits below |
| Asking this model for music can fail output moderation on copyright | **Measured** once, unbilled |
| Text rendered from a description comes back invented or garbled; text approved on a still and attached as a frame is preserved | **Measured**, several jobs. It decides the on-screen-text section below |
| The **ceiling** the budget sits under — the monologue tier at 3.5 words/s English and 5 characters/s Chinese — and the CJK budget of 4 characters/s | **Gallery practice** — prompt text counted against clip length across a public corpus, not Ofox runs. It is a Seedance 2.5 collection and this skill's default is Seedance 2.5, so the model at least matches; but for the community entries the platform that produced the clip is unrecorded. **Nothing here has been run in Chinese or Japanese**, so the character-per-second rows are exactly as strong as they were |
| A voiceover with no visible speaker | **Measured**, job `42d8b5c3` (2026-09-17, 30s, $3.30): no person in any frame, a slow continuous push with no cut, no on-screen text, and the ending held on its final subject. One run, English, 480p, 16:9. It was "gallery practice only, never run here" until then |

Practical consequence: **both shapes this skill offers have now been run**, and
both at the durations the file leads with. What is risky about a first clip
now is the **script**, not the format — specifically its sentence count, which
the old budget ignored entirely and which costs about 0.7 seconds a boundary.
A non-English script and any duration past 30 seconds are still unmeasured.
Draft short and cheap, read the frames, listen once, then price the
deliverable.

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

**That `../` is relative to this skill's own directory**, which is also where
the probe has to run. From anywhere else nothing resolves — use the absolute
path the probe printed (candidates 3–5 are absolute already), or, in a clone
of this repo, `skills/ofox-video-core/references/ofox-video.sh` from the repo
root.

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
an `OFOX_API_KEY` at `https://app.ofox.ai`) — don't dead-end the conversation,
and don't re-run this check on every subsequent request once it has passed.

`check` reports whether the key is **present**, not whether it is valid, and
makes no network call. A failing `check` is not a stop sign: the idea
selection, the script and the price can all be settled without a key — see
"Pricing a job with no API key".

## Two shapes, and what each costs you

| | **Presenter to camera** (recommended) | **Voiceover over footage** |
|---|---|---|
| What is on screen | one person, chest-up, speaking | the thing being explained; the speaker is never seen |
| Evidence | six completed Ofox jobs built around photoreal people, text-to-video — one of them this skill's own 20s run, whose speech was transcribed against the script | **one paid run**, job `42d8b5c3` (2026-09-17, 30s, $3.30): no person in any frame, a slow continuous push with no cut, no invented lettering, and the ending held on its final subject |
| Best for | an opinion, an announcement, anything whose credibility comes from a person saying it | a product, an interface, a process, a physical object |
| Watch out for | the presenter is generated fresh every job and cannot be reused | a voice with nothing on screen to anchor it reads as stock footage with narration. Whether the model produces a disembodied narrator **is no longer the open question** — it did, for 30 seconds, once. Whether it does so reliably is |
| A real presenter's photo | **not this skill** — that is `talking-head`, and it needs a different model | — |

Default to presenter-to-camera unless the subject is visual. When the subject
is an interface or a physical object, say what the voiceover shape costs in
certainty before choosing it.

## Before writing the prompt: the brief

The shared rules — the three tiers, one round of at most four questions, the
shape of a question, the "Let the AI decide" discipline, the order with the
approval gate, the fallback without `AskUserQuestion` — are in
[`../ofox-video-core/references/creative-brief.md`](../ofox-video-core/references/creative-brief.md).
This section adds only this scenario's question set.

| Tier | Explainer axes |
|---|---|
| **must-ask** | which idea from the source the clip carries; whether the source is really there (a link nobody can open is not a source) |
| **ask-if-open** | presenter or voiceover, aspect ratio, register |
| **never-ask** | resolution, model, provider, audio on/off, the spoken language (it follows the source), duration once the word count has fixed it |

### The question set

| # | Tier | `header` | Question | Options — first is recommended; "Let the AI decide" comes last where it appears, and never on a must-ask row | Ask when |
|---|---|---|---|---|---|
| 1 | must-ask | `Idea` | A clip this long holds about `<N>` spoken words in about `<S>` sentences, so it carries one idea rather than the article. Which one? (get `<N>` and `<S>` from the budget formula, not from memory — sentences cost about 0.7s each) | The two or three survivors of "Picking the idea", each shown **as the sentence that would be spoken**, with its word count; recommended = the most concrete. **No "Let the AI decide"** — it is their article. If they answer "you pick" in free text, take the most concrete, name it in the recap, and let the gate be the check | Always, unless the user already gave one sentence and asked for exactly that |
| 2 | ask-if-open | `Shape` | Who is on screen? | `A presenter, to camera (recommended)` — the shape this repo has actually run / `Voiceover over footage of the thing` — no speaker visible; better for an interface or an object, and untested here / `Let the AI decide` | The subject could go either way and the request doesn't say |
| 3 | ask-if-open | `Aspect` | Where will it be watched? | `9:16 vertical (recommended)` — feeds / `16:9 landscape` — docs, a site, YouTube / `1:1` / `Let the AI decide` | No platform word and no ratio in the input |
| 4 | ask-if-open | `Register` | How should it sound? | `Plain and direct (recommended)` — a colleague telling you something useful / `Warm and enthusiastic` — a launch / `Careful and precise` — research, security, anything where overclaiming is the failure / `Let the AI decide` | The source's own register is ambiguous and the user gave no direction |

If more than four are open, ask in this order: `Idea`, `Shape`, `Aspect`,
`Register`. Duration is not a question — it falls out of the chosen idea's word
count; it is a line in the recap and a row in the cost table.

### Skip rows specific to this scenario

On top of the generic rows in `creative-brief.md`:

| Input says… | Axis | Value |
|---|---|---|
| the language the source is written in | spoken language | that language, **never asked** — unless the user asks for a translation, which is then their words to approve |
| the user quotes one sentence and says "this, as a video" | Idea | settled; do not re-open it |
| "explain the new export feature" on a doc covering six features | Idea | narrow to that feature, then still pick one idea *within* it |
| "for LinkedIn", "for the docs site", "for the README" | Aspect | 16:9 |
| "for TikTok", "Reels", "Shorts" | Aspect | 9:16 |
| "show the app while I explain" | Shape | voiceover over footage — **measured 2026-09-17** at 30s (job `42d8b5c3`): no person, no cut, no invented lettering, and the ending held. One run, so still price a first one as a draft |
| "use my photo", "have me say it" | — | that is `talking-head` |
| "put the bullet points on screen" | — | not available from a description; see "On-screen text" |

### Every answer lands somewhere

| Answer | Where it goes |
|---|---|
| Idea | the quoted `LINE`, and the word count that sets `--duration` |
| Shape | whether the prompt has a `SPEAKER` block or a `SUBJECT` block, and whether the voice is on camera or over |
| Aspect | `--aspect-ratio` |
| Register | the `DELIVERY` note and the micro-beats |

### The recap for this scenario

```
Brief
- Source: the v4 release post you pasted (1,100 words)
- Idea: "Version 4 stops dropping queries when the connection blips. If you wrapped
  every query in a retry, you can delete that now." — 22 words (you chose it from two)
- What this clip is NOT: a summary of the post. 9 seconds holds roughly 22 words
  in 2 sentences, so it carries this one idea and nothing else
- Shape: a presenter to camera (AI's pick)
- Duration: 9s — 22 words in 2 sentences is 22/3.56 + 0.7 = about 6.9s of speech,
  leaving room to open and to close
- Register: plain and direct (AI's pick)
- 9:16, 480p draft, audio on
- Note: the budget is measured on this model at 30 seconds (job `42d8b5c3`) — each
  sentence boundary costs about 0.7s, so a script with more sentences runs longer
  at the same word count. The delivery is still a roll, so treat the draft as the
  take you listen to
```

Then the full prompt, then the cost table `approval-gate.md` specifies, all in
one message.

## On-screen text — the thing users ask for that this cannot do

An explainer wants a title, three bullets and a logo. This API does not
deliver them, and the reason is measured rather than stylistic: **text
rendered from a description comes back invented or garbled**, repeatedly,
across several jobs in this repo — while **text approved on a still image and
then attached as a frame is preserved**, which is a different task.

So:

- **Do not promise words on screen.** Put the text items in `AVOID`
  (subtitles, captions, on-screen text, watermarks, logos) and keep lettered
  surfaces out of the set — the shared file's "Unwanted text is designed out
  of the set, not forbidden in the list" has the measurement, including that a
  negative list alone fails on a set full of signage.
- **Captions and lower thirds go on in an editor afterwards**, where they are
  free, correct and editable. This is worth saying early: it is usually good
  news.
- **One route does exist and it costs the frame slot**: prepare a title card
  as an image, read it at full size, and attach it with
  `--frame-first-image`. The clip then opens on exactly that card. Attaching a
  frame makes the output follow the image's shape (the script prints a
  `NOTE:` about `adaptive`), so crop the card to the delivery ratio first —
  crop, never pad. `ofox-image-core`'s `--target-aspect W:H` does that and
  measures the real file.

## Continuity across clips — the limit to state before a series is planned

If the user wants a three-part explainer with the same presenter, say this
first: **a photoreal presenter does not survive between jobs.**

- Each `generate` is stateless; a person described in text is generated fresh
  every time.
- The usual fix — carry the previous clip's last frame into the next — is
  **refused at submission** on `bytedance/seedance-2.5` when that frame holds
  a photoreal person (`input_moderation_failed`, measured, nothing billed).
- The words route (re-describing the previous frame in the prompt) brings back
  staging, wardrobe and props; it does **not** bring back a face.

What that leaves:

| Want | Available |
|---|---|
| Three clips, same real person | not this skill. A portrait re-attached to each job is `talking-head`'s route, and its own continuity is unmeasured |
| Three clips, same *illustrated* presenter | `seedance-anime-drama` — a non-photoreal character frame is accepted, which is exactly why that skill works |
| Three clips, no presenter | voiceover shape, with a consistent `SCENE` and `STYLE` block repeated word for word. Palette and setting carry; nothing else is guaranteed |
| Three clips, three different presenters | fine, and often the right answer — three ideas, three people, cut together |

Each part is a separately billed job, and the cost table gets a row per part
plus a total, per `approval-gate.md` → "Batches get an itemised table, not one
total". Splitting is not a discount.

## The prompt template

Vocabulary is not repeated here — delivery notes, camera and focus terms and
the negative-list rows are in
[`../ofox-video-core/references/prompt-structure.md`](../ofox-video-core/references/prompt-structure.md).
An explainer is a single shot with performance beats inside it, so the shared
file's "Short prompts (10 seconds or less)" shape applies even above 10
seconds: **no shot manifest, no cut list.**

Slots in `<angle brackets>`; optional lines in `[square brackets]`.

### Presenter to camera

```
One continuous shot, <T> seconds, fixed camera, no cuts.
SPEAKER: <age range, build, hair, top with colour and material>, <one bearing word — relaxed, precise>. <No name; this person exists for one clip.>
SCENE: <a plain setting that does not compete: a home study, a quiet office, a plain wall>. <One light source and its direction.> <Nothing in the background carrying letters.>
FRAMING: chest-up medium close-up, <fixed camera | a faint breathing handheld>, background softly out of focus; real mirrorless texture, slight sensor noise, real skin texture, no smoothing.

<Speaker> faces the camera and says, <delivery: plain and direct, unhurried | warm | careful and precise>: "<the chosen idea, verbatim, in the language to be spoken>"
0–<a>s: <eye contact, one natural blink>. <a>–<b>s: on "<the key word>", <one gesture>. <b>–<c>s: <stillness>. <c>–<T>s: after "<last word>", <the ending: lips close, half-second pause, the smallest nod>.

SOUND: <room tone>, no music. Speech in <language>, mouth shape matched to it.
CONSISTENCY: face, hair, <clothing items>, background and light direction identical from the first frame to the last.
AVOID: subtitles, captions, on-screen text, watermarks, logos, diagrams, charts; a second person, a cutaway, an interview setup; music, score, soundtrack, instrumental, humming, singing; presenter cadence, theatrical over-acting, wild gesturing; skin smoothing, beauty filter, plastic skin, CGI look; camera movement, zooms, cuts.
```

### Voiceover over footage

```
One continuous shot, <T> seconds, <slow push | slow drift>, no cuts. No person on screen at any point.
SUBJECT: <what is being explained, described the way a camera sees it: a laptop on a desk with a dashboard open, a hand-held device on a bench, a machine in a workshop>.
SCENE: <where it sits, one light source and its direction>. <Nothing in frame carrying letters.>

A single voice, off-screen, says, <delivery>: "<the chosen idea, verbatim, in the language to be spoken>" — no speaker is ever visible.
0–<a>s: <what the camera is looking at>. <a>–<b>s: <what changes, tied to the words being said>. <b>–<T>s: <the close>.

SOUND: <room tone>, <one or two sounds tied to what is visible>, no music. Narration in <language>.
AVOID: subtitles, captions, on-screen text, watermarks, logos; a presenter, a face, hands entering frame, an interview setup; music, score, soundtrack, instrumental, humming, singing; cuts, zooms, whip pans; CGI look, plastic surfaces.
```

Five notes on both shapes:

- **The idea is quoted verbatim and never paraphrased.** Put the full spoken
  sentence inside the prompt shown at the approval gate, so the user reads
  exactly what will be said. A line silently rewritten is the most expensive
  thing that can go wrong here, because it looks fine until the clip plays.
- **The spoken language follows the line's language.** Write the user's own
  language in; translating to match the English examples buys them an
  English-dubbed clip they find out about after paying.
- **No music, ever.** Not taste: a prompt asking this model for a scored cue
  came back `output_moderation_failed` on audio copyright in this repo,
  unbilled. Name the music words in `AVOID` as well as writing `no music` —
  that is the pair of blocks the two clean runs used. A track goes on in an
  editor.
- **No text, per the section above**, and in the voiceover shape that extends
  to the subject: an interface full of legible labels is a set full of
  lettered surfaces, which is exactly where invented lettering shows up. Frame
  it tighter, or attach a real screenshot as the first frame and let the lock
  hold the words.
- **`--generate-audio` stays at the server default (`true`).** The speech is
  the deliverable.

### Worked example — 9 seconds, 22 words, presenter to camera

**This has not been generated as written.** It is the template filled in,
carrying the release-post idea chosen above.

```
One continuous shot, 9 seconds, fixed camera, no cuts.
SPEAKER: a man in his 30s, average build, short dark hair, a plain charcoal crew-neck sweater; relaxed, precise.
SCENE: a quiet home office; a plain pale wall behind him with nothing on it. The only light is a window to the front-left, soft and slightly cool, falling off across the far side of his face.
FRAMING: chest-up medium close-up, fixed camera, background softly out of focus; real mirrorless texture, slight sensor noise, real skin texture, no smoothing.

He faces the camera and says, plain and direct, unhurried: "Version 4 stops dropping queries when the connection blips. If you wrapped every query in a retry, you can delete that now."
0-2s: he looks straight into the lens, one natural blink. 2-5s: on "dropping queries" a single small open-palm beat, low in frame, and the hand leaves again. 5-8s: stillness; the eyebrows lift slightly on "retry". 8-9s: after "now" the lips close, one slow blink, the smallest nod, and the shot holds.

SOUND: quiet room tone, a little distant traffic. No music. Speech in English, mouth shape matched to it.
CONSISTENCY: face, short dark hair, charcoal crew-neck sweater, the pale wall and the light direction identical from the first frame to the last.
AVOID: subtitles, captions, on-screen text, watermarks, logos, diagrams, charts; a second person, a cutaway, an interview setup; music, score, soundtrack, instrumental, humming, singing; presenter cadence, theatrical over-acting, wild gesturing; skin smoothing, beauty filter, plastic skin, CGI look; camera movement, zooms, cuts.
```

The duration was derived from the script rather than the other way round:
22 words at 3.56 a second is 6.2 seconds of speaking, plus one sentence
boundary at 0.7s, giving a 6.9-second span — then room to open and to close,
rounded up to 9. **Note that the sentence count is in that arithmetic.** Break
the same 22 words into four short sentences and the span grows by about 1.4
seconds, which is most of the headroom. If a script is running long, joining
sentences buys back time that cutting words does not.

It is also why a 22-word idea gets a 9-second clip and not a 15-second one
with six seconds of nothing in it: on a per-second bill, the script decides
what you pay for.

## Recommended defaults

| Parameter | Default | Why |
|---|---|---|
| `--model` | the script's own default, `bytedance/seedance-2.5` — **unless the user named one**, which always wins | no portrait is attached here, so nothing forces a different model, and this repo's spoken-dialogue runs are all on it. See "Choosing a model" |
| `--duration` | derived from the chosen idea with `words/3.56 + 0.7 x (sentences − 1)`, plus room to open and close, then clamped to the model's range — which `ofox-video.sh models` prints. For Chinese or Japanese the only figure available is still 4 characters a second | the script decides the length; a default that ignores it produces rushed speech. The English formula is **measured on this model** at 30 seconds (job `42d8b5c3`): 3.56 w/s while speaking and ~0.7s at each of the script's 7 sentence boundaries, predicting 27.4s against a delivered 28.13s. ⚠️ **Count sentences as well as words** — that term is what the old "3 words a second" flat rate left out, and it is why "about ninety words in thirty seconds" did not fit. The CJK figure is still gallery-derived and untested |
| `--resolution` | draft at the model's cheapest tier, deliver one tier up | a face at the cheapest tier is where lip and eye detail goes first, so read the draft's frames rather than shipping it |
| `--aspect-ratio` | `9:16` unless the brief or the platform said otherwise; **not passed** if a title card is attached as a frame | short explainers are watched in feeds |
| `--generate-audio` | leave at the server default (`true`) | the speech is the deliverable |
| `--seed` | let the script roll one and keep it | printed as `SEED` and written to the `.json` sidecar. It does **not** reproduce a take — measured, an identical request on a fixed seed came back a visibly different clip — so a re-render is another roll aimed at the same shot. Say that before the user pays for one |
| `--frame-first-image` | unset, unless a prepared title card or screenshot is the opening frame | the only route to correct lettering; it also fixes the clip's shape to the image's |
| `--real-person` | leave unset | nothing in this skill needs it — the presenter is written in text, and text-generated people are not what the refusal is about. `true` is Ofox's privacy-preserving preprocessing path for **authorised** real-person *reference images*, measured lifting seedance-2.5's refusal on 2026-09-16; it is an authorisation route, never a way past the check, and a skill whose presenter comes from a photo is `talking-head`, not this one. See [`api-params.md`](../ofox-video-core/references/api-params.md) → "`--real-person true` lifts that refusal on 2.5" |

## Choosing a model

The model stays **never-ask** — the agent doesn't raise it. But never-ask is
not "never listen": if the user names a model id or a shorthand, use it.

**Model ids, prices, resolutions, durations and aspect ratios are deliberately
not tabulated in this file.** They are catalog facts, they change, and this
repo has recorded defects that trace to a hardcoded copy of somebody else's
value table. Read them live, free, with no API key:

```bash
bash ../ofox-video-core/references/ofox-video.sh models             # every model, its tiers and ranges
bash ../ofox-video-core/references/ofox-video.sh providers MODEL    # that model's per-resolution rates
```

`providers` with no model argument prints the flagship's matrix, not the
catalog — pass the id you actually mean. The rate `models` shows is the one at
each model's **own default resolution**, which differs between models, so it
ranks rather than quotes. The number you put in front of a user comes from
`generate --dry-run` at the parameters you are about to send.

Two things worth saying to a user who is choosing: a cheaper model is a
different look, not just a smaller bill — and it is faces that lose most. And
**moderation policy is per-model**, so a prompt refused on one model can be
accepted on another.

## Before you spend: the approval gate

**Never submit a paid job until the user has seen a cost table and said yes.**
The rule, the required columns and where the numbers must come from are
written down once for every Ofox skill in this repo:
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md).

Get the numbers from `--dry-run`, which validates everything and prints the
estimate **without sending a request**:

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --dry-run \
  --prompt "..." --duration 9 --resolution 480p --aspect-ratio 9:16 \
  --out-dir /absolute/path/to/out
```

Relay the `Estimated cost:` line it prints — never a number of your own — then
wait for a yes, then re-run the identical command with `--dry-run` swapped for
`--approved`. The estimate a *real* run prints comes microseconds before the
request goes out, too late to relay. Pass the same `--out-dir` to both.

`--approved` is where that yes gets typed out. Since `ofox-video-core` 2.0.0
the four billable subcommands — `generate`, `create`, `batch`, `chain` —
refuse to run without it, while `--dry-run` never needs it, so the quote above
is still free and still works with no API key. Be exact about what the flag
does: it records a stance, it cannot prove one. Nothing in a shell script can
observe the conversation you had, and it can be typed without showing anyone a
price. What it changes is that spending without quoting is no longer the
default — it has to be written into the command, where a transcript shows it.
The rule above is still the rule, and it is still yours to follow.

Three things belong in that message beyond the table:

- **the chosen idea, quoted in full**, as the words that will be said;
- **one line saying what the clip is not** — a summary of the source — so the
  expectation is corrected before the money moves, not after;
- **one line saying which parts are measured and which are a first attempt** —
  the word budget is measured on this model at 20 seconds and 480p; the
  voiceover shape, a non-English script and anything longer are not.

This skill has exactly **one cost anchor**, and it anchors one point rather
than a curve: 20 seconds at 480p on `bytedance/seedance-2.5`, text-to-video,
billed **2 dollars 20** (job `edef379e`). Another duration or resolution is a
different number, so the `--dry-run` figure at the parameters you are about to
send is still the only one to put in front of anyone.

Afterwards the **actual** bill is `VIDEO_COST` from the finished job. Report
it as money, not as the raw ten-decimal string.

## Several takes

Delivery is a roll, and this genre is judged on whether the person sounds like
they mean it. `batch` prices the whole set up front, waits concurrently, and
tiles a contact sheet:

```bash
bash ../ofox-video-core/references/ofox-video.sh batch --dry-run \
  --prompt "..." --takes 3 --duration 9 --resolution 480p \
  --aspect-ratio 9:16 --out-dir /absolute/path/to/out
```

Quote `BATCH_COST_TOTAL`, not `BATCH_COST_PER_TAKE`, and give the takes a row
each. Hand over the `CONTACT_SHEET` path on its own line, then the take paths
beneath it. **A contact sheet cannot tell you how a take sounds** — it is
frames. Listen to one before promoting it.

If the user wants several cheap vertical drafts as the deliverable rather than
one clip, [`shorts-reels`](../shorts-reels/SKILL.md) owns that ladder. The two
compose: pick the idea and write the prompt here, run the set there.

## Pricing a job with no API key

`models`, `providers` and `generate --dry-run` all work with `OFOX_API_KEY`
unset. So when a user hasn't signed up yet, **quote the job first and let them
decide whether it's worth registering** — don't open by sending them to a
signup form.

## If the script isn't found

```
bash: ../ofox-video-core/references/ofox-video.sh: No such file or directory
```

Nothing is broken — this skill delegates all execution to `ofox-video-core`
and reaches it by relative path, and that path just missed. Two different
situations wear this message, so run the probe in "Where the core skill lives"
before deciding which:

- **The probe printed a directory** — the core is installed and only the
  directory *name* was wrong, which is the normal LobeHub case
  (`ofoxai-skills-ofox-video-core`). Re-run against what the probe printed.
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

Either way, name the missing skill and where it was expected rather than
relaying the raw path error, which names neither.

A broken link to a shared reference has the same two causes. This skill
degrades gracefully: the selection procedure, the question set, the templates,
the word budget and the defaults are all written out here. What is out of
reach is the detail behind them — the full delivery and camera vocabulary, the
gallery cases behind the word rates, and the exact wording of the spend gate,
which stays mandatory either way.

## Exit codes worth knowing

Full table in [`../ofox-video-core/SKILL.md`](../ofox-video-core/SKILL.md).
The ones that come up:

| Code | Meaning | What to do |
|---|---|---|
| `1` | Parameter rejected locally, no network call, nothing billed | Fix the flag and retry freely |
| `2` | Environment problem — `curl`/`jq` missing, or no `OFOX_API_KEY` | Ask the user to fix it; `check` reports the same |
| `3` | API rejected it, or the job ended failed/cancelled/expired | Read the mapped message; a rejected create was not billed |
| `4` | Timed out waiting — **the job is still running and billable** | `poll JOB_ID`, never re-run `generate` |
| `5` | Ambiguous network failure on create | Do not retry blindly; check https://app.ofox.ai first |
| `6` | `--out-dir` unusable | Fix the path; if it happened after a create, `poll JOB_ID` |

## How long to tell the user it will take

`generate` blocks while it polls, up to `--max-wait` (default 540s). A short
low-resolution clip is usually one to three minutes. Say so before starting,
so the wait isn't silent.

If your tool call can't stay open that long, use `create` (submits and returns
a job id in seconds) followed by `poll`. That way a timeout can never strand a
job whose id you never saw. For `batch`, the worst case is `takes x max-wait`.

## Where the file lands

Always pass `--out-dir`, and **make it an absolute path**. Without it the
script writes to the current working directory — which, given that the
examples here run from this skill's own directory, would drop the user's video
inside an installed skill. Relay the **absolute** `VIDEO_PATH` the script
prints, on its own line.

Pass `--name` too, named after the idea rather than left for the script to
guess from the prompt's opening words, which here describe a shot length. The
clip lands as `<name>-<short job id>.mp4` with a `.json` sidecar holding the
full job id, the prompt, the seed and the real cost.

## Generating

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --approved \
  --prompt "<the explainer prompt built above>" \
  --name "<short idea name, e.g. v4 retry removal>" \
  --duration 9 \
  --resolution 480p \
  --aspect-ratio 9:16 \
  --out-dir /absolute/path/to/out
```

Drop `--aspect-ratio` if a title card or screenshot is attached as the first
frame — the clip then follows the image's shape.

`--approved` is not decoration: without it the script refuses, submits
nothing, and prints the quote-first steps instead. Add it only once the cost
table has actually gone in front of the user and come back with a yes — the
flag cannot check that for you.

This one call validates the parameters, submits the job, polls to completion,
downloads the mp4, and prints `STATUS`, `JOB_ID`, `VIDEO_PATH`,
`VIDEO_SECONDS`, `SEED` and `VIDEO_COST`. Report the **actual** values from
that output — never the estimate, and never a path or cost you didn't see the
script print. Do not re-implement any of the request, poll or download logic
here.

## After it lands: what to actually check

Three things, before calling it done. None of them is `STATUS completed`.

1. **Were all the words said?** Listen once and count against the script.
   Rushed, clipped or dropped endings mean the clip was over budget; the fix
   is a longer clip or fewer words, never a faster delivery. The one run
   measured here lost nothing, but that is one take on one script — delivery
   is a roll, so check it rather than assuming this one.
2. **Is the idea still the idea?** A generated delivery can land emphasis
   somewhere that changes the meaning. Read the source's claim against what
   you just heard.
3. **Did any lettering get invented?** Check a few frames for signage,
   captions or a logo nobody asked for.

Report what you checked, not just that it finished.

## Common failure modes and fixes

| Symptom | Cause | Fix |
|---|---|---|
| The user expected the article summarised and got one idea | The expectation was never corrected | Correct it **before** the cost table, in the recap's "What this clip is NOT" line. After the fact, the only remedy is another job |
| The speech is rushed, garbled, or the last words are missing | More script than the clip holds — usually a summary squeezed to fit. ⚠️ Check the **sentence count** as well as the word count: each boundary costs about 0.7s, so a script that passed a words-only check can still overrun | Fewer words, **or the same words in fewer sentences**, or a longer clip inside the model's range. Never compress the delivery. New prompt, new cost table |
| The clip ends mid-sentence | Same cause, plus no written ending beat | Re-budget with `words/3.56 + 0.7 x (sentences − 1)` **and** write the final beat explicitly. If the word count already looked safe, count the sentences — each boundary costs about 0.7s, and joining two short sentences buys that back without losing content |
| The voice speaks the wrong language | The line was translated on the way into the prompt | Put the source's own words in, untouched. The line's language decides the voice's language |
| Invented captions, a garbled title, a logo nobody asked for | Text rendered from a description is the classic failure, and a negative list alone does not hold on a lettered set | Keep the text items in `AVOID` **and** compose lettered surfaces out of the frame. Real captions go on in an editor; a title card has to be a prepared image attached as the first frame |
| A music bed nobody asked for | `--generate-audio true` and a prompt that didn't exclude music | Keep `no music` in `SOUND` *and* the music words in `AVOID` |
| Exit `3`, `output_moderation_failed` mentioning audio copyright | The prompt asked for music | Rewrite `SOUND` as room tone only and re-run — a new request, safe immediately, nothing was billed |
| Exit `3`, `input_moderation_failed` on create | An attached frame contains a photoreal person — refused at submission on this model, nothing billed | Attach a card, a screenshot or an object instead and write the person in text; or move to `talking-head`, which runs a different model for exactly this reason |
| Part 2's presenter is a different person from part 1's | Every job generates the presenter fresh, and nothing in this skill's route carries a face between jobs — the words route brings back staging, not a face | See "Continuity across clips". Choose one of the four available shapes rather than re-rolling |
| The presenter gestures like a newsreader | No delivery note, or too many gestures written | One gesture per beat at most, and a plain register in the `DELIVERY` note. New prompt, new cost table |
| The voiceover clip has a person in it anyway | A subject description that implies a user | `No person on screen at any point` in the first sentence, and a face and hands in `AVOID`. Untested shape — draft it cheaply |
| Exit `4`, timed out waiting | Still running upstream, not failed | `poll JOB_ID` with the id printed before the timeout; never re-run `generate` |
| Exit `5`, ambiguous network failure on create | No HTTP response at all — can't tell whether a job exists | Don't guess or retry; tell the user to check https://app.ofox.ai |

## When NOT to use

- **The user has a portrait and finished words** — `talking-head`. The split
  is about where the labour is: there the words already exist and a specific
  face has to say them; here the words have to be found in a source and no
  particular face is required. That skill also runs a different model, because
  `bytedance/seedance-2.5` refuses a real person's photo at submission.
- **A scene between people** — `seedance-short-drama`. The boundary is not
  "is there speech", it is *who is being addressed*: characters talking to
  each other is that skill, one voice addressing the viewer is this one. Short
  drama also owns shot lists, cuts and stage direction, none of which belongs
  in an explainer.
- **A brand or product ad** — `seedance-ad-creative`. An explainer that exists
  to sell is an ad, and that skill has the beat structure for it.
- **A handheld creator clip** — `ugc-ads`, even when the creator is
  explaining something. That skill inverts the polish this one defaults to.
- **Several cheap vertical drafts as the deliverable** — `shorts-reels` owns
  that ladder. Write the prompt here, run the set there.
- **The user wants the article summarised.** That is a writing task and it is
  free. Offer it, and let them decide whether a clip is still wanted
  afterwards.
- **Anything needing slides, diagrams, charts or readable bullets.** A
  narrated deck does that properly, costs nothing, and can be corrected. Say
  so before quoting a job that cannot deliver a legible word.
- **A three-minute explainer.** One job is one clip, and a series of them has
  the continuity limit above. Past two or three parts, a screen recording with
  a voiceover is the better product.
