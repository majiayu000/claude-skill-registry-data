---
name: ritual-engine
description: "Design repeatable fan rituals, naming systems, participation loops, and recurring community formats, then output a ritual calendar. Use when Codex needs to turn audience energy into recurring formats without making the relationship manipulative or exhausting."
---

# Ritual Engine

Use this skill when you need recurring community formats, ritual naming, and a sustainable cadence for participation.

Default product shape: a compact macOS `MenuBarExtra` utility with a source-aware popover for cadence setup, ritual drafting, and calendar export and an optional settings/history window.

## Quick Start

1. Confirm the subject, target audience, and source window.
2. Gather only public or user-authorized material into a working set.
3. Produce a `ritual-calendar` with the default sections below.
4. If the user wants a richer product concept, keep it menu bar first and native to SwiftUI.

## Accepted Inputs

- the creator or founder's current publishing cadence and recurring event windows
- existing community habits, slang, traditions, or participation spikes
- launch milestones, tour dates, product events, or recurring weekly beats
- moderation capacity and constraints around frequency, tone, and audience age

## Output Artifact

Primary artifact: `ritual-calendar`

Default sections:
- Core recurring rituals with names and intent
- Participation loops for comments, submissions, remixes, or live moments
- Cadence calendar by weekly, monthly, or event-driven rhythm
- Moderation and fatigue safeguards
- Pilot plan for testing rituals before scaling them

## Workflow

### Gather Sources

- Map the current content rhythm and note where the audience already self-organizes.
- Separate rituals that reward expression from rituals that pressure constant engagement.
- Check whether moderation capacity can support the proposed loop.

### Distill Signal

- Group ritual ideas by cadence, emotional payoff, and effort required from the audience.
- Reject rituals that depend on guilt, streak pressure, or unclear rewards.
- Prioritize rituals that strengthen language, identity, and anticipation.

### Build The Artifact

- Export a ritual calendar with names, owners, cadence, and guardrails.
- Include one lightweight pilot for each new ritual.
- Make it easy to stop or retire rituals that stop serving the audience.

### Mac Product Shape

- Prefer `MenuBarExtra` with these primary actions:
  - `Set Cadence`
  - `Draft Rituals`
  - `View Calendar`
  - `Export Plan`
- Keep the popover between 320 pt and 380 pt wide with grouped sections, clear source status, and a strong export action.
- Use a lightweight settings or history window only for source rules, saved exports, or weighting controls.

### Safety Boundaries

- Work only from public or user-authorized material.
- Do not assist with stalking, covert profiling, rumor laundering, harassment, or minors-focused manipulation.
- Do not recommend compulsive streak mechanics, guilt-driven participation, or emotionally coercive rituals.

## Example Prompts

- `Use $ritual-engine to turn this creator's weekly posting cadence into a ritual calendar with repeatable fan participation formats.`
- `Use $ritual-engine to design sustainable community rituals around this founder's product updates without making the audience feel manipulated.`

## Resources

- `references/product-spec.md`: product surface, SwiftUI layout, artifact template, icon direction, and first-run behavior.
