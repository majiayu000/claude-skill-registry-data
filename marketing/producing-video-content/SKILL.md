---
name: producing-video-content
version: "1.1.0"
description: >
  Produces, edits, and repurposes video content for FlashFusion using HeyGen
  (scripted avatar/presenter delivery), Descript (recorded content editing),
  and Invideo (written-to-video with stock footage). Routes based on starting
  material and output intent. Always runs the repurposing cascade after any
  Descript production session.

  Activate when the user mentions: video, record a tutorial, screen recording,
  Descript, Invideo, HeyGen, avatar, origin story, edit this video, make a
  clip, repurpose this, turn this into video, YouTube, LinkedIn video,
  short-form video, video from newsletter, tutorial video, walkthrough, demo
  video, screen capture, make video content, video workflow, clip this,
  captions, transcript, Studio Sound, talking head, presenter, or any request
  to produce, edit, or repurpose video content. Also activates on "I just
  recorded something" or "I have a recording."
---

# Video Content Producer

Routes FlashFusion video work through the right tool with the right workflow.
Three routes, one repurposing cascade, one voice standard.

---

## DEPENDENCY_DECLARATION

| Tool | Status | Required For |
|---|---|---|
| HyperFrames by HeyGen | ✅ Connected | Section 2 (HeyGen Route) only |
| Invideo CUSTOM | ✅ Connected | Section 3 (Invideo Route) only |
| Descript | ✅ Connected | Section 4 (Descript Route) only |

**Per-route FAIL_IF:**

| Route | If tool unavailable | Response |
|---|---|---|
| Section 2 — HeyGen | HyperFrames by HeyGen unreachable | Stop. State: "HeyGen connector is not reachable this session. Switch to Invideo (Section 3) if personal presence is not required, or reconnect via Settings → Connectors → HyperFrames by HeyGen." |
| Section 3 — Invideo | Invideo CUSTOM unreachable | Stop. State: "Invideo connector is not reachable this session. Reconnect via Settings → Connectors → Invideo, or switch to Descript (Section 4) if you have recorded footage." |
| Section 4 — Descript | Descript unreachable | Stop. State: "Descript connector is not reachable this session. Reconnect via Settings → Connectors → Descript." |

> **Availability check:** Verify tool reachability when routing to a section. A failed tool call on first use = treat as unavailable for the remainder of this session.

**Credit / limit warnings:**

- **HeyGen (Section 2):** Credit-based — each rendered video minute consumes credits. Check your HeyGen credit balance before beginning script preparation. If script runtime would exceed available credits, warn before submitting to render.
- **Invideo (Section 3):** Subscription-gated — resolution (1080p) and monthly export volume are capped by plan tier. Confirm plan supports target resolution and that monthly export quota is not exhausted before generating.

---

## Route Detection

| Starting material | Output intent | Route |
|---|---|---|
| Polished script — avatar or presenter delivery matters | Brand-building, origin story, course content, consistent presenter identity | **HeyGen** → Section 2 |
| Newsletter, blog post, written content — stock footage fine | Quick explainer, news recap, social clip | **Invideo** → Section 3 |
| Screen recording, talking-head recording, raw footage | Authentic tutorial, real demo, workshop | **Descript** → Section 4 |
| Nothing yet — need to decide | — | **Brief first** → Section 1 |
| Short clip from existing long video only | — | **Descript clip extraction** → Section 4, Step 5 only |

**The HeyGen vs. Invideo distinction:**
Both start from a script. The difference is what the video looks like and what it communicates.
Invideo produces stock footage with AI narration — good for content that needs information delivered.
HeyGen produces a presenter/avatar — good for content where *who is saying it* is part of the point.
Use HeyGen when personal brand presence matters. Use Invideo when speed and volume matter.

---

## Section 1: Video Brief (run when starting from scratch)

1. **Content type** — pick one:
   - `origin-story` — narrative about Construction over Recovery, FlashFusion backstory → HeyGen
   - `avatar-presenter` — scripted delivery of any content using your avatar → HeyGen
   - `explainer` — concept explanation with stock footage → Invideo
   - `newsletter-recap` — visual summary of a newsletter issue → Invideo
   - `tutorial` — screen recording walkthrough → Descript
   - `case-study` — real client work or project → Descript
   - `linkedin-short` — standalone short-form clip from existing content → Descript clip extraction

2. **Source material** — script written and polished, written but rough, recording exists, nothing

3. **Target platform** — determines aspect ratio:
   - YouTube long-form (16:9, 3–20 min)
   - YouTube Shorts / Reels (9:16, 30–60 sec)
   - LinkedIn (1:1 or 4:5, 60–90 sec recommended)
   - Twitter/X (16:9 or 1:1, under 2:20)

4. **Script status** — HeyGen requires a polished, ready-to-deliver script.
   If not ready: call `drafting-multi-format-content` (type: `video_script`) before continuing.

Once brief is complete, route to the appropriate section.

---

## Section 2: HeyGen Route (script → avatar/presenter video)

> ⚠️ **Before proceeding:** Verify HyperFrames by HeyGen is reachable (see DEPENDENCY_DECLARATION). Check HeyGen credit balance — credits are consumed per rendered video minute. Warn if estimated runtime would exhaust available credits before submitting to render.

Use when the content requires consistent personal presence — origin story,
course modules, brand explainers, anything where a presenter saying it
is meaningfully different from AI narration over stock footage.

### Step 1: Script preparation for HeyGen

HeyGen scripts are different from Invideo scripts. Invideo reads narration.
HeyGen delivers speech. The script needs to sound like someone talking.

**Pacing:** 130–150 words per minute for comfortable avatar delivery.
A 2-minute video = 260–300 words. A 5-minute video = 650–750 words.

**Voice patterns:**
- Contractions throughout: "it's", "I'm", "you'll" — not "it is", "I am"
- First-person, direct address: "Here's what I mean" not "One might consider"
- Short declarative sentences. Long sentences cause avatar pacing issues.
- Pauses written as em dashes or sentence breaks: "I built it. — Not because
  I knew what I was doing. Because I had to."

**Technical term handling:**
HeyGen mispronounces technical terms more than Invideo. Add pronunciation
hints in parentheses for review — do not leave them in the final render.

| Term | How HeyGen may say it | Fix in script |
|---|---|---|
| n8n | "en-ate-en", "ntn" | Write "N-8-N" and verify in preview |
| Supabase | "Soopa-base", "Supa-bay-se" | Preview and adjust if needed |
| Base44 | Usually correct | — |
| FlashFusion | Usually correct | — |
| Anthropic | Usually correct | — |

Always preview a 30-second sample before full render to catch pronunciation issues.

**For the origin story specifically:**
The script should match the Construction over Recovery voice from
`crafting-long-form-memoir` — direct, specific, anti-credential opener,
uncertainty allowed without performance. The avatar delivers the script;
the script has to earn the delivery. "I'm not a trained AI expert. I'm
an L1 service desk tech who built AI systems on the side." That sentence
works. "My journey into AI has been transformative" does not.

### Step 2: Avatar and scene setup

- **Avatar:** use your cloned avatar if available for personal brand content.
  For brand-neutral explainers, stock avatars are fine.
- **Background:** for origin story — contextual (desk, workspace) over
  corporate solid color. For course/explainer — clean, branded background.
- **Outfit/appearance:** check clone consistency against your recent photos
  before production renders.

### Step 3: Generate and preview

1. Paste script into HeyGen scene editor
2. Assign avatar and voice settings
3. **Preview first 30 seconds** before full render — check:
   - Pronunciation of technical terms (see table above)
   - Lip sync accuracy on first few sentences
   - Eye movement naturalness
4. Fix any issues in script or settings before committing to full render
5. Submit full render (5–15 minutes depending on length)

### Step 4: Review rendered video

Watch the full render before downloading. Flag and re-render if:
- [ ] Lip sync drifts after the 1:00 or 2:00 mark
- [ ] Unnatural blinking pattern (too frequent or absent)
- [ ] Technical term mispronounced
- [ ] Audio-visual sync noticeably off

Re-renders cost time, not money — catch issues before distribution.

### Step 5: Captions

HeyGen generates captions automatically. Download as SRT.
Review for technical terms before burning in or uploading to YouTube.
Use the same corrections table as Descript (Section 4, Step 2).

### Step 6: Export

Same platform specs as Descript (Section 4, Step 7).
HeyGen exports as MP4 by default — verify resolution is 1080p before downloading.

---

## Section 3: Invideo Route (written → stock footage video)

> ⚠️ **Before proceeding:** Verify Invideo CUSTOM is reachable (see DEPENDENCY_DECLARATION). Confirm your Invideo plan supports 1080p export and that monthly export quota is not exhausted. Warn if either limit is at risk before generating.

Use when you have a newsletter issue, blog post, or written content that
needs to become video quickly and personal presence is not the point.

### Step 1: Prepare the script

Tighten source material for video pacing:
- 60–90 sec clip: 130–180 words
- 2–3 min explainer: 300–450 words
- Full recap: 400–600 words

Cut everything that doesn't move forward. Short declarative sentences.
Invideo narration sounds better with Kyle's natural writing style — avoid
nested clauses and academic tone.

If scripting from scratch: `drafting-multi-format-content` → type: `video_script`.

### Step 2: Generate in Invideo

1. Paste tightened script
2. Select template:
   - `educational` — tutorials and explainers
   - `news` — newsletter recaps and weekly roundups
   - `social` — short LinkedIn/X clips
3. Review stock footage — replace generic visuals with screen captures,
   product screenshots, or relevant tech imagery
4. Add FlashFusion branding: logo, colors in lower thirds

### Step 3: Captions and audio

- Enable captions — verify AI/tech terms: `n8n`, `Supabase`, `Anthropic`,
  `Claude`, `Base44`, `Descript` are all commonly mistranscribed. Fix manually.
- AI voice: preview for pacing. Slow 5–10% if rushed.

### Step 4: Export

| Platform | Aspect ratio | Max length | Notes |
|---|---|---|---|
| LinkedIn | 1:1 or 4:5 | 10 min (aim for 90 sec) | Square performs better in feed |
| YouTube Shorts | 9:16 | 60 sec | Captions required |
| Twitter/X | 16:9 or 1:1 | 2:20 | Under 60 sec gets autoplay |
| YouTube long-form | 16:9 | — | Min 8 min for mid-roll ads |

---

## Section 4: Descript Route (recorded → polished)

> ⚠️ **Before proceeding:** Verify Descript is reachable (see DEPENDENCY_DECLARATION).

Use when you have a screen recording, talking-head recording, workshop
footage, or any raw video file.

### Step 1: Import or record

- **Import:** drag file into Descript, or connect via Descript MCP
- **Record in Descript:** screen + face cam or screen only
  - Screen recordings: 1080p minimum, full-screen app window
  - Talking head: natural light from front, camera at eye level

### Step 2: Transcription review

Descript auto-transcribes on import. One pass on technical terms:

| What you said | What Descript writes | Fix to |
|---|---|---|
| n8n | "en-8-en", "n-8-n", "Nate N" | n8n |
| Supabase | "super base", "Soupa Base" | Supabase |
| Anthropic | usually correct | — |
| Base44 | "base 44", "Bass 44" | Base44 |
| Claude | usually correct | — |
| FlashFusion | "flash fusion", "Flash Fusion" | FlashFusion |
| MCP | usually correct | — |

Fixes in transcript propagate to captions automatically.

### Step 3: Edit by transcript

- Select and delete text to cut that section from video
- Remove filler words: Edit → Remove filler words → `um`, `uh`, `like`, `you know`
- Remove long silences: Edit → Remove silence → threshold 0.8–1.2 sec
- Rearrange: select text block, drag to new position
- Misspoke a word: right-click → Overdub (replaces with your voice clone)

### Step 4: Audio cleanup

Effects → Studio Sound. Apply to full track. Listen to 30-second before/after
sample to verify it didn't over-process.

### Step 5: Identify and extract clips

1. Read transcript for moments that work standalone
2. Good clip: one clear point, strong opener, 60–120 sec
3. Tutorial: moment you reveal the finished result = good clip opener
4. Mark: highlight text → right-click → Create Clip

Target: 2–3 clips per session minimum.

### Step 6: Captions

Auto-generated from transcript. Review for technical terms from Step 2.
Style: white text, dark background, sentence case, lower third.
Export: SRT preferred for YouTube (can be toggled). Burned-in for LinkedIn/Shorts.

### Step 7: Export

| Output | Settings |
|---|---|
| YouTube full video | 1080p, 16:9, H.264, AAC audio, captions as SRT |
| LinkedIn clip | 1080x1080 (1:1) or 1080x1350 (4:5), MP4, captions burned-in |
| YouTube Shorts clip | 1080x1920 (9:16), captions burned-in |
| Twitter/X clip | 1920x1080 or 1080x1080, under 512MB |

Export full video and all clips in one session before closing the project.

---

## Section 5: Repurposing Cascade

**Run after every Descript or HeyGen production session before archiving.**

- [ ] **YouTube full video** exported with SEO title, description draft, timestamps
- [ ] **LinkedIn clips** (2–3, 60–120 sec) exported 1:1 or 4:5, captions burned-in
- [ ] **YouTube Shorts clip** (30–60 sec, 9:16) from strongest moment
- [ ] **Transcript exported** → `FlashFusion/Content/Video/transcripts/{{title}}.txt`
       → becomes draft for blog post or newsletter section
- [ ] **Thumbnail** in Canva: 1280x720, high contrast, readable at small size

If not done before archiving, it doesn't get done.

---

## Section 6: Voice Guidelines for Video

**What works the same across all three tools:**
- Anti-credential opener: "I'm not a [X]. I'm an L1 service desk tech who
  builds AI apps on the side." Opens attention immediately.
- Declarative observations: "I stopped prompting for outputs. I started
  designing flows." Works as cold open or chapter intro.
- Specific over impressive: name the tool, the error, the file path.
- Dry humor: deliver flat, don't signal the punchline.

**What needs adjustment:**
- Pacing: written rhythm = paragraph breaks. Video = silence. After a key
  point, stop. One full beat. Don't fill the gap.
- No tutorial intro: skip "in today's video we're going to..." — open on
  the problem or result.
- No outro padding: end punchy or paradoxical. Cut. No subscribe plea.

**For Descript screen recordings:**
Talk while doing. Narrate what you're building as you build it. "I'm setting
the trigger to webhook — and the reason I'm not using a schedule trigger is..."
is more engaging than commentary recorded after the fact.

**For HeyGen avatar delivery:**
The avatar amplifies whatever is in the script. A flat script produces a flat
avatar. The origin story script specifically needs the voice principles from
`crafting-long-form-memoir` — direct, specific, uncertainty without performance.
The avatar cannot save a script that's performing rather than saying something.

---

## Section 7: Post-Publish (YouTube SEO)

**Title:** keyword near front, 60 chars max, no clickbait
- Good: "Building a Multi-Agent Workflow in n8n — Step by Step"
- Bad: "This AI Workflow CHANGED My Business (You Need to See This)"

**Description:** first 150 chars = hook shown in search. Then: coverage,
chapters/timestamps, links to FlashFusion content, newsletter signup,
2–3 sentence transcript excerpt.

**Chapters:** required for any tutorial over 5 min. Format: `0:00 Intro`

**Tags:** 8–12 tags, specific + broad

**Thumbnail:** upload separately — never use YouTube auto-frame

**Cards:** add at 20% through video

Notify `publishing-optimized-content` after upload for SEO post-publish checklist.

---

## Anti-Patterns

- **Don't use Invideo for content where your presence matters.** Stock footage
  and AI narration have a lower trust ceiling. If it's a real story, real
  tutorial, or real client work — Descript or HeyGen.
- **Don't use HeyGen for content where authenticity requires real footage.**
  An avatar presenting a live workflow demo is less convincing than you
  actually doing it. HeyGen is for scripted delivery, not demonstrations.
- **Don't skip repurposing.** The full YouTube video is the least-viewed
  surface. The LinkedIn clip is where the audience is. Record once, clip always.
- **Don't skip the HeyGen preview render.** Technical term mispronunciation
  and lip sync drift are only fixable before you distribute. Catch them early.
- **Don't write a script for Descript screen recordings.** Scripted screen
  recordings sound stiff. Know what you're building, hit record, talk through
  it. Edit the mistakes in Descript.
- **Don't archive the Descript project without running the repurposing cascade.**
  The clips don't get made later. They get made now or not at all.
