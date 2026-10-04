---
name: apply-media-captions
description: Use when publishing video, audio, or any time-based media — to provide captions, transcripts, and audio descriptions for users who cannot hear or see the media content.
source: W3C WCAG 2.1 SC 1.2.1–1.2.5 (Level A/AA); W3C WebVTT specification; BBC Subtitle Guidelines; Netflix Timed Text Style Guide
tags: [accessibility, wcag, a11y, captions, transcripts, audio-description, media, developer]
related: [design-accessibility-standards, audit-accessibility, apply-text-alternatives]
---

# Apply Media Captions

Provide synchronized captions for video, transcripts for audio, and audio descriptions for visual-only content.

## Why This Is Best Practice

**Adopted by:** WCAG 2.1 SCs 1.2.1–1.2.5 are Level A/AA — legally required by Section
508 (US), ADA, EU EN 301 549, and the UK Equality Act. Netflix was sued and settled
for $755,000 in 2012 for missing captions (NAD v. Netflix) — the landmark case that
accelerated industry adoption. All major streaming platforms (YouTube, Vimeo, AWS
Elemental MediaConvert) now provide auto-captioning as baseline infrastructure.
**Impact:** WHO estimates 1.5 billion people have hearing loss. Captions also benefit
users in noisy environments, non-native language speakers, and users with cognitive
disabilities. Facebook data showed 85% of videos are watched without sound — captions
improve engagement for all users, not just those with disabilities.
**Why best:** Auto-generated captions alone are insufficient — accuracy rates of 80–90%
produce too many errors for compliance. Human-verified captions or caption editing is
required for WCAG conformance.

Sources: W3C WCAG 2.1 SC 1.2.1–1.2.5 (2018); NAD v. Netflix settlement (2012);
Facebook Captions research (2016); W3C WebVTT specification

## Steps

### Step 1: Identify what each media type requires

| Media type | Level A requirement | Level AA addition |
|------------|--------------------|--------------------|
| Pre-recorded audio-only | Transcript | — |
| Pre-recorded video-only | Audio description OR transcript | — |
| Pre-recorded video+audio | Captions | Audio description |
| Live video+audio | Live captions | — |

### Step 2: Add synchronized captions to video using WebVTT

```html
<video controls>
  <source src="product-demo.mp4" type="video/mp4">
  <track kind="captions"
         src="product-demo.en.vtt"
         srclang="en"
         label="English"
         default>
</video>
```

WebVTT format:
```
WEBVTT

00:00:01.000 --> 00:00:04.000
Welcome to the product demo.

00:00:04.500 --> 00:00:08.000
Today we'll cover the three main features.

NOTE Speaker change
00:00:08.500 --> 00:00:12.000
[Jane] First, let's look at the dashboard.
```

Caption quality requirements:
- Synchronize within 2 seconds of speech
- Identify speakers when more than one person speaks: `[Speaker Name]`
- Describe significant non-speech audio: `[applause]`, `[alarm beeping]`
- Do not exceed 42 characters per line, 2 lines per caption

### Step 3: Write transcripts for audio-only content

```html
<audio controls src="podcast-ep-42.mp3"></audio>

<details>
  <summary>Transcript — Episode 42</summary>
  <p><strong>Host:</strong> Welcome to episode 42...</p>
  <p><strong>Guest:</strong> Thank you for having me...</p>
</details>
```

Transcripts must include all speech, speaker identification, and meaningful non-speech
sounds. A transcript linked adjacent to the player satisfies WCAG 1.2.1.

### Step 4: Add audio descriptions for visual content in video

When video conveys information through visuals not described in dialogue, add an
audio description track:

```html
<video controls>
  <source src="tutorial.mp4" type="video/mp4">
  <track kind="captions" src="tutorial.en.vtt" srclang="en" label="English captions" default>
  <track kind="descriptions" src="tutorial.en.desc.vtt" srclang="en" label="Audio descriptions">
</video>
```

Or provide a separate audio-described version as a link adjacent to the player.

### Step 5: Verify caption quality before publishing

Checklist:
- [ ] Captions are synchronized (within 2s)
- [ ] All speech is captured — no paraphrasing
- [ ] Speakers identified where more than one voice
- [ ] Non-speech audio described where meaningful
- [ ] Captions do not overlap or crowd the screen
- [ ] Auto-captions reviewed and corrected (do not ship raw auto-captions)

## When NOT to Use

- **Purely decorative background video** (no meaningful audio or visual content) — mark with `aria-hidden="true"` and `muted autoplay`. No captions required.
- **Live video where real-time captions are technically infeasible** — document the exception and provide a text alternative as soon as practically possible after the live event.

## Common Mistakes

**Shipping auto-generated captions without review.** Auto-caption accuracy of 80% means 1 in 5 words is wrong. This fails WCAG 1.2.2 and produces an unreliable experience.

**Captions that only cover speech.** A video where an alarm sounds and the character reacts — but the captions say nothing about the alarm — fails to convey equivalent information.

**Transcript behind a paywall or login.** If the media itself is accessible without login, so must the transcript be.