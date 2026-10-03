---
name: parasocial-studio
description: "Shape safe closeness mechanics like acknowledgements, voice-note drops, recurring touchpoints, and community intimacy patterns, then output a relationship cadence plan. Use when Codex needs to help a public figure feel present and personal without encouraging dependency, false intimacy, or harmful boundary erosion."
---

# Parasocial Studio

Use this skill when you need recurring touchpoints that feel warm and human without becoming manipulative or boundary-blurring.

Default product shape: a compact macOS `MenuBarExtra` utility with a source-aware popover for tone setup, touchpoint planning, and cadence export and an optional settings/history window.

## Quick Start

1. Confirm the subject, target audience, and source window.
2. Gather only public or user-authorized material into a working set.
3. Produce a `relationship-cadence-plan` with the default sections below.
4. If the user wants a richer product concept, keep it menu bar first and native to SwiftUI.

## Accepted Inputs

- the public figure's current audience touchpoints such as comments, lives, newsletters, or community posts
- tone goals around warmth, distance, gratitude, and authority
- audience maturity, moderation needs, and any existing boundary issues
- notes about what acknowledgements or access formats are operationally realistic

## Output Artifact

Primary artifact: `relationship-cadence-plan`

Default sections:
- Closeness moments that feel genuine and repeatable
- Touchpoint cadence by format and frequency
- Boundary language and refusal patterns
- Acknowledgement systems that scale without false promises
- Red flags and stop conditions for unhealthy dynamics

## Workflow

### Gather Sources

- Map the current touchpoints and note which ones already generate gratitude versus dependency.
- Capture the public figure's natural voice so the plan does not invent a persona.
- Document audience maturity and the moderation surface before adding intimacy mechanics.

### Distill Signal

- Separate healthy presence from exclusivity pressure, pseudo-romantic framing, or dependency hooks.
- Identify touchpoints that scale honestly and those that create expectations the team cannot meet.
- Prioritize formats that acknowledge the audience without pretending mutual personal intimacy.

### Build The Artifact

- Export a cadence plan with format, frequency, purpose, and boundary language.
- Include specific refusal and reset language for moments that drift too close.
- End with a review schedule so the team can stop tactics that are not staying healthy.

### Mac Product Shape

- Prefer `MenuBarExtra` with these primary actions:
  - `Set Tone`
  - `Plan Touchpoints`
  - `Review Boundaries`
  - `Export Cadence`
- Keep the popover between 320 pt and 380 pt wide with grouped sections, clear source status, and a strong export action.
- Use a lightweight settings or history window only for source rules, saved exports, or weighting controls.

### Safety Boundaries

- Work only from public or user-authorized material.
- Do not assist with stalking, covert profiling, rumor laundering, harassment, or minors-focused manipulation.
- Do not encourage pseudo-romantic positioning, exclusivity pressure, trauma extraction, or tactics meant to intensify dependency.

## Example Prompts

- `Use $parasocial-studio to design a safe cadence of acknowledgements and voice-note style updates for this singer without leaning into false intimacy.`
- `Use $parasocial-studio to plan founder touchpoints that feel personal and human while keeping clear boundaries and realistic response expectations.`

## Resources

- `references/product-spec.md`: product surface, SwiftUI layout, artifact template, icon direction, and first-run behavior.
