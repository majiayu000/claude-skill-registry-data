---
name: social-calendar
description: Draft a governed social content calendar without posting externally.
risk: medium
required_tools:
  - memory.search
  - file.read
  - file.diff
  - web.search
suggested_subagent: business-operator
business_domain: marketing
cadence: weekly, monthly
approval_required_for:
  - file.write_safe
  - app.action_proposed
---

# Social Calendar

Use this skill when the user wants a content calendar for a business or personal brand.

Rules:
- Understand audience, offers, events, constraints, and brand tone before drafting.
- Mark assumptions clearly.
- Do not submit, schedule, or publish posts.
