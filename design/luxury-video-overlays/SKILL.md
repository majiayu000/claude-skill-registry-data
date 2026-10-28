---
name: luxury-video-overlays
description: Build luxury Remotion overlay edits for long-form talking-head videos. Use when Codex needs to turn an Agent Zero edited base video and transcript into a polished green/gold video with split-screen overlay cards, full-screen statement slides, animated bullet reveals, continuous ticker bands, SFX timing, and held emphasis zooms/jump cuts.
---

# Luxury Video Overlays

## Core Workflow

Use this skill to create a polished long-form video edit after Agent Zero has already done the heavy lifting: silence removal, base jump cuts, audio cleanup, and transcription.

1. Preserve the current working version before changing visuals:
   - Save the current manifest, render command, screenshots, and process notes in a dated restore folder.
   - Keep successful renders restorable by exact file name and props file.
2. Use Agent Zero outputs as inputs:
   - Edited base video: `.tmp/edited_base.mp4`
   - Transcript: `.tmp/transcript.json`
3. Install or update the Remotion assets:
   - Copy `assets/remotion/components/LuxuryOverlayKit.tsx`.
   - Copy `assets/remotion/compositions/LuxuryTalkingHeadEdit.tsx`.
   - Register the wrapper component in the target Remotion `Root.tsx`.
4. Build a manifest from transcript beats:
   - Aim for one overlay roughly every 8-12 seconds, matching flow rather than forcing strict timing.
   - Alternate overlay types: opener/count, split card, bullet reveal, full-screen statement, number counter, recap.
   - Pair every visible animation, reveal, card exit, scene return, or jump zoom with an SFX cue.
5. Render and verify:
   - Render Remotion composition with props.
   - Export final master at 1920x1080 unless the user requests another format.
   - Check screenshots around every overlay and listen for SFX timing.

## Overlay Rules

- Use split-screen cards when the speaker should remain visible: card on one half, cropped/shifted talking head on the other half.
- Use full-screen statement cards for major points, mistakes, rules, or philosophical pivots.
- Reveal bullet points one at a time with upward fade motion and a short paper/crumple/click SFX.
- Use held emphasis zooms: once a zoom punches in, keep that zoom level until the next overlay boundary or explicit reset frame.
- Keep the bottom ticker continuous. It should scroll without a visible reset or rupture.
- Avoid generic filler copy. Pull bullet text from transcript, notes, or the user's knowledge base when available.
- Do not use decorative social icons unless requested.

## SFX Mapping

Use SFX as part of the edit grammar, not as decoration:

- `whoosh`: card entrances, exits, scene transitions, return from overlay to talking head.
- `paper-crumple` or `paper-fold`: bullet reveal, idea unpacking, checklist item reveal.
- `soft-bing` or `notification-chime`: key insight, "this is the key", important emphasis.
- `low-hit` or `subtle-impact`: mistake reveal, hard truth, rule headline.
- `riser`: opener/preloader, large transition, full-screen statement reveal.

Set SFX volume high enough to be audible under voice. Start around `0.28-0.36` in the manifest and adjust by ear.

## Bundled Resources

- `assets/remotion/components/LuxuryOverlayKit.tsx`: reusable overlay kit with cards, ticker, SFX layer, counters, and full-screen statements.
- `assets/remotion/compositions/LuxuryTalkingHeadEdit.tsx`: Remotion composition wrapper for the manifest-driven edit.
- `references/workflow.md`: detailed Agent Zero plus Remotion handoff and server setup notes.
- `references/design-system.md`: visual language, timing, overlay selection, and SFX guidance.
- `references/example-manifest.json`: example props manifest.
- `scripts/install_remotion_assets.py`: copy assets into a Remotion project.
- `scripts/build_luxury_manifest.py`: generate a starter manifest from timed beats.
- `scripts/scan_for_secrets.py`: scan the package before publishing.

## Safety

Before publishing or pushing to GitHub, run a secret scan and inspect `git status`. Never include `.env`, API keys, tokens, credentials, private raw videos, private rendered videos, transcripts with confidential content, or server IPs. Use `.env.example` placeholders only.
