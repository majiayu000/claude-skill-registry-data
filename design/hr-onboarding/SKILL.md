---
name: hr-onboarding
description: |
  Employee onboarding checklist and welcome page with progress tracking,
  team introductions, and resource links. Use for "onboarding", "welcome",
  "new hire", "HR portal".
triggers:
  - "onboarding"
  - "new hire"
  - "welcome page"
  - "hr portal"
  - "employee onboarding"
df:
  mode: prototype
  platform: desktop
  scenario: internal
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
---

# HR Onboarding Skill

Produce an employee onboarding page.

## Layout
- **Welcome hero**: "Welcome to [Company]" + first-day message.
- **Progress tracker**: 4–5 steps (Offer signed → Setup → Meet team →
  First project → 30-day check-in). Visual as connected dots/bars.
- **Checklist**: tasks with checkboxes, owner, due date.
- **Team grid**: 4–6 teammate cards (avatar, name, role, fun fact).
- **Resources**: link cards to handbook, tools, Slack channels.

## Rules
- Friendly, warm tone. Not corporate-cold.
- Progress tracker shows current step highlighted.
- Completed steps: checkmark + muted color.
- `data-df-id` on each step and task.

## Output
Single `index.html`, inline CSS.
