---
name: lore-drop-planner
description: "Plan episodic reveals, callbacks, teasers, and payoff arcs for personality-led brands, then output a lore release schedule. Use when Codex needs to structure anticipation and payoff around a creator or founder's ongoing world-building."
---

# Lore Drop Planner

Use this skill when you need a sequence of reveals and callbacks that builds anticipation without becoming confusing or manipulative.

Default product shape: a compact macOS `MenuBarExtra` utility with a source-aware popover for canon loading, drop sequencing, and schedule export and an optional settings/history window.

## Quick Start

1. Confirm the subject, target audience, and source window.
2. Gather only public or user-authorized material into a working set.
3. Produce a `lore-release-schedule` with the default sections below.
4. If the user wants a richer product concept, keep it menu bar first and native to SwiftUI.

## Accepted Inputs

- canon maps, campaign notes, or world-building references
- existing content calendar, launch windows, and major dates
- notes on unresolved mysteries, recurring props, or teased payoffs
- constraints around what must stay private, fictional, or undisclosed

## Output Artifact

Primary artifact: `lore-release-schedule`

Default sections:
- Arc summary and audience promise
- Drop sequence with reveal, teaser, callback, and payoff beats
- Cross-format notes for posts, lives, clips, merch, or events
- Confusion risks and guardrails for clarity
- Review points for when to accelerate, pause, or retire the arc

## Workflow

### Gather Sources

- Inventory open loops, existing callbacks, and promised payoffs.
- Map the calendar constraints before inventing new reveals.
- Separate actual lore from campaign noise so the schedule stays coherent.

### Distill Signal

- Group open threads into clear arcs with distinct emotional roles.
- Reject reveals that only work through confusion or false alarm.
- Score each beat for anticipation, clarity, and payoff potential.

### Build The Artifact

- Export a release schedule with cadence, format, and audience takeaway.
- Show where a callback refreshes memory before a bigger reveal.
- Add pause or reset rules if the arc starts feeling convoluted or overhyped.

### Mac Product Shape

- Prefer `MenuBarExtra` with these primary actions:
  - `Load Canon`
  - `Sequence Drops`
  - `Review Timeline`
  - `Export Schedule`
- Keep the popover between 320 pt and 380 pt wide with grouped sections, clear source status, and a strong export action.
- Use a lightweight settings or history window only for source rules, saved exports, or weighting controls.

### Safety Boundaries

- Work only from public or user-authorized material.
- Do not assist with stalking, covert profiling, rumor laundering, harassment, or minors-focused manipulation.
- Do not rely on fake emergencies, manipulative ambiguity, or unresolved bait designed only to keep audiences anxious.

## Example Prompts

- `Use $lore-drop-planner to sequence this artist's callbacks and reveals across the next six weeks and export a lore release schedule.`
- `Use $lore-drop-planner to turn these founder-brand open loops into a clean teaser and payoff schedule that stays easy to follow.`

## Resources

- `references/product-spec.md`: product surface, SwiftUI layout, artifact template, icon direction, and first-run behavior.
