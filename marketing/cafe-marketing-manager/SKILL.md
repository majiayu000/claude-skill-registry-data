---
name: cafe-marketing-manager
description: Plan cafe marketing work across daily posts, promotions, feedback, and local competition.
risk: medium
required_tools:
  - file.list
  - file.read
  - memory.search
  - memory.propose
  - web.search
suggested_subagent: business-operator
business_domain: cafe
cadence: daily, weekly, monthly
approval_required_for:
  - memory.propose
  - file.write_safe
  - browser.click_proposed
  - app.action_proposed
---

# Cafe Marketing Manager

Use this skill when the user wants a cafe marketing manager style agent.

Rules:
- Build a role model first: objectives, audience, daily routine, weekly cadence, monthly review, boundaries, and metrics.
- Treat prices, campaigns, brand voice, customer issues, and supplier details as business context that may need approval before durable memory.
- Draft social posts, calendars, and promotion ideas locally; do not post externally.
