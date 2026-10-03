---
name: comment-pulse-board
description: "Cluster obsession points, recurring questions, sentiment shifts, and backlash signals across audience chatter to produce a pulse digest. Use when Codex needs a timely view of what a personal-brand audience is amplifying, asking for, or turning against."
---

# Comment Pulse Board

Use this skill when you need a fast, structured digest of what the audience is obsessing over, asking about, or turning against.

Default product shape: a compact macOS `MenuBarExtra` utility with a source-aware popover for chatter intake, pulse clustering, and shift review and an optional settings/history window.

## Quick Start

1. Confirm the subject, target audience, and source window.
2. Gather only public or user-authorized material into a working set.
3. Produce a `pulse-digest` with the default sections below.
4. If the user wants a richer product concept, keep it menu bar first and native to SwiftUI.

## Accepted Inputs

- comment dumps, replies, quote posts, and community forum snapshots
- support inbox excerpts, FAQ logs, or AMA question lists
- moderation notes about flare-ups, repeat confusion, or repeated praise
- user-provided context about recent launches, controversies, or content pivots

## Output Artifact

Primary artifact: `pulse-digest`

Default sections:
- Top obsession clusters and why they matter
- Recurring questions or unresolved confusion
- Sentiment shifts compared with the prior source window
- Backlash or fatigue signals that need human review
- Suggested response priorities for the next content cycle

## Workflow

### Gather Sources

- Normalize comments into one working set while preserving source labels.
- Separate high-volume repetition from isolated but severe complaints.
- Flag missing context when a sentiment swing may be tied to an external event.

### Distill Signal

- Cluster repeated topics, questions, and emotional reactions.
- Score clusters by volume, speed, and intensity rather than raw volume alone.
- Separate healthy criticism, confusion, delight, and harassment signals.

### Build The Artifact

- Write a pulse digest that shows what is rising, stable, cooling, or risky.
- Call out where silence is better than a response.
- End with concise next-step recommendations for content, moderation, or support.

### Mac Product Shape

- Prefer `MenuBarExtra` with these primary actions:
  - `Import Chatter`
  - `Cluster Pulse`
  - `Review Shifts`
  - `Export Digest`
- Keep the popover between 320 pt and 380 pt wide with grouped sections, clear source status, and a strong export action.
- Use a lightweight settings or history window only for source rules, saved exports, or weighting controls.

### Safety Boundaries

- Work only from public or user-authorized material.
- Do not assist with stalking, covert profiling, rumor laundering, harassment, or minors-focused manipulation.
- Do not target individual critics, encourage brigading, or reframe harassment as audience strategy.

## Example Prompts

- `Use $comment-pulse-board to analyze this week's TikTok and Instagram comments and tell me what the audience is fixated on versus what is turning negative.`
- `Use $comment-pulse-board to cluster these founder-community replies into obsession points, recurring questions, and backlash watch items.`

## Resources

- `references/product-spec.md`: product surface, SwiftUI layout, artifact template, icon direction, and first-run behavior.
