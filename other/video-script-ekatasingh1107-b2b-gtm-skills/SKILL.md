---
name: video-script
description: Generate formatted video scripts from transcripts, outlines, or topics with visual and audio columns
tags: [video, script, content, creative, production]
---

# Video Script Generator

Transforms raw transcripts, topic briefs, or outlines into production-ready video scripts. Outputs a two-column format with visual descriptions, dialogue/voiceover, on-screen text, timing, and B-roll suggestions. Supports testimonial videos, explainer videos, social shorts (Reels/TikTok/Shorts), ad spots, and long-form content. Matches brand voice from config.

## Prerequisites

- `agency.config.json` in the project root
- Raw transcript, outline, or topic from user
- Video type specification (testimonial, explainer, social short, ad)
- Optional: existing footage inventory or B-roll library notes

## Phase 0: Read Config

1. Read `agency.config.json` from the project root.
2. Extract brand voice values:
   - `agency.name`, `agency.tagline`
   - `outreach.tone` -- writing style and voice
   - `brand.voice` -- if defined, use for dialogue tone
3. Extract `services[]` for service-related videos.
4. Extract `case_studies[]` for testimonial or proof-based scripts.
5. Check `tools.video` for any production tool preferences.

## Phase 1: Gather Inputs

Collect from the user:
- **Source material**: raw transcript, bullet-point outline, or topic description
- **Video type**: testimonial, explainer, social short, ad spot, webinar intro, product demo
- **Target length**: in seconds or minutes
- **Platform**: YouTube, Instagram Reels, TikTok, LinkedIn, website, ads
- **Speaker**: founder, client, voiceover artist, or text-only (no speaker)
- **Tone override**: if different from config default
- **CTA**: what the viewer should do after watching

## Phase 2: Determine Video Structure

Select the structure template based on video type:

**Testimonial (60-120 seconds):**
```
1. Hook -- client states the result (5s)
2. Context -- who they are, what they do (10s)
3. Problem -- what was broken before (15s)
4. Discovery -- how they found you (10s)
5. Solution -- what you did for them (20s)
6. Results -- specific metrics and outcomes (15s)
7. Recommendation -- would they recommend, to whom (10s)
8. CTA -- agency branding and next step (5s)
```

**Explainer (60-90 seconds):**
```
1. Hook -- state the problem in one sentence (5s)
2. Agitate -- why this problem costs money/time (10s)
3. Introduce solution -- your approach in one line (5s)
4. Step 1 -- first part of the process (15s)
5. Step 2 -- second part (15s)
6. Step 3 -- third part (15s)
7. Results -- what the viewer gains (10s)
8. CTA -- clear next action (5s)
```

**Social Short (15-60 seconds):**
```
1. Hook -- pattern interrupt, first 3 seconds are everything (3s)
2. Setup -- one-sentence context (5s)
3. Value -- the insight, tip, or reveal (15-30s)
4. Proof -- quick metric or example (5s)
5. CTA -- follow, link in bio, comment (3s)
```

**Ad Spot (15-30 seconds):**
```
1. Hook -- problem or desire statement (3s)
2. Solution -- what you offer (5s)
3. Proof -- metric or social proof (5s)
4. Offer -- specific deal or next step (5s)
5. CTA -- clear action with urgency (3s)
```

**Product Demo (2-5 minutes):**
```
1. Hook -- the outcome this product enables (5s)
2. Overview -- what the product is (15s)
3. Feature walkthrough -- 3-5 key features (60-120s)
4. Use case -- real scenario demonstration (30s)
5. Comparison -- before/after or vs alternatives (20s)
6. Social proof -- user quote or metric (10s)
7. CTA -- trial, demo, or purchase (10s)
```

## Phase 3: Process Source Material

**If raw transcript provided:**
1. Remove filler words (um, uh, like, you know, so, basically)
2. Fix grammar without changing the speaker's natural voice
3. Identify key quotes worth keeping verbatim
4. Extract the core narrative arc
5. Flag sections that are off-topic or redundant
6. Reorder for logical flow if the original meanders

**If outline provided:**
1. Expand bullet points into natural spoken language
2. Add transitions between sections
3. Ensure each point has a clear setup and payoff
4. Match the word count to the target duration (roughly 150 words per minute for spoken content)

**If topic only:**
1. Research the topic using available tools
2. Build an outline using the structure template
3. Write the full script from scratch
4. Include data points and examples where possible

## Phase 4: Write the Two-Column Script

Format the script with parallel columns:

```
TIMECODE | VISUAL                    | AUDIO/DIALOGUE              | ON-SCREEN TEXT
---------|---------------------------|-----------------------------|-----------------
00:00    | [Camera: medium shot of   | [Speaker]: "We were         | --
         |  speaker at desk]         |  losing 40% of our cart     |
         |                           |  abandoners..."             |
00:05    | [B-roll: website          | [VO]: "Before working       | "40% cart
         |  screenshot showing       |  with the agency, their     |  abandonment
         |  checkout page]           |  checkout was broken."      |  rate"
00:10    | [Screen recording:        | [Speaker]: "They rebuilt    | --
         |  before/after of          |  our entire checkout        |
         |  the checkout flow]       |  flow in two weeks."        |
```

**Script writing rules:**
- Hook must land in the first 3 seconds -- no slow intros
- Every sentence should be speakable naturally (read it aloud mentally)
- Dialogue: use contractions, casual phrasing, real speech patterns
- Voiceover: slightly more polished but still conversational
- One idea per shot -- new idea means new visual
- On-screen text reinforces key numbers and phrases only, not full dialogue
- B-roll descriptions are specific enough for a videographer to shoot or source

**Word count targets by duration:**

| Duration | Word Count | Pace |
|----------|-----------|------|
| 15 seconds | 35-40 words | Fast, punchy |
| 30 seconds | 70-80 words | Tight, no waste |
| 60 seconds | 140-160 words | Comfortable |
| 90 seconds | 210-240 words | Room to breathe |
| 2 minutes | 280-320 words | Standard explainer |
| 5 minutes | 700-800 words | Detailed, sections |

## Phase 5: Add Production Notes

Append production guidance:

**B-roll suggestions:**
List 5-10 specific B-roll shots needed:
```
B-ROLL LIST:
1. [Shot description] -- used at [timecode]
2. [Shot description] -- used at [timecode]
3. Screen recording: [specific page/flow to capture]
4. Stock footage: [search terms for stock sites]
```

**Music and sound:**
```
AUDIO NOTES:
- Background music: [mood -- e.g., "upbeat corporate, 120 BPM"]
- Music duck at: [timecodes where music should lower for dialogue]
- Sound effects: [any SFX needed and where]
- Music out: [when to fade music]
```

**Graphics and lower thirds:**
```
GRAPHICS:
- Lower third: [Speaker name and title] at [timecode]
- Metric callout: [number] at [timecode]
- Logo: [placement and timing]
- End card: [CTA text, URL, contact info]
```

## Phase 6: Output

Return structured JSON:

```json
{
  "video_script": {
    "title": "[Video title]",
    "type": "[testimonial/explainer/social-short/ad/demo]",
    "platform": "[YouTube/Instagram/TikTok/LinkedIn/website]",
    "duration_seconds": 90,
    "word_count": 225,
    "speaker": "[who speaks]",
    "tone": "[tone used]",
    "hook": "[first line of the video -- the critical opening]",
    "cta": "[closing call to action]",
    "script": [
      {
        "timecode": "00:00",
        "duration_seconds": 5,
        "visual": "Camera: medium shot of speaker",
        "audio": "[Speaker]: Opening line here",
        "on_screen_text": "",
        "notes": "Cut tight, no dead air"
      }
    ],
    "b_roll": [
      {
        "description": "Website screenshot of checkout page",
        "used_at": "00:05",
        "source": "screen-recording"
      }
    ],
    "music": {
      "mood": "upbeat corporate",
      "duck_at": ["00:00", "00:15"],
      "fade_out": "01:25"
    },
    "graphics": [
      {
        "type": "lower-third",
        "content": "Speaker Name, Title",
        "timecode": "00:02"
      }
    ],
    "production_notes": "[Any special instructions for editors]"
  }
}
```

## Example Usage

**Trigger phrases:**
- "Turn this transcript into a video script"
- "Write a 60-second explainer video script about our CRO service"
- "Create a testimonial video script for [client]"
- "Script a 30-second Instagram Reel about [topic]"
- "Write an ad script for our YouTube pre-roll"
- "Convert this outline into a product demo script"

```
User: Write a 60-second testimonial script for a client
Assistant: [reads case study data from config, structures testimonial arc, writes two-column script with hook/problem/solution/results, adds B-roll list and production notes]
```

```
User: Script a 15-second TikTok about why D2C brands need CRO
Assistant: [writes ultra-tight 35-word script with pattern-interrupt hook, one key stat, and follow CTA, formatted for vertical video]
```
