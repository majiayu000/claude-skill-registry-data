---
name: practice-station-redesign
description: This skill should be used when redesigning golf practice station pages (driving range, short game, putting) to be goal-oriented and mobile-friendly. It provides the page structure, style patterns, and Trackman exercise templates established in the Off the Tee station redesign.
---

# Practice Station Redesign

This skill transforms drill-focused practice pages into goal-oriented, mobile-first stations.

## Core Philosophy

Old station pages had too many accordions and drills - users don't use them because they lack clear purpose. The new approach focuses on:

1. 2-3 essential shots to master (not 10 drills)
2. Clear purpose for each shot (when to use it)
3. Trackman exercises with specific metrics
4. Mobile-first cards (one card = one screen scroll)

## Page Structure

To redesign a practice station, follow this structure:

### 1. Hero Section

```html
<div class="strategy-hero">
    <div class="strategy-hero__title">[MAIN GOAL]</div>
    <div class="strategy-hero__subtitle">[Summary of shots to master]</div>
</div>
```

### 2. Overview Card

Create a quick reference table showing the 2-3 shots and when to use each.

### 3. Shot Cards (one section per essential shot)

Each shot requires 4 cards:
- **When to Use** - situations and conditions
- **Pre-Shot Routine** - numbered steps for consistency
- **Setup Keys** - table format for quick mobile scanning
- **Swing Dynamic** - power %, tempo, motion, finish

### 4. Trackman Practice (2-3 exercises)

Each exercise card uses this format:

```html
<table class="table table-sm mb-3">
    <tr><td><strong>Mode</strong></td><td>[Practice / Games → GameName]</td></tr>
    <tr><td><strong>Balls</strong></td><td>[10 shots / Knockout format]</td></tr>
    <tr><td><strong>Watch</strong></td><td>[Key metric to track]</td></tr>
</table>
```

Include: How To steps (ordered list) + Success criteria (alert-success)

### 5. Quick Fixes (accordion)

Keep troubleshooting content in accordions - users tap when they have a specific problem.

### 6. Strategy Link

Add a card linking to strategy.html for level-specific goals.

## Style Patterns

**Do:**
- Full-width Bootstrap cards (`class="card mb-3"`)
- Tables for setup keys and Trackman specs
- Ordered lists for routines and how-to steps
- `alert-info` for tips, `alert-success` for success criteria
- Keep Quick Fixes as accordion

**Avoid:**
- Accordions for main content (too hidden)
- "Goals by Level" accordions (link to strategy page instead)
- Drill libraries (keep focused on 2-3 shots)
- Nested accordions inside cards

## Trackman Exercises

Available modes for exercises:
- **Practice Mode**: Track Lateral Dispersion, use Jellybean view
- **Games → Bullseye**: Accuracy training, closest to target
- **Games → On the Edge**: Distance control, don't go over target
- **Games → Capture the Flag**: Accuracy with strategy

Each exercise needs: Purpose, Mode path, Metric to watch, Success criteria.

## Reference Files

To implement this skill, consult these files:

- `docs/station-1-off-the-tee.html` - Completed exemplar (see references/)
- `docs/strategy.html` - Card patterns and tables
- `docs/rules.html` - Quick-ref card styling
- `docs/bootstrap-custom.css` - CSS classes (.quick-fixes, .strategy-hero)

For content, pull from:
- `docs/driver.html`, `docs/irons.html`, etc. - Technical setup info
- `channels/golfdistillery/` - Source material
- `channels/golfsidekick/` - Scoring methodology

## Before Starting

Ask the user:
1. What are the 2-3 essential shots for this station?
2. What is the main goal? (accuracy, distance control, consistency)
3. What Trackman metrics matter most for this station?
