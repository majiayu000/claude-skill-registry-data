---
name: clip-to-canon-finder
description: "Identify short-form moments most likely to turn into fandom artifacts, edits, or memes from clips, transcripts, and reaction data, then output a shortlist with reuse angles. Use when Codex needs to find which moments deserve to become repeatable canon."
---

# Clip to Canon Finder

Use this skill when you need to score short-form moments by meme potential, editability, and canon value.

Default product shape: a compact macOS `MenuBarExtra` utility with a source-aware popover for clip intake, moment scoring, and shortlist export and an optional settings/history window.

## Quick Start

1. Confirm the subject, target audience, and source window.
2. Gather only public or user-authorized material into a working set.
3. Produce a `clip-shortlist` with the default sections below.
4. If the user wants a richer product concept, keep it menu bar first and native to SwiftUI.

## Accepted Inputs

- video links, rough timestamps, or short-form exports from Reels, Shorts, or TikTok
- transcripts, subtitle files, or manual clip notes
- comment samples that show which line or reaction fans keep repeating
- editor notes about current formats, cut length, and reuse constraints

## Output Artifact

Primary artifact: `clip-shortlist`

Default sections:
- Shortlisted moments with timestamps or identifiable cut points
- Why each moment sticks: line, look, reaction, or dynamic
- Fandom reuse angle for edits, memes, callbacks, or compilation posts
- Cut guidance for short-form packaging and thumbnail framing
- Moments to skip because the signal is weak, mean-spirited, or misleading

## Workflow

### Gather Sources

- Normalize clip references and match them to transcript segments when available.
- Mark where the audience is quoting, clipping, or repeatedly reacting to the same beat.
- Separate the raw moment from platform-specific editing noise.

### Distill Signal

- Score moments by surprise, clarity, quotability, and replay value.
- Differentiate wholesome fan canon from rage-bait or context collapse.
- Identify which moments can support sequels, remixes, or callback edits.

### Build The Artifact

- Export a shortlist with timestamp, hook, signal strength, and reuse angle.
- Suggest one clean cut pattern for each winning moment.
- Flag any clip where quote-mining or decontextualization would mislead the audience.

### Mac Product Shape

- Prefer `MenuBarExtra` with these primary actions:
  - `Add Clips`
  - `Score Moments`
  - `Review Shortlist`
  - `Export Angles`
- Keep the popover between 320 pt and 380 pt wide with grouped sections, clear source status, and a strong export action.
- Use a lightweight settings or history window only for source rules, saved exports, or weighting controls.

### Safety Boundaries

- Work only from public or user-authorized material.
- Do not assist with stalking, covert profiling, rumor laundering, harassment, or minors-focused manipulation.
- Do not recommend deceptive quote-mining, harassment bait, or edits that distort the original context in a harmful way.

## Example Prompts

- `Use $clip-to-canon-finder to score these livestream moments and tell me which ones can become repeatable edit bait without feeling forced.`
- `Use $clip-to-canon-finder to analyze these founder short-form videos and shortlist the moments worth turning into recurring canon callbacks.`

## Resources

- `references/product-spec.md`: product surface, SwiftUI layout, artifact template, icon direction, and first-run behavior.
