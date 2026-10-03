---
name: fan-canon-miner
description: "Mine comments, interviews, captions, and fan chatter around a creator, celebrity, or founder to identify the symbols, phrases, moments, and myths people repeat, then turn them into a canon map. Use when Codex needs fandom analysis grounded in public or user-authorized material."
---

# Fan Canon Miner

Use this skill when you need to turn recurring fan symbols, phrases, inside jokes, and breakout moments into a usable canon map.

Default product shape: a compact macOS `MenuBarExtra` utility with a source-aware popover for source intake, canon extraction, and brief export and an optional settings/history window.

## Quick Start

1. Confirm the subject, target audience, and source window.
2. Gather only public or user-authorized material into a working set.
3. Produce a `canon-map` with the default sections below.
4. If the user wants a richer product concept, keep it menu bar first and native to SwiftUI.

## Accepted Inputs

- comment exports or copied threads from TikTok, Instagram, YouTube, X, Reddit, Discord, or newsletters
- interview transcripts, Q and A logs, podcast notes, or livestream recaps
- captions, community posts, fan edit descriptions, and meme references
- user-provided notes about breakout moments, props, nicknames, or recurring story beats

## Output Artifact

Primary artifact: `canon-map`

Default sections:
- Repeated symbols and aesthetic anchors
- Signature lines, nicknames, and fan language
- Canon moments with why they stuck
- Myths, lore threads, and callbacks the audience keeps reviving
- Three practical content opportunities that respect existing canon

## Workflow

### Gather Sources

- Deduplicate overlapping source dumps and note the platform plus time window.
- Separate first-party voice from audience response before clustering patterns.
- Flag claims that appear only once so the canon map stays grounded.

### Distill Signal

- Count repeated phrases, objects, scenes, and emotional beats.
- Group references into stable canon instead of one-off jokes.
- Rank each cluster by recurrence, emotional charge, and remixability.

### Build The Artifact

- Draft a canon map with core, rising, and fragile lore buckets.
- Call out what feels audience-native versus what should not be forced.
- End with near-term content or community moves that build on the existing canon.

### Mac Product Shape

- Prefer `MenuBarExtra` with these primary actions:
  - `Add Sources`
  - `Mine Canon`
  - `View Map`
  - `Export Brief`
  - `History`
- Keep the popover between 320 pt and 380 pt wide with grouped sections, clear source status, and a strong export action.
- Use a lightweight settings or history window only for source rules, saved exports, or weighting controls.

### Safety Boundaries

- Work only from public or user-authorized material.
- Do not assist with stalking, covert profiling, rumor laundering, harassment, or minors-focused manipulation.
- Avoid speculative personal narratives, protected-private-life gossip, or attempts to intensify dependency on the public figure.

## Example Prompts

- `Use $fan-canon-miner to map the canon around this streamer from the last 90 days of comments and recap the top myths fans keep repeating.`
- `Use $fan-canon-miner to turn these founder interviews and community replies into a canon map with signature lines, props, and callback opportunities.`

## Resources

- `references/product-spec.md`: product surface, SwiftUI layout, artifact template, icon direction, and first-run behavior.
