---
name: meeting-notes
description: |
  Structured meeting notes with attendees, agenda, decisions, and action items.
  Use for "meeting notes", "standup", "retrospective", "sync notes".
triggers:
  - "meeting notes"
  - "standup notes"
  - "retrospective"
  - "sync"
  - "meeting minutes"
df:
  mode: document
  platform: desktop
  scenario: productivity
  preview:
    type: html
    entry: index.html
  design_system:
    requires: false
---

# Meeting Notes Skill

Produce a clean meeting notes document.

## Sections
1. **Meta bar** — meeting title, date, duration, facilitator.
2. **Attendees** — avatar circles + names, status indicators (present/remote/late).
3. **Agenda** — numbered list with time boxes.
4. **Notes** — per-agenda-item notes, free-form bullets.
5. **Decisions** — highlighted box with ✓ prefix.
6. **Action items** — table: task | owner | due | status.
7. **Next meeting** — date + proposed topics.

## Rules
- Clean, scan-friendly. No decorative elements.
- Action items table: status as colored dots (green=done, yellow=in progress,
  red=blocked).
- `data-df-id` on each section.

## Output
Single `index.html`, inline CSS.
