---
name: iconography-lab
description: "Define the instantly recognizable visual and verbal codes of a public figure, including palette, props, silhouettes, poses, moods, and catchphrases, then output an identity kit. Use when Codex needs to make a personality-led brand recognizable without flattening it into generic branding."
---

# Iconography Lab

Use this skill when you need a clean identity kit for a creator, celebrity, or founder whose audience responds to specific visual and verbal codes.

Default product shape: a compact macOS `MenuBarExtra` utility with a source-aware popover for reference intake, code mapping, and identity export and an optional settings/history window.

## Quick Start

1. Confirm the subject, target audience, and source window.
2. Gather only public or user-authorized material into a working set.
3. Produce a `identity-kit` with the default sections below.
4. If the user wants a richer product concept, keep it menu bar first and native to SwiftUI.

## Accepted Inputs

- photo sets, thumbnails, posters, livestream stills, or public press images
- captions, slogans, catchphrases, recurring titles, and community nicknames
- notes about props, wardrobe pieces, gestures, framing, or signature moods
- existing brand decks when the user wants continuity rather than reinvention

## Output Artifact

Primary artifact: `identity-kit`

Default sections:
- Palette and contrast direction
- Props, wardrobe anchors, and object cues
- Silhouette, pose, and framing signatures
- Verbal codes such as catchphrases, tone, and naming patterns
- Do and do not guidance for future content or merch

## Workflow

### Gather Sources

- Collect the references that the audience already recognizes, not just the team's favorite visuals.
- Separate transient campaign styling from durable identity cues.
- Note where a verbal code or prop appears consistently across formats.

### Distill Signal

- Cluster cues into color, prop, silhouette, motion, and phrase systems.
- Identify what is unmistakable versus what is merely common to the category.
- Call out where imitation would drift into infringement or impersonation.

### Build The Artifact

- Export an identity kit with reusable visual and verbal codes.
- Show how each code can scale across thumbnails, events, community posts, and merch.
- End with a short restraint note so the identity stays specific instead of overdesigned.

### Mac Product Shape

- Prefer `MenuBarExtra` with these primary actions:
  - `Collect References`
  - `Map Codes`
  - `Build Kit`
  - `Export Guide`
- Keep the popover between 320 pt and 380 pt wide with grouped sections, clear source status, and a strong export action.
- Use a lightweight settings or history window only for source rules, saved exports, or weighting controls.

### Safety Boundaries

- Work only from public or user-authorized material.
- Do not assist with stalking, covert profiling, rumor laundering, harassment, or minors-focused manipulation.
- Do not encourage deceptive impersonation, likeness misuse, or copying another artist's protected visual asset too closely.

## Example Prompts

- `Use $iconography-lab to turn these performance photos and captions into an identity kit with palette, prop system, and catchphrase guidance.`
- `Use $iconography-lab to map this founder's visual and verbal codes so our next product launch looks recognizable without becoming generic tech-branding.`

## Resources

- `references/product-spec.md`: product surface, SwiftUI layout, artifact template, icon direction, and first-run behavior.
